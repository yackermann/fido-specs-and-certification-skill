---
id: "ctt-fdo-pre-interop-dashboard-api"
source: "ctt"
title: "Conformance tools docs: FDO/Pre-Interop/Dashboard-API"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/Dashboard-API.md"
kind: "markdown"
sha256: "1b281445cb4fa8fec9f99572102a101ca92f764e937f706d58fedf8b54d6a1d4"
snapshot: "2026-11-17"
---

# Conformance tools docs: FDO/Pre-Interop/Dashboard-API

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/Dashboard-API.md (live text: `python3 scripts/resources.py read ctt-fdo-pre-interop-dashboard-api`)

## Summary

Short API reference for the FDO pre-interop dashboard logger, used by FDO implementations to report onboarding events during interop preparation. It gives the dashboard domains (including an HTTP-only one), the logger path and protocol version 101, and refers to the FDO specs for transport rules and error definitions. Requests must be CBOR with a FIDO-issued authorization token. The single command, SubmitEvent (type 10), sends the device GUID, which transfer-ownership protocol ran (TO0, TO1 or TO2) and the matching nonce, defined in CDDL; success returns HTTP 200, failures return an FDOError.

**Look here for:**
- Required headers and token → Authorization and Header `#authorization-and-header`
- SubmitEvent message structure → SubmitEvent, Type 10 `#submitevent-type-10`

## Outline

  - Authorization and Header `#authorization-and-header`
  - Commands `#commands`
    - SubmitEvent, Type 10 `#submitevent-type-10`
