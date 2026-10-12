# Install Rust Analyzer MCP

The plugin registers the local stdio command `rust-analyzer-mcp`. Install the
Rust toolchain, rust-analyzer component, and server separately on the computer
running Codex or Claude Code. The selected server release is version 0.4.0 from the
[`zeenix/rust-analyzer-mcp`](https://github.com/zeenix/rust-analyzer-mcp)
project and crates.io.

## 1. Install Rust if needed

Use the official [rustup installation page](https://rustup.rs/) for the user's
operating system. On Windows, download and run `rustup-init.exe` from that page.
On macOS/Linux, the official installer is:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Restart the shell when installation finishes. On macOS/Linux, load Cargo's
environment in the current shell if needed:

```sh
. "$HOME/.cargo/env"
```

Check the active toolchain with `rustup show`. If none exists, choose a stable
toolchain before continuing:

```sh
rustup default stable
```

Do not change an existing project override or default toolchain merely to
install the server.

## 2. Install rust-analyzer and Rust sources

Add rust-analyzer and the standard library sources to the project's toolchain.
The `rust-src` component supports standard library navigation and prevents
rust-analyzer from needing to install those sources during its first analysis:

```sh
rustup component add rust-analyzer rust-src
rust-analyzer --version
```

If the project pins a separate toolchain in `rust-toolchain.toml`, ensure the
component is installed for that toolchain as well. Keep project toolchain
selection unchanged.

```sh
rustup component add rust-analyzer rust-src --toolchain TOOLCHAIN_NAME
```

## 3. Install the MCP server

Install the published crate and retain its lockfile dependency versions:

```sh
cargo install rust-analyzer-mcp --version 0.4.0 --locked
rust-analyzer-mcp --help
```

Cargo normally places the executable in `$HOME/.cargo/bin` on macOS/Linux or
`%USERPROFILE%\.cargo\bin` on Windows. Start a new Codex or Claude Code process after
Cargo updates PATH.

## 4. Use the packaged MCP connection

The plugin's portable `mcp.json` and the `.mcp.json` read by Codex and Claude
Code register:

```json
{
  "mcpServers": {
    "rust-analyzer-mcp": {
      "type": "stdio",
      "command": "rust-analyzer-mcp"
    }
  }
}
```

Do not also add the same server with `codex mcp add` or `claude mcp add`.
After installation, start a new chat and check `/mcp`. If the shell finds the
executable but the host does not, restart the host from the updated shell or set `command` to the executable's
full path using a host-supported MCP configuration. Do not edit the plugin
cache.

The server's workspace state belongs to its MCP connection. At the start of a
project task, choose the actual Cargo workspace root with the
`rust_analyzer_set_workspace` tool before querying symbols or diagnostics.

## Local behavior and limits

The server is a child process of the MCP host and can access files available to that
process. `rust_analyzer_diagnostics` runs a fresh `cargo check`; workspace-wide
diagnostics can take longer and may create normal Cargo build artifacts. The
server uses the project's default Cargo features unless configured otherwise.
Do not force `--all-features` globally; features can be mutually incompatible.
Rename and formatting results are returned edits, so inspect and apply them
through authorized workspace tools. Removing the plugin does not uninstall
rustup components, Cargo binaries, or user settings.
