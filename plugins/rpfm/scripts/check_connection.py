"""Read-only RPFM MCP probe using Python's standard library."""
import argparse
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen


def run(endpoint):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    counter = 0

    def request(method, params=None, notification=False):
        nonlocal counter
        counter += 1
        payload = {'jsonrpc': '2.0', 'method': method}
        if not notification:
            payload['id'] = counter
        if params is not None:
            payload['params'] = params
        req = Request(endpoint, data=json.dumps(payload).encode(), headers=headers, method='POST')
        with urlopen(req, timeout=20) as response:
            session = response.headers.get('Mcp-Session-Id')
            if session:
                headers['Mcp-Session-Id'] = session
            body = response.read().decode()
            content_type = response.headers.get('Content-Type', '')
        if notification or not body.strip():
            return None
        if 'text/event-stream' in content_type:
            messages = []
            for block in body.replace('\r\n', '\n').split('\n\n'):
                data = '\n'.join(line[5:].lstrip() for line in block.splitlines() if line.startswith('data:'))
                if data:
                    messages.append(json.loads(data))
            message = next((item for item in messages if item.get('id') == payload['id']), None)
            if message is None:
                raise RuntimeError('No matching MCP response in event stream')
        else:
            message = json.loads(body)
        if 'error' in message:
            raise RuntimeError(json.dumps(message['error']))
        return message['result']

    init = request('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                                  'clientInfo': {'name': 'rpfm-plugin-check', 'version': '0.1.1'}})
    headers['MCP-Protocol-Version'] = init['protocolVersion']
    request('notifications/initialized', notification=True)
    tools = []
    cursor = None
    while True:
        page = request('tools/list', {'cursor': cursor} if cursor else {})
        tools.extend(page.get('tools', []))
        cursor = page.get('nextCursor')
        if not cursor:
            break
    names = {tool['name'] for tool in tools}
    checks = {}
    for name in ('get_game_selected', 'list_open_packs'):
        if name not in names:
            raise RuntimeError(f'Required tool missing: {name}')
        result = request('tools/call', {'name': name, 'arguments': {}})
        if result.get('isError'):
            raise RuntimeError(f'{name} returned an MCP tool error: {result}')
        checks[name] = result
    print(json.dumps({'endpoint': endpoint, 'server': init.get('serverInfo'),
                      'protocol': init['protocolVersion'], 'tool_count': len(tools),
                      'read_only_checks': checks}, indent=2))


if __name__ == '__main__':
    config = Path(__file__).resolve().parents[1] / 'mcp.json'
    default = json.loads(config.read_text(encoding='utf-8'))['mcpServers']['rpfm-tools']['url']
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default=default)
    args = parser.parse_args()
    try:
        run(args.url)
    except Exception as error:
        print(f'Connection check failed: {error}', file=sys.stderr)
        sys.exit(1)

