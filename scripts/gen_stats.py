"""Generate the stats strip (assets/stats-dark.svg, assets/stats-light.svg).

Usage: python scripts/gen_stats.py assets    (requires: pip install fonttools)

GitHub READMEs strip CSS, so the strip is an SVG image with the Geist typeface (SIL OFL 1.1)
subset and embedded; it renders identically on every OS. A light sweeps across the grid lines
using CSS animation, which browsers disable when the viewer prefers reduced motion.
"""
import base64
import io
import sys
from pathlib import Path
from urllib.request import urlopen

from fontTools import subset
from fontTools.ttLib import TTFont

OUT = Path(sys.argv[1])
FONTS = 'https://cdn.jsdelivr.net/npm/geist@1.7.2/dist/fonts/'
STATS = [('5', 'PIPELINES'), ('34', 'AUTOMATED TESTS'), ('5/5', 'REPOS TESTED IN CI'), ('0', 'CLOUD ACCOUNTS NEEDED')]
W, H, CELL = 1200, 220, 24


def embedded_font(path, text):
    font = TTFont(io.BytesIO(urlopen(FONTS + path, timeout=30).read()))
    options = subset.Options()
    options.flavor = 'woff'
    options.layout_features = ['tnum', 'kern']
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def strip(dark, number_font, label_font):
    c = dict(bg='#000000', grid='#161616', lit='#C8C8C8', rule='#2A2A2A', tick='#5C5C5C',
             number='#FAFAFA', dim='#5C5C5C', label='#8F8F8F', glow='#FFFFFF') if dark else \
        dict(bg='#FFFFFF', grid='#F0F0F0', lit='#6E6E6E', rule='#E3E3E3', tick='#A8A8A8',
             number='#0A0A0A', dim='#B0B0B0', label='#6B6B6B', glow='#000000')
    cells, ticks = [], []
    width = W / len(STATS)
    for i, (value, label) in enumerate(STATS):
        x = width * i + width / 2
        head, _, tail = value.partition('/')
        shown = f'{head}<tspan fill="{c["dim"]}">/</tspan>{tail}' if tail else value
        cells.append(f'<g class="stat" style="animation-delay:{.08 * i:.2f}s">'
                     f'<text x="{x:.0f}" y="122" class="n" text-anchor="middle">{shown}</text>'
                     f'<text x="{x:.0f}" y="164" class="l" text-anchor="middle">{label}</text></g>')
    for i in range(1, len(STATS)):
        x = width * i
        cells.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{H}" stroke="{c["rule"]}"/>')
    for x in [0] + [width * i for i in range(1, len(STATS))] + [W]:
        for y in (0, H):  # crosshair ticks where rules meet the frame
            ticks.append(f'<path d="M{x - 6:.1f} {y}H{x + 6:.1f}M{x:.1f} {y - 6}V{y + 6}" stroke="{c["tick"]}"/>')
    grid = f'<path d="{"".join(f"M{x} 0V{H}" for x in range(0, W + 1, CELL))}{"".join(f"M0 {y}H{W}" for y in range(0, H + 1, CELL))}" fill="none"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + 12}" viewBox="-6 -6 {W + 12} {H + 12}" role="img" aria-label="{', '.join(f'{v} {l.lower()}' for v, l in STATS)}">
<style>
@font-face{{font-family:GeistNum;src:url(data:font/woff;base64,{number_font}) format('woff')}}
@font-face{{font-family:GeistLabel;src:url(data:font/woff;base64,{label_font}) format('woff')}}
.n{{font:600 76px GeistNum,-apple-system,'Segoe UI',sans-serif;letter-spacing:-3px;fill:{c['number']};font-variant-numeric:tabular-nums}}
.l{{font:400 13px GeistLabel,ui-monospace,Consolas,monospace;letter-spacing:2.4px;fill:{c['label']}}}
.sweep{{animation:sweep 7s cubic-bezier(.45,0,.55,1) infinite alternate}}
.stat{{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}}
@keyframes sweep{{from{{transform:translateX(-120px)}}to{{transform:translateX(1320px)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.sweep,.stat{{animation:none}}}}
</style>
<defs>
<radialGradient id="spot"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{c['glow']}" stop-opacity=".12"/><stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/></radialGradient>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><g class="sweep"><ellipse cx="0" cy="{H / 2}" rx="280" ry="220" fill="url(#spot)"/></g></mask>
<clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="{c['bg']}"/>
<g clip-path="url(#frame)">
{grid} stroke="{c['grid']}"/>
<g mask="url(#m)">{grid} stroke="{c['lit']}"/></g>
<g class="sweep"><ellipse cx="0" cy="{H / 2}" rx="260" ry="200" fill="url(#glow)"/></g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{c['rule']}"/>
{''.join(cells)}
{''.join(ticks)}
</svg>
'''


def main():
    number_font = embedded_font('geist-sans/Geist-SemiBold.ttf', ''.join(v for v, _ in STATS) + '/')
    label_font = embedded_font('geist-mono/GeistMono-Regular.ttf', ''.join(l for _, l in STATS))
    for dark in (True, False):
        path = OUT / f'stats-{"dark" if dark else "light"}.svg'
        path.write_text(strip(dark, number_font, label_font), encoding='utf-8')
        print('ok', path.name, f'{path.stat().st_size / 1024:.1f} KB')


if __name__ == '__main__':
    main()
