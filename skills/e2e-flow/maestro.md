# Maestro — patterns that keep flows stable

## Selectors
- Prefer `id:` (React Native `testID`, iOS `accessibilityIdentifier`, Android `resource-id`, Compose `testTag`) over visible text; text changes with copy and locale.
- No id yet? Add one to the component in the same change; `e2e_preflight.py` checks every flow id exists in source.
- Find what the screen really exposes: `maestro hierarchy` (or Maestro Studio) on the failing screen; compare with the flow.

## Waiting
- `extendedWaitUntil: { visible: { id: "home" }, timeout: 20000 }` after launches, navigation and network calls; never fixed sleeps.
- `waitForAnimationToEnd` before asserting on animated screens; disable animations on Android CI (`disable-animations: true` / `adb shell settings put global animator_duration_scale 0`).
- `retry: { maxRetries: 1, commands: [...] }` only around a step classified as a flake, with a comment why.

## State
- `launchApp: { clearState: true }` at the start of every independent flow; `clearKeychain: true` on iOS when login state leaks.
- One dedicated test account per environment; credentials through `-e E2E_EMAIL=… -e E2E_PASSWORD=…` (secrets in CI), never in the flow file.
- Flows that need a logged-in user call a shared `runFlow: login.yaml` instead of duplicating steps.

## Debugging a failure (in this order)
1. `artifacts/` screenshot of the failing step and the junit message (first failing command).
2. `maestro test flow.yaml --debug-output debug/` locally; `~/.maestro/tests/<timestamp>/` holds logs and screenshots of local runs.
3. View hierarchy at the failing step: is the element there with another id/text, off-screen (`scrollUntilVisible`), behind a modal/keyboard (`hideKeyboard`), or not rendered yet (wait)?
4. Device log: `adb logcat -d | tail -200` (Android) / `xcrun simctl spawn booted log show --last 5m` (iOS) for crashes.

## Common causes → fix
| Symptom | Class | Fix |
|---|---|---|
| `Element not found` right after launch | timing / env | wait for a stable id; check the app actually installed and launched (crash on start?) |
| Works locally, fails in CI | env / data | different build type, locale, screen size, missing secret, backend URL; compare preflight NEEDS with the workflow env |
| Fails only on second run | state | `clearState`, logout step, unique test data per run |
| `appId` mismatch / app not found | env | flow appId vs bundle id / applicationId (preflight checks it) |
| Empty report, no flows | env | wrong `FLOWS` path, all flows excluded by tags, CLI not installed; `run.sh` prints BLOCKED with the log tail |
