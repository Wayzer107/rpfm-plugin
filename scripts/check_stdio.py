"""Probe a plugin's configured stdio MCP server and optionally call its tools.

Requires Python 3.10+. Always choose a workspace explicitly with --cwd.
Calls are opt-in: use only harmless tools or a disposable fixture for checks.
"""

import argparse
import asyncio
import json
import os
import signal
import sys
import tempfile
from pathlib import Path


async def probe(args):
    config = json.loads((args.plugin / "mcp.json").read_text(encoding="utf-8"))
    servers = config["mcpServers"]
    name = args.server or (next(iter(servers)) if len(servers) == 1 else None)
    if name is None:
        raise ValueError("Choose --server when a plugin has more than one MCP server")
    server = servers[name]
    if server["type"] != "stdio":
        raise ValueError("This checker supports stdio servers only")
    command = [server["command"], *server.get("args", [])]
    environment = dict(os.environ, **server.get("env", {}))
    calls = [json.loads(call) for call in args.call]
    with tempfile.TemporaryFile() as stderr:
        process = await asyncio.create_subprocess_exec(
            *command, cwd=args.cwd, env=environment,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=stderr, start_new_session=os.name == "posix",
        )
        counter = 0

        async def send(payload):
            process.stdin.write((json.dumps(payload) + "\n").encode())
            await process.stdin.drain()

        async def request(method, params=None):
            nonlocal counter
            counter += 1
            payload = {"jsonrpc": "2.0", "id": counter, "method": method}
            if params is not None:
                payload["params"] = params
            await send(payload)
            while True:
                line = await process.stdout.readline()
                if not line:
                    raise RuntimeError("MCP server exited before responding")
                message = json.loads(line)
                if "method" in message:
                    if "id" in message:
                        reply = {"jsonrpc": "2.0", "id": message["id"]}
                        if message["method"] == "ping":
                            reply["result"] = {}
                        elif message["method"] == "roots/list":
                            reply["result"] = {"roots": [{"uri": args.cwd.as_uri(), "name": args.cwd.name}]}
                        else:
                            reply["error"] = {"code": -32601, "message": "Method not supported by probe"}
                        await send(reply)
                    continue
                if message.get("id") != payload["id"]:
                    raise RuntimeError("Unexpected MCP response ID")
                if "error" in message:
                    raise RuntimeError(json.dumps(message["error"]))
                return message["result"]

        async def timed_request(method, params=None):
            return await asyncio.wait_for(request(method, params), timeout=args.timeout)

        try:
            initialization = await timed_request("initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {"roots": {}},
                "clientInfo": {"name": "plugin-stdio-check", "version": "0.1.0"},
            })
            await send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            tools = []
            cursor = None
            while True:
                page = await timed_request("tools/list", {"cursor": cursor} if cursor else {})
                tools.extend(page.get("tools", []))
                cursor = page.get("nextCursor")
                if not cursor:
                    break
            if not tools:
                raise RuntimeError("Server returned no MCP tools")
            names = {tool["name"] for tool in tools}
            results = []
            for call in calls:
                if call["name"] not in names:
                    raise RuntimeError(f"Requested tool not discovered: {call['name']}")
                attempts = args.diagnostic_attempts if call["name"] in (
                    "rust_analyzer_diagnostics", "rust_analyzer_workspace_diagnostics"
                ) else 1
                for attempt in range(attempts):
                    result = await timed_request("tools/call", call)
                    if result.get("isError"):
                        raise RuntimeError(f"{call['name']} returned a tool error: {result}")
                    incomplete = False
                    for item in result.get("content", []):
                        try:
                            content = json.loads(item.get("text", ""))
                        except json.JSONDecodeError:
                            continue
                        if isinstance(content, dict) and "may be incomplete" in content.get("note", ""):
                            incomplete = True
                    if not incomplete or args.diagnostic_attempts == 1:
                        break
                    if attempt + 1 == attempts:
                        raise RuntimeError(f"{call['name']} remained incomplete after {attempts} attempts")
                    print(f"{call['name']} is still loading/checking; retrying ({attempt + 2}/{attempts})", file=sys.stderr)
                    await asyncio.sleep(1)
                results.append({"name": call["name"], "result": result})
            return {"server": initialization.get("serverInfo"),
                    "protocol": initialization["protocolVersion"],
                    "tool_count": len(tools), "tools": sorted(names), "calls": results}
        except Exception:
            stderr.seek(0)
            tail = stderr.read().decode(errors="replace")[-6000:]
            if tail:
                print(tail, file=sys.stderr)
            raise
        finally:
            if process.stdin:
                process.stdin.close()
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            elif process.returncode is None:
                process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                if os.name == "posix":
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
                await process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin", type=Path, help="Plugin source directory")
    parser.add_argument("--server", help="MCP server name from the plugin configuration")
    parser.add_argument("--cwd", type=Path, required=True, help="Workspace to launch the server in")
    parser.add_argument("--call", action="append", default=[], help="JSON object with name and arguments")
    parser.add_argument("--timeout", type=float, default=120, help="Timeout for each MCP request in seconds")
    parser.add_argument("--diagnostic-attempts", type=int, default=1,
                        help="Maximum attempts for Rust diagnostics reporting incomplete checks (default: 1)")
    args = parser.parse_args()
    if args.diagnostic_attempts < 1:
        parser.error("--diagnostic-attempts must be positive")
    args.plugin = args.plugin.resolve()
    args.cwd = args.cwd.resolve()
    try:
        print(json.dumps(asyncio.run(probe(args)), indent=2))
    except Exception as error:
        print(f"Connection check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
