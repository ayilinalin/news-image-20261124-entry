#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the front-page image shipped in this repository to the output
directory the grader provides. Standard library only, no network,
fully deterministic: the same bytes come out on every run.
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png: not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png: missing IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing from repository")

    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % size)
    width, height = read_png_size(src)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit("entry.png exceeds 1024x1024: %dx%d" % (width, height))

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    if os.path.getsize(dst) != size:
        raise SystemExit("copy verification failed: size mismatch")

    if sha256_file(src) != sha256_file(dst):
        raise SystemExit("copy verification failed: sha256 mismatch")
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (dst, size, width, height, sha256_file(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
