---
id: "ctt-fido2-automation"
source: "ctt"
title: "Conformance tools docs: FIDO2/Automation — Test Automation"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Automation.md"
kind: "markdown"
sha256: "81c634a54f6dfd3890a3e65cc7e3bf5473926f8fd14ba74a39c2c64f73939665"
snapshot: "2026-11-17"
---

# Conformance tools docs: FIDO2/Automation — Test Automation

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Automation.md (live text: `python3 scripts/resources.py read ctt-fido2-automation`)

## Summary

Describes the test automation option in the desktop FIDO Conformance Tools, available from v1.7.25 and mostly for the CTAP 2.1 module. When it is enabled in Advanced options, the tools stop showing dialogs and instead send HTTP POST requests to localhost:3000 for user presence and power cycling. Custom peripheral hardware is expected to handle these requests and reply only after the action finishes. A failed or late reply to a power-cycle request counts as a failure. A results request at the end carries pass and fail counts, and it is separate from the official results submission. Startup flags can auto-start the last configuration and pre-answer the display and U2F-compatibility prompts.

**Look here for:**
- How do I turn automation on? → How to toggle test automation `#how-to-toggle-test-automation`
- Which HTTP requests must my rig handle? → Automation API `#automation-api`
- Which command-line flags skip prompts? → Startup arguments `#startup-arguments`

## Outline

- Test Automation `#test-automation`
  - What does it do? `#what-does-it-do`
  - How to toggle test automation `#how-to-toggle-test-automation`
  - Automation API `#automation-api`
  - Startup arguments `#startup-arguments`
