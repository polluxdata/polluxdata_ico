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
# marketplace de plugin (requiere Claude Code 2.x)
/plugin marketplace add polluxdata/polluxdata_ico
```

## Uso con Hermes Agent

```bash
# descubrimiento público
hermes skills tap add polluxdata/polluxdata_ico
# instalación (también por URL directa de SKILL.md)
hermes skills install polluxdata/polluxdata_ico/pollux-brand
hermes skills install polluxdata/polluxdata_ico/pollux-docs
```

Verificado end-to-end (2026-09-07): sesión real de Hermes carga `pollux-brand` y responde con los tokens correctos. Descubrimiento estándar también disponible en `https://polluxdata.com/.well-known/skills/index.json`.

## Ejemplo de flujo

> "Genera una oferta para Acme Corp: migración a OCI, 2 fases, 12.400 € + IVA, válida 30 días."

El agente carga `pollux-docs` (estructura de oferta) + `pollux-brand` (estilo Paper mode) y produce un PDF coherente con la marca, sin que nadie toque una plantilla.

## Estado del proyecto

Ver `ROADMAP.md` para el detalle completo. Resumen: **20/24 tareas cerradas** — 9 documentos generados y auditados, distribuciones verificadas (Claude Code, Hermes, web), vectores oficiales de marca. Abiertas: 2 generaciones de imágenes de mascota, decisión de color en portadas partner, MSA opcional.

## Muestras

La carpeta `muestras/` contiene PDFs/PPTX de demostración con datos 100% ficticios (marcados "MUESTRA · DATOS FICTICIOS"). Ver `muestras/README.md`. Los documentos reales no llevan la marca.

## Integración con la web

`HANDOFF-WEB.md` documenta el traspaso ejecutado al sitio (well-known, logo SVG, auditoría de color). La web consume los assets de este repo — no los duplica.

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

- Cambios de marca → edita solo `skills/pollux-brand/SKILL.md` + `palette.json` y registra en `skills/pollux-brand/CHANGELOG.md`
- Nueva plantilla de documento → añade `skills/pollux-docs/references/<tipo>.md`, listala en el SKILL.md y añádela al ROADMAP
- Assets nuevos de la mascota → `skills/pollux-brand/assets/mascot/` con nombres descriptivos
- Validar el repo tras cambios: `python3 scripts/validate.py` (también corre en CI)
