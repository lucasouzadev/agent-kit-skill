# Hybrid (WebView + native bridge)

- **The native bridge is the most dangerous trust boundary in the app.** XSS in WebView content becomes calls to native APIs with the app's privileges. Expose a minimal, task-specific surface and validate arguments on the native side. *Essential* (Android "WebView – Native bridges"; MASTG "Restrict Native Functionality Exposed Through WebView Bridges").
- **Untrusted remote content never runs in a WebView with a bridge.** Expose JS interfaces only to content you wrote; do not navigate to third-party pages; remove the interface before loading untrusted content. External links open in the system browser. *Essential.*
- **CSP for bundled content too**, HTTPS for anything remote, JavaScript and file access only if needed. *Essential.*
- **Secrets:** the bundled web code is as readable as a website. *Essential.*
- **OTA web-bundle updates** are an update channel: signature, verification, anti-rollback, compatibility with the installed native runtime, store policies. *Essential.*
- **Platform capabilities behind one module** (e.g. `src/platform/`), not native checks scattered across components.
- **Performance:** WebView start + JS parse at startup; batch bridge calls (every round trip costs); apply web principles (lazy loading, list virtualization) inside the WebView. *Recommended.*
