"""Generates the ThatKJ profile README SVG assets. Text is shaped with HarfBuzz and
emitted as outlined glyphs (<use> of shared <path> defs), so the artwork renders
identically on every OS without web fonts.

Usage (from the repo root):
    pip install fonttools uharfbuzz
    # Big Shoulders Display, IBM Plex Sans and IBM Plex Mono (OFL) from github.com/google/fonts
    FONTS_DIR=/path/to/fonts python3 assets/build.py
"""
import io, math, os, random, re, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("FONTS_DIR", os.path.join(HERE, "fonts"))
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
os.makedirs(OUT, exist_ok=True)

# ---- tokens ---------------------------------------------------------------
INK = "#0B1320"      # device body
PANEL = "#0E1828"    # card body
RULE = "#1F2E47"     # hairlines, borders
GRID = "#132036"     # background grid
KEY = "#15233A"      # keycap fill
PAPER = "#ECE7DB"    # primary text
MUTED = "#8A97AE"    # secondary text
DIM = "#56647C"      # tertiary
AMBER = "#F5A524"    # live signal
CYAN = "#5CC8E0"     # measured trace
CORAL = "#E0715C"    # failure / loss
LIGHT = {PAPER: "#1B2433", MUTED: "#5A6780", DIM: "#8A96AA", RULE: "#D5DBE5", AMBER: "#B8740A"}


class Face:
    def __init__(self, key, file, axes=None):
        tt = TTFont(os.path.join(FONTS, file))
        if axes:
            tt = instantiateVariableFont(tt, axes)
        buf = io.BytesIO(); tt.save(buf)
        self.tt, self.key = tt, key
        self.upem = tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(buf.getvalue()))
        self.gs = tt.getGlyphSet()
        self.paths = {}

    def shape(self, s):
        b = hb.Buffer(); b.add_str(s); b.guess_segment_properties()
        hb.shape(self.hb, b, {"kern": True, "liga": True})
        return [(self.tt.getGlyphName(i.codepoint), p.x_advance, p.x_offset, p.y_offset)
                for i, p in zip(b.glyph_infos, b.glyph_positions)]

    def width(self, s, size, ls=0):
        g = self.shape(s)
        return (sum(a for _, a, _, _ in g) + ls * self.upem * max(len(g) - 1, 0)) * size / self.upem

    def path(self, name):
        if name not in self.paths:
            pen = SVGPathPen(self.gs, ntos=lambda v: ("%.0f" % v))
            self.gs[name].draw(pen)
            self.paths[name] = pen.getCommands()
        return self.paths[name]


DISPLAY = Face("d", "BigShouldersDisplay%5Bwght%5D.ttf", {"wght": 800})
HEAD = Face("h", "BigShouldersDisplay%5Bwght%5D.ttf", {"wght": 700})
SANS = Face("s", "IBMPlexSans%5Bwdth,wght%5D.ttf", {"wght": 400, "wdth": 100})
SANSM = Face("m", "IBMPlexSans%5Bwdth,wght%5D.ttf", {"wght": 500, "wdth": 100})
MONO = Face("o", "IBMPlexMono-Regular.ttf")
MONOM = Face("n", "IBMPlexMono-Medium.ttf")


def gid(face, name):
    return face.key + re.sub(r"[^A-Za-z0-9]", "_", name)


class Doc:
    def __init__(self, w, h, title, desc):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.used, self.body, self.defs, self.css = {}, [], [], ""

    def add(self, s):
        self.body.append(s)

    def text(self, face, s, x, y, size, fill, anchor="start", ls=0, extra=""):
        g = face.shape(s)
        total = face.width(s, size, ls)
        if anchor == "middle": x -= total / 2
        elif anchor == "end": x -= total
        k = size / face.upem
        cur, uses = 0, []
        for name, adv, xo, yo in g:
            d = face.path(name)
            if d:
                self.used[gid(face, name)] = d
                uses.append('<use href="#%s" transform="matrix(%.4f 0 0 %.4f %.1f %.1f)"/>'
                            % (gid(face, name), k, -k, x + (cur + xo) * k, y - yo * k))
            cur += adv + ls * face.upem
        self.add('<g fill="%s"%s>%s</g>' % (fill, extra, "".join(uses)))
        return total

    def wrap(self, face, s, size, maxw):
        lines, line = [], ""
        for word in s.split():
            t = (line + " " + word).strip()
            if face.width(t, size) > maxw and line:
                lines.append(line); line = word
            else:
                line = t
        return lines + [line]

    def para(self, face, s, x, y, size, fill, maxw, lh):
        lines = self.wrap(face, s, size, maxw)
        for i, l in enumerate(lines):
            self.text(face, l, x, y + i * lh, size, fill)
        return y + (len(lines) - 1) * lh

    def svg(self):
        glyphs = "".join('<path id="%s" d="%s"/>' % (k, v) for k, v in self.used.items())
        style = "<style>%s</style>" % self.css if self.css else ""
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
                'role="img" aria-labelledby="t d"><title id="t">%s</title><desc id="d">%s</desc>%s'
                '<defs>%s%s</defs>%s</svg>\n'
                % (self.w, self.h, self.w, self.h, self.title, self.desc, style, glyphs,
                   "".join(self.defs), "".join(self.body)))


def save(doc, name):
    s = doc.svg()
    open(os.path.join(OUT, name), "w").write(s)
    print("%-26s %6.1f KB" % (name, len(s) / 1024))


def lighten(svg):
    for dark, light in LIGHT.items():
        svg = svg.replace(dark, light)
    return svg


def body(doc, rx=16, fill=PANEL, grid=True):
    doc.defs.append('<clipPath id="clip"><rect x="1" y="1" width="%d" height="%d" rx="%d"/></clipPath>'
                    % (doc.w - 2, doc.h - 2, rx))
    doc.defs.append('<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
                    '<path d="M24 0H0V24" fill="none" stroke="%s"/></pattern>' % GRID)
    doc.add('<rect x="1" y="1" width="%d" height="%d" rx="%d" fill="%s"/>' % (doc.w - 2, doc.h - 2, rx, fill))
    if grid:
        doc.add('<rect width="%d" height="%d" fill="url(#grid)" clip-path="url(#clip)" opacity=".7"/>' % (doc.w, doc.h))


def border(doc, rx=16):
    doc.add('<rect x="1" y="1" width="%d" height="%d" rx="%d" fill="none" stroke="%s"/>' % (doc.w - 2, doc.h - 2, rx, RULE))


def lamp(doc, x, y, color, r=4.5):
    doc.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity=".18"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            % (x, y, r * 2.4, color, x, y, r, color))


def chip(doc, s, x, y, face=MONO, size=13, fg=PAPER, stroke=RULE, fill=KEY, padx=10, h=26):
    w = face.width(s, size) + padx * 2
    doc.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="6" fill="%s" stroke="%s"/>' % (x, y, w, h, fill, stroke))
    doc.text(face, s, x + padx, y + h / 2 + size * 0.36, size, fg)
    return w


# ---- hero -------------------------------------------------------------------
def hero():
    d = Doc(1200, 440, "Kirtan Joshi (@ThatKJ)",
            "I build software that has to work outside the demo. Now building Awoken. "
            "A noisy signal settles and a tracking reticle locks onto a beacon.")
    body(d, rx=22, fill=INK)
    cx, cy = 1012, 184
    d.defs.append('<radialGradient id="glow"><stop offset="0" stop-color="%s" stop-opacity=".16"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (AMBER, AMBER))
    d.add('<circle cx="%d" cy="%d" r="250" fill="url(#glow)" clip-path="url(#clip)"/>' % (cx, cy))

    # reticle
    g = ['<g fill="none" stroke-linecap="round">']
    g.append('<circle cx="%d" cy="%d" r="120" stroke="#27395A" stroke-width="1.5"/>' % (cx, cy))
    g.append('<circle cx="%d" cy="%d" r="80" stroke="#223250" stroke-dasharray="2 6"/>' % (cx, cy))
    for a in range(0, 360, 6):
        r2 = 120 - (14 if a % 30 == 0 else 6)
        t = math.radians(a)
        g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>' % (
            cx + 120 * math.cos(t), cy + 120 * math.sin(t), cx + r2 * math.cos(t), cy + r2 * math.sin(t),
            "#3A5378" if a % 30 == 0 else "#27395A"))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3A5378"/>' % (
            cx + dx * 22, cy + dy * 22, cx + dx * 142, cy + dy * 142))
    g.append("</g>")
    d.add("".join(g))
    # lock brackets
    b, s = 34, 12
    br = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x0, y0 = cx + sx * b, cy + sy * b
        br.append("M%d %dV%dM%d %dH%d" % (x0, y0, y0 - sy * s, x0, y0, x0 - sx * s))
    d.add('<path class="lock" d="%s" stroke="%s" stroke-width="2.5" fill="none" stroke-linecap="round"/>' % ("".join(br), AMBER))
    # beacon
    d.add('<g class="beacon"><circle cx="%d" cy="%d" r="16" fill="%s" opacity=".18"/>'
          '<circle cx="%d" cy="%d" r="6" fill="%s"/></g>' % (cx, cy, CYAN, cx, cy, CYAN))
    lamp(d, cx - 58, cy + 176, AMBER, 3.5)
    d.text(MONO, "beacon locked", cx - 46, cy + 181, 14, MUTED)

    # type
    lamp(d, 66, 66, AMBER, 3.5)
    d.text(MONO, "@ThatKJ", 80, 71, 15, MUTED)
    d.text(MONO, "Bangalore, India", 162, 71, 15, DIM)
    size = 150
    while DISPLAY.width("Kirtan Joshi", size, -0.005) > 740:
        size -= 2
    d.text(DISPLAY, "Kirtan Joshi", 56, 214, size, PAPER, ls=-0.005)
    d.text(SANS, "I build software that has to work outside the demo.", 60, 268, 28, PAPER)
    d.text(SANS, "Now building Awoken, AI follow-up for real-estate sales teams.", 60, 306, 18, MUTED)

    # signal trace: noisy on the left, settling into a flat lock on the right
    rnd = random.Random(7)
    pts, x = [], 40
    while x <= 1160:
        a = 26 * math.exp(-(x - 40) / 230) if x < 900 else 0
        pts.append((x, 386 + a * (rnd.random() * 2 - 1)))
        x += 7
    dpath = "M" + " L".join("%.0f %.1f" % p for p in pts)
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    d.add('<path d="%s" fill="none" stroke="%s" stroke-width="6" opacity=".12" clip-path="url(#clip)"/>' % (dpath, AMBER))
    d.add('<path class="trace" d="%s" fill="none" stroke="%s" stroke-width="1.8" stroke-linejoin="round" '
          'stroke-dasharray="%.0f" clip-path="url(#clip)"/>' % (dpath, AMBER, length + 10))
    d.css = (
        ".trace{animation:draw 2.8s cubic-bezier(.3,.7,.2,1) both}"
        "@keyframes draw{from{stroke-dashoffset:%.0f}to{stroke-dashoffset:0}}"
        ".beacon{animation:seek 2.8s cubic-bezier(.3,.7,.2,1) both}"
        "@keyframes seek{0%%{transform:translate(78px,-56px)}28%%{transform:translate(-46px,34px)}"
        "52%%{transform:translate(24px,-16px)}74%%{transform:translate(-8px,6px)}100%%{transform:translate(0,0)}}"
        ".lock{animation:lock 2.8s linear both}"
        "@keyframes lock{0%%,86%%{opacity:0}100%%{opacity:1}}"
        "@media (prefers-reduced-motion:reduce){.trace,.beacon,.lock{animation:none}}" % (length + 10))
    border(d, 22)
    save(d, "hero.svg")


# ---- project cards ------------------------------------------------------------
def card(file, name, status, status_color, blurb, stack, link, draw, alt):
    d = Doc(600, 360, name, alt)
    body(d)
    lamp(d, 36, 38, status_color, 3.5)
    d.text(MONO, status, 50, 43, 13, MUTED)
    d.text(HEAD, name, 30, 112, 54, PAPER)
    d.para(SANS, blurb, 32, 150, 17, MUTED, 250, 25)
    x = 32
    for s in stack:
        x += chip(d, s, x, 300, size=12, h=26, padx=9) + 8
    d.text(MONO, link, 568, 318, 13, AMBER, anchor="end")
    draw(d)
    border(d)
    save(d, file)


def inst_frame(d, x, y, w, h):
    d.add('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s"/>' % (x, y, w, h, INK, RULE))


def awoken_inst(d):
    x0, y0, w, h = 312, 28, 260, 250
    inst_frame(d, x0, y0, w, h)
    msgs = [("a", "Hi Rahul, still exploring homes near Whitefield?"),
            ("l", "Depends on the price."),
            ("a", "What budget are you considering?"),
            ("l", "Around 1.2 Cr.")]
    d.text(MONO, "Example conversation", x0 + 16, y0 + 28, 12, DIM)
    y = y0 + 42
    for who, m in msgs:
        lines = d.wrap(SANS, m, 13, 170)
        bw = max(SANS.width(l, 13) for l in lines) + 22
        bh = 12 + 18 * len(lines)
        bx = x0 + w - 14 - bw if who == "a" else x0 + 14
        fill, stroke, fg = ("#1A2A40", AMBER, PAPER) if who == "a" else (KEY, RULE, MUTED)
        d.add('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="10" fill="%s" stroke="%s" stroke-opacity="%s"/>'
              % (bx, y, bw, bh, fill, stroke, ".55" if who == "a" else "1"))
        for i, l in enumerate(lines):
            d.text(SANS, l, bx + 11, y + 21 + i * 18, 13, fg)
        y += bh + 5
    lamp(d, x0 + 22, y0 + h - 22, CYAN, 3.5)
    d.text(SANSM, "Handed to sales, with context", x0 + 34, y0 + h - 17, 13, PAPER)


def margin_inst(d):
    x0, y0, w, h = 312, 28, 260, 250
    inst_frame(d, x0, y0, w, h)
    d.text(MONO, "Testnet run", x0 + 16, y0 + 28, 12, DIM)
    d.text(MONOM, "contract $1.20", x0 + w - 16, y0 + 28, 12, PAPER, anchor="end")
    rows = [("Draft", "0.05", 5), ("Repair", "0.09", 7), ("Repair", "0.09", 7), ("Premium", "1.05", 8)]
    y = y0 + 56
    for label, cost, score in rows:
        d.text(MONO, label, x0 + 16, y + 5, 13, PAPER if score == 8 else MUTED)
        d.text(MONO, "$" + cost, x0 + 136, y + 5, 13, MUTED, anchor="end")
        for i in range(8):
            c = (CYAN if score == 8 else AMBER) if i < score else "#22314A"
            d.add('<rect x="%d" y="%d" width="10" height="10" rx="2" fill="%s"/>' % (x0 + 148 + i * 12.5, y - 5, c))
        y += 26
    d.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-dasharray="3 4"/>' % (x0 + 16, y - 6, x0 + w - 16, y - 6, RULE))
    d.text(MONO, "spent", x0 + 16, y + 14, 13, MUTED)
    d.text(MONOM, "$1.28", x0 + w - 16, y + 14, 13, PAPER, anchor="end")
    d.text(MONO, "absorbed", x0 + 16, y + 36, 13, MUTED)
    d.text(MONOM, "−$0.08", x0 + w - 16, y + 36, 13, CORAL, anchor="end")
    lamp(d, x0 + 22, y0 + h - 22, CYAN, 3.5)
    d.text(SANSM, "Verified, 8 of 8 tests", x0 + 34, y0 + h - 17, 13, PAPER)


def fsoc_inst(d):
    x0, y0, w, h = 312, 28, 260, 250
    inst_frame(d, x0, y0, w, h)
    cx, cy = x0 + 130, y0 + 92
    d.add('<g fill="none"><circle cx="%d" cy="%d" r="64" stroke="#27395A"/><circle cx="%d" cy="%d" r="36" stroke="#223250" stroke-dasharray="2 5"/>'
          '<path d="M%d %dH%dM%d %dH%dM%d %dV%dM%d %dV%d" stroke="#3A5378"/></g>'
          % (cx, cy, cx, cy, cx - 76, cy, cx - 12, cx + 12, cy, cx + 76, cx, cy - 76, cy - 12, cx, cy + 12, cy + 76))
    # converging track of the beacon
    rnd = random.Random(3)
    pts = []
    for i in range(90):
        r = 56 * math.exp(-i / 24.0)
        t = i * 0.26
        pts.append((cx + r * math.cos(t) + rnd.uniform(-1, 1), cy + r * math.sin(t) * 0.8 + rnd.uniform(-1, 1)))
    d.add('<path d="M%s" fill="none" stroke="%s" stroke-opacity=".75" stroke-width="1.3"/>'
          % (" L".join("%.1f %.1f" % p for p in pts), CYAN))
    d.add('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (cx, cy, CYAN))
    by = y0 + 184
    d.text(MONO, "RMS pointing error", x0 + 16, by - 6, 11, DIM)
    for i, (label, val, frac, color) in enumerate((("open loop", "6.45°", 1.0, CORAL), ("closed loop", "0.55°", 0.085, CYAN))):
        y = by + 10 + i * 26
        d.text(MONO, label, x0 + 16, y + 9, 12, MUTED)
        d.add('<rect x="%d" y="%d" width="%.1f" height="8" rx="2" fill="%s"/>' % (x0 + 104, y + 1, max(90 * frac, 4), color))
        d.text(MONOM, val, x0 + w - 16, y + 9, 12, PAPER, anchor="end")


def gec_inst(d):
    x0, y0, w, h = 312, 28, 260, 250
    inst_frame(d, x0, y0, w, h)
    sx, sy, sw, sh = x0 + 14, y0 + 16, w - 28, 150
    grid = "".join('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (sx + i * sw / 8, sy, sx + i * sw / 8, sy + sh) for i in range(1, 8))
    grid += "".join('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (sx, sy + i * sh / 6, sx + sw, sy + i * sh / 6) for i in range(1, 6))
    d.add('<g stroke="#18263D">%s</g>' % grid)
    d.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#27395A"/>' % (sx, sy + sh / 2, sx + sw, sy + sh / 2))
    for amp, color, ph in ((58, CYAN, 0), (30, AMBER, 0.35)):
        pts = ["%.1f %.1f" % (sx + i, sy + sh / 2 - amp * math.sin(i / sw * 4 * math.pi - ph)) for i in range(0, sw + 1, 3)]
        d.add('<path d="M%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (" L".join(pts), color))
    lamp(d, sx + 8, sy + 12, CYAN, 3)
    d.text(MONO, "V", sx + 16, sy + 16, 11, MUTED)
    lamp(d, sx + 34, sy + 12, AMBER, 3)
    d.text(MONO, "I", sx + 42, sy + 16, 11, MUTED)
    d.text(MONOM, "P = V × I", x0 + 16, y0 + 196, 14, PAPER)
    x = x0 + 16
    for s in ("ESP32", "ACS712", "ZMPT101B"):
        x += chip(d, s, x, y0 + 210, size=11, h=22, padx=7, fg=MUTED) + 6


def cards():
    card("card-awoken.svg", "Awoken", "Early-stage venture", AMBER,
         "AI follow-up that brings unanswered real-estate leads back over WhatsApp, then hands warm buyers to sales.",
         ["Next.js", "TypeScript", "Supabase"], "awoken.in ↗", awoken_inst,
         "AI follow-up for real-estate sales teams. Example WhatsApp conversation ending in a handoff to sales.")
    card("card-margin402.svg", "Margin402", "Hackathon prototype", AMBER,
         "An agent pays one fixed price for a verified result instead of paying for every failed attempt.",
         ["x402", "Algorand", "Redis"], "live demo ↗", margin_inst,
         "Testnet run: Draft 5 of 8 tests, Repair 7 of 8 twice, Premium 8 of 8. Contract $1.20, spent $1.28, $0.08 absorbed.")
    card("card-fsoc.svg", "FSOC", "Simulation, SIH 2026", CYAN,
         "Camera-only pointing for a moving optical terminal. A C++20 loop that detects, tracks and steers.",
         ["C++20", "OpenCV", "ONNX"], "source ↗", fsoc_inst,
         "Simulated RMS pointing error falls from 6.45 degrees open loop to 0.55 degrees closed loop.")
    card("card-gec.svg", "GEC Platform", "Interactive explainer", CYAN,
         "An ESP32 energy-monitoring rig, explained through interactive 3D scenes, waveforms and a schematic.",
         ["Three.js", "Next.js"], "live ↗", gec_inst,
         "Voltage and current waveforms from an ESP32, ACS712 and ZMPT101B monitoring rig.")


# ---- section headers (transparent, dark + light) -----------------------------
def header(file, title, note):
    d = Doc(1200, 84, title, note)
    tw = d.text(HEAD, title, 4, 56, 46, PAPER)
    nw = MONO.width(note, 14)
    x1, x2 = 4 + tw + 24, 1196 - nw - 20
    ticks = "".join('<line x1="%d" y1="%d" x2="%d" y2="48"/>' % (x, 48 - (10 if (x - x1) % 60 == 0 else 5), x) for x in range(int(x1), int(x2), 12))
    d.add('<line x1="%d" y1="48" x2="%d" y2="48" stroke="%s"/><g stroke="%s">%s</g>' % (x1, x2, RULE, RULE, ticks))
    d.add('<circle cx="%d" cy="48" r="3.5" fill="%s"/>' % (x2, AMBER))
    d.text(MONO, note, 1196, 53, 14, MUTED, anchor="end")
    save(d, file.replace(".svg", "-dark.svg"))
    s = lighten(d.svg())
    open(os.path.join(OUT, file.replace(".svg", "-light.svg")), "w").write(s)


def headers():
    header("h-work.svg", "Selected work", "4 builds")
    header("h-oss.svg", "Open source", "3 merged, 2 open")
    header("h-more.svg", "Other builds", "earlier and smaller")
    header("h-tools.svg", "Toolbox", "used in the repos above")
    header("h-how.svg", "How I work", "one loop, repeated")


# ---- open source logbook -------------------------------------------------------
OSS = [
    ("HADES CLI", "#32", "Rust", True, "Restored native text selection by removing global mouse capture from the TUI"),
    ("HADES CLI", "#30", "Rust", True, "Conversation import and export across HADES, ChatGPT, Claude and Markdown"),
    ("awesome-ai-apps", "#317", "Python", True, "Closed a credentialed wildcard CORS hole with an allow-list that fails closed"),
    ("Node.js", "#66376", "C++", False, "Backport of two V8 fixes for a WebAssembly wrapper lifetime race"),
    ("LLMVault", "#44", "Python", False, "Brute-force guard for flag submissions: cooldown after five misses, HTTP 429"),
]


def logbook():
    rh = 62
    d = Doc(1200, 40 + rh * len(OSS) + 12, "Open source contributions",
            "; ".join("%s %s (%s, %s): %s" % (r, n, l, "merged" if m else "open", t) for r, n, l, m, t in OSS))
    body(d, fill=PANEL, grid=False)
    d.text(MONO, "Status", 36, 34, 12, DIM)
    d.text(MONO, "Project", 132, 34, 12, DIM)
    d.text(MONO, "Change", 390, 34, 12, DIM)
    d.text(MONO, "Language", 1164, 34, 12, DIM, anchor="end")
    for i, (repo, num, lang, merged, text) in enumerate(OSS):
        y = 44 + i * rh
        d.add('<line x1="24" y1="%d" x2="1176" y2="%d" stroke="%s"/>' % (y, y, RULE))
        c = CYAN if merged else AMBER
        lamp(d, 42, y + rh / 2, c, 4)
        d.text(MONO, "merged" if merged else "open", 56, y + rh / 2 + 5, 13, c)
        w = d.text(SANSM, repo, 132, y + rh / 2 + 6, 18, PAPER)
        d.text(MONO, num, 132 + w + 8, y + rh / 2 + 6, 14, MUTED)
        d.text(SANS, text, 390, y + rh / 2 + 6, 16, MUTED)
        d.text(MONO, lang, 1164, y + rh / 2 + 5, 13, MUTED, anchor="end")
    border(d)
    save(d, "oss.svg")


# ---- toolbox -------------------------------------------------------------------
TOOLS = [
    ("Languages", ["TypeScript", "Python", "C++", "JavaScript", "Rust"]),
    ("Product", ["Next.js", "React", "Tailwind", "Three.js", "Framer Motion"]),
    ("Vision", ["OpenCV DNN", "ONNX", "CMake"]),
    ("Data and infra", ["Supabase", "PostgreSQL", "Redis", "MySQL", "AWS Lambda"]),
    ("Agents and payments", ["x402", "Algorand"]),
]


def toolbox():
    rh = 46
    d = Doc(1200, 28 + rh * len(TOOLS) + 14, "Toolbox",
            "; ".join("%s: %s" % (g, ", ".join(t)) for g, t in TOOLS))
    body(d, grid=False)
    for i, (group, tools) in enumerate(TOOLS):
        y = 26 + i * rh
        d.text(SANSM, group, 36, y + 22, 16, MUTED)
        x = 260
        for t in tools:
            x += chip(d, t, x, y + 3, size=14, h=30, padx=12) + 10
    border(d)
    save(d, "toolbox.svg")


# ---- how I work ----------------------------------------------------------------
def howiwork():
    d = Doc(1200, 210, "How I work",
            "Understand the problem, build the smallest useful version, test it against reality, fix the right layer, and repeat.")
    body(d, grid=False)
    steps = ["Understand the problem", "Build the smallest useful version", "Test it against reality", "Fix the right layer"]
    xs = [150 + i * 300 for i in range(4)]
    y = 98
    d.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (xs[0], y, xs[-1], y, RULE))
    d.add('<path d="M%d %d C %d %d, %d %d, %d %d" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="4 6"/>'
          % (xs[-1], y, xs[-1], y - 70, xs[0], y - 70, xs[0], y, AMBER))
    d.add('<rect x="566" y="%d" width="68" height="20" fill="%s"/>' % (y - 63, PANEL))
    d.text(MONO, "repeat", 600, y - 48, 12, AMBER, anchor="middle")
    for i, (x, s) in enumerate(zip(xs, steps)):
        color = CYAN if i == 2 else AMBER
        d.add('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, PANEL, color))
        lines = d.wrap(SANSM, s, 19, 230)
        for j, l in enumerate(lines):
            d.text(SANSM, l, x, y + 44 + j * 26, 19, PAPER, anchor="middle")
    border(d)
    save(d, "how.svg")


# ---- footer --------------------------------------------------------------------
def footer():
    d = Doc(1200, 190, "Contact",
            "Working on something that has to work outside the demo? Email kirtan120007@gmail.com.")
    body(d, rx=22, fill=INK)
    d.text(HEAD, "Building something that has to work outside the demo?", 48, 96, 50, PAPER)
    d.text(SANS, "I'd like to hear about it. kirtan120007@gmail.com", 50, 140, 20, MUTED)
    border(d, 22)
    save(d, "footer.svg")


hero(); cards(); headers(); logbook(); toolbox(); howiwork(); footer()
