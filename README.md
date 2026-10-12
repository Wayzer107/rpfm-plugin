# Codex and Claude Code developer tools marketplace

This Git marketplace works with both Codex and Claude Code. It contains local development tools for Total War
packfiles, semantic code work, and Rust analysis. The RPFM package provides the
existing Total War workflows; Serena and Rust Analyzer MCP are separate plugins
with their own setup and usage skills.

The RPFM integration is a community project, not an official RPFM release.
RPFM plugin version: **0.4.0**. Serena and Rust Analyzer MCP plugin versions:
**0.1.0**. Marketplace: **rpfm-marketplace**.

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

Install either additional plugin from the registered marketplace:

```powershell
codex plugin add serena@rpfm-marketplace --json
codex plugin add rust-analyzer-mcp@rpfm-marketplace --json
```

Run `codex plugin marketplace upgrade rpfm-marketplace --json` first when the
marketplace is already registered and new package entries are not visible.
Each plugin starts its own local MCP process and requires its runtime to be
installed on the same computer as Codex.

## Register and install with Claude Code

The same repository is also a Claude Code marketplace
(`.claude-plugin/marketplace.json`):

```powershell
claude plugin marketplace add Wayzer107/rpfm-plugin
claude plugin install rpfm@rpfm-marketplace
claude plugin install serena@rpfm-marketplace
claude plugin install rust-analyzer-mcp@rpfm-marketplace
```

Inside a Claude Code session, use `/plugin marketplace add Wayzer107/rpfm-plugin`
and then `/plugin` to browse and install. Restart Claude Code after installing so
the MCP servers and skills load, then check them with `/mcp`. Skills are
namespaced by plugin, for example `/rpfm:setup` or `/serena:serena-setup`.

Update with `claude plugin marketplace update rpfm-marketplace`; remove with
`claude plugin uninstall <plugin>@rpfm-marketplace` and
`claude plugin marketplace remove rpfm-marketplace`.

Each plugin has a Claude Code manifest in `.claude-plugin/plugin.json`. It uses
the same skills and runtimes as the Codex package, with two host differences:
RPFM registers its endpoint with Claude Code's `"type": "http"` transport name,
and Serena starts with `--context=claude-code` instead of `--context=codex`, so
it omits tools that duplicate Claude Code's built-in file and shell tools.

## Set up Serena

Ask Codex:

> Use Serena setup to install Serena, initialize it, and verify its MCP tools.

The plugin follows Serena's current upstream `uv` quick start and Codex server
command. Serena is installed separately for each recipient; no Serena runtime
is bundled. Read the [Serena package guide](plugins/serena/README.md) for
prerequisites and the [complete setup reference](plugins/serena/skills/serena-setup/references/installation.md).

## Set up Rust Analyzer MCP

Ask Codex:

> Use Rust Analyzer MCP setup to install rust-analyzer and the MCP server, then verify the connection.

The setup guide uses the official Rust toolchain installer, adds the
`rust-analyzer` and `rust-src` components, and installs the selected `rust-analyzer-mcp` crate.
Read the [Rust Analyzer MCP package guide](plugins/rust-analyzer-mcp/README.md)
and its [complete setup reference](plugins/rust-analyzer-mcp/skills/rust-analyzer-mcp-setup/references/installation.md).

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
.agents/plugins/marketplace.json      (Codex catalog)
.claude-plugin/marketplace.json       (Claude Code catalog)
plugins/rpfm/
  plugin.json
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  mcp.json
  .mcp.json
  assets/rpfm.png
  skills/rpfm/SKILL.md
  skills/setup/SKILL.md
  skills/setup/references/server-installation.md
  scripts/check_connection.py
plugins/serena/
  plugin.json
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  mcp.json
  .mcp.json
  skills/serena/SKILL.md
  skills/serena-setup/SKILL.md
  skills/serena-setup/references/installation.md
plugins/rust-analyzer-mcp/
  plugin.json
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  mcp.json
  .mcp.json
  skills/rust-analyzer-mcp/SKILL.md
  skills/rust-analyzer-mcp-setup/SKILL.md
  skills/rust-analyzer-mcp-setup/references/installation.md
```

Relative plugin source paths in the catalog resolve inside the cloned repository.
The catalog follows the Codex .agents/plugins marketplace convention also
used by obra/superpowers. This repository is a Git marketplace, not an
OpenAI public-directory submission.

## Development checks

Run the offline packaging tests with Python 3.10+:

```sh
python3 -m unittest discover -s tests -v
```

Validate the Claude Code marketplace and plugin manifests with the Claude Code CLI:

```sh
claude plugin validate .
claude plugin validate plugins/rpfm
```

Validate portable manifests and MCP configuration against the official schemas:

```sh
uv run scripts/validate_schemas.py
```

After installing Serena, rust-analyzer, and Rust Analyzer MCP, run the live
integration checks. They use disposable Rust projects and Serena configuration:

```sh
PLUGIN_MCP_INTEGRATION=1 python3 -m unittest discover -s tests -v
```

The reusable `scripts/check_stdio.py` checker reads a package's MCP launch
configuration, initializes the server, discovers tools, and optionally makes
explicit tool calls. For example:

```sh
python3 scripts/check_stdio.py plugins/serena --cwd /path/to/project --call '{"name":"get_current_config","arguments":{}}'
```

See [verification results](VERIFICATION.md) for the tested versions and limits.

## License and provenance

MIT; see LICENSE and plugins/rpfm/UPSTREAM-LICENSE.
The original RPFM icon is preserved with upstream attribution.
[Plugin details](plugins/rpfm/README.md) contain the workflow and provenance notes.

The installation guide's fresh-machine download/extraction and Linux setup
have not been executed during preparation. Server probing was verified on an
existing Windows installation. See RELEASE-NOTES.md for distribution checks.
