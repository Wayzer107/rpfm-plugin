# RPFM plugin marketplace

A Codex plugin for Total War packfile inspection and editing through
[RPFM Server](https://frodo45127.github.io/rpfm/manual/server/overview.html).
Includes the original RPFM icon, extensive operational guides, and server setup instructions
that work when RPFM is not installed or its server is not running.

This is a community integration, not an official RPFM release.
Plugin version: **0.4.0**. Marketplace: **rpfm-marketplace**.

## Register and install

With a current Codex CLI:

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
codex plugin add rpfm@rpfm-marketplace --json
```

The full Git URL is also supported:

```powershell
codex plugin marketplace add https://github.com/Wayzer107/rpfm-plugin.git --ref main
codex plugin add rpfm@rpfm-marketplace --json
```

These are two equivalent registration methods; choose one.
Start a new Codex chat after installation. Restart the desktop app if it has
not refreshed the plugin inventory.

## Get the server running

Ask Codex:

> Use RPFM setup to get the server running and verify the connection, even if its MCP tools are currently unavailable.

The setup skill tells the agent to:

1. Check the local endpoint and reuse a working RPFM server.
2. Locate an existing compatible installation when the server is stopped.
3. Start the verified server executable from its installation directory.
4. If RPFM is missing, install the official upstream release into a separate
   versioned directory using the complete checksum-verified Windows procedure.
5. Verify MCP connectivity and actual host tool availability separately.

[Complete server installation and startup guide](plugins/rpfm/skills/setup/references/server-installation.md)
includes copy-and-use commands. It can be read without a working MCP connection.

The plugin registers Streamable HTTP at http://127.0.0.1:45127/mcp.
RPFM Server runs locally and must be available while tools are used. The plugin
does not create a service or auto-run binaries at installation time. Each
recipient gets their own local server and files; this repository hosts the
plugin package, not a shared RPFM backend.

The pinned Windows x64 download is RPFM v5.1.1, about 280 MiB. Python 3.10+
is optional for the included connection checker. It is not required for normal
plugin use.

## Documentation coverage

Version 0.4.0 adds game/schema/dependency readiness, DB/TSV persistence, search
and diagnostics, Lua tests, MyMod and scripts, localization/translation,
optimization/key deletes, specialized assets, and protocol recovery. The main
skill routes tasks to focused guides rather than loading every reference at once.

[Complete documentation audit and chapter map](plugins/rpfm/skills/rpfm/references/documentation-map.md)
routes all 50 manual pages and states review/testing limits. It includes a
[coverage CSV](plugins/rpfm/skills/rpfm/references/documentation-coverage.csv),
[155-tool catalog](plugins/rpfm/skills/rpfm/references/tool-catalog.md), complete
input schemas, and resource/prompt discovery. GUI-only and external-tool
workflows are explicitly identified. The generated Rust API was checked at
entry points and selected relevant structures, not exhaustively symbol by symbol.

## Use RPFM

Example requests:

- Inspect my Attila pack at an absolute path and explain its tables.
- Find a localization key and its references in my mod.
- Make a focused table edit and save a separate mod pack.
- Diagnose missing references in this pack.

Each MCP connection has a separate pack session, including separation from
the GUI. Open packs in the same connection used for the task. Save authorized
changes promptly; upstream may expire idle sessions after five minutes.

## Installation errors

For a generic "couldn't add plugin, try again" message, use the CLI commands
above to get a concrete error. Check installed CLI support with
`codex plugin --help`. The Git marketplace path is separate from an
account-backed plugin's install button.

If the plugin is installed but RPFM tools cannot connect, run the setup workflow.
A stopped server is resolved by server startup, not by repeatedly installing
the plugin. The plugin's instructions remain ordinary local files.

Do not install the account-backed copy, old local copy, and this Git copy
simultaneously. Use `codex plugin list --json` to identify existing marketplace
copies. Remove only the copy being replaced, using its exact selector.

## Verify the connection

From the plugins/rpfm directory, if Python is available:

```powershell
python ./scripts/check_connection.py
```

The checker discovers tools and calls only get_game_selected and list_open_packs.
It does not edit packs or settings. Check actual host calls separately.

## Update or remove

Update this registered Git marketplace and install the current package:

```powershell
codex plugin marketplace upgrade rpfm-marketplace --json
codex plugin add rpfm@rpfm-marketplace --json
```

To uninstall this marketplace copy:

```powershell
codex plugin remove rpfm@rpfm-marketplace
codex plugin marketplace remove rpfm-marketplace
```

This does not delete RPFM Server, packfiles, game installs, or RPFM settings.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/rpfm/
  plugin.json
  .codex-plugin/plugin.json
  mcp.json
  .mcp.json
  assets/rpfm.png
  skills/rpfm/SKILL.md
  skills/setup/SKILL.md
  skills/setup/references/server-installation.md
  scripts/check_connection.py
```

Relative plugin source paths in the catalog resolve inside the cloned repository.
The catalog follows the Codex .agents/plugins marketplace convention also
used by obra/superpowers. This repository is a Git marketplace, not an
OpenAI public-directory submission.

## License and provenance

MIT; see LICENSE and plugins/rpfm/UPSTREAM-LICENSE.
The original RPFM icon is preserved with upstream attribution.
[Plugin details](plugins/rpfm/README.md) contain the workflow and provenance notes.

The installation guide's fresh-machine download/extraction and Linux setup
have not been executed during preparation. Server probing was verified on an
existing Windows installation. See RELEASE-NOTES.md for distribution checks.
