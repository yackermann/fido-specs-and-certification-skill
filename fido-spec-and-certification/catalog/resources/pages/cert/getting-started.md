---
id: "getting-started"
source: "cert"
title: "Getting Started"
url: "https://fidoalliance.org/certification/getting-started/"
kind: "html"
sha256: "ee90385aee6c55e0e6a7be428740e0ead2d8159c4314b6dd834850086ed944e7"
snapshot: "2026-11-17"
---

# Getting Started

Source: https://fidoalliance.org/certification/getting-started/ (live text: `python3 scripts/resources.py read getting-started`)

## Summary

The entry page for FIDO Functional Certification. It says which specifications can be certified (UAF, U2F and FIDO2 for servers, clients and authenticators), that every implementation must pass conformance self-validation and interoperability testing, and that authenticators must additionally reach at least Authenticator Certification Level 1. It explains the rules for retiring old spec versions: a version becomes available once a valid interop event can be held (two implementations per class from different companies), and the previous version is sunset no sooner than 6 months later for servers and 18 months for clients/authenticators.

As of the snapshot, the version table lists FIDO2 1.0 and no FIDO2 2.x / CTAP 2.1 row, so it looks stale. The policy table lists Functional Certification Policy 1.3.0 to 1.3.9, with 1.3.9 active, and the change in each version.

**Look here for:**
- Which spec versions are certifiable, and their sunset dates → Supported Specification Versions `#supported-specification-versions`
- Which Functional Certification Policy version applies, and what changed → Functional Certification Policy Versions `#functional-certification-policy-versions`
- Where the authenticator security-level policy lives → Authenticator Certification Policy and Requirements `#authenticator-certification-policy-and-requirements`

## Outline

- Getting Started `#getting-started`
    - Supported Specification Versions `#supported-specification-versions`
    - Functional Certification Policy Versions `#functional-certification-policy-versions`
    - Authenticator Certification Policy and Requirements `#authenticator-certification-policy-and-requirements`

## Linked documents

- 1.3.9: https://fidoalliance.org/wp-content/uploads/2021/10/Functional_Certification_Program_Policy_v1.3.9_FINAL.pdf (catalogued: `fido-functional-certification-policy 1.3.9`)
- 1.3.8: https://fidoalliance.org/wp-content/uploads/2021/03/Functional_Certification_Program_Policy_v1.3.8_10202020_FINAL.pdf
- 1.3.7: https://fidoalliance.org/wp-content/uploads/2019/07/Functional_Certification_Program_Policy_v1.3.7_09252018_FINAL.pdf
- 1.3.6: https://fidoalliance.org/wp-content/uploads/Functional_Certification_Program_Policy_v1.3.6_08132018_FINAL.pdf
- 1.3.4: https://fidoalliance.org/wp-content/uploads/Functional_Certification_Program_Policy_v1.3.4_20180306_FINAL.pdf
- 1.3.3: https://fidoalliance.org/wp-content/uploads/Functional_Certification_Program_Policy_v1.3.3.pdf
- 1.3.2: https://fidoalliance.org/wp-content/uploads/Functional_Certification_Program_Policy_v1.3.2.pdf
- 1.3.1: https://fidoalliance.org/wp-content/uploads/Functional_Certification_Program_Policy_v1.3.1-2.pdf
- 1.3.0: https://fidoalliance.org/wp-content/uploads/FunctionalCertificationProgramPolicy_v1.3.0.pdf
