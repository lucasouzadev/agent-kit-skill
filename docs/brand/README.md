# Agent Kit — brand kit

Soft sky, glossy app icons, pixel lettering. Friendly, calm, a little retro; never corporate.

## Files
| Path | Use |
|---|---|
| `../assets/banner.png` · `../assets/social-preview.png` | README banner · GitHub → Settings → Social preview (1280×640) |
| `social/pt-br/` · `social/en/` | One package per language, one folder per network (Instagram feed carousel 1080×1350, Stories 1080×1920, profile photo; Threads 1080×1350; LinkedIn PDF carousel, 1200×1200 posts, 1584×396 cover, 1200×627 link image). Captions per network in `LEGENDAS.md` / `CAPTIONS.md` |
| `COPY.md` | Repository description, topics and the `gh repo edit` command |

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
