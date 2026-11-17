---
id: "ctt-fido2-server"
source: "ctt"
title: "Conformance tools docs: FIDO2/Server — Running FIDO2 Server tests"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Server/README.md"
kind: "markdown"
sha256: "a43a56abc33509781859758d19624e29bc18bca50d467bb3cef73b29d84a3774"
snapshot: "2026-11-17"
---

# Conformance tools docs: FIDO2/Server — Running FIDO2 Server tests

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Server/README.md (live text: `python3 scripts/resources.py read ctt-fido2-server`)

## Summary

Guide to running the FIDO2 server conformance tests in the FIDO Conformance Tools. There are five test groups: MakeCredential request and response, GetAssertion request and response, and Metadata Service tests. Setup: serve the server over HTTPS, download the test metadata and load it into the server, register the server URL with the certification-infrastructure MDS3 service (or legacy MDS2) and configure the MDS endpoints it hands out, then enter the server URL in the tool. An inspector can capture traffic.

Results can only be submitted when all five groups are run together in one pass with no failures. The test item list explains P (expect success) and F (expect error) cases and covers options generation, client data, attestation object, algorithms and each attestation format. As of the snapshot it still mentions MDS2 and the android-safetynet format, so parts may be outdated.

**Look here for:**
- MDS registration and server setup → Preparations and Configurations `#preparations-and-configurations`
- Why the submit button is missing → Submit Results `#submit-results`
- Which attestation formats are tested → "MakeCredential Response" `#makecredential-response`
- Metadata checks → "Metadata Service Tests" `#metadata-service-tests`

## Outline

- Running FIDO2 Server tests `#running-fido2-server-tests`
  - FIDO2 Server Tests Options `#fido2-server-tests-options`
  - Preparations and Configurations `#preparations-and-configurations`
  - Run tests `#run-tests`
  - Test Results `#test-results`
  - Submit Results `#submit-results`
  - Test Items `#test-items`
    - "MakeCredential Request" `#makecredential-request`
      - Server-ServerPublicKeyCredentialCreationOptions-Req-1 `#server-serverpublickeycredentialcreationoptions-req-1`
    - "MakeCredential Response" `#makecredential-response`
      - Server-ServerAuthenticatorAttestationResponse-Resp-1 `#server-serverauthenticatorattestationresponse-resp-1`
      - Server-ServerAuthenticatorAttestationResponse-Resp-2 `#server-serverauthenticatorattestationresponse-resp-2`
      - Server-ServerAuthenticatorAttestationResponse-Resp-3 `#server-serverauthenticatorattestationresponse-resp-3`
      - Server-ServerAuthenticatorAttestationResponse-Resp-4 `#server-serverauthenticatorattestationresponse-resp-4`
      - Server-ServerAuthenticatorAttestationResponse-Resp-5 `#server-serverauthenticatorattestationresponse-resp-5`
      - Server-ServerAuthenticatorAttestationResponse-Resp-6 `#server-serverauthenticatorattestationresponse-resp-6`
      - Server-ServerAuthenticatorAttestationResponse-Resp-7 `#server-serverauthenticatorattestationresponse-resp-7`
      - Server-ServerAuthenticatorAttestationResponse-Resp-8 `#server-serverauthenticatorattestationresponse-resp-8`
      - Server-ServerAuthenticatorAttestationResponse-Resp-9 `#server-serverauthenticatorattestationresponse-resp-9`
      - Server-ServerAuthenticatorAttestationResponse-Resp-A `#server-serverauthenticatorattestationresponse-resp-a`
      - Server-ServerAuthenticatorAttestationResponse-Resp-B `#server-serverauthenticatorattestationresponse-resp-b`
    - "GetAssertion Request" `#getassertion-request`
      - Server-ServerPublicKeyCredentialGetOptionsResponse-Req-1 `#server-serverpublickeycredentialgetoptionsresponse-req-1`
    - "GetAssertion Response" `#getassertion-response`
      - Server-ServerAuthenticatorAssertionResponse-Resp-1 `#server-serverauthenticatorassertionresponse-resp-1`
      - Server-ServerAuthenticatorAssertionResponse-Resp-2 `#server-serverauthenticatorassertionresponse-resp-2`
      - Server-ServerAuthenticatorAssertionResponse-Resp-3 `#server-serverauthenticatorassertionresponse-resp-3`
    - "Metadata Service Tests" `#metadata-service-tests`
      - Server-ServerAuthenticatorAttestationResponse-Resp-1 `#server-serverauthenticatorattestationresponse-resp-1-1`
