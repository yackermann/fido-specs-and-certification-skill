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

## Resource pages (`catalog/resources/pages/<source>/<id>.md`)

Same principles, different source. Replace only the block between `## Summary` and `## Outline`.
Read the page with the skill's script (it fetches the live page and caches it):

```bash
python3 fido-spec-and-certification/scripts/resources.py show <id>            # catalog page + outline
python3 fido-spec-and-certification/scripts/resources.py read <id> --max-chars 12000
python3 fido-spec-and-certification/scripts/resources.py read <id> "<heading words>"
```

Format:

```
## Summary

<1–2 short paragraphs, 50–150 words: what the page covers and who it is for, with the concrete
facts a reader comes for (steps, prerequisites, versions, deadlines, who to contact, what a test
tool does), in your own words. Mark time-sensitive facts (fees, dates, versions, lists of labs)
as "as of the snapshot" and don't copy fee amounts: say the page lists them.>

**Look here for:**
- <typical question> → <heading> `#<anchor>`   (2–5 bullets; anchors must exist in the Outline;
  if the page has no useful headings, point to the page itself without an anchor)
```

Legal-terms and very short pages: 1–3 sentences, no bullets needed. Never invent anchors, steps,
programme names or numbers. If a page contradicts another page or a spec, say so briefly.

## Reading guide (spec catalog pages)

Every spec catalog page also gets a `## Reading guide` section, placed **after the Summary block and
before `## Table of contents`** (the builder preserves everything in between). The Summary says what
the document is; the reading guide is the analysis a senior FIDO engineer would give a colleague
before they open the document: where to look, what matters, what is easy to get wrong. It is what
lets the skill pick the right sections without reading the whole document.

Read the document properly first (`fido.py toc`, then `fido.py section` on the main chapters; for
PDFs, `pipeline/.venv/bin/python fido-spec-and-certification/scripts/fido.py text <doc> --version <v>`
and read the text file). Base every point on text you read.

### Latest version of a lineage (`latest_in_lineage: true`)

```
## Reading guide

**Start here:** <2–4 sections to read first to get oriented, each with § and `#anchor`, and why>

**Section by section:**
- §<n> <title> `#<anchor>`: <what it defines and what matters in it: the key normative rules
  (MUST/SHALL), the data structures or state involved, ordering and error behaviour, options that
  change behaviour, how it connects to other sections>
- ... (cover every major part of the document; 6–20 bullets depending on size. Group small
  sections; split big ones such as individual CTAP commands or WebAuthn ceremony steps.)

**What matters most:** <the requirements implementers most often get wrong or that certification
testing leans on, and the decisions the document leaves to the implementer. 3–8 bullets, each with
§ and anchor.>

**Watch out for:** <ambiguities, deprecated or legacy parts, informative-only sections that look
normative, known errata, contradictions with other documents. Omit if nothing real.>

**Related documents:** <catalog doc_ids (with version when it matters) and why you'd read them
alongside this one>
```

Length scales with the document: 300–600 words for short documents, up to ~1500 for CTAP, WebAuthn,
UAF Protocol, FDO and Security Requirements.

### Older versions

```
## Reading guide

**Use this version when:** <who still needs it: certification rules, deployed base, L3/L3+ etc.>

**Differences from <neighbour or latest version>:** <specific sections added, removed or changed,
with § and anchor in THIS page's TOC; behaviour changes, not editorial ones. If you could not
verify a difference, say so.>

**Section by section:** <only the parts that differ or matter specifically for this version;
otherwise say "structure as in <latest version>; see that page's reading guide">
```

100–400 words.

### Rules (in addition to the general rules above)

- Every `#anchor` must exist in this page's TOC; every § number must match it.
- Paraphrase. Name fields, commands, error codes and requirement IDs exactly; quote at most a few
  words.
- Normative weight matters: say MUST / SHOULD / MAY where the document does, and flag
  informative sections.
- No guessing. If something isn't in the text you read, leave it out.
