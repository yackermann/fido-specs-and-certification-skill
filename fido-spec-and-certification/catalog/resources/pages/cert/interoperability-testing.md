---
id: "interoperability-testing"
source: "cert"
title: "Interoperability Testing"
url: "https://fidoalliance.org/certification/interoperability-testing/"
kind: "html"
sha256: "84a84a43844275fafd7bd210ed691001ffdc3f575bba9e3e9e661b42ce0b04dc"
snapshot: "2026-11-17"
---

# Interoperability Testing

Source: https://fidoalliance.org/certification/interoperability-testing/ (live text: `python3 scripts/resources.py read interoperability-testing`)

## Summary

Explains the interoperability step required for FIDO functional certification of servers and authenticators. Two routes exist: remote Interoperability Testing Events, where each implementation is tested against every compatible implementation present, and year-round Virtual On Demand testing run by the Certification Secretariat against donated reference implementations, available when at least three reference implementations from three vendors exist and requiring an NDA. Before registering for an event the implementation must have passed conformance self-validation and stay unchanged; registration closes 12 days before, optional pre-testing runs the week before, and events happen at least every 90 days. As of the snapshot the page lists FIDO2/UAF event dates in September and December 2026.

It also gives per-protocol test steps (UAF register/authenticate/transaction/de-register, U2F via Chrome, FIDO2 register/authenticate/reset plus optional PIN, resident key and HMAC checks) and the L1 security requirements checked at interop. The listed browser versions (Chrome 69, Edge 44, Firefox 61) look outdated.

**Look here for:**
- When are the next events and how far ahead to register? → Interoperability Events (FIDO2 and FIDO UAF) `#interoperability-events-fido2-and-fido-uaf`
- Can I test without attending an event? → On Demand Testing `#on-demand-testing`
- What FIDO2 tests are required versus optional? → FIDO2 Interoperability Testing Procedures `#fido2-interoperability-testing-procedures`
- Which L1 requirements are verified at interop? → Level 1 Authenticator Certification Testing Procedures `#level-1-authenticator-certification-testing-procedures`

## Outline

- Interoperability Testing `#interoperability-testing`
  - Interoperability Testing Events `#interoperability-testing-events`
  - Interoperability Events (FIDO2 and FIDO UAF) `#interoperability-events-fido2-and-fido-uaf`
  - On Demand Testing `#on-demand-testing`
  - Testing Procedures `#testing-procedures`
    - UAF Interoperability Testing Procedures `#uaf-interoperability-testing-procedures`
    - U2F Interoperability Testing Procedures `#u2f-interoperability-testing-procedures`
    - FIDO2 Interoperability Testing Procedures `#fido2-interoperability-testing-procedures`
    - Level 1 Authenticator Certification Testing Procedures `#level-1-authenticator-certification-testing-procedures`

## Linked documents

-  protect test participants’ confidential information. The non-disclosure agreement is available here: https://fidoalliance.org/wp-content/uploads/2023/04/2023-03-21-FIDO-Certification-NDA_FINAL.pdf
