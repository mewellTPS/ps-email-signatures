# Soft-launch rollout (2026-10-29)

Fifteen hardcoded CodeTwo cloud rules, one per sender address, went live on 2026-10-29. Every field is
hardcoded until Ntiva fixes Entra job titles; then people move back to the brand `default.html`
(see `docs/entra-fixes.md`). Faith's ACE rule (`09-ace-faith-collier.html`) is built but not created yet.

## Files

| Path | What |
|---|---|
| `paste/NN-*.html` | Generated paste source per rule (with comments). Built by `docs/review/build-rollout.py`. |
| `paste-clean/NN-*.html` | The same with comments stripped: **exactly what is in CodeTwo** (verified by clipboard round-trip). |
| `codetwo-before/*.html` | The template each edited rule had before 2026-10-29. Paste one back to roll a rule back. |
| `stage-assets.py` | Copies the images the paste files need into ps-assets; never overwrites. Dry run by default. |
| `verify-live.py` | Checks every ps-assets file against assets.purple-standard.app by SHA-256. |
| `../../shared-mailbox/*.html` | Backup copy/paste files for the PS shared mailboxes. CodeTwo signs these addresses; paste only if a rule is turned off. |

## What was verified

- ps-assets deployed by Michael (dashboard upload); `verify-live.py` 62/62 match. Before the deploy the same check found the 26 new files missing (positive control).
- Each rule's template was copied back out of the CodeTwo source editor and diffed against `paste-clean/`: identical for all 15. Every image URL in each file returned 200.
- CodeTwo Test Rules, sender chosen with **Select** (the From box is read-only and silently defaults to the signed-in user): each of the 15 addresses applied its own rule and no other.

## Changes since launch

- **2026-10-30:** three rules re-pasted, each verified by copying the saved source back out and diffing it against `paste-clean/` (identical), then by Test Rules (each sender applied its own rule).
  - **PS - Brady Bodden:** a blank line, then "Thanks," in Outlook's body font, above the block.
  - **ACE - Nan Mallory** and **PS - Nan Mallory (shared mailbox):** a blank line above the block, with her name kept. Nan keeps her own Outlook signature with only her closing ("Thanks, Nan"). Fonts aren't sent with mail, so her Lucida Handwriting only shows where it is installed; a CodeTwo closing would not look like hers on Mac or iPhone.
  - Michael's hand-added "Thanks," edits on Brady's and Nan's PS rules were replaced. The live sources from before this change are in `codetwo-before/ps-brady-2026-10-30.html` and `codetwo-before/ps-nan-shared-2026-10-30.html`. Nan's ACE rule matched `paste-clean/` before, so its old version is in git history.

- **2026-11-03:** **ACE - Ryan Clarke** and **PS - Ryan Clarke (shared mailbox)** re-pasted. Each has a blank line above the block, and the phone line is removed at Ryan's request (the email line takes its 8px top margin). `build-rollout.py` gains `NO_PHONE`. Before the paste, both live sources matched `paste-clean/` at HEAD, so the old versions are in git history. Each saved rule was reopened, and its source was copied back out and diffed against `paste-clean/`: identical. Senders were not changed, so Test Rules was not re-run.

- **2026-11-05:** **ACE - Patty Clarke** created (rule 17, sender pclarke@acesepticandwaste.com). Default ACE template with no job title or phone line (`build-rollout.py` gains `NO_TITLE`), plus a blank line and "Thanks," above the block. The saved source was copied back out and matched the paste file (whitespace aside); it is `paste-clean/17-ace-patty-clarke.html`. Test Rules with sender pclarke@acesepticandwaste.com: her rule applied, the other 15 were skipped. Entra also lists a second Patty Clarke mailbox, pclarkeold@septicandwaste.com, which this rule does not cover.


## Rule map

| Rule | Sender | Was |
|---|---|---|
| BPW - Danny Boyette | dboyette@BoyettePumpWell.com | Boyette |
| WTR - Sean Myatt | smyatt@wtrdr.com | WTR DR |
| PC - Kenny Morrow | kmorrow@purple-current.com | Purple Current |
| BRS - Victor Rodriguez | vrodriguez@brisaclimate.com | Brisa Climate |
| TYR - John Rodrigues | Jrodrigues@tyrianroofing.com | Tyrian Roofing |
| ACE - Ryan Clarke | rclarke@acesepticandwaste.com | ACE Septic Ryan (was unpublished, no design) |
| ACE - Nan Mallory | nmallory@acesepticandwaste.com | new (split from Nan Shared Mailbox) |
| ACE - Kelly Lanzone | klanzone@acesepticandwaste.com | new (split from Kelly Shared Mailbox) |
| ACE - Patty Clarke | pclarke@acesepticandwaste.com | new (2026-11-05) |
| PS - Brady Bodden | bbodden@purple-standard.com | Purple Standard (jirvine, mewell removed) |
| PS - Michael Ewell | mewell@purple-standard.com | new |
| PS - Josh Irvine | jirvine@purple-standard.com | new |
| PS - Nan Mallory (shared mailbox) | nmallory@purple-standard.com | Purple Standard - Nan Shared Mailbox |
| PS - Ryan Clarke (shared mailbox) | rclarke@purple-standard.com | Purple Standard - Ryan Shared Mailbox (was unpublished, no design) |
| PS - Faith Collier | fcollier@purple-standard.com | Purple Standard - Faith |
| PS - Kelly Lanzone (shared mailbox) | klanzone@purple-standard.com | Purple Standard - Kelly Shared Mailbox |
