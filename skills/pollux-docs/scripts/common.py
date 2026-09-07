"""Utilidades compartidas para los generadores de documentos PolluxData (modo Paper)."""
import json
import math
from datetime import date
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    KeepTogether,
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
S["th_num"] = ParagraphStyle("th_num", parent=S["th"], alignment=TA_RIGHT)
S["big"] = ParagraphStyle("big", fontName=F_BODY_SB, fontSize=20, leading=26,
                          textColor=ORANGE, spaceAfter=8)
S["metric"] = ParagraphStyle("metric", fontName=F_BODY_SB, fontSize=24, leading=29,
                             textColor=ORANGE, spaceAfter=4)


def fmt(n):
    s = f"{n:,.2f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def human_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MES[d.month - 1]} de {d.year}"


def spaced_kicker(c, text, x, y, size=8, color=ORANGE, gap=2.2):
    c.setFont(F_BODY_SB, size)
    c.setFillColor(color)
    for ch in text:
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, F_BODY_SB, size) + gap


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


def demo_marker(c, W, H):
    c.saveState()
    c.setFont(F_HEAD_B, 6.5)
    c.setFillColor(ORANGE)
    c.drawRightString(W - 10 * mm, H - 7 * mm, "MUESTRA · DATOS FICTICIOS")
    c.translate(W / 2, H / 2)
    c.rotate(45)
    c.setFont(F_HEAD, 92)
    c.setFillAlpha(0.10)
    c.drawCentredString(0, 0, "MUESTRA")
    c.restoreState()


def footer(c, W, H, demo=False):
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
    if demo:
        demo_marker(c, W, H)


def later_header(c, doc, data, label):
    W, H = A4
    c.saveState()
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.6)
    c.line(18 * mm, H - 12 * mm, 18 * mm + 14 * mm, H - 12 * mm)
    c.setFillColor(NAVY)
    c.setFont(F_BODY_SB, 7)
    c.drawString(18 * mm + 17.5 * mm, H - 12.4 * mm, f"POLLUXDATA · {label}")
    c.setFillColor(BODY_C)
    c.setFont(F_BODY, 7)
    c.drawRightString(W - 18 * mm, H - 12.4 * mm, f"{data['ref']}")
    footer(c, W, H, demo=data.get("demo", False))
    c.restoreState()


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


def table_style():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, SOFT]),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ])


def band_cover(c, doc, data, label, band=64 * mm, title=None, title_size=17.5,
               client_label="Preparada para"):
    W, H = A4
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
    spaced_kicker(c, label, 18 * mm, top - 27 * mm)
    y = top - 37 * mm
    if title:
        size = title_size
        lines = simpleSplit(title, F_HEAD, size, W - 36 * mm - 60 * mm)
        while len(lines) > 2 and size > 12:
            size -= 0.5
            lines = simpleSplit(title, F_HEAD, size, W - 36 * mm - 60 * mm)
        c.setFillColor(white)
        c.setFont(F_HEAD, size)
        for ln in lines:
            c.drawString(18 * mm, y, ln)
            y -= size * 1.2
        y -= 5
    cl = data["client"]
    c.setFillColor(HexColor("#C8D4E6"))
    c.setFont(F_BODY_SB, 9)
    c.drawString(18 * mm, y, f"{client_label} {cl['company']}")
    c.setFillColor(HexColor("#8B97A8"))
    c.setFont(F_BODY, 8)
    c.drawString(18 * mm, y - 12, f"Contacto: {cl['contact']} — {cl['role']}")
    draw_star(c, W - 44 * mm, H - band / 2 - 3 * mm, 14 * mm)
    footer(c, W, H, demo=data.get("demo", False))
    c.restoreState()


def signature_block(data):
    W, H = A4
    half = (W - 36 * mm) / 2 - 6 * mm
    gap = 12 * mm
    sig = [
        [Paragraph("<b>Por PolluxData</b>", S["td_b"]), Paragraph("", S["td"]),
         Paragraph(f"<b>Por {data['client']['company']}</b>", S["td_b"])],
        [Paragraph(data["sender"]["name"], S["td"]), Paragraph("", S["td"]),
         Paragraph("", S["td"])],
        [Paragraph("Cargo: ____________________", S["td"]), Paragraph("", S["td"]),
         Paragraph("Nombre: ____________________", S["td"])],
        [Paragraph("Firma", S["note"]), Paragraph("", S["td"]),
         Paragraph("Firma", S["note"])],
        [Paragraph("", S["td"]), Paragraph("", S["td"]), Paragraph("", S["td"])],
        [Paragraph("Fecha: ______ / ______ / __________", S["td"]),
         Paragraph("", S["td"]),
         Paragraph("Fecha: ______ / ______ / __________", S["td"])],
    ]
    stg = Table(sig, colWidths=[half, gap, half])
    stg.setStyle(TableStyle([
        ("LINEBELOW", (0, 4), (0, 4), 0.9, NAVY),
        ("LINEBELOW", (2, 4), (2, 4), 0.9, NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, 1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return stg


def pricing_table(data, W):
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
    return t


def totals_block(sub, tax_rate):
    tax = round(sub * tax_rate / 100, 2)
    rows = [
        [Paragraph("Subtotal", S["td"]), Paragraph(fmt(sub), S["td_num"])],
        [Paragraph(f"IVA {tax_rate}%", S["td"]), Paragraph(fmt(tax), S["td_num"])],
        [Paragraph("<b>TOTAL</b>", ParagraphStyle("t", parent=S["td_b"], fontSize=9.5,
                     textColor=ORANGE)),
         Paragraph(f"<b>{fmt(sub + tax)}</b>", ParagraphStyle("tn", parent=S["td_num"],
                     fontSize=9.5, textColor=ORANGE))],
    ]
    tt = Table(rows, colWidths=[70 * mm, 32 * mm], hAlign="RIGHT")
    tt.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, ORANGE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tt, tax
