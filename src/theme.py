"""Design tokens shared by every generated SVG.

Every asset is drawn on an 840px-wide canvas and shown at 100% width in the
README, so 1 SVG unit ~= 1 CSS px on a desktop GitHub profile.
"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "src" / "media"
OUT = ROOT / "assets"
W = 840

FONT = "'Zen Maru Gothic', 'Hiragino Maru Gothic ProN', sans-serif"

# Type scale: (size px, weight, letter-spacing px). Nothing else is used.
TYPE = {
    "display": (56, 900, 0),   # profile name in the banner
    "title": (24, 700, 0),     # card titles and key values
    "body": (16, 500, 0),      # running text
    "small": (13, 500, 0),     # secondary text, chips
    "label": (11, 700, 2.2),   # uppercase eyebrow labels
}

THEMES = {
    "light": {
        "bg": "#FFF6F3",
        "surface": "#FDE9E5",
        "line": "#F4C9C3",
        "primary": "#F28A81",
        "deep": "#C2544B",
        "ink": "#3A2327",
        "muted": "#8C6B6F",
        "star": "#F7BE4F",
    },
    "dark": {
        "bg": "#1E1417",
        "surface": "#2B1C20",
        "line": "#4A2D33",
        "primary": "#F28A81",
        "deep": "#F6A59D",
        "ink": "#FBEDEA",
        "muted": "#B39498",
        "star": "#F7BE4F",
    },
}


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def style(t, weights=(500, 700), extra=""):
    faces = "".join(
        f"@font-face{{font-family:'Zen Maru Gothic';font-weight:{w};"
        f"src:url(data:font/woff2;base64,{b64(MEDIA / f'zen-maru-{w}.woff2')}) format('woff2');}}"
        for w in weights
    )
    types = "".join(
        f".t-{name}{{font-family:{FONT};font-size:{s}px;font-weight:{wt};letter-spacing:{ls}px;}}"
        for name, (s, wt, ls) in TYPE.items()
    )
    colors = "".join(f".c-{k}{{fill:{v};}}" for k, v in t.items())
    motion = "@media (prefers-reduced-motion:reduce){*{animation:none!important;}}"
    return f"<style>{faces}{types}{colors}{extra}{motion}</style>"


def star_points(cx, cy, r, inner=0.48, rot=-90):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 36)
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    return " ".join(pts)


def star(cx, cy, r, fill, cls="", extra=""):
    """Soft five-point star, like Itsuki's hair clips."""
    sw = max(r * 0.35, 0.8)
    c = f' class="{cls}"' if cls else ""
    return (
        f'<polygon{c} points="{star_points(cx, cy, r)}" fill="{fill}" stroke="{fill}" '
        f'stroke-width="{sw:.2f}" stroke-linejoin="round" {extra}/>'
    )


def svg(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">'
        f"<title>{title}</title>{body}</svg>\n"
    )


def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
