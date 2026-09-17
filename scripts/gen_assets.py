"""Generate uniform skill tiles + header SVGs for the GitHub profile README.

Usage: python scripts/gen_assets.py assets

Logos: Devicon (MIT) and Simple Icons (CC0), fetched from jsDelivr and embedded, so the
README depends on no third-party image service at view time.
"""
import re
import sys
from pathlib import Path
from urllib.request import urlopen

OUT = Path(sys.argv[1])
DEVICON = 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{0}/{0}-{1}.svg'
# Pinned: later Simple Icons releases removed Power BI and Excel at the brands' request.
SIMPLE = 'https://cdn.jsdelivr.net/npm/simple-icons@12.0.0/icons/{0}.svg'
LIGHT = '#E6EDF3'
MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

# key: (source, name, extra). extra = devicon variant, or monogram colour.
SKILLS = {
    'python': ('dev', 'python', 'original'), 'sql': ('mono', 'SQL', '#58A6FF'),
    'java': ('dev', 'java', 'original'), 'c': ('dev', 'c', 'original'), 'cpp': ('dev', 'cplusplus', 'original'),
    'kafka': ('dev', 'apachekafka', 'original'), 'airflow': ('dev', 'apacheairflow', 'original'),
    'parquet': ('si', 'apacheparquet', None),
    'aws': ('dev', 'amazonwebservices', 'original-wordmark'), 'terraform': ('dev', 'terraform', 'original'),
    'docker': ('dev', 'docker', 'original'), 'localstack': ('mono', 'LS', '#A78BFA'),
    'githubactions': ('dev', 'githubactions', 'original'),
    'pandas': ('dev', 'pandas', 'original'), 'numpy': ('dev', 'numpy', 'original'),
    'sklearn': ('dev', 'scikitlearn', 'original'), 'xgboost': ('mono', 'XGB', '#3FB0F0'),
    'tensorflow': ('dev', 'tensorflow', 'original'), 'keras': ('dev', 'keras', 'original'),
    'postgresql': ('dev', 'postgresql', 'original'), 'mysql': ('dev', 'mysql', 'original'),
    'duckdb': ('dev', 'duckdb', 'original'), 'powerbi': ('si', 'powerbi', None),
    'excel': ('si', 'microsoftexcel', None), 'jupyter': ('dev', 'jupyter', 'original'),
}
KEEP_DARK = {'duckdb'}  # logo carries its own light background; recolouring would invert it
SCALE = {'sklearn': 50, 'docker': 44}  # logos with built-in whitespace get a larger box
RECOLOUR = {'mysql': {'#00618A': '#4E9BCD', '#00618a': '#4E9BCD'}}  # brand blue too dark for a dark tile


def fetch(url):
    with urlopen(url, timeout=20) as r:
        return r.read().decode()


def luminance(hex_colour):
    h = hex_colour.lstrip('#')
    h = ''.join(c * 2 for c in h) if len(h) == 3 else h[:6]
    lin = [(v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4) for v in (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))]
    return .2126 * lin[0] + .7152 * lin[1] + .0722 * lin[2]


def lighten_darks(svg):
    # Near-black fills vanish on a dark tile (and in GitHub dark mode); swap them for light grey.
    return re.sub(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b', lambda m: LIGHT if luminance(m.group()) < .05 else m.group(), svg)


def inner(svg):
    svg = re.sub(r'<\?xml.*?\?>|<!--.*?-->', '', svg, flags=re.S)
    view_box = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', svg, flags=re.S).group(1)
    return view_box, body.strip()


def tile(content):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            '<rect x=".5" y=".5" width="63" height="63" rx="14" fill="#161B22" stroke="#30363D"/>'
            f'{content}</svg>\n')


def build_skill(key, source, name, extra, colours):
    if source == 'mono':
        size = 17 if len(name) <= 2 else 15
        return tile(f'<text x="32" y="{32 + size * .36:.1f}" text-anchor="middle" font-family="{MONO}" '
                    f'font-size="{size}" font-weight="700" fill="{extra}">{name}</text>')
    if source == 'si':
        view_box, body = inner(fetch(SIMPLE.format(name)))
        colour = '#' + colours[name]
        body = f'<g fill="{LIGHT if luminance(colour) < .05 else colour}">{body}</g>'
    else:
        view_box, body = inner(fetch(DEVICON.format(name, extra)))
        for old, new in RECOLOUR.get(key, {}).items():
            body = body.replace(old, new)
        if key not in KEEP_DARK:
            body = f'<g fill="{LIGHT}">{lighten_darks(body)}</g>'
    size = SCALE.get(key, 36)
    offset = (64 - size) / 2
    return tile(f'<svg x="{offset}" y="{offset}" width="{size}" height="{size}" viewBox="{view_box}">{body}</svg>')


def header(dark):
    c = dict(bg='#0D1117', grid='#161B22', border='#30363D', text='#E6EDF3', muted='#9198A1', faint='#6E7681',
             accent='#2DD4BF', node='#161B22') if dark else \
        dict(bg='#FFFFFF', grid='#F3F5F7', border='#D1D9E0', text='#1F2328', muted='#59636E', faint='#818B98',
             accent='#0F766E', node='#F6F8FA')
    pill = lambda x, y, w, label, colour=c['text'], stroke=c['border']: (
        f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="{c["node"]}" stroke="{stroke}"/>'
        f'<text x="{x + w / 2}" y="{y + 22}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{colour}">{label}</text>')
    arrow = lambda x1, y1, x2, y2: (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["faint"]}" stroke-width="1.5" '
                                    f'marker-end="url(#a)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="280" viewBox="0 0 1200 280">
<defs>
<pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['grid']}"/></pattern>
<marker id="a" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" fill="{c['faint']}"/></marker>
</defs>
<rect x=".5" y=".5" width="1199" height="279" rx="14" fill="{c['bg']}" stroke="{c['border']}"/>
<rect x="1" y="1" width="1198" height="278" rx="14" fill="url(#g)"/>
<text x="64" y="92" font-family="{MONO}" font-size="14" letter-spacing="2.5" fill="{c['accent']}">DATA ENGINEER · DATA ANALYST</text>
<text x="62" y="156" font-family="{SANS}" font-size="58" font-weight="700" letter-spacing="-1" fill="{c['text']}">Satyam Medya</text>
<text x="64" y="198" font-family="{SANS}" font-size="21" fill="{c['muted']}">Streaming, orchestrated ELT and cloud lakehouse pipelines.</text>
<text x="64" y="230" font-family="{MONO}" font-size="15" fill="{c['faint']}">tested · CI-checked · reproducible</text>
{pill(790, 86, 104, 'extract')}{arrow(896, 103, 918, 103)}
{pill(922, 86, 104, 'load')}{arrow(1028, 103, 1050, 103)}
{pill(1054, 86, 110, 'transform')}
{arrow(1109, 122, 1068, 160)}
{pill(930, 164, 170, 'quality gate ✓', c['accent'], c['accent'])}
{arrow(928, 181, 904, 181)}
{pill(790, 164, 112, 'warehouse')}
</svg>
'''


def main():
    colours = {'apacheparquet': '50ABF1', 'powerbi': 'F2C811', 'microsoftexcel': '217346'}  # Simple Icons brand hex
    (OUT / 'skills').mkdir(parents=True, exist_ok=True)
    for key, (source, name, extra) in SKILLS.items():
        (OUT / 'skills' / f'{key}.svg').write_text(build_skill(key, source, name, extra, colours), encoding='utf-8')
        print('ok', key)
    (OUT / 'header-dark.svg').write_text(header(True), encoding='utf-8')
    (OUT / 'header-light.svg').write_text(header(False), encoding='utf-8')
    print('ok headers')


if __name__ == '__main__':
    main()
