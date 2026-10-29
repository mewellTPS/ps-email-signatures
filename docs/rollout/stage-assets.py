#!/usr/bin/env python3
"""Stage every image the 16 rollout signatures use into ps-assets (the Cloudflare Pages master).

Maps each hosted URL in docs/rollout/paste/*.html to the local file its build previews with
(the build's own local() mapping), then:
  NEW files   -> copied into ps-assets (never overwrites)
  existing    -> SHA-256 compared; a mismatch is reported, not overwritten
Default is a dry run; pass --copy to write.  python3 docs/rollout/stage-assets.py [--copy]
"""
import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HOST = "https://assets.purple-standard.app/"
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"

spec = importlib.util.spec_from_file_location("rollout", REPO / "docs/review/build-rollout.py")
rollout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rollout)

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
srcs = lambda h: re.findall(r'<img[^>]*?src="([^"]+)"', h)


def same_pixels(a, b):
    r = subprocess.run(["magick", "compare", "-metric", "AE", str(a), str(b), "null:"], capture_output=True, text=True)
    return r.stderr.split()[0] == "0" if r.stderr else False


def main():
    copy = "--copy" in sys.argv
    print(f"accepted: stage-assets.py {'--copy' if copy else '(dry run)'}", flush=True)
    print("step 1/3: map hosted URLs to local files", flush=True)
    mapping = {}
    for rule, sender, source, _ in rollout.RULES:
        html, mod, d = rollout.render(source, sender)
        lo = mod.local(html)
        for url, loc in zip(srcs(html), srcs(lo), strict=True):
            path = Path(loc) if loc.startswith("/") else d / loc
            if not url.startswith(HOST):
                sys.exit(f"RESULT: FAILED: {rule}: image not on assets host: {url}. Next: fix the build.")
            if not path.is_file():
                sys.exit(f"RESULT: FAILED: {rule}: local file missing: {path}. Next: run that build.")
            rel = url[len(HOST):]
            if rel in mapping and sha(mapping[rel]) != sha(path):
                sys.exit(f"RESULT: FAILED: {rel} maps to two different files. Next: rename one.")
            mapping[rel] = path
    print(f"  {len(mapping)} distinct images", flush=True)

    print("step 2/3: compare with ps-assets", flush=True)
    new, same, differ = [], [], []
    for rel, path in sorted(mapping.items()):
        dest = PS_ASSETS / rel
        if not dest.exists():
            new.append(rel)
        elif sha(dest) == sha(path) or same_pixels(dest, path):   # a rebuild rewrites PNG metadata only
            same.append(rel)
        else:
            differ.append(rel)
    for rel in new:
        print(f"  NEW     {rel}")
    for rel in differ:
        print(f"  DIFFERS {rel}  (ps-assets copy kept; local build differs)")
    print(f"  {len(same)} already identical", flush=True)

    print("step 3/3: copy", flush=True)
    if copy:
        for rel in new:
            dest = PS_ASSETS / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mapping[rel], dest)
            assert sha(dest) == sha(mapping[rel])
        print(f"  copied {len(new)} new file(s), checksums verified")
    else:
        print("  dry run: nothing copied")
    ok = not differ
    print(f"RESULT: {'ok' if ok else 'ATTENTION'}: {len(new)} new, {len(same)} identical, {len(differ)} differ")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
