---
id: "fdo-functional-certification"
source: "cert"
title: "FDO Functional Certification"
url: "https://fidoalliance.org/fdo-functional-certification/"
kind: "html"
sha256: "fa72bbddf8f1416348331e4ec57d4743d984a5acfeff41836ae548dfaabd613c"
snapshot: "2026-11-17"
---

# FDO Functional Certification

Source: https://fidoalliance.org/fdo-functional-certification/ (live text: `python3 scripts/resources.py read fdo-functional-certification`)

## Summary

Describes the two required steps of FDO Functional Certification. Conformance is self-run with the FDO Conformance Test Suite (open source on GitHub), which has three tools: DO services are tested on TO0/TO2, Rendezvous servers on TO0/TO1, and Devices on TO1/TO2. Official runs are flagged in the tool. Interoperability testing is fully remote at FDO interop events, with a dashboard that tracks DO/RV/Device pairings. Prerequisites: one NDA per company, a certification application per implementation, completed conformance, no changes to the implementation before the event, and registration at least 7 days ahead. Events are meant to run at least every 90 days for active spec versions.

The page is inconsistent: one passage says conformance results must be confirmed 14 days before an event, the prerequisite list says 7. As of the snapshot the event schedule only names 2025 windows (June/July, November/December), so it looks outdated.

**Look here for:**
- What the FDO conformance tools test, and where to get them → Conformance Self-Validation Testing `#conformance-self-validation-testing`
- Prerequisites and deadlines for an interop event → Interoperability Testing `#interoperability-testing`
- Upcoming event dates and registration → FDO Interoperability Events `#fdo-interoperability-events`

## Outline

- FDO Functional Certification `#fdo-functional-certification`
  - FIDO Device Onboard Functional Certification Process `#fido-device-onboard-functional-certification-process`
  - Conformance Self-Validation Testing `#conformance-self-validation-testing`
  - Interoperability Testing `#interoperability-testing`
    - FDO Interoperability Events `#fdo-interoperability-events`
