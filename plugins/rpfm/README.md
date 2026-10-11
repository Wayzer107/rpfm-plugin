# RPFM plugin

Version 0.3.0. RPFM packfile workflows with server installation and registration
guidance, distributed as a portable plugin and a Codex marketplace.

## What recipients get

- RPFM workflows for packfiles, DB tables, localization, references, extraction,
  diagnostics, and focused edits.
- A setup skill that guides installation of upstream RPFM Server, verifies
  its download checksum, starts it, and explains MCP registration.
- A Streamable HTTP connection to http://127.0.0.1:45127/mcp.
- The original upstream RPFM icon and its MIT license attribution.
- An optional read-only connection checker using Python 3.10+.

RPFM Server binaries are downloaded separately from the official upstream
release. The plugin does not automatically download or run executables.
Installing this plugin registers the connection; recipients then follow
the setup skill to provide a running server.

## Install from the marketplace ZIP

Register the public Git marketplace and install its plugin:

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
codex plugin add rpfm@rpfm-marketplace --json
```

The Git marketplace is named rpfm-marketplace. Codex clones the source from GitHub. If rpfm-marketplace is already registered
to another folder, inspect codex plugin marketplace list and update that
registration deliberately rather than overwriting unknown configuration.

Use one installation source at a time. If the same RPFM plugin is already
installed from Created by you, keep that installation or uninstall it before
installing the marketplace copy. Both sources provide the same workflows.

## Install and register the server

Open [the complete server setup guide](skills/setup/references/server-installation.md).
It includes a full Windows x64 procedure for RPFM v5.1.1 (about 280 MiB),
published SHA-256 verification, safe extraction into a new versioned directory,
server startup, and plugin versus direct MCP registration.

After installing the plugin, start a fresh chat and ask:

> Set up RPFM and verify its server connection.

The setup skill first checks for existing RPFM and reuses it when compatible.
No API key, Node, or Python is required for ordinary RPFM plugin use. Python is
only needed for the optional checker. The server needs to remain available
while tools are used; the plugin does not install a background service.

## Share through a marketplace

The complete marketplace ZIP contains:

```text
rpfm-marketplace-0.3.0/
  .agents/plugins/marketplace.json
  README.md
  plugins/rpfm/
    plugin.json
    .codex-plugin/plugin.json
    mcp.json
    .mcp.json
    assets/rpfm.png
    skills/rpfm/SKILL.md
    skills/rpfm/references/workflows.md
    skills/setup/SKILL.md
    skills/setup/references/server-installation.md
    scripts/check_connection.py
    LICENSE
    UPSTREAM-LICENSE
```

Share the ZIP directly, or commit the contents of the marketplace directory
to the root of a Git repository, including .agents and .codex-plugin.
Recipients can then register that repository with:

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
codex plugin add rpfm@rpfm-marketplace --json
```

The public repository is https://github.com/Wayzer107/rpfm-plugin on main. The root marketplace README includes maintainer instructions.

This is a Codex marketplace distribution, not a submission to the public
OpenAI plugin directory. Public directory review is a separate workflow.

## Connection and session behavior

Each MCP connection has its own open packs and dependency cache, separate
from the GUI and other MCP connections. Do not mix pack keys between them.
The server may reap a session after five minutes without commands; save
authorized work promptly and reopen packs after reconnecting.

A client on another machine cannot reach this machine's loopback address.
Each marketplace recipient runs RPFM Server locally. Account storage alone
does not make local packfiles accessible to a hosted client.

## Verify

From the plugin directory:

```powershell
python ./scripts/check_connection.py
```

This probes the endpoint, discovers tools, and calls only get_game_selected
and list_open_packs. Verify actual host tool calls separately. For an editing
task, verify saved pack data independently and distinguish it from in-game tests.

## Update and remove

Change source files, bump both manifest versions, and release the complete
marketplace source. Preserve the marketplace name and plugin identity across
updates. Keep mcp.json and .mcp.json endpoints synchronized. Reinstall or reload
using the host's supported plugin workflow; do not edit cached files.

To remove the marketplace installation:

```powershell
codex plugin remove rpfm@rpfm-marketplace
codex plugin marketplace remove rpfm-marketplace
```

This does not uninstall RPFM Server, delete packfiles, or reset RPFM settings.
Remove account-backed installations through the app's plugin management.

## Provenance and validation

This is a community integration. RPFM is maintained by Frodo45127
(Ismael Gutiérrez González). The original icon comes from icons/rpfm.png at
upstream revision 5204dab9e9a9376c438deabed8489de3bc319599.
UPSTREAM-LICENSE covers that asset; LICENSE covers the integration content.

The server endpoint and read-only checker were verified on the author's
existing Windows installation. The new-machine download/extraction procedure
and Linux installation were not executed during preparation. Published
release URL, byte count, and digest were checked against GitHub metadata
on 2026-10-12.

- https://github.com/Frodo45127/rpfm/releases/tag/v5.1.1
- https://frodo45127.github.io/rpfm/manual/server/mcp.html
- https://frodo45127.github.io/rpfm/manual/server/overview.html
