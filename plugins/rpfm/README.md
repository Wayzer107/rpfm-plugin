# RPFM plugin 0.4.0

Community integration for local Total War packfile work through RPFM Server.
The original RPFM icon is preserved. No server binary, game data, or API key is
bundled; setup installs/reuses the official upstream runtime and registers MCP.

## Install and update

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
codex plugin add rpfm@rpfm-marketplace --json
```

For an already registered marketplace:

```powershell
codex plugin marketplace upgrade rpfm-marketplace --json
codex plugin add rpfm@rpfm-marketplace --json
```

With Claude Code:

```powershell
claude plugin marketplace add Wayzer107/rpfm-plugin
claude plugin install rpfm@rpfm-marketplace
```

Update with `claude plugin marketplace update rpfm-marketplace`. Claude Code
reads `.claude-plugin/plugin.json`, which registers the same local endpoint as
`plugin:rpfm:rpfm-tools`; check it with `/mcp` once RPFM Server is running.

Start a fresh chat or restart the host when necessary to load changed skills.
Use one intended RPFM plugin/connection per task; do not mix session keys from
duplicate account/marketplace/direct registrations. An older account-backed
release does not automatically receive this Git marketplace update.

## Setup without a running server

Ask: "Use RPFM setup to install or locate the server, start it, and verify
the connection and game readiness."

The [setup skill](skills/setup/SKILL.md) works through the shell when MCP is
unavailable. Its [complete server guide](skills/setup/references/server-installation.md)
provides checksum-verified Windows/Linux v5.1.1 download procedures, startup,
registration alternatives, and readiness checks. Runtime installation is outside
the plugin cache. Installation registers HTTP; it does not create an auto-launch
service. Python 3.10+ is optional for the read-only checker, not normal use.

## Workflow coverage

The [main skill](skills/rpfm/SKILL.md) routes to guides for configuration/schema/
AK/cache, packfiles/tables/TSV, search/references/diagnostics, scripts/Lua/MyMod,
localization, release optimization/key deletes, assets, and protocol recovery.
The [manual map](skills/rpfm/references/documentation-map.md) routes all 50
manual pages and states review/testing limits. The [tool catalog](skills/rpfm/references/tool-catalog.md)
contains every discovered operation and links full input schemas. The discovery
snapshot includes resource/prompt lists and selected server examples.

GUI operations, library capabilities, and MCP operations are distinguished.
This plugin does not supply missing GUI tools or guarantee in-game results.
Each connection owns its packs/dependencies; shared settings are global.
Idle sessions can expire after five minutes. Save requested edits promptly.

## Verification and removal

From this plugin directory, optionally run:

```powershell
python ./scripts/check_connection.py
```

It initializes MCP, discovers tools, and calls only get_game_selected and
list_open_packs. Check actual host calls and game/schema readiness separately.
No pack edits are part of the checker.

```powershell
codex plugin remove rpfm@rpfm-marketplace
codex plugin marketplace remove rpfm-marketplace
```

With Claude Code:

```powershell
claude plugin uninstall rpfm@rpfm-marketplace
claude plugin marketplace remove rpfm-marketplace
```

Removal does not delete the server, packs, game installs, or settings.

## Share and provenance

Public repository: https://github.com/Wayzer107/rpfm-plugin. Share that Git URL
or the complete marketplace archive, including hidden manifest/catalog files.
This is a Git marketplace, not an OpenAI public-directory submission.

MIT integration license; upstream icon attribution is in UPSTREAM-LICENSE.
RPFM is maintained by Frodo45127 (Ismael Gutierrez Gonzalez). The icon comes
from icons/rpfm.png at upstream 5204dab9e9a9376c438deabed8489de3bc319599.
Release metadata and documentation were checked on 2026-10-12. Endpoint and
discovery were verified on an existing Windows installation; fresh installation,
Linux execution, advanced editing, and game behavior were not tested for this
documentation release. See the repository RELEASE-NOTES.md for release checks.
