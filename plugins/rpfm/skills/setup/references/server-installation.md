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

Install this plugin using its account listing or the supplied marketplace.
Its `mcp.json` and compatibility `.mcp.json` already register:

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

Start a fresh chat after installation; restart Codex if the tools do not load.
Ask: "Set up RPFM and verify its server connection." The setup skill should
first try `get_game_selected` and `list_open_packs` without changing real packs.

### Alternative: register only the server directly

When using Codex without the plugin, the verified CLI syntax is:

```powershell
codex mcp add rpfm --url http://127.0.0.1:45127/mcp
codex mcp get rpfm
```

Check `codex mcp list` first and preserve existing registrations. This alternative
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

## Linux and other platforms

Use the official release or upstream-supported installation method matching
the recipient's platform. Keep the release files together and locate its actual
`rpfm_server` executable; launch from its installation directory. The endpoint
and plugin registration are the same when the local server uses its defaults.
The Windows installation blocks above do not apply to Linux. This package's
Linux installation and fresh-machine Windows installation have not been tested.

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
