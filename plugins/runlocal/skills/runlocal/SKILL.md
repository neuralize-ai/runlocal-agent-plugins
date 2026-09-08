---
name: runlocal
description: Prepare, validate, upload, list, or download Runlocal model specifications with the rx CLI. Use when the user wants to submit a model from their ML codebase to Runlocal, keeping private weights local.
---

# Runlocal

Use the installed `rx` CLI to prepare the selected inference program and manage
its requests. An upload stores a model specification; it does not run optimization.

## Read the installed instructions

Run `rx --version` and `rx guide`. This skill requires
`runlocal-external-interface` 0.2.0 or newer. The guide and `rx schema authoring`
are the authority for the installed version's workflow and fields.

If the tool is missing, install it in a separate environment:

```sh
uv tool install --python 3.12 "runlocal-external-interface[onnx]>=0.2.0"
```

For an older installation, use `uv tool upgrade runlocal-external-interface`.
If `rx` is not on PATH, use `uv tool dir --bin` to locate it. Keep the customer's
ML environment and dependency versions intact. If uv is missing, follow
https://docs.astral.sh/uv/getting-started/installation/.

## Prepare the requested scope

For a new model, inspect its code and inference entry point. Ask which model
to use only if the intended boundary is unclear. Use the project's own ML
environment for export and local comparisons. Read `rx capabilities` and the
authoring schema; `rx example --out DIR` supplies a runnable starting point.

Preserve input/output behavior, dynamic dimensions, state, and shared parameter
identities. Keep private weights and derived private values local as explicit
runtime parameters. Removing or zeroing weights after export does not preserve
the program. A tensor can also be a legitimate public constant: review its origin.
Record unsupported regions and unknown facts as requirements instead of guessing.

Compare the parameterized export against the original model locally on supported
inputs. Describe the cases checked and any remaining gaps. Compile and validate
with `rx`; use the installed guide for exact commands and completeness policy.
For requests to list or download existing submissions, perform that operation
directly without preparing a new model.

## Review and send

Run `rx upload BUNDLE --dry-run` before an upload. It needs no authentication
and sends no data. Review the exact files, tensor findings, local-only parameters,
and validation scope. The preview is metadata only; it cannot prove that a model
contains no private values. Native ONNX inspection can print values, so keep
private tensor contents out of conversation output.

Summarize what will be sent and any unresolved requirements. If the user has
authorized that upload, proceed; otherwise ask after the bundle is reviewable.
Stop and repair or explain any unresolved private-data disclosure before sending.
Do not upload simply because the user asked to prepare or validate a model.

Use `rx auth status` to check the selected account. When login is needed, run
`rx login` and let the user complete browser authentication. For a remote
terminal, use `rx login --no-browser` and show its verification link and code.
Never ask for passwords or tokens in chat. An existing `RUNLOCAL_API_TOKEN`
takes precedence over the saved session; preserve the user's selected account
and API origin.

Run `rx upload BUNDLE`, then confirm the returned ID and revision digest in
`rx list` (follow pagination as needed). Report the request ID and workspace
link. On failure, use the CLI's structured diagnostics and repair actions.
Do not silently change a lineage, revision, or model scope to bypass a conflict.
