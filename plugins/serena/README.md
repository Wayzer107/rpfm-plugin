# Serena plugin 0.1.0 for Codex and Claude Code

Connect Codex or Claude Code to the local Serena MCP server for symbol-aware code navigation,
reference lookup, and refactoring. This is a community plugin package; Serena
itself is maintained upstream and is installed separately on each computer.

## Install

Register this repository once if it is not already registered:

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
```

Install or update the plugin:

```powershell
codex plugin add serena@rpfm-marketplace --json
```

Start a fresh Codex chat after installation. Restart the desktop app if its
plugin inventory has not refreshed.

With Claude Code, register the same repository and install from it:

```powershell
claude plugin marketplace add Wayzer107/rpfm-plugin
claude plugin install serena@rpfm-marketplace
```

Inside a Claude Code session the equivalent is `/plugin marketplace add
Wayzer107/rpfm-plugin`, then `/plugin install serena@rpfm-marketplace`.
Restart Claude Code after installation so the MCP server and skills load.

## Set up Serena

Ask Codex or Claude Code:

> Use Serena setup to install Serena, initialize it, and verify its MCP tools.

The plugin setup skill follows Serena's current upstream `uv` installation
instructions. Serena's current documentation warns against old marketplace
installation recipes; this package uses the current upstream runtime commands
and supplies MCP entries for Codex (`--context=codex`) and Claude Code
(`--context=claude-code`). It does not bundle Serena source, binaries, or
language servers.

See the [setup skill](skills/serena-setup/SKILL.md) and its [installation reference](skills/serena-setup/references/installation.md)
for the full procedure.

## Use Serena

Ask the agent to activate the current project, map important symbols, trace a
definition or references, or make a focused symbol-aware refactor. The
[Serena workflow skill](skills/serena/SKILL.md) guides project activation,
symbolic discovery, careful edits, and verification.

The host app may start outside the project directory. If Serena has no active
project, activate the workspace explicitly through Serena before project work.
The local server has access to files on the computer running the MCP client;
this package does not provide a hosted runtime.

## Remove

```powershell
codex plugin remove serena@rpfm-marketplace
```

With Claude Code:

```powershell
claude plugin uninstall serena@rpfm-marketplace
```

Removing the plugin removes its MCP registration, not Serena or any
Serena configuration and project memories. See [upstream Serena docs](https://oraios.github.io/serena/)
for runtime management and licensing. Serena is component-licensed: its
application is GPL-3.0-or-later and SolidLSP is MIT. This package contains no
Serena source or binaries; its own integration files use the repository's MIT
license.
