def get_theme() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   Theme toggle — dark / light mode
   (converted from src/components/theme-toggle.tsx)
   ══════════════════════════════════════════════════════════════════════ */

const THEME_STORAGE_KEY = 'sml-pulse-theme';

function getInitialTheme() {
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  if (stored === 'dark' || stored === 'light') return stored;
  if (window.matchMedia?.('(prefers-color-scheme: light)').matches) return 'light';
  return 'dark';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_STORAGE_KEY, theme);
}

function themeToggleSvg(isDark) {
  if (isDark) {
    return `<svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
  }
  return `<svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
}

function renderThemeToggle(theme, onToggle) {
  const isDark = theme === 'dark';
  const btn = document.createElement('button');
  btn.className = 'theme-toggle';
  btn.setAttribute('aria-label', `Switch to ${isDark ? 'light' : 'dark'} mode`);
  btn.title = `Switch to ${isDark ? 'light' : 'dark'} mode`;
  btn.innerHTML = `<div class="theme-toggle-knob">${themeToggleSvg(isDark)}</div>`;
  btn.addEventListener('click', onToggle);
  return btn;
}

/* SML logo SVG (converted from src/components/sml-logo.tsx) */
function smlLogoSvg(className) {
  const DOT_R = 2.2, SPACING = 6.2, COLS = 7, ROWS = 6;
  const OMIT = new Set(['0,0', '6,0', '0,5', '6,5']);
  const dots = [];
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      if (!OMIT.has(`${c},${r}`)) {
        dots.push({ cx: c * SPACING + DOT_R, cy: r * SPACING + DOT_R });
      }
    }
  }
  const markW = (COLS - 1) * SPACING + DOT_R * 2;
  const markH = (ROWS - 1) * SPACING + DOT_R * 2;
  const GAP = 10, TEXT_Y = markH / 2, FONT_SIZE = 12, FONT_SMALL = 10;

  const circles = dots.map(d => `<circle cx="${d.cx}" cy="${d.cy}" r="${DOT_R}" fill="#CC0000"/>`).join('');

  return `<svg class="${className || ''}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${markW + GAP + 130} ${markH}" height="${markH}" aria-label="Sony Music Latin" role="img">
    <g>${circles}</g>
    <g transform="translate(${markW + GAP}, 0)">
      <text x="0" y="${TEXT_Y - 3}" font-family="'DM Sans','Helvetica Neue',Arial,sans-serif" font-size="${FONT_SIZE}" font-weight="700" letter-spacing="0.08em" fill="var(--color-text-primary)">SONY MUSIC</text>
      <line x1="0" y1="${TEXT_Y + 1}" x2="120" y2="${TEXT_Y + 1}" stroke="var(--color-text-primary)" stroke-width="0.6" opacity="0.35"/>
      <text x="0" y="${TEXT_Y + 5}" font-family="'DM Sans','Helvetica Neue',Arial,sans-serif" font-size="${FONT_SMALL}" font-weight="500" letter-spacing="0.22em" fill="#999999" dominant-baseline="hanging">LATIN</text>
    </g>
  </svg>`;
}
"""
