r"""Generate the branded 1200x630 card image for a news article.

Usage:
    python scripts/news-image.py <output-slug>
    python scripts/news-image.py <output-slug> --portrait <photo> --name "<Name>"

Writes public/assets/news/<output-slug>.png. The plain card is the amber hex
grid brightening toward the upper right, matching the business plan cover, with
the horizontal wordmark centered.

The portrait card is for board announcements. It keeps the same grid and puts
the person's photo in a gold-ringed hexagon on the right. The name and a
subtitle are set in Barlow on the left with the wordmark underneath, and that
text block is centered vertically on the card. This command reproduces the card
for John Erickson's seating:

    python scripts/news-image.py 2026-11-11-john-erickson-joins-board
        --portrait public/assets/board/JohnErickson.jpg
        --name "John Erickson" --fill-corners

(Run it as one line.) Remember to update imageAlt in the news post so it
describes the new card.

Portrait options:
    --name          The name on the card. It breaks onto two lines at the last
                    space. Write "First|Last" to choose the break yourself.
    --kicker        Small amber line above the name (default "NEW DIRECTOR").
    --subtitle      Line under the name (default "Joins the Board of Directors").
    --fill-corners  Paint the white corners of a photo that was cropped to a
                    circle, such as a LinkedIn profile photo, with the gray the
                    photo uses for its backdrop. Without it the hexagon crop of
                    such a photo shows white corners.
    --center-y      Where the hexagon is centered vertically on the photo, as a
                    fraction of its height (default 0.45). Raise it to show
                    more chin and lower it to show more headroom.

Requires Pillow and two sources in _Scratch: the wordmark and Barlow.zip. This
is an authoring tool run by hand; it is not part of the site build and ships
nothing to the browser. The images it produces are brand assets, governed by
the Trademark Policy rather than the repository's open licenses.
"""

import argparse
import io
import math
import zipfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H = 1200, 630
NEAR_BLACK = (14, 13, 11)
AMBER = (232, 160, 32)
R = 52  # hex circumradius
WORDMARK_WIDTH = 800  # visible wordmark content width, after cropping padding

ROOT = Path(__file__).resolve().parent.parent
WORDMARK = ROOT / "_Scratch/OpenAR Single Hex/PNG/openar-single-hex-horizontal-dark-1120x216-transparency.png"
BARLOW_ZIP = ROOT / "_Scratch/Barlow.zip"

# Portrait card.
OFFWHITE = (244, 239, 230)
SOFT = (200, 195, 186)
GOLD_DARK = (184, 112, 14)
RING_LIGHT = (255, 214, 110)
COS30 = math.cos(math.radians(30))
SS = 4  # supersampling factor for smooth shape edges
PHOTO_PAD = 120  # backdrop padding so crops may reach past the photo's edge
HEX_CX, HEX_CY, HEX_R = 905, 318, 170  # the portrait hexagon
TEXT_X = 135  # left edge of the text block
MAX_TEXT_W = HEX_CX - HEX_R - 40 - TEXT_X  # keeps 40px clear of the hexagon
NAME_SIZE = 112
KICKER_DEFAULT = "NEW DIRECTOR"
SUBTITLE_DEFAULT = "Joins the Board of Directors"


def hex_points(cx, cy, r=R):
    return [
        (cx + r * math.cos(math.radians(60 * k)), cy + r * math.sin(math.radians(60 * k)))
        for k in range(6)
    ]


def grid_background():
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

    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def load_wordmark(width):
    # The wordmark PNG carries transparent padding; crop to content so the
    # requested width describes the visible mark.
    mark = Image.open(WORDMARK).convert("RGBA")
    mark = mark.crop(mark.getbbox())
    height = round(mark.height * width / mark.width)
    return mark.resize((width, height), Image.LANCZOS)


def build():
    img = grid_background()
    mark = load_wordmark(WORDMARK_WIDTH)
    img.paste(mark, ((W - WORDMARK_WIDTH) // 2, (H - mark.height) // 2), mark)
    return img


# ---------------------------------------------------------------- portrait


def load_portrait(path, fill_corners):
    """Return the photo padded with its own backdrop color, and that pad size."""
    im = Image.open(path).convert("RGB")
    backdrop = im.getpixel((im.width // 2, 2))  # top center is backdrop in these photos
    if fill_corners:
        for pt in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
            ImageDraw.floodfill(im, pt, backdrop, thresh=26)
    padded = Image.new("RGB", (im.width + 2 * PHOTO_PAD, im.height + 2 * PHOTO_PAD), backdrop)
    padded.paste(im, (PHOTO_PAD, PHOTO_PAD))
    return padded, im.size


def crop_square(photo, center, half_src, size):
    """Crop a square around center (in original photo pixels) down to size x size."""
    cx, cy = center[0] + PHOTO_PAD, center[1] + PHOTO_PAD
    box = (cx - half_src, cy - half_src, cx + half_src, cy + half_src)
    return photo.resize((size, size), Image.LANCZOS, box=box)


def hex_mask(size, r):
    big = size * SS
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).polygon(hex_points(big / 2, big / 2, r * SS), fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def gradient(size, light, dark):
    """Diagonal gradient, light at the upper left and dark at the lower right."""
    g = Image.new("RGB", (size, size))
    pixels = []
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            pixels.append(tuple(round(light[i] + (dark[i] - light[i]) * t) for i in range(3)))
    g.putdata(pixels)
    return g


def glow(radius, strength):
    g = Image.radial_gradient("L")  # black at the center, white at the edge
    g = ImageChops.invert(g).resize((round(2 * radius), round(2 * radius)), Image.LANCZOS)
    g = g.point(lambda v: int(255 * ((v / 255) ** 2) * strength))
    layer = Image.new("RGBA", g.size, (*AMBER, 0))
    layer.putalpha(g)
    return layer


def paste_center(base, layer, cx, cy):
    base.paste(layer, (round(cx - layer.width / 2), round(cy - layer.height / 2)), layer)


def hex_portrait(base, photo, photo_size, center_y, ring=5, gap=5):
    """Photo cropped to a hexagon with a gold ring and a thin dark gap."""
    size = 2 * round(HEX_R) + 8
    paste_center(base, glow(HEX_R * 1.9, 0.26), HEX_CX, HEX_CY)

    ring_mask = ImageChops.subtract(hex_mask(size, HEX_R), hex_mask(size, HEX_R - ring / COS30))
    ring_img = gradient(size, RING_LIGHT, GOLD_DARK).convert("RGBA")
    ring_img.putalpha(ring_mask)
    paste_center(base, ring_img, HEX_CX, HEX_CY)

    # The crop is sized from the photo's width: a hexagon with a circumradius of
    # 46.5 percent of the width fits inside the circular backdrop of a profile photo.
    width, height = photo_size
    src_r = width * 186 / 400
    r_photo = HEX_R - (ring + gap) / COS30
    scale = r_photo / src_r
    crop = crop_square(photo, (width / 2, height * center_y), (size / 2) / scale, size).convert("RGBA")
    crop.putalpha(hex_mask(size, r_photo))
    paste_center(base, crop, HEX_CX, HEX_CY)


_font_zip = None


def barlow(weight, size):
    global _font_zip
    if _font_zip is None:
        _font_zip = zipfile.ZipFile(BARLOW_ZIP)
    data = io.BytesIO(_font_zip.read(f"Barlow-{weight}.ttf"))
    return ImageFont.truetype(data, size)


def fit(text, weight, size, max_width):
    """Largest Barlow font at or below size that keeps text within max_width."""
    font = barlow(weight, size)
    while font.getlength(text) > max_width and size > 12:
        size -= 2
        font = barlow(weight, size)
    return font


def draw_tracked(draw, x, y, text, font, fill, tracking):
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + tracking


def split_name(name):
    if "|" in name:
        return [part.strip() for part in name.split("|")]
    first, sep, last = name.rpartition(" ")
    return [first, last] if sep else [name]


def build_portrait(photo_path, name, kicker, subtitle, fill_corners, center_y):
    img = grid_background()
    photo, photo_size = load_portrait(photo_path, fill_corners)
    hex_portrait(img, photo, photo_size, center_y)
    draw = ImageDraw.Draw(img)

    lines = split_name(name)
    name_font = barlow("SemiBold", NAME_SIZE)
    widest = max(lines, key=name_font.getlength)
    name_font = fit(widest, "SemiBold", NAME_SIZE, MAX_TEXT_W)
    scale = name_font.size / NAME_SIZE
    pitch = round(110 * scale)  # baseline to baseline, and kicker to first line
    sub_gap = round(58 * scale)  # last name line to subtitle
    sub_font = fit(subtitle, "Medium", 34, MAX_TEXT_W)
    kicker_font = barlow("SemiBold", 24)

    # Offsets from the kicker baseline. The block runs from the top of the
    # kicker to the bottom of the wordmark, and sits centered on the card.
    last_line = pitch * len(lines)
    sub_base = last_line + sub_gap
    mark_bottom = sub_base + 110
    mark = load_wordmark(340)
    top_rel = kicker_font.getbbox(kicker, anchor="ls")[1]  # negative: above the baseline
    k = round((H - (mark_bottom - top_rel)) / 2 - top_rel)

    draw_tracked(draw, TEXT_X, k, kicker, kicker_font, AMBER, 5)
    for i, line in enumerate(lines, start=1):
        draw.text((TEXT_X, k + pitch * i), line, font=name_font, fill=OFFWHITE, anchor="ls")
    draw.text((TEXT_X, k + sub_base), subtitle, font=sub_font, fill=SOFT, anchor="ls")
    img.paste(mark, (TEXT_X, k + mark_bottom - mark.height), mark)
    return img


def main():
    parser = argparse.ArgumentParser(description="Generate a news card image.")
    parser.add_argument("slug", help="output name, written to public/assets/news/<slug>.png")
    parser.add_argument("--portrait", type=Path, help="photo for a portrait card")
    parser.add_argument("--name", help="name on a portrait card")
    parser.add_argument("--kicker", default=KICKER_DEFAULT)
    parser.add_argument("--subtitle", default=SUBTITLE_DEFAULT)
    parser.add_argument("--fill-corners", action="store_true")
    parser.add_argument("--center-y", type=float, default=0.45)
    args = parser.parse_args()

    if args.portrait and not args.name:
        parser.error("--portrait needs --name")
    if args.name and not args.portrait:
        parser.error("--name needs --portrait")

    if args.portrait:
        img = build_portrait(
            args.portrait, args.name, args.kicker, args.subtitle, args.fill_corners, args.center_y
        )
    else:
        img = build()

    out = ROOT / "public/assets/news" / f"{args.slug}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
