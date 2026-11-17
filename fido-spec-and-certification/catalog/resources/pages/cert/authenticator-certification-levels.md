---
id: "authenticator-certification-levels"
source: "cert"
title: "FIDO Authenticator Certification Levels"
url: "https://fidoalliance.org/certification/authenticator-certification-levels/"
kind: "html"
sha256: "21b0159db2c5bbaad4a0899500f0995f32413630dba54d740c409aa4bb0c95ea"
snapshot: "2026-11-17"
---

# FIDO Authenticator Certification Levels

Source: https://fidoalliance.org/certification/authenticator-certification-levels/ (live text: `python3 scripts/resources.py read authenticator-certification-levels`)

## Summary

Hub page for FIDO Authenticator Certification. At least L1 is mandatory for UAF, U2F and FIDO2 authenticator certification, and higher levels include all lower-level requirements; as of the snapshot the supported levels are L1, L1+, L2, L3 and L3+. It links the policy, privacy principles, the Security Requirements and companion crypto, operating-environment and metadata lists (as of the snapshot v1.7 active, v1.6 active until a January 2027 sunset, v1.5.1 required for L3/L3+), VQ worksheets, the L3/L3+ Mapping Table worksheet and the FIAR template.

The process: create an account, finish Functional Certification (for L1 this includes L1 interoperability checks), get the application approved, then a security evaluation of the Vendor Questionnaire (L1, L2) or Mapping Table (L3, L3+) by the Security Secretariat (L1) or an accredited lab (L2 and up), report review, then the Certification Request and fees; trademark and MDS steps are optional. Two snapshot download links look mis-targeted (v1.5.1 crypto list, v1.7 metadata PDF).

**Look here for:**
- Which requirements document versions are current? → Policy and Requirements Documents `#policy-and-requirements-documents`
- Who performs the security evaluation at each level? → Security Evaluation `#security-evaluation`
- What is submitted after the evaluation report? → Report Review `#report-review`
- When to contact an accredited lab? → Preparation `#preparation`

## Outline

- Authenticator Security Levels `#authenticator-security-levels`
  - Policy and Requirements Documents `#policy-and-requirements-documents`
  - Authenticator Certification Process `#authenticator-certification-process`
  - High-Level Process Steps `#high-level-process-steps`
      - Preparation `#preparation`
      - Functional Certification Requirements `#functional-certification-requirements`
      - Authenticator Certification Application `#authenticator-certification-application`
      - Security Evaluation `#security-evaluation`
      - Report Review `#report-review`
      - Certification Issuance `#certification-issuance`
      - Trademark Usage (Optional) `#trademark-usage-optional`
      - Metadata Submission to MDS (Optional) `#metadata-submission-to-mds-optional`
  - Implementer Dashboard `#implementer-dashboard`

## Linked documents

- erns the Authenticator Certification Levels as part of the FIDO Certification Program. Download: PDF: https://fidoalliance.org/wp-content/uploads/2020/12/FIDO-Authenticator_Certification_Program_policy_v1.3_FINAL_September2020.pdf
- f the FIDO Certification Program and more generally all FIDO technical specifications. Download: PDF: https://fidoalliance.org/wp-content/uploads/2021/02/FIDO-Privacy-Principles.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-security-requirements-v1.7-rd-20260506.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-security-requirements-v1.6-fd-20250312.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-security-requirements-v1.5.1-fd-20251016.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-security-requirements-v1.5-fd-20211102.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-allowed-cryptography-list-v1.7-rd-20260506.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-allowed-cryptography-list-v1.6-fd-20250312.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-allowed-restricted-operating-environments-list-v1.7-rd-20260506.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-allowed-restricted-operating-environments-list-v1.6-fd-20250312.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-allowed-restricted-operating-environments-list-v1.5.1-fd-20251016.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-metadata-requirements-v1.6-fd-20250312.pdf
- PDF: https://fidoalliance.org/specs/fido-security-requirements/fido-authenticator-metadata-requirements-v1.5.1-fd-20251016.pdf
- ticator Vendors (Implementers) completing Authenticator Certification at L1 or L2. Download: Level 1: https://fidoalliance.org/wp-content/uploads/2025/10/FIDO_Authenticator_Certification-L1_VQ_20250827_RELEASE.xlsx
- Level 1+: https://fidoalliance.org/wp-content/uploads/2025/10/FIDO_Authenticator_Certification-L1-_VQ_20250827_RELEASE.xlsx
- Level 2: https://fidoalliance.org/wp-content/uploads/2025/10/FIDO_Authenticator_Certification-L2_VQ_20250827_RELEASE.xlsx
- Sample Vendor Questionnaire: https://fidoalliance.org/wp-content/uploads/2019/01/Authenticator_Sample_VQ_Answers.pdf
- icator Certification at L3 or L3+, depending on the selected Companion Program. Download: Level 3/3+: https://fidoalliance.org/wp-content/uploads/2025/10/FIDO_Authenticator_Certification-L3L3_VQ_20250827_RELEASE.xlsx
- enters) and submitted to the FIDO Security Secretariat. Download: FIDO Impact Analysis Report (FIAR): https://fidoalliance.org/wp-content/uploads/2019/03/FIDO_IAR_v1.0_RELEASE.docx
