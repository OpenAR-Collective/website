"""Generate the branded 1200x630 card image for a news article.

Usage:
    python scripts/news-image.py <output-slug>

Writes public/assets/news/<output-slug>.png. The image is the amber hex grid
brightening toward the upper right, matching the business plan cover, with the
horizontal wordmark centered.

Requires Pillow and the wordmark source in _Scratch. This is an authoring tool
run by hand; it is not part of the site build and ships nothing to the browser.
The images it produces are brand assets, governed by the Trademark Policy
rather than the repository's open licenses.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 1200, 630
NEAR_BLACK = (14, 13, 11)
AMBER = (232, 160, 32)
R = 52  # hex circumradius
WORDMARK_WIDTH = 800  # visible wordmark content width, after cropping padding

ROOT = Path(__file__).resolve().parent.parent
WORDMARK = ROOT / "_Scratch/OpenAR Single Hex/PNG/openar-single-hex-horizontal-dark-1120x216-transparency.png"


def hex_points(cx, cy):
    return [
        (cx + R * math.cos(math.radians(60 * k)), cy + R * math.sin(math.radians(60 * k)))
        for k in range(6)
    ]


def build():
    img = Image.new("RGB", (W, H), NEAR_BLACK)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Brightness falls off from the upper-right corner.
    focus = (W * 0.92, H * 0.08)
    reach = math.hypot(W, H) * 0.72
    step_y = math.sqrt(3) / 2 * R

    x = 0.0
    while x < W + 2 * R:
        offset = step_y if round(x / (1.5 * R)) % 2 else 0
        y = offset - 2 * step_y
        while y < H + 2 * step_y:
            t = max(0.0, 1 - math.hypot(x - focus[0], y - focus[1]) / reach)
            alpha = int(14 + (200 - 14) * (t**2.4))
            draw.polygon(hex_points(x, y), outline=(*AMBER, alpha), width=2)
            y += 2 * step_y
        x += 1.5 * R

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # The wordmark PNG carries transparent padding; crop to content so the
    # requested width describes the visible mark.
    mark = Image.open(WORDMARK).convert("RGBA")
    mark = mark.crop(mark.getbbox())
    height = round(mark.height * WORDMARK_WIDTH / mark.width)
    mark = mark.resize((WORDMARK_WIDTH, height), Image.LANCZOS)
    img.paste(mark, ((W - WORDMARK_WIDTH) // 2, (H - height) // 2), mark)

    return img


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/news-image.py <output-slug>")
    out = ROOT / "public/assets/news" / f"{sys.argv[1]}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    build().save(out, optimize=True)
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
