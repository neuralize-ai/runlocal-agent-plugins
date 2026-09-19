---
name: runlocal
description: Prepare model workloads for Runlocal from an ML codebase, assess gaps and evidence, and check or submit requests when asked. Also use to inspect or retrieve existing Runlocal requests. Keep private weights local.
---

# Runlocal

Turn the user's model code into an honest model workload request. Keep private
values local and make each gap visible. A submission stores a request for
inspection. It does not start an optimization.

This skill is public and short. The Runlocal API is private and has the detail:
formats, schemas, rules, operators, examples, and limits. Read them from the API
each time. Do not use a remembered payload or protocol version, and do not
invent a CLI, an exporter, or a service capability.

## The user's machine

Runlocal uses two folders. Do not mix them.

- `~/.runlocal/` is the Runlocal config folder, in the user's home folder. It
  holds API keys only, in `~/.runlocal/credentials.json`. The sign-in guide
  gives the file format and the access modes.
- `<project>/.runlocal/` is the Runlocal project folder. Put all the work for
  the project here: request sources, prepared files, frozen revisions, receipts,
  results, and notes. The authoring guide of the API gives the layout. Git
  tracks this folder, so it never holds a credential, a trained weight, a
  private sample, or a machine path. Its ignored `local/` folder holds private
  bindings and drafts.

## Authentication

There are two ways. Use the first one that is available.

1. An API key. Read the `RUNLOCAL_API_KEY` environment variable, then the key
   file in `~/.runlocal/`.
2. Device sign-in. Follow the sign-in guide. The user completes the sign-in in a
   browser. Keep the session token in memory only, renew it as the guide states,
   and use it for the whole task.

Check the account with the authentication status route. If the account has no
invite, stop and tell the user. Do not repeat a sign-in that was refused.

After a device sign-in, you can offer an API key for future use. Create and
store one only with the user's approval of its purpose and its location. Never
show a credential. Never write one to a project, a request, the chat, or a log.

## API discovery

1. GET https://www.runlocal.ai/.well-known/runlocal.json with no credentials. It
   names the sign-in guide and the discovery URL.
2. Read the sign-in guide, which is public, and authenticate.
3. GET the discovery URL. Follow its links to the agent guide, the authoring
   guide, the schemas, the operator catalogs, the examples, and the work menu.

Expect each other API route to need credentials. A 401 response names the
sign-in guide. If the API is not available, or the user does not want to sign in
yet, continue the local inspection. Report that you did not check the request
against the current contract.

## Establish the task

Find what the user wants: inspection, local preparation, a remote check, a
submission, or retrieval. Local preparation is not permission to upload. Read
the code before you ask questions. Establish the model variant, the callable
boundary, the inputs and sizes, the state, and the intended improvement. Do not
replace the requested model with a smaller component.

## Prepare from the actual source

- Use the project's own model tools, and a capture path that the agent guide
  supports. Do not rebuild an algorithm by hand to fit a format.
- Preserve the configuration, the input domain, the control flow, the state, and
  the identity and sharing of weights.
- If a capture fails, record the region that has no support. Ask before you
  narrow the scope or add a translated replacement.
- Do not choose a tolerance, a meaning, or an input limit only to pass a check.
  Ask the user, or record the gap.
- Keep these apart: what you observed, assumed, and tested, and what is missing.
  A finite comparison is evidence. It is not proof for all inputs.

## Review before you send

A remote check transmits data, although it stores nothing. Act only inside the
destination, the data, and the operation that the user approved, and ask before
you extend that scope.

Trained weights and the values derived from them stay local: quantized codes,
scales, zero points, and calibration results. A removed or zeroed value is not a
faithful privacy measure. Review the real request and files, because graphs,
names, notes, and samples can disclose information. Show a short preview first:
the scope, the files and sizes, the values kept local, and the open gaps.

## Check, submit, and report

Follow the agent guide for the check and upload sequence. Fix errors inside the
scope. Do not erase an unknown or change the model to get a clean report, and
do not retry an invalid request that you did not change.

Before a submission, read the work menu. Show the user the kinds of work that
the provided information permits, and the next item that each other kind needs.
State a want in the request only when the user asks for that kind of work.

Finish with the scope, the location of the artifacts, the checks and their
results, the open assumptions, and the next useful action. For a submission,
give the returned identity and the workspace link. An accepted upload is not
proof of correct meaning, of privacy, or of an optimization.
