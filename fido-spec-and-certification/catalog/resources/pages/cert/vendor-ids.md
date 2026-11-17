---
id: "vendor-ids"
source: "cert"
title: "Vendor IDs"
url: "https://fidoalliance.org/certification/functional-certification/vendor-ids/"
kind: "html"
sha256: "e8dcf8ba17d47d0f21e068d817091c3178d39725bc77791825e226781c5380f7"
snapshot: "2026-11-17"
---

# Vendor IDs

Source: https://fidoalliance.org/certification/functional-certification/vendor-ids/ (live text: `python3 scripts/resources.py read vendor-ids`)

## Summary

Explains the FIDO-assigned Vendor ID, which the page equates with the AAID used in the specs. Only companies with a UAF authenticator need one, and they must register before running conformance self-validation; U2F implementations and UAF servers or clients do not (the conformance page adds that FIDO2 implementations don't either). Assigned IDs are published on this page unless the vendor asks for a confidential ID, which stays hidden until its functional certification goes public. The list itself sits in an embedded external database and is not in the page text.

## Outline

- Vendor IDs `#vendor-ids`
