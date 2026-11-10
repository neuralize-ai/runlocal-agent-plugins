# Runlocal agent plugins

Let Codex or Claude Code sign in to Runlocal and use its HTTP API from your ML
codebase. Private weights stay in your environment.

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

Start a new agent session in your ML project and ask for the Runlocal task. You
can also invoke `$runlocal` in Codex or `/runlocal:runlocal` in Claude Code.

The plugin needs no Runlocal CLI, Python package, MCP server, or background
hook. The skill tells the agent how to sign in and find the API. After the
sign-in, the API gives the steps of the work.

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
  skills/runlocal/SKILL.md       --> sign-in and API discovery
```

Keep the skill to the sign-in, the keys, and API discovery. Everything else
comes from the API after the sign-in. Both manifests and the Claude catalog
entry use the same plugin version.

## Validate a change

```sh
python3 scripts/check.py
claude plugin validate --strict plugins/runlocal
claude plugin validate --strict .claude-plugin/marketplace.json
```
