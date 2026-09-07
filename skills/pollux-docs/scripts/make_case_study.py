#!/usr/bin/env python3
"""Genera un caso de éxito PolluxData en PDF (modo Paper).

Uso: make_case_study.py <caso.json> [salida.pdf]
"""
import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

from common import (
    LINE, NAVY, ORANGE, S, A4, band_cover, heading, later_header,
)


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Caso de éxito — {data['title']}",
                          author="PolluxData", subject="Caso de éxito",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 64 * mm - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: band_cover(c, d, data, "CASO DE ÉXITO",
                                                    title=data["title"],
                                                    client_label="Cliente:")),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "CASO DE ÉXITO")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "EL DESAFÍO")
    st.append(Paragraph(data["challenge"], S["body"]))

    st += heading("02", "LA SOLUCIÓN")
    st.append(Paragraph(data["solution"], S["body"]))

    st += heading("03", "RESULTADOS")
    cells = []
    for m in data["metrics"]:
        cells.append([
            Paragraph(f"<b>{m['value']}</b>", S["metric"]),
            Paragraph(m["label"], S["td_b"]),
        ])
    mt = Table([cells], colWidths=[(W - 36 * mm) / 3] * 3)
    mt.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, ORANGE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    st.append(mt)
    st.append(Spacer(1, 6))

    if data.get("detail_rows"):
        rows = [[Paragraph("Indicador", S["th"]), Paragraph("Antes", S["th_num"]),
                 Paragraph("Después", S["th_num"])]]
        for r in data["detail_rows"]:
            rows.append([Paragraph(r["k"], S["td"]),
                         Paragraph(r["before"], S["td_num"]),
                         Paragraph(r["after"], S["td_num"])])
        t = Table(rows, colWidths=[(W - 36 * mm) - 56 * mm, 28 * mm, 28 * mm])
        t.hAlign = "LEFT"
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#F6F7FB")]),
            ("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]))
        st.append(t)

    st += heading("04", "QUÉ DICEN")
    st.append(KeepTogether([
        Paragraph(
            f"<font color=\"#F07A1F\" size=18><b>—</b></font> "
            f"<font size=11.5 color=\"#06111F\"><b>{data['quote']}</b></font>",
            S["body"]),
        Spacer(1, 3),
        Paragraph(f"<font color=\"#A9B0BD\">{data['quote_author']}</font>", S["body"]),
        Spacer(1, 6),
        Paragraph(
            "Cuéntanos tu caso: "
            f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font> · "
            "polluxdata.com", S["body"]),
    ]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
