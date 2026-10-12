# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema>=4.26,<5"]
# ///
"""Validate marketplace plugin/MCP files against their declared official schemas."""

import json
import sys
from pathlib import Path
from urllib.request import urlopen

from jsonschema.validators import validator_for


def main():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    validators = {}
    failed = False
    for entry in catalog["plugins"]:
        package = root / entry["source"]["path"]
        for filename in ("plugin.json", "mcp.json"):
            path = package / filename
            content = json.loads(path.read_text(encoding="utf-8"))
            url = content["$schema"]
            if url not in validators:
                with urlopen(url, timeout=30) as response:
                    schema = json.load(response)
                validator_type = validator_for(schema)
                validator_type.check_schema(schema)
                validators[url] = validator_type(schema)
            errors = list(validators[url].iter_errors(content))
            print(f"{path.relative_to(root)}: {'FAIL' if errors else 'PASS'}")
            for error in errors:
                failed = True
                print(f"  {'.'.join(map(str, error.path)) or '<root>'}: {error.message}")
    return int(failed)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"Schema validation failed: {error}", file=sys.stderr)
        sys.exit(1)
