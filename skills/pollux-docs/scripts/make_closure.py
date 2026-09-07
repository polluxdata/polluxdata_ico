#!/usr/bin/env python3
"""Genera un informe de cierre de proyecto PolluxData en PDF (modo Paper).

Uso: make_closure.py <cierre.json> [salida.pdf]
"""
import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageTemplate,
    Paragraph, Spacer, Table,
)

from common import (
    ORANGE, S, A4, band_cover, heading, later_header, table_style,
    signature_block,
)


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Cierre de proyecto {data['ref']}",
                          author="PolluxData", subject="Informe de cierre",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 64 * mm - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: band_cover(c, d, data, "INFORME DE CIERRE DE PROYECTO",
                                                    title=data["title"])),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "CIERRE DE PROYECTO")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "RESUMEN DEL PROYECTO")
    rows = [[Paragraph("Campo", S["th"]), Paragraph("Detalle", S["th"])]]
    for k, v in data["summary"]:
        rows.append([Paragraph(f"<b>{k}</b>", S["td"]), Paragraph(v, S["td"])])
    t = Table(rows, colWidths=[40 * mm, (W - 36 * mm) - 40 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("02", "ENTREGABLES")
    rows = [[Paragraph("Entregable", S["th"]), Paragraph("Estado", S["th_num"])]]
    for e in data["deliverables"]:
        rows.append([Paragraph(e["name"], S["td"]),
                     Paragraph(f"<font color=\"#F07A1F\"><b>✓</b></font> {e['status']}",
                               S["td_num"])])
    t = Table(rows, colWidths=[(W - 36 * mm) - 42 * mm, 42 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("03", "ACCESOS Y RESPONSABLES")
    rows = [[Paragraph("Sistema", S["th"]), Paragraph("Responsable (cliente)", S["th"])]]
    for a in data["access"]:
        rows.append([Paragraph(a["system"], S["td"]),
                     Paragraph(a["owner"], S["td"])])
    t = Table(rows, colWidths=[(W - 36 * mm) / 2, (W - 36 * mm) / 2])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)
    st.append(Paragraph(
        "Las credenciales no se incluyen en este documento por seguridad; se "
        "entregaron por canal seguro durante el handover.", S["note"]))

    st += heading("04", "GARANTÍA Y SOPORTE")
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["warranty"]]

    st += heading("05", "RECOMENDACIONES")
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["recommendations"]]

    st += heading("06", "ACTA DE ACEPTACIÓN")
    st.append(Paragraph(data["acceptance"], S["body"]))
    st.append(Spacer(1, 8))
    st.append(KeepTogether([signature_block(data)]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
