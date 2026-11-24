#!/usr/bin/env python3
"""Entry program for the news-image-20261124 bounty.

Draws the 24 November 2026 world-news poster from scratch with
render_poster.py and writes it to /output/entry.png, where the grader
expects it. MAKEFUN_OUTPUT_DIR overrides /output when running locally,
and --out picks a different file to write.

Every headline was checked against wire reports on the day before
drawing (CNN, Reuters, AP, BBC, Al Jazeera, Nikkei, Bloomberg, SCMP).
"""

import argparse
import os
from pathlib import Path

from render_poster import build_poster

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None,
                        help="write the poster here instead of the output dir")
    args = parser.parse_args()

    if args.out:
        build_poster(args.out)
        print("wrote", args.out)
        return

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    build_poster(str(target))
    # Keep a local copy beside this file for inspection.
    local = HERE / "poster.png"
    build_poster(str(local))
    from PIL import Image
    print("wrote", target, Image.open(target).size)


if __name__ == "__main__":
    main()
