# Generates the animated SVG assets for the GitHub profile README.
# Text is converted to vector paths (fonts can't load inside <img> SVGs on GitHub),
# so the typography matches the portfolio exactly: Inter Tight, Instrument Serif
# italic and JetBrains Mono.
import base64, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# Layout (repo root = parent of scripts/):
#   scripts/gen_profile.py   this file
#   scripts/fonts/           OFL fonts from Google Fonts
#   scripts/shots/           app screenshots embedded in the work cards
#   assets/                  generated SVGs (committed)
# Run locally: python scripts/gen_profile.py  (uses GITHUB_TOKEN / GH_TOKEN, else `gh auth token`)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, 'fonts')
SHOTS = os.path.join(HERE, 'shots')
OUT = os.path.join(ROOT, 'assets')
LOGIN = 'AbdelkaderBarhoumi21'
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- fonts
def num(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s

class Face:
    def __init__(self, file, wght=None):
        f = TTFont(os.path.join(FONTS, file))
        if wght and 'fvar' in f:
            f = instancer.instantiateVariableFont(f, {'wght': wght})
        self.gs = f.getGlyphSet()
        self.cmap = f.getBestCmap()
        self.upm = f['head'].unitsPerEm
        self.hmtx = f['hmtx']

    def _glyph(self, ch):
        return self.cmap.get(ord(ch)) or self.cmap.get(ord('?'))

    def width(self, text, size, track=0.0):
        s = size / self.upm
        w = sum(self.hmtx[self._glyph(c)][0] * s + track * size for c in text)
        return w - (track * size if text else 0)

    def d(self, text, size, x, y, track=0.0):
        s = size / self.upm
        pen = SVGPathPen(self.gs, ntos=num)
        cx = 0.0
        for c in text:
            g = self._glyph(c)
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + cx, y)))
            cx += self.hmtx[g][0] * s + track * size
        return pen.getCommands()

DISP = Face('InterTight.ttf', 500)
BODY = Face('InterTight.ttf', 400)
SEMI = Face('InterTight.ttf', 600)
SERIF = Face('InstrumentSerif-Italic.ttf')
MONO = Face('JetBrainsMono.ttf', 400)
MONOM = Face('JetBrainsMono.ttf', 500)

def text(face, s, size, x, y, fill, track=0.0, anchor='start', attrs=''):
    w = face.width(s, size, track)
    if anchor == 'end':
        x -= w
    elif anchor == 'middle':
        x -= w / 2
    return f'<path d="{face.d(s, size, x, y, track)}" fill="{fill}" {attrs}/>', w

def label(s, size, x, y, fill, anchor='start', face=MONO, attrs=''):
    return text(face, s.upper(), size, x, y, fill, 0.14, anchor, attrs)

def wrap(face, s, size, maxw):
    lines, cur = [], ''
    for word in s.split():
        t = (cur + ' ' + word).strip()
        if face.width(t, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def mixed(parts, size, x, y, fill, serif_fill=None):
    """Heading made of plain + `serif` italic segments. Returns (svg, width)."""
    out, cx = [], x
    for s, is_serif in parts:
        face = SERIF if is_serif else DISP
        sz = size * 1.06 if is_serif else size
        tr = -0.02 if is_serif else -0.045
        svg, w = text(face, s, sz, cx, y, (serif_fill or fill) if is_serif else fill, tr)
        out.append(svg)
        cx += w
    return ''.join(out), cx - x

def b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

def write(name, body):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(body)
    print(f'{name:28} {os.path.getsize(os.path.join(OUT, name)) // 1024:>4} KB')

# ---------------------------------------------------------------- palette
INK, SURF, RAISED = '#09090B', '#16161A', '#111114'
TEXT, DIM, FAINT = '#EDEDF0', '#9C9CA8', '#5C5C68'
PAPER, PAPER_TEXT, PAPER_DIM, PAPER_FAINT = '#EEEDE8', '#0E0E11', '#55555E', '#8D8D95'
VIOLET, CYAN, GREEN = '#6C63FF', '#00D9FF', '#3DDC97'
TONES = {'violet': VIOLET, 'cyan': CYAN, 'gold': '#F2C46D', 'orange': '#FF6B2C', 'blue': '#4D86FF'}
EASE = 'cubic-bezier(.16,1,.3,1)'
EASE_IO = 'cubic-bezier(.76,0,.24,1)'

BASE_CSS = f'''
.rise{{animation:rise 1.5s {EASE} both;transform-box:fill-box;transform-origin:left top}}
.fade{{animation:fade 1.4s ease both}}
.draw{{animation:draw 1.6s {EASE_IO} both;transform-box:fill-box;transform-origin:left center}}
.float{{animation:float 7s ease-in-out infinite}}
.drift{{animation:drift 18s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
.pulse{{animation:pulse 2.2s ease-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes rise{{from{{transform:translateY(115%) rotate(3deg)}}to{{transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
@keyframes drift{{0%,100%{{transform:translate(0,0) scale(1)}}33%{{transform:translate(-50px,30px) scale(1.08)}}66%{{transform:translate(30px,-20px) scale(.95)}}}}
@keyframes pulse{{0%{{opacity:.9;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
'''

def delay(ms):
    return f'style="animation-delay:{ms}ms"'

GRAIN = ('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 1 0 0 0 0"/></filter>')

def svg(w, h, defs, body, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs><style>{BASE_CSS}{css}</style>{defs}</defs>{body}</svg>')

def card_frame(w, h, fill, rx=28, stroke_op=.08):
    defs = f'<clipPath id="card"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
    head = f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{fill}"/>'
    tail = (f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".05"/></g>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity="{stroke_op}"/>')
    return defs + GRAIN, head, tail

# AB monogram (same paths as the portfolio BrandMark), viewBox 640 1140 2720 1720
AB_PATHS = [
    'M2653.652,2828.257h249.704c231.174,0,420.312-189.139,420.312-420.311c0-94.366-31.516-181.726-84.543-252.078c-26.72-35.45-58.903-66.58-95.268-92.111c-43.229,45.323-95.27,82.158-153.281,107.761c10.292,3.826,20.272,8.306,29.889,13.391c80.082,42.351,134.97,126.595,134.97,223.037c0,138.644-113.445,252.078-252.08,252.078h-89.86h-256.973L2653.652,2828.257z',
    'M1388.119,1931.875l194.658-337.155l147.078-254.745l-97.13-168.232l-480.176,831.688c60.874-37.902,130.358-62.097,203.679-69.781C1367.007,1932.52,1377.54,1932.061,1388.119,1931.875',
    'M1877.257,1931.748l-341.661-591.771l97.13-168.234l438.791,760.005H1877.257z M2394.861,2828.257l-267.338-463.04l-88.601-153.459h194.258l355.938,616.5H2394.861z',
    'M1384.934,2155.868h1414.597c231.174,0,420.311-189.139,420.311-420.311c0-94.366-31.516-181.726-84.542-252.078c-35.99-47.748-81.889-87.66-134.567-116.609c-49.912-27.427-105.911-45.013-165.335-50.096c-11.827-1.011-23.789-1.527-35.866-1.527H1780.112l97.13,168.232c372.183,0,550.107,0,922.29,0c42.201,0,82.067,10.51,117.109,29.041c80.082,42.351,134.97,126.595,134.97,223.038c0,138.644-113.448,252.078-252.079,252.078H1410.88c-17.175,0-31.42-0.224-48.828,1.598c-129.593,13.581-251.357,86.686-321.113,207.508l-364.605,631.515H870.59l316.041-547.399C1229.489,2206.624,1305.087,2162.419,1384.934,2155.868',
]

def ab_mark(x, y, width, fill):
    s = width / 2720
    return (f'<g transform="translate({num(x)} {num(y)}) scale({s:.5f}) translate(-640 -1140)" fill="{fill}">'
            + ''.join(f'<path d="{p}"/>' for p in AB_PATHS) + '</g>')

def arrow(x, y, size, color, sw=2):
    """↗ arrow drawn with strokes, (x, y) = bottom-left."""
    return (f'<g fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{num(x)} {num(y)}L{num(x+size)} {num(y-size)}"/>'
            f'<path d="M{num(x+size*.3)} {num(y-size)}H{num(x+size)}V{num(y-size*.3)}"/></g>')

def sparkle(cx, cy, r, color):
    import math
    segs = []
    for k in range(8):
        a = k * math.pi / 4
        r1 = r * (0.35 if k % 2 == 0 else 0.45)
        r2 = r if k % 2 == 0 else r * 0.75
        segs.append(f'M{num(cx+r1*math.cos(a))} {num(cy+r1*math.sin(a))}L{num(cx+r2*math.cos(a))} {num(cy+r2*math.sin(a))}')
    return f'<path d="{"".join(segs)}" stroke="{color}" stroke-width="{num(r*0.18)}" stroke-linecap="round" fill="none"/>'

# ================================================================ HEADER
def header():
    W, H = 1200, 520
    defs, head, tail = card_frame(W, H, INK)
    defs += (f'<radialGradient id="ov"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="oc"><stop offset="0" stop-color="{CYAN}" stop-opacity=".32"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="nm" x1="0" x2="1"><stop offset=".2" stop-color="{TEXT}"/><stop offset="1" stop-color="#A49EFF"/></linearGradient>'
             f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
             '<clipPath id="l1"><rect x="0" y="120" width="1200" height="168"/></clipPath>'
             '<clipPath id="l2"><rect x="0" y="288" width="1200" height="176"/></clipPath>')
    b = [head]
    b.append('<circle class="drift" cx="1010" cy="70" r="420" fill="url(#ov)"/>')
    b.append(f'<circle class="drift" cx="760" cy="560" r="320" fill="url(#oc)" {delay(-7000)}/>')
    for i in range(1, 6):
        b.append(f'<line x1="{i*200}" y1="0" x2="{i*200}" y2="{H}" stroke="#fff" stroke-opacity=".045"/>')
    # top row
    top = [ab_mark(64, 42, 46, TEXT)]
    pill_txt = 'Open to relocation — Canada · UAE'
    tw = MONO.width(pill_txt.upper(), 12, .14)
    top.append(f'<rect x="132" y="38" width="{num(tw+56)}" height="34" rx="17" fill="#fff" fill-opacity=".03" stroke="#fff" stroke-opacity=".16"/>')
    top.append(f'<circle cx="152" cy="55" r="4" fill="{GREEN}"/><circle class="pulse" cx="152" cy="55" r="4" fill="{GREEN}"/>')
    top.append(label(pill_txt, 12, 168, 59.5, TEXT)[0])
    top.append(label('Tunis, Tunisia — GMT+1', 12, 1136, 59.5, DIM, 'end')[0])
    b.append(f'<g class="fade" {delay(200)}>{"".join(top)}</g>')
    # name
    l1, w1 = text(DISP, 'Abdelkader', 176, 56, 268, TEXT, -0.055)
    l2, _ = text(SERIF, 'Barhoumi', 188, 150, 428, 'url(#nm)', -0.03)
    b.append(f'<g clip-path="url(#l1)"><g class="rise" {delay(300)}>{l1}</g></g>')
    b.append(f'<g clip-path="url(#l2)"><g class="rise" {delay(420)}>{l2}</g></g>')
    # right intro block next to "Barhoumi"
    intro = ['I lead the mobile department at', 'Oxton Digital — shipping Flutter and', 'native Android apps for clients in', 'France, the UAE, Algeria and Tunisia.']
    blk = []
    for i, ln in enumerate(intro):
        blk.append(text(BODY, ln, 17, 868, 340 + i * 25, DIM)[0])
    b.append(f'<g class="fade" {delay(900)}>{"".join(blk)}</g>')
    # bottom row
    bot = [label('Mobile Software Engineer — Flutter & Native Android', 12, 64, 486, TEXT)[0],
           label('Mobile Lead @ Oxton Digital', 12, 1136, 486, DIM, 'end')[0]]
    b.append(f'<g class="fade" {delay(1000)}>{"".join(bot)}</g>')
    b.append(f'<rect class="draw" x="0" y="{H-3}" width="{W}" height="3" fill="url(#bar)" {delay(150)}/>')
    b.append(tail)
    write('header.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ MARQUEE
def marquee():
    W, H = 1200, 168
    words = ['Flutter', 'Kotlin', 'Jetpack Compose', 'Dart', 'BLoC', 'Riverpod', 'KMP',
             'Firebase', 'BLE & IoT', 'Rust', 'Clean Architecture']
    defs, head, tail = card_frame(W, H, INK)
    defs += ('<linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/>'
             '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<mask id="edge"><rect width="{W}" height="{H}" fill="url(#fadeX)"/></mask>')

    def row(seq, y, size, outlined, star):
        parts, x = [], 0.0
        gap = size * 0.42
        for copy in range(2):
            for wd in seq:
                if outlined:
                    p, w = text(DISP, wd, size, x, y, 'none', -0.045, attrs='stroke="#fff" stroke-opacity=".28" stroke-width="1.1"')
                else:
                    p, w = text(DISP, wd, size, x, y, TEXT, -0.045)
                parts.append(p)
                x += w + gap
                parts.append(sparkle(x, y - size * 0.34, size * 0.2, star))
                x += gap
        return ''.join(parts), x / 2

    r1, w1 = row(words, 76, 58, False, VIOLET)
    r2, w2 = row(list(reversed(words)), 144, 58, True, CYAN)
    css = (f'.m1{{animation:mq1 {int(w1/42)}s linear infinite}}.m2{{animation:mq2 {int(w2/34)}s linear infinite}}'
           f'@keyframes mq1{{from{{transform:translateX(0)}}to{{transform:translateX(-{num(w1)}px)}}}}'
           f'@keyframes mq2{{from{{transform:translateX(-{num(w2)}px)}}to{{transform:translateX(0)}}}}')
    body = (head + f'<g mask="url(#edge)"><g class="m1">{r1}</g><g class="m2">{r2}</g></g>' + tail)
    write('marquee.svg', svg(W, H, defs, body, css))

# ================================================================ SECTION HEADERS
SECTIONS = [
    ('about', '01', 'About', [('Building apps that feel ', False), ('effortless', True)]),
    ('principles', '02', 'How I work', [('Principles I ', False), ('ship', True), (' by', False)]),
    ('work', '03', 'Selected work', [('Products I’ve ', False), ('shipped', True)]),
    ('oss', '04', 'Open source', [('Side projects & ', False), ('experiments', True)]),
    ('experience', '05', 'Experience', [('Where I’ve been ', False), ('building', True)]),
    ('toolkit', '06', 'Toolkit', [('The ', False), ('toolkit', True)]),
    ('numbers', '07', 'By the numbers', [('Code in ', False), ('numbers', True)]),
    ('activity', '08', 'Contributions', [('A year of ', False), ('commits', True)]),
    ('education', '09', 'Education', [('Always ', False), ('learning', True)]),
]

def section_headers():
    W, H = 1200, 150
    for key, idx, lab, title in SECTIONS:
        for theme in ('dark', 'light'):
            fg, dim, line_op = (TEXT, DIM, .18) if theme == 'dark' else (PAPER_TEXT, PAPER_DIM, .22)
            line_col = '#fff' if theme == 'dark' else '#000'
            a, wa = label(f'({idx})', 13, 0, 26, fg, face=MONOM)
            bl, wb = label(lab, 13, wa + 18, 26, dim)
            rule_x = wa + 18 + wb + 22
            ttl, _ = mixed(title, 72, 0, 128, fg)
            defs = '<clipPath id="t"><rect x="0" y="44" width="1200" height="106"/></clipPath>'
            body = (f'<g class="fade">{a}{bl}</g>'
                    f'<rect class="draw" x="{num(rule_x)}" y="21" width="{num(W-rule_x)}" height="1" fill="{line_col}" fill-opacity="{line_op}" {delay(100)}/>'
                    f'<g clip-path="url(#t)"><g class="rise" {delay(150)}>{ttl}</g></g>')
            write(f'sec-{key}-{theme}.svg', svg(W, H, defs, body))

# ================================================================ WORK CARDS
WORK = [
    dict(key='sparta', name='Sparta Coaching', client='Oxton Digital', year='2026', cat='Fitness & coaching · iOS · Android', tone='gold',
         desc='Cross-platform fitness app — workout tracking, exercise library, training plans and real-time coach chat.',
         tags=['Flutter', 'BLoC', 'GetStream.io', 'Firebase'], shot='sparta-coaching.png', framed=True),
    dict(key='masdary', name='Masdary', client='Stoneslane · Dubai', year='2025 — Now', cat='B2B e-commerce · iOS · Android', tone='orange',
         desc='B2B commerce app — catalog, cart & checkout, payments and order tracking, live on Google Play and the App Store.',
         tags=['Flutter', 'BLoC', 'ObjectBox', 'Algolia'], shot='masdary.png', framed=False),
    dict(key='wergo', name='Wergo', client='Sifartek · Algiers', year='2026', cat='IoT · Wearable sensors', tone='cyan',
         desc='Flutter app pairing wearable IoT sensors over BLE and Wi-Fi, with offline-first storage and automatic cloud sync.',
         tags=['Flutter', 'BLE', 'Drift', 'Firebase'], shot='wergo.png', framed=True),
    dict(key='medlink', name='Medlink', client='Nexits · Paris', year='2025', cat='Healthcare · iOS · Android', tone='blue',
         desc='Healthcare app — appointments, patient profiles and notifications with role-based access, shipped to both stores.',
         tags=['Flutter', 'Riverpod', 'OpenAPI', 'Drift'], shot='medlink.png', framed=True),
    dict(key='bowling', name='Fun Bowling', client='Oxton Digital × Digi Service', year='2026', cat='Entertainment · Native Android', tone='violet',
         desc='Migrated a live bowling entertainment app from XML + Java to Kotlin + Jetpack Compose with Clean Architecture.',
         tags=['Kotlin', 'Compose', 'Clean Arch'], shot=None, framed=True),
]

def phone(cx, cy, w, tone, inner):
    h = w * 2.14
    x, y = cx - w / 2, cy - h / 2
    pad = w * 0.04
    return (f'<g class="float"><g transform="rotate(-7 {num(cx)} {num(cy)})">'
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{num(w*.17)}" fill="url(#frame)"/>'
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{num(w*.17)}" fill="none" stroke="#fff" stroke-opacity=".1"/>'
            f'<clipPath id="scr"><rect x="{num(x+pad)}" y="{num(y+pad)}" width="{num(w-2*pad)}" height="{num(h-2*pad)}" rx="{num(w*.13)}"/></clipPath>'
            f'<g clip-path="url(#scr)"><rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="#0B0B0E"/>'
            + inner(x + pad, y + pad, w - 2 * pad, h - 2 * pad) +
            f'</g><rect x="{num(cx-w*.15)}" y="{num(y+pad+w*.035)}" width="{num(w*.3)}" height="{num(w*.085)}" rx="{num(w*.0425)}" fill="#000"/>'
            '</g></g>')

def bowling_screen(tone):
    def inner(x, y, w, h):
        s = w / 100
        out = [f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h*.45)}" fill="url(#scrGlow)"/>']
        out.append(label('Entertainment', 3 * s, x + 6 * s, y + 22 * s, DIM)[0])
        out.append(text(SEMI, 'Fun Bowling', 8 * s, x + 6 * s, y + 32 * s, TEXT, -0.03)[0])
        out.append(f'<rect x="{num(x+6*s)}" y="{num(y+38*s)}" width="{num(88*s)}" height="{num(30*s)}" rx="{num(5*s)}" fill="{tone}" fill-opacity=".3"/>')
        out.append(text(MONO, 'TOTAL SCORE', 3 * s, x + 10 * s, y + 46 * s, TEXT)[0])
        out.append(text(SEMI, '246', 14 * s, x + 10 * s, y + 63 * s, TEXT, -0.05)[0])
        marks = ['X', '9/', 'X', 'X', '8/', 'X', '7/', 'X', 'X', 'X9']
        for i, m in enumerate(marks):
            cxx = x + 6 * s + (i % 5) * 17.8 * s
            cyy = y + 73 * s + (i // 5) * 17.8 * s
            strike = m.startswith('X')
            out.append(f'<rect x="{num(cxx)}" y="{num(cyy)}" width="{num(15.5*s)}" height="{num(15.5*s)}" rx="{num(3*s)}" fill="{tone if strike else "#fff"}" fill-opacity="{1 if strike else .07}"/>')
            out.append(text(SEMI, m, 5 * s, cxx + 7.75 * s, cyy + 10 * s, INK if strike else TEXT, anchor='middle')[0])
        for i, (t1, t2) in enumerate([('Lane 04', 'Available now'), ('Lane 07', 'Booked · 19:30'), ('Lane 09', 'Tournament')]):
            yy = y + 112 * s + i * 20 * s
            out.append(f'<rect x="{num(x+6*s)}" y="{num(yy)}" width="{num(88*s)}" height="{num(17*s)}" rx="{num(4*s)}" fill="#fff" fill-opacity=".055"/>')
            out.append(f'<rect x="{num(x+9*s)}" y="{num(yy+3.5*s)}" width="{num(10*s)}" height="{num(10*s)}" rx="{num(3*s)}" fill="{tone}"/>')
            out.append(text(SEMI, t1, 4 * s, x + 23 * s, yy + 8 * s, TEXT)[0])
            out.append(text(BODY, t2, 3.4 * s, x + 23 * s, yy + 13 * s, DIM)[0])
        return ''.join(out)
    return inner

def work_card(c, i):
    W, H = 600, 380
    tone = TONES[c['tone']]
    defs, head, tail = card_frame(W, H, SURF, rx=26)
    defs += (f'<radialGradient id="glow" cx="78%" cy="40%" r="60%"><stop offset="0" stop-color="{tone}" stop-opacity=".34"/><stop offset="1" stop-color="{tone}" stop-opacity="0"/></radialGradient>'
             '<linearGradient id="frame" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3a42"/><stop offset=".4" stop-color="#0c0c0f"/><stop offset=".75" stop-color="#1d1d22"/><stop offset="1" stop-color="#3a3a42"/></linearGradient>'
             f'<linearGradient id="scrGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{tone}" stop-opacity=".35"/><stop offset="1" stop-color="{tone}" stop-opacity="0"/></linearGradient>')
    b = [head, f'<rect width="{W}" height="{H}" fill="url(#glow)"/>']
    # big outline index
    num_svg, _ = text(DISP, f'{i:02d}', 210, 610, 440, 'none', -0.07, 'end', f'stroke="{tone}" stroke-opacity=".35" stroke-width="1.2"')
    b.append(num_svg)
    # visual
    if c['shot'] and c['framed']:
        img = b64(os.path.join(SHOTS, c['shot']))
        def inner(x, y, w, h, img=img):
            return f'<image href="{img}" x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" preserveAspectRatio="xMidYMin slice"/>'
        b.append(phone(470, 250, 176, tone, inner))
    elif c['shot']:
        img = b64(os.path.join(SHOTS, c['shot']))
        pw, ph = 196, 196 * 626 / 350
        px, py = 470 - pw / 2, 228 - ph / 2
        b.append(f'<g class="float"><g transform="rotate(-7 470 228)">'
                 f'<clipPath id="pst"><rect x="{num(px)}" y="{num(py)}" width="{num(pw)}" height="{num(ph)}" rx="20"/></clipPath>'
                 f'<image href="{img}" x="{num(px)}" y="{num(py)}" width="{num(pw)}" height="{num(ph)}" clip-path="url(#pst)" preserveAspectRatio="xMidYMid slice"/>'
                 f'<rect x="{num(px)}" y="{num(py)}" width="{num(pw)}" height="{num(ph)}" rx="20" fill="none" stroke="#fff" stroke-opacity=".12"/></g></g>')
    else:
        b.append(phone(470, 250, 176, tone, bowling_screen(tone)))
    # text block
    t = []
    t.append(label(f'{i:02d}', 11.5, 32, 46, tone, face=MONOM)[0])
    t.append(label(f'{c["client"]} · {c["year"]}', 11.5, 64, 46, DIM)[0])
    size = 46
    while DISP.width(c['name'], size, -0.05) > 320:
        size -= 1
    t.append(text(DISP, c['name'], size, 30, 104, TEXT, -0.05)[0])
    dot_y = 132
    t.append(f'<circle cx="37" cy="{dot_y-4}" r="3.5" fill="{tone}"/>')
    t.append(label(c['cat'], 10.5, 48, dot_y, TEXT)[0])
    for k, ln in enumerate(wrap(BODY, c['desc'], 15.5, 318)[:4]):
        t.append(text(BODY, ln, 15.5, 32, 176 + k * 24, DIM)[0])
    x, y = 32, 300
    for tag in c['tags']:
        tw = MONO.width(tag, 11.5) + 22
        if x + tw > 350:
            x, y = 32, y + 34
        t.append(f'<rect x="{num(x)}" y="{y}" width="{num(tw)}" height="26" rx="13" fill="none" stroke="#fff" stroke-opacity=".16"/>')
        t.append(text(MONO, tag, 11.5, x + 11, y + 17, TEXT)[0])
        x += tw + 8
    b.append(f'<g class="fade" {delay(100)}>{"".join(t)}</g>')
    b.append(tail)
    write(f'work-{c["key"]}.svg', svg(W, H, defs, ''.join(b)))

def work_cta():
    W, H = 600, 380
    defs, head, tail = card_frame(W, H, RAISED, rx=26)
    defs += (f'<radialGradient id="g1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="g2"><stop offset="0" stop-color="{CYAN}" stop-opacity=".3"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="t"><rect x="0" y="150" width="600" height="160"/></clipPath>')
    b = [head,
         '<circle class="drift" cx="520" cy="60" r="300" fill="url(#g1)"/>',
         f'<circle class="drift" cx="120" cy="420" r="240" fill="url(#g2)" {delay(-6000)}/>']
    b.append(label('06', 11.5, 32, 46, VIOLET, face=MONOM)[0])
    b.append(label('Case studies · Portfolio', 11.5, 64, 46, DIM)[0])
    t1, _ = text(DISP, 'See the full', 56, 30, 226, TEXT, -0.05)
    t2, _ = mixed([('case ', False), ('studies', True)], 56, 30, 290, TEXT)
    b.append(f'<g clip-path="url(#t)"><g class="rise">{t1}</g><g class="rise" {delay(120)}>{t2}</g></g>')
    b.append(label('abdelkaderbarhoumi21.github.io/portfolio', 11.5, 32, 340, TEXT)[0])
    b.append(f'<circle cx="530" cy="318" r="34" fill="{TEXT}"/>' + arrow(518, 330, 22, INK, 2.6))
    b.append(tail)
    write('work-cta.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ EXPERIENCE (paper)
EXPERIENCE = [
    ('Apr 2026 — Present', True, 'Oxton Digital', 'Mobile Department Lead — Flutter & Android', 'Tunis, Tunisia', 'Full-time · On-site'),
    ('Oct 2025 — Present', True, 'Stoneslane', 'Mobile Engineer — Flutter · Masdary', 'Dubai, UAE', 'Contract · Remote'),
    ('Feb 2026 — Apr 2026', False, 'Sifartek', 'Mobile Engineer — Flutter · BLE / IoT', 'Algiers, Algeria', 'Contract · Remote'),
    ('Oct 2025 — Dec 2025', False, 'Nexits', 'Mobile Engineer — Flutter · Medlink', 'Paris, France', 'Contract · Remote'),
]

def experience():
    W, RH, TOP = 1200, 118, 34
    H = TOP + RH * len(EXPERIENCE) + 34
    defs, head, tail = card_frame(W, H, PAPER, stroke_op=0)
    b = [head]
    for i, (period, now, comp, role, loc, emp) in enumerate(EXPERIENCE):
        y = TOP + i * RH
        d = 150 + i * 140
        b.append(f'<rect class="draw" x="48" y="{y}" width="{W-96}" height="1" fill="#000" fill-opacity=".22" {delay(d)}/>')
        row = [label(period, 12.5, 48, y + 46, PAPER_TEXT)[0]]
        if now:
            row.append(f'<rect x="48" y="{y+62}" width="70" height="26" rx="13" fill="{PAPER_TEXT}"/>'
                       f'<circle cx="64" cy="{y+75}" r="3.5" fill="{GREEN}"/>')
            row.append(label('Now', 10.5, 74, y + 79, PAPER, face=MONOM)[0])
        row.append(text(DISP, comp, 42, 330, y + 56, PAPER_TEXT, -0.045)[0])
        row.append(text(BODY, role, 17, 332, y + 88, PAPER_DIM)[0])
        row.append(label(loc, 12, W - 48, y + 46, PAPER_TEXT, 'end')[0])
        row.append(label(emp, 12, W - 48, y + 70, PAPER_FAINT, 'end')[0])
        b.append(f'<g class="fade" {delay(d+100)}>{"".join(row)}</g>')
    yb = TOP + RH * len(EXPERIENCE)
    b.append(f'<rect class="draw" x="48" y="{yb}" width="{W-96}" height="1" fill="#000" fill-opacity=".22" {delay(700)}/>')
    b.append(tail)
    write('experience.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ TOOLKIT
TOOLKIT = [
    ('Mobile — Flutter', 'Dart · BLoC/Cubit · Riverpod · GetIt/Injectable · Clean Architecture · Testing'),
    ('Native Android', 'Kotlin · Jetpack Compose · Hilt · Retrofit · Room · XML → Compose migration'),
    ('Multiplatform', 'Kotlin Multiplatform (learning) · shared logic across Android & iOS'),
    ('Backend & Real-time', 'Rust (Axum) · Node.js · Laravel · WebSockets · GetStream.io · JWT / OAuth2'),
    ('Data & Storage', 'Firebase / Firestore · PostgreSQL · MongoDB · Drift · ObjectBox · Supabase'),
    ('DevOps & Tooling', 'Git · Docker · Fastlane · GitHub Actions · CI/CD · Crashlytics · Figma'),
]

def toolkit():
    W, RH, TOP = 1200, 96, 26
    H = TOP + RH * len(TOOLKIT) + 26
    defs, head, tail = card_frame(W, H, SURF)
    b = [head]
    for i, (grp, tools) in enumerate(TOOLKIT):
        y = TOP + i * RH
        d = 120 + i * 110
        if i:
            b.append(f'<rect class="draw" x="40" y="{y}" width="{W-80}" height="1" fill="#fff" fill-opacity=".08" {delay(d)}/>')
        row = [label(f'{i+1:02d}', 12, 40, y + 54, VIOLET if i % 2 == 0 else CYAN, face=MONOM)[0],
               text(DISP, grp, 30, 96, y + 58, TEXT, -0.04)[0]]
        for k, ln in enumerate(wrap(BODY, tools, 16.5, 620)[:2]):
            row.append(text(BODY, ln, 16.5, 520, y + (46 if len(wrap(BODY, tools, 16.5, 620)) > 1 else 56) + k * 24, DIM)[0])
        b.append(f'<g class="fade" {delay(d+80)}>{"".join(row)}</g>')
    b.append(tail)
    write('toolkit.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ CONTACT
def contact():
    W, H = 1200, 460
    defs, head, tail = card_frame(W, H, INK)
    defs += (f'<radialGradient id="g"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="t1"><rect x="0" y="80" width="1200" height="124"/></clipPath>'
             '<clipPath id="t2"><rect x="0" y="204" width="1200" height="136"/></clipPath>')
    b = [head, '<ellipse class="drift" cx="600" cy="560" rx="560" ry="300" fill="url(#g)"/>']
    for i in range(1, 6):
        b.append(f'<line x1="{i*200}" y1="0" x2="{i*200}" y2="{H}" stroke="#fff" stroke-opacity=".04"/>')
    a, wa = label('(10)', 13, 56, 58, TEXT, face=MONOM)
    bl, wb = label('Contact', 13, 56 + wa + 18, 58, DIM)
    rx = 56 + wa + 18 + wb + 22
    b.append(f'<g class="fade">{a}{bl}</g><rect class="draw" x="{num(rx)}" y="53" width="{num(W-56-rx)}" height="1" fill="#fff" fill-opacity=".18" {delay(100)}/>')
    t1, _ = text(DISP, 'Let’s build', 120, 50, 186, TEXT, -0.06)
    t2, _ = mixed([('something ', False), ('great.', True)], 120, 50, 312, TEXT, '#B9B4FF')
    b.append(f'<g clip-path="url(#t1)"><g class="rise" {delay(150)}>{t1}</g></g>')
    b.append(f'<g clip-path="url(#t2)"><g class="rise" {delay(270)}>{t2}</g></g>')
    em, ew = text(DISP, 'abdelkaderbarhoumi21@gmail.com', 30, 56, 404, TEXT, -0.03)
    b.append(f'<g class="fade" {delay(700)}>{em}{arrow(56 + ew + 14, 404, 18, VIOLET, 2.4)}</g>')
    b.append(f'<g class="fade" {delay(800)}>{label("Tunis, Tunisia · GMT+1", 12, W-56, 398, DIM, "end")[0]}</g>')
    b.append(tail)
    write('contact.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ BUTTONS
def button(key, lab, solid):
    tw = DISP.width(lab, 19, -0.01)
    W, H = int(tw + 96), 60
    fill, fg, circ, arr = (TEXT, INK, INK, TEXT) if solid else (SURF, TEXT, '#2A2A31', TEXT)
    body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{(H-1)/2}" fill="{fill}" stroke="{"#000" if solid else "#fff"}" stroke-opacity="{.08 if solid else .18}"/>'
            + text(DISP, lab, 19, 26, 37, fg, -0.01)[0]
            + f'<circle cx="{W-32}" cy="30" r="21" fill="{circ}"/>' + arrow(W - 38.5, 36.5, 13, arr, 2))
    write(f'btn-{key}.svg', svg(W, H, '', body))

# ================================================================ GITHUB DATA
import json, subprocess, datetime, urllib.request

def token():
    t = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if t:
        return t
    return subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True).stdout.strip()

def gql(query, variables):
    req = urllib.request.Request('https://api.github.com/graphql',
                                 data=json.dumps({'query': query, 'variables': variables}).encode(),
                                 headers={'Authorization': f'bearer {token()}', 'User-Agent': 'profile-gen'})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if 'errors' in data:
        raise RuntimeError(data['errors'])
    return data['data']

Q = '''query($login:String!,$cursor:String){user(login:$login){
  repositories(first:100,after:$cursor,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false){
    totalCount pageInfo{hasNextPage endCursor}
    nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
  contributionsCollection{contributionCalendar{totalContributions
    weeks{contributionDays{date contributionCount contributionLevel}}}}}}'''

# Native runner folders generated by `flutter create` (windows/, linux/, ios/ ...)
# would otherwise dominate the language mix.
SCAFFOLD = {'C++', 'CMake', 'C', 'Swift', 'Objective-C', 'HTML', 'Ruby', 'Shell', 'Batchfile', 'Dockerfile', 'Makefile'}

def fetch():
    langs, cursor, cal, repos = {}, None, None, 0
    while True:
        u = gql(Q, {'login': LOGIN, 'cursor': cursor})['user']
        rp = u['repositories']
        repos = rp['totalCount']
        cal = cal or u['contributionsCollection']['contributionCalendar']
        for n in rp['nodes']:
            for e in n['languages']['edges']:
                name = e['node']['name']
                if name in SCAFFOLD:
                    continue
                size = langs.get(name, (0, None))[0]
                langs[name] = (size + e['size'], e['node']['color'] or '#8D8D95')
        if not rp['pageInfo']['hasNextPage']:
            break
        cursor = rp['pageInfo']['endCursor']
    days = [d for w in cal['weeks'] for d in w['contributionDays']]
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d['contributionCount'] else 0
        longest = max(longest, cur)
    return dict(total=cal['totalContributions'], repos=repos, longest=longest,
                active=sum(1 for d in days if d['contributionCount']), weeks=cal['weeks'], langs=langs)

# ================================================================ PRINCIPLES
PRINCIPLES = [
    ('Architecture first', 'Clean Architecture with BLoC/Cubit or Riverpod boundaries, so features stay testable and teams can grow the codebase safely.',
     '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>'),
    ('Offline by default', 'Drift and ObjectBox persistence with automatic cloud sync, so apps keep working on weak networks and flaky BLE links.',
     '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>'),
    ('Tested & automated', 'Unit, widget and integration tests wired into Fastlane CI/CD, shipping to Google Play and the App Store.',
     '<path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="m9 11 3 3L22 4"/>'),
    ('End-to-end ownership', 'From Rust, Node.js or Laravel APIs to Flutter and Compose clients, and leading the team that ships them.',
     '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>'),
]

def principles():
    W, CH = 1200, 214
    H = CH * 2
    defs, head, tail = card_frame(W, H, SURF)
    defs += f'<radialGradient id="g"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
    b = [head, '<circle class="drift" cx="1100" cy="0" r="380" fill="url(#g)"/>',
         f'<rect class="draw" x="40" y="{CH}" width="{W-80}" height="1" fill="#fff" fill-opacity=".08" {delay(200)}/>',
         f'<rect class="fade" x="{W//2}" y="34" width="1" height="{H-68}" fill="#fff" fill-opacity=".08" {delay(200)}/>']
    for i, (title, desc, icon) in enumerate(PRINCIPLES):
        cx, cy = (i % 2) * (W // 2), (i // 2) * CH
        tone = VIOLET if i in (0, 3) else CYAN
        cell = [label(f'{i+1:02d}', 12, cx + 48, cy + 58, tone, face=MONOM)[0],
                f'<g transform="translate({cx + W//2 - 88} {cy + 34}) scale(1.6)" fill="none" stroke="{tone}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{icon}</g>',
                text(DISP, title, 34, cx + 46, cy + 108, TEXT, -0.04)[0]]
        for k, ln in enumerate(wrap(BODY, desc, 16.5, 470)[:3]):
            cell.append(text(BODY, ln, 16.5, cx + 48, cy + 144 + k * 24, DIM)[0])
        b.append(f'<g class="fade" {delay(150 + i * 140)}>{"".join(cell)}</g>')
    b.append(tail)
    write('principles.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ NUMBERS
def numbers(data):
    W, H = 1200, 372
    defs, head, tail = card_frame(W, H, INK)
    defs += (f'<radialGradient id="g1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".4"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="g2"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
             '<clipPath id="n"><rect x="0" y="60" width="1200" height="118"/></clipPath>')
    b = [head, '<circle class="drift" cx="1080" cy="40" r="360" fill="url(#g1)"/>',
         f'<circle class="drift" cx="140" cy="400" r="300" fill="url(#g2)" {delay(-5000)}/>']
    stats = [(f"{data['total']:,}", 'Contributions', 'in the last year'),
             (str(data['repos']), 'Public repositories', 'built and learned in public'),
             (str(data['active']), 'Active days', 'with at least one contribution'),
             (str(data['longest']), 'Longest streak', 'consecutive days')]
    colw = (W - 96) / 4
    nums = []
    for i, (v, lab_, sub_) in enumerate(stats):
        x = 48 + i * colw
        if i:
            b.append(f'<rect class="fade" x="{num(x - 24)}" y="56" width="1" height="150" fill="#fff" fill-opacity=".08" {delay(300)}/>')
        nums.append(f'<g class="rise" {delay(150 + i * 110)}>{text(DISP, v, 92, x - 4, 166, TEXT, -0.06)[0]}</g>')
        b.append(f'<g class="fade" {delay(400 + i * 110)}>{label(lab_, 12, x, 196, TEXT)[0]}{text(BODY, sub_, 15, x, 220, DIM)[0]}</g>')
    b.append(f'<g clip-path="url(#n)">{"".join(nums)}</g>')
    # Languages by bytes across public repos.
    top = sorted(data['langs'].items(), key=lambda kv: -kv[1][0])
    total = sum(v[0] for _, v in top) or 1
    shown = top[:6]
    other = total - sum(v[0] for _, v in shown)
    segs = [(n, v[0] / total, v[1]) for n, v in shown] + ([('Other', other / total, '#5C5C68')] if other > 0 else [])
    b.append(f'<g class="fade" {delay(500)}>{label("Top languages", 12, 48, 276, TEXT)[0]}'
             f'{label("Updated daily · " + datetime.date.today().strftime("%d %b %Y"), 11, W - 48, 276, FAINT, "end")[0]}</g>')
    bx, bw = 48, W - 96
    defs += f'<clipPath id="bar"><rect x="{bx}" y="292" width="{bw}" height="10" rx="5"/></clipPath>'
    x = bx
    parts = []
    for k, (n, frac, col) in enumerate(segs):
        w = bw * frac
        parts.append(f'<rect class="draw" x="{num(x)}" y="292" width="{num(w + .5)}" height="10" fill="{col}" {delay(600 + k * 90)}/>')
        x += w
    b.append(f'<rect x="{bx}" y="292" width="{bw}" height="10" rx="5" fill="#fff" fill-opacity=".06"/><g clip-path="url(#bar)">{"".join(parts)}</g>')
    lx = 48
    leg = []
    for n, frac, col in segs:
        pct = f'{frac*100:.1f}%'
        wn = BODY.width(n, 15)
        leg.append(f'<circle cx="{num(lx + 5)}" cy="331" r="5" fill="{col}"/>')
        leg.append(text(BODY, n, 15, lx + 18, 336, TEXT)[0])
        leg.append(text(MONO, pct, 12, lx + 24 + wn, 336, DIM)[0])
        lx += 24 + wn + MONO.width(pct, 12) + 30
    b.append(f'<g class="fade" {delay(900)}>{"".join(leg)}</g>')
    b.append(tail)
    write('numbers.svg', svg(W, H, defs, ''.join(b)))

# ================================================================ ACTIVITY (contribution graph)
LEVELS = {'NONE': ('#FFFFFF', .05), 'FIRST_QUARTILE': ('#3A3488', 1), 'SECOND_QUARTILE': ('#5149C9', 1),
          'THIRD_QUARTILE': (VIOLET, 1), 'FOURTH_QUARTILE': ('#7FE6FF', 1)}

def activity(data):
    W, H = 1200, 336
    weeks = data['weeks'][-53:]
    cell, gap = 16, 4
    x0, y0 = 92, 92
    css = (f'.c{{animation:pop .9s {EASE} both;transform-box:fill-box;transform-origin:center}}'
           '@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:none}}'
           '.beam{animation:beam 7s cubic-bezier(.65,0,.35,1) 1.6s infinite}'
           '@keyframes beam{0%{transform:translateX(-260px)}55%,100%{transform:translateX(1300px)}}')
    defs, head, tail = card_frame(W, H, INK)
    defs += ('<linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    b = [head]
    months, seen = [], set()
    cells = []
    for wi, w in enumerate(weeks):
        for d in w['contributionDays']:
            dt = datetime.date.fromisoformat(d['date'])
            row = (dt.weekday() + 1) % 7  # Sunday first, like GitHub
            key = (dt.year, dt.month)
            if dt.day <= 7 and key not in seen and wi < 51:
                seen.add(key)
                months.append((wi, dt.strftime('%b')))
            col, op = LEVELS.get(d['contributionLevel'], LEVELS['NONE'])
            x, y = x0 + wi * (cell + gap), y0 + row * (cell + gap)
            cells.append(f'<rect class="c" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{col}" fill-opacity="{op}" '
                         f'style="animation-delay:{wi*16 + row*45}ms"/>')
    b.append(''.join(cells))
    for wi, m in months:
        b.append(text(MONO, m, 11, x0 + wi * (cell + gap), 74, DIM)[0])
    for row, dn in ((1, 'Mon'), (3, 'Wed'), (5, 'Fri')):
        b.append(text(MONO, dn, 11, 40, y0 + row * (cell + gap) + 12, FAINT)[0])
    b.append(f'<rect class="beam" x="0" y="80" width="240" height="{7*(cell+gap)+24}" fill="url(#beam)"/>')
    tot, wt = text(DISP, f"{data['total']:,}", 26, 40, 300, TEXT, -0.03)
    b.append(f'<g class="fade" {delay(900)}>{tot}{text(BODY, " contributions in the last year", 17, 40 + wt + 4, 299, DIM)[0]}</g>')
    lg = [label('Less', 11, 1002, 298, DIM)[0]]
    for k, key in enumerate(LEVELS):
        col, op = LEVELS[key]
        lg.append(f'<rect x="{1044 + k*18}" y="286" width="14" height="14" rx="3.5" fill="{col}" fill-opacity="{op}"/>')
    lg.append(label('More', 11, 1140, 298, DIM)[0])
    b.append(f'<g class="fade" {delay(900)}>{"".join(lg)}</g>')
    b.append(tail)
    write('activity.svg', svg(W, H, defs, ''.join(b), css))

DATA = fetch()
print('stats:', {k: DATA[k] for k in ('total', 'repos', 'active', 'longest')})
principles(); numbers(DATA); activity(DATA)

header(); marquee(); section_headers()
for i, c in enumerate(WORK, 1):
    work_card(c, i)
work_cta(); experience(); toolkit(); contact()
button('portfolio', 'Portfolio', True)
button('linkedin', 'LinkedIn', False)
button('email', 'Email me', False)
