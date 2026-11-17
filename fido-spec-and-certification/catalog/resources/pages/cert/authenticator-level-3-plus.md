---
id: "authenticator-level-3-plus"
source: "cert"
title: "Authenticator Level 3+"
url: "https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-3-plus/"
kind: "html"
sha256: "efdbf8d75f85a6f1dcdf4c5a9284421cd4fd92d97de2ce59f46adffab1eb02fc"
snapshot: "2026-11-17"
---

# Authenticator Level 3+

Source: https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-3-plus/ (live text: `python3 scripts/resources.py read authenticator-level-3-plus`)

## Summary

Explains Authenticator Certification Level 3+ (L3+), which covers resistance to moderate- or high-effort software and hardware attacks, including chip-level attacks with professional lab equipment. The authenticator must use a solution from FIDO's Allowed Restricted Operating Environment and Allowed Cryptography lists. An authenticator on a Common Criteria certified secure element or TPM is the example given. Implementations that don't meet this are pointed to Level 2.

New implementations still need Functional Certification first, though no L3+ requirements are tested during interop. Already certified authenticators go straight to the Vendor Questionnaire. The questionnaire is evaluated by a FIDO Accredited Security Laboratory that the vendor picks. Biometric authenticators must hold Biometric Component Certification before starting. FIDO certificate fees are per implementation. FIDO charges nothing for the lab evaluation, but the lab sets its own price.

**Look here for:**
- What does L3+ require, and does my design qualify? → Authenticator Level 3+ `#authenticator-level-3`
- Who performs the security evaluation? → New Authenticator Implementation `#new-authenticator-implementation`
- Do I need biometric certification first? → Biometric Certification and Authenticator Certification Relationship `#biometric-certification-and-authenticator-certification-relationship`
- What does the lab evaluation cost? → Laboratory Security Evaluation Fees `#laboratory-security-evaluation-fees`

## Outline

- Authenticator Level 3+ `#authenticator-level-3`
  - Next Steps `#next-steps`
    - Client or Server Implementation `#client-or-server-implementation`
    - New Authenticator Implementation `#new-authenticator-implementation`
    - Functionally Certified Authenticator Implementation `#functionally-certified-authenticator-implementation`
    - Biometric Certification and Authenticator Certification Relationship `#biometric-certification-and-authenticator-certification-relationship`
  - Certification Fees `#certification-fees`
    - Laboratory Security Evaluation Fees `#laboratory-security-evaluation-fees`
    - Implementer Dashboard `#implementer-dashboard`
