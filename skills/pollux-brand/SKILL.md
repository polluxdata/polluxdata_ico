---
name: pollux-brand
description: Applies PolluxData's official brand system (colors, typography, logo, mascot "Pollux", tone of voice) to any artifact — commercial documents, offers, proformas, presentations, web content or generated images. Use it whenever a PolluxData deliverable is created or styled.
license: Proprietary — PolluxData. Internal use only.
metadata:
  tags: [brand, design, documents, mascot]
  related_skills: [pollux-docs]
---

# PolluxData Brand System

## Overview

This skill encodes the PolluxData identity so any agent can produce coherent artifacts without reinventing the look. Two operating modes exist: **Dark cinematic** (marketing, presentation covers, partner scenes) and **Paper mode** (formal documents like offers and proformas). When in doubt, check the visual mode rules below.

**Keywords**: branding, polluxdata, pollux, look and feel, colors, typography, mascot, styling

## Brand story (why the star)

PolluxData is named after Pollux, a white schnauzer (2011–2026) who accompanied the founders for fifteen years. The star in the logo is his memory — the star that guides. Treat any reference to the real Pollux with respect: it may appear in storytelling and tribute contexts, never as a commercial gimmick.

## Colors

### Core brand

| Token | Hex | Usage |
|---|---|---|
| `brand.primary` | `#F07A1F` | Main accent: buttons, links, highlights, chart series 1 |
| `brand.primary-dark` | `#D94A38` | Hover states, gradient end |
| `brand.primary-light` | `#FF9B3D` | Gradient start, subtle fills |
| `brand.star` | `#F05A24` | Isotipo star ONLY (logo/favicon). Historical exception, do not reuse elsewhere |
| `mascot.red` | `#C8102E` | Mascot jacket accents, tribute/emotional pieces ONLY |
| `mascot.neon-red` | `#FF1E2D` | Light/neon effects on dark scenes ONLY (never for text) |

### Dark cinematic palette (mode 1)

| Token | Hex | Usage |
|---|---|---|
| `dark.bg` | `#06111F` | Primary background |
| `dark.bg-2` | `#071A2D` | Elevated surfaces |
| `dark.bg-blue` | `#0B2F55` | Panels, cards on dark |
| `dark.text-primary` | `#FFFFFF` | Headings on dark |
| `dark.text-body` | `#FFFFFFB8` | Body text on dark (72% white) |
| `dark.text-muted` | `#A9B0BD` | Captions, metadata |

### Paper mode palette (mode 2 — formal documents)

| Token | Hex | Usage |
|---|---|---|
| `paper.bg` | `#FFFFFF` | Page background |
| `paper.bg-soft` | `#F6F7FB` | Section bands, table stripes |
| `paper.heading` | `#06111F` | Headings, primary text |
| `paper.body` | `#5B6573` | Body text |
| `paper.muted` | `#A9B0BD` | Footnotes, metadata |
| `paper.dark-text` | `#C8D4E6` | Text on navy bands |
| `paper.accent` | `#F07A1F` | Rules, key numbers, section markers |
| `paper.navy-band` | `#06111F` | Header/footer bands, cover blocks |

### Partner accents (ONLY when the partner's logo is present in the artifact)

| Partner | Hex |
|---|---|
| Oracle | `#E8112D` (neon `#FF1E2D`) |
| Microsoft Azure | `#0078D4` (neon `#3AA0FF`) |
| AWS | `#FF9900` |
| Status/online | `#31D887` |

## Typography

- **Headings**: Manrope, fallback Inter → Arial
- **Body**: Inter, fallback system-ui → Arial
- **Mono** (code, prices in tables): SF Mono / Fira Code, fallback monospace
- **Serif** (Playfair Display): ONLY for tribute/emotional storytelling (like the in memoriam piece). Never in offers, proformas or technical docs
- **Logo**: never retype it — always use the image file `assets/logo/pollux-logo.png`

## Logo

- **Vector oficial**: `assets/logo/pollux-wordmark.svg` (extraído del logofinal.svg original — tipografía ATComputer + BankGothicCLtBT convertidas a contornos, estrella #D45500)
- **Fuentes del logo**: ATComputer (P✦LLUX) y BankGothicCLtBT (DATA) — no reescribir el logo con otras tipografías; usar siempre el SVG
- Variantes oficiales en `assets/logo/official/`: logofinal.svg/.pdf/.png (navy #002255 sobre blanco), logofinal_blanco.png (blanco), logofinal_bw.png (B/N), estrella.svg/.png
- Isotipo digital: `assets/logo/pollux-star.svg` (estrella sola, transparente)
- Clear space: minimum = height of the star around all sides
- Minimum width: 120 px digital / 25 mm print
- Preferred on dark backgrounds; on white, navy bands or soft gray are acceptable. Never place the logo on orange/red backgrounds
- Never recolor, distort, rotate or add effects to the logo

## Mascot — Pollux

### Canonical character description

Anthropomorphic cream-white schnauzer (`#F2EFE7`), hyperrealistic cinematic CGI (NOT flat cartoon, NOT thick-line, NOT childish), bushy beard and eyebrows, folded ear tips. Black Ray-Ban Wayfarer sunglasses with opaque lenses and micro-text "pollux" on the temple arm. Black softshell jacket with high collar, red `#C8102E` inner lining and zippers, red 8-point nautical star patch on the left shoulder. Calm confident expression, chin up, "relaxed winner" attitude. Never smiles caricaturistically.

English prompt base for image generators:

> Anthropomorphic cream-white schnauzer, hyperrealistic cinematic CGI, bushy beard and eyebrows, folded-ear tips. Black Wayfarer-style sunglasses with opaque lenses, "pollux" printed on the temple arm. Black softshell jacket with high collar, red `#C8102E` inner lining and zippers, red 8-point nautical star patch on left shoulder. Calm confident expression, chin up, relaxed winner attitude.

### Existing assets (reuse before generating new ones)

| File | Scene |
|---|---|
| `assets/mascot/pollux-oracle.png` | Oracle datacenter, neon red cloud |
| `assets/mascot/pollux-azure.png` | Oracle + Azure, arms crossed, red/blue symmetric |
| `assets/mascot/pollux-oracle-aws.png` | Oracle + AWS, arms crossed, red/amber |
| `assets/mascot/pollux-in-memoriam.png` | Tribute: from behind, watching the star |
| `assets/mascot/pollux-office-lifestyle.jpg` | Daylight office lifestyle variant |

### PolluxDog icon (flat, informal)

Flat navy `#202B56` silhouette of the schnauzer head, front view: dropped triangular ears, spiky beard, and his signature **Wayfarer sunglasses rendered as pixel-art patches** at eye level (abstract pixel style, no frame detail). This is the informal Pollux — same character as the CGI mascot, different rendering. For informal contexts:

| File | Content | Usage |
|---|---|---|
| `assets/mascot/polluxdog.png` | Head only, 88 px | Email signatures, inline icons. Never scale beyond ~150 px |
| `assets/mascot/PolluxDog-DisenoSoloCara-Dog-Azul.png` | Head, full-res | Avatars, social profiles, stickers, informal document covers |
| `assets/mascot/PolluxDog-DisenoCompleto-Dog-Azul.png` | Head + tagline "DOMINA LA BASE DE DATOS" | Marketing material only (posters, landing). Never as icon — tagline illegible at small sizes |
| `assets/mascot/polluxdog_black.jpg` | Black variant | Dark/light prints where navy doesn't work |

Rules: PolluxDog is welcome in email signatures, informal emails, social media and casual one-pagers. NEVER in formal documents (offers, proformas, assessments — those use the isotype star), never recolored, never rebuilt.

### Usage rules

1. **The Wayfarers are non-negotiable.** The character wears them in 100% of images, any context or pose. Eyes are never visible.
2. **Uniform**: black softshell + red lining + red star patch on left shoulder. The jacket-less variant exists only in daylight lifestyle scenes.
3. **Where the mascot appears**:
   - Presentation covers: yes, prominently
   - Offer/proforma cover: optional, small banner — never inside pricing or legal sections
   - Pricing tables, terms, contracts: never
   - Web/blog/marketing: yes
4. **Poses allowed**: ¾ profile facing camera; arms crossed facing camera; seated observing. Looking at camera in all standard material. From behind ONLY in tribute/emotional pieces (looking at the star).
5. **Background default**: dark cinematic datacenter, neon cloud colored by the partner mentioned (`#FF1E2D` Oracle, `#0078D4` Azure, `#FF9900` AWS). Two partners = symmetric composition, mascot centered between both clouds. One partner = mascot in left third, brand cloud right.
6. **Style**: photorealistic CGI with neon glow, high fur detail, rim light of the neon color. Daylight lifestyle scenes use realistic photography light, never flat illustration.

## Visual modes — when to use which

| Mode | Artifacts |
|---|---|
| 1. Dark cinematic | Presentation covers, marketing, social, partner scenes |
| 2. Paper mode | Offers, proformas, proposals, technical PDFs: white background, navy header band, orange accents. The mascot may appear only as a small cover element |
| 3. Lifestyle | Product/office contexts, blog imagery |

## Tone of voice

Attitude: **informal-ganadora** (casual winner).

- Direct, confident, close. Short sentences. No rigid corporate boilerplate
- Address the client as "tú" in Spanish marketing content; "usted" is acceptable in formal contracts if the client's tone requires it — match the client
- Confident but never arrogant or salesy-pushy: state facts and capabilities plainly
- Humor is welcome in web/blog, minimal in offers, absent in legal sections
- Tribute content (Pollux in memoriam): reverent, warm, never commercial

## Do / Don't

| ✅ Do | ❌ Don't |
|---|---|
| Orange `#F07A1F` for all interactive accents | Use `#F05A24` outside the isotipo |
| Red `#C8102E` only for mascot/tribute | Red for buttons, links or CTAs |
| Partner colors only with partner logos | Inventing new accent colors per document |
| Manrope/Inter everywhere | Playfair outside tribute pieces |
| Dark cinematic for presentations | Dark cinematic for printable offers (use Paper mode) |
| Reuse existing mascot assets | Generate cartoon versions of Pollux |
| One star glyph (8 points, inscribed circle) | Redesigning the star per use case |
