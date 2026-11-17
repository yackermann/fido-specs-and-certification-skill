---
name: fido-spec-and-certification
description: Answers questions about FIDO Alliance specifications and FIDO certification (CTAP/FIDO2, WebAuthn, UAF, U2F/CTAP1, Metadata Service, Authenticator Security Requirements L1–L3+, Biometric Component certification, FIDO2 server requirements, FDO, CXF). Finds the right document and version, downloads the official file from fidoalliance.org or w3.org on demand, and answers with section-level citations. Also covers the certification programme itself (process, levels, labs, fees pages, interop events, biometric, FDO and identity-verification programmes), the conformance test tools (docs and their public issue tracker, searchable by test ID), the FIDO2 interop web app, and the awesome-webauthn list of libraries and tools. Also browses the FIDO Metadata Service (MDS3) BLOB: look up an authenticator by AAGUID, AAID or name, its certification status, level and metadata statement. Use when someone asks what a FIDO spec requires, which documents or levels apply to their product, how to prepare for FIDO certification, what changed between versions, or wants a requirement, command, error code or field explained.
---

# FIDO specifications and certification

> This skill is independent and **not affiliated with, endorsed by or sponsored by the FIDO
> Alliance** or W3C. Its summaries are unofficial; the downloaded documents and FIDO's certification
> pages are authoritative. If a user seems to take you for an official FIDO source, say so.

This skill ships a **catalog** (summary + table of contents for each document version), not the
documents themselves. When you need the actual text, the script downloads the official file into a
local cache and extracts just the sections you ask for.

- `catalog/INDEX.md`: one line per document, grouped by family. **Read this first.**
- `catalog/docs/<family>/<doc_id>/<version>_<date>.md`: summary, certification status and full TOC with anchors
- `catalog/catalog.json`: machine-readable list (URLs, sha256, status)
- `scripts/fido.py`: search, download, section extraction (Python 3 stdlib, no installs)
- `scripts/mds.py`: browse the FIDO Metadata Service BLOB (see "Metadata Service lookups" below)
- `scripts/resources.py` + `catalog/resources/`: certification web pages, conformance tools docs and
  issues, interop app, awesome-webauthn (see "Certification process, test tools and ecosystem" below)

Run the script from the skill folder: `python3 scripts/fido.py <command>`. Commands:

| Command | Use |
|---|---|
| `list [--family F] [--all-versions]` | what's available |
| `versions DOC` | every catalogued version with its status |
| `search TERMS... [--all-versions]` | search titles, summaries and section titles |
| `show DOC [--version V]` | the catalog page (summary + TOC) |
| `fetch DOC [--version V]` | download the official file, print the local path |
| `toc DOC [--version V]` | section list of the downloaded document |
| `section DOC ANCHOR [--version V] [--max-chars N]` | text of one section (by anchor, number like `6.5.5.7`, or title words) |
| `text DOC [--version V]` | whole document as plain text, written to a file |

DOC is a doc_id or a short alias (`ctap`, `webauthn`, `sr`, `acl`, `aroe`, `bio`, `mds`,
`metadata-statement`, `server-requirements`, `fdo`, `cxf`, …). Without `--version` you get the
latest catalogued version. Errata editions: `--version 2.1-errata`.

## Workflow

### 1. Pin down the context, asking only what you don't already know

FIDO answers depend heavily on role, protocol and version. Before reading specs, establish:

1. **Role:** authenticator vendor (roaming key, platform, software), client or platform developer,
   relying party or FIDO server developer, biometric component vendor, or certification lab or consultant.
2. **Protocol family:** FIDO2 (CTAP + WebAuthn), UAF, U2F/CTAP1, Metadata (MDS), FDO, CXF.
3. **Version:** default to the latest. For certification work, use the versions FIDO currently
   accepts (see the version table below). If the user names an older version, use that one.
4. **For certification questions:** the goal (Functional certification, Authenticator Level
   L1 / L1+ / L2 / L3 / L3+, Biometric Component) and, if relevant, the transport (USB, NFC, BLE, hybrid).

Infer what you can from the request (a question about `authenticatorClientPIN` is CTAP; a question
about "the vendor questionnaire" is SR). Ask the rest in **one** short message, offering the likely
options (use your client's structured-question tool if it has one). If the question is purely explanatory
and the version barely matters, answer from the latest version and say which one you used.

### 2. Find the document and section

1. Read `catalog/INDEX.md` to pick candidate documents.
2. `fido.py search <terms>` to find sections by title. `fido.py show <doc>` for the summary and full TOC.
3. Choose the exact section anchors you need.

### 3. Download and read

1. `fido.py fetch <doc> --version <v>`. Tell the user which document you downloaded, its version,
   the source URL and the local path.
2. `fido.py section <doc> <anchor> --version <v>` for each section you need. Prefer several focused
   sections over one huge one. Raise `--max-chars` only when needed.
3. For PDF-only documents (for example the Functional Certification Policy), run `text`. If `pypdf`
   is installed, it writes a text file with `[page N]` markers that you can grep. Otherwise, open the
   PDF path from `fetch` with a file-reading tool that handles PDFs, if your client has one (for
   example Claude's Read tool with `pages`). If neither works, suggest `pip install pypdf`.
4. If the download fails, work down this list. The sandbox may block the domain (claude.ai and
   some managed environments allow only listed domains), the site may reject the client, or the
   machine may be offline.
   1. **curl** (when you have a shell), saving to the cache path the script printed:
      `curl -sL -A "fido-spec-and-certification-skill/0.1" -o "<cache path>" "<url>"`. Then rerun the
      `fido.py` command; it picks up the cached file and checks the hash.
   2. **A web fetch or browsing tool**, if your client has one (it usually runs outside the code sandbox). Fetch the document URL from the catalog
      page and ask for the **exact text** of the section you need, by number and title from the
      catalog TOC (for example "the verbatim text of §6.5.5.7 Operations to Obtain a
      pinUvAuthToken"). URL fragments (`#anchor`) are usually ignored, so name the section. The tool
      may condense long pages. Rely only on text it returns verbatim for normative detail, and say
      the source was fetched this way. Cite with the catalog URL and anchor as usual.
   3. **Ask the user** to download the URL in a browser and save it at the cache path, then continue.

   If none of these works, answer from the catalog summary and TOC only. Say clearly that you
   couldn't read the document itself, so the answer isn't verified against the spec text.

### 4. Answer

- **Cite every claim:** document title, version, section number, and a link `<url>#<anchor>`.
- **Separate normative from informative:** MUST/SHALL/SHOULD carry requirement weight; notes and
  "non-normative" sections don't.
- **State the certification status** of the version you used (the `status` field in the catalog page).
- **Paraphrase.** The documents are copyrighted by FIDO Alliance / W3C. Quote only short fragments
  (a requirement sentence, a field name). Don't reproduce sections wholesale.
- **Never invent** requirement IDs, command codes, error codes or section numbers. If you can't find
  something, say so and show where you looked.
- This skill is not affiliated with the FIDO Alliance and is not an accredited lab. For binding decisions (eligibility,
  fees, timelines, test-tool behaviour), point the user to the FIDO certification team or their lab.

## Metadata Service lookups (`scripts/mds.py`)

The MDS3 BLOB lists every authenticator with a metadata statement: AAGUID (FIDO2), AAID (UAF) or
attestation key identifiers (U2F), certification status history with certificate numbers and
levels, the metadata statement itself and, for FIDO2, `authenticatorGetInfo`. Use it for questions
like "is this AAGUID certified, and at which level?", "which authenticators are L3+?", "what
transports or extensions does this key report?".

| Command | Use |
|---|---|
| `update [--force]` | download the BLOB, verify its signature, cache it |
| `info` | BLOB number, `nextUpdate`, download time, pull budget left, counts by protocol and status |
| `search TERMS... [--status S] [--protocol fido2\|uaf\|u2f] [--limit N]` | find entries by name, AAGUID, AAID, key identifier or certificate number (use `""` to match all) |
| `show ID [--json] [--icon]` | one entry: identifiers, status reports (newest first), statement fields, getInfo |

Rules:

- **FIDO allows only two BLOB downloads per day.** Only `update` downloads. It refuses when two
  pulls were made in the last 24 h, and skips the download if the cached BLOB is less than 24 h old
  (`--force` overrides that skip, not the limit). Every other command reads the cache. Never
  download the BLOB any other way (curl, web fetch), since that would bypass the counter.
- **Run `update` only when needed:** no cached BLOB, or `info` says `nextUpdate` has passed, or the
  user asks for the latest data. Otherwise use the cache and say which BLOB number and download
  date the answer comes from.
- **Before the first download, tell the user** that retrieving and using the BLOB means accepting
  FIDO's MDS legal terms (https://fidoalliance.org/metadata/metadata-legal-terms/).
- The signature is checked against GlobalSign Root R46, the root FIDO publishes for the BLOB, which
  is embedded in the script. No system certificate store is used. Revocation (CRL) is not checked.
  If verification fails, the previous BLOB is kept: say so and don't use the rejected file.
- The latest status report is the current status. `REVOKED`, `USER_KEY_PHYSICAL_COMPROMISE` and
  similar statuses matter for relying parties: point them out. For field meanings, cite the
  Metadata Statement 3.1.1 and MDS 3.1.1 specs (`metadata-statement`, `mds`) as usual.
- The BLOB is FIDO data, not this skill's: quote fields as they are, and don't infer
  certification beyond what the status reports say.

## Certification process, test tools and ecosystem (`scripts/resources.py`)

Specifications say what to implement; these sources say how certification works and how the test
tools behave. Each web or docs page has a catalog page (summary and outline) and is read live, like
the specs. Run `python3 scripts/resources.py <command>`:

| Command | Use |
|---|---|
| `search TERMS...` | one search across pages, issue titles and awesome-webauthn entries |
| `list [--source cert\|ctt\|interop]` | all catalogued pages |
| `show PAGE` | catalog page: summary, outline, linked documents (PDFs, with catalog doc ids when known) |
| `read PAGE [SECTION]` | live text of the page or one section (cached 7 days, `--refresh` to force) |
| `issues [TERMS] [--test ID] [--label L] [--state open\|closed]` | the conformance tools issue index |
| `issue N` | the live issue thread, with the template boilerplate removed |
| `awesome [TERMS] [--category C] [--badge certified\|conformant]` | libraries, demos, authenticators, tools |

Sources and when to use them:

- **`cert`: fidoalliance.org certification pages.** Process steps, what each level (L1–L3+) requires,
  companion programmes, labs, fees, interop events, derivative and delta certification, biometric,
  FDO, DocAuth and Face Verification programmes, MDS terms, certification marks. Use them for "how do I
  get certified", "what does L2 involve", "how does interop testing work". `read` flags a page whose
  text changed since the catalog snapshot: then trust the live text and say it changed. Don't quote fee
  amounts from memory or the catalog; read the fees page live. The certified products directory is a
  dynamic site that isn't catalogued: point users to https://fidoalliance.org/certification/fido-certified-products/
  or use `mds.py` for authenticators.
- **`ctt`: conformance test tools docs.** How to run the FIDO2 server, authenticator and UAF server
  tests, the conformance test server API that a server under test must expose, test automation, the
  GetInfo snapshot, FDO pre-interop. Access to the tools themselves requires registering with FIDO.
- **`issues`: the public conformance tools issue tracker** (850+ issues, titles and metadata in the
  catalog). When a user reports a failing test, search by test ID first (`issues --test
  Authr-ClientPin2`), then by words, then read the matching threads. A closed issue with a fix
  ("fixed in v1.9.3") usually means: update the tool. Say which issue you relied on, link it, and say
  that tool behaviour is the FIDO tools team's call, not the spec's. The spec still decides what is
  correct: if a thread and the spec disagree, say so and cite both.
- **`interop`: the FIDO2 interop web app** a FIDO2 server vendor hosts for interop events. Its
  README says not to modify it for the event.
- **`awesome`: awesome-webauthn** (CC0 community list, shipped as data). Use it to suggest libraries,
  demos and tools. Its `FIDO CERTIFIED` / `FIDO CONFORMANT` badges are the list's own claims
  (CONFORMANT is self-reported): verify certification on FIDO's certified products list before
  relying on it.

GitHub's API allows 60 unauthenticated requests per hour (`issue` uses one or two). If the user has
a token, `GITHUB_TOKEN` raises the limit. When the API fails, use a web fetch tool on the issue URL.

## Running in a sandbox (Codex, managed environments)

The scripts need Python 3 only and work in any agent that can run shell commands (Claude Code,
claude.ai, Codex and others). Sandboxes change two things:

- **Network.** Downloads fail when the sandbox blocks network access; the scripts then say so. Ask
  the user to approve running the command outside the sandbox, or to enable network access for
  the session (in Codex, network access is off in the default `workspace-write` mode), then
  rerun. Meanwhile use the fallbacks in step 3.4.
- **Cache folder.** `fido.py` uses `~/.cache/fido-spec-and-certification` and falls back to a temp
  folder when that isn't writable; documents already downloaded there are still read. Suggest
  setting `FIDO_SPEC_CACHE` to a folder inside the workspace if downloads should survive the session.
  `mds.py update` has no fallback, because its pull log must persist: it explains the options instead.

## Which documents apply (certification map)

| Goal | Read |
|---|---|
| FIDO2 authenticator, functional | CTAP 2.3 (`ctap`), WebAuthn L3 (`webauthn`), Metadata Statement 3.1.1 |
| Authenticator security level L1 / L1+ / L2 | Security Requirements (`sr`: Vendor Questionnaire + requirements per level), Allowed Cryptography List (`acl`), Authenticator Metadata Requirements, Authenticator Certification Policy; L1+ also: L1+ Application of Attack Potential |
| L3 / L3+ | Security Requirements **v1.5.1** (required for L3/L3+), AROE List (`aroe`), ACL, Authenticator Certification Policy |
| Biometric component | Biometrics Requirements (`bio`), Biometric Component Certification Policy, Authenticator Metadata Requirements |
| FIDO2 server / relying party | FIDO2 Server Requirements 2.3 (`server-requirements`), WebAuthn L3, MDS 3.1.1 (`mds`) |
| UAF authenticator, client or server | UAF 1.1 (certifiable) or 1.2 docs, plus SR documents for authenticators |
| U2F / CTAP1 | U2F 1.2 docs; CTAP 2.x covers CTAP1 interoperation |
| Process, steps, interop testing | Functional Certification Policy 1.3.9, Authenticator Certification Policy 1.4.1 |
| Device onboarding (IoT) | FDO 2.0 (separate FDO certification program) |
| Credential import/export between providers | CXF 1.0 errata edition (no FIDO certification program) |

## Versions FIDO accepts for certification (as of 2026-11-16)

The catalog page's `status` field carries the same information. When dates matter, follow
"Keeping status current" below.

| Document | Accepted | Notes |
|---|---|---|
| Authenticator Security Requirements (+ ACL, AROE, Metadata Req.) | 1.7 ACTIVE; 1.6 until 2027-01-13; 1.5.1 no expiry | 1.5.1 is mandatory for L3/L3+ (CTAP 2.1 only); 1.5 and earlier are sunset |
| Biometrics Requirements | 5.0 ACTIVE; 4.1 until 2027-03-31 | 3.0 and earlier sunset |
| Biometric Component Certification Policy | 1.5 | 1.4 sunset |
| FIDO2 Server Requirements | 2.3 | WebAuthn L3 + CTAP 2.3 |
| UAF | 1.1 | 1.0 sunset (2019 servers, 2020 clients/authenticators) |
| U2F | 1.2 | 1.0 and 1.1 sunset (2019–2022) |
| CTAP | 2.3 | FIDO's own table only says "FIDO2 1.0"; vendor sources report new FIDO2 certifications are issued against CTAP 2.3 |

Some ACTIVE certification documents are published with Review Draft file names (SR 1.7,
Biometrics 5.0, Server Requirements 2.3). FIDO's certification pages list them as active, so treat
them as current.

## Keeping status current

The catalog is a snapshot; its build date is `built` in `catalog/catalog.json`. FIDO changes these
lists rarely, but the answer must still reflect the live state. Check the live sources when **any**
of these holds:

- the answer depends on what is certifiable, active or sunset, or on a date or deadline;
- a sunset date in the table above has already passed;
- the catalog is more than 3 months old;
- the user mentions a version or document the catalog doesn't have.

Live sources (fetch with a web fetch or browsing tool, or `curl`):

| What | Where |
|---|---|
| Spec versions accepted, sunset rules, Functional Certification Policy | https://fidoalliance.org/certification/getting-started/ |
| Security Requirements, ACL, AROE, Metadata Requirements: active/sunset | https://fidoalliance.org/certification/authenticator-certification-levels/ |
| Biometrics Requirements and Biometric Certification Policy | https://fidoalliance.org/certification/resource-documentation-biometric/ |
| FIDO2 Server Requirements | https://fidoalliance.org/certification/functional-certification/functional-certification-servers/ |
| New spec releases (new `-ps-` folders or files) | https://fidoalliance.org/specs/ (directory listing) |
| WebAuthn | https://www.w3.org/TR/webauthn/ (latest level) |

How to use them:

1. Compare what the live page says with the catalog `status`. When they differ, the live page wins.
   Tell the user plainly, e.g. "The catalog (built 2026-11-16) lists SR 1.6 as active until 2027-01-13;
   FIDO's page now lists it as sunset."
2. If a newer version exists that the catalog lacks, you can still use it: download it from the
   live URL with `curl -A "fido-spec-and-certification-skill/0.1"`, then read it. Say that it isn't
   catalogued yet, so there's no summary or TOC for it.
3. Mention once at the end of the answer that the catalog needs a refresh (maintainers: see the
   repository README, "Updating the catalog"). Don't block the answer on it.

## Not covered

The conformance tools themselves (registration required), member-only material (test-tool output,
interop event logistics), FIDO's certified products directory (dynamic site), and documents outside
the catalog. Say so, and point the user to fidoalliance.org.
