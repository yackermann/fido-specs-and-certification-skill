# FIDO spec and certification skill

A Claude skill for FIDO specifications and FIDO certification. It ships **summaries and tables of
contents only**. The official documents are downloaded from fidoalliance.org / w3.org when a user
needs them, so no FIDO or W3C text is redistributed.

> **Disclaimer:** This is an independent project. It is not affiliated with, endorsed by or
> sponsored by the FIDO Alliance or W3C. FIDO, FIDO2 and FIDO Alliance are trademarks of the FIDO
> Alliance. The catalog summaries are unofficial; the downloaded specifications and FIDO's own
> certification pages are the authoritative sources.

```
fido-spec-and-certification/          ← the skill (this folder is what you distribute)
  SKILL.md                   workflow: clarify role/protocol/version → find → download → cite
  catalog/INDEX.md           one line per document, read first
  catalog/catalog.json       every document version: URL, sha256, status
  catalog/docs/…/*.md        summary + certification status + TOC with anchors, per version
  scripts/fido.py            list / search / show / fetch / toc / section / text (stdlib only)
  scripts/mds.py             MDS3 BLOB browser: update / info / search / show (stdlib only)
pipeline/                    maintainer tools (not distributed)
  crawl_index.py             crawl https://fidoalliance.org/specs/ directory listings
  build_catalog.py           scope rules, download, hash, TOC extraction, catalog pages
  certification_sources.json curated ACTIVE certification documents (not PS-labelled)
  make_index.py              INDEX.md + SCOPE.md
  SUMMARY_GUIDE.md           how summaries are written
SCOPE.md                     the approved document list
```

## Install

- **Claude Code:** copy or symlink `fido-spec-and-certification/` into `~/.claude/skills/` (personal) or
  `.claude/skills/` (project).
- **claude.ai:** zip the `fido-spec-and-certification/` folder and upload it under Settings → Capabilities → Skills.
  Downloads need network access to fidoalliance.org and w3.org.

Downloaded documents are cached in `~/.cache/fido-spec-and-certification` (override with `FIDO_SPEC_CACHE`).
The MDS BLOB is cached in its `mds/` subfolder. FIDO allows two BLOB downloads per day, so
`mds.py update` keeps a pull log there and refuses a third download within 24 hours. The BLOB's
signature is verified against GlobalSign Root R46 (the root FIDO publishes), embedded in the script.

## Scope

Proposed Standards only, with these rules: U2F 1.2 only; UAF 1.1 and later; MDS / Metadata
Statement 3.1.1 only; the `fido-v2.0-ps-20150904/` and `fido-v2.0-ps-20170927/` folders are excluded.
The certification documents FIDO lists as ACTIVE are added from `pipeline/certification_sources.json`
(Security Requirements 1.5.1/1.6/1.7 and companions, Biometrics Requirements 4.1/5.0, certification
policies, FIDO2 Server Requirements, WebAuthn L2/L3). See `SCOPE.md` for the full list.

## Updating the catalog

```bash
python3 -m venv pipeline/.venv && pipeline/.venv/bin/pip install pypdf   # once, for PDF outlines
python3 pipeline/crawl_index.py > pipeline/out/specs-index.json          # discover new files
# edit pipeline/certification_sources.json if FIDO's ACTIVE/sunset lists changed
python3 pipeline/build_catalog.py                                         # pages + catalog.json (keeps summaries)
# write summaries for new pages (pipeline/SUMMARY_GUIDE.md), then:
python3 pipeline/make_index.py
git diff fido-spec-and-certification/catalog                                       # review, commit, tag e.g. catalog-2026.11
```

When FIDO re-publishes a file, its hash changes. `fido.py` then warns that the catalog TOC may be
stale, and the next `build_catalog.py` run picks up the new hash.
