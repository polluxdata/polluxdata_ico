# Case Study — structure and rules

Output: **PDF, Paper mode, 1–2 pages**. Client success story with metrics.

Ref format: `CE-YYYY-NNN`.

## Required inputs

- Challenge (client situation, pain-focused)
- Solution (what was done, process-focused)
- 3 hero metrics (value + label)
- Optional detail table (indicador / antes / después)
- Quote + author (real, with permission)
- CTA

## Structure

```
[BAND 64mm] title + "Cliente: X" (NOT "Preparada para")
[01 — EL DESAFÍO]
[02 — LA SOLUCIÓN]
[03 — RESULTADOS]       3 big metrics (S["metric"] style) over orange rule + optional table
[04 — QUÉ DICEN]        quote (bold navy, orange dash) + attribution + CTA line
```

## Rules

- Metrics use the dedicated metric style (24pt with 29pt leading) — never inline size in body style (collision bug)
- Quote + attribution + CTA travel together (KeepTogether) — no orphan CTA page
- Band uses `client_label="Cliente:"`
- Numbers must be real and verifiable — ask the user, never invent

## Verification

- [ ] No orphan page with a single line
- [ ] Metrics legible, labels below numbers
- [ ] Quote attributed with name + role
