# Complete discovered tool catalog

Captured 2026-10-12 from RPFM 5.1.1: **155 tools**. These are upstream
operations exposed through the plugin connection, not 155 custom tools
implemented by this plugin. Discovery does not test their behavior.

The [JSON catalog](tool-catalog.json) contains every description and complete
input schema. The [discovery snapshot](discovery-snapshot.json) lists 11
resources, 11 prompts, and four read-only resource examples for offline
reference. Prefer current discovery over either snapshot.

Required arguments below are names only. Optional arguments, defaults,
types, nested structures, and JSON-string encoding are in the catalog.
Consult the matching task guide before using write/update/script/game tools.

| Operation | Required arguments |
| --- | --- |
| `add_keys_to_key_deletes` | `pack_key`, `table_file_name`, `key_table_name`, `keys` |
| `add_line_to_pack_ignored_diagnostics` | `pack_key`, `value` |
| `add_note` | `pack_key`, `note` |
| `add_packed_files` | `pack_key`, `source_paths`, `destination_paths` |
| `add_packed_files_from_animpack` | `anim_pack_key`, `pack_key`, `source`, `animpack_path`, `container_paths` |
| `add_packed_files_from_pack_file` | `pack_key`, `source_pack_path`, `container_paths` |
| `add_packed_files_from_pack_file_to_animpack` | `source_pack_key`, `pack_key`, `animpack_path`, `container_paths` |
| `assembly_kit_path` | none |
| `backup_autosave_path` | none |
| `backup_settings` | none |
| `build_starpos` | `pack_key`, `campaign_id`, `process_hlp_spd` |
| `build_starpos_check_victory_conditions` | `pack_key` |
| `build_starpos_cleanup` | `pack_key`, `campaign_id`, `process_hlp_spd` |
| `build_starpos_get_campaign_ids` | `pack_key` |
| `build_starpos_post` | `pack_key`, `campaign_id`, `process_hlp_spd` |
| `call_command` | `command` |
| `cascade_edition` | `pack_key`, `table_name`, `definition`, `changes` |
| `change_compression_format` | `pack_key`, `format` |
| `change_data_is_encrypted` | `pack_key`, `value` |
| `change_index_includes_timestamp` | `pack_key`, `value` |
| `change_index_is_encrypted` | `pack_key`, `value` |
| `check_empire_and_napoleon_ak_updates` | none |
| `check_lua_autogen_updates` | none |
| `check_schema_updates` | none |
| `check_translations_updates` | none |
| `check_updates` | none |
| `clean_and_save_pack_as` | `pack_key`, `path` |
| `clean_cache` | `pack_key`, `paths` |
| `clear_settings` | none |
| `close_all_packs` | none |
| `close_pack` | `pack_key` |
| `config_path` | none |
| `copy_packed_files` | `paths_by_pack` |
| `cut_packed_files` | `paths_by_pack` |
| `decode_packed_file` | `pack_key`, `path`, `source` |
| `definition_by_table_name_and_version` | `name`, `version` |
| `definitions_by_table_name` | `value` |
| `delete_definition` | `name`, `version` |
| `delete_from_animpack` | `pack_key`, `animpack_path`, `container_paths` |
| `delete_note` | `pack_key`, `path`, `id` |
| `delete_packed_files` | `pack_key`, `paths` |
| `dependencies_art_set_ids` | none |
| `dependencies_cache_path` | none |
| `dependencies_column_values` | `table_name`, `column_name` |
| `diagnostics_check` | `ignored`, `check_ak_only_refs` |
| `diagnostics_update` | `diagnostics`, `paths`, `check_ak_only_refs` |
| `duplicate_packed_files` | `pack_key`, `paths` |
| `export_rigid_to_gltf` | `rigid_model`, `output_path` |
| `export_tsv` | `pack_key`, `tsv_path`, `table_path` |
| `extract_packed_files` | `pack_key`, `source_paths`, `destination_path`, `export_as_tsv` |
| `fields_processed` | `definition` |
| `folder_exists` | `pack_key`, `value` |
| `generate_dependencies_cache` | none |
| `generate_missing_loc_data` | `pack_key` |
| `generate_vanilla_translation_source` | `src_lang` |
| `get_anim_paths_by_skeleton_name` | `value` |
| `get_custom_table_list` | none |
| `get_dependency_pack_files_list` | `pack_key` |
| `get_game_selected` | none |
| `get_missing_definitions` | `pack_key` |
| `get_optimizer_options` | none |
| `get_pack_file_name` | `pack_key` |
| `get_pack_file_path` | `pack_key` |
| `get_pack_settings` | `pack_key` |
| `get_pack_translation` | `pack_key`, `language` |
| `get_packed_file_raw_data` | `pack_key`, `value` |
| `get_packed_files_info` | `pack_key`, `values` |
| `get_packed_files_names_starting_with_path_from_all_sources` | `path` |
| `get_reference_data_from_definition` | `pack_key`, `table_name`, `definition`, `force` |
| `get_rfile_info` | `pack_key`, `value` |
| `get_rfiles_from_all_sources` | `paths`, `lowercase` |
| `get_schema` | none |
| `get_source_data_from_loc_key` | `pack_key`, `value` |
| `get_table_definition_from_dependency_pack_file` | `value` |
| `get_table_list_from_dependency_pack_file` | none |
| `get_table_version_from_dependency_pack_file` | `value` |
| `get_tables_by_table_name` | `pack_key`, `value` |
| `get_tables_from_dependencies` | `value` |
| `global_search` | `pack_key`, `search` |
| `global_search_replace_all` | `pack_key`, `search` |
| `global_search_replace_matches` | `pack_key`, `search`, `matches` |
| `go_to_definition` | `pack_key`, `table_name`, `column_name`, `values` |
| `go_to_loc` | `pack_key`, `value` |
| `import_dependencies_to_open_pack_file` | `pack_key`, `paths` |
| `import_schema_patch` | `patches` |
| `import_tsv` | `pack_key`, `tsv_path`, `table_path` |
| `initialize_my_mod_folder` | `name`, `game`, `sublime`, `vscode` |
| `is_schema_loaded` | none |
| `is_there_a_dependency_database` | `value` |
| `list_open_packs` | none |
| `live_export` | `pack_key` |
| `load_all_ca_pack_files` | none |
| `local_art_set_ids` | `pack_key` |
| `lua_run_tests` | `test_source` |
| `merge_files` | `pack_key`, `paths`, `merged_path`, `delete_source` |
| `new_pack` | none |
| `new_packed_file` | `pack_key`, `path`, `new_file` |
| `notes_for_path` | `pack_key`, `value` |
| `old_ak_data_path` | none |
| `open_containing_folder` | `pack_key` |
| `open_pack_info` | `pack_key` |
| `open_packed_file_in_external_program` | `pack_key`, `source`, `container_path` |
| `open_packfiles` | `paths` |
| `optimize_pack_file` | `pack_key`, `options` |
| `pack_map` | `pack_key`, `tile_maps`, `tiles` |
| `packed_file_exists` | `pack_key`, `value` |
| `paste_packed_files` | `pack_key`, `destination_path` |
| `patch_siege_ai` | `pack_key` |
| `rebuild_dependencies` | `value` |
| `referencing_columns_for_definition` | `table_name`, `definition` |
| `remove_local_schema_patches_for_table` | `value` |
| `remove_local_schema_patches_for_table_and_field` | `key`, `value` |
| `rename_packed_files` | `pack_key`, `renames` |
| `restore_backup_settings` | none |
| `save_local_schema_patch` | `patches` |
| `save_pack_as` | `pack_key`, `path` |
| `save_packed_file_from_external_view` | `pack_key`, `internal_path`, `external_path` |
| `save_packed_file_from_view` | `pack_key`, `path`, `data` |
| `save_packed_files_to_pack_file_and_clean` | `pack_key`, `files`, `optimize` |
| `save_packfile` | `pack_key` |
| `save_schema` | `schema` |
| `schemas_path` | none |
| `search_references` | `pack_key`, `reference_map`, `value` |
| `set_dependency_pack_files_list` | `pack_key`, `list` |
| `set_game_selected` | `game_name`, `rebuild_dependencies` |
| `set_pack_file_type` | `pack_key`, `pack_file_type` |
| `set_pack_settings` | `pack_key`, `settings` |
| `set_video_format` | `pack_key`, `path`, `format` |
| `settings_clear_path` | `path` |
| `settings_get_all` | none |
| `settings_get_bool` | `value` |
| `settings_get_f32` | `value` |
| `settings_get_i32` | `value` |
| `settings_get_path_buf` | `value` |
| `settings_get_string` | `value` |
| `settings_get_vec_raw` | `value` |
| `settings_get_vec_string` | `value` |
| `settings_set_bool` | `key`, `value` |
| `settings_set_f32` | `key`, `value` |
| `settings_set_i32` | `key`, `value` |
| `settings_set_path_buf` | `key`, `value` |
| `settings_set_string` | `key`, `value` |
| `settings_set_vec_raw` | `key`, `value` |
| `settings_set_vec_string` | `key`, `value` |
| `table_profiles_path` | none |
| `translations_local_path` | none |
| `trigger_backup_autosave` | `pack_key` |
| `update_anim_ids` | `pack_key`, `starting_id`, `offset` |
| `update_current_schema_from_asskit` | none |
| `update_empire_and_napoleon_ak` | none |
| `update_lua_autogen` | none |
| `update_main_program` | none |
| `update_schemas` | none |
| `update_table` | `pack_key`, `value` |
| `update_translations` | none |

Sources: [MCP manual](https://frodo45127.github.io/rpfm/manual/server/mcp.html)
and actual tools/list, resources/list, prompts/list, and selected resources/read.
