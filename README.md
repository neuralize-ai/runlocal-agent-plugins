# Runlocal agent plugins

Let Codex or Claude Code prepare and upload a model graph from your ML codebase
through the Runlocal HTTP API. Private weights stay in your environment.

## Install

For Codex, run in your terminal:

```sh
codex plugin marketplace add neuralize-ai/runlocal-agent-plugins
codex plugin add runlocal@runlocal
```

For Claude Code, run inside Claude:

```text
/plugin marketplace add neuralize-ai/runlocal-agent-plugins
/plugin install runlocal@runlocal
```

Start a new agent session in your ML project, then ask:

> Prepare this model graph for Runlocal using its HTTP API. Keep private weights
> local, review every artifact, validate the bundle, then upload it.

The skill can be selected automatically. You can also invoke `$runlocal` in
Codex or `/runlocal:runlocal` in Claude Code. To prepare without sending data,
ask the agent to stop after the upload preview.

The plugin needs no Runlocal CLI, Python package, MCP server, or background hook.
It reads the live API guide and schemas, then uses an existing environment API
key or the documented WorkOS browser device flow. Model export still uses the
project's own ML stack; the plugin cannot prove that an arbitrary export contains
no private values.

See the [Runlocal docs](https://www.runlocal.ai/docs/agents).

## Update

```sh
codex plugin marketplace upgrade
codex plugin add runlocal@runlocal
```

In Claude Code, use `/plugin marketplace update runlocal`, then
`/plugin update runlocal@runlocal`. Start a new session after an update.

## Structure

```text
.agents/plugins/marketplace.json  --> Codex catalog
.claude-plugin/marketplace.json   --> Claude catalog
plugins/runlocal/
  .codex-plugin/plugin.json      --> Codex metadata
  .claude-plugin/plugin.json     --> Claude metadata
  skills/runlocal/SKILL.md       --> shared workflow
                                      |
                                      v
                              API discovery + live guide
                                      |
                                      v
                         schemas --> validate --> upload
```

Keep the shared skill concise. Detailed commands, schemas, examples, limits, and
authentication instructions come from the live API. Both manifests and the
Claude catalog entry use the same plugin version.

## Validate a change

```sh
python3 scripts/check.py
claude plugin validate --strict plugins/runlocal
claude plugin validate --strict .claude-plugin/marketplace.json
```

Also test installation through both clients. For a workflow check, use a
temporary ML project, fetch API discovery and validate a request. Test uploads
only with an authorized test account, then remove test data through the service's
test tooling.
