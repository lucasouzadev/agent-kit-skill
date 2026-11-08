# Desktop on a web runtime (renderer + privileged process)

- **Renderer isolation is non-negotiable:** no direct OS/Node access from the renderer, context isolation between page and preload, sandbox on **every** window. Electron defaults: `nodeIntegration: false` (v5+), `contextIsolation: true` (v12+), sandbox (v20+). Do not turn them off. *Essential.*
- **IPC is a privileged API:** narrow, specific handlers; validate the **sender** and the payload on every message; never a generic "run command X". *Essential.*
- **Controlled navigation and external opening:** block navigation and new windows to unexpected origins; validate URLs before handing them to the OS; permission handler that denies by default (camera, notifications). *Essential.*
- **The embedded runtime is a critical dependency:** you ship a whole browser; a late runtime update ships known vulnerabilities. Track days between upstream patch and your release. *Essential.*
- **Auto-update and code signing:** signed (and notarized where required) binaries, HTTPS updates with verified signature and anti-rollback. *Essential.*
- **Performance:** memory per process/window, defer main-process work at startup, no synchronous I/O on the main process. *Recommended.*
