"""Star chart: every day with contributions becomes a star.

Standard library only, so the daily workflow needs no installs.
"""
import datetime as dt
import re
import urllib.request

from theme import THEMES, W, star, style, svg, write

USER = "Kqwaiyi"
CELL = 14
GRID_X = (W - 53 * CELL) // 2
GRID_Y = 72
H = 230


def fetch():
    req = urllib.request.Request(
        f"https://github.com/users/{USER}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (star-chart)"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    cells = {}
    for m in re.finditer(r'<td[^>]*?data-date="([\d-]+)"[^>]*?id="contribution-day-component-(\d+)-(\d+)"[^>]*?data-level="(\d)"', html):
        date, row, col, level = m.groups()
        cells[f"contribution-day-component-{row}-{col}"] = {
            "date": dt.date.fromisoformat(date), "row": int(row), "col": int(col), "level": int(level), "count": 0,
        }
    for m in re.finditer(r'for="(contribution-day-component-\d+-\d+)"[^>]*>(\d+) contributions? on', html):
        if m.group(1) in cells:
            cells[m.group(1)]["count"] = int(m.group(2))
    return list(cells.values())


def chart(days, t, mode):
    total = sum(d["count"] for d in days)
    lit = sorted((d for d in days if d["level"]), key=lambda d: d["date"])
    extra = (
        "@keyframes twinkle{0%,100%{opacity:1;}50%{opacity:.4;}}"
        ".tw{animation:twinkle 3.6s ease-in-out infinite;}"
    )

    def center(d):
        return GRID_X + d["col"] * CELL + CELL / 2, GRID_Y + d["row"] * CELL + CELL / 2

    dust = "".join(
        f'<circle cx="{center(d)[0]:.1f}" cy="{center(d)[1]:.1f}" r="1.3" class="c-muted" opacity=".3"/>'
        for d in days if not d["level"]
    )
    stars = ""
    for i, d in enumerate(lit):
        x, y = center(d)
        r = 3 + d["level"] * 0.9
        fill = t["star"] if d["level"] >= 3 else t["primary"]
        stars += star(x, y, r, fill, "tw", f'style="animation-delay:{(i * 0.37) % 3.6:.2f}s"')

    months, seen = "", None
    for d in sorted((d for d in days if d["row"] == 0), key=lambda d: d["col"]):
        m = d["date"].month
        if seen is not None and m != seen and d["col"] < 51:
            months += (
                f'<text x="{GRID_X + d["col"] * CELL}" y="{GRID_Y + 7 * CELL + 24}" '
                f'class="t-small c-muted">{d["date"].strftime("%b")}</text>'
            )
        seen = m

    title = f"{total:,} star{'s' if total != 1 else ''} collected"
    body = f"""{style(t, extra=extra)}
<text x="{GRID_X}" y="36" class="t-body c-ink">{title}</text>
<text x="{GRID_X + 53 * CELL}" y="36" text-anchor="end" class="t-small c-muted">{len(lit)} bright days in the past year</text>
{dust}{stars}{months}"""
    return svg(W, H, body, f"Star chart — {title}")


if __name__ == "__main__":
    days = fetch()
    if not days:
        raise SystemExit("no contribution data parsed")
    for mode, t in THEMES.items():
        write(f"stars-{mode}.svg", chart(days, t, mode))
    print(f"star chart: {len(days)} days, {sum(d['count'] for d in days)} contributions")
