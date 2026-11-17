# FIDO document catalog

Built 2026-11-16. 77 document versions. Each line is one document (lineage); versions in **bold** are the latest catalogued. Status in braces comes from the FIDO certification pages.
Open a page with `python3 scripts/fido.py show <doc_id> --version <v>`.

## ctap — FIDO2 Client to Authenticator Protocol (CTAP)

- `fido-client-to-authenticator-protocol` — Client to Authenticator Protocol (CTAP). Versions: 2.0, 2.1, 2.1-errata, 2.2, **2.3**. CTAP (Client to Authenticator Protocol) 2.3 is the current FIDO Alliance specification for how a client platform talks to a roaming authenticator.
- `fido-client-to-authenticator-protocol-errata-list` — CTAP 2.1 Errata. Versions: **2.1**. This is the FIDO Alliance errata list for CTAP 2.1, dated 2022-06-21.

## webauthn — W3C Web Authentication (WebAuthn)

- `webauthn` — Web Authentication: An API for accessing Public Key Credentials - Level 3. Versions: 2 {superseded by Level 3}, **3** {current W3C Recommendation}. Web Authentication Level 3 is the current W3C Recommendation (2026-08-25) for the browser API that lets web applications create and use scoped public key credentials (passkeys) to authenticate users.

## sr — Authenticator Security Requirements and Authenticator Certification (L1-L3+)

- `fido-authenticator-allowed-cryptography-list` — FIDO Authenticator Allowed Cryptography List. Versions: 1.5.1 {ACTIVE, no expiry (L3/L3+)}, 1.6 {ACTIVE until 2027-01-13}, **1.7** {ACTIVE}. Companion list to the Security and Privacy Requirements.
- `fido-authenticator-allowed-restricted-operating-environments-list` — FIDO Authenticator Allowed Restricted Operating Environments List. Versions: 1.5.1 {ACTIVE, no expiry (L3/L3+)}, 1.6 {ACTIVE until 2027-01-13}, **1.7** {ACTIVE}. Companion to the Security and Privacy Requirements.
- `fido-authenticator-certification-policy` — FIDO Authenticator Certification Policy. Versions: **1.4.1** {latest published (the certification-levels page still links v1.3 PDF)}. The rules of the FIDO Authenticator Certification Program.
- `fido-authenticator-metadata-requirements` — FIDO Authenticator Metadata Requirements. Versions: 1.5.1 {ACTIVE, no expiry (L3/L3+)}, 1.6 {ACTIVE until 2027-01-13}, **1.7** {ACTIVE}. Lists which Metadata Statement fields are mandatory for Authenticator Certification, grouped as functional, security and biometric fields, each with a short note on when it applies.
- `fido-authenticator-security-requirements` — FIDO Authenticator Security and Privacy Requirements. Versions: 1.5.1 {ACTIVE, no expiry; required for L3/L3+ (CTAP 2.1 only, GP FIDO2 SE companion program)}, 1.6 {ACTIVE until 2027-01-13}, **1.7** {ACTIVE}. The central document of FIDO Authenticator Certification.
- `fido-l1plus-application-of-attack-potential` — Application of attack potential to FIDO L1+ Authenticator. Versions: **1.5.1** {latest published}. The rating method labs use when evaluating L1+ authenticators, which are software authenticators protected by software techniques such as code obfuscation and white-box cryptography.

## bio — Biometric Component Certification

- `fido-biometric-component-certification-policy` — FIDO Biometrics Certification Policy. Versions: **1.5** {ACTIVE}. The Biometric Component Certification Policy sets out how FIDO runs its biometric certification programs: the Biometric Component program (BCC) and, since v1.5, Face Verification for Remote Identity Verification (IdV Face).
- `fido-biometrics-requirements` — FIDO Biometrics Requirements. Versions: 4.1 {ACTIVE until 2027-03-31}, **5.0** {ACTIVE}. The FIDO Biometrics Requirements define the performance and presentation-attack criteria, and the laboratory test procedures, for two FIDO biometric certification programs: the Biometric Component for FIDO authenticators (BCC; the abstract calls it BCA) and Face Verification for Remote Identity Verification (IdV Face).

## cert — Certification program policies and server requirements

- `fido-functional-certification-policy` — Functional Certification. Versions: **1.3.9** {ACTIVE}. The Functional Certification Program Policy governs FIDO functional (conformance and interoperability) certification for U2F, UAF and FIDO2 servers, clients and authenticators.
- `fido-server-requirements` — Server Requirements (WebAuthn Level 3 and CTAP2.3). Versions: **2.3** {ACTIVE (FIDO2 servers: WebAuthn L3 + CTAP 2.3)}. The FIDO2 Server Requirements bring together, in one place, the WebAuthn rules that apply to a FIDO2 server (relying-party side).

## mds — Metadata Service and Metadata Statements

- `fido-convenience-metadata-service` — FIDO Convenience Metadata Service. Versions: **1.0**. The Convenience Metadata Service defines a lightweight feed with only display information for authenticators and passkey providers.
- `fido-metadata-service` — FIDO Metadata Service. Versions: **3.1.1**. The FIDO Metadata Service (MDS) specification defines how relying parties get authenticator metadata from FIDO. The MDS publishes a single signed BLOB, a JWS-signed JWT, at a well-known URL (mds.fidoalliance.org).
- `fido-metadata-statement` — FIDO Metadata Statement. Versions: **3.1.1**. The FIDO Metadata Statement specification defines the JSON document that describes an authenticator model, so that servers and relying parties can interoperate with it and make risk decisions.

## uaf — FIDO UAF (Universal Authentication Framework)

- `fido-uaf-apccbor` — FIDO UAF Android Protected Confirmation Assertion Format. Versions: **1.2**. This UAF 1.2 document defines the APCV1CBOR assertion scheme, which uses Android Protected Confirmation (APC) to carry out UAF transaction confirmation.
- `fido-uaf-apdu` — FIDO UAF APDU. Versions: 1.1, **1.2**. The UAF APDU specification maps UAF Authenticator Commands onto ISO 7816-4 APDUs so that a UAF authenticator can be built on a Secure Element (UICC, eSE, microSD and similar).
- `fido-uaf-asm-api` — FIDO UAF Authenticator-Specific Module API. Versions: 1.1, **1.2**. The ASM API specifies the interface between a UAF Client and an Authenticator-Specific Module (ASM).
- `fido-uaf-authnr-cmds` — FIDO UAF Authenticator Commands. Versions: 1.1, **1.2**. UAF Authenticator Commands defines the normative behaviour of a UAF authenticator at its lowest interface.
- `fido-uaf-client-api-transport` — FIDO UAF Application API and Transport Binding Specification. Versions: 1.1, **1.2**. The UAF Application API and Transport Binding Specification defines how a relying party's web page or native app talks to the UAF Client, and how UAF messages travel to the FIDO Server.
- `fido-uaf-overview` — FIDO UAF Architectural Overview. Versions: 1.1, **1.2**. The UAF Architectural Overview is the non-normative entry point to the UAF specification set.
- `fido-uaf-protocol` — FIDO UAF Protocol Specification. Versions: 1.1, **1.2**. The UAF Protocol Specification is the core normative UAF document.
- `fido-uaf-reg` — FIDO UAF Registry of Predefined Values. Versions: 1.1, **1.2**. The UAF Registry of Predefined Values collects the identifiers and constants that only UAF uses.
- `fido-uaf-webauthn` — FIDO UAF WebAuthentication Assertion Format. Versions: **1.2**. This UAF 1.2 document defines the WAV1CBOR assertion scheme, which lets a WebAuthn/CTAP2 authenticator be used through the UAF protocol.

## u2f — FIDO U2F (Universal 2nd Factor)

- `fido-u2f-authenticator-transports-extension` — FIDO U2F Authenticator Transports Extension. Versions: **1.2**. Defines an optional, non-critical X.509 extension that lets a U2F authenticator state in its attestation certificate which transports it supports, so relying parties can tailor their UI. The attestation certificate must be X.509 v3 and DER-encoded, profiled on RFC 5280.
- `fido-u2f-bt-protocol` — FIDO Bluetooth® Specification v1.0. Versions: **1.2**. Specifies how U2F messages travel over Bluetooth Low Energy (titled FIDO Bluetooth Specification v1.0 inside the U2F 1.2 suite).
- `fido-u2f-hid-protocol` — FIDO U2F HID Protocol Specification. Versions: **1.2**. Specifies U2FHID, the framing that carries U2F raw messages over USB using the HID class.
- `fido-u2f-implementation-considerations` — FIDO U2F Implementation Considerations. Versions: **1.2**. Short guidance note for people building U2F tokens, clients and relying-party servers.
- `fido-u2f-javascript-api` — FIDO U2F JavaScript API. Versions: **1.2**. Defines the JavaScript API that relying-party web pages used to reach U2F tokens through the browser before WebAuthn.
- `fido-u2f-nfc-protocol` — FIDO NFC Protocol Specification v1.0. Versions: **1.2**. Short specification of how a FIDO client talks to a U2F authenticator over NFC. No extra framing is added: commands are the U2F raw message APDUs, in short or extended length encoding.
- `fido-u2f-overview` — Universal 2nd Factor (U2F) Overview. Versions: **1.2**. Non-normative introduction to FIDO Universal 2nd Factor (U2F) 1.2, meant as the first read before the detailed U2F specifications.
- `fido-u2f-raw-message-formats` — FIDO U2F Raw Message Formats. Versions: **1.2**. Normative definition of the transport-independent U2F messages exchanged between a FIDO client and a U2F token, encoded as ISO 7816-4 style APDUs (short or extended length).

## common — Common specifications (shared by UAF, U2F, FIDO2)

- `fido-appid-and-facets` — FIDO AppID and Facet Specification. Versions: 1.1, 1.2, **2.1**. Defines the AppID and FacetID model that scopes UAF and U2F credentials to an application.
- `fido-ecdaa-algorithm` — FIDO ECDAA Algorithm. Versions: 1.1, 1.2, **2.1**. Specifies FIDO ECDAA, an attestation scheme based on elliptic-curve Direct Anonymous Attestation with bilinear pairings over Barreto-Naehrig curves.
- `fido-glossary` — FIDO Technical Glossary. Versions: 1.1, 1.2, **2.1**. The FIDO Alliance glossary of normative technical terms, shared by UAF, U2F, FIDO2 (CTAP/WebAuthn) and the certification documents.
- `fido-registry` — FIDO Registry of Predefined Values. Versions: 1.1, 1.2, 2.1, 2.2, **2.3**. The FIDO Registry of Predefined Values: the numeric and string constants for authenticator characteristics shared by UAF, FIDO2 and the Metadata Service.
- `fido-security-ref` — FIDO Security Reference. Versions: 1.1, 1.2, **2.1**. Security analysis of the FIDO protocols: UAF, U2F, and FIDO2 (CTAP and WebAuthn).

## fdo — FIDO Device Onboard (FDO)

- `fido-device-onboard` — FIDO Device Onboard Specification. Versions: 1.0, 1.1, **2.0**. FIDO Device Onboard (FDO) 2.0 is the current version of FIDO's automatic onboarding protocol.
- `pv4fdo` — Path Verification for FDO (PV4FDO). Versions: **1.0**. Path Verification for FDO (PV4FDO) 1.0 is an optional companion to FIDO Device Onboard.

## cx — Credential Exchange (CXF)

- `cxf` — Credential Exchange Format. Versions: 1.0, **1.0-errata**. The Credential Exchange Format (CXF) 1.0 defines a JSON data model for moving a user's credentials between credential providers, such as password managers and passkey providers.
