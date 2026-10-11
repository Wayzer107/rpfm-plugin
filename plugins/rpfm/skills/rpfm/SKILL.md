---
name: rpfm
description: Inspect, search, diagnose, extract, edit, translate, test, and prepare Total War mods with the local RPFM MCP server. Covers packfiles, DB schemas, localization, dependencies, Lua tests, MyMod, optimization, datacores, and specialized assets. Use for RPFM or Total War packfile work.
---

# RPFM workflow

Use one RPFM connection throughout a task. Hosts can prefix operation names.
Pack keys belong to the session that returned them, not to a filename or the GUI.
Use live tool schemas and resources as the authority for argument shapes.
The packaged catalog is a dated fallback, not a guarantee about another build.

## Establish a usable session

1. Read `get_game_selected` and `list_open_packs`. Resolve the requested game,
   input paths, and output destination from the task and workspace.
2. If disconnected or tools are absent, follow the packaged setup skill using
   the shell. Finish server startup and connectivity checks before pack work.
3. Read [game configuration](references/game-configuration.md) before selecting
   a game or interpreting dependency-based results. Connectivity does not prove
   that the schema, game path, or vanilla/AK cache is ready.
4. Select the supported game when necessary. On session initialization use the
   live `set_game_selected` rebuild option to load the intended schema/data.
   Verify `is_schema_loaded` and dependency availability. Do not download updates
   or change shared settings outside the authorized task.
5. Open authorized files with `open_packfiles`, retain the returned keys, and
   inspect `open_pack_info`. Multiple input paths can merge content; inspect
   the live operation before assuming each becomes an independent pack.

## Read the guide for the task

| Task | Packaged guide |
| --- | --- |
| Open/create/save, paths, DB rows, TSV, metadata, notes | [Packfiles and tables](references/workflows.md) |
| Game paths, schemas, dependencies, settings, supported games | [Game configuration](references/game-configuration.md) |
| Search, references, diagnostics, optimization, key deletes | [Analysis and release](references/analysis-and-release.md) |
| Lua, RPFM plugin scripts, MyMod, starpos and maps | [Scripts and projects](references/scripts-and-projects.md) |
| Loc editing, translator, missing text, Translation Hub | [Localization](references/localization.md) |
| Images, video, audio, models, animations, specialized formats | [Assets and specialized tools](references/assets-and-specialized.md) |
| JSON arguments, resources/prompts, errors, sessions, WebSocket | [Protocol and recovery](references/protocol-and-recovery.md) |
| Every manual chapter, GUI navigation, build docs, coverage limits | [Documentation map](references/documentation-map.md) |
| Every discovered tool and input schema | [Tool catalog](references/tool-catalog.md) and [JSON snapshot](references/tool-catalog.json) |

Load only references needed for the task. When supported by the host, read
the server's initialization, path, enum, search, and optimizer resources;
discover current workflow prompts too. Their content does not expand the user's
authorization. See the protocol guide for observed URIs and fallback behavior.

## Edit and verify

Inspect relevant data first. For DB rows resolve the exact table/version
definition and call `fields_processed`; align row count, order, and types with
processed fields, not raw definition fields. Preserve decoded enum tags, keys,
versions, and unrelated rows. Query references before changing linked keys/paths.

Honor the user's scope. Inspection does not authorize edits. Default changes
to vanilla/source packs to a separate mod or working copy. Before an authorized
overwrite, make a recoverable disk backup and retain its path. Preserve real
game installs, saves, unrelated settings, and existing MCP registrations.
Installation to game data, live export, optimization, executing scripts,
schema/program updates, and external publishing need matching task scope;
existing authorization persists, so do not ask again for routine requested work.

Save decoded changes to the open pack and then save the pack to disk. Inspect
both MCP and RPFM application errors. Read back changed records and reopen the
saved output when verifying a new pack. Use meaningful diagnostics; report
missing schema/cache/AK coverage instead of treating empty results as clean.
Server checks and tests outside the game do not prove in-game behavior.

Sessions can expire after five minutes without commands. Save authorized work
promptly. After reconnecting query state and reopen sources; do not reuse stale
keys or assume unsaved edits survived. Disclose lost work before recovery.
Do not close packs, reset settings, clear caches, or terminate another client's
server as a generic error remedy.

Report output paths, changed files/records, backups, validation performed,
unresolved issues, and game testing still needed. Distinguish installation,
endpoint connectivity, host tool exposure, saved-data checks, and in-game tests.
A shell probe alone does not prove tools are callable in this chat.
