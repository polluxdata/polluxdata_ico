# Handoff → Agente del repo web (polluxdata.com)

Tarea para el agente que mantiene el sitio web de PolluxData (Astro). Este documento es autocontenido: todo lo que necesitas está aquí o en el repo público de marca.

**Repo de marca**: `polluxdata/polluxdata_ico` (público, tag recomendado `v1.2.0` o el último `main`)
**Regla de aislamiento**: la web NO vende el repo entero — descarga solo los assets indicados por URL raw y los copia a `public/`.

## Tarea 1 — Descubrimiento estándar de skills (well-known)

1. Crear en el repo web: `public/.well-known/skills/index.json`
2. Copiar el contenido de:
   `https://raw.githubusercontent.com/polluxdata/polluxdata_ico/main/.well-known/skills/index.json`
3. Desplegar. Verificación:
   ```bash
   curl -s https://polluxdata.com/.well-known/skills/index.json | python3 -m json.tool
   # debe devolver el JSON con pollux-brand y pollux-docs (hoy da 404)
   ```

## Tarea 2 — Migrar el logo a SVG (además de resolver el pixelado)

El sitio usa `images/pollux-logo.png` (218 px, se pixela). Reemplazo:

| Uso en la web | Asset correcto |
|---|---|
| Header/footer sobre fondo **claro** | `https://raw.githubusercontent.com/polluxdata/polluxdata_ico/main/skills/pollux-brand/assets/logo/official/logofinal.svg` (letras navy #002255, es el archivo oficial) |
| Footer/hero sobre fondo **oscuro** | `https://raw.githubusercontent.com/polluxdata/polluxdata_ico/main/skills/pollux-brand/assets/logo/pollux-wordmark.svg` (letras blancas) |
| Isotipo solo (favicon, badges) | `.../assets/logo/pollux-star.svg` |

Pasos:
1. Descargar los 2-3 SVG a `public/images/` (o `src/assets/`) del repo web — NO enlazarlos en caliente a GitHub en producción (latencia + dependencia externa)
2. Buscar todos los usos de `pollux-logo.png` en el sitio y sustituir por el SVG según fondo
3. Ajustar `width/height` (el SVG tiene proporción distinta al PNG de 218×150 — revisar CSS)
4. Borrar `pollux-logo.png` si queda sin referencias

Verificación: logo nítido a cualquier zoom, sin pixelado.

## Tarea 3 — Auditoría de color del isotipo

El color oficial de la estrella cambió: **`#F05A24` → `#D45500`** (valor del SVG fuente, ver CHANGELOG v1.2.0 del repo de marca).

```bash
grep -rn "F05A24\|f05a24" --include="*.astro" --include="*.css" --include="*.js" .
```

- Si aparece `#F05A24` en contextos de isotipo/estrella → cambiar a `#D45500`
- **No tocar** `#F07A1F` (brand primary para botones/links — sigue siendo oficial)

## Criterios de aceptación (los 3)

- [ ] `https://polluxdata.com/.well-known/skills/index.json` responde 200 con JSON válido
- [ ] Ninguna referencia activa a `pollux-logo.png`; el logo en pantalla es nítido (SVG)
- [ ] Cero apariciones de `#F05A24` en el código fuente del sitio

## Notas

- Los assets de marca son la fuente de verdad; si algún día cambian, re-sincronizar desde el repo de marca y actualizar el hash/commit
- Este repo expone además `assets/mascot/polluxdog.png` y variantes si el sitio quisiera añadir el toque informal (leer `skills/pollux-brand/SKILL.md` → sección PolluxDog para reglas de uso y fondos)