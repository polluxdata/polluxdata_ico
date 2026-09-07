#!/usr/bin/env python3
"""Genera un email de seguimiento comercial PolluxData (.txt).

Uso: make_email.py <email.json> [salida.txt]
"""
import json
import sys
from pathlib import Path

TPL = """Asunto: {subject}

Hola {contact_name}:

{body}

{cta}

Si prefieres, te llamo hoy mismo — dime una hora y te marco.

Un saludo,

{sender_name}
PolluxData · polluxdata.com · {sender_email}
"""


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".txt")
    out.write_text(TPL.format(**data))
    print(out)


if __name__ == "__main__":
    main()
