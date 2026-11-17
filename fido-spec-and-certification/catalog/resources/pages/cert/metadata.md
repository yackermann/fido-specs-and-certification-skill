---
id: "metadata"
source: "cert"
title: "FIDO Metadata Service (MDS) Overview"
url: "https://fidoalliance.org/metadata/"
kind: "html"
sha256: "ed7ac2b8fa36c1d0f3709a9dfe81ad928e43917b41754e226d8a29ada7d5924c"
snapshot: "2026-11-17"
---

# FIDO Metadata Service (MDS) Overview

Source: https://fidoalliance.org/metadata/ (live text: `python3 scripts/resources.py read metadata`)

## Summary

Landing page for the FIDO Metadata Service (MDS), aimed at both relying parties and authenticator vendors. It explains that vendors publish metadata statements through the MDS Portal and these end up in the signed MDS3 BLOB, which servers download and cache to check whether an authenticator is FIDO Certified, apply policy on its capabilities or certification level, react to revocations and show proper names and icons.

For relying parties it links the public BLOB endpoint (no token needed; monthly refresh with caching is suggested), the GlobalSign R46 root used to verify the BLOB signature, the Convenience Metadata Service for display names and logos, the three relevant specifications, and the usage terms for RPs and for developers. For vendors it links MyMDS registration, the portal user guides for Vendor Admin and Vendor User roles, a support contact and the submission terms.

**Look here for:**
- Where to download the BLOB and which root certificate verifies it → MDS Implementation `#mds-implementation`
- Which specs define the BLOB and statement format → Developer Resources `#developer-resources`
- Licence terms for using MDS data → Policy and Licensing `#policy-and-licensing`
- How a vendor submits metadata statements → Resources for Authenticator Vendors `#resources-for-authenticator-vendors`

## Outline

- FIDO Alliance Metadata Service `#fido-alliance-metadata-service`
  - How it Works `#how-it-works`
  - Get started `#get-started`
    - Resources for Relying Parties and Developers `#resources-for-relying-parties-and-developers`
      - MDS Implementation `#mds-implementation`
      - Developer Resources `#developer-resources`
      - Policy and Licensing `#policy-and-licensing`
    - Resources for Authenticator Vendors `#resources-for-authenticator-vendors`
      - Policy `#policy`
  - MDS Updates Sign-Up `#mds-updates-sign-up`
