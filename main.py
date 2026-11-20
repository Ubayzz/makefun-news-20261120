"""main.py — news-image-20261120 entrypoint.

Copies the pre-rendered infographic to /output/entry.png.
Pure stdlib: no external deps, no network.  The output file is a valid
JPEG (magic bytes ffd8ff) saved as entry.png per the gate rules.

Infographic sums up world news of Friday 20 November 2026 in an
illustrated newspaper-editorial layout.  See NEWS_RESEARCH.md and
CREATIVE_BRIEF.md for full source list.

Artwork: ChatGPT-generated image, fact-checked against real news sources
for 20 November 2026.  Entry is the pre-rendered JPEG already in the repo;
main.py just stages it.
"""

import hashlib
import os
import shutil
import sys

# ---------------------------------------------------------------------------
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_SRC = os.path.join(REPO_DIR, "entry_final.jpg")
IMAGE_DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
IMAGE_DST = os.path.join(IMAGE_DST_DIR, "entry.png")

BYTES_1_MIB = 1_048_576


def validate_source(path: str) -> None:
    """Bail out early if the source file is missing or too large."""
    if not os.path.isfile(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(path)
    if size > BYTES_1_MIB:
        print(
            f"ERROR: {path} is {size} bytes — exceeds 1 MiB limit",
            file=sys.stderr,
        )
        sys.exit(1)


def copy_image(src: str, dst: str) -> None:
    """Copy the image file and verify the destination hash matches.

    The gate reads the file by magic bytes (ffd8ff for JPEG) not by
    extension — entry.png is the required filename regardless of the
    underlying format.
    """
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

    # Verify the copy landed byte-for-byte identical
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()

    if src_hash != dst_hash:
        print("ERROR: destination hash differs from source", file=sys.stderr)
        sys.exit(1)

    print(f"{os.path.basename(src)} → {dst}  ({os.path.getsize(dst)} bytes, sha256={dst_hash[:12]}…)")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    validate_source(IMAGE_SRC)
    copy_image(IMAGE_SRC, IMAGE_DST)