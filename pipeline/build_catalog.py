#!/usr/bin/env python3
"""Build the distributable catalog from the crawled FIDO spec index.

Only Proposed Standard (PS) documents are included: any file whose path carries a
"-ps-" maturity tag (this also covers the official "ps-errata" editions).

For every PS document version it:
  1. picks the best source file (HTML preferred, PDF otherwise),
  2. downloads it into pipeline/.cache/ (never committed, never distributed),
  3. records sha256 + size so end-user downloads can be verified,
  4. extracts the table of contents (section numbers, titles, anchors),
  5. writes catalog/catalog.json and catalog/docs/<family>/<doc_id>/<version>.md

Summaries are written afterwards (see pipeline/README.md); this script keeps any
existing "## Summary" block when it regenerates a document page.

Usage: python3 pipeline/build_catalog.py [--offline]
  --offline  reuse files already in pipeline/.cache, download nothing new
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "pipeline/out/specs-index.json"
CACHE = ROOT / "pipeline/.cache"
CATALOG = ROOT / "fido-certification/catalog"
UA = "fido-certification-skill/0.1 (catalog builder)"
BASE = "https://fidoalliance.org/specs/"

# ---------------------------------------------------------------- classification

FAMILIES = [
    # (family id, family title, predicate on doc name)
    ("ctap", "FIDO2 Client to Authenticator Protocol (CTAP)", lambda n: n.startswith("fido-client-to-authenticator-protocol")),
    ("mds", "Metadata Service and Metadata Statements", lambda n: "metadata" in n),
    ("uaf", "FIDO UAF (Universal Authentication Framework)", lambda n: n.startswith("fido-uaf")),
    ("u2f", "FIDO U2F (Universal 2nd Factor)", lambda n: n.startswith("fido-u2f")),
    ("fdo", "FIDO Device Onboard (FDO)", lambda n: n.startswith(("fido-device-onboard", "pv4fdo"))),
    ("cx", "Credential Exchange (CXF)", lambda n: n.startswith("cxf")),
    ("common", "Common specifications (shared by UAF, U2F, FIDO2)", lambda n: True),
]

SKIP = re.compile(r"(\.zip$|COMPLETE|-cn\.|\.h-v|u2f\.h|u2f_hid\.h|\.original$)", re.I)

# name[-vX.Y][-ps][-errata]-YYYYMMDD   (FDO uses Name-PS-vX.Y-YYYYMMDD)
NAME_RE = re.compile(
    r"^(?P<name>.+?)(?:-v(?P<ver>\d+(?:\.\d+)*))?(?P<ps>-ps)?(?P<errata>-errata)?-(?P<date>\d{8})$", re.I
)
FDO_RE = re.compile(r"^(?P<name>FIDO-Device-Onboard)-PS-v(?P<ver>[\d.]+)-(?P<date>\d{8})$", re.I)
DIR_VER = re.compile(r"-v(\d+(?:\.\d+)*)-ps-", re.I)


# Scope decisions (approved by the maintainer, 2026-11-16):
#  - Proposed Standards only
#  - U2F: 1.2 only (1.0 and 1.1 are sunset from FIDO certification)
#  - UAF: 1.1 and higher (1.0 is sunset)
#  - fido-v2.0-ps-20150904/ (2015 W3C submission) and fido-v2.0-ps-20170927/ (pre-final CTAP 2.0)
#    are excluded entirely
#  - MDS / Metadata Statement: 3.1.1 only (approved 2026-11-16)
EXCLUDE_DIRS = ("fido-v2.0-ps-20150904/", "fido-v2.0-ps-20170927/")
MIN_VERSION = {"fido-metadata-service": "3.1.1", "fido-metadata-statement": "3.1.1"}
CURATED = ROOT / "pipeline/certification_sources.json"


def in_scope(path: str) -> bool:
    p = path.lower()
    if p.startswith(EXCLUDE_DIRS):
        return False
    if "/" not in p:  # loose 2014/2015 PDFs at the archive root are the U2F 1.0 release
        return False
    top = p.split("/", 1)[0]
    if top.startswith("fido-u2f-") and not top.startswith("fido-u2f-v1.2-"):
        return False
    if top.startswith(("fido-uaf-v1.0-", "uaf-v1.0-")):
        return False
    return True


def classify(path: str) -> dict | None:
    if "-ps-" not in path.lower() or SKIP.search(path) or not in_scope(path):
        return None
    fname = path.rsplit("/", 1)[-1]
    stem, _, ext = fname.rpartition(".")
    if ext.lower() not in ("html", "pdf"):
        return None
    m = FDO_RE.match(stem) or NAME_RE.match(stem)
    if not m:
        print(f"skip (unparsed name): {path}", file=sys.stderr)
        return None
    name = m.group("name").lower()
    ver = m.group("ver")
    if not ver:  # 2014/2015 files carry the version only in their folder name
        dm = DIR_VER.search(path)
        ver = dm.group(1) if dm else "1.0"
    gd = m.groupdict()
    errata = bool(gd.get("errata"))
    is_ps_file = bool(gd.get("ps")) or bool(FDO_RE.match(stem))
    # "fido-client-to-authenticator-protocol-v2.1-errata-20220621" is the errata *list*,
    # "...-v2.1-ps-errata-20220621" is the PS edition with errata applied.
    if errata and not is_ps_file:
        name = name + "-errata-list"
        edition = "errata-list"
    elif errata:
        edition = "ps-errata"
    else:
        edition = "ps"
    if name in MIN_VERSION and version_key(ver) < version_key(MIN_VERSION[name]):
        return None
    family = next(f for f, _, pred in FAMILIES if pred(name))
    date = m.group("date")
    return {
        "family": family,
        "doc_id": name,
        "version": ver,
        "edition": edition,
        "date": f"{date[:4]}-{date[4:6]}-{date[6:]}",
        "format": ext.lower(),
        "path": path,
        "url": BASE + path,
        "maturity": "Proposed Standard",
        "status": "",
    }


# ---------------------------------------------------------------- download

CF_INJECT = re.compile(rb"<script>\(function\(\)\{function c\(\).*?</script>", re.S)


def content_sha256(data: bytes) -> str:
    """sha256 with the per-request Cloudflare beacon script removed (it changes on every download)."""
    return hashlib.sha256(CF_INJECT.sub(b"", data)).hexdigest()


def download(url: str, dest: Path, offline: bool) -> bytes | None:
    if dest.exists():
        return dest.read_bytes()
    if offline:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    dest.write_bytes(data)
    time.sleep(0.3)
    return data


# ---------------------------------------------------------------- TOC extraction (HTML)


class SpecParser(HTMLParser):
    """Collects h2-h5 headings (with anchor ids) plus title/abstract/status text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.headings: list[dict] = []
        self._in_title = False
        self._h: dict | None = None
        self._section_ids: list[str | None] = []
        self._capture: str | None = None  # "abstract" | "sotd"
        self._capture_depth = 0
        self.abstract = ""
        self.sotd = ""
        self._skip_depth = 0  # inside <a class="self-link"> etc.

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "section":
            self._section_ids.append(a.get("id"))
            if a.get("id") in ("abstract", "sotd") and not self._capture:
                self._capture, self._capture_depth = a["id"], len(self._section_ids)
        if tag in ("h2", "h3", "h4", "h5") and self._h is None:
            sid = a.get("id") or (self._section_ids[-1] if self._section_ids else None)
            self._h = {"level": int(tag[1]), "id": sid, "text": ""}
        if self._h is not None and tag == "a" and "self-link" in (a.get("class") or ""):
            self._skip_depth += 1
        if tag == "div" and a.get("id") in ("abstract", "sotd") and not self._capture:
            self._capture, self._capture_depth = a["id"], -1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("h2", "h3", "h4", "h5") and self._h is not None and tag == f"h{self._h['level']}":
            text = re.sub(r"\s+", " ", self._h["text"]).strip().replace("¶", "").strip()
            if text:
                self._h["text"] = text
                self.headings.append(self._h)
            self._h = None
        if tag == "a" and self._skip_depth:
            self._skip_depth -= 1
        if tag == "section":
            if self._capture and self._capture_depth == len(self._section_ids):
                self._capture = None
            if self._section_ids:
                self._section_ids.pop()
        if tag == "div" and self._capture and self._capture_depth == -1:
            self._capture = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h is not None and not self._skip_depth:
            self._h["text"] += data
        if self._capture == "abstract":
            self.abstract += data
        elif self._capture == "sotd":
            self.sotd += data


def parse_html(data: bytes) -> dict:
    p = SpecParser()
    p.feed(data.decode("utf-8", "replace"))
    heads = [h for h in p.headings
             if h["text"].lower() not in ("table of contents", "contents") and h.get("id") != "subtitle"]
    return {
        "title": re.sub(r"\s+", " ", p.title).strip(),
        "abstract": re.sub(r"\s+", " ", p.abstract).strip(),
        "headings": heads,
    }


# ---------------------------------------------------------------- TOC extraction (PDF, optional)


def parse_pdf(path: Path) -> dict:
    """Use the PDF outline (bookmarks) when pypdf is available in pipeline/.venv."""
    venv_py = ROOT / "pipeline/.venv/bin/python"
    if not venv_py.exists():
        return {"title": "", "abstract": "", "headings": []}
    code = r"""
import json, sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
out = []
def walk(items, level):
    for it in items:
        if isinstance(it, list):
            walk(it, level + 1)
        else:
            try: page = r.get_destination_page_number(it) + 1
            except Exception: page = None
            out.append({"level": level, "text": it.title.strip(), "page": page})
walk(r.outline, 2)
title = (r.metadata.title if r.metadata else "") or ""
if not out:
    # no bookmarks: read the printed "Table of Contents" (2014/2015 ReSpec PDF exports)
    import re
    text = "\n".join((r.pages[i].extract_text() or "") for i in range(min(6, len(r.pages))))
    title = title or text.strip().splitlines()[0].strip()
    toc_at = text.find("Table of Contents")
    if toc_at >= 0:
        lines = [l.strip() for l in text[toc_at:].splitlines()[1:]]
        entry = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(\S.*)$")
        first = None
        for l in lines:
            m = entry.match(l)
            if not m:
                if out and not l:
                    continue
                if out and not entry.match(l) and len(out) > 2 and l and not l[0].isdigit():
                    # wrapped title line or end of TOC; stop at body text
                    if len(l) > 60:
                        break
                    out[-1]["text"] += " " + l
                continue
            if first is not None and l == first:
                break  # body starts with the first heading again
            first = first or l
            num = m.group(1)
            out.append({"level": 2 + num.count("."), "text": num + ". " + m.group(2).strip(), "page": None})
print(json.dumps({"title": title, "headings": out}))
"""
    res = subprocess.run([str(venv_py), "-I", "-c", code, str(path)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"warn: pdf outline failed for {path.name}: {res.stderr[-300:]}", file=sys.stderr)
        return {"title": "", "abstract": "", "headings": []}
    d = json.loads(res.stdout)
    d["abstract"] = ""
    return d


# ---------------------------------------------------------------- output


def version_key(v: str):
    return tuple(int(x) for x in v.split("."))


def page_path(doc: dict) -> Path:
    v = doc["version"] + ("-errata" if doc["edition"] == "ps-errata" else "")
    return CATALOG / "docs" / doc["family"] / doc["doc_id"] / f"{v}_{doc['date']}.md"


def existing_summary(p: Path) -> str | None:
    if not p.exists():
        return None
    m = re.search(r"(## Summary\n.*?)(?=\n## Table of contents)", p.read_text(), re.S)
    return m.group(1).rstrip() if m else None


def render(doc: dict, toc: dict) -> str:
    lines = [
        "---",
        f"doc_id: {doc['doc_id']}",
        f"title: {json.dumps(doc['title'])}",
        f"family: {doc['family']}",
        f"version: \"{doc['version']}\"",
        f"edition: {doc['edition']}",
        f"maturity: {doc['maturity']}",
        f"status: {json.dumps(doc['status'])}",
        f"date: {doc['date']}",
        f"url: {doc['url']}",
        f"format: {doc['format']}",
        f"sha256: {doc['sha256']}",
        f"bytes: {doc['bytes']}",
        f"latest_in_lineage: {str(doc['latest']).lower()}",
        "---",
        "",
        f"# {doc['title']}",
        "",
        f"Version {doc['version']} · {doc['maturity']}" + (" (errata edition)" if doc["edition"] == "ps-errata" else "")
        + f" · {doc['date']}" + (f" · **{doc['status']}**" if doc["status"] else "") + f" · [source]({doc['url']})",
        "",
    ]
    summary = existing_summary(page_path(doc))
    lines.append(summary or "## Summary\n\n_TODO: summary not written yet._")
    lines += ["", "## Table of contents", ""]
    if doc["format"] == "html":
        lines += ["Anchors are fragment ids in the source HTML: `<url>#<anchor>`.", ""]
    if not toc["headings"]:
        lines.append("_No machine-readable table of contents (PDF without outline)._")
    for h in toc["headings"]:
        indent = "  " * max(0, h["level"] - 2)
        if h.get("id") and doc["format"] == "html":
            lines.append(f"{indent}- {h['text']} `#{h['id']}`")
        elif h.get("page"):
            lines.append(f"{indent}- {h['text']} (p. {h['page']})")
        else:
            lines.append(f"{indent}- {h['text']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    offline = "--offline" in sys.argv
    files = json.loads(INDEX.read_text())
    cands = [c for f in files if (c := classify(f["path"]))]

    # one entry per (doc, version, edition, date); prefer HTML over PDF
    docs: dict[tuple, dict] = {}
    for c in cands:
        key = (c["doc_id"], c["version"], c["edition"], c["date"])
        rank = (c["format"] == "html", len(c["path"]))  # HTML first, then the suite-folder copy
        cur = docs.get(key)
        if cur is None or rank > (cur["format"] == "html", len(cur["path"])):
            docs[key] = c

    # curated certification documents (not PS-labelled, listed as ACTIVE by FIDO)
    curated = json.loads(CURATED.read_text())
    for c in curated["documents"]:
        u = urllib.parse.urlsplit(c["url"])
        fmt = "pdf" if u.path.lower().endswith(".pdf") else "html"
        path = u.netloc + u.path + ("index.html" if u.path.endswith("/") else "")
        docs[(c["doc_id"], c["version"], "current", c["date"])] = {
            **c, "edition": "current", "format": fmt, "path": path}

    # mark latest version per lineage (doc_id), errata edition beats plain PS of same version
    by_doc: dict[str, list] = {}
    for d in docs.values():
        by_doc.setdefault(d["doc_id"], []).append(d)
    for lst in by_doc.values():
        lst.sort(key=lambda d: (version_key(d["version"]), d["date"], d["edition"] == "ps-errata"))
        for d in lst:
            d["latest"] = d is lst[-1]

    out = []
    for d in sorted(docs.values(), key=lambda d: (d["family"], d["doc_id"], version_key(d["version"]), d["date"])):
        data = download(d["url"], CACHE / d["path"], offline)
        if data is None:
            print(f"missing (offline): {d['path']}", file=sys.stderr)
            continue
        d["sha256"] = content_sha256(data)
        d["bytes"] = len(data)
        toc = parse_html(data) if d["format"] == "html" else parse_pdf(CACHE / d["path"])
        title = html.unescape(toc["title"]) or d["doc_id"].replace("-", " ").title()
        d["title"] = re.sub(r"\s*\(?(Proposed Standard|PS)\)?\s*$", "", title).strip()
        d["sections"] = len(toc["headings"])
        d["page"] = str(page_path(d).relative_to(CATALOG))
        p = page_path(d)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render(d, toc))
        if toc.get("abstract"):
            (CACHE / "abstracts").mkdir(parents=True, exist_ok=True)
            (CACHE / "abstracts" / (d["page"].replace("/", "__") + ".txt")).write_text(toc["abstract"])
        out.append({k: d[k] for k in ("family", "doc_id", "title", "version", "edition", "maturity", "status",
                                      "date", "format", "url", "sha256", "bytes", "sections", "latest", "page")})
        print(f"ok  {d['family']:10} {d['doc_id']:50} v{d['version']:7} {d['edition']:10} {d['sections']:4} sections",
              file=sys.stderr)

    fam_titles = {f: t for f, t, _ in FAMILIES} | curated["families"]
    CATALOG.mkdir(exist_ok=True)
    (CATALOG / "catalog.json").write_text(json.dumps({
        "source": BASE,
        "maturity_filter": "Proposed Standards (scope rules in pipeline/build_catalog.py) + curated ACTIVE certification documents (pipeline/certification_sources.json)",
        "built": time.strftime("%Y-%m-%d"),
        "families": fam_titles,
        "documents": out,
    }, indent=1) + "\n")
    print(f"{len(out)} documents", file=sys.stderr)


if __name__ == "__main__":
    main()
