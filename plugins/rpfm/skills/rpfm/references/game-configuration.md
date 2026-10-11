# Game configuration, schemas, and dependencies

## Readiness

Check current session state first. The MCP SDK identity (such as `rmcp 3.1.0`)
is not the RPFM application version. Recent builds expose read-only `/version`;
older builds may not. Record executable/version evidence for compatibility.

Observed game keys: `pharaoh_dynasties`, `pharaoh`, `warhammer_3`, `troy`,
`three_kingdoms`, `warhammer_2`, `warhammer`, `thrones_of_britannia`, `attila`,
`rome_2`, `shogun_2`, `napoleon`, `empire`, `arena`. Prefer the live games
resource/tool description as the list evolves. Arena is browse-only in the
manual; do not promise writable support.

Game paths point to folders containing the executable. Steam discovery fills
empty settings only and does not cover every distribution. Inspect the relevant
typed setting and disk evidence. Derive exact setting keys from the current
build/Preferences rather than game display names. Preserve unrelated paths.
Session game selection differs from persistent default-game preference; do not
rewrite defaults just to inspect one mod.

## Schemas

After selection verify `is_schema_loaded`, required table/version definitions,
and `schemas_path` when needed. Missing schemas, unknown table versions, and
broken row data require different remedies. Documentation differs about schemas
shipping in releases; inspect the actual installation. Authorized setup can use
`check_schema_updates`/`update_schemas`, reload the intended game, and verify
definitions. Do not update the whole program to solve a schema problem.

Use definition queries plus `fields_processed`. The DB Decoder is a GUI binary
layout investigation workflow; MCP definition/schema operations do not reproduce
its visual controls. Use `get_missing_definitions` for evidence before editing.
AK-derived schema updates, `save_schema`, and local patch save/import affect
later interpretation. Preserve patches, exact game/version provenance, and
rollback copies. Removing definitions/patches can break unrelated mods. Validate
the target after a patch; schema save success does not validate all tables.

## Vanilla, parents, and Assembly Kit

Use the live `set_game_selected` rebuild option to initialize schema and vanilla
data. Verify `is_there_a_dependency_database` using its actual argument meaning.
`generate_dependencies_cache` builds a disk cache from configured game/optional
AK data; `rebuild_dependencies` loads/rebuilds session state. These differ from
declaring parent mods inside a pack. Cache generation can take minutes and
consume substantial resources; regenerate after relevant game/schema changes.

AK fills reference tables missing from vanilla packs. Configure installed AK
paths and regenerate cache when needed. Not every game has an AK; Empire and
Napoleon use optional archived-data downloads. Missing AK can explain unresolved
references. Do not require a large AK install for raw pack inspection.

Inspect `get_dependency_pack_files_list`; change declarations only for intended
dependencies. Preserve exact boolean/string tuple meaning from the running build.
The manual mixes lookup and engine load-order language; a declaration is not
proof of launcher order. Resolve actual parent locations/deployment. Use
`get_tables_from_dependencies`, `dependencies_column_values`,
`get_rfiles_from_all_sources`, and `import_dependencies_to_open_pack_file` for
needed records. Keep vanilla, parent, AK, and open-pack provenance distinct.

## Shared settings

Settings are server-wide even when packs/dependencies are session-specific.
Read only necessary typed keys. `settings_get_all` can expose API keys; do not
log/package it as a diagnostic dump. `config_path` identifies the real location;
current settings use `settings.json` and a loadable backup. Back up the actual
file before authorized disk edits and validate the complete result.
`backup_settings` is in-memory, not a durable disk backup.

Do not clear settings, paths, schemas, or cache folders as generic remedies.
Preserve table behavior, debug flags, diagnostic triggers, AI credentials, and
GitHub choices. Telemetry and crash-upload toggles are currently opt-out and
take effect immediately; change only when requested. Local crash/log files can
still exist with uploads disabled. Keep credentials out of packs and Git.

Sources: [first-time setup](https://frodo45127.github.io/rpfm/manual/intro/first-time-config.html),
[dependencies](https://frodo45127.github.io/rpfm/manual/packs/dependencies.html),
[schemas](https://frodo45127.github.io/rpfm/manual/reference/schemas.html),
[settings](https://frodo45127.github.io/rpfm/manual/reference/settings.html),
[games](https://frodo45127.github.io/rpfm/manual/reference/supported-games.html),
[telemetry](https://frodo45127.github.io/rpfm/manual/reference/telemetry.html).
