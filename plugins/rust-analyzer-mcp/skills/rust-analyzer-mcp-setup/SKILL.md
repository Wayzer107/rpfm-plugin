---
name: rust-analyzer-mcp-setup
description: Install or repair rust-analyzer and the local rust-analyzer-mcp server, then make the server available through this plugin. Use when the server is missing, disconnected, or newly installed.
---

# Set up Rust Analyzer MCP

The plugin starts the `rust-analyzer-mcp` executable as a local stdio server.
When the user asks for setup, check the existing toolchain, install only
missing prerequisites, and verify the MCP connection.

## Check current tools

1. If Rust Analyzer MCP tools are callable, make a harmless read-only call in
   the intended project and reuse the working installation.
2. Otherwise check `rustup show`, `cargo --version`, `rust-analyzer --version`,
   and `rust-analyzer-mcp --help`. On Windows use `Get-Command` to locate the
   executables; on macOS/Linux use `command -v`.
3. Read the [installation reference](references/installation.md) for clean
   machine setup and Cargo PATH recovery.

## Install and connect

If rustup is missing, install it from the official instructions for the user's
operating system. Preserve existing toolchain overrides and settings. Add the
`rust-analyzer` and `rust-src` components to the toolchain used by the workspace, then install
the selected server release:

```sh
rustup component add rust-analyzer rust-src
cargo install rust-analyzer-mcp --version 0.4.0 --locked
```

If no Rust toolchain is installed, select a stable toolchain with rustup before
adding the component. Do not overwrite an existing `rust-toolchain.toml`,
project override, or Cargo configuration as a generic setup step.

The plugin already registers the stdio MCP server. Do not also run `codex mcp
add` or `claude mcp add` for the same server. After installation, open a fresh
chat (or restart Claude Code), confirm the server in `/mcp`, set the intended workspace with
`rust_analyzer_set_workspace`, and make a harmless read-only call.

## Report

Report toolchain, component, server executable, MCP connection, and callable
tool checks separately. If the shell sees `rust-analyzer-mcp` but the host
(Codex or Claude Code) does not, refresh the host process or follow the
reference to set the full executable path in a host-supported MCP
configuration. A shell check alone does not prove the host loaded the server.
