#!/usr/bin/env python3
"""Genera un informe de assessment PolluxData en PDF (modo Paper).

Uso: make_assessment.py <assessment.json> [salida.pdf]
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
)

SEV = {"alta": ORANGE, "media": NAVY, "baja": NAVY}


def build(data, out):
    W, H = A4
    doc = BaseDocTemplate(str(out), pagesize=A4,
                          title=f"Assessment {data['ref']} — {data['title']}",
                          author="PolluxData", subject="Informe de assessment",
                          leftMargin=18 * mm, rightMargin=18 * mm)
    cover_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 64 * mm - 32 * mm, id="cf")
    later_f = Frame(18 * mm, 24 * mm, W - 36 * mm, H - 24 * mm - 18 * mm, id="lf")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_f],
                     onPage=lambda c, d: band_cover(c, d, data, "INFORME DE ASSESSMENT",
                                                    title=data["title"])),
        PageTemplate(id="later", frames=[later_f],
                     onPage=lambda c, d: later_header(c, d, data, "INFORME DE ASSESSMENT")),
    ])

    st = [NextPageTemplate("later")]
    st.append(Spacer(1, 1))

    st += heading("01", "RESUMEN DE HALLAZGOS")
    rows = [[Paragraph("Área", S["th"]), Paragraph("Hallazgo", S["th"]),
             Paragraph("Severidad", S["th_num"])]]
    for f in data["findings"]:
        sev = f["severity"]
        rows.append([Paragraph(f["area"], S["td"]),
                     Paragraph(f["summary"], S["td"]),
                     Paragraph(f"<b>{sev.upper()}</b>",
                               S["td_num"] if sev != "alta" else
                               S["td_num"], )])
    t = Table(rows, colWidths=[30 * mm, (W - 36 * mm) - 30 * mm - 26 * mm, 26 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)
    st.append(Spacer(1, 4))
    n_high = sum(1 for f in data["findings"] if f["severity"] == "alta")
    st.append(Paragraph(
        f"<b>{len(data['findings'])} hallazgos</b> identificados, de ellos "
        f"<font color=\"#F07A1F\"><b>{n_high} de severidad alta</b></font>. "
        "El detalle y las recomendaciones siguen abajo.", S["body"]))

    st += heading("02", "ESTADO ACTUAL")
    for p in data["current_state"]:
        st.append(Paragraph(p, S["body"]))

    st += heading("03", "HALLAZGOS DETALLADOS")
    for i, f in enumerate(data["findings"], 1):
        color = "#F07A1F" if f["severity"] == "alta" else "#06111F"
        st.append(KeepTogether([
            Paragraph(f'<font color="{color}"><b>0{i} · {f["area"].upper()}</b></font>'
                      f'<font color="#5B6573">  ·  severidad {f["severity"]}</font>',
                      S["td_b"]),
            Paragraph(f["summary"], S["body"]),
            Paragraph(f"<b>Riesgo:</b> {f['risk']}", S["body"]),
            Spacer(1, 4),
        ]))

    st += heading("04", "RECOMENDACIONES")
    st += [Paragraph(f"<b>{i}.</b> {rec}", S["li"], bulletText="")
           for i, rec in enumerate(data["recommendations"], 1)]

    st += heading("05", "ROADMAP PROPUESTO")
    rows = [[Paragraph("Fase", S["th"]), Paragraph("Acción", S["th"]),
             Paragraph("Prioridad", S["th_num"])]]
    for r in data["roadmap"]:
        rows.append([Paragraph(r["phase"], S["td_b"]),
                     Paragraph(r["action"], S["td"]),
                     Paragraph(r["priority"], S["td_num"])])
    t = Table(rows, colWidths=[22 * mm, (W - 36 * mm) - 22 * mm - 24 * mm, 24 * mm])
    t.hAlign = "LEFT"
    t.setStyle(table_style())
    st.append(t)

    st += heading("06", "SIGUIENTES PASOS")
    st.append(Paragraph(data["next_steps"], S["body"]))
    st.append(Spacer(1, 4))
    st.append(Paragraph(
        f"Dudas sobre este informe: "
        f"<font color=\"#F07A1F\"><b>{data['sender']['email']}</b></font>", S["body"]))

    doc.build(st)


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")
    build(data, out)
    print(out)


if __name__ == "__main__":
    main()
