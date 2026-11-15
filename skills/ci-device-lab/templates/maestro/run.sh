#!/usr/bin/env bash
# Run Maestro flows and keep only flow names + PASS/FAIL in the public summary.
# Never an empty result: no report or zero flows run = BLOCKED with the reason and the last log lines.
# Usage: bash maestro/run.sh <android|ios>   Env: FLOWS (file/folder), E2E_EMAIL/E2E_PASSWORD (optional),
#   LOG_TAIL (log lines shown when nothing ran; default 15, set 0 in PUBLIC repos: logs are public)
set -uo pipefail
PREFLIGHT="${PREFLIGHT:-.claude/agent-kit/e2e_preflight.py}"
if [ -f "$PREFLIGHT" ]; then python3 "$PREFLIGHT" --flows "${FLOWS:-maestro/flows}" || { echo "BLOCKED: repo preflight failed (fix the FAIL lines above before running devices)"; exit 2; }; fi
platform="${1:?android|ios}"
FLOWS="${FLOWS:-maestro/flows}"
here="$(cd "$(dirname "$0")" && pwd)"
[ -e "$FLOWS" ] || FLOWS="$here/flows"
out="${RUNNER_TEMP:-/tmp}/maestro"; mkdir -p "$out"
tags=()
if [ -z "${E2E_EMAIL:-}" ]; then tags=(--exclude-tags login); echo "no test account: skipping flows tagged 'login'"; fi
env_args=(); [ -n "${E2E_EMAIL:-}" ] && env_args=(-e "E2E_EMAIL=$E2E_EMAIL" -e "E2E_PASSWORD=$E2E_PASSWORD")
[ -n "${APP_ID:-}" ] && env_args+=(-e "APP_ID=$APP_ID")
maestro test "$FLOWS" "${tags[@]}" "${env_args[@]}" \
  --format junit --output "$out/report.xml" --test-output-dir "$out/artifacts" > "$out/maestro.log" 2>&1
rc=$?
# Scrub the test password from text files before they are packaged.
if [ -n "${E2E_PASSWORD:-}" ]; then
  grep -rlF -- "$E2E_PASSWORD" "$out" 2>/dev/null | while read -r f; do sed -i.bak "s|$(printf '%s' "$E2E_PASSWORD" | sed 's/[|&/\]/\\&/g')|***|g" "$f" && rm -f "$f.bak"; done
fi
LOG_TAIL="${LOG_TAIL:-15}" python3 - "$out/report.xml" "$platform" "$out/maestro.log" > "$out/summary.txt" <<'PY'
import os, sys, xml.etree.ElementTree as ET
p, plat, logf = sys.argv[1], sys.argv[2], sys.argv[3]
print(f"### Maestro {plat}")
n = 0
try:
    for tc in ET.parse(p).getroot().iter("testcase"):
        n += 1
        bad = tc.find("failure") is not None or tc.find("error") is not None
        msg = ""
        if bad:
            el = tc.find("failure") if tc.find("failure") is not None else tc.find("error")
            msg = " - " + ((el.get("message") or el.text or "").strip().splitlines() or [""])[0][:160]
        print(f"- {'FAIL' if bad else 'PASS'} {tc.get('name')}{msg}")
except Exception:
    pass
if n == 0:
    k = int(os.environ.get("LOG_TAIL", "15"))
    print("- BLOCKED: no flow ran (no report or empty report)." + (" Last log lines:" if k else " Read maestro.log in the (encrypted) artifacts."))
    try:
        tail = [l.rstrip() for l in open(logf, errors="replace")][-k:] if k else []
    except OSError:
        tail = ["(no maestro.log: the CLI did not start; check install/PATH and the device)"]
    for l in tail:
        print(f"    {l}")
    sys.exit(3)
PY
sum_rc=$?
cat "$out/summary.txt"
[ "$sum_rc" = 3 ] && exit 3
exit $rc
