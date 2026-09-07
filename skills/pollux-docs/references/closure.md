# Project Closure Report — structure and rules

Output: **PDF, Paper mode, 1–2 pages**. Handover + acceptance act at project end.

Ref format: `CI-YYYY-NNN` (usually `CI-` + offer number).

## Required inputs

- Project summary rows (proyecto, oferta de referencia, inicio, go-live, estado)
- Deliverables with final status
- Access ownership table (system → client owner) — NO credentials here
- Warranty terms
- Recommendations
- Acceptance wording

## Structure

```
[BAND 64mm] title + client
[01 — RESUMEN DEL PROYECTO]    table (campo / detalle)
[02 — ENTREGABLES]             table with orange ✓ status
[03 — ACCESOS Y RESPONSABLES]  table + security note
[04 — GARANTÍA Y SOPORTE]      bullets (dates, channels, next plan)
[05 — RECOMENDACIONES]         bullets
[06 — ACTA DE ACEPTACIÓN]      paragraph + signature block
```

## Rules

- Never include passwords, tokens or connection strings — reference the secure channel used
- ✓ checks in orange, aligned right
- Warranty end date computed from go-live + 30 days
- Cross-reference the offer ref and the proposed support plan ref

## Verification

- [ ] No credentials in the document
- [ ] Deliverables all closed (no "en curso" in a closure)
- [ ] Acceptance act references what is being accepted
