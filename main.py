#!/usr/bin/env python3
"""Entry program for the news-image-20261124 bounty.

The image this entry submits is poster.png, drawn by render_poster.py and
kept next to this file. The grader expects the image at /output/entry.png,
so emit the poster's bytes there (MAKEFUN_OUTPUT_DIR overrides /output when
running outside the grader's container).
"""

import os
from pathlib import Path

poster = Path(__file__).with_name("poster.png")
target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
target_dir.mkdir(parents=True, exist_ok=True)
(target_dir / "entry.png").write_bytes(poster.read_bytes())
