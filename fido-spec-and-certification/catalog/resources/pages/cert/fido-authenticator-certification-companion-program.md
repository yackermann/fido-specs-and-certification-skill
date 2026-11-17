---
id: "fido-authenticator-certification-companion-program"
source: "cert"
title: "Companion Programs"
url: "https://fidoalliance.org/certification/authenticator-certification-levels/fido-authenticator-certification-companion-program/"
kind: "html"
sha256: "7c50d10134c887d74d7e461ff5aa929dc5c043ff24a507ab8cd7be7f70744d41"
snapshot: "2026-11-17"
---

# Companion Programs

Source: https://fidoalliance.org/certification/authenticator-certification-levels/fido-authenticator-certification-companion-program/ (live text: `python3 scripts/resources.py read fido-authenticator-certification-companion-program`)

## Summary

Explains Companion Programs: outside certification schemes whose results can be reused at Authenticator Levels 3 and 3+, usually to cover the underlying platform (for example IC plus Java Card OS) beneath the FIDO authenticator application. The vendor gets an SRWG-prepared guidance document and a mapping table that links companion-programme requirements to the FIDO Security and Privacy Requirements. The vendor then writes a Security Target for the application on its own, maps it against the certified platform's ST with a coverage rationale, justifies when the application can rely on platform security functions, and submits the evidence to a FIDO Accredited Lab. FIDO advises against seeking L3/L3+ without a companion programme.

As of the snapshot the approved programmes are Common Criteria with secure-element Protection Profiles at AVA_VAN.3 or higher (IC PP0084, Java Card PP0099, U2F PP0096) and GlobalPlatform TEE (TEE PP, AVA_VAN.AP3). FIPS 140-3 and EMVCo are listed as future programmes.

**Look here for:**
- How companion evidence is mapped for L3/L3+ → Companion Programs `#companion-programs`
- Which programmes and Protection Profiles are accepted → Current Approved FIDO Authenticator Certification Companion Programs: `#current-approved-fido-authenticator-certification-companion-programs`
- Programmes still in development → Certification Companion Programs for Future Development: `#certification-companion-programs-for-future-development`

## Outline

- Companion Programs `#companion-programs`
    - Current Approved FIDO Authenticator Certification Companion Programs: `#current-approved-fido-authenticator-certification-companion-programs`
    - Certification Companion Programs for Future Development: `#certification-companion-programs-for-future-development`

## Linked documents

-  factors, claiming an AVA_VAN.3 (or higher) vulnerability assessment. This includes: - IC PP (PP0084: https://www.commoncriteriaportal.org/files/ppfiles/pp0084b_pdf.pdf
- ) - Java Card PP (PP0099: https://www.commoncriteriaportal.org/files/ppfiles/ANSSI-CC-profil_PP-2010-03en.pdf
- ) - U2F PP (PP0096: https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Zertifizierung/Reporte/ReportePP/pp0096b_pdf.pdf?__blob=publicationFile&v=2
