---
name: serena
description: Use Serena's MCP tools for symbol-aware code navigation, reference tracing, and focused refactoring in a project. Use when a task benefits from semantic understanding rather than text search alone.
---

# Serena code workflow

Use one Serena connection for the project. If its tools are missing, follow
[Serena setup](../serena-setup/SKILL.md) before code work. Treat live MCP schemas
and the active project's Serena instructions as authoritative.

## Activate and understand the project

1. Confirm the intended project root from the task and workspace.
2. If Serena has no active project, use its `activate_project` tool with the
   intended directory. The host app (for example the Codex App) may not start in the repository
   directory.
3. Read Serena's initial instructions and relevant project memories before
   choosing a workflow. Do not create or overwrite memories unless useful and
   within the user's request.
4. Use the symbol overview/search tools to find the relevant module and
   declaration. Resolve references and callers before changing shared APIs.

## Make focused changes

- Prefer symbol-aware lookup and edits for functions, types, and other language
  symbols. Use text search for non-code files or when the language server lacks
  the needed capability.
- Inspect the target symbol and nearby call sites before editing. Preserve
  unrelated code, public interfaces, and user changes.
- Use rename/refactor tools only for the requested scope. Review the affected
  locations before accepting broad changes.
- Confirm what the tool actually changed, then inspect the resulting diff. Run
  project checks only when they fit the task and are authorized.

## Recovery and limits

After reconnecting, re-check the active project instead of assuming prior
server state survived. If symbol results are empty or incomplete, check project
activation, language-server availability, indexing, and workspace configuration
before treating the result as proof that a symbol is unused. Serena's language
server capabilities vary by language; consult its live tools and
[language support](https://oraios.github.io/serena/01-about/020_programming-languages.html).
