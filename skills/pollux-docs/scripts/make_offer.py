#!/usr/bin/env python3
"""Genera una oferta comercial PolluxData en PDF (modo Paper).

Uso: make_offer.py <oferta.json> [salida.pdf]
"""
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    HRFlowable,
    KeepTogether,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[3]
FONTS = ROOT / "skills" / "pollux-brand" / "assets" / "fonts"
ASSETS = ROOT / "skills" / "pollux-brand" / "assets"
PAL = json.loads((ASSETS / "palette.json").read_text())

NAVY = HexColor("#06111F")
ORANGE = HexColor(PAL["core"]["brand.primary"])
BODY_C = HexColor(PAL["paper_mode"]["paper.body"])
MUTED_C = HexColor(PAL["paper_mode"]["paper.muted"])
SOFT = HexColor(PAL["paper_mode"]["paper.bg-soft"])
LINE = HexColor("#E3E8EF")

MASCOTS = {
    "oracle": "pollux-oracle.png",
    "azure": "pollux-azure.png",
    "aws": "pollux-oracle-aws.png",
}

MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
       "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def reg(name, fname, fallback):
    p = FONTS / fname
    if p.exists():
        pdfmetrics.registerFont(TTFont(name, str(p)))
        return name
    return fallback


F_HEAD = reg("Manrope", "Manrope-ExtraBold.ttf", "Helvetica-Bold")
F_HEAD_B = reg("Manrope-Bold", "Manrope-Bold.ttf", "Helvetica-Bold")
F_HEAD_R = reg("Manrope", "Manrope-Regular.ttf", "Helvetica")
F_BODY = reg("Inter", "Inter-Regular.ttf", "Helvetica")
F_BODY_SB = reg("Inter-SB", "Inter-SemiBold.ttf", "Helvetica-Bold")
F_BODY_B = reg("Inter-B", "Inter-Bold.ttf", "Helvetica-Bold")

S_BODY = ParagraphStyle("body", fontName=F_BODY, fontSize=9.5, leading=14.5,
                        textColor=BODY_C, alignment=TA_LEFT, spaceAfter=5)
S = {
    "body": S_BODY,
    "li": ParagraphStyle("li", parent=S_BODY, leftIndent=10, spaceAfter=3.5,
                         bulletIndent=0, bulletFontName=F_BODY_B, bulletFontSize=8),
    "h": ParagraphStyle("h", fontName=F_HEAD_B, fontSize=12.5, leading=15,
                        textColor=NAVY, spaceBefore=2, spaceAfter=2),
    "th": ParagraphStyle("th", fontName=F_HEAD_B, fontSize=8.3, leading=11,
                         textColor=white),
    "td": ParagraphStyle("td", fontName=F_BODY, fontSize=8.8, leading=12,
                         textColor=BODY_C),
    "td_b": ParagraphStyle("td_b", fontName=F_BODY_SB, fontSize=8.8, leading=12,
                           textColor=NAVY),
    "td_num": ParagraphStyle("td_num", fontName=F_BODY_SB, fontSize=8.8,
                             leading=12, textColor=BODY_C, alignment=TA_RIGHT),
    "note": ParagraphStyle("note", fontName=F_BODY, fontSize=8, leading=11.5,
                           textColor=MUTED_C),
}


def fmt(n):
    s = f"{n:,.2f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def human_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MES[d.month - 1]} de {d.year}"


def draw_star(c, cx, cy, r):
    c.saveState()
    c.setStrokeColor(ORANGE)
    c.setStrokeAlpha(0.42)
    c.setLineWidth(0.9)
    for i in range(8):
        ang = math.radians(90 + i * 45)
        rr = r if i % 2 == 0 else r * 0.62
        c.line(cx, cy, cx + rr * math.cos(ang), cy + rr * math.sin(ang))
    c.setStrokeAlpha(0.3)
    c.circle(cx, cy, r * 0.5, stroke=1, fill=0)
    c.restoreState()


def cover_footer(c, doc, data):
    W, H = A4
    band = 64 * mm
    top = H
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - band, W, band, stroke=0, fill=1)

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

    c.setFont(F_BODY_SB, 8)
    c.setFillColor(ORANGE)
    kx = 18 * mm
    ky = top - 27 * mm
    for ch in "PROPUESTA COMERCIAL":
        c.drawString(kx, ky, ch)
        kx += pdfmetrics.stringWidth(ch, F_BODY_SB, 8) + 2.2

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

    draw_star(c, W - 44 * mm, H - band / 2 - 3 * mm, 14 * mm)
    _footer(c, W, H)
    c.restoreState()


def later_footer(c, doc, data):
    W, H = A4
    c.saveState()
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.6)
    c.line(18 * mm, H - 12 * mm, 18 * mm + 14 * mm, H - 12 * mm)
    c.setFillColor(NAVY)
    c.setFont(F_BODY_SB, 7)
    c.drawString(18 * mm + 17.5 * mm, H - 12.4 * mm, "POLLUXDATA · PROPUESTA COMERCIAL")
    c.setFillColor(BODY_C)
    c.setFont(F_BODY, 7)
    c.drawRightString(W - 18 * mm, H - 12.4 * mm, f"{data['ref']}")
    _footer(c, W, H)
    c.restoreState()


def _footer(c, W, H):
    fh = 15 * mm
    c.setFillColor(NAVY)
    c.rect(0, 0, W, fh, stroke=0, fill=1)
    logo = ASSETS / "logo" / "pollux-logo.png"
    lw = 17 * mm
    if logo.exists():
        c.drawImage(str(logo), 18 * mm, 2.2 * mm, width=lw, height=lw * 150 / 218,
                    mask="auto")
    x = 18 * mm + lw + 6 * mm
    c.setFillColor(white)
    c.setFont(F_BODY_SB, 7.5)
    c.drawString(x, fh / 2 + 2.6, "La estrella que nos guía.")
    c.setFillColor(HexColor("#9AA6B5"))
    c.setFont(F_BODY, 7)
    c.drawRightString(W - 18 * mm, fh / 2 + 3.4, "info@polluxdata.com · polluxdata.com")
    c.setFillColor(HexColor("#5F6B7A"))
    c.setFont(F_BODY, 6.5)
    c.drawRightString(W - 18 * mm, fh / 2 - 4.2, f"Página {c.getPageNumber():02d}")


def heading(num, title):
    return [
        CondPageBreak(45 * mm),
        Spacer(1, 6),
        KeepTogether([
            Paragraph(f'<font color="#F07A1F">{num}</font>'
                      f'<font color="#06111F">  —  {title}</font>', S["h"]),
            HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=3,
                       spaceAfter=8),
        ]),
    ]


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4, title=f"Propuesta {data['ref']} — {data['project_title']}",
                          author="PolluxData", subject="Propuesta comercial",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 64 * mm - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: cover_footer(c, d, data)),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_footer(c, d, data)),
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
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, SOFT]),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    st.append(t)
    st.append(Paragraph(
        "Las duraciones son estimaciones de trabajo efectivo y se confirman en el "
        "kickoff. Cada fase se cierra con aceptación escrita antes de continuar.",
        S["note"]))

    st += heading("05", "INVERSIÓN")
    cols = [9 * mm, 0, 20 * mm, 14 * mm, 30 * mm, 32 * mm]
    cols[1] = (W - 36 * mm) - sum(cols) + cols[1]
    head = [Paragraph(x, S["th"]) for x in
            ["#", "Concepto", "Unidad", "Cant.", "P. unit. (USD)", "Total (USD)"]]
    rows = [head]
    for i, it in enumerate(data["pricing"], 1):
        tot = it["qty"] * it["unit_price"]
        rows.append([Paragraph(str(i), S["td_num"]), Paragraph(it["item"], S["td"]),
                     Paragraph(it["unit"], S["td"]), Paragraph(str(it["qty"]), S["td_num"]),
                     Paragraph(fmt(it["unit_price"]), S["td_num"]), Paragraph(fmt(tot), S["td_num"])])
    t = Table(rows, colWidths=cols, repeatRows=1)
    t.hAlign = "LEFT"
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, SOFT]),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (3, 0), (5, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    st.append(t)
    st.append(Spacer(1, 6))

    sub = sum(i["qty"] * i["unit_price"] for i in data["pricing"])
    tax = round(sub * data["tax_rate"] / 100, 2)
    tot_rows = [
        [Paragraph("Subtotal", S["td"]), Paragraph(fmt(sub), S["td_num"])],
        [Paragraph(f"IVA {data['tax_rate']}%", S["td"]), Paragraph(fmt(tax), S["td_num"])],
        [Paragraph("<b>TOTAL</b>", ParagraphStyle("t", parent=S["td_b"], fontSize=9.5,
                     textColor=ORANGE)),
         Paragraph(f"<b>{fmt(sub + tax)}</b>", ParagraphStyle("tn", parent=S["td_num"],
                     fontSize=9.5, textColor=ORANGE))],
    ]
    tt = Table(tot_rows, colWidths=[70 * mm, 32 * mm], hAlign="RIGHT")
    tt.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, ORANGE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
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
    half = (W - 36 * mm) / 2 - 6 * mm
    sig = [
        [Paragraph("<b>Por PolluxData</b>", S["td_b"]),
         Paragraph(f"<b>Por {data['client']['company']}</b>", S["td_b"])],
        [Paragraph(data["sender"]["name"], S["td"]), Paragraph("", S["td"])],
        [Paragraph(f"Cargo: ____________________", S["td"]),
         Paragraph("Nombre: ____________________", S["td"])],
        [Paragraph("Firma", S["note"]), Paragraph("Firma", S["note"])],
        [Paragraph("", S["td"]), Paragraph("", S["td"])],
        [Paragraph("Fecha: ______ / ______ / __________", S["td"]),
         Paragraph("Fecha: ______ / ______ / __________", S["td"])],
    ]
    stg = Table(sig, colWidths=[half, half])
    stg.setStyle(TableStyle([
        ("LINEBELOW", (0, 4), (-1, 4), 0.9, NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, 1), 24),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    st.append(KeepTogether([stg]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
