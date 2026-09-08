#!/usr/bin/env python3
"""Genera una proforma PolluxData en PDF (modo Paper).

Uso: make_proforma.py <proforma.json> [salida.pdf]
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
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
    ASSETS, F_BODY, F_BODY_SB, F_HEAD_B, NAVY, ORANGE, S,
    draw_star, fmt, footer, heading, human_date, later_header, spaced_kicker,
    table_style, totals_block,
)

BAND = 46 * mm


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
    c.drawRightString(W - 18 * mm, top - 12 * mm, f"Ref {data['ref']}")
    c.setFillColor(HexColor("#A9B0BD"))
    c.setFont(F_BODY, 7.5)
    c.drawRightString(W - 18 * mm, top - 16.5 * mm, human_date(data["date"]))

    spaced_kicker(c, "PROFORMA", 18 * mm, top - 27 * mm)

    c.setFillColor(HexColor("#C8D4E6"))
    c.setFont(F_BODY, 9.5)
    cl = data["client"]
    y = top - 36 * mm
    c.setFont(F_BODY_SB, 9)
    c.setFillColor(HexColor("#C8D4E6"))
    c.drawString(18 * mm, y, f"Preparada para {cl['company']}")
    c.setFont(F_BODY, 8)
    c.setFillColor(HexColor("#8B97A8"))
    c.drawString(18 * mm, y - 4.6 * mm, f"Contacto: {cl['contact']} — {cl['role']}")

    draw_star(c, W - 58 * mm, H - BAND / 2 - 2 * mm, 9.5 * mm)
    footer(c, W, H, demo=data.get("demo", False))
    c.restoreState()


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Proforma {data['ref']}",
                          author="PolluxData", subject="Proforma",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - BAND - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: cover(c, d, data)),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "PROFORMA")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "DETALLE")
    cols = [9 * mm, 0, 22 * mm, 14 * mm, 30 * mm, 32 * mm]
    cols[1] = (W - 36 * mm) - sum(cols) + cols[1]
    head = [Paragraph("#", S["th_num"]), Paragraph("Descripción", S["th"]),
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
    st.append(Spacer(1, 3))
    st.append(Paragraph(
        "Esta proforma no constituye factura. Los consumos de nube se facturan "
        "aparte según uso.", S["note"]))
    st.append(Spacer(1, 6))

    sub = sum(i["qty"] * i["unit_price"] for i in data["pricing"])
    tt, tax = totals_block(sub, data["tax_rate"])
    st.append(KeepTogether([tt]))

    st.append(Spacer(1, 16))

    st += heading("02", "CONDICIONES")
    val = date.fromisoformat(data["date"]) + timedelta(days=data["validity_days"])
    conds = [
        f"<b>Validez:</b> {data['validity_days']} días desde el "
        f"{human_date(data['date'])}, es decir, hasta el "
        f"{human_date(val.isoformat())}.",
        f"<b>Forma de pago:</b> {data['payment_terms_detail']}",
        f"<b>Tiempo de entrega:</b> {data['delivery_time']}",
        f"<b>Datos de pago:</b> {data['payment_details']}",
    ]
    st += [Paragraph(x, S["li"], bulletText="—") for x in conds]

    st.append(Spacer(1, 16))

    st += heading("03", "ACEPTACIÓN")
    st.append(Paragraph(
        "Para aceptar esta proforma, firma y devuelve una copia a "
        f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font>.", S["body"]))
    st.append(Spacer(1, 10))
    sig = [[
        Paragraph("Nombre: ___________________________", S["td"]),
        Paragraph("Firma: ___________________________", S["td"]),
        Paragraph("Fecha: ______ / ______ / ________", S["td"]),
    ]]
    stg = Table(sig, colWidths=[(W - 36 * mm) / 3] * 3)
    stg.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    st.append(KeepTogether([stg]))
    st.append(Spacer(1, 14))
    st.append(Paragraph(
        f"Emitida por <b>PolluxData</b> — {data['sender']['name']} · "
        f"{data['sender']['email']} · polluxdata.com", S["note"]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
