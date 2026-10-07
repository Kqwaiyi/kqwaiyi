"""Builds the static README art: banner, Personal Info and footer.

Nothing sits in a panel: every block draws straight onto GitHub's own page,
and the facts are labelled stars joined into constellations.

Requires: pip install fonttools brotli   (used only to measure text)
"""
import re

from fontTools.ttLib import TTFont

from theme import MEDIA, THEMES, TYPE, W, b64, star, style, svg, write

PROFILE = {
    "name": "Steven",
    "tagline": ["2nd Year Software Engineering Student,", "Aspiring Software Engineer."],
    "full_name": "Steven Fernando Goenawan",
    "focus": "Full-stack web development",
    "hobbies": "Valorant — Immortal, Piano",
    "stack": ["HTML", "CSS", "JavaScript", "TypeScript", "React", "Python", "Git"],
}

ICONS = {"HTML": "html5"}  # Simple Icons slug when it isn't just the lowercased name

TWINKLE = (
    "@keyframes twinkle{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.35;transform:scale(.7);}}"
    ".tw{transform-box:fill-box;transform-origin:center;animation:twinkle 3.2s ease-in-out infinite;}"
)

_fonts = {}


def text_width(text, kind):
    size, weight = TYPE[kind]
    if weight not in _fonts:
        _fonts[weight] = TTFont(MEDIA / f"zen-maru-{weight}.woff2")
    f = _fonts[weight]
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    units = sum(hmtx[cmap[ord(ch)]][0] for ch in text if ord(ch) in cmap)
    return units * size / upm


def icon(name, x, y, size, fill):
    file = ICONS.get(name, name.lower())
    d = re.search(r'd="([^"]+)"', (MEDIA / "icons" / f"{file}.svg").read_text()).group(1)
    return f'<path transform="translate({x},{y}) scale({size / 24})" fill="{fill}" d="{d}"/>'


def image(name):
    return f"data:image/webp;base64,{b64(MEDIA / name)}"


def fade_mask(id_, y1, y2):
    """Fades art out between y1 and y2 so it sinks into the page."""
    return (
        f'<linearGradient id="{id_}g" x1="0" y1="{y1}" x2="0" y2="{y2}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="{id_}"><rect x="0" y="0" width="{W}" height="{y2}" fill="url(#{id_}g)"/></mask>'
    )


def link(t, pts, opacity=".55"):
    """A thin constellation line through the given points."""
    p = " ".join(f"{x},{y}" for x, y in pts)
    return (
        f'<polyline points="{p}" fill="none" stroke="{t["primary"]}" stroke-opacity="{opacity}" '
        f'stroke-width="1" stroke-linejoin="round"/>'
    )


def twinkles(t, pts):
    return "".join(star(x, y, r, t["star"], "tw", f'style="animation-delay:{d}s"') for x, y, r, d in pts)


# ---------------------------------------------------------------- banner

def banner(t, mode):
    H = 440
    img_h = H
    img_w = round(610 * img_h / 600)
    img_x = W - img_w
    face = (img_x + round(300 * img_w / 610), 196)
    extra = TWINKLE + (
        "@keyframes spin{to{transform:rotate(360deg);}}"
        f".ring{{transform-origin:{face[0]}px {face[1]}px;animation:spin 80s linear infinite;}}"
    )
    con = [(48, 120), (150, 96), (238, 130), (330, 104)]
    body = f"""{style(t, (500, 900), extra)}
<defs>{fade_mask("sink", H - 110, H)}</defs>
<circle cx="{face[0]}" cy="{face[1]}" r="186" fill="none" stroke="{t['primary']}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="1 9" stroke-linecap="round" class="ring"/>
<circle cx="{face[0]}" cy="{face[1]}" r="146" fill="none" stroke="{t['primary']}" stroke-opacity=".22" stroke-width="1"/>
<image x="{img_x}" y="0" width="{img_w}" height="{img_h}" mask="url(#sink)" href="{image('itsuki-banner.webp')}"/>
{link(t, con)}
{twinkles(t, [(x, y, r, d) for (x, y), r, d in zip(con, (7, 5, 8, 5), (0, 1.1, 2.0, .5))])}
<text x="44" y="240" class="t-display c-ink">{PROFILE['name']}</text>
<text x="48" y="280" class="t-body c-muted">{PROFILE['tagline'][0]}</text>
<text x="48" y="304" class="t-body c-muted">{PROFILE['tagline'][1]}</text>
{twinkles(t, [(800, 60, 7, .8), (806, 320, 8, 2.4), (470, 400, 5, 1.2)])}"""
    return svg(W, H, body, f"{PROFILE['name']} — Itsuki Nakano banner")


# ---------------------------------------------------------------- Personal Info

def card(t, mode):
    H = 300
    facts = [
        ((48, 58), 9, "Name", PROFILE["full_name"]),
        ((96, 150), 7, "Focus", PROFILE["focus"]),
        ((58, 242), 7, "Hobbies", PROFILE["hobbies"]),
    ]
    out = [link(t, [p for p, *_ in facts])]
    for (x, y), r, label, value in facts:
        out.append(star(x, y, r, t["star"]))
        out.append(f'<text x="{x + 20}" y="{y + 1}" class="t-body c-ink">{value}</text>')
        out.append(f'<text x="{x + 20}" y="{y + 22}" class="t-small c-muted">{label}</text>')

    # the stack is its own constellation; labels sit on the side away from the lines
    sky = [("HTML", 482, 52, "r"), ("CSS", 590, 96, "r"), ("JavaScript", 690, 46, "r"),
           ("TypeScript", 800, 128, "l"), ("React", 742, 214, "l"), ("Python", 600, 250, "r"), ("Git", 470, 178, "r")]
    out.append(link(t, [(x, y) for _, x, y, _ in sky] + [sky[0][1:3]], ".4"))
    for name, x, y, side in sky:
        out.append(star(x, y, 5, t["primary"]))
        w = 16 + 6 + text_width(name, "small")
        lx = x + 14 if side == "r" else x - 14 - w
        out.append(icon(name, lx, y - 8, 16, t["deep"]))
        out.append(f'<text x="{lx + 22:.1f}" y="{y + 5}" class="t-small c-ink">{name}</text>')

    return svg(W, H, style(t) + "".join(out), f"Personal Info — {PROFILE['full_name']}")


# ---------------------------------------------------------------- footer

def footer(t, mode):
    H = 210
    pw = 200
    ph = round(523 * pw / 540)
    extra = TWINKLE + "@keyframes bob{0%,100%{transform:translateY(0);}50%{transform:translateY(7px);}}.peek{animation:bob 4s ease-in-out infinite;}"
    a, b = (W / 2 - 170, 52), (W / 2 + 170, 52)
    body = f"""{style(t, (500,), extra)}
<defs><clipPath id="edge"><rect width="{W}" height="{H}"/></clipPath>{fade_mask("sink", H - 30, H)}</defs>
{link(t, [a, (W / 2 - 112, 52)], ".5")}{link(t, [(W / 2 + 112, 52), b], ".5")}
{twinkles(t, [(*a, 6, 0), (*b, 6, 1.4)])}
<text x="{W / 2}" y="57" text-anchor="middle" class="t-small c-muted">see you in the next commit</text>
<g clip-path="url(#edge)" mask="url(#sink)"><g class="peek">
  <image x="{(W - pw) / 2}" y="{H - 168}" width="{pw}" height="{ph}" href="{image('itsuki-peek.webp')}"/>
</g></g>"""
    return svg(W, H, body, "Itsuki waving goodbye")


if __name__ == "__main__":
    for mode, t in THEMES.items():
        write(f"banner-{mode}.svg", banner(t, mode))
        write(f"card-{mode}.svg", card(t, mode))
        write(f"footer-{mode}.svg", footer(t, mode))
    print("built banner, card, footer")
