---
id: "ctt-uaf-server-conformance-test-api"
source: "ctt"
title: "Conformance tools docs: UAF/Server/Conformance-Test-API"
url: "https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/UAF/Server/Conformance-Test-API.md"
kind: "markdown"
sha256: "15ebcb095319fc64134f6425a5596cffe498a6fd7edf546f69551629bcd0aaf2"
snapshot: "2026-11-17"
---

# Conformance tools docs: UAF/Server/Conformance-Test-API

Source: https://github.com/fido-alliance/conformance-test-tools-resources/blob/main/docs/UAF/Server/Conformance-Test-API.md (live text: `python3 scripts/resources.py read ctt-uaf-server-conformance-test-api`)

## Summary

Specifies the API adapter a UAF server vendor must expose so the conformance tools can test it. It follows the UAF v1.1 Client API and Transport spec. There are two POST endpoints. `/get` takes an operation (Reg, Auth or Dereg) and a JSON context string with the username, and returns a UAF request with a status code. It also accepts an optional transaction text for Auth, and a specific AAID or a "deregister all" flag for Dereg. `/respond` takes the client's UAF response and returns a status code. The page includes IDL definitions, example payloads, success and error codes, and sample fetch calls. Questions go to conformance-tools@fidoalliance.org.

Watch for some copy errors. The SendUAFResponse IDL repeats ReturnUAFRequest, the registration sample call posts to `/get` instead of `/respond`, and the example registration request has op Auth. The page has no headings, so read it directly.

## Outline

_(no headings)_
