#!/usr/bin/env python3
"""Print PolluxData brand tokens. Usage: palette.py [--json | --css | --token NAME]"""
import json
import sys
from pathlib import Path

PALETTE = Path(__file__).resolve().parent.parent / "assets" / "palette.json"


def flatten(obj, prefix=""):
    out = {}
    for k, v in obj.items():
        if isinstance(v, dict):
            out.update(flatten(v, f"{prefix}{k}."))
        else:
            out[f"{prefix}{k}"] = v
    return out


def main():
    data = json.loads(PALETTE.read_text())
    tokens = flatten({k: v for k, v in data.items() if k not in ("$schema", "meta")})
    arg = sys.argv[1] if len(sys.argv) > 1 else "--json"
    if arg == "--json":
        print(json.dumps(tokens, indent=2))
    elif arg == "--css":
        print(":root {")
        for k, v in tokens.items():
            print(f"  --{k.replace('_', '-')}: {v};")
        print("}")
    elif arg == "--token":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        print(tokens.get(name, f"UNKNOWN: {name}"))
        sys.exit(0 if name in tokens else 1)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
