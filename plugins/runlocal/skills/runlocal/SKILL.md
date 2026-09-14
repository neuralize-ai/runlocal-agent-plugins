---
name: runlocal
description: Prepare, validate, upload, list, or download Runlocal model graph requests through the HTTP API. Use when the user wants to submit a model graph from an ML codebase while keeping private weights local.
---

# Runlocal

Use Runlocal's HTTP API directly. No Runlocal CLI or Python package is required.
An upload stores a model graph request for inspection; it does not start
optimization.

## Discover the current contract

Start at:

```text
https://courteous-perch-757.eu-west-1.convex.site/api/v1
```

Fetch the discovery document, then read its `agent_guide` and fetch the linked
request schema, bundle schema, and example. Treat those live resources as the
authority for endpoints, fields, encoding, authentication, limits, and result
handling. Do not reconstruct the protocol from this skill or require an
installed package.

## Prepare the model graph

Inspect the selected inference entry point and use the project's existing ML
environment for export and local comparisons. Ask which graph to use only when
the intended boundary is unclear.

Preserve input/output behavior, dynamic dimensions, state, and shared parameter
identities. Keep private weights and derived private values local as explicit
runtime parameters. Removing or zeroing weights after export does not preserve
the program. A tensor can also be a legitimate public constant: review its origin.
Record unsupported regions and unknown facts as requirements instead of guessing.

Build the request JSON and exact object catalog from the live schemas. Preserve
the protocol's field names even when the product calls the submission a model
graph. Compare a parameterized export against the original locally when the
project can execute both, and describe the cases checked and remaining gaps.

## Review every byte

Before any network request, review the request text and every object that will
be encoded into the bundle. Summarize object sizes and digests, local-only
parameters, and unresolved requirements without printing private tensor values.
Neither the schema nor the server can prove that submitted artifacts contain no
private or derived weight values.

The validation endpoint transmits every supplied byte to Runlocal even though it
does not persist the request. A request to prepare locally does not authorize
validation or upload. If the user explicitly asked to validate or upload, that
instruction supplies the corresponding authorization; otherwise wait until the
bundle is reviewable before asking.

## Authenticate

Prefer an existing `RUNLOCAL_API_TOKEN` and send it as `Authorization: Bearer
<token>` without displaying it. Otherwise follow the live guide's WorkOS browser
device flow and keep the resulting access token out of source files, logs, and
conversation output. Verify the selected identity with the live guide's
`/api/v1/auth/status` route.

## Validate and upload

Encode the transport exactly as the bundle schema requires. POST it first to
the discovered validation endpoint. Fix schema or content failures before
uploading; do not blindly retry rejected input. On success, POST the same reviewed
body to the discovered requests endpoint.

An identical upload is safe to retry. A conflict means the same lineage and
revision already identify different content; inspect it and choose a truthful
new revision rather than silently changing scope. Use bounded exponential
backoff only for `429` and temporary `5xx` responses.

Report the returned request ID, revision digest, verification scope, and a
workspace link constructed from the discovery document. Do not describe wire or
digest verification as semantic validation, privacy validation, or optimization.

For list, read, and download requests, use the discovered request endpoints
directly and preserve pagination cursors as opaque values. Verify downloaded
object bytes against the retained catalog before using them.
