---
name: pollux-docs
description: Generates PolluxData commercial documents (offers, proposals, proformas, presentations) with a consistent structure and PolluxData brand styling. Use it when asked to create an offer, quote, proforma, proposal or commercial presentation for a client.
license: Proprietary — PolluxData. Internal use only.
metadata:
  tags: [documents, offer, proforma, presentation, commercial]
  related_skills: [pollux-brand]
---

# PolluxData Documents

## Overview

This skill defines the structure of each PolluxData commercial document type. **Always load the `pollux-brand` skill alongside** — it provides colors, typography and mascot rules; this skill provides document structure.

## How to use

1. Load `pollux-brand` for styling (this skill never works alone)
2. Pick the reference for the requested document type from `references/`
3. Collect the required inputs listed in the reference (client, scope, pricing). Ask only for what is missing — never invent prices, dates or legal terms
4. Fill the `{{variables}}` from the reference
5. Apply the correct brand visual mode:
   - Offer / proposal / proforma → **Paper mode** (white, navy bands, orange accents)
   - Presentation → **Dark cinematic** cover + Paper mode interior
6. Verify before delivering: prices sum correctly, dates are coherent (validity = issue date + 30 days by default), no placeholder text remains, tone matches the brand (informal-ganadora, professional clarity)

## Document types

| Type | Reference | Output format |
|---|---|---|
| Offer / proposal | `references/offer.md` | PDF |
| Proforma | `references/proforma.md` | PDF |
| Presentation | `references/presentation.md` | PPTX |
| Service sheet (one-pager) | `references/service-sheet.md` | PDF |
| Assessment report | `references/assessment.md` | PDF |
| Support plan (PolluxData Care) | `references/support-plan.md` | PDF |
| Case study | `references/case-study.md` | PDF |
| Project closure | `references/closure.md` | PDF |
| Follow-up email | `references/followup-email.md` | TXT |

Each type has a `sample-*.json` next to its reference for testing. Shared generator code lives in `scripts/common.py` (band cover, footer, headings, tables, totals, signature block, tokens).

## Pitfalls

- Never put the mascot inside pricing, scope or legal sections
- Partner logos and colors appear only if that partner is actually in the proposed solution
- If a price, legal term or client detail is unknown, ask — do not guess
- Keep one currency per document; state taxes (IVA) explicitly and separately
- Do not invent certifications or partnerships (Oracle, AWS, Azure) not confirmed by the user
