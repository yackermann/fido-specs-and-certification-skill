#!/usr/bin/env python3
"""Write fido-spec-and-certification/catalog/INDEX.md (read first by the skill) and SCOPE.md (maintainer record).

Run after build_catalog.py and after summaries are written:
    python3 pipeline/make_index.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "fido-spec-and-certification/catalog"
ORDER = ["ctap", "webauthn", "sr", "bio", "cert", "mds", "uaf", "u2f", "common", "fdo", "cx"]


def first_sentence(page: Path) -> str:
    text = page.read_text()
    m = re.search(r"## Summary\n\n(.*?)\n", text)
    if not m or m.group(1).startswith("_TODO"):
        return ""
    s = m.group(1).strip()
    cut = re.search(r"(?<=[a-z0-9)\]`])\.\s", s)
    return s[: cut.start() + 1] if cut else s


def vkey(d):
    return tuple(int(x) for x in d["version"].split("."))


def main():
    c = json.loads((CAT / "catalog.json").read_text())
    docs = c["documents"]
    fams = sorted({d["family"] for d in docs}, key=lambda f: ORDER.index(f) if f in ORDER else 99)

    idx = [
        "# FIDO document catalog",
        "",
        f"Built {c['built']}. {len(docs)} document versions. Each line is one document (lineage); versions "
        "in **bold** are the latest catalogued. Status in braces comes from the FIDO certification pages.",
        "Open a page with `python3 scripts/fido.py show <doc_id> --version <v>`.",
    ]
    for f in fams:
        idx += ["", f"## {f} — {c['families'][f]}", ""]
        lineages = {}
        for d in docs:
            if d["family"] == f:
                lineages.setdefault(d["doc_id"], []).append(d)
        for doc_id, vers in sorted(lineages.items()):
            vers.sort(key=lambda d: (vkey(d), d["date"], d["edition"] == "ps-errata"))
            latest = vers[-1]
            vs = []
            for d in vers:
                v = d["version"] + ("-errata" if d["edition"] == "ps-errata" else "")
                v = f"**{v}**" if d is latest else v
                vs.append(v + (f" {{{d['status']}}}" if d.get("status") else ""))
            blurb = first_sentence(CAT / latest["page"])
            idx.append(f"- `{doc_id}` — {latest['title']}. Versions: {', '.join(vs)}."
                       + (f" {blurb}" if blurb else ""))
    (CAT / "INDEX.md").write_text("\n".join(idx) + "\n")

    scope = [
        "# Catalog scope (approved 2026-11-16)",
        "",
        "Rules: Proposed Standards only, except curated certification documents that FIDO lists as ACTIVE "
        "(`pipeline/certification_sources.json`). U2F 1.2 only; UAF 1.1+; MDS / Metadata Statement 3.1.1 only; "
        "folders `fido-v2.0-ps-20150904/` and `fido-v2.0-ps-20170927/` excluded. "
        "Security Requirements ≤1.5 and Biometrics Requirements ≤3.0 are sunset and excluded.",
        "",
        "| Family | Document | Version | Maturity | Date | Status | File |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in fams:
        for d in sorted((d for d in docs if d["family"] == f), key=lambda d: (d["doc_id"], vkey(d), d["date"])):
            v = d["version"] + (" (errata ed.)" if d["edition"] == "ps-errata" else "")
            name = d["url"].rstrip("/").rsplit("/", 1)[-1]
            scope.append(f"| {f} | {d['title']} | {v} | {d['maturity']} | {d['date']} | {d.get('status') or ''} | "
                         f"[{name}]({d['url']}) |")
    (ROOT / "SCOPE.md").write_text("\n".join(scope) + "\n")
    print(f"INDEX.md and SCOPE.md written ({len(docs)} documents)")


if __name__ == "__main__":
    main()
