#!/usr/bin/env python3
"""Genera pollux-wordmark.svg: reconstrucción vectorial del wordmark P✦LLUX DATA.

Usa Michroma (OFL) como sustituta de la techno-sans original.
Uso: make_wordmark_svg.py [salida.svg]
"""
import sys
import tempfile
import urllib.request
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "logo" / "pollux-wordmark.svg"
MICHROMA_URL = ("https://raw.githubusercontent.com/google/fonts/main/"
                "ofl/michroma/Michroma-Regular.ttf")


def load_font():
    local = Path(tempfile.gettempdir()) / "Michroma.ttf"
    if not local.exists():
        urllib.request.urlretrieve(MICHROMA_URL, local)
    return TTFont(str(local))


def glyph_path(font, gs, name, x, y, scale):
    spen = SVGPathPen(gs)
    tpen = TransformPen(spen, (scale, 0, 0, -scale, x, y))
    tpen.addComponent = tpen.addComponent
    gs[name].draw(tpen)
    return spen.getCommands()


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    font = load_font()
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]

    def adv(ch):
        return hmtx[cmap[ord(ch)]][0]

    def bounds(ch):
        bp = BoundsPen(gs)
        gs[cmap[ord(ch)]].draw(bp)
        return bp.bounds

    cap = bounds("P")[3]
    scale = 1.0
    track = 0.06 * upm
    pad = 0.10 * cap

    x = 0.0
    parts = []
    x += adv("P") + 0.12 * cap

    k = cap * 0.95 / 100
    cx, cy = x + 50 * k, -cap / 2
    parts.append(
        f'<g stroke="#F05A24" stroke-width="{3.0 / (upm / 1000) * (upm / 1000):.1f}" '
        f'stroke-linecap="round" fill="none" transform="translate({cx:.1f},{cy:.1f}) '
        f'scale({k:.4f})">'
        '<line x1="0" y1="-46" x2="0" y2="46"/>'
        '<line x1="-46" y1="0" x2="46" y2="0"/>'
        '<line x1="-32.5" y1="-32.5" x2="32.5" y2="32.5"/>'
        '<line x1="32.5" y1="-32.5" x2="-32.5" y2="32.5"/>'
        '<circle cx="0" cy="0" r="22"/></g>')
    x += 100 * k + 0.12 * cap

    for ch in "LLUX":
        parts.append(glyph_path(font, gs, cmap[ord(ch)], x, 0, scale))
        x += adv(ch) + track

    line1_w = x
    s2 = 0.62
    y2 = s2 * cap + 0.22 * cap
    x2 = 0.0
    track2 = 0.14 * upm * 0.62
    for ch in "DATA":
        parts.append(glyph_path(font, gs, cmap[ord(ch)], x2, y2, s2))
        x2 += adv(ch) * s2 + track2
    line2_w = x2 - track2

    width = max(line1_w, line2_w) + 2 * pad
    height = cap + y2 + pad
    vb_y = -cap - pad

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{-pad:.0f} {vb_y:.0f} {width:.0f} {height:.0f}" '
        'fill="none" role="img" aria-label="PolluxData">\n'
        '  <g fill="#FFFFFF">\n    '
        + "\n    ".join(parts if False else
                        [p for p in parts if not p.startswith("<g stroke")])
        + "\n  </g>\n  "
        + next(p for p in parts if p.startswith("<g stroke"))
        + "\n</svg>\n"
    )
    out.write_text(svg)
    print(out)


if __name__ == "__main__":
    main()
