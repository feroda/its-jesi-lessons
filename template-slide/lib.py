"""Piccola libreria per generare le slide SVG nello stile del deck Docker."""
from xml.sax.saxutils import escape
import os

INK = "#1F2933"
INK2 = "#3E4C59"
GREY = "#52606D"
PAPER = "#F6F3EC"
DOCKER = "#2496ED"
NAVY = "#1C64C8"
GRAFANA = "#E8590C"
LOKI = "#1C64C8"
ALLOY = "#2F9E44"
PROM = "#C92A2A"
TEAL = "#0C8599"
AMBER = "#B7791F"
PINK = "#C2255C"
PURPLE = "#6741D9"
MONO = "DejaVu Sans Mono, monospace"

LIGHT = {GRAFANA: "#FFF4E6", LOKI: "#E7F0FD", ALLOY: "#EBFBEE", PROM: "#FFF5F5",
         DOCKER: "#DCEFFD", TEAL: "#E3FAFC", AMBER: "#FFF9DB", PURPLE: "#F3F0FF",
         GREY: "#FFFFFF", INK: "#FFFFFF", PINK: "#FFF0F6"}

DEFS = """<defs>
""" + "".join(
    f'<marker id="a{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>\n'
    for k, c in [("K", INK), ("G", ALLOY), ("O", GRAFANA), ("T", TEAL), ("A", AMBER),
                 ("R", PROM), ("D", DOCKER), ("B", NAVY), ("Y", GREY), ("P", PURPLE)]) + "</defs>\n"
MARK = {INK: "K", ALLOY: "G", GRAFANA: "O", TEAL: "T", AMBER: "A", PROM: "R",
        DOCKER: "D", NAVY: "B", GREY: "Y", PURPLE: "P"}


def page(body, side=False):
    head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" '
            'font-family="Atkinson Hyperlegible, DejaVu Sans, Arial, sans-serif">\n' + DEFS +
            f'<rect width="1600" height="900" fill="{PAPER}"/>\n')
    if side:
        head += f'<rect x="0" y="0" width="28" height="900" fill="{NAVY}"/><rect x="28" y="0" width="10" height="900" fill="{DOCKER}"/>\n'
    else:
        head += f'<rect x="0" y="0" width="1600" height="10" fill="{DOCKER}"/>\n'
    return head + "".join(body) + "</svg>\n"


def t(x, y, s, size=30, color=INK, bold=False, anchor="start", mono=False, italic=False):
    a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{color}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if mono:
        a.append(f'font-family="{MONO}"')
    return f'<text xml:space="preserve" {" ".join(a)}>{escape(s)}</text>\n'


def h(title, sub=None):
    out = t(70, 100, title, 52, INK, True)
    if sub:
        out += t(70, 152, sub, 27, GREY)
    return out


def rect(x, y, w, hh, fill="#FFFFFF", stroke=None, sw=3, rx=14, dash=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="{rx}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>\n"


def code(x, y, w, lines, size=26, lh=None, dark=False, pad=36):
    """lines: str oppure (testo, colore, grassetto)."""
    lh = lh or int(size * 1.6)
    hh = pad * 2 + lh * (len(lines) - 1) + size
    out = rect(x, y, w, hh, INK if dark else "#FFFFFF", None if dark else INK2, 3)
    yy = y + pad + int(size * 0.8)
    ys = []
    for ln in lines:
        ys.append(yy)
        if isinstance(ln, str):
            ln = (ln, "#FFFFFF" if dark else INK, False)
        txt, col, b = (list(ln) + [False])[:3]
        out += t(x + 32, yy, txt, size, col, b, mono=True)
        yy += lh
    return out, y + hh, ys


def step(n, y, cmd, note=None, x=110, size=32, color=DOCKER, mono=True, note_x=1530):
    out = f'<circle cx="{x}" cy="{y - 12}" r="26" fill="{color}"/>'
    out += t(x, y - 2, str(n), 28, "#FFFFFF", True, "middle")
    out += t(x + 55, y, cmd, size, INK, True, mono=mono)
    if note:
        out += t(note_x, y, note, 28, INK2, anchor="end")
    return out


def box(x, y, w, hh, color, label, size=34, sub=None, subsize=24, fill=None):
    out = rect(x, y, w, hh, fill or LIGHT.get(color, "#FFFFFF"), color, 3, 12)
    cy = y + hh / 2 + size * 0.35 - (subsize * 0.7 if sub else 0)
    out += t(x + w / 2, cy, label, size, color, True, "middle")
    if sub:
        out += t(x + w / 2, cy + subsize * 1.5, sub, subsize, GREY, anchor="middle")
    return out


def arrow(x1, y1, x2, y2, color=INK, w=5, dash=None, both=False):
    m = MARK.get(color, "K")
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#a{m})"'
    if both:
        s += f' marker-start="url(#a{m})"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + "/>\n"


def pill(x, y, w, label, color, size=28, hh=60):
    return rect(x, y, w, hh, color, rx=10) + t(x + w / 2, y + hh / 2 + size * 0.36, label, size, "#FFFFFF", True, "middle")


def bullets(x, y, items, size=34, gap=None, color=INK, dot=DOCKER):
    gap = gap or int(size * 2)
    out = ""
    for it in items:
        out += f'<circle cx="{x}" cy="{y - size * 0.32}" r="9" fill="{dot}"/>'
        out += t(x + 30, y, it, size, color)
        y += gap
    return out


def note(y, s, size=30, color=INK, bold=True, x=70):
    return t(x, y, s, size, color, bold)


def titlepage(lesson, l1, l2, art=""):
    body = [
        t(110, 250, lesson, 30, DOCKER, True),
        t(110, 350, l1, 96, INK, True),
        t(110, 460, l2, 96, INK, True),
        rect(114, 500, 180, 10, DOCKER, rx=5),
        t(110, 590, "ITS CyberSecurity - Jesi (AN) 2026/2027", 36, INK),
        t(110, 645, "Corso Logging, Monitoring, Troubleshooting", 28, GREY),
        t(110, 790, "prof. Luca Ferroni", 34, NAVY, True),
        art,
    ]
    return page(body, side=True)


def save(outdir, slides):
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith(".svg"):
            os.remove(os.path.join(outdir, f))
    for i, (name, svg) in enumerate(slides):
        with open(os.path.join(outdir, f"slide{i}-{name}.svg"), "w") as fh:
            fh.write(svg)
    print(outdir, len(slides), "slide")
