#!/usr/bin/env python3
"""FIDO spec catalog + on-demand downloader (Python stdlib only).

The skill ships only summaries and tables of contents. This script looks documents
up in the catalog and downloads the official file from fidoalliance.org into a
local cache when the user needs the actual text.

Commands
  list     [--family F] [--all-versions]      list documents (latest version by default)
  versions DOC                                 every catalogued version of a document
  search   TERMS... [--family F] [--all-versions]
                                               search titles, summaries and section titles
  show     DOC [--version V]                   print the catalog page (summary + TOC)
  fetch    DOC [--version V]                   download the official file, verify sha256, print path
  toc      DOC [--version V]                   section list of the downloaded file (with anchors)
  section  DOC ANCHOR [--version V]            plain text of one section (downloads if needed)
  text     DOC [--version V]                   write the whole document as plain text, print path

DOC is a doc_id (e.g. fido-client-to-authenticator-protocol) or a unique part of one
(e.g. "ctap", "metadata-statement"). V is a version like 2.2; add "-errata" for an
errata edition (2.1-errata). Without --version the latest PS edition is used.

Cache: $FIDO_SPEC_CACHE or ~/.cache/fido-certification
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CATALOG = SKILL / "catalog"
CACHE = Path(os.environ.get("FIDO_SPEC_CACHE", Path.home() / ".cache" / "fido-certification"))
UA = "fido-certification-skill/0.1"
ALIASES = {
    "ctap": "fido-client-to-authenticator-protocol",
    "ctap2": "fido-client-to-authenticator-protocol",
    "fido2": "fido-client-to-authenticator-protocol",
    "mds": "fido-metadata-service",
    "metadata-statement": "fido-metadata-statement",
    "fdo": "fido-device-onboard",
    "cxf": "cxf",
    "registry": "fido-registry",
    "glossary": "fido-glossary",
    "security-ref": "fido-security-ref",
    "sr": "fido-authenticator-security-requirements",
    "security-requirements": "fido-authenticator-security-requirements",
    "acl": "fido-authenticator-allowed-cryptography-list",
    "aroe": "fido-authenticator-allowed-restricted-operating-environments-list",
    "biometric-requirements": "fido-biometrics-requirements",
    "bio": "fido-biometrics-requirements",
    "server-requirements": "fido-server-requirements",
}


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def load() -> dict:
    return json.loads((CATALOG / "catalog.json").read_text())


def vkey(d: dict):
    return (tuple(int(x) for x in d["version"].split(".")), d["date"], d["edition"] == "ps-errata")


def resolve(cat: dict, doc: str, version: str | None) -> dict:
    docs = cat["documents"]
    q = ALIASES.get(doc.lower(), doc.lower())
    ids = sorted({d["doc_id"] for d in docs})
    if q in ids:
        match = q
    else:
        cands = [i for i in ids if q in i and not i.endswith("errata-list")] or [i for i in ids if q in i]
        if len(cands) != 1:
            die(f"'{doc}' matches {len(cands)} documents: {', '.join(cands) or '-'}. Use a doc_id from `list`.")
        match = cands[0]
    vers = sorted((d for d in docs if d["doc_id"] == match), key=vkey)
    if not version:
        return vers[-1]
    want_errata = version.endswith("-errata")
    v = version.removesuffix("-errata").lstrip("v")
    hits = [d for d in vers if d["version"] == v and (d["edition"] == "ps-errata") == want_errata]
    if not hits:
        hits = [d for d in vers if d["version"] == v]
    if not hits:
        die(f"{match} has no catalogued version {version}. Available: "
            + ", ".join(sorted({d['version'] + ('-errata' if d['edition'] == 'ps-errata' else '') for d in vers})))
    return hits[-1]


def label(d: dict) -> str:
    ed = {"ps": "", "current": ""}.get(d["edition"], f" [{d['edition']}]")
    latest = " (latest)" if d["latest"] else ""
    status = f"  {{{d['status']}}}" if d.get("status") else ""
    return f"{d['doc_id']}  v{d['version']}{ed}  {d.get('maturity', '')}  {d['date']}{latest}{status}"


# ------------------------------------------------------------------ download


CF_INJECT = re.compile(rb"<script>\(function\(\)\{function c\(\).*?</script>", re.S)


def content_sha256(data: bytes) -> str:
    """sha256 with the per-request Cloudflare beacon script removed (it changes on every download)."""
    return hashlib.sha256(CF_INJECT.sub(b"", data)).hexdigest()


def local_path(d: dict) -> Path:
    u = urllib.parse.urlsplit(d["url"])
    path = u.path + ("index.html" if u.path.endswith("/") else "")
    return CACHE / u.netloc / urllib.parse.unquote(path).lstrip("/")


def fetch(d: dict, quiet: bool = False) -> Path:
    p = local_path(d)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(d["url"], headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
        except Exception as e:  # network blocked, 403, offline ...
            die(f"download failed for {d['url']}: {e}\n"
                f"Ask the user to download it in a browser and save it as {p}")
        tmp = p.with_suffix(p.suffix + ".part")
        tmp.write_bytes(data)
        tmp.rename(p)
    digest = content_sha256(p.read_bytes())
    if digest != d["sha256"] and not quiet:
        print(f"warning: sha256 differs from the catalog snapshot ({d['sha256'][:12]}… vs {digest[:12]}…). "
              "FIDO may have re-published the file; treat the catalog TOC as approximate.", file=sys.stderr)
    return p


# ------------------------------------------------------------------ HTML -> text


BLOCK = {"p", "div", "section", "li", "tr", "pre", "table", "dl", "dt", "dd", "blockquote", "figure",
         "figcaption", "br", "ul", "ol", "h1", "h6"}
HEAD = {"h2": 2, "h3": 3, "h4": 4, "h5": 5}


class ToText(HTMLParser):
    """Spec HTML -> text. Headings become `@@L|anchor|title` marker lines."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.sec_ids: list[str | None] = []
        self.head: list | None = None  # [level, id, text]
        self.selflink = 0
        self.nav_depth = 0
        self.nav_skip_at: int | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):  # not <head>: Bikeshed omits the optional </head>
            self.skip += 1
            return
        if tag == "nav":  # the built-in table of contents (ReSpec / Bikeshed) is noise here
            self.nav_depth += 1
            if self.nav_skip_at is None and (a.get("id") == "toc" or a.get("data-fill-with") == "table-of-contents"):
                self.nav_skip_at = self.nav_depth
        if self.nav_skip_at is not None:
            return
        if self.skip:
            return
        if tag == "section":
            self.sec_ids.append(a.get("id"))
        if tag in HEAD and self.head is None:
            self.head = [HEAD[tag], a.get("id") or (self.sec_ids[-1] if self.sec_ids else ""), ""]
        elif self.head is not None and tag == "a" and "self-link" in (a.get("class") or ""):
            self.selflink += 1
        elif tag in BLOCK:
            self.out.append("\n")
        if tag == "li":
            self.out.append("- ")
        if tag in ("td", "th"):
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "nav":
            if self.nav_skip_at == self.nav_depth:
                self.nav_skip_at = None
            self.nav_depth = max(0, self.nav_depth - 1)
            return
        if self.nav_skip_at is not None:
            return
        if tag == "section" and self.sec_ids:
            self.sec_ids.pop()
        if self.head is not None and tag == "a" and self.selflink:
            self.selflink -= 1
        elif self.head is not None and tag in HEAD and HEAD[tag] == self.head[0]:
            title = re.sub(r"\s+", " ", self.head[2]).replace("¶", "").strip()
            self.out.append(f"\n@@{self.head[0]}|{self.head[1] or ''}|{title}\n")
            self.head = None
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip or self.nav_skip_at is not None:
            return
        if self.head is not None:
            if not self.selflink:
                self.head[2] += data
            return
        self.out.append(data)


def html_text(p: Path) -> str:
    cached = p.with_suffix(".marked.txt")
    if cached.exists() and cached.stat().st_mtime >= p.stat().st_mtime:
        return cached.read_text()
    parser = ToText()
    raw = p.read_text(errors="replace")
    parser.feed(raw)
    text = "".join(parser.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"^- \s+", "- ", text, flags=re.M)  # "<li>\n<p>text" -> "- text"
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    cached.write_text(text)
    return text


def headings(text: str) -> list[tuple[int, str, str, int]]:
    return [(int(m.group(1)), m.group(2), m.group(3), m.start())
            for m in re.finditer(r"^@@(\d)\|([^|]*)\|(.*)$", text, re.M)]


def pretty(text: str) -> str:
    return re.sub(r"^@@(\d)\|([^|]*)\|(.*)$",
                  lambda m: "#" * int(m.group(1)) + f" {m.group(3)}" + (f"  {{#{m.group(2)}}}" if m.group(2) else ""),
                  text, flags=re.M)


def pdf_text(p: Path) -> Path | None:
    """PDF -> text with page markers, using pypdf if it is installed (optional)."""
    out = p.with_suffix(".txt")
    if out.exists():
        return out
    try:
        from pypdf import PdfReader  # optional dependency
    except ImportError:
        return None
    r = PdfReader(str(p))
    out.write_text("\n".join(f"\n[page {i + 1}]\n{pg.extract_text() or ''}" for i, pg in enumerate(r.pages)))
    return out


def need_html(d: dict) -> None:
    if d["format"] != "html":
        p = fetch(d)
        t = pdf_text(p)
        if t:
            die(f"{d['doc_id']} v{d['version']} is only published as PDF. Plain text with [page N] markers:\n{t}\n"
                "Search it with grep and read the pages you need.")
        die(f"{d['doc_id']} v{d['version']} is only published as PDF. Downloaded to:\n{p}\n"
            "Open it with the Read tool (pages parameter). If that fails, run `pip install pypdf` and retry "
            "this command to get a text version.")


# ------------------------------------------------------------------ commands


def cmd_list(cat, a):
    docs = [d for d in cat["documents"] if (a.all_versions or d["latest"]) and (not a.family or d["family"] == a.family)]
    fam = None
    for d in sorted(docs, key=lambda d: (d["family"], d["doc_id"], vkey(d))):
        if d["family"] != fam:
            fam = d["family"]
            print(f"\n## {fam} — {cat['families'][fam]}")
        print(f"- {label(d)} — {d['title']}")


def cmd_versions(cat, a):
    d0 = resolve(cat, a.doc, None)
    for d in sorted((x for x in cat["documents"] if x["doc_id"] == d0["doc_id"]), key=vkey):
        print(f"- {label(d)}  {d['format']}  {d['url']}")


def cmd_search(cat, a):
    terms = [t.lower() for t in a.terms]
    rows = []
    for d in cat["documents"]:
        if (not a.all_versions and not d["latest"]) or (a.family and d["family"] != a.family):
            continue
        page = (CATALOG / d["page"]).read_text()
        body = page.split("\n---\n", 1)[-1]
        summary, _, toc = body.partition("## Table of contents")
        score = 0
        hay_title = d["title"].lower() + " " + d["doc_id"]
        score += sum(5 for t in terms if t in hay_title)
        score += sum(2 * summary.lower().count(t) for t in terms)
        hits = [l.strip() for l in toc.splitlines() if l.strip().startswith("-") and all(t in l.lower() for t in terms)]
        score += 3 * len(hits)
        if score:
            rows.append((score, d, hits))
    if not rows:
        print("no matches in titles, summaries or section titles")
    for score, d, hits in sorted(rows, key=lambda r: -r[0])[:12]:
        print(f"\n{label(d)} — {d['title']}  (score {score})")
        for h in hits[:8]:
            print(f"    {h}")


def cmd_show(cat, a):
    d = resolve(cat, a.doc, a.version)
    print((CATALOG / d["page"]).read_text())


def cmd_fetch(cat, a):
    d = resolve(cat, a.doc, a.version)
    p = fetch(d)
    print(f"{label(d)}\n{p}")


def cmd_toc(cat, a):
    d = resolve(cat, a.doc, a.version)
    need_html(d)
    for lvl, anchor, title, _ in headings(html_text(fetch(d))):
        print(f"{'  ' * (lvl - 2)}- {title}" + (f"  #{anchor}" if anchor else ""))


def cmd_section(cat, a):
    d = resolve(cat, a.doc, a.version)
    need_html(d)
    text = html_text(fetch(d, quiet=True))
    hs = headings(text)
    want = a.anchor.lstrip("#")
    idx = next((i for i, h in enumerate(hs) if h[1] == want), None)
    if idx is None:  # allow section number or title fragment
        idx = next((i for i, h in enumerate(hs) if h[2].lower().startswith(want.lower() + ".")
                    or h[2].lower().startswith(want.lower() + " ")), None)
    if idx is None:
        idx = next((i for i, h in enumerate(hs) if want.lower() in h[2].lower()), None)
    if idx is None:
        die(f"no section '{a.anchor}' in {d['doc_id']} v{d['version']}. Run `toc` to list anchors.")
    lvl, start = hs[idx][0], hs[idx][3]
    end = next((h[3] for h in hs[idx + 1:] if h[0] <= lvl), len(text))
    chunk = pretty(text[start:end]).strip()
    limit = a.max_chars
    print(f"[{label(d)} — {d['url']}#{hs[idx][1]}]\n")
    print(chunk[:limit] + (f"\n\n… truncated at {limit} chars; request a subsection or raise --max-chars"
                          if len(chunk) > limit else ""))


def cmd_text(cat, a):
    d = resolve(cat, a.doc, a.version)
    if d["format"] == "pdf" and (t := pdf_text(fetch(d))):
        print(t)
        return
    need_html(d)
    p = fetch(d)
    out = p.with_suffix(".txt")
    out.write_text(f"{label(d)}\n{d['url']}\n\n" + pretty(html_text(p)))
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--family"); s.add_argument("--all-versions", action="store_true")
    s = sub.add_parser("versions"); s.add_argument("doc")
    s = sub.add_parser("search"); s.add_argument("terms", nargs="+"); s.add_argument("--family")
    s.add_argument("--all-versions", action="store_true")
    for name in ("show", "fetch", "toc", "text"):
        s = sub.add_parser(name); s.add_argument("doc"); s.add_argument("--version")
    s = sub.add_parser("section"); s.add_argument("doc"); s.add_argument("anchor"); s.add_argument("--version")
    s.add_argument("--max-chars", type=int, default=20000)
    a = ap.parse_args()
    globals()[f"cmd_{a.cmd}"](load(), a)


if __name__ == "__main__":
    main()
