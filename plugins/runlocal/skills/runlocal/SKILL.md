---
name: runlocal
description: Sign in to Runlocal and reach its HTTP API with an API key. Use for any Runlocal task. After the sign-in, the agent guide of the API gives the steps of the work.
---

# Runlocal

This skill tells how to sign in to Runlocal and find its API. It is public and
short. The API is private, and its agent guide gives each step of the work.
Read the guide from the API each time. Do not use a remembered route, payload,
or version, and do not invent a CLI or a service capability.

## The user's machine

`~/.runlocal/` is the config folder, in the user's home folder. It holds API
keys only. Never put a key in a project, a request, the chat, or a log.

## Authentication

There are two ways: an API key that the user has, or a device sign-in that the
user completes in a browser. The sign-in guide has the steps and names where a
key is. Keep a session token in memory only. If the account has no invite, stop
and tell the user.

Offer to keep an API key only after a sign-in, and only with the user's approval
of its purpose and its place. Never show a credential.

## API discovery

1. GET https://www.runlocal.ai/.well-known/runlocal.json with no credentials. It
   names the sign-in guide and the discovery URL.
2. Read the sign-in guide, which is public, and authenticate.
3. GET the discovery URL with the key, and read the agent guide that it names.
   Follow the agent guide for the work that the user asks for.

Each other route needs credentials. If the API is not available, or the user
does not want to sign in, tell the user, and send nothing.

## Before you send

Send data to Runlocal only for the work that the user asked for, and ask before
an upload. Keep trained weights and other private values on the user's machine.
