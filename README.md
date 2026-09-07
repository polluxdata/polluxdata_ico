# PolluxData Brand Skills

Sistema de marca y documentos comerciales de **PolluxData** en formato [Agent Skills](https://agentskills.io) — compatible con Claude Code, Hermes Agent y otros agentes que soporten el estándar.

La idea: **1 skill de marca + N plantillas de documento**. Un solo diseño, cero derivas.

## Skills

| Skill | Qué hace |
|---|---|
| [`pollux-brand`](skills/pollux-brand/) | Look & feel: colores, tipografía, logo, mascota Pollux, tono de voz, modos visuales |
| [`pollux-docs`](skills/pollux-docs/) | Estructura de documentos comerciales: oferta, proforma, presentación |

## Uso con Claude Code

```bash
# desde este repo (o clonado en cualquier máquina)
/plugin marketplace add <owner>/polluxdata-brand-skills
```

O simplemente menciona los skills en tu sesión si están en `.claude/skills/` o instalados.

## Uso con Hermes Agent

```bash
hermes skills tap add <owner>/polluxdata-brand-skills
hermes skills install <owner>/polluxdata-brand-skills/pollux-brand
hermes skills install <owner>/polluxdata-brand-skills/pollux-docs
```

## Ejemplo de flujo

> "Genera una oferta para Acme Corp: migración a OCI, 2 fases, 12.400 € + IVA, válida 30 días."

El agente carga `pollux-docs` (estructura de oferta) + `pollux-brand` (estilo Paper mode) y produce un PDF coherente con la marca, sin que nadie toque una plantilla.

## Estructura

```
├── .well-known/skills/index.json   # descubrimiento estándar
├── skills/
│   ├── pollux-brand/
│   │   ├── SKILL.md                # reglas de marca (lo que lee el agente)
│   │   ├── assets/
│   │   │   ├── logo/               # wordmark + isotipo estrella
│   │   │   ├── mascot/             # Pollux: escenas oficiales
│   │   │   └── palette.json        # tokens legibles por script
│   │   └── scripts/palette.py      # imprime tokens (--json | --css | --token)
│   └── pollux-docs/
│       ├── SKILL.md
│       └── references/offer.md     # estructura de la oferta
└── brand-assets-raw/               # staging de descargas (no publicar)
```

## Decisión de acentos (normalización)

- **Naranja `#F07A1F`** = color de acción/marca digital (unifica logo y web)
- **`#F05A24`** = solo el isotipo (excepción histórica)
- **Rojo `#C8102E`** = solo la mascota y piezas emocionales
- Colores de partner (Oracle/Azure/AWS) = solo cuando el partner aparece en el artefacto

## Mantenimiento

- Cambios de marca → edita solo `skills/pollux-brand/SKILL.md` + `palette.json`
- Nueva plantilla de documento → añade `skills/pollux-docs/references/<tipo>.md`
- Assets nuevos de la mascota → `skills/pollux-brand/assets/mascot/` con nombres descriptivos
