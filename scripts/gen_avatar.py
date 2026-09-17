"""Avatar variants drawn in GitHub's own design language (Primer).

Usage: python gen_avatar_gh.py <flat|accent|contrib> out.svg

Primer colours (canvas #0D1117, border #30363D, accent #58A6FF, contribution greens) and
GitHub's Mona Sans (SIL OFL 1.1, embedded from @fontsource). Full-bleed square because
GitHub crops avatars to a circle.
"""
import base64
import sys
from pathlib import Path
from urllib.request import urlopen

SIZE = 1024
MONOGRAM = 'SM'
FONT = 'https://cdn.jsdelivr.net/npm/@fontsource/mona-sans/files/mona-sans-latin-600-normal.woff2'
CANVAS, SUBTLE, BORDER, MUTED = '#0D1117', '#161B22', '#30363D', '#8B949E'
FG, ACCENT = '#F0F6FC', '#58A6FF'
GREENS = ['#0E4429', '#006D32', '#26A641', '#39D353']


def font_b64():
    return base64.b64encode(urlopen(FONT, timeout=30).read()).decode()


def circle(cx, cy, r):
    return f'M{cx - r} {cy}a{r} {r} 0 1 0 {r * 2} 0a{r} {r} 0 1 0 {-r * 2} 0Z'


def variant_layers(kind, cx, cy):
    """Extra artwork per variant, plus the monogram's vertical nudge."""
    if kind == 'flat':
        return '', 0
    if kind == 'accent':
        return (f'<circle cx="{cx}" cy="{cy}" r="470" fill="none" stroke="{ACCENT}" stroke-opacity=".9"'
                f' stroke-width="10" stroke-linecap="round" stroke-dasharray="360 2954" transform="rotate(-128 {cx} {cy})"/>'), 0
    # contrib: a strip of contribution cells under the monogram
    # Fewer, larger, brighter cells so the strip still reads at 20px.
    cells, cell, gap = [], 62, 16
    cols, rows = 5, 2
    total_w = cols * cell + (cols - 1) * gap
    x0, y0 = cx - total_w / 2, cy + 104
    pattern = [[2, 3, 1, 3, 2], [3, 1, 3, 2, 3]]
    for r in range(rows):
        for c in range(cols):
            level = pattern[r][c]
            x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
            cells.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="13"'
                         f' fill="{GREENS[level]}" fill-opacity="{.62 + .13 * level:.2f}"/>'
                         f'<path d="M{x + 13:.0f} {y + 2:.0f}h{cell - 26}" stroke="#FFFFFF" stroke-opacity=".22" stroke-width="3" stroke-linecap="round"/>'
                         f'<path d="M{x + 13:.0f} {y + cell - 2:.0f}h{cell - 26}" stroke="#000000" stroke-opacity=".28" stroke-width="3" stroke-linecap="round"/>')
    return f'<g filter="url(#cellLift)">{"".join(cells)}</g>', -86


def icon(kind):
    cx = cy = SIZE / 2
    extra, nudge = variant_layers(kind, cx, cy)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
<defs>
<style>@font-face{{font-family:MonaSans;src:url(data:font/woff2;base64,{font_b64()}) format("woff2");font-weight:600}}</style>
<radialGradient id="lift" cx=".5" cy=".12" r=".85">
  <stop offset="0" stop-color="{SUBTLE}"/><stop offset="1" stop-color="{CANVAS}"/>
</radialGradient>
<pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">
  <path d="M64 0H0V64" fill="none" stroke="{BORDER}" stroke-opacity=".55"/>
</pattern>
<linearGradient id="rimTop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<linearGradient id="rimFoot" x1="0" y1="0" x2="0" y2="1">
  <stop offset=".6" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/>
</linearGradient>
<linearGradient id="markFace" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#C9D1D9"/>
</linearGradient>
<mask id="rimTopMask"><rect width="{SIZE}" height="{SIZE}" fill="url(#rimTop)"/></mask>
<mask id="rimFootMask"><rect width="{SIZE}" height="{SIZE}" fill="url(#rimFoot)"/></mask>
<filter id="cellLift" x="-20%" y="-20%" width="140%" height="160%">
  <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#000000" flood-opacity=".5"/>
</filter>
<filter id="markLift" x="-20%" y="-30%" width="140%" height="180%">
  <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#000000" flood-opacity=".55"/>
</filter>
<mask id="fade"><radialGradient id="fadeg" cx=".5" cy=".5" r=".5">
  <stop offset=".55" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</radialGradient><rect width="{SIZE}" height="{SIZE}" fill="url(#fadeg)"/></mask>
</defs>
<rect width="{SIZE}" height="{SIZE}" fill="url(#lift)"/>
<rect width="{SIZE}" height="{SIZE}" fill="url(#grid)" mask="url(#fade)"/>
<path d="{circle(cx, cy, 497)}" fill="none" stroke="{BORDER}" stroke-width="6"/>
<path d="{circle(cx, cy, 494)}" fill="none" stroke="#FFFFFF" stroke-opacity=".16" stroke-width="7" mask="url(#rimTopMask)"/>
<path d="{circle(cx, cy, 494)}" fill="none" stroke="#000000" stroke-opacity=".5" stroke-width="9" mask="url(#rimFootMask)"/>
{extra}
<text x="{cx}" y="{cy + 122 + nudge}" text-anchor="middle" fill="url(#markFace)" filter="url(#markLift)"
      style="font-family:MonaSans;font-weight:600;font-size:372px;letter-spacing:-16px">{MONOGRAM}</text>
</svg>
'''


if __name__ == '__main__':
    kind, out = sys.argv[1], Path(sys.argv[2])
    out.write_text(icon(kind), encoding='utf-8')
    print('wrote', out, f'{out.stat().st_size / 1024:.1f} KB')
