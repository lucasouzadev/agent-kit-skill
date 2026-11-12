# Agent Kit — brand kit

Soft sky, glossy app icons, pixel lettering. Friendly, calm, a little retro; never corporate.

## Files
| Path | Size | Use |
|---|---|---|
| `../assets/banner.png` | 1280×640 | README banner |
| `../assets/social-preview.png` | 1280×640 | GitHub → Settings → Social preview |
| `social/<en\|pt>/square/*.jpg` | 1080×1080 | Instagram / LinkedIn feed, carousel (01–06) |
| `social/<en\|pt>/portrait/*.jpg` | 1080×1350 | Instagram portrait feed |
| `social/<en\|pt>/header-1500x500.jpg` | 1500×500 | X / LinkedIn profile header |
| `social/<en\|pt>/link-1200x630.jpg` | 1200×630 | Link card, LinkedIn post image |
| `COPY.md` | — | Repository description and topics, bios, launch posts, threads, captions (PT/EN) |

## System
- **Sky:** `#3F9CFF` → `#58ADFF` → `#86C4FF` (top to bottom), procedural clouds, white haze at the edges.
- **Accents:** glossy red `#FF2D2D`, pink sticker `#FF4F86` → `#FF8DB1`, success green `#21C25A`, icon blue `#2F7FE8` → `#7CC0FF`.
- **Type:** VT323 (headlines, uppercase, letter-spacing 0.06em) · Space Mono (body). Both SIL OFL 1.1, in `src/fonts/`.
- **Icon:** white glossy rounded tile (24 % radius), tilted −7°, soft blue shadow; hero icon wears the red glossy ball.
- **Sticker:** `agent·kit` pink pill with white border, bottom right, rotated −8°.

## Regenerate
```bash
node docs/brand/src/render.js     # needs Playwright + Chromium
```
Edit texts in `COPY` inside `src/render.js`; clouds change with each job's `seed`. No stock photos or third-party artwork: clouds are generated and every icon is drawn in SVG.
