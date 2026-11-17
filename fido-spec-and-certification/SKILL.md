---
name: fido-spec-and-certification
description: Answers questions about FIDO Alliance specifications and FIDO certification (CTAP/FIDO2, WebAuthn, UAF, U2F/CTAP1, Metadata Service, Authenticator Security Requirements L1–L3+, Biometric Component certification, FIDO2 server requirements, FDO, CXF). Finds the right document and version, downloads the official file from fidoalliance.org or w3.org on demand, and answers with section-level citations. Use when someone asks what a FIDO spec requires, which documents or levels apply to their product, how to prepare for FIDO certification, what changed between versions, or wants a requirement, command, error code or field explained.
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
options (use the AskUserQuestion tool when it's available). If the question is purely explanatory
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
   PDF path from `fetch` with the Read tool, passing `pages`. If that also fails, suggest `pip install pypdf`.
4. If the download fails, work down this list. The sandbox may block the domain (claude.ai and
   some managed environments allow only listed domains), the site may reject the client, or the
   machine may be offline.
   1. **curl** (when you have a shell), saving to the cache path the script printed:
      `curl -sL -A "fido-spec-and-certification-skill/0.1" -o "<cache path>" "<url>"`. Then rerun the
      `fido.py` command; it picks up the cached file and checks the hash.
   2. **Web fetch tool** (it runs outside the code sandbox). Fetch the document URL from the catalog
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

Live sources (fetch with the web fetch tool or `curl`):

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

Member-only material (test tools, test-tool output, interop event details), the fee schedule, and
documents outside the catalog. Say so, and point the user to fidoalliance.org.
