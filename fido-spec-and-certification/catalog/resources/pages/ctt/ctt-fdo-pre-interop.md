---
id: "ctt-fdo-pre-interop"
source: "ctt"
title: "Conformance tools docs: FDO/Pre-Interop — FIDO Alliance Pre-Interop Requirements"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/README.md"
kind: "markdown"
sha256: "42db4fbbbc758e8a78dd292259bf40919b6e5802395e9f6c410c43d7bec59b58"
snapshot: "2026-11-17"
---

# Conformance tools docs: FDO/Pre-Interop — FIDO Alliance Pre-Interop Requirements

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/README.md (live text: `python3 scripts/resources.py read ctt-fdo-pre-interop`)

## Summary

README from the FIDO conformance test tools repository describing how FDO interoperability testing works, for Device, Rendezvous (RV) and Device Onboarding (DO) implementers. Testing is run as matchmaking: each participant gets an access token, the DO reports its own state to a referee dashboard and passes the device's token to the device in ServiceInfo, and the device reports successful onboarding, so a pass requires every party to have interacted. The page gives the RV server and dashboard hostnames (with HTTP-only variants), a pointer to the dashboard API reference, minimum crypto support (SHA256/384 HMAC and hash, ECDH key exchange, X509 and COSE keys, ES256/ES384, AES128 CTR with HMAC-SHA256), the PEM voucher-plus-unencrypted-key format with a sample, and the `fido_alliance:dev_conformance` ServiceInfo key that carries the token.

**Look here for:**
- How results are reported in FDO interop → Dashboard API `#dashboard-api`
- Which RV and dashboard hosts to use → URLs `#urls`
- What algorithms an implementation must support → Minimum requirements `#minimum-requirements`
- How vouchers must be encoded → Voucher encoding format `#voucher-encoding-format`
- Which ServiceInfo key carries the token → Conformance Service Info `#conformance-service-info`

## Outline

- FIDO Alliance Pre-Interop Requirements `#fido-alliance-pre-interop-requirements`
  - Dashboard API `#dashboard-api`
  - URLs `#urls`
  - Minimum requirements `#minimum-requirements`
  - Voucher encoding format `#voucher-encoding-format`
  - Conformance Service Info `#conformance-service-info`
