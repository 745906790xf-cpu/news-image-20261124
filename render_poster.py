"""Draw the 24 November 2026 world-news poster (v2).

A single 1024x1024 newspaper front page: masthead, a "day in numbers"
strip, one lead story beside a dateline globe, six story cards in two
columns, and a numbered "Also on Tuesday" list of eight more stories.
Run it directly or through main.py; the output is deterministic.

v2 fixes (QC audit 2026-11-24): the Merkury is a corvette, not a
frigate; the Nvidia summary now gives the real reason for the return
(resignation amid scandal, Trump pressed the board; shares +31%)
instead of an invented demand rationale; the space story attributes
the warning to Western intelligence and dates the possible launch to
December; the House story notes the largest majority since 1992 and
the Senate win; the also-strip gains the $3.79bn GTA VI record and
seven more verified stories, a numbers strip and a globe.
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (248, 244, 232)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (148, 28, 28)
MUTED = (90, 86, 76)
NAVY = (29, 58, 95)

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


def globe(draw, cx, cy, r):
    """Schematic dateline globe marking where the day's stories broke."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    for k in (-0.66, -0.33, 0.0, 0.33, 0.66):
        w = r * (1 - k * k) ** 0.5
        draw.ellipse([cx - w, cy - r, cx + w, cy + r],
                     outline=(120, 145, 175), width=1)
        draw.line([cx - w, cy + k * r, cx + w, cy + k * r],
                  fill=(120, 145, 175), width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=(120, 145, 175), width=1)
    spots = [
        (-0.62, -0.28, "WASHINGTON", -6, 8),
        (-0.55, 0.32, "LAS VEGAS", 9, -5),
        (0.02, -0.44, "ANTALYA", 10, -14),
        (0.30, -0.02, "BENGHAZI", 9, 8),
        (0.58, -0.32, "MANILA", 9, -5),
    ]
    for dx, dy, label, tx, ty in spots:
        px, py = cx + dx * r, cy + dy * r
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=ACCENT)
        draw.text((px + tx, py + ty), label, font=SANS_BOLD(10), fill=NAVY)


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

    # Day in numbers strip.
    y += 10
    numbers = ("THE DAY IN NUMBERS  •  258 seats  •  Nvidia +31%  •  "
               "$952bn in a day  •  14 killed near Kyiv  •  "
               "$3.79bn GTA day one  •  7 drones")
    centred(draw, y, numbers, SANS_BOLD(12), fill=NAVY,
            x0=margin, x1=right)
    y += 26
    draw.line([(margin, y), (right, y)], fill=RULE, width=1)

    # Lead story: COP31, left; globe, right.
    y += 14
    lead_w = 660
    y = headline_block(
        draw, margin, y, lead_w,
        "CLIMATE  —  LEAD STORY",
        "COP31 talks collapse without a deal",
        "Negotiators leave the summit with no final agreement, as "
        "climate finance and fossil-fuel language stay unresolved.",
        head_size=38, sum_size=20)
    globe(draw, 830, 262, 72)
    draw.text((830 - draw.textlength("Where today's stories broke",
              font=SANS(13)) / 2, 340),
              "Where today's stories broke", font=SANS(13), fill=MUTED)
    y = 356
    draw.line([(margin, y), (right, y)], fill=RULE, width=1)

    # Six stories, two columns x three rows.
    stories = [
        ("TECHNOLOGY",
         "Nvidia brings back Jensen Huang as chief executive",
         "Reinstated 11 days after resigning amid a scandal, after "
         "Trump pressed the board; shares jump 31%."),
        ("WAR AT SEA",
         "Ukraine says it sank a Russian corvette off Libya",
         "Seven sea drones struck the Merkury in Benghazi port, and "
         "a cargo ship was hit too."),
        ("UKRAINE",
         "Russian strikes kill at least 14 near Kyiv",
         "Overnight attacks hit Dymer and other towns in the Kyiv "
         "region; a block of flats collapses."),
        ("UNITED STATES",
         "Democrats retake the House with 258 seats",
         "Largest House majority since 1992 — and Democrats take "
         "the Senate too."),
        ("SPACE",
         "Russia may put a nuclear weapon in orbit",
         "Western intelligence warns of a possible December launch, "
         "and NATO vows to defend space."),
        ("ASIA",
         "Trump offers the Philippines a $2.4bn package",
         "Mostly loans, plus $400m in military aid, in a new push to "
         "shore up the Pacific ally."),
    ]
    col_w = (right - margin - 28) // 2
    row_y = y + 14
    row_h = 136
    for i, (kicker, head, summ) in enumerate(stories):
        cx = margin + (i % 2) * (col_w + 28)
        cy = row_y + (i // 2) * row_h
        if i % 2 == 1:
            draw.line([(margin + col_w + 14, cy + 4),
                       (margin + col_w + 14, cy + row_h - 14)],
                      fill=(200, 194, 178), width=1)
        headline_block(draw, cx, cy, col_w, kicker, head, summ,
                       head_size=22, sum_size=15, gap=6)
        if i // 2 < 2:
            draw.line([(margin, cy + row_h - 6), (right, cy + row_h - 6)],
                      fill=(200, 194, 178), width=1)

    # Also on Tuesday: eight more verified stories, numbered.
    y = row_y + 3 * row_h + 8
    draw.text((margin, y), "ALSO ON TUESDAY", font=SANS_BOLD(16), fill=ACCENT)
    also = [
        "GTA VI hacker Kurtaj jailed for 7 years — freed the same day",
        "GTA VI makes $3.79bn on day one, a record launch",
        "Markets soar: Nasdaq +6.5%, S&P +4.7% as Nvidia jumps 31%",
        "NATO meets after Russian missiles land in Poland",
        "Verstappen wins Las Vegas GP; Liverpool rout Man Utd 4-0",
        "Alcaraz wins first ATP Finals title, beating Zverev",
        "Trump, Putin and Xi: Shenzhen pact, no binding arms deal",
        "Asia rallies: Korea's Kospi +6.2% as AI stocks rebound",
    ]
    ay = y + 26
    row_h2 = 40
    for i, item in enumerate(also):
        ax = margin + (i % 2) * (col_w + 28)
        ayy = ay + (i // 2) * row_h2
        num = f"{i + 1}."
        draw.text((ax, ayy), num, font=SANS_BOLD(14), fill=ACCENT)
        nw = draw.textlength(num + " ", font=SANS_BOLD(14))
        for j, line in enumerate(wrap(draw, item, SANS(14), col_w - nw)):
            draw.text((ax + nw, ayy + j * 18), line, font=SANS(14), fill=INK)

    # Footer.
    fy = SIZE - 34
    draw.line([(margin, fy - 12), (right, fy - 12)], fill=RULE, width=1)
    foot = ("Every story here broke or was first reported 22–24 Nov 2026.  "
            "Sources: CNN, Reuters, AP, BBC, Al Jazeera, Nikkei, Bloomberg, SCMP")
    centred(draw, fy, foot, SANS(13), fill=MUTED)

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import sys
    build_poster(sys.argv[1] if len(sys.argv) > 1 else "poster.png")
