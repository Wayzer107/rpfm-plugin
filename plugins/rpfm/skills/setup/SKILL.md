---
name: setup
description: Install and register RPFM Server, set up the RPFM plugin on a new computer, or troubleshoot missing tools and connection errors. Use when the user asks for RPFM installation, server setup, MCP registration, or marketplace onboarding.
---

# Install and connect RPFM

Setup is usable even when RPFM tools fail to connect: use the local shell and
the packaged installation reference to start the server first. Missing tools
must not cause setup to stop with only a suggestion to retry installation.

When the user asks to get RPFM working, that authorizes the required local
setup actions. Complete discovery, startup, and verification. If installation
is needed, explain the download size and destination and proceed within that
request; do not ask again for routine setup steps already authorized.

This plugin connects to http://127.0.0.1:45127/mcp on the computer running
the local MCP client. It supplies the MCP registration and installation
instructions. The server executable is installed separately.

Read references/server-installation.md for the complete installation procedure,
verified upstream release URL and checksum, startup commands, and registration
alternatives. Read the plugin-root README.md for marketplace installation and
sharing. Resolve the actual platform and existing RPFM installation first.

## Check before installation

Try the plugin's get_game_selected and list_open_packs tools when available.
These checks do not change the selected game or open real packs. If tools
are unavailable, inspect the configured endpoint and existing listener/process.
An open port alone does not identify a working RPFM MCP server.

If no listener exists, inspect running RPFM processes and common existing
installation directories first. Use user-provided paths, LOCALAPPDATA/Programs/RPFM,
and executable discovery; do not assume a path from the author's computer.
Default new installations to LOCALAPPDATA/Programs/RPFM/v5.1.1, outside the
plugin cache so upgrades do not delete the runtime. The plugin registers the
Streamable HTTP endpoint but HTTP registration does not auto-launch a process.
Locate the actual rpfm_server.exe, launch it hidden from its own directory,
then poll MCP readiness with bounded retries. If the executable cannot be
found, follow the full checksum-verified installation procedure in the reference.
If startup fails, inspect stderr by running the executable in a terminal.
Do not claim startup succeeded merely because Start-Process returned a PID.

Reuse a compatible installation and working server. Do not replace an
installation, kill another client's server, reset settings, update schemas, or
open a game pack merely to test setup.

## Install when requested

When the user authorizes setup, follow the reference's complete procedure.
Show the platform, download size, and destination before downloading. The
Windows procedure pins v5.1.1, verifies the published SHA-256, and refuses to
overwrite an existing versioned directory. Check that rpfm_server exists after
extraction. Preserve the complete runtime layout. Do not guess a download URL,
checksum, executable path, or a server launch flag.

Start the GUI or verified standalone server as appropriate. Use hidden
background windows on Windows. Check for an existing listener first.
Do not add a Windows service or login startup unless requested.

## Register exactly one intended connection

Installing the plugin already registers its MCP endpoint through mcp.json.
Do not add a duplicate direct codex mcp registration during plugin setup.
The reference includes a direct registration alternative for users who want
only the server without this plugin. Inspect existing config before changes,
preserve unrelated entries, and validate the complete config after edits.

If tools are absent but direct MCP checks succeed, explain that the current
conversation may need refreshing. Start a fresh chat or restart Codex when
needed, then verify actual callable tools. A shell probe does not prove host
tool exposure. The optional scripts/check_connection.py uses Python 3.10+
and makes only read-only calls.

## Recover and report

Each MCP connection owns separate packs and dependencies. GUI packs may
need opening again in this connection. Sessions can expire after five minutes
of inactivity. Re-query session state after reconnecting and disclose any
lost unsaved edits; do not reuse stale pack keys.

Report separately: installation/download verification, running endpoint,
host tool availability, and harmless host call results. Do not claim a fresh
installation, Linux setup, or game behavior was tested unless actually run.
