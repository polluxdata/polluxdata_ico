# Muestras — documentos de prueba

⚠️ **Estos documentos son MUESTRAS generadas automáticamente.**

- Todos los datos son **100% ficticios**: "Importadora Andes Cía. Ltda.", sus precios, fechas, resultados y la cita de cliente no corresponden a ninguna empresa real.
- Llevan la marca **"MUESTRA · DATOS FICTICIOS"** y marca de agua en diagonal.
- Su único propósito es mostrar el sistema de plantillas de PolluxData (skills/pollux-docs): estructura, estilos de marca y formatos de salida.
- **No** constituyen ofertas, cotizaciones ni compromisos de ningún tipo.

Para generar un documento real, un agente con los skills `pollux-docs` + `pollux-brand` instalados procesa un JSON **sin** la bandera `"demo"` (ver `skills/pollux-docs/SKILL.md`).

Regenerarlas localmente:

```bash
python3 skills/pollux-docs/scripts/make_offer.py skills/pollux-docs/references/sample-offer.json muestras/OF-2026-042.pdf
# (repetir con cada generador)
```
