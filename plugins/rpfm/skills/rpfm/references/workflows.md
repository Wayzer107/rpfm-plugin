# Operation guidance

Discover the live tool schemas before calls. These examples identify operations,
not complete argument templates for every RPFM build.

| Task | Operations to inspect |
| --- | --- |
| Select game and open packs | `get_game_selected`, `set_game_selected`, `open_packfiles`, `list_open_packs` |
| Inspect files | `open_pack_info`, `get_packed_files_info`, `decode_packed_file` |
| Find records or references | `global_search`, `search_references`, `go_to_definition` |
| Resolve table layout | `definition_by_table_name_and_version`, `definitions_by_table_name`, `fields_processed` |
| Dependencies | `get_tables_from_dependencies`, `dependencies_column_values`, `get_rfiles_from_all_sources` |
| Table and localization edits | `save_packed_file_from_view`, `import_tsv`, `export_tsv`, `new_packed_file` |
| Extract files | `extract_packed_files` |
| Persist pack | `save_pack_as`, `save_packfile` |
| Diagnose pack | `diagnostics_check`, `get_missing_definitions` |

## Tables and argument encoding

Definition fields can describe a different layout from processed row fields.
Use `fields_processed` before constructing rows; keep its column order and
types. Inspect decoded data to preserve the exact server representation.

Some complex arguments are JSON encoded strings. If the schema says `string`
for a container path list or definition, serialize the structured value once
into that field. If it says `object` or `array`, pass structured JSON directly.
Never guess enum spelling from a UI label.

## Persistence and errors

`save_packed_file_from_view` updates decoded content in an open pack.
`save_pack_as` or `save_packfile` persists the pack on disk. Keep the returned
key from opening or saving operations; re-query current keys when needed.
Do not use `close_pack` to discard unsaved work until the user intends it.

Responses may contain serialized RPFM response enums in MCP text content.
Decode them and check for application errors. A successful HTTP request is
not proof that a command succeeded. Diagnose an error before retrying a write.
Use `call_command` only when no suitable named tool exists and the upstream
command format is known. Do not fall back to speculative commands.

## Upstream references

- MCP interface: https://frodo45127.github.io/rpfm/manual/server/mcp.html
- Server overview: https://frodo45127.github.io/rpfm/manual/server/overview.html
- Full server reference: https://frodo45127.github.io/rpfm/#server
- Source: https://github.com/Frodo45127/rpfm
