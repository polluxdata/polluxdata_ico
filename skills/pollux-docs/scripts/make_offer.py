#!/usr/bin/env python3
"""Genera una oferta comercial PolluxData en PDF (modo Paper).

Uso: make_offer.py <oferta.json> [salida.pdf]
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from common import (
    ASSETS, F_BODY, F_BODY_SB, F_HEAD, F_HEAD_B, NAVY, ORANGE, S,
    draw_star, fmt, footer, heading, human_date, later_header,
    spaced_kicker, table_style, totals_block,
)

BAND = 64 * mm


def cover(c, doc, data):
    W, H = A4
    top = H
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - BAND, W, BAND, stroke=0, fill=1)

    logo = ASSETS / "logo" / "pollux-logo.png"
    lw = 24 * mm
    if logo.exists():
        c.drawImage(str(logo), 18 * mm, top - 6 * mm - lw * 150 / 218,
                    width=lw, height=lw * 150 / 218, mask="auto")

    c.setFillColor(ORANGE)
    c.setFont(F_HEAD_B, 9.5)
    c.drawRightString(W - 18 * mm, top - 12 * mm, f"Ref {data['ref']}")
    c.setFillColor(HexColor("#A9B0BD"))
    c.setFont(F_BODY, 7.5)
    c.drawRightString(W - 18 * mm, top - 16.5 * mm, human_date(data["date"]))

    spaced_kicker(c, "PROPUESTA COMERCIAL", 18 * mm, top - 27 * mm)

    c.setFillColor(white)
    size = 17.5
    tw = W - 36 * mm - 60 * mm
    lines = simpleSplit(data["project_title"], F_HEAD, size, tw)
    while len(lines) > 2 and size > 12:
        size -= 0.5
        lines = simpleSplit(data["project_title"], F_HEAD, size, tw)
    c.setFont(F_HEAD, size)
    y = top - 37 * mm
    for ln in lines:
        c.drawString(18 * mm, y, ln)
        y -= size * 1.2
    y -= 5
    c.setFillColor(HexColor("#C8D4E6"))
    c.setFont(F_BODY_SB, 9)
    c.drawString(18 * mm, y, f"Preparada para {data['client']['company']}")
    y -= 12
    c.setFillColor(HexColor("#8B97A8"))
    c.setFont(F_BODY, 8)
    cl = data["client"]
    c.drawString(18 * mm, y, f"Contacto: {cl['contact']} — {cl['role']}")

    draw_star(c, W - 44 * mm, H - BAND / 2 - 3 * mm, 14 * mm)
    footer(c, W, H, demo=data.get("demo", False))
    c.restoreState()


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Propuesta {data['ref']} — {data['project_title']}",
                          author="PolluxData", subject="Propuesta comercial",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - BAND - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: cover(c, d, data)),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "PROPUESTA COMERCIAL")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "RESUMEN EJECUTIVO")
    st.append(Paragraph(data["executive_summary"], S["body"]))

    st += heading("02", "CONTEXTO Y OBJETIVO")
    st.append(Paragraph(data["context"], S["body"]))
    st.append(Spacer(1, 2))
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["goals"]]

    st += heading("03", "ALCANCE")
    st.append(Paragraph("<b>Incluye</b>", S["td_b"]))
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["scope_in"]]
    st.append(Spacer(1, 3))
    st.append(Paragraph("<b>No incluye</b>", S["td_b"]))
    st += [Paragraph(x, S["li"], bulletText="—") for x in data["scope_out"]]

    st += heading("04", "METODOLOGÍA Y PLAN DE TRABAJO")
    rows = [[Paragraph("Fase", S["th"]), Paragraph("Entregable", S["th"]),
             Paragraph("Duración", S["th"])]]
    for i, p in enumerate(data["phases"], 1):
        rows.append([Paragraph(f"Fase {i}", S["td_b"]), Paragraph(p["deliverable"], S["td"]),
                     Paragraph(p["duration"], S["td_num"])])
    t = Table(rows, colWidths=[22 * mm, (W - 36 * mm) - 22 * mm - 30 * mm, 30 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)
    st.append(Paragraph(
        "Las duraciones son estimaciones de trabajo efectivo y se confirman en el "
        "kickoff. Cada fase se cierra con aceptación escrita antes de continuar.",
        S["note"]))

    st += heading("05", "INVERSIÓN")
    cols = [9 * mm, 0, 20 * mm, 14 * mm, 30 * mm, 32 * mm]
    cols[1] = (W - 36 * mm) - sum(cols) + cols[1]
    head = [Paragraph("#", S["th_num"]), Paragraph("Concepto", S["th"]),
            Paragraph("Unidad", S["th"])] + \
           [Paragraph(x, S["th_num"]) for x in ["Cant.", "P. unit. (USD)", "Total (USD)"]]
    rows = [head]
    for i, it in enumerate(data["pricing"], 1):
        tot = it["qty"] * it["unit_price"]
        rows.append([Paragraph(str(i), S["td_num"]), Paragraph(it["item"], S["td"]),
                     Paragraph(it["unit"], S["td"]), Paragraph(str(it["qty"]), S["td_num"]),
                     Paragraph(fmt(it["unit_price"]), S["td_num"]), Paragraph(fmt(tot), S["td_num"])])
    t = Table(rows, colWidths=cols, repeatRows=1)
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)
    st.append(Spacer(1, 6))

    sub = sum(i["qty"] * i["unit_price"] for i in data["pricing"])
    tt, tax = totals_block(sub, data["tax_rate"])
    st.append(KeepTogether([
        tt,
        Spacer(1, 4),
        Paragraph(data["payment_terms"], S["body"]),
    ]))

    st += heading("06", "CONDICIONES")
    val = date.fromisoformat(data["date"]) + timedelta(days=data["validity_days"])
    conds = [
        f"<b>Validez de la oferta:</b> {data['validity_days']} días desde el "
        f"{human_date(data['date'])}, es decir, hasta el "
        f"{human_date(val.isoformat())}.",
        f"<b>Pagos:</b> {data['payment_terms_detail']}",
        f"<b>Garantía:</b> {data['warranty']}",
        "<b>Confidencialidad:</b> esta propuesta es confidencial y de uso exclusivo "
        "para el destinatario.",
        "<b>Facturación:</b> los precios no incluyen servicios de terceros ni "
        "consumos de nube, que se facturan aparte según uso.",
    ]
    st += [Paragraph(x, S["li"], bulletText="—") for x in conds]

    st += heading("07", "ACEPTACIÓN Y SIGUIENTE PASO")
    st.append(Paragraph(
        "Para aceptar esta propuesta, firma ambas copias y devuelve una a "
        f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font>. "
        "Cualquier duda la respondemos el mismo día.", S["body"]))
    st.append(Spacer(1, 8))
    from common import signature_block
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
