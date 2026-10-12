# Serena and Rust Analyzer MCP verification

Verification performed on 2026-10-12 in the Linux x86_64 cloud workspace.
Runtime installations, source fixtures, and Serena configuration used temporary
directories. Temporary Codex marketplace/plugin registrations were removed
after the installation check.

## Package checks

- All nine tests pass: seven offline packaging tests and two live MCP
  integration tests. The final combined run completed in 55.9 seconds.
- All three portable plugin manifests and MCP configurations pass the official
  Agent Plugins 1.0.0 JSON schemas.
- Seven offline packaging tests check required catalog entries, package paths,
  synchronized manifests and MCP configuration, listing constraints, skill
  frontmatter, and local documentation links.
- Codex CLI `0.159.0-alpha.3` registered a temporary local marketplace and
  installed both new plugin packages at version `0.1.0` successfully.

## Runtime checks

The configured stdio commands were exercised against a disposable Cargo
workspace containing `add` and `doubled` functions.

| Runtime | Tested result |
| --- | --- |
| Serena `1.7.0`, installed with `uv tool install -p 3.13 serena-agent` | `serena init` succeeds; MCP discovers 24 tools in the Codex context; the active project and language server are ready; symbol overview returns both fixture functions. |
| Rust Analyzer MCP `0.4.0`, installed with `cargo install rust-analyzer-mcp --version 0.4.0 --locked` | MCP discovers 11 tools; workspace selection and symbol lookup succeed; diagnostics return zero errors; hover returns the correct function type; rename proposes two edits and leaves the source file unchanged. |

The Rust toolchain was installed with rustup's minimal profile, using stable
Rust `1.99.0` and its rust-analyzer component. rust-analyzer installed `rust-src`
while loading the fixture; setup instructions now install that component
explicitly. An initial Rust hover query before
indexing completed returned `null`; after the diagnostic check completed, hover
returned the expected type. The workflow skill already instructs callers to
wait for indexing and avoid treating empty startup results as conclusive.

## Repeat the checks

```sh
python3 -m unittest discover -s tests -v
uv run scripts/validate_schemas.py
PLUGIN_MCP_INTEGRATION=1 python3 -m unittest discover -s tests -v
```

The first command is offline and skips live server tests. The schema command
fetches the declared official schemas. The integration command requires
Serena, rust-analyzer, Rust Analyzer MCP, Cargo, and Git on PATH and exercises
the real servers using disposable projects and configuration. Rust diagnostics
are retried at most three times when the server explicitly reports incomplete
checks; the test fails if a complete result is still unavailable.

## Limits

The runtime tests cover Linux. Windows and macOS installer commands were not
executed. Codex package registration/installation and direct MCP calls were
tested; an interactive Codex chat using the installed tools was not run.
The Serena test configuration disables automatic dashboard/browser startup.
No advanced project refactor was applied, and the existing RPFM runtime was
not retested as part of these additions.
