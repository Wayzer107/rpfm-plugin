# Documentation coverage map

Audit date: 2026-10-12. Plugin: 0.4.0.

All **50 pages** linked from the upstream manual table of contents were fetched
and indexed (about 45,630 extracted words). Narrative chapters were reviewed;
the two long command/shared-type specifications were inspected selectively for
relevant structures and commands. Every page is routed below. This is operational
guidance and source navigation, not a copy of every documented field or a claim
that every operation was exercised.

The [live catalog](tool-catalog.md) captures all 155 tools and complete schemas;
11 resources and 11 prompts were discovered. Four initialization/path/search/
optimizer resources were read. The RPFM 5.1.1 endpoint was checked read-only.
No game/mod files were changed and no advanced editing workflow was run as part
of the audit. Fresh-machine installation and Linux commands remain unexecuted.

The homepage and Rust API landing/module pages were also checked. Selected
server/protocol/type documentation informed the guides. The entire generated
Rust API symbol tree was not read or tested; modules can show different versions.
Use live schemas and matching source when prose/examples conflict.

## GUI orientation

The GUI has a pack tree, editor tabs, dependency tree, search/diagnostics/reference
panels, and notes. Filtering the pack tree finds paths, while global search finds
supported decoded content. Preview tabs differ from opened editor tabs. Modified
markers indicate memory changes, not a completed disk save. Multi-pack clipboard
actions differ from single-pack drag/drop.

Use the command palette (documented Ctrl+P) and action names when a menu differs
between builds. Shortcuts are rebindable; consult the linked shortcut chapter
and Preferences for the actual binding. MCP tools operate server data rather
than clicking GUI widgets. Quick Notes is a per-editor view; pack notes are
available through the dedicated notes view.

## Coverage by chapter

The coverage column explains the scope of the packaged guidance. A route/link
does not mean every GUI control has a named MCP equivalent.

| Manual chapter | Packaged guide | Scope | Review |
| --- | --- | --- | --- |
| [Introduction](https://frodo45127.github.io/rpfm/manual/intro/what-is-rpfm.html) | [Guide](../SKILL.md) | Overview and operational entry point | Chapter reviewed |
| [1. Installation](https://frodo45127.github.io/rpfm/manual/intro/installation.html) | [Guide](../../setup/references/server-installation.md) | Platform/runtime setup; GUI build requirements are separate | Chapter reviewed |
| [2. First-time configuration](https://frodo45127.github.io/rpfm/manual/intro/first-time-config.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [3. The main window](https://frodo45127.github.io/rpfm/manual/packs/main-window.html) | [Guide](documentation-map.md) | GUI navigation notes here and direct chapter link | Chapter reviewed |
| [4. Opening, creating and saving Packs](https://frodo45127.github.io/rpfm/manual/packs/pack-operations.html) | [Guide](workflows.md) | Pack/file/table/notes operations and persistence | Chapter reviewed |
| [5. The Pack tree](https://frodo45127.github.io/rpfm/manual/packs/pack-tree.html) | [Guide](workflows.md) | Pack/file/table/notes operations and persistence | Chapter reviewed |
| [6. Pack settings & notes](https://frodo45127.github.io/rpfm/manual/packs/pack-settings.html) | [Guide](workflows.md) | Pack/file/table/notes operations and persistence | Chapter reviewed |
| [7. Dependencies](https://frodo45127.github.io/rpfm/manual/packs/dependencies.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [8. Plugin scripts](https://frodo45127.github.io/rpfm/manual/packs/plugin-scripts.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [9. Lua tests](https://frodo45127.github.io/rpfm/manual/packs/lua-tests.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [10. Overview](https://frodo45127.github.io/rpfm/manual/editors/overview.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [11. DB tables](https://frodo45127.github.io/rpfm/manual/editors/db.html) | [Guide](workflows.md) | Pack/file/table/notes operations and persistence | Chapter reviewed |
| [12. Loc files](https://frodo45127.github.io/rpfm/manual/editors/loc.html) | [Guide](localization.md) | Local translation workflow; service/Hub publication boundaries | Chapter reviewed |
| [13. Text & scripts](https://frodo45127.github.io/rpfm/manual/editors/text.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [14. Images & DDS](https://frodo45127.github.io/rpfm/manual/editors/images.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [15. Video (CA_VP8)](https://frodo45127.github.io/rpfm/manual/editors/video.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [16. AnimPack](https://frodo45127.github.io/rpfm/manual/editors/animpack.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [17. Animations (AnimTable, AnimFragment, MatchedCombat)](https://frodo45127.github.io/rpfm/manual/editors/animations.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [18. Portrait Settings](https://frodo45127.github.io/rpfm/manual/editors/portrait-settings.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [19. Audio](https://frodo45127.github.io/rpfm/manual/editors/audio.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [20. RigidModel](https://frodo45127.github.io/rpfm/manual/editors/rigidmodel.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [21. Specialised editors (ESF, BMD, UIC, Atlas, …)](https://frodo45127.github.io/rpfm/manual/editors/specialised.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [22. The DB Decoder](https://frodo45127.github.io/rpfm/manual/editors/decoder.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [23. Global Search](https://frodo45127.github.io/rpfm/manual/search/global-search.html) | [Guide](analysis-and-release.md) | Search/diagnostics/release guidance with game and coverage limits | Chapter reviewed |
| [24. Diagnostics panel](https://frodo45127.github.io/rpfm/manual/search/diagnostics.html) | [Guide](analysis-and-release.md) | Search/diagnostics/release guidance with game and coverage limits | Chapter reviewed |
| [25. References panel](https://frodo45127.github.io/rpfm/manual/search/references.html) | [Guide](analysis-and-release.md) | Search/diagnostics/release guidance with game and coverage limits | Chapter reviewed |
| [26. Quick Notes](https://frodo45127.github.io/rpfm/manual/search/notes.html) | [Guide](workflows.md) | Pack/file/table/notes operations and persistence | Chapter reviewed |
| [27. What is MyMod?](https://frodo45127.github.io/rpfm/manual/mymod/overview.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [28. Creating and managing a MyMod](https://frodo45127.github.io/rpfm/manual/mymod/managing.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [29. Import / Export](https://frodo45127.github.io/rpfm/manual/mymod/import-export.html) | [Guide](scripts-and-projects.md) | Workflow guidance and named-tool/GUI/execution boundaries | Chapter reviewed |
| [30. Translator](https://frodo45127.github.io/rpfm/manual/tools/translator.html) | [Guide](localization.md) | Local translation workflow; service/Hub publication boundaries | Chapter reviewed |
| [31. Faction Painter](https://frodo45127.github.io/rpfm/manual/tools/faction-painter.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [32. Unit Editor](https://frodo45127.github.io/rpfm/manual/tools/unit-editor.html) | [Guide](assets-and-specialized.md) | Format guidance; external tools/GUI/build support explicitly qualified | Chapter reviewed |
| [33. Translating a mod](https://frodo45127.github.io/rpfm/manual/tutorials/translating-a-mod.html) | [Guide](localization.md) | Local translation workflow; service/Hub publication boundaries | Chapter reviewed |
| [34. Optimising a mod](https://frodo45127.github.io/rpfm/manual/tutorials/optimising-a-mod.html) | [Guide](analysis-and-release.md) | Search/diagnostics/release guidance with game and coverage limits | Chapter reviewed |
| [35. Datacores (twad_key_deletes)](https://frodo45127.github.io/rpfm/manual/tutorials/datacores.html) | [Guide](analysis-and-release.md) | Search/diagnostics/release guidance with game and coverage limits | Chapter reviewed |
| [36. Overview](https://frodo45127.github.io/rpfm/manual/server/overview.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [37. Sessions & connection lifecycle](https://frodo45127.github.io/rpfm/manual/server/sessions.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [38. WebSocket protocol](https://frodo45127.github.io/rpfm/manual/server/ws-protocol.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [38.1. Shared types](https://frodo45127.github.io/rpfm/manual/server/ws-shared-types.html) | [Guide](protocol-and-recovery.md) | Protocol and live catalog; targeted specification review, not every enum field tested | Targeted sections inspected; complete page indexed |
| [38.2. Commands](https://frodo45127.github.io/rpfm/manual/server/ws-commands.html) | [Guide](protocol-and-recovery.md) | Protocol and live catalog; targeted specification review, not every enum field tested | Targeted sections inspected; complete page indexed |
| [38.3. Responses](https://frodo45127.github.io/rpfm/manual/server/ws-responses.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [39. MCP interface](https://frodo45127.github.io/rpfm/manual/server/mcp.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [40. Client example](https://frodo45127.github.io/rpfm/manual/server/client-example.html) | [Guide](protocol-and-recovery.md) | Protocol, session recovery, and discovery; example-client limitations stated | Chapter reviewed |
| [41. Settings & preferences](https://frodo45127.github.io/rpfm/manual/reference/settings.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [42. Keyboard shortcuts](https://frodo45127.github.io/rpfm/manual/reference/shortcuts.html) | [Guide](documentation-map.md) | GUI navigation notes here and direct chapter link | Chapter reviewed |
| [43. Supported games](https://frodo45127.github.io/rpfm/manual/reference/supported-games.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [44. Schemas & patches](https://frodo45127.github.io/rpfm/manual/reference/schemas.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [45. Telemetry & crash reports](https://frodo45127.github.io/rpfm/manual/reference/telemetry.html) | [Guide](game-configuration.md) | Configuration/schema/dependency guidance; interactive decoder remains GUI | Chapter reviewed |
| [Building from source](https://frodo45127.github.io/rpfm/manual/building.html) | [Guide](../../setup/references/server-installation.md) | Platform/runtime setup; GUI build requirements are separate | Chapter reviewed |

## API entry points

- [RPFM API index](https://frodo45127.github.io/rpfm/api/)
- [File formats/library](https://frodo45127.github.io/rpfm/api/rpfm_lib/index.html)
- [Extensions](https://frodo45127.github.io/rpfm/api/rpfm_extensions/index.html)
- [IPC](https://frodo45127.github.io/rpfm/api/rpfm_ipc/index.html)
- [Server](https://frodo45127.github.io/rpfm/api/rpfm_server/index.html)
- [Matching source/release](https://github.com/Frodo45127/rpfm)

## Material gaps fixed since 0.3.0

Game readiness checks; schemas/AK/cache distinctions; complete persistence;
TSV replacement semantics; reference-aware renames; all-pack diagnostics;
Lua emulation limits; script execution and MyMod boundaries; translation
review/Hub scope; optimization/datacore precautions; asset support limits;
resource/prompt discovery; WebSocket/example drift; platform installation.

## Boundaries that remain

This package provides instructions and registration for the upstream server.
It does not implement missing GUI actions, bundle game/AK data, contain a
complete animation/audio/model authoring suite, or guarantee game behavior.
A matching tool catalog and complete chapter map improve guidance but do not
substitute for saved-data checks and task-specific in-game validation.
