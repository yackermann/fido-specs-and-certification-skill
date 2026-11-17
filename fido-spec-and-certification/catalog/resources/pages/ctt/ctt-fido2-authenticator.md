---
id: "ctt-fido2-authenticator"
source: "ctt"
title: "Conformance tools docs: FIDO2/Authenticator — FIDO2 Testing"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Authenticator/README.md"
kind: "markdown"
sha256: "6e57f89fe10a7ddcf89cf3b766f927082356e9973a2bdc5142fb356ba2c386cd"
snapshot: "2026-11-17"
---

# Conformance tools docs: FIDO2/Authenticator — FIDO2 Testing

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Authenticator/README.md (live text: `python3 scripts/resources.py read ctt-fido2-authenticator`)

## Summary

Conformance-tool note for FIDO2 authenticator (security key) testing that covers only the CTAP 2.1+ enterprise attestation test. It gives the RP ID list the authenticator must be configured with and a test enterprise attestation certificate and private key to provision. Decoded, that test certificate expires on 3 November 2026, which is before the snapshot date, so the note may be outdated unless the tool accepts expired test material.

**Look here for:**
- How to configure an authenticator for the enterprise attestation test → Enterprise attestation (CTAP2.1+) `#enterprise-attestation-ctap21`

## Outline

- FIDO2 Testing `#fido2-testing`
    - Enterprise attestation (CTAP2.1+) `#enterprise-attestation-ctap21`
