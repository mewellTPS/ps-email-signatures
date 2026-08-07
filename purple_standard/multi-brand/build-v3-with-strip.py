#!/usr/bin/env python3
"""Generate signature-purple-standard-v3-with-strip.html from the v2 and v3 files.

The combined variant is derived, never hand-authored, so it cannot drift from
either parent. Run this after editing v2's brand-icon row or v3's badge.

Usage: python3 build-v3-with-strip.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE / "signature-purple-standard-v2.html"
V3 = HERE / "signature-purple-standard-v3.html"
OUT = HERE / "signature-purple-standard-v3-with-strip.html"

HEADER = """\
<!-- Purple Standard email signature — v3+strip (CodeTwo-ready, dynamic). -->
<!--                                                                                     -->
<!-- The combined variant: v3's animated badge AND v2's static 6-icon strip together.     -->
<!-- Generated from signature-purple-standard-v2.html + signature-purple-standard-v3.html -->
<!-- by build-v3-with-strip.py, so it cannot drift from either parent — regenerate rather  -->
<!-- than hand-editing this file.                                                          -->
<!--                                                                                     -->
<!-- Included so the v2-vs-v3 choice can be judged against all three options rather than  -->
<!-- two. Be aware it states the portfolio twice: the badge cycles the same six brands    -->
<!-- the strip already shows, plus tps-badge. Reach for this only if the redundancy is    -->
<!-- wanted for emphasis; otherwise v2 or v3 is the cleaner choice.                       -->
"""

BANNER = '    <tr data-codetwo-visible="Banner">'

# Container elements whose open/close counts must match. Presence checks ("is
# the row there? are there 8 icons?") pass happily on truncated markup, so the
# structural check is the one that actually catches a bad extraction.
PAIRED = ("table", "tbody", "tr", "td")


def _markup(html: str) -> str:
    """Drop HTML comments before counting tags.

    These files carry long explanatory comment headers that mention tags in
    prose ('the only hunk should be the "Brand icons" <tr>'). Counting those
    reports a phantom imbalance on perfectly good markup — a false alarm that
    trains you to ignore the check, which is worse than not having it.
    """
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def balanced(html: str) -> bool:
    t = _markup(html)
    return all(
        len(re.findall(rf"<{tag}[\s>]", t)) == len(re.findall(rf"</{tag}>", t))
        for tag in PAIRED
    )


def tag_counts(html: str) -> str:
    t = _markup(html)
    return "  ".join(
        f"{tag}:{len(re.findall(rf'<{tag}[\s>]', t))}/{len(re.findall(rf'</{tag}>', t))}"
        for tag in PAIRED
    )


def main() -> int:
    v2, v3 = V2.read_text(), V3.read_text()

    # Anchor the closing tag to the OUTER row's exact 4-space indent. A loose
    # `.*?\n *</tr>\n` matches the INNER row's `</tr>` (12 spaces) first, which
    # silently truncates the block mid-table and leaves <table>/<tbody>/<td>
    # unclosed — the icons then render at irregular gaps instead of failing.
    m = re.search(r'( {4}<tr data-codetwo-visible="Brand icons">\n.*?\n {4}</tr>\n)', v2, re.S)
    if not m:
        print(f"error: no brand-icon row found in {V2.name}", file=sys.stderr)
        return 1
    row = m.group(1)

    if not balanced(row):
        print(f"error: extracted row has unbalanced tags:\n{row}", file=sys.stderr)
        return 1

    if v3.count(BANNER) != 1:
        print(f"error: expected exactly 1 Banner row in {V3.name}, found {v3.count(BANNER)}",
              file=sys.stderr)
        return 1

    body = v3.replace(BANNER, row + BANNER)
    OUT.write_text(HEADER + body[body.index("<table"):])

    text = OUT.read_text()
    # v2's own brand row is the reference: the combined file must carry it verbatim.
    v2row = re.search(r'( {4}<tr data-codetwo-visible="Brand icons">\n.*?\n {4}</tr>\n)', v2, re.S)
    checks = {
        "tags balanced":     balanced(text),
        "row verbatim from v2": bool(v2row) and v2row.group(1) in text,
        "brand-icon row":    text.count('data-codetwo-visible="Brand icons"') == 1,
        "animated badge":    text.count("tps-badge-cycle.gif") == 1,
        "6 brand icons":     text.count("out/c-native/brand-") == 6,
        "static badge gone": "email-signature/tps-badge.png" not in text,
        "endorsement kept":  text.count("tps-endorsement.png") == 1,
        "no MOR/ENG chips":  "brand-mor.png" not in text and "brand-eng.png" not in text,
        "row before banner": text.index('data-codetwo-visible="Brand icons"')
                             < text.index('data-codetwo-visible="Banner"'),
    }
    for name, ok in checks.items():
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
    print(f"\n  tag balance (open/close): {tag_counts(text)}")
    if not all(checks.values()):
        return 1
    print(f"\nwrote {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
