---
name: runlocal
description: Prepare, check, validate, upload, list, or download Runlocal model graph requests through the HTTP API. Use when the user wants to submit a model graph from an ML codebase while keeping trained weights and source code private.
---

# Runlocal

Use Runlocal's HTTP API directly. No Runlocal CLI or Python package is required.
An upload stores a model graph request for inspection; it does not start
optimization.

## Privacy first

The user's data is theirs. Nothing leaves their machine without their explicit
permission for that specific transmission. Before any request that carries
their data, show exactly what would be sent and ask: the request text, sample
inputs, JSON graphs, optional source artifacts, and anything that describes
their source code, including file names, function names, notes, and summaries.
Permission to prepare is not permission to send. Permission to check is not
permission to validate or upload.

Runlocal does not accept trained weights: values learned from data, and
anything derived from them, such as a folded scale or a merged bias. Declare
those as weights, private and supplied at run time, so their values never
appear in any file, external data, sample, graph, note, or check.
Everything else that decides what the model computes must be sent, and must
be exact: initializers and constants that are not trained, such as shapes,
axes, indices, masks, scales fixed by the architecture, and tables computed by
formula. The weight policy is where each tensor is sorted into one of these
two, and it is the decision that matters most: a constant declared as a
weight strips meaning the model needs, and a weight declared as a constant
leaks training. Decide from the tensor's origin in the source, and when its
origin is unclear, ask. If a faithful export that separates the two cannot be
produced, stop and explain the blocker rather than sending an approximation.

Sort by origin, per tensor:

- Learned by training, or computed from learned values: a weight. This
  includes quantized weights, and the scales and zero points computed from
  them.
- Computed from calibration data, such as activation scales and zero points:
  a weight unless the user says it may be sent.
- Fixed by the architecture or computed by formula, such as shapes, axes,
  indices, masks, rotary tables, and constant scales: a constant, sent in
  the file with its exact values.
- A float tensor produced by folding a dequantization or any other operation
  over a weight is a weight that has leaked. Undo the fold.

A quantized model needs its contract to say so. As written, the quantize and
dequantize pairs run in float, which forbids the fused integer kernels the
model was quantized for; the `quantized` numerics term grants them, under an
accumulation precision and an output tolerance. The tolerance is the user's
decision about their model's accuracy: ask for it, in steps of the output's
scale for quantized outputs and absolute plus relative for float outputs, and
never invent it. The term applies only where the model already quantizes;
nothing else may be quantized on Runlocal's side.

Precision over convenience. The JSON graph must describe the model exactly:
never guess a shape, a dtype, an operator's meaning, a tied weight, or a piece
of state. Whatever you cannot establish, raise with the
user and record in the request as an unknown, each with what would resolve
it: an export the user could allow, a fact they could supply, a file they
could share, or a narrower scope. The report from the check endpoint lists the
unknowns it finds; bring those to the user the same way.

## Discover the current contract

Start at the stable service manifest:

```text
https://www.runlocal.ai/.well-known/runlocal.json
```

Fetch its `discovery` URL, then fetch that discovery document. Read the linked
`agent_guide`. Fetch the linked request, graph, bundle, validation report, and
operator extension schemas. Fetch the ONNX operator catalog and the public
examples too. Treat those live resources as the authority for endpoints,
fields, encoding, authentication, limits, and result handling. Do not
reconstruct the protocol from this skill or require an installed package.

## Prepare the model graph

Inspect the selected inference entry point and use the project's existing ML
environment for export and local comparisons. Ask which graph to use only when
the intended boundary is unclear.

Preserve input/output behavior, dynamic dimensions, state, tied weights, and
every constant the computation depends on. Keep trained weights and values
derived from them local, declared as weights supplied at run time. Removing or
zeroing weights after export does not preserve the program, and neither does
dropping a constant. Record unsupported regions and unknown facts as unknowns,
with the possible resolutions, instead of guessing.

Every operator the model applies is registered in the request, standard
operators included, with the opset it runs at, how many nodes apply it, and
its source of meaning. Resolve a standard operator from the service's pinned
ONNX catalog by domain, operator type, overload, and imported opset. Use the
catalog's input, output, attribute, default, and type rules. Report an
unsupported version as unresolved. Do not write a new description of a
standard operator.

For another domain, prefer a local function made from resolved operators when
it describes the behavior exactly. Resolve every operator in that function,
including operators in `If`, `Loop`, and `Scan` graph bodies. If a local
function cannot describe the behavior, use a versioned extension that follows
the live operator extension schema. Bundle its schema and specification. State
its inputs, outputs, attributes, shape rules, valid inputs, defaults, boundary
behavior, numerical behavior, permitted nondeterminism, and state effects. Add
a reference implementation and tests when practical. State whether the
reference implementation defines the behavior or implements the separate
specification. Resolve every operator that the extension uses.

An explicit unknown is valid while the request is being prepared, but it
blocks each optimization scope that can reach it. Never treat an unknown as
`Identity`, assume it is pure, or infer its behavior from a similar name. A
link can help a reader find source code or documentation. It does not define
an operator. The API checks the registry and every dependency against the JSON
graphs.

Every graph body names an authoritative JSON document that follows the live
graph schema. It states every input, output, initializer, node, attribute,
subgraph, and local function. It also states each tensor's type, data location,
and byte count, and it never includes a weight's values. Build it with the
project's model tools. An ONNX file or another source artifact is optional. If
one helped make the graph, list it as the body's source. It records provenance
only and does not define the computation. The API checks the JSON graph against
the request. It does not need the source artifact and cannot check that the
graph matches it.

Build the request JSON and exact object catalog from the live schemas. Preserve
the protocol's field names even when the product calls the submission a model
graph. Compare a weight-free export against the original locally when the
project can execute both. Add a `source_equivalence` check that names the exact
contract digest, subjects, procedure, cases, results, and evidence artifacts.
Include boundary cases from the source behavior. For control flow, include
both branches, zero iterations, early termination, and state changes when they
apply. For neighborhood operators, include empty neighborhoods, boundary
distances, duplicate points, and ordering when they apply. Record replacement
tests under `replacement_equivalence`. Finite tests are evidence; they do not
prove behavior for every input.

## Check before encoding

POST the request text with the JSON graphs and without optional source files
to the discovered check endpoint. It stores nothing and answers a validation
report with status 200 whether or not the request passed. Read every finding,
pointer, repair, check result, and digest. Read each operator's definition,
node validation, and backend support separately. Read the same separate fields
for the model, each example, and each optimization target, together with source
evidence, replacement evidence, and readiness. A resolved operator can still
be unsupported. A supported operator can still have an invalid export. Finite
evidence does not make an unresolved scope ready. Fix every diagnostic, then
check again, until the diagnostics list is empty. Only then encode the bundle.
Raise with the user what the report leaves incomplete: the unknowns it names,
unsupported targets, and checks it could not run.

## Review every byte

Before any network request, review the request text and every object that will
be encoded into the bundle, and show the user what will be sent: object names,
sizes, and digests, which weights stay local, what the notes and names reveal
about their code, and the unresolved unknowns. Never print private tensor
values. Neither the schema nor the server can prove that submitted artifacts
contain no weight values; that review is yours and the user's.

The check endpoint transmits the request text and every file included with it,
and the validation endpoint transmits every byte of the bundle, even though
neither persists the request. If the user explicitly asked to check, validate,
or upload, that instruction supplies the corresponding authorization for what
they named; otherwise wait until the request is reviewable, then ask before
each step.

## Authenticate

Prefer an existing `RUNLOCAL_API_TOKEN` and send it as `Authorization: Bearer
<token>` without displaying it. Otherwise follow the live guide's WorkOS browser
device flow and keep the resulting access token out of source files, logs, and
conversation output. Verify the selected identity with the live guide's
`/api/v1/auth/status` route.

## Validate and upload

Encode the transport exactly as the bundle schema requires. POST it first to
the discovered validation endpoint. A rejection lists every finding, not only
the first; fix them all before uploading, and do not blindly retry rejected
input. On success, POST the same reviewed body to the discovered requests
endpoint.

An identical upload is safe to retry. A conflict means the same name and
version already identify different content; inspect it and choose a truthful
new version rather than silently changing scope. Use bounded exponential
backoff only for `429` and temporary `5xx` responses.

Report the returned request ID, revision digest, verification scope, server
validation report, and a workspace link constructed from the discovery
document. Do not describe wire or digest verification as semantic validation,
privacy validation, or optimization.

For list, read, and download requests, use the discovered request endpoints
directly and preserve pagination cursors as opaque values. Verify downloaded
object bytes against the retained catalog before using them.
