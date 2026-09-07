# Proforma — structure and rules

Output: **PDF, Paper mode** (see `pollux-brand` skill).

A proforma is a **transactional quotation**: numbered lines of products/services with prices. Unlike the offer, it has no commercial narrative — minimal prose, straight to the numbers. Ref format: `PF-YYYY-NNN`.

## Required inputs

- Client: company, contact name, role
- Line items: description, unit, quantity, unit price, currency
- Tax rate (default: 15%)
- Validity (default: 15 days — shorter than an offer)
- Payment terms and delivery time
- Payment details (optional — bank/account reference)

## Document structure

```
[COVER BAND — compact (46mm), Paper mode]
  Navy band: logo top-left · Ref PF-YYYY-NNN + date right
  Kicker orange spaced: "PROFORMA"
  Client: "Preparada para {{client_company}}" + contact line
  Right: isotype star (orange, subtle)

[01 — DETALLE]
  Lines table: | # | Descripción | Unidad | Cant. | P. unit. (USD) | Total (USD) |
  Note: "Esta proforma no constituye factura. Los consumos de nube se facturan aparte según uso."
  Totals block right: Subtotal / IVA / TOTAL (orange)

[02 — CONDICIONES]
  - Validez: {{validity_days}} días desde {{date}}
  - Forma de pago: {{payment_terms_detail}}
  - Tiempo de entrega: {{delivery_time}}
  - Datos de pago: {{payment_details}} (optional)

[03 — ACEPTACIÓN]
  Short paragraph: to accept, sign and return to {{sender_email}}
  Single signature line: Nombre · Firma · Fecha
```

## Style rules (from pollux-brand)

- Same tokens as the offer: navy bands, orange accents, Manrope/Inter, zebra tables
- Mascot: never (transactional document)
- Numbers right-aligned; currency stated once in column headers
- No commercial prose, no executive summary

## Variables

{{client_company}}, {{client_contact}}, {{client_role}}, {{date}}, {{ref}},
{{tax_rate}}, {{validity_days}}, {{payment_terms_detail}}, {{delivery_time}},
{{payment_details}}, {{sender_email}}

## Verification checklist

- [ ] Line totals = qty × unit price; subtotal/IVA/total sum correctly
- [ ] Validity date = issue date + validity_days
- [ ] No {{placeholders}} remain
- [ ] Ref format PF-YYYY-NNN
- [ ] No mascot, no partner logos unless partner is in the lines
- [ ] Prose minimal — it must read like a quotation, not an offer
