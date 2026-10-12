---
name: rust-analyzer-mcp
description: Use rust-analyzer-mcp for semantic navigation, completion, diagnostics, and refactoring in Rust workspaces. Use when a Rust task needs compiler-aware context or symbol relationships.
---

# Rust Analyzer MCP workflow

Use one Rust Analyzer MCP connection for the project. If the tools are missing,
follow [setup](../rust-analyzer-mcp-setup/SKILL.md) first. Live MCP schemas and
the selected server's current documentation are authoritative.

## Select the workspace

1. Resolve the intended Cargo workspace root from the task and repository.
   For a monorepo, use the requested crate or nested workspace when appropriate.
2. Call `rust_analyzer_set_workspace` with that root before querying symbols.
3. Confirm the target file belongs to the selected workspace and allow initial
   indexing to finish. Empty or partial results during startup are not proof
   that a symbol or diagnostic is absent.

## Investigate Rust code

- Use symbols, definition, references, and hover tools to understand the target
  and its call sites. Position arguments use the units and schema documented by
  the live server tools.
- Use completion or code actions only for the relevant file/range, then inspect
  the server's returned result.
- A file diagnostic runs a fresh `cargo check`. Workspace diagnostics check
  more code and can take longer; explain that cost when relevant. Check active
  feature selection before treating missing feature-gated symbols as errors.
- If diagnostics include a `note` saying loading or checking is incomplete,
  retry after the workspace becomes ready. Keep those results pending until a
  complete response is returned; zero reported errors alone is insufficient.

## Apply changes carefully

- The server's rename operation returns workspace edits and does not write
  files. Formatting also returns edits to apply. Review affected paths and
  changes, then apply only the authorized edits through workspace tools.
- Code actions may produce edits or other results; follow the live schema and
  inspect the result before applying anything.
- Preserve user changes and unrelated code. After applying an edit, inspect the
  diff and re-query the affected symbol. Run tests or Cargo checks only when
  they fit the user's request and are authorized.

## Recovery

If tools fail, re-check the active workspace, Cargo toolchain, rust-analyzer
component, indexing status, and the exact MCP error. After reconnecting, select
the workspace again; do not assume state carried over from a previous server
process. Consult the
[upstream README](https://github.com/zeenix/rust-analyzer-mcp#readme) for
server-specific behavior and current options.
