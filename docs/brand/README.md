# Agent Kit — brand kit

Soft sky, glossy app icons, pixel lettering. Friendly, calm, a little retro; never corporate.

## Files
| Path | Use |
|---|---|
| `../assets/banner.png` · `../assets/social-preview.png` | README banner · GitHub → Settings → Social preview (1280×640) |
| `src/` | Generator and the OFL fonts it uses |

Campaign material for social networks is kept outside this repository.

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
Clouds are generated from a seed; no stock photos or third-party artwork.
