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


def footer(c, W, H):
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
    footer(c, W, H)
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
