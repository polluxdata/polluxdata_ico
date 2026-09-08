# Changelog — pollux-brand

Todos los cambios de identidad visual se registran aquí. Un cambio de token pasa por este archivo antes de tocar `palette.json`.

## 1.2.0 — 2026-09-07

- **Vectores oficiales obtenidos** de MKT/Logos (OneDrive): `pollux-wordmark.svg` regenerado con los contornos reales (ATComputer + BankGothicCLtBT; la reconstrucción Michroma retirada definitivamente)
- Color oficial del isotipo confirmado desde el SVG fuente: `#D45500` (la medición previa `#D04503` venía del antialiasing del favicon)
- Carpeta `assets/logo/official/` con los archivos fuente de marca: logofinal.svg/.pdf/.png, logofinal_blanco.png, logofinal_bw.png, estrella.svg/.png
- Nuevos assets de mascota informal: familia **PolluxDog** (silueta flat navy #202B56 de frente, con sus Wayfarer renderizadas como parches pixel-art a la altura de los ojos) — polluxdog.png, DisenoSoloCara, DisenoCompleto con tagline, variante negra. Reglas de uso documentadas en SKILL.md (emails/firmas informales; nunca en documentos formales)

## 1.1.1 — 2026-09-07

- **Corrección de isotipo**: `brand.star` medido por píxel sobre el favicon oficial → `#D04503` (antes `#F05A24`, estimación visual imprecisa). Sustituido en v1.2.0 por el valor oficial del SVG fuente: `#D45500`
- `assets/logo/pollux-star.svg` regenerado con la geometría real medida del favicon (aguja vertical 1.66:1, rayos que no tocan el punto central, anillo r=0.72, diagonales cortas que mueren en el anillo)
- Retirado `pollux-wordmark.svg` y su generador: la reconstrucción con Michroma no era fiel al wordmark original. Pendiente obtener el vector real (ver ROADMAP)
- `draw_star` de los generadores actualizado a las proporciones medidas

## 1.1.0 — 2026-09-07

- Fuentes Manrope e Inter incluidas en `assets/fonts/` (licencia OFL), con name tables corregidas (families: `Manrope`, `Manrope Bold`, `Manrope ExtraBold`, `Inter`, `Inter SemiBold`, `Inter Bold`)
- Modo demo: bandera `"demo": true` estampa "MUESTRA · DATOS FICTICIOS" (implementado en los generadores de pollux-docs)
- Añadido `assets/logo/pollux-star.svg` (isotipo vectorial) y `pollux-wordmark.svg` (reconstrucción aproximada en Michroma — pendiente el vector original de la marca)

## 1.0.0 — 2026-09-06

- Sistema de marca inicial: tokens de color (core, dark cinematic, paper mode, partners)
- Tipografía: Manrope (headings) / Inter (cuerpo) / Playfair Display (solo tributo)
- Mascota Pollux: descripción canónica, reglas de uso, poses y prohibiciones
- Normalización de acentos: naranja `#F07A1F` unificado, `#F05A24` solo isotipo, rojo `#C8102E` solo mascota/tributo
