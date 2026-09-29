"""Builds the static README art: banner, student ID card and footer.

Requires: pip install fonttools brotli   (used only to measure text)
"""
import re

from fontTools.ttLib import TTFont

from theme import MEDIA, THEMES, TYPE, W, b64, star, style, svg, write

PROFILE = {
    "name": "Kqwaiyi",
    "tagline": ["Making games with Godot,", "one star at a time."],
    "enrolled": "Jul 2020",
    "currently": "Building Companix",
    "stack": ["Godot", "GDScript", "JavaScript", "HTML"],
}

_fonts = {}


def text_width(text, kind):
    size, weight, ls = TYPE[kind]
    if weight not in _fonts:
        _fonts[weight] = TTFont(MEDIA / f"zen-maru-{weight}.woff2")
    f = _fonts[weight]
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    units = sum(hmtx[cmap[ord(ch)]][0] for ch in text if ord(ch) in cmap)
    return units * size / upm + ls * len(text)


def icon(name, x, y, size, fill):
    if name == "GDScript":  # no brand mark exists; a quiet code glyph instead
        s = size / 24
        return (
            f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{fill}" '
            f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M8 6l-6 6 6 6M16 6l6 6-6 6M13.5 4l-3 16"/></g>'
        )
    file = {"Godot": "godotengine", "JavaScript": "javascript", "HTML": "html5"}[name]
    d = re.search(r'd="([^"]+)"', (MEDIA / "icons" / f"{file}.svg").read_text()).group(1)
    return f'<path transform="translate({x},{y}) scale({size / 24})" fill="{fill}" d="{d}"/>'


# ---------------------------------------------------------------- banner

def banner(t, mode):
    H = 440
    img_h = H
    img_w = round(610 * img_h / 600)
    img_x = W - img_w
    face = (img_x + round(300 * img_w / 610), 196)
    extra = (
        "@keyframes spin{to{transform:rotate(360deg);}}"
        f".ring{{transform-origin:{face[0]}px {face[1]}px;animation:spin 60s linear infinite;}}"
        "@keyframes twinkle{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.35;transform:scale(.7);}}"
        ".tw{transform-box:fill-box;transform-origin:center;animation:twinkle 3.2s ease-in-out infinite;}"
    )
    stars = [(468, 92, 11, 0), (792, 64, 7, 0.8), (370, 58, 6, 1.6), (800, 300, 9, 2.4), (486, 396, 6, 1.2)]
    tw = "".join(
        star(x, y, r, t["star"], "tw", f'style="animation-delay:{d}s"') for x, y, r, d in stars
    )
    body = f"""{style(t, (500, 700, 900), extra)}
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
  <radialGradient id="glow" cx="{face[0]}" cy="{face[1] + 40}" r="300" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['primary']}" stop-opacity="{0.30 if mode == 'light' else 0.22}"/>
    <stop offset="1" stop-color="{t['primary']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="tone" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <circle cx="5" cy="5" r="1.7" fill="{t['primary']}"/>
  </pattern>
  <linearGradient id="fade" x1="340" y1="{H}" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="toneMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" class="c-bg"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect width="{W}" height="{H}" fill="url(#tone)" mask="url(#toneMask)" opacity="{0.32 if mode == 'light' else 0.22}"/>
  <circle cx="{face[0]}" cy="{face[1]}" r="176" fill="none" stroke="{t['primary']}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="1 9" stroke-linecap="round" class="ring"/>
  <circle cx="{face[0]}" cy="{face[1]}" r="136" fill="none" stroke="{t['primary']}" stroke-opacity=".25" stroke-width="1"/>
  <image x="{img_x}" y="0" width="{img_w}" height="{img_h}" href="data:image/webp;base64,{b64(MEDIA / 'itsuki-banner.webp')}"/>
  {tw}
  <rect x="56" y="140" width="32" height="4" rx="2" class="c-primary"/>
  <text x="56" y="176" class="t-label c-deep">HELLO, I'M</text>
  <text x="52" y="236" class="t-display c-ink">{PROFILE['name']}</text>
  <text x="56" y="276" class="t-body c-muted">{PROFILE['tagline'][0]}</text>
  <text x="56" y="300" class="t-body c-muted">{PROFILE['tagline'][1]}</text>
  <text x="56" y="{H - 44}" class="t-label c-muted">NO.05 · 中野五月</text>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="27.25" fill="none" stroke="{t['line']}" stroke-width="1.5"/>"""
    return svg(W, H, body, "Kqwaiyi — Itsuki Nakano banner")


# ---------------------------------------------------------------- ID card

def card(t, mode):
    H = 300
    px, py, pw, ph = 32, 88, 148, 180
    col1, col2 = 212, 420

    chips, x = [], col1
    for name in PROFILE["stack"]:
        w = round(14 + 16 + 8 + text_width(name, "small") + 16)
        chips.append(
            f'<rect x="{x}" y="236" width="{w}" height="32" rx="16" class="c-surface" stroke="{t["line"]}"/>'
            + icon(name, x + 14, 244, 16, t["primary"])
            + f'<text x="{x + 38}" y="256.5" class="t-small c-ink">{name}</text>'
        )
        x += w + 8

    seal_x, seal_y = 744, 150
    head_w = text_width("STUDENT ID", "label")
    body = f"""{style(t, (500, 700))}
<defs><clipPath id="photo"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16"/></clipPath></defs>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" class="c-bg" stroke="{t['line']}" stroke-width="1.5"/>
{star(38, 40, 6, t['star'])}
<text x="54" y="44" class="t-label c-deep">STUDENT ID</text>
<text x="{54 + head_w + 8}" y="44" class="t-small c-muted">学生証</text>
<text x="{W - 32}" y="44" text-anchor="end" class="t-label c-muted">NO. 2020-05</text>
<line x1="32" y1="64" x2="{W - 32}" y2="64" stroke="{t['line']}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
<g clip-path="url(#photo)">
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" class="c-surface"/>
  <image x="{px - 16}" y="{py}" width="{ph}" height="{ph}" preserveAspectRatio="xMidYMid slice" href="data:image/webp;base64,{b64(MEDIA / 'itsuki-card.webp')}"/>
</g>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="none" stroke="{t['primary']}" stroke-width="1.5"/>
<text x="{col1}" y="104" class="t-label c-muted">NAME</text>
<text x="{col1}" y="136" class="t-title c-ink">{PROFILE['name']}</text>
<text x="{col1}" y="176" class="t-label c-muted">ENROLLED</text>
<text x="{col1}" y="200" class="t-body c-ink">{PROFILE['enrolled']}</text>
<text x="{col2}" y="176" class="t-label c-muted">CURRENTLY</text>
<text x="{col2}" y="200" class="t-body c-ink">{PROFILE['currently']}</text>
{''.join(chips)}
<g transform="rotate(-12 {seal_x} {seal_y})" opacity=".9">
  <circle cx="{seal_x}" cy="{seal_y}" r="46" fill="none" stroke="{t['primary']}" stroke-width="3"/>
  <circle cx="{seal_x}" cy="{seal_y}" r="39" fill="none" stroke="{t['primary']}" stroke-width="1"/>
  <text x="{seal_x}" y="{seal_y - 4}" text-anchor="middle" class="t-title c-primary">五</text>
  <text x="{seal_x}" y="{seal_y + 22}" text-anchor="middle" class="t-title c-primary">月</text>
</g>"""
    return svg(W, H, body, "Student ID — Kqwaiyi")


# ---------------------------------------------------------------- footer

def footer(t, mode):
    H = 200
    base = 150
    pw = 190
    ph = round(523 * pw / 540)
    extra = (
        "@keyframes bob{0%,100%{transform:translateY(0);}50%{transform:translateY(7px);}}"
        ".peek{animation:bob 4s ease-in-out infinite;}"
        "@keyframes twinkle{0%,100%{opacity:1;}50%{opacity:.3;}}"
        ".tw{animation:twinkle 2.8s ease-in-out infinite;}"
    )
    body = f"""{style(t, (500,), extra)}
<defs><clipPath id="desk"><rect x="0" y="0" width="{W}" height="{base}"/></clipPath></defs>
<g clip-path="url(#desk)"><g class="peek">
  <image x="{(W - pw) / 2}" y="{base - 146}" width="{pw}" height="{ph}" href="data:image/webp;base64,{b64(MEDIA / 'itsuki-peek.webp')}"/>
</g></g>
{star(W / 2 - 128, 64, 8, t['star'], 'tw')}
{star(W / 2 + 122, 40, 6, t['star'], 'tw', 'style="animation-delay:1.4s"')}
<rect x="{W / 2 - 200}" y="{base}" width="400" height="5" rx="2.5" class="c-primary"/>
<text x="{W / 2}" y="{base + 38}" text-anchor="middle" class="t-small c-muted">see you in the next commit</text>"""
    return svg(W, H, body, "Itsuki waving goodbye")


if __name__ == "__main__":
    for mode, t in THEMES.items():
        write(f"banner-{mode}.svg", banner(t, mode))
        write(f"card-{mode}.svg", card(t, mode))
        write(f"footer-{mode}.svg", footer(t, mode))
    print("built banner, card, footer")
