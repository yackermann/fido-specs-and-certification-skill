---
id: "authenticator-level-2"
source: "cert"
title: "Authenticator Level 2"
url: "https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-2/"
kind: "html"
sha256: "61b090cd34ea848117a8a41052940f31b8b291185572b59dbb985473569583ec"
snapshot: "2026-11-17"
---

# Authenticator Level 2

Source: https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-2/ (live text: `python3 scripts/resources.py read authenticator-level-2`)

## Summary

Describes Authenticator Certification Level 2, which targets protection against basic, scalable attacks. An L2 authenticator must use a solution from the FIDO Allowed Restricted Operating Environment and Allowed Cryptography lists; pure Rich OS software authenticators and authenticators without attestation cannot reach L2 and are pointed to L1.

Next steps depend on the starting point: clients and servers only do Functional Certification; a new authenticator starts with Functional Certification (interop testing checks no L2 security requirements) and then follows the Authenticator Certification Policy; an already functionally certified authenticator goes straight to the Vendor Questionnaire. In both authenticator cases a FIDO Accredited Security Laboratory chosen by the vendor evaluates the L2 questionnaire, and a certification account is required. Fees are per implementation and due before the certificate; FIDO charges nothing for the lab evaluation itself, the lab sets its own price.

**Look here for:**
- What disqualifies an implementation from L2 → Authenticator Level 2 `#authenticator-level-2`
- Path for a new authenticator → New Authenticator Implementation `#new-authenticator-implementation`
- Path for an already certified authenticator → Functionally Certified Authenticator Implementation `#functionally-certified-authenticator-implementation`
- Who pays the lab and where fees are listed → L2 Certification Fees `#l2-certification-fees`

## Outline

- Authenticator Level 2 `#authenticator-level-2`
  - Next Steps `#next-steps`
    - Client or Server Implementation `#client-or-server-implementation`
    - New Authenticator Implementation `#new-authenticator-implementation`
    - Functionally Certified Authenticator Implementation `#functionally-certified-authenticator-implementation`
  - L2 Certification Fees `#l2-certification-fees`
    - Laboratory Security Evaluation Fees `#laboratory-security-evaluation-fees`
    - Implementer Dashboard `#implementer-dashboard`
