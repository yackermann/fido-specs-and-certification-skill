#!/usr/bin/env python3
"""Crawl the public FIDO Alliance spec directory index (https://fidoalliance.org/specs/)
and write a flat JSON listing of every file: path, url, size, last-modified.

Maintainer tool: run it to discover new documents before updating catalog/catalog.yaml.
It does not download documents, only the directory listings.

Usage: python3 pipeline/crawl_index.py > pipeline/out/specs-index.json
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://fidoalliance.org/specs/"
UA = "fido-spec-and-certification-skill/0.1 (catalog crawler)"
# asset folders of the HTML spec renderings, not documents
SKIP_DIRS = {"fancy-index/", "img/", "images/", "resources/", "vendor/", "css/", "js/", "fonts/", "scripts/", "styles/"}

# nginx autoindex row: <a href="x">x</a>   20-Dec-2023 18:49    435265
ROW = re.compile(r'<a href="(?P<href>[^"?]+)">[^<]*</a>\s+(?P<date>\d{2}-\w{3}-\d{4} \d{2}:\d{2})\s+(?P<size>\S+)')
HREF = re.compile(r'<a href="([^"?]+)"')


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def crawl(url: str, out: list, depth: int = 0) -> None:
    if depth > 6:
        return
    html = get(url)
    rows = {m.group("href"): (m.group("date").strip(), m.group("size").strip()) for m in ROW.finditer(html)}
    hrefs = rows.keys() or HREF.findall(html)
    for href in hrefs:
        if href.startswith(("/", "..", "http", "#", "mailto:")) or href in SKIP_DIRS:
            continue
        full = urllib.parse.urljoin(url, href)
        if not full.startswith(BASE):
            continue
        if href.endswith("/"):
            time.sleep(0.2)
            try:
                crawl(full, out, depth + 1)
            except Exception as e:  # keep going on a bad directory
                print(f"warn: {full}: {e}", file=sys.stderr)
        else:
            date, size = rows.get(href, ("", ""))
            out.append({"path": full[len(BASE):], "url": full, "modified": date, "size": size})


if __name__ == "__main__":
    files: list = []
    crawl(BASE, files)
    files.sort(key=lambda f: f["path"])
    json.dump(files, sys.stdout, indent=1)
    print(f"{len(files)} files", file=sys.stderr)
