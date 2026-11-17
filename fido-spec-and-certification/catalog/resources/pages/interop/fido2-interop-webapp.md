---
id: "fido2-interop-webapp"
source: "interop"
title: "FIDO2 interop web app (repository README)"
url: "https://github.com/fido-alliance/fido2-interop-webapp/blob/master/README.md"
kind: "markdown"
sha256: "4ae6da6c60060be4242a7bbb3c5c3ab7fa2888a34f0fb5d795fedad393fdc4f5"
snapshot: "2026-11-17"
---

# FIDO2 interop web app (repository README)

Source: https://github.com/fido-alliance/fido2-interop-webapp/blob/master/README.md (live text: `python3 scripts/resources.py read fido2-interop-webapp`)

## Summary

A single-page test client (`index.html`, titled "FIDO2 Interop v1.2") that FIDO2 server vendors host on their own server at interop events, so authenticator and client vendors can run WebAuthn ceremonies against it. The only edits allowed are setting `window.serverURL` to the server's base URL and `window.vendorName` to the company name. The README warns that changing any FIDO code can cancel interop results; extra tests may only go in a marked vendors' area.

Using a random username, it offers seven cross-platform steps: make credential and get assertion; the same with a resident key; multiple resident keys; and attestation `none` plus assertion (platform tests exist in code but have no buttons). Each step POSTs to `<serverURL>/attestation/options` and `/attestation/result`, or `/assertion/options` and `/assertion/result`, with cookies, and fails on any `status` other than `ok`. This is the same API as the server conformance tests.

**Look here for:**
- Setup instructions and the do-not-modify rule → fido2-interop-webapp `#fido2-interop-webapp`
- Where to report problems → IF YOU HAVE ANY ISSUES PLEASE REPORT HERE `#if-you-have-any-issues-please-report-here`

## Outline

- fido2-interop-webapp `#fido2-interop-webapp`
  - DO NOT MODIFY FIDO CODE IF YOU ARE PARTICIPATING IN THE INTEROPERABILITY EVENT! `#do-not-modify-fido-code-if-you-are-participating-in-the-interoperability-event`
  - FAIL TO COMPLY MAY RESULT IN CANCELATION OF THE INTEROP RESULTS `#fail-to-comply-may-result-in-cancelation-of-the-interop-results`
  - IF YOU HAVE ANY ISSUES PLEASE REPORT HERE `#if-you-have-any-issues-please-report-here`
  - OR EMAIL CONFORMANCE-TOOLS@FIDOALLIANCE.ORG `#or-email-conformance-toolsfidoallianceorg`
