---
id: "ctt-fdo-pre-interop-step-by-step"
source: "ctt"
title: "Conformance tools docs: FDO/Pre-Interop/Step-by-step — Pre-Interop Process Step-By-Step"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/Step-by-step.md"
kind: "markdown"
sha256: "232f8c5d5bf717b42eed0326551e92efe0ea5533bcdc96516c625b109069018f"
snapshot: "2026-11-17"
---

# Conformance tools docs: FDO/Pre-Interop/Step-by-step — Pre-Interop Process Step-By-Step

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/FDO/Pre-Interop/Step-by-step.md (live text: `python3 scripts/resources.py read ctt-fdo-pre-interop-step-by-step`)

## Summary

A step-by-step guide to the FDO pre-interop event for Device, Device Onboarding (DO) and Rendezvous (RV) vendors. The goal is to show that each Device/DO/RV triplet completes TO0, TO1 and TO2, with matching events logged to the FIDO FDO Interop Dashboard. Success means matching DO and RV logs for TO0 (same GUID and nonce), one RV log for TO1, and matching Device and DO logs for TO2. Each device must work with at least two RV vendors and two DO vendors, so device vendors bring two devices. Each DO must register with at least two RVs.

FIDO randomly assigns RVs to device vendors and vouchers to DOs. Vouchers are PEM files that include the last OVEntry private key. Vendors must support the Dashboard API and the conformance ServiceInfo module. Note that the page expands "DO" both as Device Onboarding Service and as Device Owner.

**Look here for:**
- What counts as a passing interop? → Measure of success `#measure-of-success`
- How many partner vendors must each device or DO test with? → FIDO Requirements `#fido-requirements`
- How must vouchers be encoded, and what must I support? → Voucher, SIM and Logger support `#voucher-sim-and-logger-support`
- Which nonce goes in each logger event? → Operational `#operational`

## Outline

- Pre-Interop Process Step-By-Step `#pre-interop-process-step-by-step`
  - Terms `#terms`
  - Entities involved `#entities-involved`
  - Goal `#goal`
  - Measure of success `#measure-of-success`
    - Expected Logs `#expected-logs`
    - FIDO Requirements `#fido-requirements`
  - Voucher, SIM and Logger support `#voucher-sim-and-logger-support`
  - Setup `#setup`
  - Operational `#operational`
