# jules-mcp

A small Model Context Protocol (MCP) bridge that lets Codex interact with Google Jules through the official Jules REST API.

## Goal

Expose Jules as a set of MCP tools so Codex can:

- discover Jules-connected GitHub repositories
- start Jules coding sessions
- inspect session state and activity
- send follow-up instructions or answer Jules questions
- approve plans explicitly
- retrieve completed outputs and pull-request links

The Jules API is currently `v1alpha`, so this project keeps all Jules-specific HTTP details behind a small client layer.

## Safety defaults

- `JULES_API_KEY` is read from the environment and must never be committed.
- New sessions require plan approval by default.
- Automatic PR creation is opt-in per session.

## Requirements

- Python 3.10+
- `uv` or another Python package manager
- A Jules API key from Jules settings
- At least one GitHub repository connected to Jules
- Codex with MCP client support

## Install

```bash
git clone https://github.com/jbolt25/jules-mcp.git
cd jules-mcp
uv sync
```

Set the Jules API key.

PowerShell:

```powershell
$env:JULES_API_KEY="your-key-here"
```

bash/zsh:

```bash
export JULES_API_KEY="your-key-here"
```

Run the server directly:

```bash
uv run jules-mcp
```

The default transport is stdio, which is what Codex expects for a local MCP server.

## Codex configuration

Add a server entry to `~/.codex/config.toml` and replace the working directory with the local clone path:

```toml
[mcp_servers.jules]
command = "uv"
args = ["run", "jules-mcp"]
cwd = "C:\\path\\to\\jules-mcp"
env_vars = ["JULES_API_KEY"]
```

Then restart Codex and verify the Jules MCP tools are visible.

## MCP tools

The initial server exposes:

- `jules_list_sources`
- `jules_list_sessions`
- `jules_start`
- `jules_status`
- `jules_activity`
- `jules_send`
- `jules_approve_plan`
- `jules_result`

Example intent from Codex:

> Start a Jules session on `owner/repo` from `main` to fix the BACnet scanner race condition. Require plan approval and do not auto-create a PR.

When Jules reaches a state that requires feedback, Codex can read the activity stream, present the question to the user, and send the response back through `jules_send`.

## Development

```bash
uv sync --extra dev
uv run mcp dev src/jules_mcp/server.py
```

## Architecture

```text
User
  |
  v
Codex
  |
  | MCP / stdio
  v
jules-mcp
  |
  | HTTPS + x-goog-api-key
  v
Jules REST API
  |
  v
Jules coding session
```
