# Assets and specialized tools

Determine decoded type, game/version, and running build before editing. Library
decode support, GUI controls, and named MCP operations differ. Preserve original
bytes and unsupported fields. Unknown binaries are not editable text. External
replacements must preserve paths, dimensions, formats, and references. Saved-data
validation differs from visual/audio game tests.

| Format/task | Practical route and limits |
| --- | --- |
| Images/DDS | GUI viewing; substantive editing needs external tools. Extract/replace intended assets and check dimensions/compression/alpha. |
| Video | CA_VP8/IVF conversion via `set_video_format`; not a full editor or arbitrary transcoder. Inspect actual format. |
| Audio | Playback/inspection does not imply arbitrary bank authoring. Use external tools for unsupported edits; verify codecs/references. |
| AnimPack | Nested add/extract/delete operations preserve inner paths and outer archive. Inner rename may require extract/reinsert rather than ordinary pack rename. |
| AnimFragmentBattle | Game/version-specific structures; preserve skeletons, animation refs, slots, and metadata. |
| AnimsTable/MatchedCombat | Structured/debug editing with game-specific layouts. Library `.anim` reading is not a complete animation editor. |
| PortraitSettings | Edit art sets/variants/textures/masks; inspect local/dependency IDs and every referenced asset. |
| RigidModel | Detailed page describes metadata/material/texture/LOD edits; overview is more conservative. Probe actual decoded build. Geometry remains external. `export_rigid_to_gltf` exports, not arbitrary mesh authoring. |
| Atlas | Regions/dimensions must agree with source texture coordinates. |
| GroupFormations | Layout varies by game; preview/simulation is not engine validation. |
| UnitVariant | Preserve meshes, variant refs, and weights; GUI/debug views differ. |
| ESF | Save/startpos data can be large and debug/feature gated. Work on explicitly authorized copies; protect real saves. |
| BMD/UIC | JSON/debug/feature support varies; verify build before promising editable round trips. |
| VMD/WSModel | Often text-backed; preserve XML/model paths and linked assets. |

For structured edits retain RFileDecoded, change understood fields, save memory
and a separate pack, then read back. For external editing use extraction and
`save_packed_file_from_external_view` or supported add operations. Launching
`open_packed_file_in_external_program` executes an associated local application;
use for the intended editing task. Reimport/verify rather than assuming external
save already persisted the containing pack.

## Faction Painter and Unit Editor

Faction Painter is a GUI over game-specific faction/banner/uniform colors.
There is no named painter tool in the snapshot. Resolve actual tables/keys and
processed color representation for equivalent DB edits; do not invent RGB fields.

Unit Editor is experimental and documented for Warhammer 2/3; it does not expose
every unit field/asset. Cloning requires linked keys, Loc, permissions/groupings,
recruitment, costs, and assets according to game schema. One changed row is not
a complete unit. No named unit-editor tool was found. Use actual DB operations
or GUI and report remaining linked work and game validation.

The [documentation map](documentation-map.md) links every editor chapter.
Do not enable debug/render features or add large dependencies merely to browse
data when a raw/decoded read answers the task.

Sources: [overview](https://frodo45127.github.io/rpfm/manual/editors/overview.html),
[RigidModel](https://frodo45127.github.io/rpfm/manual/editors/rigidmodel.html),
[specialized](https://frodo45127.github.io/rpfm/manual/editors/specialised.html),
[Painter](https://frodo45127.github.io/rpfm/manual/tools/faction-painter.html),
[Unit Editor](https://frodo45127.github.io/rpfm/manual/tools/unit-editor.html).
