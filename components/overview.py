def get_overview() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   UI component renderers — return HTML strings (converted from App.tsx
   and the src/components/*.tsx files)
   ══════════════════════════════════════════════════════════════════════ */

// ── Masthead ─────────────────────────────────────────────────────────

function renderMasthead(snapshot) {
  const el = document.createElement('header');
  el.className = 'masthead anim-fade-in';
  el.innerHTML = `
    <div class="masthead-logo-row">
      <div id="sml-logo-slot"></div>
      <div id="theme-toggle-slot"></div>
    </div>
    <div class="masthead-rule"></div>
    <div class="masthead-eyebrow-row">
      <p class="eyebrow">Sony Music Latin · Artist Intelligence</p>
      <p class="eyebrow eyebrow-tight">${escapeHtml(snapshot.snapshot_date)}<span class="cursor-blink">▌</span></p>
    </div>
    <h1>SONY MUSIC LATIN PULSE</h1>
  `;
  el.querySelector('#sml-logo-slot').innerHTML = smlLogoSvg('h-[34px]');
  return el;
}

// ── News ticker ──────────────────────────────────────────────────────

const TICKER_SIGNAL_COLOR = {
  milestone: '#fbbf24', new_release: '#4ade80', chart_movement: '#4ade80',
  rapid_follower_surge: '#60a5fa', platform_silence_breaking: '#60a5fa',
  viral_spike: '#f472b6', collaboration: '#a78bfa', award: '#fbbf24',
  pr_event: '#22d3ee', tour_announcement: '#fb923c',
  declining_metrics: '#f87171', platform_silence: '#f87171',
};

const TICKER_SIGNAL_LABEL = {
  rapid_follower_surge: 'SURGE', platform_silence_breaking: 'RETURN',
  new_release: 'NEW DROP', declining_metrics: 'DECLINE', platform_silence: 'DARK',
  viral_spike: 'VIRAL', milestone: 'MILESTONE', chart_movement: 'CHART',
  award: 'AWARD', collaboration: 'COLLAB', pr_event: 'PRESS', tour_announcement: 'TOUR',
};

function renderNewsTicker(briefing, imageBySlug) {
  const items = [...briefing.items, ...briefing.items];
  const itemsHtml = items.map(item => {
    const accentColor = TICKER_SIGNAL_COLOR[item.signal_type] ?? '#999';
    const signalLabel = TICKER_SIGNAL_LABEL[item.signal_type] ?? item.signal_type.replace(/_/g, ' ').toUpperCase();
    const imgUrl = imageBySlug[item.artist_slug];
    return `
      <span class="ticker-item">
        ${imgUrl ? `<img src="${escapeHtml(imgUrl)}" alt="${escapeHtml(item.artist_name)}" class="ticker-avatar" style="border-color:${accentColor}66">` : ''}
        <span class="ticker-badge" style="background:${accentColor}20;color:${accentColor};border:1px solid ${accentColor}44">${escapeHtml(signalLabel)}</span>
        <span class="ticker-artist" style="color:${accentColor}">${escapeHtml(item.artist_name)}</span>
        <span class="ticker-headline">${escapeHtml(item.headline)}</span>
        <span class="ticker-diamond" style="color:${accentColor}">◆</span>
      </span>`;
  }).join('');

  const el = document.createElement('div');
  el.className = 'ticker-wrap anim-fade-in';
  el.style.animationDelay = '180ms';
  el.innerHTML = `
    <div class="ticker-glow-top"></div>
    <div class="ticker-glow-bottom"></div>
    <div class="ticker-inner">
      <div class="ticker-live">
        <span class="ticker-dot"><span class="ticker-dot-ping"></span><span class="ticker-dot-solid"></span></span>
        <span class="ticker-live-label">Live</span>
        <span class="ticker-sep">│</span>
      </div>
      <div class="ticker-viewport">
        <div class="ticker-track">${itemsHtml}</div>
      </div>
    </div>
  `;
  return el;
}

// ── Tab navigation ───────────────────────────────────────────────────

const TABS = [
  { id: 'stories',      label: 'Top Stories',      color: '#f472b6', activeBg: 'rgba(244,114,182,0.18)', hasCount: true },
  { id: 'roster',       label: 'Artist Roster',    color: '#60a5fa', activeBg: 'rgba(96,165,250,0.18)',  hasCount: true },
  { id: 'leaderboards', label: 'KPI Leaderboards', color: '#fbbf24', activeBg: 'rgba(251,191,36,0.18)',  hasCount: true },
  { id: 'analyst',      label: 'AI Analyst',       color: '#4ade80', activeBg: 'rgba(74,222,128,0.18)',  hasCount: false },
  { id: 'overview',     label: 'Overview',         color: '#a78bfa', activeBg: 'rgba(167,139,250,0.18)', hasCount: false },
];

function renderTabNav(active, counts, onSelect) {
  const el = document.createElement('nav');
  el.className = 'tabnav anim-fade-in';
  const row = document.createElement('div');
  row.className = 'tabnav-row';

  TABS.forEach(tab => {
    const isActive = active === tab.id;
    const btn = document.createElement('button');
    btn.className = 'tab-btn';
    btn.style.borderColor = isActive ? tab.color : `${tab.color}44`;
    btn.style.background  = isActive ? tab.activeBg : 'transparent';
    btn.style.color       = isActive ? tab.color : `${tab.color}88`;
    btn.style.boxShadow   = isActive ? `0 0 12px ${tab.color}22` : 'none';

    let inner = escapeHtml(tab.label);
    if (tab.hasCount) {
      const count = counts[tab.id];
      const bg = isActive ? tab.color : `${tab.color}22`;
      const fg = isActive ? 'var(--color-bg-primary)' : tab.color;
      inner += ` <span class="tab-count" style="background:${bg};color:${fg}">${count}</span>`;
    }
    btn.innerHTML = inner;
    btn.addEventListener('click', () => onSelect(tab.id));
    row.appendChild(btn);
  });

  el.appendChild(row);
  const rule = document.createElement('div');
  rule.className = 'tabnav-rule';
  el.appendChild(rule);
  return el;
}

// ── Overview page ────────────────────────────────────────────────────

const KPI_QUICK_REF = KPI_REGISTRY.map(k => ({
  id: String(k.id).padStart(2, '0'),
  name: k.name,
  desc: k.description,
  domain: getDomainMeta(k.domain),
}));

const TIER_LEGEND = [
  ['●', '#fff',  'Mega',     '>50M total reach — global superstar'],
  ['●', '#999',  'Major',    '10M–50M reach — regional powerhouse'],
  ['●', '#666',  'Rising',   '1M–10M reach — growing momentum'],
  ['●', '#444',  'Emerging', '<1M reach — early-stage artist'],
];

const CONFIDENCE_LEGEND = [
  ['●●●●●', 'Verified',  'Direct from platform, fetched today'],
  ['●●●●○', 'Recent',    'From aggregator or search, <48h old'],
  ['●●●○○', 'Estimated', 'Multiple sources averaged, <7 days'],
  ['●●○○○', 'Stale',     'Best available data, >7 days old'],
  ['●○○○○', 'Inferred',  'Derived from indirect signals'],
];

function renderOverview(roster, snapshot, briefing) {
  const alertCount = snapshot.artists.reduce((n, a) => n + a.kpis.filter(k => k.alert !== null).length, 0);
  const domainCounts = getDomainCounts();

  const kpiRefItems = KPI_QUICK_REF.map(k => `
    <div class="kpi-ref-item">
      <span class="kpi-ref-id">${k.id}</span>
      <div>
        <p class="kpi-ref-name">${escapeHtml(k.name)}</p>
        <p class="kpi-ref-desc"><span style="color:${k.domain.color}">${escapeHtml(k.domain.label)}</span> · ${escapeHtml(k.desc)}</p>
      </div>
    </div>`).join('');

  const tierLegendHtml = TIER_LEGEND.map(([dot, color, tier, desc]) => `
    <div class="badge-row">
      <span class="badge-row-dot" style="color:${color}">${dot}</span>
      <div><span class="badge-row-label">${tier}</span><span class="badge-row-desc">${desc}</span></div>
    </div>`).join('');

  const domainLegendHtml = DOMAIN_REGISTRY.map(domain => `
    <div class="badge-row">
      <span class="badge-row-dot" style="color:${domain.color}">●</span>
      <div><span class="badge-row-label">${domain.label}</span><span class="badge-row-desc">${domain.description} (${domainCounts[domain.id] ?? 0} KPIs)</span></div>
    </div>`).join('');

  const confLegendHtml = CONFIDENCE_LEGEND.map(([dots, label, desc]) => `
    <div class="badge-row">
      <span class="badge-row-dots">${dots}</span>
      <div><span class="badge-row-label">${label}</span><span class="badge-row-desc">${desc}</span></div>
    </div>`).join('');

  const stats = [
    ['Artists tracked', roster.artist_count.toString()],
    ['KPIs per artist',  String(getKpiCount())],
    ['Stories today',    briefing.items.length.toString()],
    ['Data as of',       snapshot.snapshot_date],
  ].map(([label, val]) => `
    <div><p class="ov-stat-label">${label}</p><p class="ov-stat-value">${escapeHtml(val)}</p></div>
  `).join('');

  const el = document.createElement('div');
  el.className = 'ov-space';
  el.innerHTML = `
    <div class="anim-fade-up">
      <div class="ov-hero">
        <p class="ref-eyebrow">What is this?</p>
        <h2>Your daily intelligence briefing<br>for the Sony Music Latin roster.</h2>
        <p class="lede">Sony Latin Pulse runs a daily data pipeline that harvests social metrics, streaming numbers,
        and press mentions for every artist on the roster. It computes ${getKpiCount()} KPIs per artist,
        detects significant changes, and surfaces the most newsworthy developments — all styled
        as a monochrome editorial newsroom.</p>
        <div class="ov-stat-row">${stats}</div>
      </div>
    </div>

    <div class="anim-fade-up" style="animation-delay:100ms">
      <p class="ref-eyebrow" style="margin-bottom:1rem">How to use this app</p>
    </div>

    <div class="grid-2">
      <div class="anim-fade-up" style="animation-delay:150ms">
        <div class="ov-card">
          <div class="ov-card-head"><span class="ov-card-icon">01</span><h3 class="ov-card-title">Top Stories</h3></div>
          <div class="ov-card-body">
            <p>The <strong>Top Stories</strong> tab shows today's most newsworthy developments across the roster, ranked by significance score.</p>
            <p>Each story card shows the artist image, a signal type badge (e.g. <em>MILESTONE</em>, <em>VIRAL</em>, <em>NEW RELEASE</em>), headline, KPI impact, and a 2–3 sentence editorial summary written by the AI news desk.</p>
            <p>Stories are scored using a weighted rubric — milestone crossings score highest (10), new releases and chart entries follow (9), then viral spikes and collaborations (8).</p>
          </div>
        </div>
      </div>
      <div class="anim-fade-up" style="animation-delay:200ms">
        <div class="ov-card">
          <div class="ov-card-head"><span class="ov-card-icon">02</span><h3 class="ov-card-title">Artist Roster</h3></div>
          <div class="ov-card-body">
            <p>The <strong>Artist Roster</strong> tab shows every artist as a card with their photo, tier, and 4 headline KPIs at a glance.</p>
            <p><strong>Click any card</strong> to expand all ${getKpiCount()} KPIs with current values, trend arrows (▲ up / ▼ down), and percentage deltas versus the previous snapshot.</p>
            <p>Artist images are grayscale by default — <strong>hover</strong> any image to reveal color. Tier dots (white = Mega, gray = Major, dark = Rising/Emerging) appear top-right of each photo.</p>
          </div>
        </div>
      </div>
      <div class="anim-fade-up" style="animation-delay:250ms">
        <div class="ov-card">
          <div class="ov-card-head"><span class="ov-card-icon">03</span><h3 class="ov-card-title">KPI Leaderboards</h3></div>
          <div class="ov-card-body">
            <p>The <strong>KPI Leaderboards</strong> tab ranks the top 5 artists for each of the ${getKpiCount()} KPIs side-by-side.</p>
            <p>Use the <strong>↓ DESC / ↑ ASC</strong> toggle on any leaderboard to flip the sort direction — useful for spotting artists at the bottom of a metric (e.g. longest release gap, lowest engagement rate).</p>
            <p>Delta percentages (Δ column) show the change since the last snapshot. Trend arrows color-code each movement: white = up, gray = down, dash = flat.</p>
          </div>
        </div>
      </div>
      <div class="anim-fade-up" style="animation-delay:300ms">
        <div class="ov-card">
          <div class="ov-card-head"><span class="ov-card-icon">04</span><h3 class="ov-card-title">News Ticker</h3></div>
          <div class="ov-card-body">
            <p>The <strong>scrolling ticker</strong> beneath the masthead always shows the current day's headlines — one per story, in priority order, looping continuously.</p>
            <p>The ticker is present on every tab so you never lose sight of today's most important movements while browsing the roster or leaderboards.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="anim-fade-up" style="animation-delay:350ms">
      <div class="kpi-ref-card">
        <p class="ref-eyebrow">KPI Reference</p>
        <h3 class="ref-title">The ${getKpiCount()} tracked metrics — what each one means</h3>
        <div class="kpi-ref-grid">${kpiRefItems}</div>
      </div>
    </div>

    <div class="anim-fade-up" style="animation-delay:375ms">
      <div class="badge-ref-card">
        <p class="ref-eyebrow">Business domains</p>
        <h3 class="ref-title">Where the KPIs live today</h3>
        <div class="badge-grid">
          <div><p class="badge-col-title">Domain map</p>${domainLegendHtml}</div>
          <div><p class="badge-col-title">What this means</p><div class="badge-row"><span class="badge-row-dot" style="color:var(--color-text-muted)">●</span><div><span class="badge-row-label">Financial / Contracts ready</span><span class="badge-row-desc">The registry already reserves slots for internal business metrics, so we can swap in finance and contract KPIs without rewriting the newsroom shell.</span></div></div></div>
        </div>
      </div>
    </div>

    <div class="anim-fade-up" style="animation-delay:400ms">
      <div class="badge-ref-card">
        <p class="ref-eyebrow">Reading the badges</p>
        <h3 class="ref-title">Alert labels and artist tiers</h3>
        <div class="badge-grid">
          <div><p class="badge-col-title">Artist Tiers</p>${tierLegendHtml}</div>
          <div><p class="badge-col-title">Data Confidence</p>${confLegendHtml}</div>
        </div>
      </div>
    </div>
  `;
  return el;
}
"""
