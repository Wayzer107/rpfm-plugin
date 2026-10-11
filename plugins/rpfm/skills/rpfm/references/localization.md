# Localization and translation

## Loc edits

Decode Loc and preserve key/text/tooltip cells and typed representation. Match
full keys, check duplicates, and preserve markup, placeholders, line breaks,
and game formatting. `go_to_loc`, `get_source_data_from_loc_key`, and reference
lookups establish origin/usage. The tooltip field exists; do not infer a new
meaning or rewrite it. Follow the pack guide's complete save/read-back sequence.

For bulk edits export the actual TSV, keep headers/encoding, and validate
imported keys/counts. Avoid spreadsheet key conversion or flattened control
characters. `generate_missing_loc_data` can derive entries from DB fields;
inspect results, supply text, and preserve existing translations.

## Translator

Establish source/target languages, game, mod, and parents. `get_pack_translation`
retrieves data; it does not itself write a translated pack.
`generate_vanilla_translation_source` obtains a source-language baseline from
locale packs. Missing locale packs limit coverage; do not change Steam language
or install language data without a matching request.

Preserve original/translated text, review state, source language, authors,
glossary, flags, and the actual format (old format-0 and newer format-1 differ).
Reconcile changed/removed keys instead of marking all strings current. Review
new/outdated text, placeholders, markup, terminology, and names before publishing.
Machine translation is not automatically reviewed/approved text.

For MCP output, prepare Loc via standard decoded/TSV edits and disk save.
Verify game-specific path/priority from actual sources. The tutorial uses a
high-priority translated filename for newer games and a different convention
for older titles/Thrones of Britannia; do not apply one universally. Preserve
the original mod and verify load order.

The catalog has translation retrieval/vanilla-source generation but not every
GUI review/export/Hub action. Use GUI or an exact verified `call_command` enum
for missing actions; do not invent a translator-save tool.

## Services and Hub

AI/DeepL credentials belong in supported local settings/keyring, not packfiles,
prompts, Git, or diagnostic dumps. Read only needed settings and redact secrets.
A local translation request does not authorize uploading text to an external
service or submitting it to GitHub. Follow existing explicit service/publication
authorization and finish reviewable local outputs first. For Hub contributions
verify authors, target language, mod/version, submitted content, and resulting
PR/reference. Preserve originals and translation metadata.

Verify saved Loc and unresolved status. Loading it in the target-language game
is separate: correct bytes do not prove the engine selected the intended text.

Sources: [Loc](https://frodo45127.github.io/rpfm/manual/editors/loc.html),
[Translator](https://frodo45127.github.io/rpfm/manual/tools/translator.html),
[tutorial](https://frodo45127.github.io/rpfm/manual/tutorials/translating-a-mod.html).
