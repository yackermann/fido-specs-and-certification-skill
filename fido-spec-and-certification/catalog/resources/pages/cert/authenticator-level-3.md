---
id: "authenticator-level-3"
source: "cert"
title: "Authenticator Level 3"
url: "https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-3/"
kind: "html"
sha256: "0813ac2f131febfa54cf94d394f89d53e736147a8a7f5afde97c7d583e283213"
snapshot: "2026-11-17"
---

# Authenticator Level 3

Source: https://fidoalliance.org/certification/authenticator-certification-levels/authenticator-level-3/ (live text: `python3 scripts/resources.py read authenticator-level-3`)

## Summary

Describes Authenticator Certification Level 3, which targets protection against enhanced-basic software and hardware attacks and requires the authenticator to use an entry on the Allowed Restricted Operating Environments and Allowed Cryptography lists. The page gives example designs (a hardened U2F token, UAF in a certified TEE, a FIDO2 authenticator with protected RAM).

New implementations start with Functional Certification; already functionally certified authenticators go straight to the security evaluation, which must be done by a FIDO accredited security lab of the vendor's choosing. Biometric authenticators at L3 or above must complete Biometric Component Certification first. Fees are per implementation and paid before issuance; the page links the fee pages rather than listing amounts, and lab costs are set by the lab. Note: this page calls the L3 input a Vendor Questionnaire, whereas the Authenticator Certification Levels page says L3/L3+ use a Mapping Table.

**Look here for:**
- What path does an already functionally certified authenticator take? → Functionally Certified Authenticator Implementation `#functionally-certified-authenticator-implementation`
- Is biometric certification needed first? → Biometric Component Certification and Authenticator Certification Relationship `#biometric-component-certification-and-authenticator-certification-relationship`
- Who charges for the lab evaluation? → Laboratory Security Evaluation Fees `#laboratory-security-evaluation-fees`

## Outline

- Authenticator Level 3 `#authenticator-level-3`
  - Next Steps `#next-steps`
    - Client or Server Implementation `#client-or-server-implementation`
    - New Authenticator Implementation `#new-authenticator-implementation`
    - Functionally Certified Authenticator Implementation `#functionally-certified-authenticator-implementation`
    - Biometric Component Certification and Authenticator Certification Relationship `#biometric-component-certification-and-authenticator-certification-relationship`
  - L3 Certification Fees `#l3-certification-fees`
    - Laboratory Security Evaluation Fees `#laboratory-security-evaluation-fees`
    - Implementer Dashboard `#implementer-dashboard`
