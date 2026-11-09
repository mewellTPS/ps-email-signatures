#!/usr/bin/env python3
"""Soft-launch rollout: one card per CodeTwo rule (16), for Michael's approval before anything goes live.

Duplicates the c-suite review page (build-c-suite.py) as one card per sender. Everything is
hardcoded until Ntiva fixes Entra titles and phones (Michael, 2026-10-29). Operators come from
their own builds; PS and ACE staff reuse the PS (Michael) and ACE E v2 builds with each person
swapped in. Shared mailboxes get their own full CodeTwo rule, like everyone else (Michael, 2026-10-29).

Run the brand builds first, then: python3 docs/review/build-rollout.py
Writes:
  docs/rollout/paste/NN-<slug>.html          CodeTwo paste source per rule (hosted URLs)
  docs/review/signatures-rollout-review.html self-contained review page (images inlined)
"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PASTE = REPO / "docs/rollout/paste"
SHARED_DIR = REPO / "shared-mailbox"   # backup copy/paste files; CodeTwo signs these addresses (Michael, 2026-10-29)
SHARED = {"nmallory@purple-standard.com", "rclarke@purple-standard.com", "klanzone@purple-standard.com",
          "fcollier@purple-standard.com"}   # Faith's may be shared (Michael confirming)
DARK_BG = "#1E1E1E"

spec = importlib.util.spec_from_file_location("c_suite", HERE / "build-c-suite.py")
c_suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c_suite)
load, inline = c_suite.load, c_suite.inline

# People supplied by Michael, 2026-10-29 (one phone each; Kelly's is ACE's main office line).
PEOPLE = {
    "brady": ("Brady Bodden", "Director of Operations", "(813) 943-5160"),
    "josh": ("Josh Irvine", "Director of Marketing", "(619) 905-0077"),
    "michael": ("Michael Ewell", "SEO and Data Specialist", "(801) 641-5387"),
    "nan": ("Nan Mallory", "Director of Finance &amp; Administration", "(727) 743-8261"),
    "ryan": ("Ryan Clarke", "Co-Founder", "(813) 363-3794"),
    "kelly": ("Kelly Lanzone", "Accounting &amp; Billing Manager", "(813) 971-8770"),
    "faith": ("Faith Collier", "Finance and Payroll Administrator", "(270) 780-4205"),
    "patty": ("Patty Clarke", "", ""),   # no title or phone (Michael, 2026-11-05)
    # Email only until the phone situation is sorted; no personal cells (Michael, 2026-11-09)
    "laya": ("Laya Nawabit", "Administrative Support", ""),
    "alyssa": ("Alyssa Baker", "Administrative Support", ""),
}
OFFICE_LINE = {"kelly"}   # label O: (office) instead of P:

# Above the signature: a blank line so it isn't pushed against the email, plus an optional closer in
# Outlook's body font (Michael, 2026-10-30). Nan keeps her own "Thanks, Nan" in Outlook: fonts aren't
# sent with mail, so her Lucida Handwriting only shows where it is installed (Nan, 2026-10-30).
SIGNOFF = {"brady": "Thanks,", "nan": None, "ryan": None, "patty": "Thanks,", "laya": "Thanks,", "alyssa": "Thanks,"}
# No phone line: Ryan asked for his cell to be removed (Michael, 2026-11-03). Email takes its top margin.
NO_PHONE = {"ryan", "patty", "laya", "alyssa"}
# No job title line (Michael, 2026-11-05). The email line keeps its 8px top margin below the name.
NO_TITLE = {"patty"}
# Blank lines added by hand in CodeTwo above the block, kept verbatim (found live 2026-11-09).
LIVE_PREFIX = {
    "michael": '<p style="margin: 0.1pt; font-family: Arial; font-size: 10pt;"><br></p>' * 2,
    "josh": '<p style="font-family: Arial; font-size: 10pt; margin: 0.1pt;"><br></p>',
}
INK = "#111111"   # Outlook dark -> about #F2F2F2
BODY_FONT = "font-family: Aptos, Calibri, Arial, Helvetica, sans-serif; font-size: 11pt; line-height: 1.15"

# (rule name, sender, source, note). Source: ("op", build dir, variant) | ("ps", person) | ("ace", person)
RULES = [
    ("BPW - Danny Boyette", "dboyette@BoyettePumpWell.com", ("op", "boyette/_mockup/danny", "c"), ""),
    ("WTR - Sean Myatt", "smyatt@wtrdr.com", ("op", "wtr-dr/_mockup/sean", "c"), ""),
    ("PC - Kenny Morrow", "kmorrow@purple-current.com", ("op", "purple-current/_mockup/kenny", "e"), ""),
    ("BRS - Victor Rodriguez", "vrodriguez@brisaclimate.com", ("op", "brisa/_mockup/victor", "e"), ""),
    ("TYR - John Rodrigues", "Jrodrigues@tyrianroofing.com", ("op", "tyrian/_mockup/john", "e"), ""),
    ("ACE - Nan Mallory", "nmallory@acesepticandwaste.com", ("ace", "nan"), ""),
    ("ACE - Ryan Clarke", "rclarke@acesepticandwaste.com", ("ace", "ryan"), ""),
    ("ACE - Kelly Lanzone", "klanzone@acesepticandwaste.com", ("ace", "kelly"), "Phone is ACE's main office line, labelled O:."),
    ("ACE - Faith Collier", "fcollier@acesepticandwaste.com", ("ace", "faith"), "Card only: the rule is created later (Michael, 2026-10-29)."),
    ("PS - Brady Bodden", "bbodden@purple-standard.com", ("ps", "brady"), ""),
    ("PS - Michael Ewell", "mewell@purple-standard.com", ("ps", "michael"), ""),
    ("PS - Josh Irvine", "jirvine@purple-standard.com", ("ps", "josh"), ""),
    ("PS - Nan Mallory (shared mailbox)", "nmallory@purple-standard.com", ("ps", "nan"), "Shared mailbox: Nan keeps an Outlook signature with only her closing (\"Thanks, Nan\"); CodeTwo adds the block below it."),
    ("PS - Ryan Clarke (shared mailbox)", "rclarke@purple-standard.com", ("ps", "ryan"), "Shared mailbox: Ryan removes his Outlook signature so it isn't doubled."),
    ("PS - Faith Collier", "fcollier@purple-standard.com", ("ps", "faith"), "May be a shared mailbox (Michael is confirming); the signature is the same either way."),
    ("PS - Kelly Lanzone (shared mailbox)", "klanzone@purple-standard.com", ("ps", "kelly"), "Shared mailbox: Kelly removes her Outlook signature so it isn't doubled."),
    ("ACE - Patty Clarke", "pclarke@acesepticandwaste.com", ("ace", "patty"), ""),
    ("ACE - Laya Nawabit", "lnawabit@acesepticandwaste.com", ("ace", "laya"), ""),
    ("PS - Laya Nawabit", "lnawabit@purple-standard.com", ("ps", "laya"), ""),
    ("PS - Alyssa Baker", "abaker@purple-standard.com", ("ps", "alyssa"), ""),
]


def tel(phone):
    return "+1" + re.sub(r"\D", "", phone)


def signoff(source, html):
    if source[0] == "op" or source[1] not in SIGNOFF:
        return html
    out = f'<p style="margin: 0; {BODY_FONT}; color: {INK}" data-codetwo-visible="Spacer">&nbsp;</p>\n'
    closer = SIGNOFF[source[1]]
    if closer:
        out += f'<p style="margin: 0 0 12px 0; {BODY_FONT}; color: {INK}" data-codetwo-visible="Sign-off">{closer}</p>\n'
    return out + html


def drop_phone(source, html):
    if source[0] == "op" or source[1] not in NO_PHONE:
        return html
    html, n = re.subn(r'\n?[ \t]*<p style="margin: 0; ([^"]*?)margin: 8px 0 0 0; [^"]*" data-codetwo-visible="Phone">.*?</p>', "", html, count=1)
    assert n == 1, "phone line not found"
    html, n = re.subn(r'<p style="margin: 0; (font-family: [^;]+;) (font-size[^"]*" data-codetwo-visible="Email")',
                      r'<p style="margin: 0; \1 margin: 8px 0 0 0; \2', html, count=1)
    assert n == 1, "email line not found"
    return html


def drop_title(source, html):
    if source[0] == "op" or source[1] not in NO_TITLE:
        return html
    html, n = re.subn(r'\n?[ \t]*<p style="[^"]*" data-codetwo-visible="Job title">.*?</p>', "", html, count=1)
    assert n == 1, "job title line not found"
    return html


def render(source, sender):
    html, mod, d = _render(source, sender)
    html = signoff(source, drop_title(source, drop_phone(source, html)))
    if source[0] != "op" and source[1] in LIVE_PREFIX:
        html = LIVE_PREFIX[source[1]] + "\n" + html
    return html, mod, d


def _render(source, sender):
    """Return (paste html with hosted URLs, module for local()/outlook_dark(), build dir)."""
    kind = source[0]
    if kind == "op":
        d = REPO / source[1]
        return (d / f"signature-{source[2]}.html").read_text(), load(d), d
    name, title, phone = PEOPLE[source[1]]
    if kind == "ps":
        d = REPO / "purple_standard/_mockup/michael"
        mod = load(d)
        mod.PERSON = {"name": name, "title": title, "phone": phone, "tel": tel(phone), "email": sender}
        html = mod.signature("pledge-text")   # E, approved
        if source[1] in OFFICE_LINE:
            html = html.replace(">P:</b>", ">O:</b>", 1)
        return html, mod, d
    d = REPO / "ace/_mockup/e"
    mod = load(d)
    mod.PERSON = {"name": name, "title": title, "office": phone, "office_tel": tel(phone),
                  "office_label": "O" if source[1] in OFFICE_LINE else "P", "email": sender}
    return mod.signature(pledge=True), mod, d   # E v2, approved


def main():
    PASTE.mkdir(parents=True, exist_ok=True)
    print(f"step 1/2: {len(RULES)} rules", flush=True)
    cards = []
    for i, (rule, sender, source, note) in enumerate(RULES, 1):
        html, mod, d = render(source, sender)
        slug = re.sub(r"[^a-z0-9]+", "-", rule.lower()).strip("-")
        (PASTE / f"{i:02d}-{slug}.html").write_text(html)
        if sender in SHARED:
            local_part, domain = sender.split("@")
            (SHARED_DIR / f"{local_part}-{domain.split('.')[0]}.html").write_text(
                f"""<!doctype html><meta charset="utf-8"><title>{rule}: email signature</title>
<!-- BACKUP ONLY: CodeTwo adds this signature automatically. Paste it into Outlook only if Michael asks,
     or the signature will appear twice. To use: open in a browser, Cmd/Ctrl+A, Cmd/Ctrl+C, then paste
     into Outlook Settings > Signatures. -->
<body style="margin:16px;background:#fff">
{html}</body>
""")
        lo = mod.local(html)
        lo = re.sub(r'src="(?!/|data:)([^"]+)"', lambda m: f'src="{d / m.group(1)}"', lo)
        lo = inline(lo)
        print(f"  {i:2d}. {rule} <{sender}>", flush=True)
        cards.append(f"""<section><h2><span class="n">{i}</span> {rule}</h2>
<p class="meta">Sender: <b>{sender}</b> · paste file <code>docs/rollout/paste/{i:02d}-{slug}.html</code></p>
{f'<p class="note">{note}</p>' if note else ''}<div class="pair">
<div><h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div></div>
<div><h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{re.sub(rf"(?<![-\w])color: ?{INK}", "color: #F2F2F2", mod.outlook_dark(lo), flags=re.I)}</div></div>
</div></section>""")
    print("step 2/2: page", flush=True)
    out = HERE / "signatures-rollout-review.html"
    out.write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signature rollout review</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:16px 24px 48px;max-width:1160px}}h1{{font-size:22px;margin:8px 0}}
h2{{font-size:18px;margin:36px 0 2px}}h3{{font-size:14px;margin:8px 0;color:#555}}
.n{{display:inline-block;min-width:1.6em;padding:0 6px;margin-right:4px;border-radius:4px;background:#49104F;color:#fff;text-align:center}}
.meta{{margin:0 0 4px;color:#444}}.note{{margin:0 0 4px;color:#7a4b00}}.pair{{display:flex;gap:24px;flex-wrap:wrap}}
.mail{{padding:24px;border:1px solid #ccc;border-radius:6px;width:fit-content}}code{{font-size:13px}}</style>
<main><h1>Email signature rollout: one card per CodeTwo rule</h1>
<p>{len(RULES)} rules, one per sender address. Every field is hardcoded until Ntiva fixes the job titles
in Entra. Each card shows the signature on white and in Outlook dark mode (simulated: Outlook recolors
text but not images).</p>
{''.join(cards)}</main>
""")
    print(f"RESULT: ok {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
