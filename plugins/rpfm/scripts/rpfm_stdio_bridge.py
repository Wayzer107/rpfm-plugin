"""Stdio bridge from Claude Code to the local RPFM Streamable HTTP server.

RPFM Server 5.1.1 (rmcp 3.1.0) answers the stateless `server/discover` probe,
so current Claude Code builds validate its list results against that newer MCP
revision. RPFM's tools/prompts/resources results omit the `ttlMs`/`cacheScope`
fields that revision requires, and Claude Code rejects the whole tool list
("Connected - tools fetch failed"). This bridge:

  * refuses `server/discover`, so the client negotiates through `initialize`;
  * adds `ttlMs: 0, cacheScope: "private"` to list/read results lacking them;
  * starts a verified local rpfm_server hidden when nothing is listening.

Standard library only (Python 3.10+). Everything else is forwarded unchanged.
Environment overrides: RPFM_MCP_URL, RPFM_SERVER_EXE.
"""
import glob
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = os.environ.get("RPFM_MCP_URL", "http://127.0.0.1:45127/mcp")
CACHE_RESULT_KEYS = ("tools", "prompts", "resources", "resourceTemplates", "contents")

session_id = None
protocol_version = None
out_lock = threading.Lock()


def log(message):
    sys.stderr.write("rpfm-bridge: %s\n" % message)
    sys.stderr.flush()


def emit(message):
    data = json.dumps(message, separators=(",", ":"))
    with out_lock:
        sys.stdout.write(data + "\n")
        sys.stdout.flush()


def endpoint_address():
    parts = urllib.parse.urlsplit(ENDPOINT)
    return parts.hostname or "127.0.0.1", parts.port or 80


def listening():
    try:
        with socket.create_connection(endpoint_address(), timeout=0.5):
            return True
    except OSError:
        return False


def server_executable():
    explicit = os.environ.get("RPFM_SERVER_EXE")
    if explicit:
        return explicit
    if os.name == "nt":
        pattern = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "RPFM", "*", "rpfm_server.exe")
    else:
        data_home = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        pattern = os.path.join(data_home, "rpfm", "*", "**", "rpfm_server")
    found = sorted(glob.glob(pattern, recursive=True))
    return found[-1] if found else shutil.which("rpfm_server")


def ensure_server():
    """Start the installed server only for a loopback endpoint with no listener."""
    if listening():
        return True
    host = endpoint_address()[0]
    exe = server_executable()
    if host not in ("127.0.0.1", "localhost", "::1") or not exe or not os.path.isfile(exe):
        log("no listener at %s and no local rpfm_server to start" % ENDPOINT)
        return False
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    subprocess.Popen([exe], cwd=os.path.dirname(exe), creationflags=flags,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     close_fds=True, start_new_session=os.name != "nt")
    for _ in range(40):
        time.sleep(0.25)
        if listening():
            log("started %s" % exe)
            return True
    log("rpfm_server did not start listening at %s" % ENDPOINT)
    return False


def patch(message):
    """Fill cache fields required by newer clients when the server omits them."""
    result = message.get("result") if isinstance(message, dict) else None
    if isinstance(result, dict) and any(key in result for key in CACHE_RESULT_KEYS):
        result.setdefault("ttlMs", 0)
        result.setdefault("cacheScope", "private")
    return message


def decode(body, content_type):
    """Return JSON-RPC messages from a JSON or server-sent-events response body."""
    if "text/event-stream" in content_type:
        messages = []
        for line in body.splitlines():
            if line.startswith("data:"):
                payload = line[5:].strip()
                if payload:
                    messages.append(json.loads(payload))
        return messages
    body = body.strip()
    if not body:
        return []
    parsed = json.loads(body)
    return parsed if isinstance(parsed, list) else [parsed]


def post(message):
    global session_id, protocol_version
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    if protocol_version:
        headers["MCP-Protocol-Version"] = protocol_version
    request = urllib.request.Request(ENDPOINT, data=json.dumps(message).encode("utf-8"),
                                     headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            sid = response.headers.get("Mcp-Session-Id")
            if sid:
                session_id = sid
            replies = decode(response.read().decode("utf-8"), response.headers.get("Content-Type", ""))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        try:
            replies = decode(body, error.headers.get("Content-Type", "application/json"))
        except ValueError:
            replies = []
        if not replies and "id" in message:
            replies = [{"jsonrpc": "2.0", "id": message["id"],
                        "error": {"code": -32603, "message": "RPFM HTTP %d: %s" % (error.code, body[:300])}}]
    for reply in replies:
        if message.get("method") == "initialize" and isinstance(reply.get("result"), dict):
            protocol_version = reply["result"].get("protocolVersion")
        emit(patch(reply))


def handle(message):
    method = message.get("method")
    if method == "server/discover":
        emit({"jsonrpc": "2.0", "id": message.get("id"),
              "error": {"code": -32601, "message": "Method not found"}})
        return
    if method == "initialize" and not ensure_server():
        emit({"jsonrpc": "2.0", "id": message.get("id"),
              "error": {"code": -32603, "message": "RPFM Server is not running and could not be started"}})
        return
    try:
        post(message)
    except Exception as error:  # report the failure rather than ending the bridge
        log("request failed: %r" % (error,))
        if "id" in message and method is not None:
            emit({"jsonrpc": "2.0", "id": message["id"],
                  "error": {"code": -32603, "message": "RPFM bridge error: %s" % error}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            log("ignored non-JSON input")
            continue
        for item in message if isinstance(message, list) else [message]:
            if not isinstance(item, dict):
                continue
            if item.get("method") == "tools/call":
                # Long tool calls must not block pings or cancellations.
                threading.Thread(target=handle, args=(item,), daemon=True).start()
            else:
                handle(item)


if __name__ == "__main__":
    main()
