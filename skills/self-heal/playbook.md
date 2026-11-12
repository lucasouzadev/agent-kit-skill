# Self-heal playbook — environment defects

Reset the smallest thing first; each line is one attempt. Re-run the failing command after each.

## iOS simulator
| Symptom | Heal |
|---|---|
| Won't boot / "Unable to boot device in current state" | `xcrun simctl shutdown all`, then `xcrun simctl boot <udid>`; still stuck → `xcrun simctl erase <udid>` (wipes only that simulator) |
| App crashes on launch after native change | rebuild (not just reload): `npx expo run:ios` / `xcodebuild … build`; clear `~/Library/Developer/Xcode/DerivedData/<App>-*` |
| `pod install` errors | `cd ios && pod install --repo-update`; still failing → `pod deintegrate && pod install` |
| Simulator hangs / black screen | `xcrun simctl shutdown <udid> && xcrun simctl boot <udid>`; `killall Simulator` |
| Wrong runtime/device missing | `xcrun simctl list devices available`, pick an existing one; do not download runtimes without asking (large) |

## Android emulator
| Symptom | Heal |
|---|---|
| `device offline` / `unauthorized` | `adb kill-server && adb start-server`; `adb devices` |
| Won't boot / stuck on logo | cold boot: `emulator -avd <name> -no-snapshot-load`; still stuck → `-wipe-data` (only that AVD) |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | `adb uninstall <applicationId>` then install again |
| Gradle daemon / cache errors | `./gradlew --stop`; `./gradlew clean`; delete `android/.gradle` and `android/app/build` |
| Out of memory | close other AVDs; `org.gradle.jvmargs=-Xmx4g` in the user (not project) gradle.properties |

## JS / React Native / Expo
| Symptom | Heal |
|---|---|
| Red box "Unable to resolve module" after install | `npx expo start -c` / `npx react-native start --reset-cache` |
| Port 8081/3000 in use | find the process (`lsof -i :8081`), stop **your own** stale dev server; never kill unknown processes |
| `node_modules` out of sync with lockfile | the project's clean install (`npm ci` / `pnpm i --frozen-lockfile` / `bun i --frozen-lockfile`); never edit the lockfile by hand |
| Jest/Vitest snapshot mismatch | update the snapshot **only** when the diff is the intended change of this task; otherwise it is a bug |

## Web / E2E
| Symptom | Heal |
|---|---|
| Playwright browser missing | use the installed browser; do not reinstall versions the project did not pin |
| Flaky E2E step | re-run that spec once; second failure → defect: read the trace/screenshot, fix the selector or the wait (`expect(...).toBeVisible()`), never `waitForTimeout` |
| Maestro element not found | read the failing screenshot; prefer ids, `extendedWaitUntil`; disable animations |

## CI (feature branch only)
See skill `ci-monitor`. Infra flake (runner lost, network, registry 5xx, timeout) → one re-run of failed jobs if the guard allows it, else report. Defect from the change → fix, push to the same feature branch, watch again.
