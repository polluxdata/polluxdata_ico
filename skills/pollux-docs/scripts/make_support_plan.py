#!/usr/bin/env python3
"""Genera una propuesta de soporte mensual PolluxData en PDF (modo Paper).

Uso: make_support_plan.py <soporte.json> [salida.pdf]
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
    NAVY, ORANGE, S, A4, band_cover, heading, later_header, table_style,
    totals_block, signature_block,
)


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Plan de soporte {data['ref']}",
                          author="PolluxData", subject="Propuesta de soporte mensual",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 64 * mm - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: band_cover(c, d, data, "PLAN DE SOPORTE GESTIONADO",
                                                    title=data["title"])),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "PLAN DE SOPORTE")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "QUÉ INCLUYE EL PLAN")
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["includes"]]

    st += heading("02", "ACUERDO DE NIVEL DE SERVICIO")
    rows = [[Paragraph("Severidad", S["th"]), Paragraph("Ejemplo", S["th"]),
             Paragraph("Respuesta", S["th_num"])]]
    for sla in data["sla"]:
        rows.append([Paragraph(sla["level"], S["td_b"]),
                     Paragraph(sla["example"], S["td"]),
                     Paragraph(sla["response"], S["td_num"])])
    t = Table(rows, colWidths=[30 * mm, (W - 36 * mm) - 30 * mm - 34 * mm, 34 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("03", "ALCANCE MENSUAL")
    rows = [[Paragraph("Concepto", S["th"]), Paragraph("Incluye", S["th_num"])]]
    for a in data["monthly_scope"]:
        rows.append([Paragraph(a["concept"], S["td"]),
                     Paragraph(a["value"], S["td_num"])])
    t = Table(rows, colWidths=[(W - 36 * mm) - 40 * mm, 40 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("04", "INVERSIÓN MENSUAL")
    sub = data["monthly_fee"]
    tt, tax = totals_block(sub, data["tax_rate"])
    st.append(KeepTogether([
        tt,
        Spacer(1, 4),
        Paragraph(data["payment_terms"], S["body"]),
    ]))

    st += heading("05", "CONDICIONES")
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["conditions"]]

    st += heading("06", "ACEPTACIÓN")
    st.append(Paragraph(
        "Para activar el plan, firma y devuelve una copia a "
        f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font>. "
        "El soporte queda operativo en 48 horas desde la firma.", S["body"]))
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
