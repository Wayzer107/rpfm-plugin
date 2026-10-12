# Scripts, tests, MyMod, and game tools

## Text and Lua

Decode Text and preserve format/encoding when saving. Lua, XML, VMD, and WSModel
have game-specific path/validation rules. Inspect DB keys, events, and file paths.
GUI highlighting/completion differs from MCP data editing. Save changes and use
appropriate diagnostics.

`lua_run_tests` uses Lua 5.1 and game script libraries against all open packs.
It needs the intended game's AK scripting docs. Tests are experimental and do
not reproduce every engine behavior or battle scripting. The schema accepts
`test_source` and optional `campaign`, not a guessed test-file path. Load only
intended packs. Read the live description for the `rpfm` API: object creation,
test registration, events, time/turn progression, mocks, and call/value assertions.
Each test gets a fresh Lua state after boot/first tick. Keep packaged tests
outside game-loaded `script/`, for example `tests/`.

Inspect errors, listener/script failures, output, and undocumented methods.
Emulated methods can return neutral placeholders, producing misleading passes.
State the scenario tested; a pass does not establish an actual campaign/save.
Do not execute untrusted tests/scripts merely to inspect a pack.

## RPFM plugin scripts

These executable Python/Lua extensions in RPFM's config `scripts` folder are
distinct from this agent plugin. GUI Run Script exports selected DB/Loc files as
TSV and others as raw data, invokes the chosen script with paths, and reimports
original selections. Newly created/deleted export files are not automatically
applied as pack additions/deletions. `scripts/last_run.log` is overwritten on
subsequent runs.

No dedicated Run Script named tool was found in the 155-tool snapshot. Inspect
trusted source and use GUI instructions or explicit extract-transform-import
operations with correct TSV handling. Do not invent a tool or classify script
execution as a read. Verify intended inputs/outputs and imported data before save.

## MyMod

MyMod combines an editable source tree and a pack for iteration. Establish the
base path/game before `initialize_my_mod_folder`; inspect returned paths. Manual
overview/management examples differ in pack placement. Preserve existing folders
and Git state; optional VS Code/Sublime metadata must match the user's choice.

Extract source for external editing and import supported changed files/TSV with
the appropriate operations. Treat import as additive unless the operation
explicitly implements deletion synchronization. Missing source files are not
permission to remove packed content.

The catalog has initialization/file tools but no dedicated tools for every GUI
MyMod action. Use GUI for unsupported lifecycle actions or `call_command` only
after verifying the build's enum/shape in source. Install/uninstall and
`live_export` can write real game data: execute only for a requested deployment
or test, with rollback copies. Do not delete sources to remove a deployed pack.

## Starpos, maps, animation IDs

These operations are game/build-specific and can need external AK/game tools.
Read matching command definitions and live schemas first.
`build_starpos_get_campaign_ids` and `build_starpos_check_victory_conditions`
establish inputs. Preprocessing, external generation, postprocessing, and
cleanup are separate stages. Preserve outputs/logs before cleanup; preprocessing
alone is not a finished playable startpos.

For `pack_map`, `patch_siege_ai`, and `live_export`, establish game, source paths,
destinations, and game-write authorization. Do not test on real installs just
to discover availability. `update_anim_ids` changes IDs; inspect collisions,
skeleton mappings/references with `get_anim_paths_by_skeleton_name` and matching
schema data. Back up/read back changed structures; visuals and AI need game tests.

Sources: [text](https://frodo45127.github.io/rpfm/manual/editors/text.html),
[Lua](https://frodo45127.github.io/rpfm/manual/packs/lua-tests.html),
[plugin scripts](https://frodo45127.github.io/rpfm/manual/packs/plugin-scripts.html),
[MyMod](https://frodo45127.github.io/rpfm/manual/mymod/overview.html),
[management](https://frodo45127.github.io/rpfm/manual/mymod/managing.html),
[import/export](https://frodo45127.github.io/rpfm/manual/mymod/import-export.html),
[commands](https://frodo45127.github.io/rpfm/manual/server/ws-commands.html).
