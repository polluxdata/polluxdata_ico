#!/usr/bin/env python3
"""Valida el repo de skills PolluxData (estructura, frontmatter, referencias, demo flag).

Uso: validate.py [raiz-del-repo]
"""
import ast
import json
import re
import sys
from pathlib import Path


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = []

    for skill in ("pollux-brand", "pollux-docs"):
        md = root / "skills" / skill / "SKILL.md"
        if not md.exists():
            errors.append(f"skills/{skill}/SKILL.md no existe")
            continue
        text = md.read_text()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{skill}: SKILL.md sin frontmatter YAML")
        else:
            fm = m.group(1)
            if not re.search(r"^name:\s*\S+", fm, re.M):
                errors.append(f"{skill}: frontmatter sin 'name'")
            if not re.search(r"^description:\s*\S+", fm, re.M):
                errors.append(f"{skill}: frontmatter sin 'description'")

    palette = root / "skills" / "pollux-brand" / "assets" / "palette.json"
    try:
        json.loads(palette.read_text())
    except Exception as e:
        errors.append(f"palette.json inválido: {e}")

    docs = root / "skills" / "pollux-docs"
    skill_text = (docs / "SKILL.md").read_text() if (docs / "SKILL.md").exists() else ""
    refs = sorted(p.name for p in (docs / "references").glob("*.md")
                  if not p.name.startswith("sample-"))
    for r in refs:
        if r not in skill_text:
            errors.append(f"reference '{r}' no listada en pollux-docs/SKILL.md")
    for sample in sorted((docs / "references").glob("sample-*.json")):
        try:
            d = json.loads(sample.read_text())
        except Exception as e:
            errors.append(f"{sample.name} inválido: {e}")
            continue
        if not d.get("demo"):
            errors.append(f"{sample.name} sin 'demo': true (obligatorio en muestras)")
    if "demo" not in skill_text.lower():
        errors.append("pollux-docs/SKILL.md no documenta el modo demo")

    scripts = docs / "scripts"
    for py in sorted(scripts.glob("*.py")):
        try:
            ast.parse(py.read_text())
        except SyntaxError as e:
            errors.append(f"{py.name}: error de sintaxis ({e})")

    idx = root / ".well-known" / "skills" / "index.json"
    try:
        data = json.loads(idx.read_text())
        for s in data.get("skills", []):
            if not (root / s["path"] / "SKILL.md").exists():
                errors.append(f"well-known apunta a ruta inexistente: {s['path']}")
    except Exception as e:
        errors.append(f"well-known index.json inválido: {e}")

    if errors:
        print("FALLOS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK: repo válido ({len(refs)} referencias, "
          f"{len(list(scripts.glob('*.py')))} scripts)")


if __name__ == "__main__":
    main()
