# Install Serena and connect the plugin

This plugin registers a local stdio MCP process. Codex runs:

```text
serena start-mcp-server --project-from-cwd --context=codex
```

Claude Code reads `.claude-plugin/plugin.json` instead and runs the same command
with `--context=claude-code`, which omits Serena tools that duplicate Claude
Code's built-in file and shell tools.

Serena itself is installed separately on each computer. No API key or hosted
server is required. Follow the current [Serena Quick Start](https://github.com/oraios/serena#quick-start)
and [client guide](https://oraios.github.io/serena/02-usage/030_clients.html)
when upstream instructions change.

## 1. Install uv if needed

Serena's current quick start names uv as its only required prerequisite. Use
Astral's official installation instructions:

- Windows PowerShell:

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- macOS/Linux:

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Restart the shell and host (Codex or Claude Code) if the installer updates PATH. Check with
`uv --version` before continuing.

## 2. Install and initialize Serena

Use the current upstream command to install Serena with its managed Python 3.13
runtime:

```sh
uv tool install -p 3.13 serena-agent
serena init
```

If Serena is already installed, keep it unless there is a specific version or
startup error to resolve. Do not clear user or project configuration as a
generic repair step.

## 3. Start Serena through the plugin

The package's `mcp.json` and `.mcp.json` configure a stdio server for Codex with
the following (Claude Code uses the same entry with `--context=claude-code`):

```json
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "serena",
      "args": ["start-mcp-server", "--project-from-cwd", "--context=codex"]
    }
  }
}
```

Do not also run `serena setup codex` or `serena setup claude-code` while this
plugin is installed; those commands add a separate global MCP entry. Start a fresh chat and use `/mcp` to
check the packaged connection. The host app may not launch in the project
directory, so activate the intended project with Serena before doing project
work.

## 4. Resolve command discovery

If the shell can find Serena but the host reports that the command is missing:

1. Check the executable directory with `uv tool dir --bin`.
2. Restart the host from a shell that has the uv tool directory on PATH.
3. If the host still cannot resolve `serena`, set the MCP command to the full
   executable path in the host-supported plugin configuration and retain the
   packaged arguments.

Do not edit the plugin cache. If the executable does not exist, rerun the
upstream install command and inspect its actual error.

## Local access and scope

Serena runs as a child process of the local MCP client and can read or edit
files available to that process. Project activation does not grant additional
authorization. Preserve the user's scope, review edits, and use project checks
only when the task permits them. Serena may require extra language-specific
dependencies beyond uv; consult its [language support guide](https://oraios.github.io/serena/01-about/020_programming-languages.html).
