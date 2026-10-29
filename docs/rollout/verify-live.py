#!/usr/bin/env python3
"""Check every ps-assets file against assets.purple-standard.app by SHA-256 (served bytes, not status).

Exit 0 only when every local file is served with identical bytes and an image content type.
python3 docs/rollout/verify-live.py
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
HOST = "https://assets.purple-standard.app/"


def main():
    print("accepted: verify-live.py", flush=True)
    files = sorted(p for p in PS_ASSETS.rglob("*") if p.is_file() and p.name != ".DS_Store")
    print(f"step 1/1: {len(files)} files", flush=True)
    bad = []
    for i, p in enumerate(files, 1):
        rel = p.relative_to(PS_ASSETS).as_posix()
        req = urllib.request.Request(HOST + rel, headers={"Cache-Control": "no-cache", "User-Agent": "ps-verify"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body, ctype = r.read(), r.headers.get("Content-Type", "")
            ok = hashlib.sha256(body).digest() == hashlib.sha256(p.read_bytes()).digest() and ctype.startswith("image/")
            status = "MATCH" if ok else f"DIFF ({ctype})"
        except Exception as e:   # 404 and network errors
            ok, status = False, f"ERROR {e}"
        if not ok:
            bad.append(rel)
        print(f"  {status:6} {rel}")
        if i % 20 == 0:
            print(f"  ... {i}/{len(files)} checked", flush=True)
    print(f"RESULT: {'ok' if not bad else 'FAILED'}: {len(files) - len(bad)}/{len(files)} match"
          + (f"; next: re-upload the whole folder, or wait for the edge if only new files fail" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
