# Install and register RPFM Server

This plugin registers the MCP connection through its packaged `mcp.json`.
RPFM is installed separately on each recipient's computer. No API key is required
for the default loopback endpoint. No server binary is bundled in this plugin.

## 1. Check for an existing installation

Reuse an existing compatible RPFM installation. Check whether the server is
already listening before starting another process:

```powershell
Get-NetTCPConnection -LocalPort 45127 -State Listen -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process -Filter "name='rpfm_server.exe'" |
    Select-Object ProcessId, ExecutablePath
```

An open port alone does not prove it is RPFM. Verify with the packaged MCP
checker or actual RPFM tool calls. Do not kill a server owned by another client.

## 2. Install on Windows x64 when RPFM is missing

Upstream release metadata checked on 2026-10-12 identifies v5.1.1 as the latest
stable release. Its Windows ZIP is 293,600,799 bytes (about 280 MiB); extraction
needs additional space. This procedure pins that version and verifies the
SHA-256 digest published by GitHub. It installs into a new versioned directory
without administrator rights and refuses to overwrite an existing directory.

Copy this entire block into PowerShell on Windows x64:

```powershell
$ErrorActionPreference = 'Stop'
$rpfmVersion = 'v5.1.1'
$rpfmAsset = 'rpfm-v5.1.1-x86_64-pc-windows-msvc.zip'
$rpfmUrl = "https://github.com/Frodo45127/rpfm/releases/download/$rpfmVersion/$rpfmAsset"
$rpfmExpectedHash = '3dea798c4feff7630956590786e4e429eb3fc8a322756e6d41742709a139a8bf'
$rpfmInstallDir = Join-Path $env:LOCALAPPDATA "Programs\RPFM\$rpfmVersion"
$rpfmDownloadDir = Join-Path $env:TEMP ('rpfm-download-' + [guid]::NewGuid().ToString('N'))
$rpfmZip = Join-Path $rpfmDownloadDir $rpfmAsset

if (Test-Path -LiteralPath $rpfmInstallDir) {
    throw "Already exists: $rpfmInstallDir. Reuse it or choose a new installation directory."
}
New-Item -ItemType Directory -Path $rpfmDownloadDir | Out-Null
Write-Host "Downloading about 280 MiB from the official RPFM release."
Invoke-WebRequest -Uri $rpfmUrl -OutFile $rpfmZip
$rpfmActualHash = (Get-FileHash -LiteralPath $rpfmZip -Algorithm SHA256).Hash
if ($rpfmActualHash -ne $rpfmExpectedHash) {
    throw "Checksum mismatch. Archive retained at $rpfmZip; do not extract or run it."
}
New-Item -ItemType Directory -Path $rpfmInstallDir -Force | Out-Null
Expand-Archive -LiteralPath $rpfmZip -DestinationPath $rpfmInstallDir
$rpfmServers = @(Get-ChildItem -LiteralPath $rpfmInstallDir -Filter 'rpfm_server.exe' -File -Recurse)
if ($rpfmServers.Count -ne 1) {
    throw "Expected one rpfm_server.exe, found $($rpfmServers.Count). Inspect $rpfmInstallDir."
}
Write-Host "Verified installation: $rpfmInstallDir"
Write-Host "Server executable: $($rpfmServers[0].FullName)"
Write-Host "Download retained at: $rpfmZip"
```

Keep the complete extracted release together so required runtime files remain
beside the executables. If download or extraction fails, diagnose that error;
do not reset an existing RPFM installation or its settings. For a newer version,
obtain its actual asset URL and published digest from the official release
metadata and update the whole procedure consistently.

Official downloads: https://github.com/Frodo45127/rpfm/releases
Pinned release: https://github.com/Frodo45127/rpfm/releases/tag/v5.1.1
Release metadata: https://api.github.com/repos/Frodo45127/rpfm/releases/latest

## 3. Start the server

The easiest option is to start `rpfm_ui.exe` from the extracted release and
keep it open. Upstream documents that the GUI starts and owns the server.

For a standalone server from the installation above, use this complete block:

```powershell
$ErrorActionPreference = 'Stop'
$rpfmInstallDir = Join-Path $env:LOCALAPPDATA 'Programs\RPFM\v5.1.1'
$rpfmListener = Get-NetTCPConnection -LocalPort 45127 -State Listen -ErrorAction SilentlyContinue
if ($rpfmListener) {
    Write-Host 'Port 45127 already has a listener. Verify that endpoint before starting another server.'
} else {
    $rpfmServers = @(Get-ChildItem -LiteralPath $rpfmInstallDir -Filter 'rpfm_server.exe' -File -Recurse)
    if ($rpfmServers.Count -ne 1) {
        throw "Expected one rpfm_server.exe under $rpfmInstallDir."
    }
    $rpfmServerExe = $rpfmServers[0].FullName
    $rpfmProcess = Start-Process -FilePath $rpfmServerExe -WorkingDirectory (Split-Path -Parent $rpfmServerExe) -WindowStyle Hidden -PassThru
    Write-Host "Started RPFM Server with process ID $($rpfmProcess.Id). Verify MCP connectivity next."
}
```

For an existing installation, substitute its verified installation directory.
The plugin does not create a Windows service, scheduled task, or login startup.
If the process exits or the endpoint is unavailable, run the executable in a
terminal to inspect stderr and check the upstream lifecycle documentation.
Do not assume it stays running indefinitely without clients.

## 4. Register through the plugin

Install this version from the public Git marketplace.
Its `mcp.json` and compatibility `.mcp.json` already register the endpoint
below. Claude Code reads the same endpoint from `.claude-plugin/plugin.json`
using its `"type": "http"` spelling for Streamable HTTP:

```json
{
  "mcpServers": {
    "rpfm-tools": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:45127/mcp"
    }
  }
}
```

Start a fresh chat after installation; restart Codex or Claude Code if the
tools do not load. In Claude Code, `/mcp` can reconnect after the server starts.
Ask: "Set up RPFM and verify its server connection." The setup skill should
first try `get_game_selected` and `list_open_packs` without changing real packs.

### Alternative: register only the server directly

When using Codex without the plugin, the verified CLI syntax is:

```powershell
codex mcp add rpfm --url http://127.0.0.1:45127/mcp
codex mcp get rpfm
```

When using Claude Code without the plugin (including the Claude desktop app's
Code tab, which does not load CLI Git-marketplace plugins), register the
bundled stdio bridge rather than the raw HTTP endpoint. Current Claude Code
rejects RPFM 5.1.1's raw tool list because it omits `ttlMs`/`cacheScope`:

```powershell
claude mcp add -s user rpfm-tools -- python -I <plugin-dir>/scripts/rpfm_stdio_bridge.py
claude mcp get rpfm-tools
```

Copy the plugin's skills to `~/.claude/skills/rpfm` and
`~/.claude/skills/rpfm-setup` (with `name: rpfm-setup`) for slash-command access.

Check `codex mcp list` or `claude mcp list` first and preserve existing registrations. This alternative
does not install RPFM or launch its server. Do not add it alongside the plugin
unless a second independent connection is intended. For another client, use
that client's Streamable HTTP registration flow with the same local endpoint.
The server's WebSocket `/ws` address is not the MCP endpoint.

## 5. Verify

From the plugin directory, with Python 3.10+ available:

```powershell
python ./scripts/check_connection.py
```

The checker initializes MCP, lists tools, and calls only `get_game_selected`
and `list_open_packs`. Successful direct checks prove server connectivity;
successful calls through the host prove the host loaded the plugin connection.
Check application errors in tool text content too. Tool counts can vary by
upstream build; 155 were observed during package preparation.

## Linux x86_64

The pinned official v5.1.1 archive is 266,059,240 bytes (about 254 MiB), with
additional extraction space needed. Use the following complete Bash procedure
on a compatible Linux x86_64 system with curl, sha256sum, GNU tar, and zstd.
Install missing prerequisites through the distribution's supported package
manager. Do not run the Windows commands on Linux.

```bash
set -euo pipefail
rpfmVersion='v5.1.1'
rpfmAsset='rpfm-v5.1.1-x86_64-unknown-linux-gnu.tar.zst'
rpfmUrl="https://github.com/Frodo45127/rpfm/releases/download/$rpfmVersion/$rpfmAsset"
rpfmHash='3b260ac552ba43c3485bd23f90a1ebe1559e2d01c716f687aafeaa69829dfe15'
rpfmInstall="${XDG_DATA_HOME:-$HOME/.local/share}/rpfm/$rpfmVersion"
for rpfmRequired in curl sha256sum tar zstd find; do
    command -v "$rpfmRequired" >/dev/null || { echo "Missing: $rpfmRequired" >&2; exit 1; }
done
if [[ -e "$rpfmInstall" || -L "$rpfmInstall" ]]; then
    echo "Already exists: $rpfmInstall. Reuse it or choose a new directory." >&2
    exit 1
fi
rpfmDownload=$(mktemp -d -t rpfm-download-XXXXXXXX)
rpfmArchive="$rpfmDownload/$rpfmAsset"
curl --fail --location --retry 3 "$rpfmUrl" --output "$rpfmArchive"
printf '%s  %s\n' "$rpfmHash" "$rpfmArchive" | sha256sum --check --status
mkdir -p "$rpfmInstall"
tar --zstd -xf "$rpfmArchive" -C "$rpfmInstall"
mapfile -t rpfmServers < <(find "$rpfmInstall" -type f -name rpfm_server)
if [[ ${#rpfmServers[@]} -ne 1 ]]; then
    echo "Expected one rpfm_server; inspect $rpfmInstall" >&2
    exit 1
fi
printf 'Verified installation: %s\nServer executable: %s\nArchive retained: %s\n' \
    "$rpfmInstall" "${rpfmServers[0]}" "$rpfmArchive"
```

Check for an existing listener/server first using the platform's process/socket
tools. Launch the verified executable from its own directory, or start the GUI
that owns it. Keep the extracted release together. Inspect missing-library errors
instead of copying only the binary or installing every GUI build dependency.
The default endpoint and Codex/Claude Code registration commands match Windows. Verify MCP
readiness; a launched PID alone is insufficient.

Upstream also documents AUR/Flatpak distribution. Flatpak filesystem permissions
can restrict game access; use the documented Copy Command/Flatseal workflow for
the intended game folders rather than granting unrestricted access blindly.
The server's actual presence/location in any alternate package must be verified.
There is no maintained macOS release in the reviewed installation chapter;
do not promise the Windows/Linux packages will work there.

For source builds read the selected revision's Cargo targets and
[build instructions](https://frodo45127.github.io/rpfm/manual/building.html).
GUI Qt/KDE requirements are not automatically requirements for using a released
headless server. Do not run a blanket workspace build as the default installer.
Fresh-machine Windows extraction and Linux installation have not been executed
during preparation; these are documented procedures, not tested platform claims.

## 6. Configure the intended game

Once connected, read [game configuration](../../rpfm/references/game-configuration.md).
Verify selected game, game-install path, schema, vanilla cache, and optional AK
data. Initialize the session's selected game with the live rebuild option;
acquire missing schemas when authorized and verify actual loaded definitions.
Connectivity alone does not prove editing/diagnostics readiness. Preserve
unrelated settings and distinguish missing environment coverage from mod errors.

## Sessions, scope, and removal

Each MCP connection has separate open packs and dependency state, including
separation from the GUI. Sessions may expire after five minutes of inactivity;
save authorized edits promptly and recover context after reconnecting.
Loopback is local to the client machine; uploading the plugin does not make
local files accessible to a hosted client. Keep the default local binding.

Removing the plugin removes its connection, not RPFM or its settings. Stop only
a server process you intentionally started and no longer need. Preserve RPFM
configuration and backups when removing a downloaded installation.

Upstream server reference: https://frodo45127.github.io/rpfm/manual/server/overview.html
Upstream MCP reference: https://frodo45127.github.io/rpfm/manual/server/mcp.html
