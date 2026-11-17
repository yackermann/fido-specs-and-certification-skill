#!/usr/bin/env python3
"""Certification resources beyond the specifications: FIDO certification web pages, the conformance
test tools documentation and issue tracker, the FIDO2 interop web app, and the awesome-webauthn list.

  python3 scripts/resources.py list [--source S]
  python3 scripts/resources.py search TERMS... [--source S]      pages, issues and awesome-webauthn entries
  python3 scripts/resources.py show PAGE                          catalog page: summary, outline, linked documents
  python3 scripts/resources.py read PAGE [SECTION] [--refresh] [--max-chars N]   live text (cached 7 days)
  python3 scripts/resources.py issues [TERMS...] [--test ID] [--label L] [--state open|closed] [--limit N]
  python3 scripts/resources.py issue NUMBER [--refresh] [--max-chars N]          live issue thread
  python3 scripts/resources.py awesome [TERMS...] [--category C] [--badge certified|conformant]

PAGE is a page id, its URL, or words from its title. SECTION is a heading's anchor or words from it.
Sources: cert (fidoalliance.org certification pages), ctt (conformance test tools docs),
interop (FIDO2 interop web app). Set GITHUB_TOKEN to raise GitHub's API limit (60 requests/hour without).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fido import CACHE, SANDBOX_HINT, UA, die  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
RES = SKILL / "catalog" / "resources"
MAX_AGE = dt.timedelta(days=7)
ISSUE_AGE = dt.timedelta(days=1)
DOC_EXT = (".pdf", ".docx", ".doc", ".xlsx", ".xls", ".zip", ".pptx")


def load(name: str) -> dict:
    return json.loads((RES / name).read_text())


# ---------------------------------------------------------------- HTML / Markdown -> text

def slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s]+", "-", s)


class WPText(HTMLParser):
    """fidoalliance.org (WordPress) content -> Markdown-ish text with '#' headings and '|' table rows."""
    SKIP = {"script", "style", "noscript", "svg", "form", "button", "select", "iframe"}
    BLOCK = {"p", "div", "section", "ul", "ol", "table", "blockquote", "figure", "br", "hr", "dl", "dd", "dt"}

    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base, self.out, self.skip = base, [], 0
        self.head, self.link, self.cell = None, None, None
        self.row: list[str] | None = None

    def emit(self, s: str):
        if self.cell is not None:
            self.cell.append(s)
        elif self.head is not None:
            self.head[1].append(s)
        else:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5"):
            self.head = (int(tag[1]), [])
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "li":
            self.emit("\n- ")
        elif tag == "a" and a.get("href"):
            self.link = urllib.parse.urljoin(self.base, a["href"])
            self.link_text_start = len(self.cell if self.cell is not None else
                                       self.head[1] if self.head is not None else self.out)
        elif tag in self.BLOCK:
            self.emit("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5") and self.head:
            level, parts = self.head
            self.head = None
            title = re.sub(r"\s+", " ", "".join(parts)).strip()
            if title:
                self.out.append(f"\n\n{'#' * level} {title}\n\n")
        elif tag in ("td", "th") and self.cell is not None:
            self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.out.append("\n| " + " | ".join(self.row) + " |")
            self.row = None
        elif tag == "a" and self.link:
            u, self.link = self.link, None
            if u.startswith(("http", "mailto:")) and "#" not in u.split("/")[-1][:1]:
                self.emit(f" <{u}>")
        elif tag in self.BLOCK or tag == "li":
            self.emit("\n")

    def handle_data(self, data):
        if not self.skip:
            self.emit(data)


def wp_text(html: str, url: str) -> str:
    start = html.find("entry-content")
    start = html.rfind("<", 0, start) if start >= 0 else 0
    end = len(html)
    for marker in ("Stay Connected, Stay Engaged", "<footer"):
        i = html.find(marker, start)
        if i >= 0:
            end = min(end, html.rfind("<h", start, i) if marker.startswith("Stay") else i)
    m = re.search(r"<h1[^>]*>.*?</h1>", html[:start], re.S)  # page title often sits above entry-content
    p = WPText(url)
    p.feed((m.group(0) if m else "") + html[start:end])
    text = "".join(p.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n- \n+", "\n- ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def headings(text: str) -> list[list]:
    """[[level, title, anchor], ...] from '#' lines (fenced code skipped)."""
    out, fence, seen = [], False, {}
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,5})\s+(.+?)\s*#*\s*$", line)
        if m:
            title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(2)).strip()
            a = slug(title)
            n = seen.get(a, 0)
            seen[a] = n + 1
            out.append([len(m.group(1)), title, a if n == 0 else f"{a}-{n}"])
    return out


def doc_links(text: str) -> list[list]:
    """Documents (PDF etc.) linked from a page: [[link text, url], ...]."""
    out, seen = [], set()
    for m in re.finditer(r"([^\n<|]{0,120}?)\s*<(https?://[^>\s]+)>", text):
        u = m.group(2)
        if urllib.parse.urlsplit(u).path.lower().endswith(DOC_EXT) and u not in seen:
            seen.add(u)
            out.append([re.sub(r"^[-\s]+", "", m.group(1)).strip()[-100:], u])
    for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text):
        u = m.group(2)
        if urllib.parse.urlsplit(u).path.lower().endswith(DOC_EXT) and u not in seen:
            seen.add(u)
            out.append([m.group(1), u])
    return out


def to_text(raw: str, kind: str, url: str) -> str:
    return wp_text(raw, url) if kind == "html" else raw


def text_sha(text: str) -> str:
    return hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode()).hexdigest()


# ---------------------------------------------------------------- network + cache

def http_get(url: str, headers: dict | None = None) -> bytes:
    h = {"User-Agent": UA, **(headers or {})}
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def cache_file(url: str, suffix: str = "") -> Path:
    u = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(u.path).strip("/") or "index"
    return CACHE / "resources" / u.netloc / (path + suffix)


def fresh(p: Path, age: dt.timedelta) -> bool:
    return p.exists() and time.time() - p.stat().st_mtime < age.total_seconds()


def get_cached(url: str, age: dt.timedelta, refresh: bool, suffix: str = ".raw", headers=None) -> tuple[str, str]:
    """Return (content, note). Uses the cache when fresh; falls back to a stale cache when offline."""
    p = cache_file(url, suffix)
    if fresh(p, age) and not refresh:
        return p.read_text(errors="replace"), f"cached {dt.datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d}"
    try:
        data = http_get(url, headers).decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        if p.exists():
            return (p.read_text(errors="replace"),
                    f"live fetch failed ({e}); using cached copy from {dt.datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d}")
        raise
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data)
    except OSError:
        pass  # read-only cache: still return the live content
    return data, f"fetched live {dt.date.today()}"


# ---------------------------------------------------------------- pages

def find_page(cat: dict, q: str) -> dict:
    pages = cat["pages"]
    for d in pages:
        if q in (d["id"], d["url"], d["url"].rstrip("/")) or q.rstrip("/") == d["url"].rstrip("/"):
            return d
    words = q.lower().split()
    hits = [d for d in pages if all(w in (d["id"] + " " + d["title"]).lower() for w in words)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        die(f"no resource page matches {q!r}. Try `resources.py search {q}` or `resources.py list`.")
    die(f"{len(hits)} pages match {q!r}:\n" + "\n".join(f"  {d['id']:44} {d['title']}" for d in hits[:25]))


def page_md(d: dict) -> str:
    return (RES / d["page"]).read_text()


def summary_of(d: dict) -> str:
    m = re.search(r"## Summary\n\n(.*?)\n\n## ", page_md(d), re.S)
    return m.group(1).strip() if m else ""


def cmd_list(a):
    cat = load("resources.json")
    for src, info in cat["sources"].items():
        if a.source and a.source != src:
            continue
        print(f"## {src} — {info['title']}  ({info['url']})")
        for d in cat["pages"]:
            if d["source"] == src:
                print(f"  {d['id']:46} {d['title']}")
        print()
    if not a.source or a.source == "issues":
        iss = load("issues.json")
        print(f"## issues — {len(iss['issues'])} conformance tools issues (`resources.py issues`)")
    if not a.source or a.source == "awesome":
        aw = load("awesome.json")
        print(f"## awesome — {len(aw['entries'])} awesome-webauthn entries (`resources.py awesome`)")


def match(hay: str, terms: list[str]) -> bool:
    hay = hay.lower()
    return all(t.lower() in hay for t in terms)


def cmd_search(a):
    cat = load("resources.json")
    n = 0
    for d in cat["pages"]:
        if a.source and d["source"] != a.source:
            continue
        hs = [h for h in d["headings"] if match(h[1], a.terms)]
        if match(d["id"].replace("-", " ") + " " + d["title"] + " " + summary_of(d), a.terms) or hs:
            n += 1
            print(f"[page] {d['id']}  {d['title']}  {d['url']}")
            for h in hs[:5]:
                print(f"         § {h[1]}  #{h[2]}")
    if not a.source or a.source == "issues":
        hits = [i for i in load("issues.json")["issues"] if match(i["title"] + " " + " ".join(i["tests"]), a.terms)]
        for i in hits[:15]:
            print(f"[issue] #{i['n']} {i['state']:6} {i['created'][:10]} {','.join(i['labels'])}  {i['title']}")
        if len(hits) > 15:
            print(f"[issue] … {len(hits) - 15} more: resources.py issues {' '.join(a.terms)}")
        n += len(hits)
    if not a.source or a.source == "awesome":
        for e in load("awesome.json")["entries"]:
            if match(f"{e['name']} {e['desc']} {e['category']} {' '.join(e['badges'])}", a.terms):
                n += 1
                print(f"[awesome] {e['category']}: {e['name']}  {e['url']}")
    if not n:
        print("no matches", file=sys.stderr)


def cmd_show(a):
    d = find_page(load("resources.json"), a.page)
    print(page_md(d))


def section_text(text: str, q: str) -> str:
    hs = headings(text)
    ql = q.lower().lstrip("#")
    pick = next((h for h in hs if h[2] == ql), None) or next((h for h in hs if ql in h[1].lower()), None)
    if not pick:
        die(f"no section matching {q!r}. Headings:\n" + "\n".join(f"  {'  ' * (h[0] - 1)}{h[1]}  #{h[2]}" for h in hs))
    lines, out, on, fence, idx = text.splitlines(), [], False, False, -1
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"^(#{1,5})\s+", line)
        if m:
            idx += 1
            if on and len(m.group(1)) <= pick[0]:
                break
            if hs[idx] is pick:
                on = True
        if on:
            out.append(line)
    return "\n".join(out)


def cmd_read(a):
    cat = load("resources.json")
    d = find_page(cat, a.page)
    try:
        raw, note = get_cached(d["raw_url"], MAX_AGE, a.refresh)
    except Exception as e:  # noqa: BLE001
        die(f"could not fetch {d['raw_url']}: {e}\n{SANDBOX_HINT}\n"
            f"Fallback: a web fetch tool on {d['url']}, asking for the exact text of the section you need.")
    text = to_text(raw, d["kind"], d["url"])
    changed = text_sha(text) != d["sha256"]
    print(f"[{d['title']} — {d['url']} — {note}"
          + (f"; CHANGED since the catalog snapshot of {cat['built']}" if changed else "") + "]\n")
    body = section_text(text, a.section) if a.section else text
    if len(body) > a.max_chars:
        body = body[: a.max_chars] + f"\n\n[… truncated at {a.max_chars} chars; ask for a section or raise --max-chars]"
    print(body)


# ---------------------------------------------------------------- issues

def gh_headers() -> dict:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    h = {"Accept": "application/vnd.github+json"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def cmd_issues(a):
    iss = load("issues.json")
    hits = []
    for i in iss["issues"]:
        if a.terms and not match(i["title"] + " " + " ".join(i["tests"]), a.terms):
            continue
        if a.test and not any(a.test.lower() in t.lower() for t in i["tests"]):
            continue
        if a.label and not any(a.label.lower() == x.lower() for x in i["labels"]):
            continue
        if a.state and i["state"] != a.state:
            continue
        hits.append(i)
    for i in hits[: a.limit]:
        print(f"#{i['n']:<4} {i['state']:6} {i['created'][:10]}  {','.join(i['labels']) or '-':28} {i['title']}")
    print(f"{len(hits)} issue(s) in the snapshot of {iss['fetched']}" + (f", showing {a.limit}" if len(hits) > a.limit else "")
          + f". Read one with `resources.py issue N`. Repository: {iss['url']}", file=sys.stderr)


TEMPLATE_NOISE = re.compile(
    r"^\s*(?:- \[ \].*|By submitting this issue.*|If you have privacy concerns.*|.*SOLEMNLY SWEAR.*|"
    r"NOTE: UAF 1\.0 certification.*|If you are platform authenticator vendor.*|For desktop tools|For UAF mobile tools)\s*$",
    re.I)


def clean_body(body: str) -> str:
    """Drop the issue template's unticked options and fixed notices; keep the reporter's answers."""
    lines = [ln for ln in (body or "").replace("\r\n", "\n").splitlines() if not TEMPLATE_NOISE.match(ln)]
    text = "\n".join(lines)
    text = re.sub(r"\n#+ [^\n]*\n+(?=#+ |\Z)", "\n", text)  # headings left with nothing under them
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def cmd_issue(a):
    iss = load("issues.json")
    api = f"https://api.github.com/repos/{iss['repo']}/issues/{a.number}"
    try:
        raw, note = get_cached(api, ISSUE_AGE, a.refresh, ".json", gh_headers())
        i = json.loads(raw)
        comments = []
        if i.get("comments"):
            rc, _ = get_cached(api + "/comments?per_page=100", ISSUE_AGE, a.refresh, ".comments.json", gh_headers())
            comments = json.loads(rc)
    except urllib.error.HTTPError as e:
        hint = (" GitHub's unauthenticated limit is 60 requests/hour; set GITHUB_TOKEN to raise it."
                if e.code in (403, 429) else "")
        die(f"GitHub API error {e.code} for issue {a.number}.{hint}\n"
            f"Fallback: a web fetch tool on https://github.com/{iss['repo']}/issues/{a.number}")
    except Exception as e:  # noqa: BLE001
        die(f"could not fetch issue {a.number}: {e}\n{SANDBOX_HINT}\n"
            f"Fallback: a web fetch tool on https://github.com/{iss['repo']}/issues/{a.number}")
    if "pull_request" in i:
        print("(this number is a pull request)")
    out = [f"# #{i['number']} {i['title']}",
           f"{i['html_url']} — {i['state']}"
           + (f" ({i.get('state_reason')})" if i.get("state_reason") else "")
           + f", opened {i['created_at'][:10]} by {i['user']['login']}"
           + (f", closed {i['closed_at'][:10]}" if i.get("closed_at") else "")
           + f"; labels: {', '.join(l['name'] for l in i['labels']) or '-'} [{note}]",
           "", clean_body(i.get("body"))]
    for c in comments:
        out += ["", f"--- {c['user']['login']} ({c.get('author_association', '').lower()}), {c['created_at'][:10]}",
                clean_body(c.get("body"))]
    text = "\n".join(out)
    if len(text) > a.max_chars:
        text = text[: a.max_chars] + f"\n\n[… truncated at {a.max_chars} chars; raise --max-chars]"
    print(text)


# ---------------------------------------------------------------- awesome-webauthn

def cmd_awesome(a):
    aw = load("awesome.json")
    hits = [e for e in aw["entries"]
            if (not a.terms or match(f"{e['name']} {e['desc']} {e['url']}", a.terms))
            and (not a.category or a.category.lower() in e["category"].lower())
            and (not a.badge or any(a.badge.lower() in b.lower() for b in e["badges"]))]
    cat = None
    for e in hits:
        if e["category"] != cat:
            cat = e["category"]
            print(f"\n## {cat}")
        badges = f"`{'` `'.join(e['badges'])}` " if e["badges"] else ""
        print(f"- {badges}{e['name']} — {e['url']}" + (f"\n  {e['desc']}" if e["desc"] else ""))
    print(f"\n{len(hits)} entr{'y' if len(hits) == 1 else 'ies'} from {aw['url']} (CC0, commit {aw['commit'][:7]}, "
          f"{aw['fetched']}). Badges are the list's own claims; check FIDO's certified products list for "
          "certification.", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--source")
    s = sub.add_parser("search"); s.add_argument("terms", nargs="+"); s.add_argument("--source")
    s = sub.add_parser("show"); s.add_argument("page")
    s = sub.add_parser("read"); s.add_argument("page"); s.add_argument("section", nargs="?")
    s.add_argument("--refresh", action="store_true"); s.add_argument("--max-chars", type=int, default=20000)
    s = sub.add_parser("issues"); s.add_argument("terms", nargs="*"); s.add_argument("--test")
    s.add_argument("--label"); s.add_argument("--state", choices=["open", "closed"]); s.add_argument("--limit", type=int, default=30)
    s = sub.add_parser("issue"); s.add_argument("number", type=int); s.add_argument("--refresh", action="store_true")
    s.add_argument("--max-chars", type=int, default=15000)
    s = sub.add_parser("awesome"); s.add_argument("terms", nargs="*"); s.add_argument("--category"); s.add_argument("--badge")
    a = p.parse_args()
    {"list": cmd_list, "search": cmd_search, "show": cmd_show, "read": cmd_read, "issues": cmd_issues,
     "issue": cmd_issue, "awesome": cmd_awesome}[a.cmd](a)


if __name__ == "__main__":
    main()
