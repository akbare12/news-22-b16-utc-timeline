#!/usr/bin/env python3
"""news-image-20261122 entry: copies the bundled entry.png to the output directory.

The grader runs this program with a read-only repository and a writable
output directory in MAKEFUN_OUTPUT_DIR. Nothing is ever written next to
this file: the destination is always inside MAKEFUN_OUTPUT_DIR.
"""
import hashlib
import os
import shutil
import struct
import sys


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("source is not a PNG")
    if head[12:16] != b"IHDR":
        raise ValueError("source has no IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        print(f"bad size: {w}x{h}", file=sys.stderr)
        return 1
    if sha256(dst) != sha256(src):
        print("copy mismatch", file=sys.stderr)
        return 1
    nbytes = os.path.getsize(dst)
    if nbytes > 1048576:
        print(f"output too large: {nbytes} bytes", file=sys.stderr)
        return 1
    print(f"OK {dst} {w}x{h} {nbytes} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
