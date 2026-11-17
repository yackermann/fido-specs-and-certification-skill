#!/usr/bin/env python3
"""Build fido-spec-and-certification/catalog/resources/ (maintainer tool).

Sources:
  cert     fidoalliance.org certification pages, crawled from https://fidoalliance.org/fido-certification/
  ctt      https://github.com/fido-alliance/conformance-test-tools-resources (docs/ and README;
           the wiki says it moved to docs/, so it is not catalogued)
  interop  https://github.com/fido-alliance/fido2-interop-webapp
  issues   the conformance tools issue tracker (titles, labels, state, test IDs; bodies are fetched live)
  awesome  https://github.com/yackermann/awesome-webauthn (CC0: entries are shipped as data)

    python3 pipeline/build_resources.py            # fetch everything (about 70 web pages, ~12 GitHub API calls)
    python3 pipeline/build_resources.py --offline  # rebuild from pipeline/.cache

Existing summaries in the catalog pages are kept. Set GITHUB_TOKEN to raise the GitHub API limit.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "fido-spec-and-certification/scripts"))
import resources as R  # noqa: E402

OUT = ROOT / "fido-spec-and-certification/catalog/resources"
CACHE = ROOT / "pipeline/.cache/resources"
CATALOG = ROOT / "fido-spec-and-certification/catalog/catalog.json"
UA = "fido-spec-and-certification-skill/0.1 (resources builder)"

HUB = "https://fidoalliance.org/fido-certification/"
CERT_PREFIXES = ("/certification/", "/fido-certification/")
# Pages outside /certification/ that the hub links to and that belong to the programme.
CERT_EXTRA = {
    "/fido-certification-fees/", "/laboratory-overview/", "/accreditation-process-fees-biometrics/",
    "/certification-biometric-component-fido-biometric-certification-faq/", "/fdo-certification-process-overview/",
    "/fdo-functional-certification/", "/fido-user-authentication-certification-programs/", "/metadata/",
    "/metadata-legal-terms/", "/metadata-usage-terms-for-relying-parties-or-service-providers-2/",
    "/metadata-usage-terms-for-developers/", "/metadata-submission-terms-for-authenticator-vendors-2/",
    "/device-onboarding-overview/device-onboarding-certification/resource-documentation-fdo/",
    "/fido-certified-showcase/",
}
CERT_SKIP = ("password-recovery", "certification-account-request", "lab-accreditation-request",
             "certification-request-agreement/certification-request", "certified-logo-violation")
MIN_TEXT = 400  # pages with less extracted text (login stubs, empty forms) are dropped

REPOS = {
    "ctt": ("fido-alliance/conformance-test-tools-resources", "main"),
    "interop": ("fido-alliance/fido2-interop-webapp", "master"),
    "awesome": ("yackermann/awesome-webauthn", "main"),
}
TEST_ID = re.compile(r"\b(?:[A-Z][A-Za-z0-9]*-){1,6}[A-Za-z0-9]*\d+\b")
NOT_TESTS = {"Client-ASM", "FASM-API", "Client-Authenticator", "UAF-Client"}
TEST_PREFIX = re.compile(r"\b(?:Authr|Authnr|Server|Protocol|FASM|FC|Metadata|U2F|UAF|Client|ASM|Platform|MDS)"
                         r"(?:-[A-Za-z0-9]+)+")


def fetch(url: str, offline: bool, headers: dict | None = None) -> str:
    p = CACHE / "http" / re.sub(r"[^\w.-]+", "_", url)[:200]
    if p.exists() and (offline or p.stat().st_mtime > time.time() - 6 * 3600):
        return p.read_text(errors="replace")
    if offline:
        raise FileNotFoundError(url)
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read().decode("utf-8", errors="replace")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data)
    time.sleep(1)  # be polite
    return data


GENERIC = {"process-overview", "resource-documentation", "get-certified", "fido-certified-products",
           "accredited-labs", "overview"}


def page_id(path: str, used: set) -> str:
    parts = [x for x in path.strip("/").split("/") if x]
    pid = parts[-1] if parts else "index"
    i = 2
    if pid in GENERIC and len(parts) > 1:
        pid, i = "-".join(parts[-2:]), 3
    while pid in used and i <= len(parts):
        pid = "-".join(parts[-i:])
        i += 1
    used.add(pid)
    return pid


def crawl_cert(offline: bool) -> list[dict]:
    seen, queue, pages, used = set(), [(HUB, 0)], [], set()
    while queue:
        url, depth = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html = fetch(url, offline)
        except Exception as e:  # noqa: BLE001
            print(f"  skip {url}: {e}", file=sys.stderr)
            continue
        text = R.wp_text(html, url)
        title = re.sub(r"\s*\|\s*FIDO(?: Alliance)?\s*$", "", (re.search(r"<title>(.*?)</title>", html, re.S) or [None, url])[1]).strip()
        title = re.sub(r"&#0?38;|&amp;", "&", title).replace("&#8211;", "–").replace("&#8217;", "’")
        title = re.sub(r"\s*\|\s*FIDO(?: Alliance)?\s*$", "", title)
        sha = R.text_sha(text)
        dup = next((q for q in pages if q["sha256"] == sha), None)
        if dup:
            dup.setdefault("aliases", []).append(url)
            print(f"  duplicate of {dup['id']}: {url}", file=sys.stderr)
        elif len(text) >= MIN_TEXT:
            path = urllib.parse.urlsplit(url).path
            pages.append({"id": page_id(path, used), "source": "cert", "title": title, "url": url, "raw_url": url,
                          "kind": "html", "text": text, "sha256": sha})
        else:
            print(f"  drop (little text) {url}", file=sys.stderr)
        if depth >= 2:
            continue
        for href in re.findall(r'href="(https://fidoalliance\.org/[^"#?]*)"', html):
            path = urllib.parse.urlsplit(href).path
            if not path.endswith("/"):
                continue
            if any(s in path for s in CERT_SKIP):
                continue
            if path.startswith(CERT_PREFIXES) or path in CERT_EXTRA:
                queue.append((href, depth + 1))
    return pages


def clone(repo: str, branch: str, offline: bool) -> tuple[Path, str]:
    d = CACHE / "repos" / repo.replace("/", "__")
    if not offline:
        if d.exists():
            subprocess.run(["git", "-C", str(d), "fetch", "-q", "--depth", "1", "origin", branch], check=True)
            subprocess.run(["git", "-C", str(d), "reset", "-q", "--hard", f"origin/{branch}"], check=True)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", "--depth", "1", "-b", branch, f"https://github.com/{repo}.git", str(d)],
                           check=True)
    commit = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return d, commit


def md_title(text: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def repo_pages(offline: bool) -> tuple[list[dict], dict]:
    pages, used, commits = [], set(), {}
    for src in ("ctt", "interop"):
        repo, branch = REPOS[src]
        d, commits[src] = clone(repo, branch, offline)
        files = ["README.md"] + sorted(str(p.relative_to(d)) for p in (d / "docs").rglob("*.md")) if (d / "docs").exists() \
            else ["README.md"]
        for rel in files:
            text = (d / rel).read_text(errors="replace")
            if len(text.strip()) < 200:
                continue
            name = "docs-index" if rel == "docs/README.md" else \
                rel[:-3].replace("docs/", "").replace("/README", "").replace("/", "-")
            pid = f"{src}-{name}".lower() if src == "ctt" else "fido2-interop-webapp"
            used.add(pid)
            q = urllib.parse.quote(rel)
            fallback = f"{repo.split('/')[1]} {rel}"
            h1 = md_title(text, "")
            if src == "ctt" and rel != "README.md":
                where = rel[5:-3].replace("/README", "") if rel != "docs/README.md" else "index"
                title = f"Conformance tools docs: {where}" + (f" — {h1}" if h1 else "")
            elif src == "ctt":
                title = "Conformance test tools resources (repository README)"
            else:
                title = "FIDO2 interop web app (repository README)"
            pages.append({"id": pid, "source": src, "title": title,
                          "url": f"https://github.com/{repo}/blob/{branch}/{q}",
                          "raw_url": f"https://raw.githubusercontent.com/{repo}/{branch}/{q}",
                          "kind": "markdown", "text": text})
    return pages, commits


def issues(offline: bool) -> list[dict]:
    repo = REPOS["ctt"][0]
    out, page = [], 1
    hdr = R.gh_headers()
    while True:
        raw = fetch(f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}", offline, hdr)
        batch = json.loads(raw)
        if not batch:
            break
        for i in batch:
            if "pull_request" in i:
                continue
            tests = sorted({t for t in TEST_ID.findall(i["title"]) + TEST_PREFIX.findall(i["title"])
                            if len(t) >= 8 and not re.fullmatch(r"(?:CTAP|FIDO|U2F|UAF|ISO|v)[\d.-]+", t)
                            and t not in NOT_TESTS})
            out.append({"n": i["number"], "title": i["title"].strip(), "state": i["state"],
                        "labels": [l["name"] for l in i["labels"]], "created": i["created_at"],
                        "closed": i.get("closed_at"), "comments": i["comments"], "tests": tests})
        page += 1
    return sorted(out, key=lambda i: -i["n"])


def awesome(offline: bool) -> tuple[list[dict], str, str]:
    d, commit = clone(*REPOS["awesome"], offline)
    entries, cat = [], None
    readme = (d / "README.md").read_text()
    faq = readme.split("\n## FAQ", 1)[1].split("\n## ", 1)[0].strip() if "\n## FAQ" in readme else ""
    for line in (d / "README.md").read_text().splitlines():
        h = re.match(r"^##\s+(.+)", line)
        if h:
            cat = h.group(1).strip()
            continue
        if cat in (None, "Contents"):
            continue
        m = re.match(r"^\s*[-*]\s+((?:`[^`]+`\s*)*)\[([^\]]+)\]\(([^)]+)\)\s*(?:[-–—:]\s*)?(.*)$", line)
        if m:
            badges = re.findall(r"`([^`]+)`", m.group(1))
            entries.append({"category": cat, "name": m.group(2).strip(), "url": m.group(3).strip(),
                            "desc": m.group(4).strip(), "badges": badges})
        elif entries and line.startswith("  ") and line.strip() and entries[-1]["category"] == cat:
            entries[-1]["desc"] = (entries[-1]["desc"] + " " + line.strip()).strip()  # wrapped description
    return entries, commit, faq


def existing_summary(p: Path) -> str | None:
    if not p.exists():
        return None
    m = re.search(r"## Summary\n\n(.*?)\n\n## Outline", p.read_text(), re.S)
    return m.group(1) if m else None


def render(d: dict, spec_urls: dict, built: str) -> str:
    rel = f"pages/{d['source']}/{d['id']}.md"
    summary = existing_summary(OUT / rel) or "_TODO: summary not written yet._"
    fm = {"id": d["id"], "source": d["source"], "title": d["title"], "url": d["url"], "kind": d["kind"],
          "sha256": d["sha256"], "snapshot": built}
    out = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", "",
           f"# {d['title']}", "", f"Source: {d['url']} (live text: `python3 scripts/resources.py read {d['id']}`)", "",
           "## Summary", "", summary, "", "## Outline", ""]
    if d.get("aliases"):
        out[out.index("## Summary") - 1:out.index("## Summary") - 1] = ["Same content also at: " + ", ".join(d["aliases"]), ""]
    out += [f"{'  ' * max(0, h[0] - 1)}- {h[1]} `#{h[2]}`" for h in d["headings"]] or ["_(no headings)_"]
    if d["links"]:
        out += ["", "## Linked documents", ""]
        for text, u in d["links"]:
            ref = f" (catalogued: `{spec_urls[u]}`)" if u in spec_urls else ""
            out.append(f"- {text or u.rsplit('/', 1)[-1]}: {u}{ref}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    built = dt.date.today().isoformat()
    print("crawling certification pages…", file=sys.stderr)
    pages = crawl_cert(a.offline)
    print(f"  {len(pages)} cert pages", file=sys.stderr)
    rp, commits = repo_pages(a.offline)
    pages += rp
    spec_urls = {d["url"]: f"{d['doc_id']} {d['version']}" for d in json.loads(CATALOG.read_text())["documents"]}
    OUT.mkdir(parents=True, exist_ok=True)
    live = set()
    for d in pages:
        d["sha256"] = R.text_sha(d["text"])
        d["headings"] = R.headings(d["text"])
        d["links"] = R.doc_links(d["text"])
        d["page"] = f"pages/{d['source']}/{d['id']}.md"
        p = OUT / d["page"]
        md = render(d, spec_urls, built)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md)
        live.add(p)
    for old in (OUT / "pages").rglob("*.md"):
        if old not in live:
            print(f"  removed stale page {old.relative_to(OUT)}", file=sys.stderr)
            old.unlink()
    sources = {
        "cert": {"title": "FIDO Alliance certification programme pages", "url": HUB},
        "ctt": {"title": "Conformance test tools resources (docs; issues via `issues`)",
                "url": f"https://github.com/{REPOS['ctt'][0]}", "commit": commits["ctt"]},
        "interop": {"title": "FIDO2 interop web app", "url": f"https://github.com/{REPOS['interop'][0]}",
                    "commit": commits["interop"]},
    }
    (OUT / "resources.json").write_text(json.dumps({
        "built": built, "sources": sources,
        "pages": [{k: v for k, v in d.items() if k != "text"} for d in pages]}, indent=1, ensure_ascii=False))
    iss = issues(a.offline)
    (OUT / "issues.json").write_text(json.dumps({
        "repo": REPOS["ctt"][0], "url": f"https://github.com/{REPOS['ctt'][0]}/issues", "fetched": built,
        "note": "Titles and metadata only. Read the thread with `resources.py issue N`.", "issues": iss},
        indent=0, ensure_ascii=False))
    ent, commit, faq = awesome(a.offline)
    (OUT / "awesome.json").write_text(json.dumps({
        "url": f"https://github.com/{REPOS['awesome'][0]}", "license": "CC0-1.0", "commit": commit, "fetched": built,
        "faq": faq, "entries": ent}, indent=1, ensure_ascii=False))
    todo = sum("_TODO" in (OUT / d["page"]).read_text() for d in pages)
    print(f"{len(pages)} pages ({todo} without summary), {len(iss)} issues, {len(ent)} awesome entries", file=sys.stderr)


if __name__ == "__main__":
    main()
