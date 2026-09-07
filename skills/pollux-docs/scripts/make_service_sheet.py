#!/usr/bin/env python3
"""Genera una ficha de servicio PolluxData (one-pager) en PDF (modo Paper).

Uso: make_service_sheet.py <ficha.json> [salida.pdf]
"""
import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

from common import (
    ASSETS, F_BODY, F_HEAD, F_HEAD_B, MUTED_C, NAVY, ORANGE, S, A4, LINE,
    draw_star, footer, heading, later_header, spaced_kicker, table_style,
    human_date,
)

BAND = 56 * mm


def cover(c, doc, data):
    W, H = A4
    top = H
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - BAND, W, BAND, stroke=0, fill=1)
    logo = ASSETS / "logo" / "pollux-logo.png"
    lw = 22 * mm
    if logo.exists():
        c.drawImage(str(logo), 18 * mm, top - 6 * mm - lw * 150 / 218,
                    width=lw, height=lw * 150 / 218, mask="auto")
    c.setFillColor(ORANGE)
    c.setFont(F_HEAD_B, 9.5)
    c.drawRightString(W - 18 * mm, top - 12 * mm, data["ref"])
    c.setFillColor(HexColor("#A9B0BD"))
    c.setFont(F_BODY, 7.5)
    c.drawRightString(W - 18 * mm, top - 16.5 * mm, human_date(data["date"]))
    spaced_kicker(c, "FICHA DE SERVICIO", 18 * mm, top - 26 * mm)
    c.setFillColor(HexColor("#FFFFFF"))
    size = 14
    y = top - 33 * mm
    c.setFont(F_HEAD, size)
    c.drawString(18 * mm, y, data["service"])
    draw_star(c, W - 58 * mm, H - BAND / 2 - 1 * mm, 9.5 * mm)
    footer(c, W, H)
    c.restoreState()


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Ficha de servicio — {data['service']}",
                          author="PolluxData", subject="Ficha de servicio",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - BAND - 30 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: cover(c, d, data)),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "FICHA DE SERVICIO")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "QUÉ RESUELVE")
    st.append(Paragraph(data["solves"], S["body"]))

    st += heading("02", "QUÉ INCLUYE")
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["includes"]]

    st += heading("03", "ENTREGABLES Y PLAZOS")
    rows = [[Paragraph("Entregable", S["th"]), Paragraph("Plazo", S["th_num"])]]
    for e in data["deliverables"]:
        rows.append([Paragraph(e["name"], S["td"]),
                     Paragraph(e["when"], S["td_num"])])
    t = Table(rows, colWidths=[(W - 36 * mm) - 32 * mm, 32 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("04", "INVERSIÓN")
    st.append(Paragraph(f"<b>Desde USD {data['from_price']}</b>", S["big"]))
    st.append(Paragraph(
        "Precio final según alcance y tamaño del entorno. Solicita tu proforma "
        "sin compromiso — la respondemos el mismo día.", S["note"]))

    st.append(Spacer(1, 10))
    st.append(Paragraph(
        f"¿Hablamos? Escríbenos a "
        f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font> o visita "
        "polluxdata.com", S["body"]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
