# Packfiles and tables

## Pack lifecycle and paths

Inspect `list_open_packs`, select the intended game, and open absolute disk
paths with `open_packfiles`. Its returned key identifies this session's pack;
use `open_pack_info` to enumerate contents. Inspect multi-path opening semantics
before using it to load independent mods: it can merge input packs. `new_pack`
creates an in-memory output; `save_pack_as` gives it a new absolute disk path.

Disk paths and internal paths differ. Internal paths use `/`, relative to the
pack root: `db/land_units_tables/my_mod`, `text/db/my_mod.loc`, or
`script/campaign/mod/my_mod.lua`. Inspect actual paths; conventions vary by game
and purpose. ContainerPath is tagged (`{"File":"..."}` or `{"Folder":"..."}`),
while the tool argument may contain that structure as a JSON string. Refer to
the live schema and enum resources.

Browse with `get_packed_files_info`, `get_rfile_info`, and `decode_packed_file`.
Sources include PackFile, GameFiles, ParentFiles, AssKitFiles, and ExternalFile.
Prefer specific dependency lookup/import over opening every vanilla pack;
`load_all_ca_pack_files` can be expensive and broaden scope. Extract to a
separate directory and inspect returned paths. Create files only using the
current NewFile enum/definition; add files from disk or another pack with the
named add operations.

Before rename/move inspect referencing DB/text fields. `rename_packed_files`
changes paths without repairing table references. Copy/cut/paste uses a session
clipboard; a cut can remove source content on paste. Check both packs,
collisions, and destinations. Folder operations affect children. Prefer explicit
file selections for narrow changes. Inspect generated duplicate paths.

## DB editing sequence

1. Enumerate tables with `get_tables_by_table_name` and inspect the exact file.
2. Decode it and preserve representation/metadata. Resolve the definition for
   its game, table name, and version. Do not upgrade old versions just because
   a newer definition exists.
3. Call `fields_processed`. Raw fields can split colors or expand differently
   from actual rows. Use processed columns to map values and validate exact
   row length/types. Identify all primary-key fields.
4. Match complete target keys and inspect dependencies/references. Preserve
   typed cells, enum wrappers, unknown fields, and unrelated records.
5. Pass the modified RFileDecoded value to `save_packed_file_from_view`.
   The audited tool takes `data` as a JSON string. Match its live schema and
   serialize once rather than repeatedly.
6. Read back the table, save with `save_pack_as` for a new output or
   `save_packfile` for an authorized existing path, then reopen the disk output
   and verify values, row count, keys, and relevant references.

`merge_files` requires compatible definitions; `delete_source` is consequential.
Review source order/duplicate keys. `update_table` can change columns/defaults;
retain a pre-update copy and inspect results. `cascade_edition` changes linked
data: resolve affected records and authorization before calling. Shared schema
edits are not a routine way to silence row validation errors.

## TSV round trips

Export the actual table with `export_tsv` and retain a baseline. RPFM TSV has
column-name and metadata header rows containing table identity/version/path.
Preserve headers, order, encoding, booleans, empty values, and numeric precision.
Import replaces table data rather than applying a sparse patch. Spreadsheets
can alter keys, leading zeroes, and scientific notation.

RPFM script-export conventions use CRLF and disabled quoting; avoid embedded
tab/newline delimiters. Check the actual export and table-order settings instead
of generating guessed generic TSV. Import into the intended pack/path, decode
to validate the complete table, and save the pack separately. See
[localization](localization.md) for Loc-specific concerns.

## Metadata and notes

Mod is the usual launcher-enabled type. Movie loads automatically, changing
deployment behavior. Boot/Release/Patch omit reserved notes, dependency-manager,
and pack-settings sections on save. Do not change type merely to strip notes.
Read `get_pack_settings` and parent declarations before editing.

Compression depends on game and file type. Older games can crash on compressed
DB tables; do not infer support from chronological release order. Verify the
running build's compatibility before changing compression/header flags.
Encryption needs supported headers (PFH4+). Preserve existing flags unless a
deliberate packaging change is requested.

Use `notes_for_path`, `add_note`, and `delete_note` with current IDs/paths.
Notes can attach to files or packs and include URLs. Quick Notes is a GUI view;
dependency-only files do not have editable pack notes. Save for Release runs
optimization but retains notes in Mod/Movie packs.

## Persistence and recovery

Decoded-file save changes memory; pack save writes disk. Query current keys
after save/rename changes. Closing packs discards unsaved work. Autosave is
supplementary; retain a disk backup before overwriting originals.

Inspect save errors, permissions, and data format before retrying.
`clean_and_save_pack_as` is recovery that may change content; use a separate
output and compare what survived. Never label a rescued pack complete without
checking its contents. Do not clear caches/discard packs as blind repairs.

Sources: [pack operations](https://frodo45127.github.io/rpfm/manual/packs/pack-operations.html),
[pack tree](https://frodo45127.github.io/rpfm/manual/packs/pack-tree.html),
[DB editor](https://frodo45127.github.io/rpfm/manual/editors/db.html),
[pack settings](https://frodo45127.github.io/rpfm/manual/packs/pack-settings.html).
