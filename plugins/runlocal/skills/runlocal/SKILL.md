---
name: runlocal
description: Prepare model workloads for Runlocal from an ML codebase, assess gaps and evidence, and check or submit requests when asked. Also use to inspect or retrieve existing Runlocal requests. Keep private weights local.
---

# Runlocal

Turn the user's model code into an honest, useful model workload request.
Preserve its behavior, keep private values local, and make uncertainty visible.
Submitting a request stores it for inspection; it does not start optimization.

## Establish the task

Determine whether the user wants inspection, local preparation, remote checking,
submission, or retrieval. Do not turn local preparation into an upload workflow.
For an existing request, use the read path; do not repeat model preparation.

Inspect the code and configuration before asking questions. Establish the model
variant, callable boundary, relevant inputs and sizes, execution mode, state,
and intended improvement. Ask for choices the code cannot establish. Do not
silently substitute a smaller component for the requested model. Keep a named
component's coverage distinct from coverage of the full model.

## Discover the current contract

Start at https://www.runlocal.ai/.well-known/runlocal.json and follow its
discovery URL. Read the linked agent guide. Fetch the schemas, capabilities,
and public examples relevant to this task, following the returned links.

These resources own the accepted formats, field definitions, semantic rules,
tools, authentication, endpoints, and limits. Use them instead of remembered
payloads or a protocol version written elsewhere. Do not invent a CLI, exporter,
adapter, or service capability. If discovery is unavailable, local inspection
can continue, but report that current compatibility has not been checked.

## Prepare from the actual source

Use the project's existing model tools and environment. Preserve the selected
configuration, input domain, control flow, state, weight identity and sharing,
and constants that determine behavior. Separate the source reference from any
captured graph or proposed replacement.

Use supported capture or export tooling. Do not manually reconstruct an
algorithm just to fit a submission format. If capture fails, identify the
affected computation and preserve its original implementation where the current
contract permits. Record unsupported regions. Ask before narrowing scope or
introducing a translated replacement; label that replacement as a candidate,
not a direct export.

Use declared weight interfaces to keep supplied values separate from computation.
Synthetic weights can support local tests without disclosing trained weights;
they do not establish trained-model accuracy. Do not hide a cast, transpose, or
other transformation in a weight binding.

Treat trained quantized codes, scales, zero points, and values derived from
calibration as private. Keep them local unless the user has approved their exact
disclosure. A local quantization tensor binding is relative to the weight source
selected by the example. Confirm that this source can supply the complete stored
tensor set. A sample, generated, or unbound weight source cannot stand in for
that private storage. Use a public quantization-tensor file only for exact values
that are safe to send.

Keep the function body as the float computation. The function's quantization
overlay is the only statement that a weight or graph value is quantized. Name
each logical target and its stored codes and parameters there. Use a storage
extension when packing, tensor order, or another physical layout needs a
logical-to-physical mapping. A quantized tensor type or native QDQ nodes alone
do not mark the function as quantized.

Quantization does not add a fusion permission. There is no fusion field. An
optimizer may dequantize first, keep quantized values, or use a fused kernel if
the result follows the function contract. Do not change the float body to request
one of those choices.

When the live API offers ONNX QDQ lift, use it only through the documented local
or HTTP path. Review every finding. A supported lift needs complete direct Q to
DQ, or DynamicQ to DQ, in the main graph under standard catalog-resolved ONNX
semantics. One unsupported use leaves that graph unchanged. Do not manually
remove QDQ nodes, infer parameters from names, or accept a partial lift. Static
lifted parameters become an exact public content-addressed file, so include them
in the disclosure review. If exact initializer values are missing, keep the graph
unchanged and report the gap.

If a required tolerance, semantic choice, or input restriction is not established,
ask or record the gap. Do not choose it merely to make a check pass.

## State what is known and what was checked

Distinguish source observations, assumptions, missing information, successful
capture, source comparisons, and backend support. One does not establish another.
Use the current contract's evidence and uncertainty fields where supported.
Scope each concern to the affected computation, explain its consequence, and
state what would resolve it. A subjective confidence estimate is not proof or
a measured probability. Do not invent fields to record one.

Compare the prepared computation with the original locally when both can run.
Choose cases from the source behavior, including relevant boundaries and control
paths. Record the exact artifacts, procedure, cases, results, and limitations.
Distinguish source-equivalence tests from tests of an optimized replacement.
Finite comparisons are evidence, not proof for all inputs. If tests cannot run,
say which were not run and why.

## Review disclosure before transmission

Determine each tensor's origin. Keep trained weights and private derived values
local. Retain exact public constants required by the computation; removing or
zeroing values is not a faithful privacy measure. Resolve unclear origins before
sending the affected artifacts.

Review the actual request and selected files, not only their declared roles.
Graphs, names, notes, samples, and source files can disclose information too.
Show a concise transmission preview: scope, files and sizes, private values kept
local, and remaining gaps. Do not print private tensor values or credentials.

Remote checking and validation transmit data even when they do not store it.
Act within the user's explicit authorization for the destination, data, and
operation. Ask before expanding that scope; do not ask again for an unchanged
action already authorized. Local preparation alone authorizes no transmission.
Uploading executable content does not authorize running it remotely.

## Authenticate when needed

Use `RUNLOCAL_API_KEY` as the API-key environment variable. Reuse an available
key from it or a valid session token for the intended account. Do not put a
session token in `RUNLOCAL_API_KEY` or display the variable's value.
If neither is available, follow the live guide's device-code login flow and let
the user complete browser sign-in. Verify the account through the documented
authentication-status check. Use the session token for the requested task;
do not start a new login for every POST or other authenticated request.

Keep session credentials in memory. Follow the live guide for renewal when
available, and request a new sign-in only when the session cannot be renewed.
An access denial is not a reason to repeat login indefinitely. Authentication
does not grant permission to transmit more data than the user approved.

For future use, offer an API key as an optional convenience, not a requirement
for the current task. Create and persist one only with the user's approval of
its purpose and secure storage location. Use a descriptive key name and a
documented, session-authenticated creation interface. If the live guide does not
expose one, direct the user to the workspace's key settings; do not call
undocumented backend functions. Do not write credentials to the repository,
request artifacts, chat, or logs. If approved secure storage is unavailable,
continue with the session instead of creating a key. Make an approved stored
key available to future requests through `RUNLOCAL_API_KEY`.

## Check and hand off

Follow the live guide for local checks and authorized remote operations. Treat
invalid content, unresolved meaning, unsupported execution, and missing evidence
as different outcomes. Fix errors within scope. Do not erase unknowns or change
the model to obtain a clean report. Stop and explain when progress needs a new
user decision or unavailable capability. Do not retry unchanged invalid requests.

For submission, use the guide's validation and upload sequence. If reviewed
content changes, review the change and confirm it remains within authorization.
Use documented authentication without exposing secrets. For downloads, verify
content identity before use and do not execute retrieved code merely to inspect it.

Finish with the included and excluded scope, local or submitted artifact location,
checks and their results, unresolved assumptions or blockers, and the next useful
action. For a submission, include the returned identity and workspace link.
Describe verification only as far as the evidence supports; upload success is
not proof of semantic correctness, privacy, or optimization.
