---
name: serena-setup
description: Install or repair the official local Serena CLI and make its MCP tools available through this plugin. Use when Serena is missing, disconnected, or newly installed.
---

# Set up Serena

This plugin's MCP configuration launches the installed `serena` command as a
local stdio server. Set up the upstream runtime first when the command is not
available. When the user asks for Serena setup, complete the required local
checks, install, and verification without stopping at instructions alone.

## Check the current installation

1. If Serena tools are callable, use a harmless read-only tool to confirm the
   connection and current project state. Do not reinstall a working server.
2. Otherwise check `uv --version`, `uv tool list`, and `serena --help` in the
   user's shell. On Windows use `Get-Command uv` and `Get-Command serena`; on
   macOS/Linux use `command -v uv` and `command -v serena`.
3. Read [the installation reference](references/installation.md) for the
   current official setup procedure and host PATH recovery.

## Install and connect

If `uv` is missing, install it from Astral's official instructions in the
reference. Open a new terminal if needed so PATH changes take effect. Then:

```sh
uv tool install -p 3.13 serena-agent
serena init
```

Reuse an existing Serena installation and configuration. Do not erase
`~/.serena`, project memories, or project configuration to resolve a connection
problem. The package already contains the MCP registration for Codex (`--context=codex`)
and Claude Code (`--context=claude-code`); do not also run `serena setup codex`,
`serena setup claude-code`, or add another global Serena server.

After setup, check the host's MCP list (`/mcp` in Codex or Claude Code) and make
a harmless Serena tool call. If the shell can run Serena but the host cannot,
restart the host process or follow the reference's executable-path
instructions. A successful shell command alone does not prove the host loaded
the tools.

## Report

Separate the installed runtime, Serena initialization, server connection, and
callable tool checks. If the connection works but the current project is not
active, ask Serena to activate the intended workspace and then verify it before
code work. Language-specific servers may need additional tools; consult
[Serena language support](https://oraios.github.io/serena/01-about/020_programming-languages.html)
for the requested language.
