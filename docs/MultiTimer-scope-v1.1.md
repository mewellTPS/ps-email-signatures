# MultiTimer — Scope v1.1
**File:** MultiTimer-scope-v1.1.md
**Version:** 1.1 (supersedes v1.0)
**Date:** 2026-05-08
**Maintained by:** Michael
**Repo:** amewell/mobileapp (personal sandbox; not a TPS DEV portfolio repo)

---

## What This Is

A paired iPhone + Apple Watch app delivering 30-second haptic posture reminders. User taps a home screen widget → iPhone app opens → picks session duration → sends start command to Watch → Watch fires haptics every 30 seconds until session ends or user stops it.

Replaces a Shortcuts-based approach that was not viable due to iOS background execution limits suspending loops when the screen locks.

**Project disposition:** Both a learning vehicle (first hands-on Claude Code + iOS development) and a real app intended for personal daily use. Design rigor reflects both — the app needs to work reliably enough to actually use, and the codebase needs to be readable enough to learn from.

---

## v1.1 Changes from v1.0

- **Source of truth split.** v1.0 said "iPhone is always source of truth for session state." This was in tension with the reason for going native (iOS background execution limits prevent iPhone from running a reliable 30-minute timer loop while locked). v1.1 splits the concept: iPhone is source of truth for session *control* (start, stop, duration); Watch is source of truth for session *execution* (timer, haptics, countdown). Watch reports session-end back to iPhone.
- **Timer loop on Watch, not iPhone.** Watch app stays active for the duration of a session natively. iPhone start command includes duration; Watch runs the loop independently; iPhone can be locked, backgrounded, or killed mid-session without affecting execution.
- **iPhone session recovery on app launch.** When iPhone app opens and a session is running on Watch, iPhone queries Watch state and shows the running UI rather than the idle picker.
- **iPhone-only fallback added.** When no Watch is paired (or paired Watch is unreachable), iPhone fires haptics itself. Foreground-only — locked-screen behavior is a known limitation.
- **Async task loop replaces Timer.scheduledTimer hedge.** Decision committed; no "if Swift 6 flags it" wording.
- **iPhone running UI replaces the disabled-picker state.** Whole iPhone screen swaps to running-state view (MM:SS, Stop button) when session is active, mirroring the Watch's two-view pattern.
- **Error states specified.** Watch-not-reachable behavior on Start; malformed-message handling on Watch.

---

## Architecture

### Source of truth split

- **iPhone is source of truth for session control.** Start, stop, duration selection. UI for these actions lives only on iPhone (no local Start button on Watch).
- **Watch is source of truth for session execution.** Once started, Watch runs the timer loop, fires haptics on its own schedule, and tracks countdown state. iPhone does not "drive" the running session.
- **Watch reports back to iPhone on session end.** Either natural completion or user-tapped Stop on Watch sends `sessionEnded` to iPhone.

### Connection-loss behavior

- **iPhone backgrounded or locked mid-session:** Session continues normally. Watch keeps firing haptics. When iPhone reopens, it queries Watch for current state and reflects it.
- **Watch loses connection to iPhone mid-session:** Session continues normally on Watch. When connection restores, Watch's outbound `sessionEnded` (if applicable) is delivered.
- **iPhone app killed mid-session:** Session continues on Watch. On next iPhone app launch, iPhone queries Watch state and recovers the running UI if session is still live.
- **Watch app force-quit mid-session:** Session is lost. No recovery — acceptable for a 30-minute posture reminder.
- **Both devices killed simultaneously:** Session is lost. Acceptable.

### iPhone-only fallback (no Watch paired or Watch unreachable)

When iPhone determines no Watch is available to receive the start command, iPhone fires haptics itself using `UINotificationFeedbackGenerator` (or equivalent Taptic Engine API).

**Known limitation:** iPhone-fired haptics work only while the app is in the foreground. If the user locks their phone or switches apps during an iPhone-only session, the haptic loop will be suspended by iOS background execution limits. This is the same limitation that pushed the project off Shortcuts. UI must communicate this clearly when iPhone-only mode is engaged ("Keep the app open — your phone can't buzz on its own when locked").

The fallback exists for users who don't have a Watch but still want posture reminders during focused work sessions. It is explicitly a degraded experience compared to the Watch path.

### Shared timer-loop logic

Both the Watch and iPhone-fallback paths run the same 30-second-interval timer loop. Logic is shared via a common `HapticTimerEngine` (struct or actor — design call during build) that takes a duration and a "fire haptic" callback, with platform-specific implementations supplying the actual haptic call.

---

## Design Decisions Log

### Why native Swift over Shortcuts
Shortcuts repeat loops pause when the screen locks. There is no reliable workaround for a 30-second interval background task without native app execution.

### Why paired app (not Watch-only)
- User explicitly requested a home screen widget trigger on iPhone
- Widget → URL scheme → iPhone app → WatchConnectivity is the only reliable widget-to-Watch path
- A Watch-only app cannot be triggered from an iPhone widget

### Why WatchConnectivity over other IPC
- Only supported mechanism for real-time bidirectional iPhone ↔ Watch messaging
- `sendMessage` used for session start/stop commands (requires both devices reachable)
- `transferUserInfo` used as fallback for `sessionEnded` notifications when iPhone is unreachable at the moment of session end

### Why Watch owns the timer loop
Watch app stays active for the duration of a session natively. iPhone cannot guarantee active execution for a 30-minute background haptic loop without abusing a background mode entitlement (no standard background mode legitimately covers "fire a haptic every 30 seconds"). iPhone sends start command with duration; Watch runs the loop; Watch sends session-end notification back. iPhone retains source-of-truth ownership for session *control* but not session *execution*.

### Why iPhone recovers running-session UI on launch
A user who closes the iPhone app and reopens it mid-session expects to see the running session, not the idle picker. iPhone queries Watch state via `sendMessage` on launch (or reads queued `transferUserInfo`) and reflects current state. Cheap to build; alternative feels broken.

### Why iPhone-only fallback exists
Users without an Apple Watch can still use the app for foreground-only posture reminders. Foreground-only is a real limitation, communicated in UI when this mode is active. The fallback is degraded but useful.

### Why `.notification` haptic
- Strongest haptic available via `WKInterfaceDevice.current().play()`
- Appropriate for attention-getting posture reminders
- Can be swapped to `.directionUp`, `.success`, or `.click` — not hardcoded

### Why haptic fires on session start
- Immediate confirmation Watch received the command
- Avoids a 30-second silent window that could appear like a failed start

### Why async task loop, not Timer.scheduledTimer
- Idiomatic Swift 6 pattern for a long-running periodic loop
- Cleanly cancellable via `Task.cancel()`
- Naturally `@MainActor`-isolated; doesn't fight Swift 6 concurrency checking
- Pattern worth learning for future Swift work

### Duration picker design
- Range: 5–60 minutes in 5-minute increments
- Default: 30 minutes
- Wheel picker (`PickerStyle.wheel`)
- Visible only in idle state — replaced entirely by running-state UI when session is active (matches Watch's two-view pattern)
- Duration passed as `Int` (minutes) in WatchConnectivity message payload

### Watch UI states
Two distinct views, no navigation stack:
- **Idle:** Icon + "Waiting for iPhone." No local start button — all session control originates from iPhone.
- **Running:** MM:SS countdown, "next haptic in Xs" label, circular progress ring for 30-second interval, Stop button.
Stop on Watch sends `sessionEnded` back to iPhone.

### iPhone UI states
Two distinct views, mirroring Watch:
- **Idle:** Duration picker + Start button.
- **Running:** MM:SS countdown, Stop button. (Picker is not present; running state is its own view.)

### Widget design
- Static — no timeline refresh, no dynamic data
- Tap fires URL scheme `multitimer://start` → opens iPhone app
- Supports `.systemSmall` and `.systemMedium`
- Widget opens app only — does not start a session directly. Prevents accidental starts from pocket taps.

### Swift 6 concurrency approach
All code Swift 6 strict concurrency safe from the start:
- All UI updates `@MainActor` or via `await MainActor.run {}`
- No `DispatchQueue.main.async` — legacy pattern in Swift 6
- All `WCSessionDelegate` callbacks explicitly isolated to `@MainActor`
- Managers use `@Observable` — no Combine, no `ObservableObject`
- Timer loop implemented as `Task { @MainActor in while ... { try await Task.sleep(for: .seconds(1)); tick() } }`

### No third-party dependencies
SwiftUI, WatchKit, WatchConnectivity, WidgetKit only. No SPM packages.

---

## Error Handling

### iPhone: Watch not reachable when user taps Start
- Start button is always tappable (reachability state can flicker; pre-checking feels worse than a clear error after attempt).
- On `sendMessage` failure or `WCSession.isReachable == false` after attempt, show alert: "Couldn't reach your Watch — make sure it's on your wrist and unlocked. Or start without your Watch (foreground only)."
- Alert offers two paths: retry, or proceed with iPhone-only fallback.

### Watch: malformed message from iPhone
- Log to console (development; gated behind debug flag for release).
- Ignore the message; stay in current state.
- No user-facing error. Malformed messages are bugs, not user conditions.

### iPhone-only mode: app backgrounded or phone locked mid-session
- iOS will suspend the haptic loop. Session effectively pauses.
- When user returns to foreground, app detects suspension gap (compare wall-clock to expected elapsed) and either:
  - Resumes if gap is small (<5 seconds — the user briefly checked something)
  - Ends session and shows "Session interrupted — your phone was locked or another app was used" if gap is larger
- Specific threshold tunable during build.

---

## Persistence

- iPhone session state recovered on app launch by querying Watch (one `sendMessage` call; if unreachable, assume idle).
- No local persistence on iPhone beyond the current launch's recovered state — if both devices restart, session is lost.
- No local persistence on Watch either — Watch holds session state in memory only.
- This is acceptable for a posture-reminder app. A 30-minute session lost to a phone restart is not worth the persistence layer.

---

## Open Build-Time Decisions

These are deliberately deferred until build, when the right answer becomes obvious from context:

- `HapticTimerEngine` as struct vs. actor (concurrency-checking pressure during build will reveal the right call)
- Specific threshold for iPhone-only "interrupted" detection (5s? 10s? 30s? — tune to feel during testing)
- Exact wording of UI strings (will iterate during build)
- Whether widget supports `.systemLarge` or only `.systemSmall` and `.systemMedium` (current scope says small/medium; revisit if large is trivially free)

---

## Out of Scope (v1.1)

Not in this build. Listed to prevent scope creep:

- Multiple concurrent sessions
- Session history or analytics
- Custom haptic patterns beyond the four listed
- Notification-based session reminders ("you haven't done a session today")
- Apple Watch complications
- Custom durations outside the 5–60 minute range
- iCloud sync
- Settings screen (haptic style is hardcoded for v1.1; configurable in a future version if needed)

---

*Personal project. No distribution restrictions.*
