import base64

def get_style_css() -> str:
    try:
        with open("data/images/Sony-Music-cursor-32.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            cursor32_url = f"data:image/png;base64,{b64}"
    except Exception:
        cursor32_url = ""

    css = r"""/* ══════════════════════════════════════════════════════════════════════
   Sony Music Latin Pulse — plain CSS (converted from Tailwind + React)
   ══════════════════════════════════════════════════════════════════════ */

:root {
  /* Palette — dark (default) */
  --color-bg-primary:    #0A0A0A;
  --color-bg-secondary:  #141414;
  --color-bg-card:       #1A1A1A;
  --color-bg-card-hover: #222222;
  --color-text-primary:  #FFFFFF;
  --color-text-secondary:#999999;
  --color-text-muted:    #666666;
  --color-border:        #2A2A2A;
  --color-border-light:  #333333;
  --color-accent-up:     #FFFFFF;
  --color-accent-down:   #666666;
  --color-accent-highlight: #E0E0E0;

  --font-headline: "Playfair Display", Georgia, serif;
  --font-mono:     "IBM Plex Mono", "SF Mono", monospace;
  --font-ui:       "DM Sans", "Helvetica Neue", sans-serif;
}

[data-theme="light"] {
  --color-bg-primary:    #F5F3EF;
  --color-bg-secondary:  #EBE8E2;
  --color-bg-card:       #FFFFFF;
  --color-bg-card-hover: #F0EDE7;
  --color-text-primary:  #1A1A1A;
  --color-text-secondary:#555555;
  --color-text-muted:    #888888;
  --color-border:        #D8D4CC;
  --color-border-light:  #C8C4BC;
  --color-accent-up:     #1A1A1A;
  --color-accent-down:   #888888;
  --color-accent-highlight: #333333;
}

/* ── Animations ─────────────────────────────────────────── */
@keyframes ticker    { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@keyframes fadeUp     { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn     { from { opacity: 0; } to { opacity: 1; } }
@keyframes blink      { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
@keyframes ping       { 75%, 100% { transform: scale(2); opacity: 0; } }
@keyframes pulse      { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }

.anim-fade-up { animation: fadeUp .5s cubic-bezier(.16,1,.3,1) both; }
.anim-fade-in { animation: fadeIn .4s ease both; }
.anim-ping    { animation: ping 1.4s cubic-bezier(0,0,.2,1) infinite; }
.anim-pulse   { animation: pulse 1.4s ease-in-out infinite; }

/* ── Base ───────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html {
  scroll-behavior: smooth;
  -ms-overflow-style: none;
  scrollbar-width: none;
  background-color: var(--color-bg-primary);
  transition: background-color .4s ease;
}
html::-webkit-scrollbar, body::-webkit-scrollbar, *::-webkit-scrollbar { display: none; }
html, body { min-height: 100%; margin: 0; }

body {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-family: var(--font-ui);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background-color .4s ease, color .4s ease;
  cursor: url('CURSOR32_URL_PLACEHOLDER') 16 16, auto;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(255,255,255,.018) 3px, rgba(255,255,255,.018) 4px);
  pointer-events: none;
  z-index: 9998;
}
[data-theme="light"] body::before {
  background-image: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,.012) 3px, rgba(0,0,0,.012) 4px);
}

a { color: inherit; }
button { font: inherit; }
img { max-width: 100%; display: block; }

.min-h-screen { min-height: 100vh; }
.container-px { padding-left: 1.5rem; padding-right: 1.5rem; }

/* ── Theme toggle ───────────────────────────────────────── */
.theme-toggle {
  position: relative; width: 56px; height: 28px; border-radius: 14px;
  background: var(--color-bg-card); border: 1.5px solid var(--color-border-light);
  cursor: pointer; transition: background .3s ease, border-color .3s ease; flex-shrink: 0;
}
.theme-toggle:hover { border-color: var(--color-text-muted); }
.theme-toggle-knob {
  position: absolute; top: 2px; left: 2px; width: 22px; height: 22px; border-radius: 50%;
  background: var(--color-text-primary); display: flex; align-items: center; justify-content: center;
  transition: transform .35s cubic-bezier(.4,0,.2,1), background .3s ease;
}
[data-theme="light"] .theme-toggle-knob { transform: translateX(28px); }
.theme-toggle-icon { width: 13px; height: 13px; color: var(--color-bg-primary); }

/* ── Masthead ───────────────────────────────────────────── */
.masthead { padding: 1.25rem 1.5rem 0; }
.masthead-logo-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.masthead-rule { border-top: 2px solid var(--color-text-primary); margin-bottom: 0.75rem; }
.masthead-eyebrow-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; }
.eyebrow { font-family: var(--font-mono); font-size: 11px; letter-spacing: .35em; text-transform: uppercase; color: var(--color-text-primary); }
.eyebrow-tight { letter-spacing: .2em; }
.masthead h1 {
  font-family: var(--font-headline); font-weight: 900; line-height: 1; letter-spacing: -0.02em;
  color: var(--color-text-primary); font-size: clamp(1.75rem, 4vw, 3.5rem); margin: 0;
}
.cursor-blink { margin-left: 2px; color: transparent; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; display: inline-block; width: 14px; height: 14px; animation: blink 1.1s step-end infinite; }

/* ── News ticker ────────────────────────────────────────── */
.ticker-wrap { margin-top: 1.5rem; overflow: hidden; position: relative; }
.ticker-glow-top, .ticker-glow-bottom { position: absolute; left: 0; right: 0; height: 1px; }
.ticker-glow-top { top: 0; background: linear-gradient(90deg, transparent, rgba(251,191,36,.5) 20%, rgba(244,114,182,.5) 50%, rgba(96,165,250,.5) 80%, transparent); }
.ticker-glow-bottom { bottom: 0; background: linear-gradient(90deg, transparent, rgba(96,165,250,.5) 20%, rgba(74,222,128,.5) 50%, rgba(251,191,36,.5) 80%, transparent); }
.ticker-inner { background: var(--color-bg-secondary); padding: 1.25rem 0; display: flex; align-items: center; }
.ticker-live { flex-shrink: 0; display: flex; align-items: center; gap: .5rem; padding: 0 1rem 0 1.5rem; z-index: 10; background: var(--color-bg-secondary); }
.ticker-dot { position: relative; width: 16px; height: 16px; }
.ticker-dot-ping { position: absolute; inset: 0; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; opacity: .4; animation: ping 1.4s cubic-bezier(0,0,.2,1) infinite; }
.ticker-dot-solid { position: relative; width: 16px; height: 16px; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; }
.ticker-live-label { font-family: var(--font-mono); font-size: 13px; letter-spacing: .3em; text-transform: uppercase; font-weight: 700; color: #f87171; }
.ticker-sep { color: var(--color-border-light); opacity: .4; }
.ticker-viewport { overflow: hidden; flex: 1; }
.ticker-track { display: flex; gap: 0; white-space: nowrap; align-items: center; animation: ticker 160s linear infinite; width: max-content; }
.ticker-item { display: inline-flex; align-items: center; gap: .875rem; padding: 0 1.5rem; }
.ticker-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 2px solid; }
.ticker-badge { font-family: var(--font-mono); font-size: 11px; letter-spacing: .15em; text-transform: uppercase; font-weight: 700; padding: 4px 8px; border-radius: 2px; flex-shrink: 0; }
.ticker-artist { font-family: var(--font-mono); font-size: 15px; letter-spacing: .05em; text-transform: uppercase; font-weight: 700; flex-shrink: 0; }
.ticker-headline { color: var(--color-text-primary); font-family: var(--font-ui); font-size: 16px; font-weight: 500; }
.ticker-diamond { font-family: var(--font-mono); font-size: 14px; opacity: .2; margin-left: .75rem; flex-shrink: 0; }

/* ── Tabs ───────────────────────────────────────────────── */
.tabnav { margin: 2rem 1.5rem 0; }
.tabnav-row { display: flex; flex-wrap: wrap; gap: .5rem; }
.tab-btn {
  position: relative; display: flex; align-items: center; gap: .5rem; padding: .75rem 1.25rem;
  font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; text-transform: uppercase; font-weight: 700;
  border-radius: 2px; border: 2px solid; transition: all .2s ease; cursor: pointer; background: transparent;
}
.tab-count { font-family: var(--font-mono); font-size: 11px; padding: 2px 6px; border-radius: 2px; font-weight: 700; }
.tabnav-rule { border-top: 1px solid var(--color-border); margin-top: .75rem; }

/* ── Section label ──────────────────────────────────────── */
.section-label-row { display: flex; align-items: baseline; gap: .75rem; margin-bottom: 1.5rem; }
.section-label { font-family: var(--font-headline); font-weight: 900; font-size: 1.5rem; color: var(--color-text-primary); letter-spacing: -0.01em; margin: 0; }
.section-meta { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: .15em; }
.divider { border-top: 1px solid var(--color-border); margin: 3rem 0; }

.tab-content { margin: 0 1.5rem; }

/* ── Overview page ──────────────────────────────────────── */
.ov-space > * + * { margin-top: 2.5rem; }
.ov-hero { border: 1px solid var(--color-border); border-radius: 2px; padding: 2rem; background: var(--color-bg-secondary); }
.ov-hero h2 { font-family: var(--font-headline); font-weight: 900; color: var(--color-text-primary); line-height: 1.15; letter-spacing: -0.01em; margin: 0 0 1rem; font-size: clamp(1.5rem, 3vw, 2.5rem); }
.ov-hero p.lede { font-size: 15px; color: var(--color-text-secondary); line-height: 1.7; max-width: 48rem; margin: 0; }
.ov-stat-row { display: flex; flex-wrap: wrap; gap: 2rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--color-border); }
.ov-stat-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: .15em; text-transform: uppercase; color: var(--color-text-muted); margin: 0; }
.ov-stat-value { font-family: var(--font-mono); font-size: 18px; color: var(--color-text-primary); margin: 2px 0 0; }

.grid-2 { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 768px) { .grid-2 { grid-template-columns: 1fr 1fr; } }

.ov-card { background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 2px; padding: 1.5rem; }
.ov-card-head { display: flex; align-items: center; gap: .75rem; margin-bottom: 1rem; }
.ov-card-icon { font-family: var(--font-headline); font-size: 1.5rem; color: var(--color-text-primary); }
.ov-card-title { font-family: var(--font-headline); font-weight: 900; font-size: 17px; color: var(--color-text-primary); letter-spacing: -0.01em; margin: 0; }
.ov-card-body { font-family: var(--font-ui); font-size: 14px; color: var(--color-text-secondary); line-height: 1.7; }
.ov-card-body p { margin: 0 0 .5rem; }
.ov-card-body p:last-child { margin-bottom: 0; }
.ov-card-body strong { color: var(--color-text-primary); }

.kpi-ref-card, .badge-ref-card { background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 2px; padding: 1.5rem; margin-top: 1rem; }
.ref-eyebrow { font-family: var(--font-mono); font-size: 11px; letter-spacing: .3em; text-transform: uppercase; color: var(--color-text-muted); margin: 0 0 .5rem; }
.ref-title { font-family: var(--font-headline); font-weight: 900; font-size: 17px; color: var(--color-text-primary); margin: 0 0 1rem; }

.kpi-ref-grid { display: grid; grid-template-columns: 1fr; gap: .5rem; margin-top: .5rem; }
@media (min-width: 640px) { .kpi-ref-grid { grid-template-columns: 1fr 1fr; } }
.kpi-ref-item { display: flex; gap: .75rem; align-items: flex-start; }
.kpi-ref-id { flex-shrink: 0; font-family: var(--font-mono); font-size: 11px; color: var(--color-text-muted); margin-top: 2px; }
.kpi-ref-name { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-primary); letter-spacing: .03em; margin: 0; }
.kpi-ref-desc { font-size: 13px; color: var(--color-text-muted); line-height: 1.4; margin: 2px 0 0; }

.badge-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; }
@media (min-width: 640px) { .badge-grid { grid-template-columns: 1fr 1fr; } }
.badge-col-title { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: .15em; margin: 0 0 .75rem; }
.badge-row { display: flex; align-items: flex-start; gap: .75rem; margin-bottom: .5rem; }
.badge-row-dot { font-size: 16px; line-height: 1; margin-top: 2px; flex-shrink: 0; }
.badge-row-dots { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-secondary); flex-shrink: 0; margin-top: 2px; }
.badge-row-label { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-primary); }
.badge-row-desc { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); margin-left: .5rem; }

/* ── News feed / story cards ────────────────────────────── */
.story-list { display: flex; flex-direction: column; gap: .5rem; }
.story-card {
  position: relative; display: flex; gap: 1rem; align-items: flex-start; overflow: hidden;
  background: var(--color-bg-card); border: 1px solid var(--color-border); border-left: 2px solid transparent;
  border-radius: 2px; padding: 1rem; transition: all .3s ease; cursor: pointer;
}
.story-card:hover { background: var(--color-bg-card-hover); border-color: var(--color-border-light); border-left-color: var(--color-text-muted); }
.story-card.top3:hover { border-left-color: var(--color-text-primary); }
.story-priority { flex-shrink: 0; width: 2rem; text-align: right; }
.story-priority span { font-family: var(--font-headline); font-weight: 900; line-height: 1; }
.story-priority.top3 span { font-size: 24px; color: var(--color-text-primary); }
.story-priority:not(.top3) span { font-size: 20px; color: var(--color-text-muted); }
.story-thumb { flex-shrink: 0; width: 144px; height: 144px; border-radius: 50%; object-fit: cover; border: 2px solid var(--color-border-light); filter: grayscale(100%); transition: filter .5s ease, box-shadow .5s ease, border-color .5s ease; }
.story-card:hover .story-thumb { filter: grayscale(0%); border-color: rgba(255,255,255,.2); }
.story-body { flex: 1; min-width: 0; }
.story-top-row { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-bottom: .375rem; }
.signal-badge { font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; text-transform: uppercase; padding: 2px 8px; border-radius: 2px; font-weight: 700; }
.story-artist-line { font-family: var(--font-mono); font-size: 14px; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: .1em; }
.story-headline { font-family: var(--font-headline); font-weight: 900; line-height: 1.25; color: var(--color-text-primary); margin: 0; }
.story-headline.top3 { font-size: 19px; } .story-headline:not(.top3) { font-size: 17px; }
.kpi-impact-row { margin-top: .5rem; display: flex; flex-wrap: wrap; gap: .75rem .75rem; }
.kpi-impact { display: inline-flex; align-items: center; gap: 4px; font-family: var(--font-mono); font-size: 14px; }
.story-summary { margin-top: .5rem; font-size: 15px; color: var(--color-text-secondary); line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.story-footer { margin-top: .5rem; display: flex; flex-wrap: wrap; align-items: center; gap: .375rem .5rem; }
.story-footer-item { font-family: var(--font-mono); font-size: 13px; color: var(--color-text-muted); }
.story-footer-item.source { font-size: 12px; max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.story-footer-sep { color: var(--color-border-light); opacity: .4; font-size: 13px; }
.conf-dots { font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; }
.conf-filled { color: var(--color-text-secondary); }
.conf-empty { color: var(--color-border-light); opacity: .5; }

.story-modal-overlay {
  position: fixed; inset: 0; z-index: 10000; display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; background: rgba(10, 10, 10, 0.85); overflow: auto;
}
.story-modal-panel {
  position: relative; width: min(100%, 720px); background: var(--color-bg-secondary); border: 1px solid var(--color-border); border-radius: 8px; padding: 1.5rem;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.75);
}
.story-modal-close {
  position: absolute; top: 1rem; right: 1rem; width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--color-border-light);
  background: var(--color-bg-card); color: var(--color-text-primary); font-size: 18px; cursor: pointer;
}
.story-modal-header { display: flex; gap: 1rem; align-items: flex-start; }
.story-modal-thumb { width: 120px; height: 120px; border-radius: 16px; object-fit: cover; border: 1px solid var(--color-border); }
.story-modal-title-wrap { flex: 1; }
.story-modal-badge { display: inline-flex; align-items: center; font-family: var(--font-mono); font-size: 11px; letter-spacing: .15em; text-transform: uppercase; font-weight: 700; padding: 4px 8px; border-radius: 2px; margin-bottom: .75rem; }
.story-modal-title { font-family: var(--font-headline); font-weight: 900; font-size: 1.35rem; color: var(--color-text-primary); margin: 0 0 .5rem; line-height: 1.1; }
.story-modal-subtitle { font-family: var(--font-mono); font-size: 13px; letter-spacing: .12em; text-transform: uppercase; color: var(--color-text-muted); }
.story-modal-meta { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1rem; font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); }
.story-modal-body { margin-top: 1.5rem; color: var(--color-text-secondary); line-height: 1.8; }
.story-modal-details { margin-top: 1rem; display: grid; gap: .75rem; }
.story-modal-detail-row { display: flex; justify-content: space-between; gap: .75rem; font-size: 13px; }
.story-modal-label { font-family: var(--font-mono); color: var(--color-text-muted); text-transform: uppercase; letter-spacing: .12em; }
.story-modal-impact { margin-top: 1.5rem; }
.story-modal-impact h3 { margin: 0 0 .75rem; font-family: var(--font-headline); font-size: 1rem; color: var(--color-text-primary); }
.story-modal-impact-item { display: flex; justify-content: space-between; gap: .75rem; padding: .75rem 1rem; background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 4px; }
.story-modal-impact-name { font-family: var(--font-mono); font-size: 13px; color: var(--color-text-primary); }
.story-modal-impact-delta { font-family: var(--font-mono); font-size: 13px; color: var(--color-text-secondary); }
.story-modal-empty { margin: 0; color: var(--color-text-muted); }

/* ── Roster ─────────────────────────────────────────────── */
.roster-toolbar { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
@media (min-width: 1024px) { .roster-toolbar { flex-direction: row; align-items: flex-start; justify-content: space-between; } }
.roster-title { font-family: var(--font-headline); font-weight: 900; font-size: 1.5rem; color: var(--color-text-primary); letter-spacing: -0.01em; margin: 0; }
.roster-subtitle { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: .15em; margin: 2px 0 0; }
.roster-controls { display: flex; flex-direction: column; gap: .75rem; flex-shrink: 0; }
@media (min-width: 640px) { .roster-controls { flex-direction: row; align-items: center; } }
.search-wrap { position: relative; display: flex; align-items: center; }
.search-icon { position: absolute; left: 12px; font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); pointer-events: none; }
.search-input {
  font-family: var(--font-mono); font-size: 12px; letter-spacing: .03em; background: transparent; color: var(--color-text-primary);
  border: 1px solid var(--color-border-light); border-radius: 2px; padding: 6px 32px; width: 240px; transition: border-color .15s ease;
}
.search-input::placeholder { color: var(--color-text-muted); }
.search-input:focus { outline: none; border-color: var(--color-text-secondary); }
.search-clear { position: absolute; right: 8px; font-family: var(--font-mono); font-size: 14px; color: var(--color-text-muted); cursor: pointer; background: none; border: none; line-height: 1; }
.search-clear:hover { color: var(--color-text-primary); }
.tier-filter-row { display: flex; flex-wrap: wrap; gap: .375rem; padding-top: 2px; }
.tier-btn { font-family: var(--font-mono); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; padding: 6px 12px; border-radius: 2px; border: 1px solid; transition: all .15s ease; cursor: pointer; background: transparent; }
.tier-btn .count { margin-left: 4px; opacity: .6; }

.roster-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1rem; }
@media (min-width: 640px)  { .roster-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 768px)  { .roster-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .roster-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
@media (min-width: 1280px) { .roster-grid { grid-template-columns: repeat(5, minmax(0, 1fr)); } }
.empty-msg { font-family: var(--font-mono); font-size: 13px; color: var(--color-text-muted); padding: 3rem 0; text-align: center; }

/* Artist card */
.artist-card {
  position: relative; display: flex; flex-direction: column; overflow: hidden;
  background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 2px;
  cursor: pointer; user-select: none; transition: all .3s ease; min-width: 0;
}
.artist-card:hover { background: var(--color-bg-card-hover); border-color: var(--color-border-light); transform: scale(1.02); box-shadow: 0 16px 48px rgba(0,0,0,.8); }
.artist-card-sweep { position: absolute; inset-inline: 0; top: 0; height: 2px; transform: scaleX(0); transform-origin: left; transition: transform .3s ease; }
.artist-card:hover .artist-card-sweep { transform: scaleX(1); }
.ac-avatar-wrap { display: flex; justify-content: center; padding: 1.5rem 0 1rem; position: relative; }
.ac-avatar-inner { position: relative; }
.ac-avatar { width: 192px; height: 192px; border-radius: 50%; object-fit: cover; border: 2px solid; filter: grayscale(100%); transition: filter .5s ease, box-shadow .5s ease; }
.artist-card:hover .ac-avatar { filter: grayscale(0%); box-shadow: 0 0 32px rgba(255,255,255,.1); }
.ac-tier-dot { position: absolute; top: -2px; right: -2px; width: 14px; height: 14px; border-radius: 50%; border: 2px solid var(--color-bg-card); }
.ac-identity { padding: 0 1rem .75rem; text-align: center; }
.ac-name { font-family: var(--font-headline); font-weight: 900; font-size: 17px; line-height: 1.2; color: var(--color-text-primary); letter-spacing: -0.01em; margin: 0; }
.ac-tier-line { margin-top: 4px; font-family: var(--font-mono); font-size: 13px; letter-spacing: .15em; text-transform: uppercase; }
.ac-tier-line .tier-label { font-weight: 700; }
.ac-tier-line .sep { margin: 0 6px; opacity: .3; color: var(--color-text-muted); }
.ac-tier-line .reach-val { color: var(--color-text-muted); }
.ac-narrative { margin: 10px 4px 0; font-size: 13px; line-height: 1.4; font-family: var(--font-ui); font-style: italic; color: var(--color-text-primary); }
.ac-divider { margin: 0 1rem; border-top: 1px solid var(--color-border); }
.ac-kpis { padding: .75rem 1rem; display: flex; flex-direction: column; gap: .625rem; }
.ac-kpi-row { display: flex; align-items: baseline; justify-content: space-between; gap: .5rem; }
.ac-kpi-label { font-family: var(--font-mono); font-size: 13px; text-transform: uppercase; letter-spacing: .1em; flex-shrink: 0; }
.ac-kpi-value { font-family: var(--font-mono); font-size: 16px; color: var(--color-text-primary); text-align: right; }
.ac-kpi-value .delta { margin-left: 6px; font-size: 14px; }
.ac-alerts { padding: 10px 1rem; display: flex; flex-wrap: wrap; gap: 6px; }
.alert-badge { display: inline-flex; align-items: center; padding: 2px 6px; border-radius: 2px; font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; text-transform: uppercase; border: 1px solid; }
.ac-expand-hint { margin-top: auto; padding: 4px 1rem 12px; display: flex; justify-content: center; }
.ac-expand-hint span { font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; text-transform: uppercase; opacity: 0; transition: opacity .2s ease; }
.artist-card:hover .ac-expand-hint span { opacity: 1; }

.ac-expanded { margin: 4px 1rem 1rem; min-width: 0; }
.ac-expanded-inner { border-top: 1px solid var(--color-border); padding-top: .75rem; }
.ac-expanded-label { font-family: var(--font-mono); font-size: 13px; letter-spacing: .15em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 .75rem; }
.kpi-row { display: grid; grid-template-columns: 1fr auto auto; align-items: center; gap: 0 .75rem; padding: 10px 0; border-bottom: 1px solid var(--color-border); }
.kpi-row:last-child { border-bottom: none; }
.kpi-row-name { font-size: 15px; line-height: 1.2; font-weight: 500; margin: 0; }
.kpi-row-delta { text-align: right; font-family: var(--font-mono); font-size: 14px; }
.kpi-row-value { font-family: var(--font-mono); font-size: 15px; text-align: right; white-space: nowrap; font-weight: 600; }

.am-panel { margin-top: 1rem; padding-top: .75rem; border-top: 1px solid var(--color-border); }
.am-eyebrow { font-family: var(--font-mono); font-size: 13px; letter-spacing: .15em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 .5rem; }
.am-eyebrow .genre { margin-left: 8px; opacity: .6; text-transform: none; letter-spacing: normal; }
.am-latest { margin-bottom: .75rem; }
.am-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: .1em; color: var(--color-text-muted); text-transform: uppercase; margin: 0; }
.am-title { font-size: 14px; color: var(--color-text-primary); line-height: 1.2; margin: 2px 0 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.am-meta { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); margin: 2px 0 0; }
.am-songs-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: .1em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 4px; }
.am-song-row { display: flex; align-items: baseline; gap: .75rem; font-family: var(--font-mono); font-size: 13px; margin-bottom: 2px; }
.am-song-idx { color: var(--color-text-muted); width: 16px; }
.am-song-title { color: var(--color-text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; min-width: 0; max-width: 30%; }
.am-song-album { color: var(--color-text-muted); font-size: 12px; opacity: .7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; max-width: 45%; text-align: right; }

/* ── Leaderboards ───────────────────────────────────────── */
.lb-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 640px)  { .lb-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 768px)  { .lb-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 1024px) { .lb-grid { grid-template-columns: repeat(4, 1fr); } }
@media (min-width: 1280px) { .lb-grid { grid-template-columns: repeat(5, 1fr); } }
.lb-card { background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 2px; overflow: hidden; }
.lb-head { padding: .75rem 1rem; border-bottom: 1px solid var(--color-border); }
.lb-head-top { display: flex; align-items: flex-start; justify-content: space-between; gap: .5rem; margin-bottom: .5rem; }
.lb-kpi-num { font-family: var(--font-mono); font-size: 12px; letter-spacing: .25em; text-transform: uppercase; font-weight: 700; margin: 0; }
.lb-title { font-family: var(--font-ui); font-weight: 700; font-size: 16px; color: var(--color-text-primary); line-height: 1.2; letter-spacing: -0.01em; margin: 2px 0 0; }
.lb-sort-btn { flex-shrink: 0; font-family: var(--font-mono); font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: var(--color-text-muted); background: none; border: none; cursor: pointer; transition: color .15s ease; }
.lb-sort-btn:hover { color: var(--color-text-secondary); }
.lb-narrative { font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; margin: 4px 0 0; }
.lb-colhead { display: grid; grid-template-columns: 16px 1fr auto auto; align-items: center; gap: 0 .75rem; padding: 6px 1rem; border-bottom: 1px solid var(--color-border); }
.lb-colhead span { font-family: var(--font-mono); font-size: 12px; letter-spacing: .1em; color: var(--color-text-muted); text-transform: uppercase; }
.lb-colhead span.right { text-align: right; font-size: 8px; }
.lb-row { display: grid; grid-template-columns: 16px 1fr auto auto; align-items: center; gap: 0 .75rem; padding: 10px 1rem; border-bottom: 1px solid var(--color-border); transition: background .1s ease; }
.lb-row:last-child { border-bottom: none; }
.lb-row:hover { background: var(--color-bg-card-hover); }
.lb-rank { font-family: var(--font-mono); font-size: 14px; }
.lb-artist { display: flex; align-items: center; gap: 6px; min-width: 0; }
.lb-tier-dot { flex-shrink: 0; width: 6px; height: 6px; border-radius: 50%; }
.lb-artist-name { font-size: 15px; color: var(--color-text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; line-height: 1.2; }
.lb-alert-tag { flex-shrink: 0; font-family: var(--font-mono); font-size: 12px; letter-spacing: .1em; text-transform: uppercase; opacity: .6; color: var(--color-text-muted); }
.lb-delta { text-align: right; font-family: var(--font-mono); font-size: 14px; }
.lb-value-wrap { text-align: right; }
.lb-value { font-family: var(--font-mono); font-size: 15px; white-space: nowrap; font-weight: 600; }
.lb-benchmark { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); white-space: nowrap; margin: 0; }

/* ── AI Analyst chat panel ──────────────────────────────── */
.chat-panel { border: 1px solid var(--color-border); border-radius: 2px; background: var(--color-bg-secondary); margin-bottom: 2rem; overflow: hidden; }
.chat-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; cursor: pointer; border-bottom: 1px solid var(--color-border); transition: background .15s ease; }
.chat-header:hover { background: var(--color-bg-card); }
.chat-header-left { display: flex; align-items: center; gap: .75rem; }
.chat-header-right { display: flex; align-items: center; gap: 1rem; }
.chat-live-dot { position: relative; width: 14px; height: 14px; }
.chat-live-dot-ping { position: absolute; inset: 0; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; opacity: .3; animation: ping 1.4s cubic-bezier(0,0,.2,1) infinite; }
.chat-live-dot-solid { position: relative; width: 14px; height: 14px; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; }
.chat-title { font-family: var(--font-mono); font-size: 11px; letter-spacing: .3em; color: var(--color-text-primary); text-transform: uppercase; }
.chat-subtitle { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-muted); }
.chat-key-badge { font-family: var(--font-mono); font-size: 10px; color: var(--color-text-muted); border: 1px solid var(--color-border); padding: 2px 8px; border-radius: 2px; cursor: pointer; background: none; }
.chat-clear-btn { font-family: var(--font-mono); font-size: 10px; letter-spacing: .1em; color: var(--color-text-muted); text-transform: uppercase; background: none; border: none; cursor: pointer; }
.chat-clear-btn:hover { color: var(--color-text-secondary); }
.chat-caret { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); }

.chat-nokey-notice { padding: 16px 20px; border-bottom: 1px solid var(--color-border); }
.chat-nokey-notice p { font-family: var(--font-mono); font-size: 12px; color: var(--color-text-muted); margin: 0; }
.chat-nokey-notice code { color: var(--color-text-secondary); }
.chat-nokey-notice input { margin-top: 8px; width: 100%; max-width: 420px; font-family: var(--font-mono); font-size: 12px; background: var(--color-bg-card); border: 1px solid var(--color-border); color: var(--color-text-primary); padding: 8px 10px; border-radius: 2px; }

.chat-questions { padding: 16px 20px 12px; border-bottom: 1px solid var(--color-border); }
.chat-questions-label { font-family: var(--font-mono); font-size: 12px; letter-spacing: .25em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 12px; }
.chat-q-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.chat-q-chip {
  display: flex; align-items: flex-start; gap: 10px; text-align: left; padding: 10px 14px; border-radius: 2px; border: 2px solid;
  transition: all .15s ease; cursor: pointer; font-family: var(--font-ui); font-size: 14px; line-height: 1.3; font-weight: 700; background: transparent;
}
.chat-q-chip:disabled { opacity: .4; cursor: not-allowed; }
.chat-q-num { flex-shrink: 0; font-family: var(--font-mono); font-size: 13px; font-weight: 900; margin-top: 2px; width: 20px; }

.chat-history { padding: 16px 20px; display: flex; flex-direction: column; gap: 1rem; max-height: 400px; overflow-y: auto; border-bottom: 1px solid var(--color-border); }
.chat-msg { display: flex; gap: 12px; }
.chat-msg.user { flex-direction: row-reverse; }
.chat-avatar { flex-shrink: 0; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 2px; }
.chat-avatar.user { background: var(--color-text-primary); }
.chat-avatar.ai { background: var(--color-bg-secondary); border: 1px solid var(--color-border-light); }
.chat-avatar span { font-family: var(--font-mono); font-size: 8px; font-weight: 700; }
.chat-avatar.user span { color: var(--color-bg-primary); }
.chat-avatar.ai span { color: var(--color-text-muted); }
.chat-bubble { max-width: 78%; border-radius: 2px; padding: 10px 14px; }
.chat-bubble.user { background: var(--color-text-primary); color: var(--color-bg-primary); }
.chat-bubble.ai { background: var(--color-bg-secondary); border: 1px solid var(--color-border); color: var(--color-text-secondary); }
.chat-bubble p { font-size: 15px; line-height: 1.6; white-space: pre-wrap; font-family: var(--font-ui); margin: 0; }

.chat-input-row { padding: 14px 20px; display: flex; gap: 12px; align-items: flex-end; }
.chat-textarea {
  flex: 1; resize: none; background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: 2px;
  padding: 10px 14px; font-family: var(--font-ui); font-size: 15px; color: var(--color-text-primary);
  min-height: 42px; max-height: 120px; line-height: 1.5; transition: border-color .15s ease;
}
.chat-textarea::placeholder { color: var(--color-text-muted); }
.chat-textarea:focus { outline: none; border-color: var(--color-border-light); }
.chat-send-btn {
  flex-shrink: 0; display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 2px; border: 1px solid;
  font-family: var(--font-mono); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; cursor: pointer; transition: all .15s ease;
}
.chat-send-btn.active { border-color: var(--color-text-primary); background: var(--color-text-primary); color: var(--color-bg-primary); }
.chat-send-btn.active:hover { opacity: .9; }
.chat-send-btn:disabled { border-color: var(--color-border); color: var(--color-text-muted); opacity: .5; cursor: not-allowed; }

/* ── Analyst full page ──────────────────────────────────── */
.analyst-page { display: flex; flex-direction: column; min-height: calc(100vh - 200px); }
.analyst-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 40vh; gap: 1rem; }
.analyst-empty p:first-child { font-family: var(--font-mono); font-size: 16px; color: var(--color-text-muted); letter-spacing: .1em; text-transform: uppercase; }
.analyst-empty p:last-child { font-size: 15px; color: var(--color-text-muted); text-align: center; max-width: 24rem; }
.analyst-header { display: flex; align-items: flex-start; justify-content: flex-end; gap: 1.5rem; margin-bottom: 2rem; }
.analyst-date-label { font-family: var(--font-mono); font-size: 12px; letter-spacing: .2em; color: var(--color-text-muted); text-transform: uppercase; margin: 0; text-align: right; }
.analyst-date-value { font-family: var(--font-mono); font-size: 18px; font-weight: 700; color: #fbbf24; margin: 0; text-align: right; }
.analyst-question-block { margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 2px solid; }
.analyst-q-eyebrow { font-family: var(--font-mono); font-size: 12px; letter-spacing: .3em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 1rem; }
.analyst-q-title { font-family: var(--font-headline); font-weight: 900; line-height: 1.2; color: var(--color-text-primary); font-size: clamp(1.6rem, 3.5vw, 2.8rem); margin: 0; }
.analyst-answer-area { flex: 1; overflow-y: auto; padding-bottom: 2rem; max-height: calc(100vh - 440px); min-height: 300px; }
.analyst-loading { display: flex; align-items: center; gap: 12px; }
.analyst-loading-dot { width: 16px; height: 16px; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; animation: ping 1.4s cubic-bezier(0,0,.2,1) infinite; }
.analyst-loading-label { font-family: var(--font-mono); font-size: 15px; color: var(--color-text-muted); letter-spacing: .1em; }
.analyst-error { font-size: 18px; color: #f87171; }
.analyst-cursor { display: inline-block; width: 16px; height: 16px; margin-left: 4px; background-image: url('CURSOR32_URL_PLACEHOLDER'); background-size: contain; background-repeat: no-repeat; animation: pulse 1.4s ease-in-out infinite; vertical-align: middle; }
.answer-p { font-size: 18px; line-height: 1.6; color: var(--color-text-secondary); margin: 0 0 12px; }
.answer-p strong { color: var(--color-text-primary); font-weight: 700; }
.answer-heading { font-family: var(--font-mono); font-size: 14px; letter-spacing: .1em; text-transform: uppercase; color: #a78bfa; margin: 16px 0 4px; }
.answer-li { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 12px; }
.answer-li-num { flex-shrink: 0; font-family: var(--font-mono); font-size: 16px; font-weight: 700; width: 28px; text-align: right; color: #60a5fa; }
.answer-li-bullet { flex-shrink: 0; font-size: 18px; margin-top: 2px; color: #fbbf24; }
.answer-li p { flex: 1; font-size: 18px; line-height: 1.6; color: var(--color-text-secondary); margin: 0; }

.analyst-tray { position: sticky; bottom: 0; left: 0; right: 0; margin-top: 2rem; padding-top: 1rem; border-top: 2px solid var(--color-border); background: var(--color-bg-primary); }
.analyst-tray-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: .3em; color: var(--color-text-muted); text-transform: uppercase; margin: 0 0 .75rem; }
.analyst-tray-row { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 1rem; scrollbar-width: thin; }
.analyst-tray-chip {
  flex-shrink: 0; display: flex; align-items: flex-start; gap: 8px; text-align: left; padding: 10px 14px; border-radius: 2px; border: 2px solid;
  transition: all .15s ease; cursor: pointer; max-width: 200px; font-family: var(--font-ui); font-size: 13px; font-weight: 700; line-height: 1.3; background: transparent;
}
.analyst-tray-chip:disabled { opacity: .5; cursor: not-allowed; }
.analyst-tray-num { flex-shrink: 0; font-family: var(--font-mono); font-size: 13px; font-weight: 900; }
.analyst-tray-text { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* ── Footer ─────────────────────────────────────────────── */
.footer { border-top: 1px solid var(--color-border); padding: 2rem 0 3rem; }
.footer-row { display: flex; flex-direction: column; gap: 1.5rem; justify-content: space-between; }
@media (min-width: 640px) { .footer-row { flex-direction: row; align-items: flex-start; } }
.footer-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: .2em; color: var(--color-text-primary); text-transform: uppercase; margin: 0; }
.footer-value { font-family: var(--font-mono); font-size: 13px; color: var(--color-text-primary); margin: 2px 0 0; }
.footer-value.small { font-size: 12px; color: var(--color-text-primary); }
.footer-bottom { margin-top: 1.5rem; display: flex; flex-direction: column; align-items: center; justify-content: space-between; gap: .75rem; }
@media (min-width: 640px) { .footer-bottom { flex-direction: row; } }
.footer-wordmark { font-family: var(--font-headline); font-weight: 900; font-size: 13px; color: var(--color-text-primary); letter-spacing: .1em; }
.footer-copyright { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-primary); }
.footer-attribution { margin-top: 1rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; text-align: center; }
@media (min-width: 640px) { .footer-attribution { flex-direction: row; } }
.footer-attribution .powered-by { font-family: var(--font-mono); font-size: 11px; color: var(--color-text-primary); letter-spacing: .1em; text-transform: uppercase; }
.footer-attribution .chromadata { font-family: var(--font-headline); font-weight: 900; font-size: 14px; letter-spacing: .03em; color: #60a5fa; }

/* ── Utility ────────────────────────────────────────────── */
.hidden { display: none !important; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }

@media (max-width: 640px) {
  .masthead, .tabnav, .tab-content { margin-left: 0; margin-right: 0; padding-left: 1rem; padding-right: 1rem; }
}
"""
    return css.replace("CURSOR32_URL_PLACEHOLDER", cursor32_url)
