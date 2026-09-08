# Runlocal agent plugins

Let Codex or Claude Code prepare and upload a model specification from your ML
codebase. Private weights stay in your environment as runtime parameters.

## Install

Install the CLI once:

```sh
uv tool install --python 3.12 "runlocal-external-interface[onnx]>=0.2.0"
rx login
```

For Codex, run in your terminal:

```sh
codex plugin marketplace add kinghchan/runlocal-agent-plugins
codex plugin add runlocal@runlocal
```

For Claude Code, run inside Claude:

```text
/plugin marketplace add kinghchan/runlocal-agent-plugins
/plugin install runlocal@runlocal
```

Start a new agent session in your ML project, then ask:

> Prepare this model for Runlocal. Keep private weights local, check the export,
> and explain what will be uploaded. Then upload it to my workspace.

The skill can be selected automatically. You can also invoke `$runlocal` in
Codex or `/runlocal:runlocal` in Claude Code. To prepare without sending data,
ask the agent to stop after the upload preview.

The plugin does not install Python dependencies or sign in at installation time.
It uses the CLI's existing session or environment API key. No MCP server or
background hook is required. Model export depends on the project's ML stack;
the tool does not automatically strip arbitrary weight files.

See the [Runlocal docs](https://dropzone-eight-rust.vercel.app/docs/agents).

## Update

```sh
uv tool upgrade runlocal-external-interface
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
                                   rx guide + schemas
                                      |
                                      v
                                   rx CLI --> Runlocal API
```

Keep the shared skill concise. Detailed commands and schemas come from the
installed CLI so that they match its version. Both manifests and the Claude
catalog entry use the same plugin version.

## Validate a change

```sh
python3 scripts/check.py
claude plugin validate --strict plugins/runlocal
claude plugin validate --strict .claude-plugin/marketplace.json
```

Also test installation through both clients. For a workflow check, use a
temporary ML project, prepare and validate a request, and inspect the dry run.
Test uploads only with an authorized test account. Verify the returned request
ID through `rx list`, then remove test data through the service's test tooling.
