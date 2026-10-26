# Handoff: Email-signature task consolidation in Asana (2026-10-23)

From: Michael Ewell's Claude Code session (email-signatures build).
To: Bjolan Holyoak's Claude instance (Asana organization, analytics, reporting).
Status: Consolidation written. Old-task closures NOT done. Your instance decides how to close them and how to report it.

## 1. What happened

Michael asked for every open email-signature item to be tracked under one parent task. On 2026-10-23 this session:

1. Wrote the description of the parent task `1219829427750825` "Marketing - Email Signatures" (project DEV and Automation `1214004056241063`, section Marketing). Michael created this task himself the same day.
2. Created 9 grouping subtasks under it (one per brand, plus one cross-brand group).
3. Created 41 work items under those 9 subtasks.
4. Changed no existing task. All 26 source tasks are still open, unedited, in their original projects.

**This was a reorganization, not new work.** 21 of the 41 items carry work that already existed in 26 older tasks; several older tasks were merged into one item. 20 items are new, written from repo/vault notes that were never in Asana (listed in section 4).

## 2. Reporting guidance (main reason for this handoff)

- Do NOT report this as "41 tasks opened". Report: 26 existing tasks consolidated into 21 items; 20 previously untracked items added; 9 grouping subtasks created.
- Do NOT report closing the 26 old tasks as "26 tasks completed". None were finished on 2026-10-23. Closing them is a move. If your workflow must close by completing, tag or comment them as "consolidated", and exclude them from throughput/velocity.
- Grouping subtasks (section 3) are containers, not work. Exclude them from work counts.
- Real work done 2026-10-23, for activity reporting if wanted: ACE c-suite signature designed (4 options, Michael chose D), CodeTwo-ready template built (`ace/signature-ace-csuite.html`, not yet loaded into CodeTwo); Outlook add-in options researched; this consolidation.
- Earlier real completion hidden inside an old task: on 2026-09-04 the Brisa address, Facebook/Instagram/Google links, and review link were finished. Old task `1217564147740995` still shows them as open.

## 3. New structure

Parent `1219829427750825`. Grouping subtasks (naming: `(CODE) Brand email signature`):

| GID | Name |
|---|---|
| 1219831637957734 | (ALL) Rollout & infrastructure — cross-brand / program work |
| 1219831616665316 | (PS) Purple Standard email signature — PS's own signature only |
| 1219831616645600 | (ACE) ACE Septic email signature |
| 1219831569332302 | (BPW) Boyette email signature |
| 1219831569394899 | (BRS) Brisa email signature |
| 1219831637955140 | (TYR) Tyrian email signature |
| 1219831616637111 | (WTR) WTRDR email signature |
| 1219831572727496 | (PC) Purple Current email signature |
| 1219831637886082 | (DAT) Datova email signature |

Categorization rule: work about the program (CodeTwo, Entra profile data, Outlook add-in, hosting, image standards, testing, repo cleanup) goes under (ALL). Work on one brand's signature goes under that brand. Purple Standard's own signature is a brand like the others; do not file program work under (PS).

Known gaps for your reporting:
- **Subtasks have no project membership** (`projects: []`). Project-level views, searches, and reports on DEV and Automation will not see them. Traverse from the parent, or add them to the project.
- **No custom fields set** on any subtask (Business Area, Priority, Urgency, Timeline, Status, Date Added). The parent has Urgency High, Timeline Preferred, Status Ongoing, due 2026-10-26.
- **Display order is scrambled.** Asana created the subtasks concurrently. Reorder in the UI if order matters.
- **Assignment:** only the 7 address items and Danny's phone item are assigned (Michael, with the original due dates). Michael currently has two open copies of each of these 8 in My Tasks until the old ones are closed.

## 4. Old-to-new mapping

### 4a. Old tasks with a human requester (brand projects)

| Old GID | Old task (project) | New item GID |
|---|---|---|
| 1219749322087211 | PS - Email Signature Address Update (Purple Standard) | 1219831569937629 |
| 1219749099512472 | BRS - Email Signature Address Update (Brisa Climate) | 1219831638007953 |
| 1219749174471120 | WTR - Email Signature Address Update (WTR DR) | 1219831638876480 |
| 1219749174808042 | TYR - Email Signature Address Update (Tyrian Roofing) | 1219831461300892 |
| 1219749175678535 | BPW - Email Signature Address Update (Boyette) | 1219831638772911 |
| 1219749175843659 | DAT - Email Signature Address Update (Datova EI) | 1219831638784424 |
| 1219749284805093 | PC - Email Signature Address Update (Purple Current) | 1219831617341943 |
| 1219592769906734 | BPW - Update Danny Phone Number in Email Signature (Boyette; Josh Irvine comment) | 1219831573329339 |

The 7 address tasks were requested by Bjolan on 2026-10-21 (due 2026-10-23). New address for all except ACE: 21516 Carson Dr, Land O Lakes, FL 34639. ACE (8005 Land O' Lakes Blvd) had no task; a confirm item exists (`1219831569991614`). Datova has no signature built yet, so its address task has nothing to update.

### 4b. Old tasks generated by Claude (DEV Project Board `1217351463270253`)

These came from Claude's next-step.md migration (2026-08-17) or Claude session closes. They have no comments and no human history.

| Old GID | Summary | New item GID |
|---|---|---|
| 1217564115620431 | Decide image delivery (embedded vs hosted) | 1219831461397180 |
| 1217564243857061 | Rule: don't host on Google Drive | 1219831461397180 (merged) |
| 1217564258282406 | Review-badge service inputs | 1219831616785102 |
| 1217564087303664 | Choose PS v2 / v3 / v3+strip | 1219831616972228 |
| 1217564115151154 | Choose brand-strip spacing | 1219831616972228 (merged) |
| 1217564233844815 | Upload c-native icons | 1219831617034148 |
| 1218201363497399 | Deploy six brand-*.png strip icons | 1219831617034148 (merged) |
| 1217564272768560 | Send per-brand website URLs | 1219831617034148 (merged) |
| 1217564109930398 | Confirm CodeTwo accepts animated GIF | 1219831617034148 (merged) |
| 1219468726810873 | Recheck PS dark-mode images | 1219831573234200 |
| 1219468469909652 | Confirm deleted brands PNGs intended | 1219831569752288 (one bullet) |
| 1217564272776891 | Ask ACE for simplified icon | 1219831569937705 |
| 1217564116623941 | Fix ACE host WebP | 1219831461722060 |
| 1217564272946961 | Provide 4 Boyette badge URLs | 1219831462026225 |
| 1218201356671602 | Brisa office phone | 1219832027053062 |
| 1217564147740995 | Brisa info (phone, address, socials, palette) | 1219832027053062 (phone) + 1219831617282501 (palette); rest done 2026-09-04 |
| 1217564148686133 | Tyrian socials / address / domain | 1219831461861242 (address part answered by 1219831461300892) |
| 1219468470024712 | WTR DR Glossy orb decision | 1219831570010859 |

### 4c. Referenced only; leave open

`1217564007930184` and `1219236560487254` belong to the hub-platform build. Item `1219831616796381` links to them. Do not close them as part of this consolidation.

### 4d. New items with no older task (20)

(ALL): 1219831616848665 Entra profile fixes (missing phones/titles), 1219831572535553 Outlook add-in rollout, 1219831461344584 validate default.html in CodeTwo, 1219831616796381 hosting reference, 1219831569653170 96 DPI image spec, 1219831616850091 Outlook testing, 1219831572942901 MOR decision. 1219831569752288 Repo housekeeping is mostly new; one bullet came from 1219468469909652.
(PS): 1219831569968948 link colour.
(ACE): 1219831461997919 load c-suite template, 1219832027051746 department signatures, 1219831617216472 promo banner, 1219831569991614 confirm 8005 address.
(BPW): 1219831462001724 Reddick location, 1219831616782649 old file cleanup, 1219831617077634 body font.
(WTR): 1219831569720622 finish signature, 1219832027149458 Mobile line.
(PC): 1219831638672807 Mobile line.
(DAT): 1219831572942633 logo/brand assets, 1219831573434377 build signature.

## 5. Closure recommendations (your instance decides)

Michael approves each closure before it happens. Recommendations only:

1. **4a (8 tasks with human requesters):** keep the originals as the record, and delete this session's copies instead. Then re-parent each original under its brand subtask. Reason: the originals hold Bjolan's request, Josh's comment, brand-project membership, and history. This also avoids a duplicate open/close pair in metrics. Before deleting a copy, carry over its extra notes into the original (repo file list, the Entra explanation on Danny's item, the Datova "no signature yet" note). Alternative: keep the copies and close the originals as consolidated.
2. **4b (18 Claude-generated DEV Project Board tasks):** delete, don't complete. None were finished; all content is preserved in the new items. Exception to consider: `1217564147740995` (Brisa) includes real work finished 2026-09-04. If you report completions, attribute that work to 2026-09-04, not to the closure date.
3. **4c:** leave open.
4. Asana rule from Michael's setup: each state change names exactly one task GID; no bulk operations. Claude writes are limited to DEV Project Board `1217351463270253` and DEV and Automation `1214004056241063`. The 4a originals live in brand projects, so changing them may fall outside that limit; confirm with Michael.

## 6. Facts your instance should know

- CodeTwo Email Signatures 365 runs in cloud mode and **works** (Michael, 2026-10-23). The signature is added about 30 seconds after sending; nothing shows while drafting. Earlier Asana/vault notes saying "no signatures are applied" (from 2026-07-31 and 2026-08-03) are out of date.
- The most common staff complaints (missing phone numbers and titles) come from Microsoft Entra profile data, not the templates. Track them under (ALL) item 1219831616848665, not as per-brand design work.
- Business Area suggestion for this tree: "IT/Infrastructure" for (ALL) items; leave brand design items to your judgment. This is a suggestion; the field is unset.
