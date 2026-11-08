# Web

- **Headers and policies as defense in depth:** restrictive CSP (start in Report-Only with a report endpoint, enforce after observing real traffic), HSTS, cookies `Secure`/`HttpOnly`/`SameSite`, clickjacking protection, CORS by allowlist. *Essential* (ASVS 5.0 V3).
- **Third-party scripts are runtime supply chain:** inventory, Subresource Integrity where possible, minimum third parties on login/checkout pages. *Recommended* (A03/A08).
- **Client storage is readable by any XSS:** no long-lived secrets in `localStorage`; prefer HttpOnly cookies or short-lived, server-validated grants.
- **Performance:** Core Web Vitals at p75 (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1), mobile and desktop separately. *Essential.*
