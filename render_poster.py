"""Draw the 24 November 2026 world-news poster.

A single 1024x1024 newspaper front page: masthead, one lead story, six
story cards in two columns, and an "Also today" strip at the bottom.
Run it directly or through main.py; the output is deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (248, 244, 232)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (148, 28, 28)
MUTED = (90, 86, 76)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit width."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, y, text, fnt, fill=INK, x0=0, x1=SIZE):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def headline_block(draw, x, y, width, kicker, headline, summary,
                   head_size=30, sum_size=19, gap=8):
    draw.text((x, y), kicker, font=SANS_BOLD(15), fill=ACCENT)
    y += 22
    for line in wrap(draw, headline, SANS_BOLD(head_size), width):
        draw.text((x, y), line, font=SANS_BOLD(head_size), fill=INK)
        y += head_size + 4
    y += gap - 4
    for line in wrap(draw, summary, SANS(sum_size), width):
        draw.text((x, y), line, font=SANS(sum_size), fill=MUTED)
        y += sum_size + 5
    return y


def build_poster(path):
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    margin = 44
    right = SIZE - margin

    # Masthead.
    y = 30
    y = centred(draw, y, "THE WORLD TODAY", SERIF_BOLD(62))
    draw.line([(margin, y + 2), (right, y + 2)], fill=RULE, width=3)
    draw.line([(margin, y + 8), (right, y + 8)], fill=RULE, width=1)
    y += 16
    draw.text((margin, y), "Tuesday, 24 November 2026",
              font=SANS_BOLD(18), fill=INK)
    tag = "One image  •  One day  •  The world in a page"
    w = draw.textlength(tag, font=SANS(18))
    draw.text((right - w, y), tag, font=SANS(18), fill=MUTED)
    y += 34
    draw.line([(margin, y), (right, y)], fill=RULE, width=2)

    # Lead story: COP31.
    y += 18
    y = headline_block(
        draw, margin, y, right - margin,
        "CLIMATE  —  LEAD STORY",
        "COP31 talks collapse without a deal",
        "Negotiators leave the summit with no final agreement, as "
        "climate finance and fossil-fuel language stay unresolved.",
        head_size=44, sum_size=21)
    y += 6
    draw.line([(margin, y), (right, y)], fill=RULE, width=1)

    # Six stories, two columns x three rows.
    stories = [
        ("TECHNOLOGY",
         "Nvidia brings back Jensen Huang as chief executive",
         "The chipmaker rehires its co-founder to lead the company "
         "again as demand for AI hardware surges."),
        ("WAR AT SEA",
         "Ukraine says it sank a Russian frigate off Libya",
         "Kyiv claims uncrewed boats struck the Merkury in the "
         "Mediterranean, far from home waters."),
        ("UKRAINE",
         "Russian strikes kill at least 14 near Kyiv",
         "Overnight attacks hit the Kyiv region in the latest deadly "
         "barrage on civilian areas."),
        ("UNITED STATES",
         "Democrats retake the House with 258 seats",
         "The opposition wins a clear majority in the lower chamber, "
         "reshaping the balance in Washington."),
        ("SPACE",
         "Russia may put a nuclear weapon in orbit",
         "US intelligence warns of a possible launch next month, and "
         "NATO vows to defend space."),
        ("ASIA",
         "Trump offers the Philippines a $2.4bn package",
         "Mostly loans, plus $400m in military aid, in a new push to "
         "shore up the Pacific ally."),
    ]
    col_w = (right - margin - 28) // 2
    row_y = y + 16
    row_h = 168
    for i, (kicker, head, summ) in enumerate(stories):
        cx = margin + (i % 2) * (col_w + 28)
        cy = row_y + (i // 2) * row_h
        if i % 2 == 1:
            draw.line([(margin + col_w + 14, cy + 4),
                       (margin + col_w + 14, cy + row_h - 16)],
                      fill=(200, 194, 178), width=1)
        headline_block(draw, cx, cy, col_w, kicker, head, summ,
                       head_size=24, sum_size=17, gap=6)
        if i // 2 < 2:
            draw.line([(margin, cy + row_h - 6), (right, cy + row_h - 6)],
                      fill=(200, 194, 178), width=1)

    # Also today strip.
    y = row_y + 3 * row_h + 10
    draw.rectangle([(margin, y), (right, y + 92)], outline=RULE, width=2)
    draw.text((margin + 16, y + 12), "ALSO TODAY",
              font=SANS_BOLD(16), fill=ACCENT)
    draw.text((margin + 16, y + 38),
              "GTA VI hacker Kurtaj jailed for 7 years — freed the same day",
              font=SANS_BOLD(19), fill=INK)
    draw.text((margin + 16, y + 64),
              "Grand Theft Auto VI launched on 19 November",
              font=SANS(18), fill=MUTED)

    # Footer.
    fy = SIZE - 34
    foot = "Sources: CNN, Reuters, AP, BBC, Al Jazeera, Nikkei, Bloomberg, SCMP"
    centred(draw, fy, foot, SANS(14), fill=MUTED)

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import sys
    build_poster(sys.argv[1] if len(sys.argv) > 1 else "poster.png")
