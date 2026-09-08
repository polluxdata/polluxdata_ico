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

- [x] Generadores reales en `skills/pollux-docs/scripts/`: oferta, proforma, presentación, ficha, assessment, soporte, caso de éxito, cierre y email (comparten `common.py`)
- [x] Fuentes incluidas en `skills/pollux-brand/assets/fonts/` (Manrope, Inter, licencia OFL, name tables corregidas)
- [x] Versiones SVG del logo: wordmark e isotipo oficiales en assets/logo/
- [x] Validación CI: `scripts/validate.py` + GitHub Action (frontmatter, JSONs, references listadas, demo flag, sintaxis)
- [ ] Ampliar catálogo de la mascota: poses catalogadas con nombre (`pollux-thumbs-up`, `pollux-pointing`, `pollux-thinking`) y regla de uso de cada una
- [ ] Decidir política de color en portadas con mascota: aceptar el rojo de la escena partner (Oracle) como acento justificado o regenerar escena en navy/naranja
- [ ] Fuentes corregidas y sincronizadas; si se cambian, re-ejecutar el fix de name tables (Manrope-ExtraLight bug del instancer) y re-instalar en LibreOffice (`Resources/fonts/truetype`)
- [ ] Asset de mascota "modo Paper": variante con fondo navy `#06111F` o transparente, sin escena de partner (los assets actuales llevan la escena roja/neón incrustada, no apta para bandas de documentos) — pendiente de generar
- [x] Logo en alta resolución: isotipo y wordmark vectoriales oficiales (`pollux-star.svg`, `pollux-wordmark.svg`, extraídos del logofinal.svg de MKT/Logos)
- [x] Color del isotipo corregido a `#D45500` — web auditada y migrada por el agente del sitio (verificado desde fuera: 0 usos de `#F05A24`, logo SVG idéntico al repo)
- [x] Versionado de marca: `CHANGELOG.md` en `pollux-brand` — cualquier cambio de token pasa por ahí

## 3. Distribución

- [x] Servir descubrimiento estándar en `https://polluxdata.com/.well-known/skills/index.json` — ejecutado por el agente de la web (HANDOFF-WEB.md), verificado 200/JSON válido
- [x] Marketplace de plugin de Claude Code (`.claude-plugin/marketplace.json` + plugin.json por skill)
- [x] Tap en Hermes verificado end-to-end (2026-09-07): `tap add` OK, instalación por URL OK (ambos skills en ~/.hermes/skills/), sesión real carga el skill y responde con los tokens correctos. Pendiente menor: la indexación del tap por búsqueda requiere un GITHUB_TOKEN válido — el de ~/.hermes/.env está comentado y caducado ("Bad credentials")
- [ ] Opcional: alta en skills.sh para descubrimiento público

## 4. Prueba de fuego

- [x] Oferta de prueba generada y validada (OF-2026-042: totales, fechas, tono, checklist; APTA por visión)
- [x] Presentación de prueba generada (PRES-OF-2026-042, 8 slides, APTA por visión)
- [x] Revisión visual de la familia completa (9 documentos auditados por visión; reconocibles como una sola marca)
