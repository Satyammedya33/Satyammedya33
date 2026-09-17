"""Generate every panel the profile README renders (assets/*-dark.svg, *-light.svg).

Usage: python scripts/gen_readme.py assets    (requires: pip install fonttools)

GitHub strips CSS and JS from READMEs, so each section is an SVG image: a black/white line
grid, the Geist typeface (SIL OFL 1.1) subset and embedded per panel so it renders identically
everywhere, and a light that sweeps the grid via CSS animation (disabled for viewers who prefer
reduced motion). Logos come from Devicon (MIT) and Simple Icons (CC0), inlined for the same reason.

Panel text lives in CONTENT below: edit there, rerun, commit. Alt text for the README is printed
at the end so the page stays readable to screen readers and search engines.
"""
import base64
import io
import re
import sys
import textwrap
from pathlib import Path
from urllib.request import urlopen

from fontTools import subset
from fontTools.ttLib import TTFont

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'assets')
GEIST = 'https://cdn.jsdelivr.net/npm/geist@1.7.2/dist/fonts/'
DEVICON = 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{0}/{0}-{1}.svg'
# Pinned: later Simple Icons releases removed Power BI and Excel at the brands' request.
SIMPLE = 'https://cdn.jsdelivr.net/npm/simple-icons@12.0.0/icons/{0}.svg'

DARK = dict(bg='#000000', grid='#161616', lit='#C8C8C8', rule='#2A2A2A', tick='#5C5C5C',
            fg='#FAFAFA', body='#A8A8A8', dim='#8F8F8F', faint='#5C5C5C', chip='#0C0C0C', glow='#FFFFFF')
LIGHT = dict(bg='#FFFFFF', grid='#F0F0F0', lit='#6E6E6E', rule='#E3E3E3', tick='#A8A8A8',
             fg='#0A0A0A', body='#4A4A4A', dim='#6B6B6B', faint='#9A9A9A', chip='#FAFAFA', glow='#000000')
CELL = 24
LOGO_TILE = '#161B22'  # logo tiles keep a constant dark chip in both themes, like app icons


class Font:
    """Measures text and emits a base64 subset of only the characters a panel uses."""

    def __init__(self, path):
        self.raw = urlopen(GEIST + path, timeout=30).read()
        font = TTFont(io.BytesIO(self.raw))
        self.upem = font['head'].unitsPerEm
        self.cmap = font.getBestCmap()
        self.widths = font['hmtx'].metrics

    def width(self, text, size, tracking=0):
        total = 0
        for ch in text:
            name = self.cmap.get(ord(ch))
            total += self.widths[name][0] if name else self.upem // 2
        return total * size / self.upem + tracking * len(text)

    def subset_b64(self, chars):
        font = TTFont(io.BytesIO(self.raw))
        options = subset.Options()
        options.flavor = 'woff'
        options.layout_features = ['tnum', 'kern']
        sub = subset.Subsetter(options)
        sub.populate(text=''.join(sorted(chars)) or 'A')
        sub.subset(font)
        buf = io.BytesIO()
        font.save(buf)
        return base64.b64encode(buf.getvalue()).decode()


def wrap(text, font, size, max_width, tracking=0):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if line and font.width(trial, size, tracking) > max_width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + ([line] if line else [])


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Panel:
    """A grid panel: background grid, sweeping highlight, then text drawn on top."""

    def __init__(self, width, colours, fonts):
        self.w, self.c, self.fonts = width, colours, fonts
        self.body, self.used = [], set()

    def text(self, x, y, content, font='sans', size=14, colour=None, weight=None, anchor='start', tracking=0):
        self.used.update(content)
        key = font if weight is None else f'{font}-{weight}'
        style = [f'font-family:{self.fonts[key][0]}', f'font-size:{size}px', f'fill:{colour or self.c["fg"]}']
        if tracking:
            style.append(f'letter-spacing:{tracking}px')
        self.body.append(f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" style="{";".join(style)}">{esc(content)}</text>')
        return self.fonts[key][1].width(content, size, tracking)

    def rect(self, x, y, w, h, fill='none', stroke=None, rx=0):
        self.body.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{fill}"'
                         + (f' stroke="{stroke}"' if stroke else '') + '/>')

    def raw(self, markup):
        self.body.append(markup)

    def render(self, height, label, ticks_at=(), wash=.78):
        c, h = self.c, height
        grid = ('<path fill="none" d="'
                + ''.join(f'M{x} 0V{h}' for x in range(0, self.w + 1, CELL))
                + ''.join(f'M0 {y}H{self.w}' for y in range(0, int(h) + 1, CELL)) + '"')
        marks = ''.join(f'<path d="M{x - 6:g} {y}H{x + 6:g}M{x:g} {y - 6}V{y + 6}" stroke="{c["tick"]}"/>'
                        for x in ticks_at for y in (0, h))
        faces = ''.join(f'@font-face{{font-family:{name};src:url(data:font/woff;base64,{font.subset_b64(self.used)}) format("woff")}}'
                        for name, font in {n: f for n, f in self.fonts.values()}.items())
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h + 12:g}" viewBox="-6 -6 {self.w + 12} {h + 12:g}" role="img" aria-label="{esc(label)}">
<style>{faces}
.sweep{{animation:sweep 7s cubic-bezier(.45,0,.55,1) infinite alternate}}
@keyframes sweep{{from{{transform:translateX(-140px)}}to{{transform:translateX({self.w + 140}px)}}}}
@media (prefers-reduced-motion:reduce){{.sweep{{animation:none}}}}
</style>
<defs>
<radialGradient id="spot"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{c['glow']}" stop-opacity=".12"/><stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset=".55" stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg']}" stop-opacity="0"/></radialGradient>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.w}" height="{h:g}"><g class="sweep"><ellipse cx="0" cy="{h / 2:g}" rx="280" ry="{max(h, 160):g}" fill="url(#spot)"/></g></mask>
<clipPath id="frame"><rect width="{self.w}" height="{h:g}"/></clipPath>
</defs>
<rect width="{self.w}" height="{h:g}" fill="{c['bg']}"/>
<g clip-path="url(#frame)">{grid} stroke="{c['grid']}"/><g mask="url(#m)">{grid} stroke="{c['lit']}"/></g>
<g class="sweep"><ellipse cx="0" cy="{h / 2:g}" rx="260" ry="{max(h, 150):g}" fill="url(#glow)"/></g></g>
<rect width="{self.w}" height="{h:g}" fill="{c['bg']}" opacity="{wash}"/>
<rect x=".5" y=".5" width="{self.w - 1}" height="{h - 1:g}" fill="none" stroke="{c['rule']}"/>
{marks}
{''.join(self.body)}
</svg>
'''


# ---------------------------------------------------------------- logos

def logo_markup(spec):
    source, name, extra = spec
    if source == 'mono':
        return None, extra, name
    url = SIMPLE.format(name) if source == 'si' else DEVICON.format(name, extra)
    svg = urlopen(url, timeout=30).read().decode()
    view_box = svg.split('viewBox="')[1].split('"')[0]
    inner = svg[svg.index('>', svg.index('<svg')) + 1:svg.rindex('</svg>')].strip()
    if source == 'si':
        inner = f'<g fill="#{extra}">{inner}</g>'
    return view_box, inner, None


def luminance(hex_colour):
    h = hex_colour.lstrip('#')
    h = ''.join(ch * 2 for ch in h) if len(h) == 3 else h[:6]
    parts = [(v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4) for v in (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))]
    return .2126 * parts[0] + .7152 * parts[1] + .0722 * parts[2]


def lighten(svg):
    return re.sub(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b',
                  lambda m: '#E6EDF3' if luminance(m.group()) < .05 else m.group(), svg)


LOGOS = {
    'python': ('dev', 'python', 'original'), 'sql': ('mono', 'SQL', '#58A6FF'),
    'java': ('dev', 'java', 'original'), 'c': ('dev', 'c', 'original'), 'cpp': ('dev', 'cplusplus', 'original'),
    'kafka': ('dev', 'apachekafka', 'original'), 'airflow': ('dev', 'apacheairflow', 'original'),
    'parquet': ('si', 'apacheparquet', '50ABF1'), 'duckdb': ('dev', 'duckdb', 'original'),
    'aws': ('dev', 'amazonwebservices', 'original-wordmark'), 'terraform': ('dev', 'terraform', 'original'),
    'docker': ('dev', 'docker', 'original'), 'localstack': ('mono', 'LS', '#A78BFA'),
    'actions': ('dev', 'githubactions', 'original'),
    'pandas': ('dev', 'pandas', 'original'), 'numpy': ('dev', 'numpy', 'original'),
    'sklearn': ('dev', 'scikitlearn', 'original'), 'xgboost': ('mono', 'XGB', '#3FB0F0'),
    'tensorflow': ('dev', 'tensorflow', 'original'), 'keras': ('dev', 'keras', 'original'),
    'jupyter': ('dev', 'jupyter', 'original'), 'postgresql': ('dev', 'postgresql', 'original'),
    'mysql': ('dev', 'mysql', 'original'), 'powerbi': ('si', 'powerbi', 'F2C811'),
    'excel': ('si', 'microsoftexcel', '217346'),
}
KEEP_DARK = {'duckdb'}  # logo carries its own light background
LOGO_SCALE = {'sklearn': 1.35, 'docker': 1.2}  # logos with built-in whitespace
LOGO_FIX = {'mysql': [('#00618A', '#4E9BCD'), ('#00618a', '#4E9BCD')]}  # brand blue too dark on a dark tile
CAPTIONS = {'sql': 'SQL', 'cpp': 'C++', 'c': 'C', 'aws': 'AWS', 'actions': 'Actions', 'sklearn': 'scikit-learn',
            'parquet': 'Parquet', 'localstack': 'LocalStack', 'xgboost': 'XGBoost', 'powerbi': 'Power BI',
            'postgresql': 'PostgreSQL', 'duckdb': 'DuckDB', 'mysql': 'MySQL', 'tensorflow': 'TensorFlow'}


def draw_logo(panel, key, x, y, box=56):
    view_box, inner, mono = logo_markup(LOGOS[key])
    panel.rect(x, y, box, box, fill=LOGO_TILE, stroke='#30363D', rx=12)
    if view_box is None:  # monogram tile for logos that do not exist
        size = 15 if len(mono) > 2 else 17
        panel.used.update(mono)
        panel.raw(f'<text x="{x + box / 2:g}" y="{y + box / 2 + size * .36:g}" text-anchor="middle" '
                  f'style="font-family:{panel.fonts["mono"][0]};font-size:{size}px;font-weight:700;fill:{inner}">{mono}</text>')
        return
    for old, new in LOGO_FIX.get(key, []):
        inner = inner.replace(old, new)
    if key not in KEEP_DARK:
        inner = f'<g fill="#E6EDF3">{lighten(inner)}</g>'
    side = box * .58 * LOGO_SCALE.get(key, 1)
    off = (box - side) / 2
    panel.raw(f'<svg x="{x + off:g}" y="{y + off:g}" width="{side:g}" height="{side:g}" viewBox="{view_box}">{inner}</svg>')


# ---------------------------------------------------------------- content

CONTENT = dict(
    header=dict(eyebrow='DATA ENGINEER · DATA ANALYST', name='Satyam Medya',
                tagline='Streaming, orchestrated ELT and cloud lakehouse pipelines.',
                note='tested · CI-checked · reproducible',
                flow=[('extract', 'load', 'transform'), ('quality gate', 'warehouse')]),
    stats=[('5', 'PIPELINES'), ('34', 'AUTOMATED TESTS'), ('5/5', 'REPOS TESTED IN CI'), ('0', 'CLOUD ACCOUNTS NEEDED')],
    stack=[('LANGUAGES', ['python', 'sql', 'java', 'c', 'cpp'], ''),
           ('DATA ENGINEERING', ['kafka', 'airflow', 'parquet', 'duckdb'],
            'ETL / ELT design · dbt-style SQL modelling · star-schema warehousing · data-quality validation'),
           ('CLOUD & DEVOPS', ['aws', 'terraform', 'docker', 'localstack', 'actions'], 'S3 · Glue · Athena · IAM'),
           ('DATA & ML', ['pandas', 'numpy', 'sklearn', 'xgboost', 'tensorflow', 'keras', 'jupyter'], ''),
           ('DATABASES & BI', ['postgresql', 'mysql', 'powerbi', 'excel'],
            'Security: LLM prompt-injection red-teaming · network intrusion detection · applied ML for security')],
    cards=[
        dict(key='airflow', title='Airflow ELT Warehouse',
             desc='Orchestrated ELT from raw operational data to a PostgreSQL star schema.',
             flow='extract → load → SQL models → quality gate',
             points=['3 dimensions + 1 fact table built by dependency-ordered, dbt-style SQL models',
                     'Final DAG task runs not-null, unique, range and referential-integrity checks, and fails the run on any violation',
                     'Source data deliberately contains invalid rows, so the gate is tested against real failures'],
             stack='AIRFLOW · POSTGRESQL · SQL · DOCKER COMPOSE · 7 TESTS'),
        dict(key='retail', title='Real-Time Retail Analytics',
             desc='Event streaming with live metrics and in-flight anomaly detection.',
             flow='Kafka → 60s windows → z-score → Postgres',
             points=['Revenue, order count and average order value per 60-second tumbling window',
                     'Rolling z-score flags anomalous order amounts as they stream through',
                     'Windowing and scoring are pure functions, unit-tested without a broker; full stack runs in Docker Compose'],
             stack='KAFKA · POSTGRESQL · STREAMLIT · DOCKER COMPOSE · 8 TESTS'),
        dict(key='lakehouse', title='AWS Data Lakehouse',
             desc='Medallion lakehouse for IoT telemetry and clickstream events.',
             flow='bronze → silver → gold → DuckDB SQL',
             points=['Terraform: versioned, encrypted S3 with public access blocked, lifecycle rules, Glue catalog, least-privilege IAM role',
                     'Same code runs on local disk, LocalStack or real S3, switched by one environment variable',
                     'Silver layer types data into Parquet and drops faulty sensor readings'],
             stack='TERRAFORM · AWS · PARQUET · DUCKDB · LOCALSTACK · 3 TESTS'),
        dict(key='llm', title='LLM Red-Team Framework',
             desc='Defensive harness measuring how well an LLM resists manipulation.',
             flow='probes → target → canary scoring → report',
             points=['12 probes across 7 categories: prompt injection, jailbreaks, system-prompt extraction and more',
                     'Deterministic canary-token and refusal-pattern scoring, with no LLM judge in the loop',
                     'Reference reports in the repo: safe target 100% robust, leaky target 34%; adapters for OpenAI, Anthropic and an offline mock'],
             stack='PYTHON · OPENAI / ANTHROPIC APIS · YAML · 9 TESTS'),
        dict(key='ids', title='ML Intrusion Detection',
             desc='Classifies network flows as Normal, DoS, Probe or R2L.',
             flow='flows → features → RF / XGBoost → metrics',
             points=['Random Forest and XGBoost compared on NSL-KDD-style flow features',
                     'Per-class precision, recall and F1, confusion matrix and ROC-AUC, because a missed attack costs more than a false alarm',
                     'Data source isolated in one module, ready to swap the synthetic generator for real NSL-KDD or CICIDS2017'],
             stack='SCIKIT-LEARN · XGBOOST · PANDAS · STREAMLIT · 7 TESTS'),
    ],
    principles=dict(title='HOW I BUILD', items=[
        ('Every push is tested.', 'pytest runs in GitHub Actions on each push.'),
        ('Data quality is a gate, not a report.', 'Bad data stops the pipeline before it reaches consumers.'),
        ('Infrastructure is code.', 'Cloud resources are declared in Terraform, not clicked together.'),
        ('Anyone can run it.', 'Docker Compose, LocalStack and mock adapters mean no cloud bill or API key to evaluate the work.'),
        ('Honest data.', 'Where data is synthetic, the README says so.'),
    ]),
    education=dict(title='EDUCATION', school='Vellore Institute of Technology',
                   degree='B.Tech, Computer Science & Engineering (Data Science) · 2021 – 2026',
                   coursework='Data Structures & Algorithms · DBMS · Operating Systems · Computer Networks · Statistics & Probability',
                   certs='Certifications: Advanced Machine Learning & Python Bootcamp · IoT Architecture (VIT)'),
)


# ---------------------------------------------------------------- panels

def header_panel(c, fonts):
    d = CONTENT['header']
    p = Panel(1200, c, fonts)
    p.raw(f'<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
          f'<path d="M0 0L8 4L0 8z" fill="{c["faint"]}"/></marker></defs>')
    p.text(48, 84, d['eyebrow'], 'mono', 13, c['dim'], tracking=2.6)
    p.text(46, 168, d['name'], 'sans', 70, c['fg'], weight=600, tracking=-2.5)
    p.text(48, 212, d['tagline'], 'sans', 20, c['body'])
    p.text(48, 246, d['note'], 'mono', 13, c['dim'], tracking=1.2)
    for y, labels in ((96, d['flow'][0]), (176, d['flow'][1])):
        widths = [p.fonts['mono'][1].width(t, 12.5, 1) + 44 for t in labels]
        x = 1152 - sum(widths) - 22 * (len(labels) - 1)
        for i, (label, width) in enumerate(zip(labels, widths)):
            bright = label.startswith('quality')
            p.rect(x, y, width, 34, fill=c['chip'], stroke=c['fg'] if bright else c['rule'], rx=17)
            p.text(x + width / 2, y + 22, label, 'mono', 12.5, c['fg'] if bright else c['body'], anchor='middle', tracking=1)
            if i < len(labels) - 1:
                p.raw(f'<path d="M{x + width + 5:g} {y + 17}h11" stroke="{c["faint"]}" marker-end="url(#arrow)"/>')
            x += width + 22
    label = f"{d['name']} — data engineer and data analyst. {d['tagline']} {d['note']}"
    return p.render(300, label)


def stats_panel(c, fonts):
    stats = CONTENT['stats']
    p, h = Panel(1200, c, fonts), 220
    width = p.w / len(stats)
    for i, (value, label) in enumerate(stats):
        x = width * i + width / 2
        p.raw(f'<ellipse cx="{x:g}" cy="{h / 2 + 8:g}" rx="{width * .5:g}" ry="78" fill="url(#halo)"/>')
        if '/' in value:
            head, tail = value.split('/')
            total = p.fonts['sans-600'][1].width(value, 76, -3)
            p.text(x - total / 2, 122, head, 'sans', 76, c['fg'], weight=600, tracking=-3)
            p.text(x - total / 2 + p.fonts['sans-600'][1].width(head, 76, -3), 122, '/', 'sans', 76, c['faint'], weight=600, tracking=-3)
            p.text(x + total / 2, 122, tail, 'sans', 76, c['fg'], weight=600, tracking=-3, anchor='end')
        else:
            p.text(x, 122, value, 'sans', 76, c['fg'], weight=600, tracking=-3, anchor='middle')
        p.text(x, 164, label, 'mono', 13, c['dim'], anchor='middle', tracking=2.4)
    for i in range(1, len(stats)):
        p.raw(f'<line x1="{width * i:g}" y1="0" x2="{width * i:g}" y2="{h}" stroke="{c["rule"]}"/>')
    label = ', '.join(f'{v} {l.lower()}' for v, l in stats)
    return p.render(h, label, ticks_at=[0] + [width * i for i in range(1, len(stats))] + [p.w], wash=0)


def stack_panel(c, fonts):
    rows = CONTENT['stack']
    p = Panel(1200, c, fonts)
    row_h, top, tile, gap, tiles_x = 104, 56, 56, 80, 250
    p.text(36, 44, 'TECH STACK', 'mono', 12.5, c['dim'], tracking=2.4)
    for r, (category, keys, extra) in enumerate(rows):
        y = top + r * row_h
        p.text(36, y + tile / 2 + 5, category, 'mono', 12.5, c['dim'], tracking=2)
        for i, key in enumerate(keys):
            x = tiles_x + i * gap
            draw_logo(p, key, x, y, tile)
            p.text(x + tile / 2, y + tile + 18, CAPTIONS.get(key, key.capitalize()), 'mono', 10.5, c['body'], anchor='middle')
        if extra:
            x = tiles_x + len(keys) * gap + 16
            for j, line in enumerate(wrap(extra, p.fonts['sans'][1], 12.5, p.w - x - 36)[:3]):
                p.text(x, y + 26 + j * 19, line, 'sans', 12.5, c['body'])
        if r < len(rows) - 1:
            p.raw(f'<line x1="0" y1="{y + row_h - 24:g}" x2="{p.w}" y2="{y + row_h - 24:g}" stroke="{c["rule"]}"/>')
    label = 'Tech stack. ' + ' '.join(
        f'{cat.title()}: {", ".join(CAPTIONS.get(k, k.capitalize()) for k in keys)}. {extra}' for cat, keys, extra in rows)
    return p.render(top + len(rows) * row_h, label)


def card_panel(card, c, fonts):
    p, pad = Panel(600, c, fonts), 30
    inner = p.w - pad * 2
    y = 52
    p.text(pad, y, card['title'], 'sans', 24, c['fg'], weight=600, tracking=-.5)
    y += 30
    for line in wrap(card['desc'], p.fonts['sans'][1], 14.5, inner):
        p.text(pad, y, line, 'sans', 14.5, c['body'])
        y += 21
    y += 8
    flow_w = min(p.fonts['mono'][1].width(card['flow'], 12.5, .6) + 28, inner)
    p.rect(pad, y, flow_w, 32, fill=c['chip'], stroke=c['rule'], rx=6)
    p.text(pad + 14, y + 21, card['flow'], 'mono', 12.5, c['fg'], tracking=.6)
    y += 54
    for point in card['points']:
        p.raw(f'<path d="M{pad + 1} {y - 5}h7" stroke="{c["faint"]}" stroke-width="1.5"/>')
        for line in wrap(point, p.fonts['sans'][1], 13.5, inner - 18):
            p.text(pad + 18, y, line, 'sans', 13.5, c['body'])
            y += 19
        y += 7
    y += 4
    p.text(pad, y, card['stack'], 'mono', 10.5, c['dim'], tracking=1.1)
    label = f"{card['title']}: {card['desc']} Pipeline: {card['flow']}. " + ' '.join(card['points']) + f" Stack: {card['stack'].title()}."
    return p.render(y + 24, label)


def principles_panel(c, fonts):
    d = CONTENT['principles']
    p, pad = Panel(600, c, fonts), 30
    p.text(pad, 52, d['title'], 'mono', 12.5, c['dim'], tracking=2.4)
    y = 90
    for lead, detail in d['items']:
        p.raw(f'<path d="M{pad + 1} {y - 5}h7" stroke="{c["faint"]}" stroke-width="1.5"/>')
        p.text(pad + 18, y, lead, 'sans', 14, c['fg'], weight=600)
        y += 20
        for line in wrap(detail, p.fonts['sans'][1], 13.5, p.w - pad * 2 - 18):
            p.text(pad + 18, y, line, 'sans', 13.5, c['body'])
            y += 19
        y += 10
    label = d['title'].title() + '. ' + ' '.join(f'{lead} {detail}' for lead, detail in d['items'])
    return p.render(y + 6, label)


def education_panel(c, fonts):
    d = CONTENT['education']
    p, pad = Panel(1200, c, fonts), 36
    p.text(pad, 50, d['title'], 'mono', 12.5, c['dim'], tracking=2.4)
    p.text(pad, 94, d['school'], 'sans', 20, c['fg'], weight=600, tracking=-.4)
    p.text(pad, 122, d['degree'], 'sans', 14.5, c['body'])
    p.text(pad, 154, d['coursework'], 'sans', 13, c['body'])
    p.text(pad, 186, d['certs'], 'sans', 13, c['body'])
    return p.render(212, f"{d['title'].title()}. {d['school']}. {d['degree']}. Coursework: {d['coursework']}. {d['certs']}")


PANELS = {'header': header_panel, 'stats': stats_panel, 'stack': stack_panel,
          'principles': principles_panel, 'education': education_panel}


def main():
    fonts = {'sans': ('GeistSans', Font('geist-sans/Geist-Regular.ttf')),
             'sans-600': ('GeistBold', Font('geist-sans/Geist-SemiBold.ttf')),
             'mono': ('GeistMono', Font('geist-mono/GeistMono-Regular.ttf'))}
    OUT.mkdir(parents=True, exist_ok=True)
    alts = {}
    for theme, colours in (('dark', DARK), ('light', LIGHT)):
        for name, build in PANELS.items():
            svg = build(colours, fonts)
            (OUT / f'{name}-{theme}.svg').write_text(svg, encoding='utf-8')
            alts[name] = svg.split('aria-label="')[1].split('"')[0]
            print('ok', f'{name}-{theme}.svg', f'{len(svg) / 1024:.0f} KB')
        for card in CONTENT['cards']:
            svg = card_panel(card, colours, fonts)
            (OUT / f"card-{card['key']}-{theme}.svg").write_text(svg, encoding='utf-8')
            alts[card['key']] = svg.split('aria-label="')[1].split('"')[0]
            print('ok', f"card-{card['key']}-{theme}.svg", f'{len(svg) / 1024:.0f} KB')
    print('\n--- alt text for README ---')
    for name, alt in alts.items():
        print(f'\n[{name}]\n' + textwrap.fill(alt, 110))


if __name__ == '__main__':
    main()
