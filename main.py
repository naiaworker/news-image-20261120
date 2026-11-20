#!/usr/bin/env python3
"""Hand-in program for the make.fun bounty news-image-20261120.

Copies the pre-rendered front page (entry.png, shipped in this repo) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only.
Never deletes the output directory; creates it if missing.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
