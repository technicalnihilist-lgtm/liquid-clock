# Liquid Clock — optimisation roadmap, 1 → 20 November 2026

**Ground rule: the app must look exactly the same.** No changes to layout, spacing, colours, typography, wording, icons, motion feel or any screen the user sees. Every item below is invisible: performance, correctness, stability, battery, memory, edge cases and code hygiene.

Ten items per day, twenty days, two hundred in total. Each item is small enough to implement, build and verify on its own. A day is done when all ten are ticked, the APK is rebuilt, signed, pushed and attached to that day's release.

Versioning: day *D* produces `1.(D+2).1` … `1.(D+2).10`, versionCode continuing from 3 (day 1 = 4…13, day 2 = 14…23, … day 20 = 194…203). The final APK of each day goes into `releases/`; all ten go onto the day's GitHub release.

---

## Day 1 — 2026-11-01 — Frame loop and rendering discipline

- [ ] 1.1 Stop the frame loop entirely while `document.hidden` is true, and restart it on `visibilitychange` instead of letting rAF throttle itself.
- [ ] 1.2 Audit every DOM write in `paint()` so a value is written only when it actually changed (extend the existing `put()` guard to the arc offset and the button labels).
- [ ] 1.3 Replace remaining `innerHTML` writes whose markup never varies with `textContent`.
- [ ] 1.4 Compute the 60 tick marks and 12 numerals once at load and reuse the string across mounts instead of rebuilding them per page mount.
- [ ] 1.5 Remove layout reads from the frame loop: cache the nav rect used by the depth engine and refresh it only on resize/mount.
- [ ] 1.6 Drive `dt` from `document.timeline.currentTime` so easing stays correct when the tab is throttled.
- [ ] 1.7 Skip sub-second hand updates when the measured frame interval exceeds 40 ms (battery saver / low-end devices) and fall back to one update per second.
- [ ] 1.8 Drop `will-change` from elements that never animate and keep it only on the three blobs, the lens and the view.
- [ ] 1.9 Guard the loop against a single throw killing all future frames (separate try/catch per subsystem, not one wrapper).
- [ ] 1.10 Re-measure: record frames-per-second and per-frame JS time over 10 s in the run report.

## Day 2 — 2026-11-02 — Stopwatch and timer accuracy

- [ ] 2.1 Rebase the stopwatch on `Date.now()` deltas only at start/stop, and use a monotonic source for the running display so a wall-clock change cannot move the elapsed time.
- [ ] 2.2 Clamp stored stopwatch and timer values to sane ranges on load (no negative elapsed, no `NaN`).
- [ ] 2.3 Fix lap numbering when a lap is added while the stopwatch is stopped mid-run.
- [ ] 2.4 Cap stored laps at 500 and drop the oldest, so localStorage cannot grow without bound.
- [ ] 2.5 Recompute timer state on resume from a killed process: if `end` passed while dead, land in the done state with the alarm flagged as missed.
- [ ] 2.6 Prevent a double-tap on Start from starting, stopping and restarting within one gesture.
- [ ] 2.7 Ignore a resume that would produce a negative remaining time; clamp to zero and mark done.
- [ ] 2.8 Verify the 1/5/10/25 preset buttons rebuild `total` correctly after a finished timer.
- [ ] 2.9 Format timers over one hour without breaking the existing layout width.
- [ ] 2.10 Add a headless test that runs a 3 s timer and asserts the done state fires exactly once.

## Day 3 — 2026-11-03 — Startup cost and memory

- [ ] 3.1 Build the glass-settings sheet lazily on first open instead of at load, and keep it in the DOM afterwards.
- [ ] 3.2 Move non-critical wiring (settings sheet, sensor listeners) to `requestIdleCallback` with a timeout fallback.
- [ ] 3.3 Measure and reduce time-to-first-frame; log the number in the report.
- [ ] 3.4 Release the previous page's nodes and listeners before mounting the next page (no detached subtree growth across tab switches).
- [ ] 3.5 Remove the duplicate `Intl.DateTimeFormat` construction path left over from the cached formatter map.
- [ ] 3.6 Pre-size the arrays used by the depth engine instead of rebuilding them on every mount.
- [ ] 3.7 Confirm `WebView.destroy()` plus `removeJavascriptInterface` run on activity destroy, and null the reference.
- [ ] 3.8 Handle `onRenderProcessGone` by recreating the WebView instead of crashing the activity.
- [ ] 3.9 Trim the initial HTML payload: no dead CSS rules, no unused variables, no commented-out code.
- [ ] 3.10 Record APK size and cold-start frame count in the report; flag any regression against day 2.

## Day 4 — 2026-11-04 — Time, timezone and calendar correctness

- [ ] 4.1 Cache the `toLocaleDateString` formatters used by `dayWord` — it currently allocates two formatters per city per second.
- [ ] 4.2 Recompute the Today/Tomorrow/Yesterday labels exactly once per minute instead of once per second.
- [ ] 4.3 Verify 12-hour formatting at 00:00, 00:59, 12:00 and 12:59 and fix any off-by-one.
- [ ] 4.4 Handle a device timezone that `Intl` cannot resolve by falling back to the system offset instead of throwing.
- [ ] 4.5 Correct the day rollover: at 23:59:59.9 the second hand and the date line must not disagree.
- [ ] 4.6 Guard DST transitions: a city that shifts mid-hour must not show a duplicate or skipped minute.
- [ ] 4.7 Validate the timezone list once at load and drop entries the runtime cannot format.
- [ ] 4.8 Keep the date line locale-stable (weekday, month, day) across devices with unusual locales.
- [ ] 4.9 Add a test that renders every city at a fixed instant and asserts the expected strings.
- [ ] 4.10 Make sure a system clock jump backwards does not make the analog hands stutter or spin.

## Day 5 — 2026-11-05 — Input, gestures and taps

- [ ] 5.1 Cancel in-flight page animations before mounting a new page so rapid tab switching cannot stack animations.
- [ ] 5.2 Swallow the click that follows a nav drag (the existing guard) and extend it to the pill and gear buttons.
- [ ] 5.3 Release pointer capture on `pointercancel` as well as `pointerup`.
- [ ] 5.4 Prevent scroll chaining on the sheet and on the nav so a drag never scrolls the page underneath.
- [ ] 5.5 Tune `touch-action` on the sliders so horizontal drags never scroll the sheet.
- [ ] 5.6 Handle a second finger landing mid-rubber-band without jumping the offset.
- [ ] 5.7 Debounce repeated taps on the 12/24-hour pill so it cannot flip twice from one tap.
- [ ] 5.8 Make the whole nav button area respond, not only the glyph (hit area inside the existing visual bounds).
- [ ] 5.9 Ignore pointer events while the settings sheet is open except on the sheet and scrim.
- [ ] 5.10 Test 50 rapid tab switches headlessly and assert the DOM ends in a consistent state.

## Day 6 — 2026-11-06 — Battery and lifecycle

- [ ] 6.1 Detach the `deviceorientation` listener when the depth slider is at 0 and re-attach when it rises.
- [ ] 6.2 Detach sensor and pointer listeners while the page is hidden.
- [ ] 6.3 Suspend and resume the audio context with the activity lifecycle instead of leaving it running.
- [ ] 6.4 Release the screen-awake flag on pause and restore it on resume only if the app still wants it.
- [ ] 6.5 Pause the WebView (`onPause`) and resume it with the activity — verify timers still behave.
- [ ] 6.6 Reduce the blur radius automatically when the system reports battery saver, without changing the user's saved setting.
- [ ] 6.7 Stop the blob animation when the app is not visible.
- [ ] 6.8 Avoid creating the audio context until the first sound is actually needed.
- [ ] 6.9 Measure CPU while idle on the clock tab for 60 s and report the figure.
- [ ] 6.10 Verify no wake lock or listener survives activity destroy.

## Day 7 — 2026-11-07 — Persistence and migrations

- [ ] 7.1 Version the stored schema and migrate old keys forward on load.
- [ ] 7.2 Validate and clamp every restored value (settings, stopwatch, timer) instead of trusting storage.
- [ ] 7.3 Debounce storage writes so a slider drag writes once on release, not once per frame.
- [ ] 7.4 Handle `QuotaExceededError` by pruning the lap list and retrying once.
- [ ] 7.5 Restore the last active tab so a relaunch lands where the user left off.
- [ ] 7.6 Detect and clear corrupted JSON instead of silently falling back to defaults forever.
- [ ] 7.7 Avoid the flash of default values on cold start by reading storage before the first paint.
- [ ] 7.8 Store only the fields that differ from the defaults.
- [ ] 7.9 Make `store.set` never throw, even with storage disabled.
- [ ] 7.10 Add a migration test: write v1-shaped data, load, assert the new shape.

## Day 8 — 2026-11-08 — Accessibility and semantics (no visual change)

- [ ] 8.1 Give the icon-only buttons real `aria-label`s.
- [ ] 8.2 Add `aria-live="off"` to the digital readout so screen readers do not announce every second.
- [ ] 8.3 Add `role="tablist"` / `role="tab"` / `aria-selected` to the nav without touching its styling.
- [ ] 8.4 Announce timer completion politely once, not every frame.
- [ ] 8.5 Respect `prefers-reduced-motion` in the depth engine and the page transitions.
- [ ] 8.6 Ensure every interactive element is reachable and operable by keyboard.
- [ ] 8.7 Label the range inputs with their setting name (already partly done — verify all six).
- [ ] 8.8 Verify focus order matches visual order on all three tabs.
- [ ] 8.9 Keep the sheet dismissible with Escape.
- [ ] 8.10 Run an automated accessibility snapshot and fix what it flags.

## Day 9 — 2026-11-09 — Error handling and crash-proofing

- [ ] 9.1 Wrap every user-triggered handler in a guard so one exception cannot break the page.
- [ ] 9.2 Add a global `error` and `unhandledrejection` handler that logs and keeps the loop alive.
- [ ] 9.3 Null-check every cached element reference after a re-render.
- [ ] 9.4 Guard `Intl`, `localStorage`, `AudioContext`, `navigator.vibrate` and `getAnimations` behind feature checks.
- [ ] 9.5 Prevent `show()` from recursing when a transition is interrupted repeatedly.
- [ ] 9.6 Catch and recover from a failed `mount()` by falling back to a fresh render of the current tab.
- [ ] 9.7 Guard the JS bridge so a missing native method never throws into the loop.
- [ ] 9.8 Add a native-side guard around `evaluateJavascript` calls after destroy.
- [ ] 9.9 Log the WebView console to logcat only in debug builds.
- [ ] 9.10 Fault-inject: break storage, break audio, break Intl in tests and confirm the UI still works.

## Day 10 — 2026-11-10 — Paint cost and compositing

- [ ] 10.1 Audit `backdrop-filter` usage and keep the blur radius inside what a mid-range GPU can composite at 60 fps.
- [ ] 10.2 Add `contain: paint` to the glass cards so their shadows and highlights cannot invalidate neighbours.
- [ ] 10.3 Confirm no animation touches `box-shadow`, `filter` or layout properties.
- [ ] 10.4 Reduce the blob blur cost on low-end devices without changing their appearance at rest.
- [ ] 10.5 Promote only the layers that actually animate; drop the rest.
- [ ] 10.6 Make the specular highlight update cheap: quantise `--lx/--ly` so they change at most a few times per second.
- [ ] 10.7 Avoid restyling the whole document when a single CSS variable changes.
- [ ] 10.8 Verify the glass still renders correctly in dark mode after the containment changes.
- [ ] 10.9 Measure paint time per tab and report it.
- [ ] 10.10 Confirm scrolling the world clock list stays at 60 fps with depth enabled.

## Day 11 — 2026-11-11 — JavaScript micro-optimisations

- [ ] 11.1 Remove per-frame allocations: no array literals, no template strings and no closures inside the loop.
- [ ] 11.2 Cache tab indices and the tab list lookups instead of calling `findIndex` on every interaction.
- [ ] 11.3 Convert the hot loops to plain indexed `for` loops.
- [ ] 11.4 Cache the strings produced by the formatters for a whole second and reuse them.
- [ ] 11.5 Avoid re-parsing stored JSON on every read; keep an in-memory copy.
- [ ] 11.6 Short-circuit world-clock updates when the minute has not changed.
- [ ] 11.7 Replace `Math.max/min` chains in the hot path with a single clamp helper.
- [ ] 11.8 Avoid `getComputedStyle` at runtime; resolve the spring easing once at load.
- [ ] 11.9 Verify with a profiler that no function allocates in the steady state.
- [ ] 11.10 Report the per-frame JS budget before and after.

## Day 12 — 2026-11-12 — Animation smoothness

- [ ] 12.1 Compose the depth transform and the entry animation instead of letting the inline transform fight the Web Animation.
- [ ] 12.2 Cancel stale animations before starting new ones on the same element.
- [ ] 12.3 Make page transitions FLIP-based so they never reflow.
- [ ] 12.4 Cap the stagger delay so a long list cannot take seconds to settle.
- [ ] 12.5 Ensure the lens and the page transition share one duration so they never look out of step.
- [ ] 12.6 Avoid starting an animation on an element that is off-screen.
- [ ] 12.7 Keep the spring easing identical across browsers with the existing `linear()` fallback.
- [ ] 12.8 Verify no animation frame is dropped during a tab switch on a mid-range device profile.
- [ ] 12.9 Respect reduced motion in every new animation added since day 1.
- [ ] 12.10 Report the longest frame during a tab switch.

## Day 13 — 2026-11-13 — Layout stability

- [ ] 13.1 Verify no cumulative layout shift on load, on theme switch and on tab switch.
- [ ] 13.2 Keep the digital readout width stable at every digit count.
- [ ] 13.3 Prevent the content from jumping when the scrollbar appears or disappears.
- [ ] 13.4 Restore scroll position when returning to a tab.
- [ ] 13.5 Make sure the safe-area insets apply once, not twice, on notched devices.
- [ ] 13.6 Clamp the rubber-band offset so the page cannot be dragged beyond its bounds.
- [ ] 13.7 Confirm the nav never overlaps content in a way that blocks a tap.
- [ ] 13.8 Verify the sheet height with all six sliders on a short screen.
- [ ] 13.9 Keep the clock face circular at every viewport width.
- [ ] 13.10 Test at 320×568, 412×915 and 480×1200 and report any shift.

## Day 14 — 2026-11-14 — Settings quality

- [ ] 14.1 Clamp every slider to its range on load and on input.
- [ ] 14.2 Add per-setting reset without adding a new visible control (long-press on the label).
- [ ] 14.3 Write to storage only on release, never during the drag.
- [ ] 14.4 Migrate any out-of-range stored value to the nearest valid one.
- [ ] 14.5 Validate that a stored depth of 0 truly disables the engine (no listener, no transforms).
- [ ] 14.6 Keep the reset-all behaviour after the lazy sheet refactor.
- [ ] 14.7 Make the sheet remember nothing it should not (no stale DOM state between opens).
- [ ] 14.8 Ensure the settings survive a theme switch and an app restart.
- [ ] 14.9 Verify the readouts update live while dragging without layout shift.
- [ ] 14.10 Test with every slider at minimum and at maximum simultaneously.

## Day 15 — 2026-11-15 — Native shell

- [ ] 15.1 Use the insets animation API so rotation and keyboard changes do not jump.
- [ ] 15.2 Never reload the page on a configuration change.
- [ ] 15.3 Reduce bridge calls: batch insets and theme pushes instead of one call each.
- [ ] 15.4 Handle `onTrimMemory` by letting the WebView release what it can.
- [ ] 15.5 Recreate the WebView on `onRenderProcessGone` and restore state.
- [ ] 15.6 Guard `evaluateJavascript` against a null WebView after destroy.
- [ ] 15.7 Make the back button close the sheet, then return to the clock tab, then exit — verified in one test.
- [ ] 15.8 Keep the status bar icon contrast correct in both themes after every resume.
- [ ] 15.9 Handle a WebView load error without showing a blank screen.
- [ ] 15.10 Verify the app survives being backgrounded for 30 minutes and resumed.

## Day 16 — 2026-11-16 — Audio and haptics reliability

- [ ] 16.1 Unlock the audio context on the first user gesture so the timer beep is never silent.
- [ ] 16.2 Reuse one gain node instead of building three per beep.
- [ ] 16.3 Stop any in-flight beep when the timer is reset or the app is hidden.
- [ ] 16.4 Fall back to the native vibrator when `navigator.vibrate` is missing.
- [ ] 16.5 Debounce haptics so a rapid tap sequence does not queue a long buzz.
- [ ] 16.6 Verify the vibrate permission path on a device without a vibrator.
- [ ] 16.7 Make the completion buzz and beep fire together, not 200 ms apart.
- [ ] 16.8 Ensure no audio plays when the timer completes while the app is hidden.
- [ ] 16.9 Check that repeated timers do not leak oscillators.
- [ ] 16.10 Report measured latency from timer end to first sound.

## Day 17 — 2026-11-17 — Formatting edge cases

- [ ] 17.1 Correct midnight and noon in 12-hour mode across all cities.
- [ ] 17.2 Keep the AM/PM suffix consistent with the existing styling.
- [ ] 17.3 Round seconds at the boundary so 59.6 s never displays as 60.
- [ ] 17.4 Guard against negative or `NaN` durations reaching the formatter.
- [ ] 17.5 Confirm hour-long and multi-hour timers still fit the ring readout.
- [ ] 17.6 Verify the stopwatch centiseconds never jump backwards on a slow frame.
- [ ] 17.7 Make the date line correct at month and year boundaries.
- [ ] 17.8 Confirm the world clock list ordering is stable across timezones.
- [ ] 17.9 Check that a device set to a 24-hour locale still respects the in-app toggle.
- [ ] 17.10 Snapshot-test every formatter output at fixed instants.

## Day 18 — 2026-11-18 — Build pipeline and APK

- [ ] 18.1 Fail the build if the APK exceeds 300 KB.
- [ ] 18.2 Verify signature and alignment as part of every build.
- [ ] 18.3 Make the build deterministic: same source, same tree.
- [ ] 18.4 Inject versionName and versionCode from one place only.
- [ ] 18.5 Trim icon PNGs without changing how they look.
- [ ] 18.6 Confirm `--release` dex optimisation is applied.
- [ ] 18.7 Add a build report line: version, size, signature digest, asset count.
- [ ] 18.8 Keep the workflow file in sync with the local build script.
- [ ] 18.9 Verify the APK installs over the previous versionCode without a wipe.
- [ ] 18.10 Document the release procedure in the repo.

## Day 19 — 2026-11-19 — Stress and soak testing

- [ ] 19.1 Soak: 10 minutes on the clock tab, measure memory growth and report it.
- [ ] 19.2 Stress: 200 rapid tab switches, assert no leak and no stuck state.
- [ ] 19.3 Stress: 100 laps, assert the list stays responsive.
- [ ] 19.4 Stress: timer started, reset, restarted 50 times.
- [ ] 19.5 Stress: theme toggled 100 times.
- [ ] 19.6 Stress: every slider dragged to both ends repeatedly.
- [ ] 19.7 Verify no listener count growth after all of the above.
- [ ] 19.8 Verify no timer or interval leaks.
- [ ] 19.9 Commit the smoke-test script to the repo so it runs every day after this.
- [ ] 19.10 Report a pass/fail table for all of the above.

## Day 20 — 2026-11-20 — Final audit

- [ ] 20.1 Re-run every test from days 1–19 against the final build.
- [ ] 20.2 Re-measure startup, frame budget, idle CPU, memory and APK size.
- [ ] 20.3 Fix anything the audit finds.
- [ ] 20.4 Consolidate the changelog for the whole series.
- [ ] 20.5 Add a performance section to the README with the measured numbers.
- [ ] 20.6 Confirm the UI is pixel-identical to the 1.2.0 baseline.
- [ ] 20.7 Verify all 200 roadmap items are ticked or explicitly deferred with a reason.
- [ ] 20.8 Publish the final APK and release notes.
- [ ] 20.9 Write the series summary report.
- [ ] 20.10 Close the series: no further scheduled runs after 20 November.

---

## Hard rules for every day

1. **No visual change.** No edits to layout, spacing, colour, typography, copy, iconography, motion feel, or any element the user sees. If a fix would be visible, defer it and note it.
2. **Nothing removed.** All existing features keep working exactly as they do.
3. **Every change is verified.** Build, sign, install-check by `apksigner`, and a headless render of all three tabs plus the settings sheet.
4. **Every change is reversible.** One item, one commit message, so a bad change can be reverted alone.
5. **Report honestly.** If an item cannot be done safely, say so and leave it unticked rather than shipping something broken.
