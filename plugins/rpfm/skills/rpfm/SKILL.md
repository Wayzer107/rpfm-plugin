---
name: rpfm
description: Use the local RPFM MCP server to inspect, search, extract, diagnose, or edit Total War packfiles, DB tables, localization, and mod dependencies. Use when the user mentions RPFM or asks to work with Total War packs.
---

# RPFM packfile workflow

Use the tools supplied by this plugin's RPFM MCP connection. Match tools by
their operation names; the host may prefix the namespace. If an older direct
RPFM connection is also present, consistently use one connection throughout a
task. Pack keys belong to the session that returned them.

## Establish context

1. Call `get_game_selected` and `list_open_packs` to inspect this session.
2. Determine the intended game and absolute packfile paths from the request and
   available project context. Ask only if required information is missing.
3. When needed, call `set_game_selected` with the supported game key. Inspect
   its live schema before selecting dependency rebuild options.
4. Open the requested files with `open_packfiles`; retain its returned pack
   keys. Use `list_open_packs` to resolve keys and `open_pack_info` to browse.

Each MCP connection has separate open packs and dependencies. A pack open in
the GUI may need opening in this MCP session. Sessions can expire after five
minutes of command inactivity. After an expired-session or unknown-pack error,
re-establish context and reopen source files; do not reuse stale keys or assume
unsaved edits survived. Disclose any lost work before reconstructing it.

## Inspect and edit

Use live tool input schemas as the authority for argument names, types, and
serialization. Read `references/workflows.md` when handling tables, complex
arguments, save operations, or tool errors. The reference links to upstream
documentation; it is guidance rather than an exhaustive tool catalog.

Inspect the relevant data before changing it. For DB rows, resolve the correct
table definition and call `fields_processed` before aligning row values or
validating field count. Preserve keys, data types, table versions, and unrelated
rows. Use dependency and reference queries when a value has linked records.

Honor the user's authorized scope. Inspection requests do not authorize edits.
For changes to source or vanilla packs, default to a separate mod/output pack
or a working copy. Before an authorized overwrite, create a recoverable backup
with local file tools and retain its path. Do not change game installs, saves,
shared RPFM settings, schemas, or run program updates unless the task requires
and authorizes those changes. Existing authorization persists; do not ask again
for routine edits already requested.

Saving decoded data into an open pack is distinct from writing the pack to
disk. Complete both steps for an authorized edit. Check tool responses for
errors even if MCP transport succeeded. Verify changed data by reading it back
and, for a newly written pack, reopening the saved copy. Use focused diagnostics
when they meaningfully verify the requested change. Report the final output
path, affected records/files, backup path if applicable, and any unresolved
diagnostics. Distinguish server verification from testing the mod in the game.

If the connection is unavailable, follow the packaged setup skill. Do not
claim that a shell probe means tools are exposed in the current conversation.
