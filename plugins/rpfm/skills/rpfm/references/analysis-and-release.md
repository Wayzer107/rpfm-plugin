# Search, diagnostics, and release preparation

## Search and references

Construct GlobalSearch using its live example resource and JSON-encode where
required. SearchSource differs from DataSource: observed sources include
`{"Pack":"returned-key"}`, `"GameFiles"`, `"ParentFiles"`, `"AssKitFiles"`.
Limit sources/file types; use literal matching unless regex is intended. Inspect
paths, fields, row indices, and provenance before acting.

Replacement is a separate mutation. Preview matches and prefer
`global_search_replace_matches` for explicit subsets. Replace only authorized
writable open-pack content. A dependency result is not authorization to edit
vanilla. Broad replacement can touch unrelated text/keys; decode touched files
and verify intended changes after disk save.

Resolve definitions and use `referencing_columns_for_definition`,
`get_reference_data_from_definition`, `search_references`, and `go_to_definition`.
Use `go_to_loc`/`get_source_data_from_loc_key` for text origins. Include complete
keys and relevant sources; string search alone is not complete reference
analysis. File rename/move does not repair DB references automatically.

## Diagnostics

Establish game path, schema/version, vanilla cache, and AK coverage first.
The audited `diagnostics_check` checks **all open packs**, not an invented
`pack_key` argument. Record scope, ignores, and AK-only-reference choice.
`diagnostics_update` uses the returned diagnostic representation and changed
paths. Use checks where linked data/scripts need validation; a simple read-back
can be sufficient for a small isolated edit.

Group issues by environment/schema gaps, invalid keys/references, duplicates,
paths, versions, and Lua errors. Explain consequences/severity and distinguish
pre-existing issues. Empty results/ignored errors do not prove completeness.
`add_line_to_pack_ignored_diagnostics` changes the ignore list; suppression is
not repair. Lua syntax checks and AK-dependent API/key/event checks have
different coverage. See [scripts and projects](scripts-and-projects.md).

## Optimization and release copies

Optimize only within an authorized optimization/release task. Keep editable
source and separate release output. Compare paths, counts, keys, and important
values before/after. Verify game, current vanilla/parents, schema, and language.

Read `get_optimizer_options` and its example resource. Choose removals
deliberately: duplicates, empty data, identical-to-master (ITM) files/rows,
unreferenced master-identical rows (ITNR), portraits, and map metadata differ.
Stale dependencies make comparison unreliable. Identical Loc text may matter
for language compatibility. Compression/encryption also affect packaging.
Do not assume defaults suit every mod. Leave datacore options disabled unless
that workflow is intended.

Run `optimize_pack_file` on the release working copy, inspect removals, save,
and reopen. GUI Save for Release opens optimizer choices; it is not a generic
clean-save guarantee. Mod/Movie notes remain. Report removed content and
warnings; actual game launch/load-order tests are separate.

## Datacores and key deletes

The documented `twad_key_deletes_tables` replacement is specific to **Warhammer
3 patch 6.3+**. Verify game patch and definition before proposing it. Other games
need supported alternatives. Overriding rows, identical copies, and whole-table
datacores have different loading behavior; preserve intended priority.

For migration, identify intended deleted vanilla/parent rows from current data.
Use the selected optimizer conversion option on a working copy, inspect every
generated table/key, then remove old datacores only when the replacement is
understood. Rename the generated delete table to a stable mod-specific name:
rerunning the generator can overwrite its generated filename.

For targeted deletion use `add_keys_to_key_deletes` with its live schema.
Resolve all primary keys and the build's composite-key encoding, not guessed
joined strings. Verify destination table/file and source records. Query incoming
references before deletion. Current diagnostics do not validate key-delete
references, so clean diagnostics are insufficient. Bad keys can silently fail;
deleting referenced rows can crash the game. Confirm behavior with appropriate
in-game/load-order tests; another mod can undo/conflict with deletion.

Sources: [search](https://frodo45127.github.io/rpfm/manual/search/global-search.html),
[references](https://frodo45127.github.io/rpfm/manual/search/references.html),
[diagnostics](https://frodo45127.github.io/rpfm/manual/search/diagnostics.html),
[optimization](https://frodo45127.github.io/rpfm/manual/tutorials/optimising-a-mod.html),
[datacores](https://frodo45127.github.io/rpfm/manual/tutorials/datacores.html).
