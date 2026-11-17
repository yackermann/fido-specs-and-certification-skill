# How catalog summaries are written

Each catalog page `fido-spec-and-certification/catalog/docs/<family>/<doc_id>/<version>_<date>.md` has a
`## Summary` block that starts as `_TODO: summary not written yet._`. Replace **only that block**
(everything between `## Summary` and `## Table of contents`). Don't touch the front matter or the TOC:
`pipeline/build_catalog.py` regenerates them and keeps your summary.

## Reading the source

Use the skill's own script. Read only the parts you need, never the whole document:

```bash
export FIDO_SPEC_CACHE=<shared cache dir given in your brief>
python3 fido-spec-and-certification/scripts/fido.py show  <doc_id> --version <v>      # catalog page + TOC
python3 fido-spec-and-certification/scripts/fido.py section <doc_id> <anchor|number> --version <v> --max-chars 6000
```

Errata editions use `--version 2.1-errata`. For PDF-only documents, `fetch` prints the local path;
read it with the Read tool and the `pages` parameter.

Good sections to read: abstract, introduction/overview, conformance, any "changes", "differences"
or "revision history" section, and the main normative chapter headings.

## What to write

Format (Markdown, inside the Summary block):

```
## Summary

<1–3 short paragraphs: what the document is, what it defines or governs, and how it fits with the
other FIDO documents. Latest version of a lineage: 120–220 words. Older versions: 60–120 words,
focused on how this version differs from its neighbours.>

**Who needs it:** <authenticator vendors / platform & client developers / relying parties & server
developers / certification applicants / labs, as applicable>

**Look here for:**
- <a typical question this document answers> → §<number> `#<anchor>`
- ... (3–6 bullets; anchors must exist in this page's TOC)

**Changes from previous version:** <only if there is a previous catalogued version; be specific
about the features added or removed, or write "Editorial only" if that's all it is>
```

## Rules

- **Your own words.** Never copy sentences from the spec. Short technical terms, command names,
  field names and requirement IDs are fine. No quotes longer than a few words.
- **Accuracy over coverage.** State only what you read. If you could not confirm a difference
  between versions, say "differences not verified" instead of guessing.
- Name the certification relevance when it is real (for example, "the Vendor Questionnaire for
  L1/L2 lives in this document").
- No marketing tone, no hedging filler.
- Every anchor you cite must appear in that page's TOC.
