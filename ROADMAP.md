# Roadmap — PolluxData Brand Skills

Tareas futuras del sistema de marca y plantillas. Si un agente mantiene este repo, empieza por aquí.

## 1. Plantillas de documentos (pollux-docs)

Lista de documentos que PolluxData debe tener como plantilla, por prioridad:

| Estado | Documento | Reference | Formato | Notas |
|---|---|---|---|---|
| ✅ Hecha | Oferta / propuesta | `references/offer.md` | PDF / DOCX | Estructura completa, modo Paper |
| ✅ Hecha | Proforma | `references/proforma.md` | PDF | Transaccional 1 página, banda compacta, sin prosa comercial |
| ✅ Hecha | Presentación comercial | `references/presentation.md` | PPTX | 8 slides: portada dark con mascota, interior Paper mode, cierre CTA |
| ✅ Hecha | Ficha de servicio (one-pager) | `references/service-sheet.md` | PDF | Transaccional 1 página, banda compacta 56mm, precio "Desde USD" |
| ✅ Hecha | Informe de assessment | `references/assessment.md` | PDF | Hallazgos con severidad (alta en naranja), roadmap y recomendaciones |
| ✅ Hecha | Propuesta de soporte mensual | `references/support-plan.md` | PDF | PolluxData Care: SLA, alcance, tarifa mensual, firmas |
| ✅ Hecha | Caso de éxito | `references/case-study.md` | PDF / PPTX | Métricas hero naranjas, tabla antes/después, cita de cliente — 1 página |
| ✅ Hecha | Informe de cierre de proyecto | `references/project-closure.md` | PDF | Entregables con ✓, accesos sin credenciales, acta de aceptación |
| ✅ Hecha | Email de seguimiento comercial | `references/followup-email.md` | Texto | Plantilla .txt con make_email.py, CTA con dos opciones |
| ⬜ Opcional | Acuerdo marco de servicios (MSA) | `references/msa.md` | DOCX | Legal — revisar con asesor antes de automatizar |

## 2. Infraestructura del repo

- [ ] Generadores reales en `skills/pollux-docs/scripts/`: `make_offer.py`, `make_proforma.py` (DOCX→PDF con tokens de marca vía `palette.py`)
- [ ] Incluir fuentes en `skills/pollux-brand/assets/fonts/` (Manrope, Inter — verificar licencia OFL para redistribución)
- [ ] Crear versiones SVG del logo (wordmark e isotipo) — ahora solo hay PNG pequeños
- [ ] Validación CI: lint de SKILL.md (frontmatter válido), JSON schemas, chequeo de que toda reference nueva está listada en el `SKILL.md` y en este roadmap
- [ ] Ampliar catálogo de la mascota: poses catalogadas con nombre (`pollux-thumbs-up`, `pollux-pointing`, `pollux-thinking`) y regla de uso de cada una
- [ ] Decidir política de color en portadas con mascota: aceptar el rojo de la escena partner (Oracle) como acento justificado o regenerar escena en navy/naranja
- [ ] Fuentes corregidas y sincronizadas; si se cambian, re-ejecutar el fix de name tables (Manrope-ExtraLight bug del instancer) y re-instalar en LibreOffice (`Resources/fonts/truetype`)
- [ ] Asset de mascota "modo Paper": variante con fondo navy `#06111F` o transparente, sin escena de partner (los assets actuales llevan la escena roja/neón incrustada, no apta para bandas de documentos) — pendiente de generar
- [ ] Logo en alta resolución: isotipo SVG ✅ (medido del favicon, `pollux-star.svg`); **falta el wordmark vectorial original** — pedirlo al diseñador/fuente original (la reconstrucción con Michroma se descartó por infiel)
- [ ] Color del isotipo corregido a `#D04503` (medido por píxel) — revisar usos web actuales que usen `#F05A24`
- [ ] Versionado de marca: `CHANGELOG.md` en `pollux-brand` — cualquier cambio de token pasa por ahí

## 3. Distribución

- [ ] Servir descubrimiento estándar en `https://polluxdata.com/.well-known/skills/index.json` (copiar a `public/.well-known/skills/` en el repo de la web Astro y desplegar)
- [ ] Registrar el repo como marketplace de plugin de Claude Code (`.claude-plugin/marketplace.json`)
- [ ] Dar de alta el tap en Hermes: verificar `hermes skills tap add polluxdata/polluxdata_ico` end-to-end
- [ ] Opcional: alta en skills.sh para descubrimiento público

## 4. Prueba de fuego

- [ ] Generar una oferta real de prueba con un agente cargando los dos skills y validar: totales, fechas, tono, sin placeholders
- [ ] Generar una presentación de prueba y contrastar con las escenas oficiales de `assets/mascot/`
- [ ] Revisión visual de la familia de documentos: ¿se reconoce como una sola marca a primera vista?
