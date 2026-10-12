# Serena Codex plugin 0.1.0

Connect Codex to the local Serena MCP server for symbol-aware code navigation,
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

## Set up Serena

Ask Codex:

> Use Serena setup to install Serena, initialize it, and verify its MCP tools.

The plugin setup skill follows Serena's current upstream `uv` installation
instructions. Serena's current documentation warns against old marketplace
installation recipes; this package uses the current upstream runtime commands
and supplies a Codex MCP entry. It does not bundle Serena source, binaries, or
language servers.

See the [setup skill](skills/serena-setup/SKILL.md) and its [installation reference](skills/serena-setup/references/installation.md)
for the full procedure.

## Use Serena

Ask Codex to activate the current project, map important symbols, trace a
definition or references, or make a focused symbol-aware refactor. The
[Serena workflow skill](skills/serena/SKILL.md) guides project activation,
symbolic discovery, careful edits, and verification.

The Codex App may start outside the project directory. If Serena has no active
project, activate the workspace explicitly through Serena before project work.
The local server has access to files on the computer running the MCP client;
this package does not provide a hosted runtime.

## Remove

```powershell
codex plugin remove serena@rpfm-marketplace
```

Removing the plugin removes its Codex MCP registration, not Serena or any
Serena configuration and project memories. See [upstream Serena docs](https://oraios.github.io/serena/)
for runtime management and licensing. Serena is component-licensed: its
application is GPL-3.0-or-later and SolidLSP is MIT. This package contains no
Serena source or binaries; its own integration files use the repository's MIT
license.
