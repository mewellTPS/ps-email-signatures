#!/usr/bin/env python3
"""Verify PNG pHYs chunks are exactly 96 DPI (ADR 0008).

ImageMagick reports 96 DPI as "37.79 PixelsPerCentimeter" because PNG can only
store pixels-per-metre, so `identify %x` is not a usable oracle. This parses the
pHYs chunk bytes directly: 96 DPI == 3780 px/m (96 / 0.0254 = 3779.5, rounded).

Usage: python3 verify-phys.py <file-or-dir> [...]
Exit 0 if every PNG conforms, 1 otherwise.
"""
import struct
import sys
from pathlib import Path

TARGET_PX_PER_M = 3780
TOLERANCE = 1  # allow 3779/3780/3781 rounding


def read_phys(path: Path):
    """Return (px_per_unit_x, px_per_unit_y, unit) or None if no pHYs chunk."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        ctype = data[pos + 4 : pos + 8]
        body = data[pos + 8 : pos + 8 + length]
        if ctype == b"pHYs":
            x, y = struct.unpack(">II", body[:8])
            return x, y, body[8]
        if ctype == b"IEND":
            return None
        pos += 12 + length
    return None


def read_ihdr(path: Path):
    data = path.read_bytes()
    w, h, depth, color = struct.unpack(">IIBB", data[16:26])
    return w, h, depth, color


def main(argv):
    targets = []
    for a in argv:
        p = Path(a)
        targets.extend(sorted(p.rglob("*.png")) if p.is_dir() else [p])
    if not targets:
        print("no PNGs found")
        return 1

    fails = []
    for f in targets:
        w, h, depth, color = read_ihdr(f)
        phys = read_phys(f)
        alpha = "alpha" if color in (4, 6) else "NO-ALPHA"
        if phys is None:
            status, detail = "FAIL", "no pHYs chunk"
        else:
            x, y, unit = phys
            if unit != 1:
                status, detail = "FAIL", f"unit={unit} (want 1=metre)"
            elif abs(x - TARGET_PX_PER_M) > TOLERANCE or abs(y - TARGET_PX_PER_M) > TOLERANCE:
                status, detail = "FAIL", f"{x}x{y} px/m = {x*0.0254:.1f} DPI"
            else:
                status, detail = "OK", f"{x} px/m = {round(x*0.0254)} DPI"
        if status == "FAIL":
            fails.append(f)
        print(f"  {status:<4} {w}x{h} {alpha:<8} {detail:<26} {f.name}")

    print()
    if fails:
        print(f"{len(fails)} of {len(targets)} file(s) FAILED the 96 DPI check")
        return 1
    print(f"All {len(targets)} file(s) conform: 96 DPI, pHYs unit=metre (ADR 0008)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
