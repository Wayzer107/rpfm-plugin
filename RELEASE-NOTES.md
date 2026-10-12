# 0.4.1

- Fix Claude Code tool discovery for RPFM Server 5.1.1. It answers the newer
  `server/discover` probe, so Claude Code required `ttlMs`/`cacheScope` in list
  results and rejected the tool list ("tools fetch failed").
- Add `plugins/rpfm/scripts/rpfm_stdio_bridge.py` and register it in the Claude
  Code manifest. It refuses `server/discover`, fills the missing fields, and
  starts an installed hidden `rpfm_server` when nothing is listening.
- Codex is unchanged: its manifest and `mcp.json`/`.mcp.json` keep direct
  Streamable HTTP registration.
- Document the Claude desktop Code tab path (user skills plus user-scope bridge).

Validation: 14 offline tests (including new bridge and Codex-isolation tests),
`claude plugin validate`, official schema validation, an isolated Codex
marketplace install showing direct HTTP, and a live Windows bridge session
against RPFM Server 5.1.1 (155 tools listed, read-only calls succeeded).

# 0.4.0

- Expand operational guidance after an audit of all 50 linked manual pages.
- Add game/schema/vanilla/AK readiness checks and shared-settings safeguards.
- Cover table/TSV persistence, search/references, all-pack diagnostics, Lua tests,
  plugin scripts, MyMod, localization/translation, release optimization,
  Warhammer 3 key deletes, and specialized asset/GUI boundaries.
- Include a full 155-tool input-schema snapshot, 11-resource/11-prompt discovery,
  selected resource examples, and chapter-by-chapter documentation coverage CSV.
- Add complete checksum-verified Linux x86_64 installation instructions and
  identify schema/client-example/API-version inconsistencies.
- Preserve plugin/marketplace identities, endpoint, and original icon.

Review: all manual pages fetched/indexed; narrative chapters reviewed; long
command/shared-type specifications inspected selectively. Generated Rust API
entry points and relevant structures checked, not every symbol.

Validation: local paths/links, named tool references, synchronized manifests/MCP
config, complete catalog, PowerShell instruction syntax, and existing Windows
server read-only checks. Public Git installation/update is verified during
release preparation. These checks do not test fresh runtime installation,
Linux execution, advanced mutation tools, or game behavior.

# 0.3.0

- Distribute through the public Wayzer107/rpfm-plugin Git marketplace.
- Register rpfm@rpfm-marketplace using the Codex marketplace catalog.
- Preserve the original RPFM icon and packfile workflows.
- Make setup usable when MCP tools are unavailable: locate or install RPFM,
  start its server, and verify the connection before working with packs.
- Include checksum-verified Windows server installation instructions.

Validation: package identities, relative paths, PowerShell instruction syntax,
and read-only server discovery. Git registration and installation are checked
from the published repository during release preparation. Fresh-machine server
installation and Linux setup remain untested.
