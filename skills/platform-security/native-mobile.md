# Native mobile

- **Storage and keys in the OS vault** (Keychain/Keystore). Nothing sensitive in preferences, unencrypted SQLite, logs or backups. *Essential* (MASVS-STORAGE/CRYPTO).
- **Exported components and IPC are public entry points.** Intents, URL schemes and extensions receive data from any app: validate it; use explicit intents for internal IPC. *Essential* (MASTG best practices).
- **Deep links:** prefer domain-verified links (Universal Links/App Links) over custom schemes any app can register. Never carry sensitive data or tokens in a link; treat parameters as hostile; never run a privileged action without confirmation. *Essential* (Mobile Top 10 lists unprotected deep-link endpoints as emerging risk).
- **Resilience** (obfuscation, anti-debug, root/jailbreak detection, attestation) according to the risk profile; never instead of server controls. *Advanced* (MASVS-RESILIENCE).
- **OS permissions** asked at the moment of use, with a clear reason; degrade gracefully on denial.
- **Performance:** cold start < 5 s as a floor, UI thread free (ANR/hang), crash rate < 1.09 %, memory and battery. *Essential.*
