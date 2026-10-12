# Rust Analyzer MCP plugin 0.1.0 for Codex and Claude Code

Connect Codex or Claude Code to the local [`rust-analyzer-mcp`](https://github.com/zeenix/rust-analyzer-mcp)
server for semantic Rust navigation, diagnostics, completions, and refactoring
support. The plugin package does not bundle the MCP server or rust-analyzer.

## Install

Register this repository once if it is not already registered:

```powershell
codex plugin marketplace add Wayzer107/rpfm-plugin --ref main
```

Install or update the plugin:

```powershell
codex plugin add rust-analyzer-mcp@rpfm-marketplace --json
```

Start a fresh Codex chat after installation. Restart the desktop app if its
plugin inventory has not refreshed.

With Claude Code, register the same repository and install from it:

```powershell
claude plugin marketplace add Wayzer107/rpfm-plugin
claude plugin install rust-analyzer-mcp@rpfm-marketplace
```

Inside a Claude Code session the equivalent is `/plugin marketplace add
Wayzer107/rpfm-plugin`, then `/plugin install rust-analyzer-mcp@rpfm-marketplace`.
Restart Claude Code after installation so the MCP server and skills load.

## Set up the server

Ask Codex or Claude Code:

> Use Rust Analyzer MCP setup to install rust-analyzer and the MCP server, then verify the connection.

The setup skill installs the `rust-analyzer` and `rust-src` rustup components and version 0.4.0
of the MCP server from crates.io when they are not already available. It keeps
existing Rust toolchains and settings. See the [setup skill](skills/rust-analyzer-mcp-setup/SKILL.md)
and [installation reference](skills/rust-analyzer-mcp-setup/references/installation.md)
for clean-machine instructions.

## Use Rust Analyzer MCP

The [Rust workflow skill](skills/rust-analyzer-mcp/SKILL.md) sets the workspace
root, uses semantic tools for definitions, references, hover information, and
diagnostics, and guides review of edits returned by the server. Diagnostic
calls can run `cargo check`; feature-gated code may require a project-specific
feature selection.

The MCP process runs locally and can access files permitted to the host
process. Removing the plugin removes its MCP connection, not the Cargo-installed
server, Rust toolchain, or rust-analyzer component.

## Remove

```powershell
codex plugin remove rust-analyzer-mcp@rpfm-marketplace
```

With Claude Code:

```powershell
claude plugin uninstall rust-analyzer-mcp@rpfm-marketplace
```

The server is MIT-licensed. See the
[upstream repository](https://github.com/zeenix/rust-analyzer-mcp) for current
source, release, and license details.
