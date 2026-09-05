# Codex + Jules MCP: How to Use It

This guide explains how Codex should use the local Jules MCP server. The server lets Codex discover Jules-connected GitHub repositories, start and monitor Jules coding sessions, review plans, send follow-up messages, and retrieve completed results.

## Before using Jules

1. Restart Codex after changing MCP configuration.
2. Open a new local task and type `/mcp`.
3. Confirm that `jules` is listed as enabled.

The Jules API key is supplied through the local environment. Never paste it into a prompt, command, file, URL, Git commit, or Git note.

## Read-only requests

These requests do not start or change a Jules session:

```text
Use the Jules MCP to list my connected repositories. Do not start a session.
```

```text
Use Jules MCP to list my recent sessions. Do not send messages or change anything.
```

```text
Use Jules MCP to show the status and activity for session sessions/123. Read-only.
```

The corresponding tools are:

- `jules_list_sources`
- `jules_list_sessions`
- `jules_status`
- `jules_activity`

When starting a task, first use `jules_list_sources` and use the exact source ID it returns. A source ID looks like `github/jbolt25/bacnet_collector`.

## Starting a Jules session

Starting a session is a state-changing action. Ask for it explicitly and include the repository, branch, task, and safety settings:

```text
Use Jules MCP to start a session for github/jbolt25/bacnet_collector on the main branch.

Task: inspect the scanner batching logic and explain any race conditions.
Require plan approval. Do not create a PR automatically.
```

Jules sessions require plan approval by default, and automatic PR creation is disabled unless explicitly requested.

## Reviewing and approving a plan

After Jules reports a plan, inspect it before approving:

```text
Read the plan and activity for Jules session sessions/123. Do not approve it yet.
```

Only after the user explicitly approves the plan:

```text
Approve the plan for Jules session sessions/123.
```

The approval tool is `jules_approve_plan`.

## Sending follow-up instructions

Sending a message changes the session. Address the exact session and give the complete instruction:

```text
Send this feedback to Jules session sessions/123:
Keep the change limited to the scanner batching logic and add focused tests.
```

The tool is `jules_send`.

## Monitoring and retrieving results

Use status and activity while Jules works:

```text
Check the status and latest activity for Jules session sessions/123. Read-only.
```

When it finishes:

```text
Retrieve the completed result for Jules session sessions/123, including any pull-request link.
```

The result tool is `jules_result`.

## Tool safety rules for Codex

- Treat listing, status, activity, and result retrieval as read-only.
- Treat starting sessions, sending messages, and approving plans as state-changing.
- Do not call `jules_start` for an ambiguous request; ask for the repository, branch, and task details.
- Do not approve a plan unless the user explicitly asks for approval.
- Do not create a PR automatically unless the user explicitly requests it.
- Do not expose credentials or copy them into logs, prompts, commits, or notes.
- Do not start a Jules session when the user only asks to list repositories.

## Complete example workflow

```text
1. Use Jules MCP to list my connected repositories. Read-only.
2. Start a session for github/jbolt25/home-pulse-103 on main to review the sensor API error handling. Require plan approval and do not create a PR.
3. Show the plan and latest activity for the new session. Do not approve yet.
4. Approve the plan for session sessions/123.
5. Send this feedback to session sessions/123: keep the change limited to error handling and add tests.
6. Retrieve the completed result for session sessions/123.
```

If `jules` does not appear under `/mcp`, restart Codex again and open a new local task. The local configuration is in `C:\Users\Will\.codex\config.toml`.
