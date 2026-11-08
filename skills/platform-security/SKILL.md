---
name: platform-security
description: Security and performance considerations by platform type - native mobile (iOS/Android), web, hybrid apps with a WebView and native bridge (e.g. Capacitor/Cordova), and desktop apps on a web runtime (e.g. Electron/Tauri). Use when touching platform code, deep links, IPC, WebViews, headers/CSP, third-party scripts, auto-update or OTA bundles.
---

# Platform security and performance

Open only the section for your platform. Core principles: `security-core`, `performance-core`.

| Platform | Read |
|---|---|
| Native mobile (Swift/Kotlin, React Native/Flutter native layer) | [native-mobile.md](native-mobile.md) |
| Web (pages, APIs, headers, third-party scripts) | [web.md](web.md) |
| Hybrid with WebView + native bridge | [hybrid-webview.md](hybrid-webview.md) |
| Desktop on a web runtime (renderer + privileged process) | [desktop-webruntime.md](desktop-webruntime.md) |

## Always true
- Every platform boundary (bridge, IPC, intent, URL scheme, deep link, postMessage) receives hostile input: minimal surface, validate on the privileged side, deny by default.
- Client-side hardening (obfuscation, root/jailbreak detection, pinning, attestation) only raises attack cost; it never replaces server controls.
- The update channel is code execution on every client: signed, verified, anti-rollback (`supply-chain`).
