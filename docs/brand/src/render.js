// Agent Kit brand renderer: sky + procedural clouds + glossy app icon + pixel lettering.
// Usage (repo root): node docs/brand/src/render.js        -> writes docs/brand/** and docs/assets/banner.png
// Needs Playwright with Chromium. Fonts are local (OFL), clouds are generated (feTurbulence) per seed.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../../..');
const FONTS = path.join(__dirname, 'fonts');
const font = (f) => 'data:font/ttf;base64,' + fs.readFileSync(path.join(FONTS, f)).toString('base64');
const FONT_CSS = `
@font-face{font-family:Pix;src:url(${font('VT323-Regular.ttf')})}
@font-face{font-family:Mono;src:url(${font('SpaceMono-Regular.ttf')})}
@font-face{font-family:MonoB;src:url(${font('SpaceMono-Bold.ttf')})}`;

// ---------- icons (each a 100x100 glyph drawn inside the glossy tile) ----------
const ICONS = {
  chat: `
    <path d="M18 28a12 12 0 0 1 12-12h40a12 12 0 0 1 12 12v26a12 12 0 0 1-12 12H44L28 80V66h0a12 12 0 0 1-10-12z" fill="url(#gBlue)"/>
    <text x="50" y="50" text-anchor="middle" font-family="MonoB" font-size="22" fill="#fff">&gt;_</text>`,
  noslash: `
    <rect x="18" y="20" width="64" height="56" rx="10" fill="#1d2b44"/>
    <text x="50" y="62" text-anchor="middle" font-family="MonoB" font-size="40" fill="#cfe3ff">/</text>
    <circle cx="50" cy="48" r="26" fill="none" stroke="url(#gRed)" stroke-width="7"/>
    <path d="M32 66 68 30" stroke="url(#gRed)" stroke-width="7" stroke-linecap="round"/>`,
  heal: `
    <g transform="translate(50 50) scale(1.25) rotate(-35) translate(-50 -50)">
      <rect x="14" y="36" width="72" height="28" rx="14" fill="url(#gSkin)"/>
      <rect x="38" y="36" width="24" height="28" fill="#f1d3b3"/>
      <g fill="#c9a07a"><circle cx="44" cy="44" r="1.8"/><circle cx="50" cy="44" r="1.8"/><circle cx="56" cy="44" r="1.8"/>
      <circle cx="44" cy="50" r="1.8"/><circle cx="50" cy="50" r="1.8"/><circle cx="56" cy="50" r="1.8"/>
      <circle cx="44" cy="56" r="1.8"/><circle cx="50" cy="56" r="1.8"/><circle cx="56" cy="56" r="1.8"/></g>
    </g>`,
  ci: `
    <g fill="url(#gBlue)"><circle cx="34" cy="54" r="14"/><circle cx="52" cy="42" r="19"/><circle cx="68" cy="54" r="13"/><rect x="34" y="50" width="34" height="18"/></g>
    <circle cx="68" cy="68" r="15" fill="url(#gGreen)" stroke="#fff" stroke-width="3"/>
    <path d="M61 68l5 5 9-10" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
  track: `
    <path d="M20 70 C 30 30, 45 30, 50 50 S 70 70, 80 30" stroke="#b9cbe6" stroke-width="4" fill="none" stroke-dasharray="2 6" stroke-linecap="round"/>
    <circle cx="20" cy="70" r="7" fill="url(#gBlue)"/><circle cx="50" cy="50" r="7" fill="url(#gBlue)"/><circle cx="80" cy="30" r="9" fill="url(#gRed)"/>`,
  kit: `
    <rect x="16" y="34" width="68" height="44" rx="8" fill="url(#gBlue)"/>
    <path d="M38 34v-6a6 6 0 0 1 6-6h12a6 6 0 0 1 6 6v6" stroke="#2a6fd6" stroke-width="6" fill="none"/>
    <rect x="16" y="50" width="68" height="6" fill="#2a6fd6" opacity=".55"/>
    <rect x="44" y="46" width="12" height="14" rx="3" fill="#fff"/>`,
};

const DEFS = `<defs>
  <linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc0ff"/><stop offset="1" stop-color="#2f7fe8"/></linearGradient>
  <radialGradient id="gRed" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ff8a8a"/><stop offset=".45" stop-color="#ff2d2d"/><stop offset="1" stop-color="#b30f12"/></radialGradient>
  <radialGradient id="gGreen" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#8ff0a4"/><stop offset=".5" stop-color="#21c25a"/><stop offset="1" stop-color="#0f8a3a"/></radialGradient>
  <linearGradient id="gSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2c4"/><stop offset="1" stop-color="#e5b48a"/></linearGradient>
  <linearGradient id="gCloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cfe2ff"/></linearGradient>
</defs>`;

// glossy tile, a little tilted, with a red glossy ball "badge" on the hero icon
const tile = (icon, size, badge) => `
<div class="tile" style="width:${size}px;height:${size}px">
  <svg viewBox="0 0 100 100" width="${size * 0.78}" height="${size * 0.78}">${DEFS}${ICONS[icon]}</svg>
  <div class="gloss"></div>
  ${badge ? `<div class="ball" style="width:${size * 0.34}px;height:${size * 0.34}px"></div>` : ''}
</div>`;

const clouds = (w, h, seed) => `
<svg class="clouds" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <filter id="c" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${(1.6 / Math.max(w, h)).toFixed(5)} ${(3.2 / Math.max(w, h)).toFixed(5)}" numOctaves="6" seed="${seed}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 3.4 -1.6"/>
    <feGaussianBlur stdDeviation="${Math.round(Math.max(w, h) / 260)}"/>
  </filter>
  <rect width="100%" height="100%" filter="url(#c)" opacity=".9"/>
</svg>`;

const sticker = (scale, up) => `<div class="sticker" style="transform:rotate(-8deg) scale(${scale})${up ? `;bottom:${up}px` : ''}">agent·kit</div>`;

function page({ w, h, seed, body, wide, noSticker, stickerUp }) {
  const u = wide ? Math.min(w / 1280, h / 640) : Math.min(w, h) / 1080; // unit scale
  return `<!doctype html><html><head><meta charset="utf-8"><style>${FONT_CSS}
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:${w}px;height:${h}px;overflow:hidden}
  body{position:relative;background:linear-gradient(180deg,#3f9cff 0%,#58adff 45%,#86c4ff 100%);font-family:Mono}
  .clouds{position:absolute;inset:0}
  .haze{position:absolute;inset:0;box-shadow:inset 0 0 ${150 * u}px ${70 * u}px rgba(255,255,255,.78);pointer-events:none}
  .stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
  .tile{position:relative;flex:none;border-radius:24%;display:flex;align-items:center;justify-content:center;
    background:linear-gradient(160deg,#ffffff 0%,#eef4fb 55%,#d9e4f1 100%);transform:rotate(-7deg);
    box-shadow:0 ${18 * u}px ${36 * u}px rgba(20,60,120,.35),0 ${3 * u}px ${6 * u}px rgba(20,60,120,.25),inset 0 -${4 * u}px ${8 * u}px rgba(120,150,190,.35)}
  .gloss{position:absolute;inset:0;border-radius:24%;background:linear-gradient(180deg,rgba(255,255,255,.85) 0%,rgba(255,255,255,0) 46%);mix-blend-mode:screen;pointer-events:none}
  .ball{position:absolute;right:-9%;top:-12%;border-radius:50%;
    background:radial-gradient(circle at 33% 28%,#ffd0d0 0%,#ff3b3b 30%,#d10f17 70%,#8a050b 100%);
    box-shadow:0 ${8 * u}px ${14 * u}px rgba(90,0,0,.35)}
  .pix{font-family:Pix;color:#fff;text-transform:uppercase;letter-spacing:.06em;line-height:.92;
    text-shadow:0 ${2 * u}px ${3 * u}px rgba(15,55,125,.35),0 0 ${18 * u}px rgba(20,80,170,.4)}
  .sub{font-family:Mono;color:#fff;text-shadow:0 1px ${2 * u}px rgba(15,55,125,.65),0 0 ${14 * u}px rgba(20,80,170,.55)}
  .sticker{position:absolute;right:${46 * u}px;bottom:${42 * u}px;font-family:MonoB;font-size:${30 * u}px;color:#fff;
    background:linear-gradient(180deg,#ff8db1,#ff4f86);padding:${6 * u}px ${18 * u}px;border-radius:${30 * u}px;
    border:${4 * u}px solid #fff;box-shadow:0 ${6 * u}px ${12 * u}px rgba(160,20,70,.3);transform-origin:right bottom}
  .chips{display:flex;flex-wrap:wrap;gap:${10 * u}px}
  .chip{font-family:Pix;color:#fff;font-size:${30 * u}px;letter-spacing:.06em;padding:${2 * u}px ${12 * u}px;border:${2 * u}px solid rgba(255,255,255,.75);border-radius:${8 * u}px;background:rgba(255,255,255,.12)}
  </style></head><body>${clouds(w, h, seed)}<div class="haze"></div>${body(u)}${noSticker ? '' : sticker(u, stickerUp)}</body></html>`;
}

// ---------- compositions ----------
const post = ({ icon, title, sub, badge }) => (u) => `
<div class="stage" style="gap:${64 * u}px;padding:0 ${90 * u}px">
  ${tile(icon, 190 * u, badge)}
  <div style="max-width:${640 * u}px">
    <div class="pix" style="font-size:${96 * u}px">${title}</div>
    ${sub ? `<div class="sub" style="font-size:${25 * u}px;margin-top:${26 * u}px;max-width:${560 * u}px;line-height:1.4">${sub}</div>` : ''}
  </div>
</div>`;

const story = ({ icon, title, sub, badge }) => (u) => `
<div class="stage" style="flex-direction:column;text-align:center;gap:${70 * u}px;padding:0 ${80 * u}px">
  ${tile(icon, 280 * u, badge)}
  <div class="pix" style="font-size:${118 * u}px">${title}</div>
  ${sub ? `<div class="sub" style="font-size:${40 * u}px;max-width:${860 * u}px;line-height:1.4">${sub}</div>` : ''}
</div>`;

const avatar = () => (u) => `<div class="stage">${tile('chat', 470 * u, true)}</div>`;

const hero = ({ tagline, sub, steps, right }) => (u) => `
<div class="stage" style="gap:${70 * u}px;padding:0 ${80 * u}px;${right ? 'justify-content:flex-end' : ''}">
  ${tile('chat', 230 * u, true)}
  <div>
    <div class="pix" style="font-size:${150 * u}px">AGENT KIT</div>
    <div class="pix" style="font-size:${62 * u}px;margin-top:${14 * u}px;opacity:.97">${tagline}</div>
    <div class="sub" style="font-size:${24 * u}px;margin-top:${22 * u}px;max-width:${760 * u}px;line-height:1.4">${sub}</div>
    ${steps ? `<div class="chips" style="margin-top:${26 * u}px;max-width:${820 * u}px">${steps.map((s) => `<span class="chip">${s}</span>`).join('')}</div>` : ''}
  </div>
</div>`;

const COPY = {
  en: {
    tagline: 'JUST TALK. IT CODES.',
    sub: 'Open-source skills that make AI coding agents follow the plan, fix their own small mistakes and watch your CI. No commands.',
    steps: ['BOOT', 'BRIEF', 'PLAN', 'YES', 'BUILD', 'SELF-HEAL', 'VERIFY', 'WATCH CI', 'CLOSE'],
    posts: [
      { id: '01-just-talk', icon: 'chat', badge: true, title: 'JUST TALK.<br>IT CODES.', sub: 'agent-kit · open-source skills for AI coding agents' },
      { id: '02-no-commands', icon: 'noslash', title: 'NO SLASH COMMANDS', sub: 'It greets you, asks one question and leads the rest.' },
      { id: '03-self-heal', icon: 'heal', title: 'FIXES ITS OWN MESS', sub: 'Crashed simulator? Stale cache? Broken test? Handled. No questions.' },
      { id: '04-ci-watch', icon: 'ci', title: 'KEEPS AN EYE ON YOUR CI', sub: 'A lighter model watches every run in the background.' },
      { id: '05-track', icon: 'track', title: '9 STEPS.<br>NONE SKIPPED.', sub: 'Hooks make the agent follow the plan, not just read it.' },
      { id: '06-get-it', icon: 'kit', badge: true, title: 'FREE & OPEN SOURCE', sub: 'github.com/lucasouzadev/<br><span style="white-space:nowrap">agent-kit-skill</span>' },
    ],
  },
  pt: {
    tagline: 'SÓ CONVERSA. ELE PROGRAMA.',
    sub: 'Skills open-source que fazem agentes de código seguirem o plano, consertarem os próprios erros e vigiarem seu CI. Sem comandos.',
    steps: ['INÍCIO', 'BRIEF', 'PLANO', 'SIM', 'BUILD', 'AUTOCORREÇÃO', 'VERIFICA', 'CI', 'FECHA'],
    posts: [
      { id: '01-so-conversa', icon: 'chat', badge: true, title: 'SÓ CONVERSA.<br>ELE PROGRAMA.', sub: 'agent-kit · skills open-source para agentes de código' },
      { id: '02-sem-comandos', icon: 'noslash', title: 'SEM COMANDOS COM /', sub: 'Ele cumprimenta, faz uma pergunta e conduz o resto.' },
      { id: '03-autocorrecao', icon: 'heal', title: 'CONSERTA A PRÓPRIA BAGUNÇA', sub: 'Simulador travou? Cache velho? Teste quebrado? Resolvido. Sem perguntas.' },
      { id: '04-ci', icon: 'ci', title: 'DE OLHO NO SEU CI', sub: 'Um modelo mais leve acompanha cada execução em segundo plano.' },
      { id: '05-trilha', icon: 'track', title: '9 ETAPAS.<br>NENHUMA PULADA.', sub: 'Hooks fazem o agente seguir o plano, não só ler.' },
      { id: '06-gratis', icon: 'kit', badge: true, title: 'GRÁTIS E OPEN SOURCE', sub: 'github.com/lucasouzadev/<br><span style="white-space:nowrap">agent-kit-skill</span>' },
    ],
  },
};

(async () => {
  const browser = await chromium.launch();
  const jobs = [];
  const out = (rel) => { const p = path.join(ROOT, rel); fs.mkdirSync(path.dirname(p), { recursive: true }); return p; };
  jobs.push({ file: 'docs/assets/banner.png', w: 1280, h: 640, seed: 7, wide: true, body: hero(COPY.en) });
  jobs.push({ file: 'docs/assets/social-preview.png', w: 1280, h: 640, seed: 7, wide: true, body: hero(COPY.en) });
  // One package per language, one folder per network, only the sizes each network uses.
  const PKG = { pt: { dir: 'pt-br', ig: 'instagram', feed: 'feed-carrossel-1080x1350', stories: 'stories-1080x1920', li: 'linkedin',
                      liPost: 'post-1200x1200', liCover: 'capa-perfil-1584x396.jpg', liLink: 'imagem-link-1200x627.jpg', th: 'threads', thPost: 'post-carrossel-1080x1350', pdf: 'carrossel-documento-1080x1350.pdf', avatar: 'foto-perfil-1080x1080.jpg' },
                en: { dir: 'en', ig: 'instagram', feed: 'feed-carousel-1080x1350', stories: 'stories-1080x1920', li: 'linkedin',
                      liPost: 'post-1200x1200', liCover: 'profile-cover-1584x396.jpg', liLink: 'link-image-1200x627.jpg', th: 'threads', thPost: 'post-carousel-1080x1350', pdf: 'carousel-document-1080x1350.pdf', avatar: 'profile-photo-1080x1080.jpg' } };
  const pdfs = [];
  for (const lang of ['pt', 'en']) {
    const c = COPY[lang], k = PKG[lang], base = `docs/brand/social/${k.dir}`;
    const feed = [];
    c.posts.forEach((p, i) => {
      const n = `${p.id}.jpg`;
      feed.push(`${base}/${k.ig}/${k.feed}/${n}`);
      jobs.push({ file: `${base}/${k.ig}/${k.feed}/${n}`, w: 1080, h: 1350, seed: 31 + i, body: post(p) });
      jobs.push({ file: `${base}/${k.ig}/${k.stories}/${n}`, w: 1080, h: 1920, seed: 71 + i, stickerUp: 300, body: story(p) });
      jobs.push({ file: `${base}/${k.th}/${k.thPost}/${n}`, w: 1080, h: 1350, seed: 31 + i, body: post(p) });
      jobs.push({ file: `${base}/${k.li}/${k.liPost}/${n}`, w: 1200, h: 1200, seed: 11 + i, body: post(p) });
    });
    jobs.push({ file: `${base}/${k.ig}/${k.avatar}`, w: 1080, h: 1080, seed: 91, noSticker: true, body: avatar() });
    jobs.push({ file: `${base}/${k.li}/${k.liCover}`, w: 1584, h: 396, seed: 51, wide: true, body: hero({ ...c, steps: null, right: true }) });
    jobs.push({ file: `${base}/${k.li}/${k.liLink}`, w: 1200, h: 627, seed: 61, wide: true, body: hero(c) });
    pdfs.push({ out: `${base}/${k.li}/${k.pdf}`, pages: feed });
  }
  for (const j of jobs) {
    const pg = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await pg.setContent(page(j), { waitUntil: 'load' });
    await pg.evaluate(() => document.fonts.ready);
    await pg.screenshot(j.file.endsWith('.jpg') ? { path: out(j.file), type: 'jpeg', quality: 90 } : { path: out(j.file) });
    await pg.close();
    console.log('wrote', j.file);
  }
  await browser.close();
  // LinkedIn carousels are uploaded as a PDF document: one page per feed image.
  const { execFileSync } = require('child_process');
  for (const d of pdfs) {
    execFileSync('python3', ['-c', 'import sys\nfrom PIL import Image\nims=[Image.open(p).convert("RGB") for p in sys.argv[2:]]\nims[0].save(sys.argv[1],save_all=True,append_images=ims[1:],resolution=144)',
      out(d.out), ...d.pages.map((p) => path.join(ROOT, p))]);
    console.log('wrote', d.out);
  }
})();
