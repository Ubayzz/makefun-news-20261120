"""main.py — entrypoint for make.fun bounty news-image-20261120.

Copies the pre-rendered infographic (entry_final.jpg) to /output/entry.png.
Pure Python stdlib — no dependencies, no network. The output file is a
valid JPEG (the gate reads magic bytes; JPEG content with .png name allowed).

The image sums up the world's news of Friday 20 November 2026 with an
illustrated newspaper editorial layout.

Artwork: ChatGPT image generation, verified against November 20, 2026 sources.
See NEWS_RESEARCH.md and CREATIVE_BRIEF.md for full source list.
"""

import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_final.jpg")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

if not os.path.isfile(SRC):
    print(f"ERROR: source image not found at {SRC}", file=sys.stderr)
    sys.exit(1)

if os.path.getsize(SRC) > 1_048_576:
    print(f"ERROR: entry_final.jpg exceeds 1 MiB limit", file=sys.stderr)
    sys.exit(1)

os.makedirs(DST_DIR, exist_ok=True)
shutil.copy2(SRC, DST)
print(f"entry_final.jpg → {DST}")