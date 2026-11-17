---
id: "ctt-fido2-server-conformance-test-api"
source: "ctt"
title: "Conformance tools docs: FIDO2/Server/Conformance-Test-API — FIDO2: Conformance testing server API"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Server/Conformance-Test-API.md"
kind: "markdown"
sha256: "cdc52787ebc258ea4e05dd48b0f24b2fe617a5f7bfee1de65f5133e4a52aa321"
snapshot: "2026-11-17"
---

# Conformance tools docs: FIDO2/Server/Conformance-Test-API — FIDO2: Conformance testing server API

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FIDO2/Server/Conformance-Test-API.md (live text: `python3 scripts/resources.py read ctt-fido2-server-conformance-test-api`)

## Summary

Defines the REST interface that a FIDO2 server must expose so that the FIDO2 server conformance tools (and the interop web app) can drive it. The interface is non-normative, intended for testing only, and can be removed from production builds; it borrows WebAuthn's IDL but deliberately differs from it in places. Registration uses POST `/attestation/options` to get creation options, then POST `/attestation/result` with the attestation response. Authentication uses POST `/assertion/options` and `/assertion/result` in the same way. Every reply carries `status` (`ok` or `failed`) and `errorMessage`, which must not be empty when the call fails. The server validates results per WebAuthn §7.1/§7.2. Each step comes with example JSON, the error format and sample fetch code, followed by IDL for each message.

**Look here for:**
- Which endpoints the server must implement, and the call order → Registration Overview `#registration-overview`, Authentication Overview `#authentication-overview`
- Example request/response bodies → Registration Example: Credential Creation Options `#registration-example-credential-creation-options`, Authentication Example: Credential Get Options `#authentication-example-credential-get-options`
- Required fields in the options request → ServerPublicKeyCredentialCreationOptionsRequest `#serverpublickeycredentialcreationoptionsrequest`
- Success/error response format → ServerResponse `#serverresponse`

## Outline

- FIDO2: Conformance testing server API `#fido2-conformance-testing-server-api`
  - Contents `#contents`
  - Introduction `#introduction`
  - Registration `#registration`
    - Registration Overview `#registration-overview`
    - Registration Examples `#registration-examples`
      - Registration Example: Credential Creation Options `#registration-example-credential-creation-options`
      - Registration Example: Authenticator Attestation Response `#registration-example-authenticator-attestation-response`
    - Registration Primary IDL `#registration-primary-idl`
      - ServerPublicKeyCredentialCreationOptionsRequest `#serverpublickeycredentialcreationoptionsrequest`
      - ServerPublicKeyCredentialCreationOptionsResponse `#serverpublickeycredentialcreationoptionsresponse`
      - ServerAuthenticatorAttestationResponse `#serverauthenticatorattestationresponse`
    - Registration Supporting IDL `#registration-supporting-idl`
      - ServerPublicKeyCredential `#serverpublickeycredential`
      - ServerPublicKeyCredentialUserEntity `#serverpublickeycredentialuserentity`
      - ServerPublicKeyCredentialDescriptor `#serverpublickeycredentialdescriptor`
  - Authentication `#authentication`
    - Authentication Overview `#authentication-overview`
    - Authentication Examples `#authentication-examples`
      - Authentication Example: Credential Get Options `#authentication-example-credential-get-options`
      - Authentication Example: Authenticator Assertion Response `#authentication-example-authenticator-assertion-response`
    - Authentication IDL `#authentication-idl`
      - ServerPublicKeyCredentialGetOptionsRequest `#serverpublickeycredentialgetoptionsrequest`
      - ServerPublicKeyCredentialGetOptionsResponse `#serverpublickeycredentialgetoptionsresponse`
      - ServerAuthenticatorAssertionResponse `#serverauthenticatorassertionresponse`
  - Common `#common`
    - Common IDL `#common-idl`
      - ServerResponse `#serverresponse`
