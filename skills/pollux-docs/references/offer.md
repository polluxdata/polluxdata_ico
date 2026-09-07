# Offer / Proposal — structure and rules

Output: **PDF (preferred) or DOCX, Paper mode** (see `pollux-brand` skill).

## Required inputs

- Client: company, contact name, email
- Project title and brief description of need
- Scope: services/deliverables, explicitly in-scope and out-of-scope
- Pricing: line items with unit prices, currency, taxes (IVA %)
- Timeline: start date, phases, estimated duration
- Validity of the offer (default: 30 days from issue)
- Payment terms (default: to confirm with user)

## Document structure

```
[COVER — Paper mode]
  Navy band (#06111F) top: logo pollux-logo.png (white area) + offer number
  Title: {{project_title}}
  Subtitle: Propuesta comercial
  Client: {{client_company}} — {{client_contact}}
  Date: {{issue_date}} · Ref: OF-{{YYYY}}-{{seq}}
  Optional: small Pollux mascot banner (assets/mascot/), never covering text
  Partner logos ONLY if partner is part of the solution (Oracle/AWS/Azure)

[1. Resumen ejecutivo]
  3-5 sentences: client need, proposed solution, expected outcome.
  Tone: informal-ganadora — direct and confident, no filler.

[2. Contexto y objetivo]
  Restate the client's situation and the objective of the project.
  1 short paragraph + bullet list of goals.

[3. Alcance]
  In-scope (bullets, concrete deliverables)
  Out-of-scope (bullets — protects both sides, always include)

[4. Metodología y plan de trabajo]
  Phases with duration table:
  | Fase | Entregable | Duración estimada |

[5. Inversión]
  Pricing table (mono font for numbers):
  | # | Concepto | Unidad | Cant. | P. unitario | Total |
  Subtotal / IVA {{tax}}% / TOTAL (orange accent on total)
  Currency stated once, next to the first price.
  Payment terms paragraph.

[6. Condiciones]
  - Validez de la oferta: {{validity_days}} días desde {{issue_date}}
  - Condiciones de pago: {{payment_terms}}
  - Soporte y garantía: {{warranty_terms}}
  - Confidencialidad: esta propuesta es confidencial para el destinatario

[CLOSING — navy band]
  Logo + "La estrella que nos guía." + contact:
  {{sender_name}} · {{sender_email}} · polluxdata.com
```

## Style rules (from pollux-brand)

- Headings: Manrope bold, `#06111F`; accent rules/marks: orange `#F07A1F`
- Body: Inter 10.5–11 pt, `#5B6573`; section bands `#F6F7FB`
- Numbers/prices: mono font
- Mascot: cover only, small; NEVER in sections 3–6
- No partner colors unless partner logos present

## Variables

{{project_title}}, {{client_company}}, {{client_contact}}, {{issue_date}}, {{YYYY}}, {{seq}},
{{tax}}, {{validity_days}}, {{payment_terms}}, {{warranty_terms}}, {{sender_name}}, {{sender_email}}

## Verification checklist

- [ ] Totals sum correctly (subtotal + IVA = total)
- [ ] Validity date = issue date + validity_days
- [ ] No {{placeholders}} remain
- [ ] Partner logos match actual proposed solution
- [ ] Out-of-scope section present
- [ ] Tone: confident, direct, no corporate filler
