# Protocol, discovery, and recovery

## MCP

Use Streamable HTTP at `http://127.0.0.1:45127/mcp`. `/ws` is a different
WebSocket protocol. Keep default loopback for local clients. Remote/cloud access
needs an explicit deployment design; account storage does not host the server.

Discover current tools/resources/prompts. The [catalog](tool-catalog.md) holds
all 155 input schemas observed on 2026-10-12; compare with the running build.
Complex definitions, decoded files, search state, and options often have schema
type `string`: encode JSON once into that field. Other fields are actual arrays/
objects. Respect names, optional/null fields, tags, and integer types.

Check JSON-RPC errors and MCP `isError`. Results can contain JSON-serialized
Response enums in text: parse them and inspect `Error` even if transport worked.
Decoded responses can combine data/metadata in tuples; preserve the decoded
enum wrapper for save, not a blindly forwarded tuple.

Use named tools first. `call_command` accepts a JSON string of the actual IPC
Command enum. Match the selected build's variant and argument order/types in
source; do not guess operations absent from the catalog. Never use internal
`Exit` for recovery.

## Resources and prompts

Observed resources (discover availability before reading):

- `rpfm://games`
- `rpfm://enums/PFHFileType`
- `rpfm://enums/CompressionFormat`
- `rpfm://enums/DataSource`
- `rpfm://enums/ContainerPath`
- `rpfm://enums/NewFile`
- `rpfm://enums/SupportedFormats`
- `rpfm://examples/global_search`
- `rpfm://examples/optimizer_options`
- `rpfm://reference/initialization`
- `rpfm://reference/path_conventions`

Observed prompts: `create_new_mod`, `edit_db_table`, `file_operations`,
`manage_dependencies`, `open_and_inspect_pack`, `run_diagnostics`,
`schema_operations`, `search_and_replace`, `translation_workflow`,
`troubleshooting`, `tsv_workflow`. Some hosts expose tools without resources or
prompts; then use packaged guidance and do not claim the resource was read.
Prompt suggestions do not expand authorization for writes/updates/code/publishing.

The live search example supplies `matches`, `search_on`, sources, game key,
pattern/replacement, and case/regex flags. Start with its complete shape and empty
matches. SearchSource differs from DataSource. Preserve returned state for a
requested replacement. Read optimizer defaults and choose options explicitly.

## Sessions and errors

Connections have separate packs/dependencies from GUI/other clients. Settings
are shared. MCP sessions can expire after five minutes without commands. Save
requested work promptly. Fresh connections do not recover old memory. On
unknown-key/session errors query current state and reopen disk inputs. Disclose
unsaved losses; inspect any autosave before claiming recovery.

| Symptom | Diagnosis/recovery |
| --- | --- |
| Refused/stopped endpoint | Follow setup; identify listener/executable, start verified runtime, use bounded readiness retries. |
| Probe works, host tools absent | Check plugin registration/reload; fresh chat or restart may be necessary. |
| Unknown pack key | Inspect this connection's packs; reopen disk sources, never borrow GUI keys. |
| Missing definition/schema | Verify game/schema/table version and authorized acquisition; do not reset settings. |
| Row length/type error | Align processed columns and typed decoded values before retry. |
| Empty reference/diagnostic data | Check path/cache/AK and scope before concluding clean. |
| Save failure | Inspect application error, path/access, and data format; preserve source and separate recovery output. |
| Port collision | Identify owner/endpoint; do not kill another client or randomly change config. |

## WebSocket and documentation drift

Custom clients exchange `{id,data}` messages at `/ws`. Correlate unique nonzero
IDs; `id:0` carries session/shared-settings events. Serde units are strings,
newtypes tagged objects, tuples tagged arrays, and structs tagged objects.
Reconnect with the documented session ID only while valid. Real clients need
timeouts, close/error handling, pending-request rejection, and complete-message
fragment handling.

Send `ClientDisconnecting` for an intentional WebSocket shutdown; do not wait
indefinitely for a response because chapters disagree on whether one is sent.
Client examples also disagree on SettingsAll shape. Live responses and matching
source govern. Example clients need production handling; this plugin does not
bundle one. Rust API modules may advertise different versions; inspect matching
source when examples conflict rather than inventing a new shape.

Sources: [MCP](https://frodo45127.github.io/rpfm/manual/server/mcp.html),
[sessions](https://frodo45127.github.io/rpfm/manual/server/sessions.html),
[WebSocket](https://frodo45127.github.io/rpfm/manual/server/ws-protocol.html),
[types](https://frodo45127.github.io/rpfm/manual/server/ws-shared-types.html),
[commands](https://frodo45127.github.io/rpfm/manual/server/ws-commands.html),
[responses](https://frodo45127.github.io/rpfm/manual/server/ws-responses.html),
[client example](https://frodo45127.github.io/rpfm/manual/server/client-example.html).
