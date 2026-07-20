def get_roster() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   Artist card + Roster grid
   (converted from src/components/artist-card.tsx + RosterGrid in App.tsx)
   ══════════════════════════════════════════════════════════════════════ */

function alertBadgeHtml(label) {
  const { bg, text, border } = alertColors(label);
  const clean = label.replace(/—.*/, '').trim();
  return `<span class="alert-badge" style="background:${bg};color:${text};border:1px solid ${border}">${escapeHtml(clean)}</span>`;
}

function appleMusicPanelHtml(kpi11) {
  if (!kpi11) return '';
  const latest = kpi11.latest_release || {};
  const topSongs = kpi11.top_songs || [];
  const totalAlbums = kpi11.total_albums;
  const genre = kpi11.primary_genre;

  if (!latest.title && topSongs.length === 0 && !totalAlbums) return '';

  let html = `<div class="am-panel"><p class="am-eyebrow">Apple Music${genre ? `<span class="genre">· ${escapeHtml(genre)}</span>` : ''}</p>`;

  if (latest.title) {
    html += `<div class="am-latest">
      <p class="am-label">Latest release</p>
      <p class="am-title">${escapeHtml(latest.title)}</p>
      <p class="am-meta">${escapeHtml(latest.date ?? '—')}${latest.type ? `<span style="opacity:.6;margin-left:8px">· ${escapeHtml(latest.type)}</span>` : ''}${totalAlbums != null ? `<span style="opacity:.6;margin-left:12px">${totalAlbums} albums in catalog</span>` : ''}</p>
    </div>`;
  }

  if (topSongs.length > 0) {
    html += `<div><p class="am-songs-label">Top songs</p><ol style="list-style:none;padding:0;margin:0">`;
    topSongs.slice(0, 5).forEach((s, i) => {
      html += `<li class="am-song-row"><span class="am-song-idx">${i + 1}</span><span class="am-song-title">${escapeHtml(s.title ?? '—')}</span>${s.album ? `<span class="am-song-album">${escapeHtml(s.album)}</span>` : ''}</li>`;
    });
    html += `</ol></div>`;
  }

  html += `</div>`;
  return html;
}

function kpiRowHtml(kpi) {
  const showPct = kpi.delta_percent !== null && Math.abs(kpi.delta_percent) < 500;
  const labelColor = KPI_COLOR[kpi.kpi_id] ?? '#9ca3af';
  const v = kpi.current_value;
  let displayValue;
  if (v == null) {
    displayValue = '—';
  } else {
    switch (kpi.kpi_id) {
      case 1: displayValue = fmtNumber(v); break;
      case 2: displayValue = `${v.toFixed(2)}%`; break;
      case 3: displayValue = `${v.toFixed(2)}%`; break;
      case 4: displayValue = fmtNumber(v); break;
      case 5: displayValue = `${v.toFixed(2)}%`; break;
      case 6: displayValue = `${v} posts/wk`; break;
      case 7: displayValue = `${(v * 100).toFixed(0)}%`; break;
      case 8: displayValue = fmtNumber(v); break;
      case 9: displayValue = fmtRecencyDays(v); break;
      case 10: displayValue = `${v} articles`; break;
      case 12: displayValue = fmtCurrency(v); break;
      case 13: displayValue = fmtExpiryDays(v); break;
      case 14: displayValue = fmtCurrency(v); break;
      case 15: displayValue = fmtCurrency(v); break;
      case 16: displayValue = `${v} placements`; break;
      case 18: displayValue = `${v.toFixed(2)}%`; break;
      case 19: displayValue = fmtNumber(v); break;
      case 20: displayValue = `${v.toFixed(2)}%`; break;
      default: displayValue = v.toString();
    }
  }

  let valueColor = 'var(--color-text-primary)';
  if (kpi.kpi_id === 9) valueColor = recencyColor(v);
  if (kpi.kpi_id === 3) valueColor = engColor(kpi.benchmark_tier);
  if (kpi.kpi_id === 2 || kpi.kpi_id === 5) {
    if (kpi.trend === 'up') valueColor = CLR.up;
    if (kpi.trend === 'down') valueColor = CLR.down;
  }

  const deltaColor = kpi.trend === 'up' ? CLR.up : kpi.trend === 'down' ? CLR.down : CLR.flat;

  return `
    <div class="kpi-row">
      <div>
        <p class="kpi-row-name" style="color:${labelColor}">${escapeHtml(kpi.kpi_name)}</p>
        ${kpi.alert ? alertBadgeHtml(kpi.alert) : ''}
      </div>
      <div class="kpi-row-delta">
        ${showPct && kpi.delta_percent !== null ? `<span style="color:${deltaColor}">${trendArrowHtml(kpi.trend, CLR.up, CLR.down, CLR.flat)} ${fmtDelta(kpi.delta_percent)}</span>` : ''}
      </div>
      <div class="kpi-row-value" style="color:${valueColor}">${displayValue}</div>
    </div>
  `;
}

function renderArtistCard(artist, snapshot, initiallyExpanded) {
  const kpi = Object.fromEntries(snapshot.kpis.map(k => [k.kpi_id, k]));
  const reach = kpi[1], velocity = kpi[2], engagement = kpi[3], spotify = kpi[4], recency = kpi[9];

  const alerts = snapshot.kpis.filter(k => k.alert !== null).map(k => ({ id: k.kpi_id, label: k.alert }));
  const tierColor = TIER_COLOR[snapshot.tier];
  const velColor = velocity.trend === 'up' ? CLR.up : velocity.trend === 'down' ? CLR.down : CLR.flat;
  const spTrColor = spotify.trend === 'up' ? CLR.up : spotify.trend === 'down' ? CLR.down : CLR.flat;

  const article = document.createElement('article');
  article.className = 'artist-card';
  article.setAttribute('role', 'button');
  article.setAttribute('aria-label', `${artist.name} artist card`);

  let expanded = !!initiallyExpanded;

  const fallbackSrc = `https://placehold.co/192x192/1A1A1A/444444?text=${encodeURIComponent(artist.slug)}`;

  function alertsHtml() {
    if (alerts.length === 0) return '';
    return `<div class="ac-divider"></div><div class="ac-alerts">${alerts.map(a => alertBadgeHtml(a.label)).join('')}</div>`;
  }

  function expandedHtml() {
    if (!expanded) return '';
    const kpisHtml = snapshot.kpis.map(kpiRowHtml).join('');
    const am = appleMusicPanelHtml(snapshot.kpis.find(k => k.kpi_id === 11));
    return `
      <div class="ac-expanded">
        <div class="ac-expanded-inner">
          <p class="ac-expanded-label">All KPIs · ${new Date().toISOString().slice(0, 10)}</p>
          ${kpisHtml}
          ${am}
        </div>
      </div>
    `;
  }

  function render() {
    article.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    article.innerHTML = `
      <div class="artist-card-sweep" style="background:${tierColor}"></div>
      <div class="ac-avatar-wrap">
        <div class="ac-avatar-inner">
          <img class="ac-avatar" src="${escapeHtml(artist.image_url)}" alt="${escapeHtml(artist.name)}" width="192" height="192" style="border-color:${tierColor}55" onerror="this.onerror=null;this.src='${fallbackSrc}'">
          <span class="ac-tier-dot" style="background:${tierColor}" title="${snapshot.tier} tier"></span>
        </div>
      </div>
      <div class="ac-identity">
        <h3 class="ac-name">${escapeHtml(artist.name)}</h3>
        <p class="ac-tier-line">
          <span class="tier-label" style="color:${tierColor}">${TIER_LABEL[snapshot.tier]}</span>
          <span class="sep">·</span>
          <span class="reach-val">${fmtNumber(reach.current_value)}</span>
        </p>
        <p class="ac-narrative">${escapeHtml(buildNarrative(snapshot))}</p>
      </div>
      <div class="ac-divider"></div>
      <div class="ac-kpis">
        <div class="ac-kpi-row">
          <span class="ac-kpi-label" style="color:${CLR.reach}">Reach</span>
          <span class="ac-kpi-value">${fmtNumber(reach.current_value)}${velocity.current_value != null ? `<span class="delta" style="color:${velColor}">${trendArrowHtml(velocity.trend, CLR.up, CLR.down, CLR.flat)} ${fmtDelta(velocity.current_value)}</span>` : ''}</span>
        </div>
        <div class="ac-kpi-row">
          <span class="ac-kpi-label" style="color:${CLR.spotify}">Spotify</span>
          <span class="ac-kpi-value">${fmtNumber(spotify.current_value)}<span class="delta" style="color:${spTrColor}">${trendArrowHtml(spotify.trend, CLR.up, CLR.down, CLR.flat)}</span></span>
        </div>
        <div class="ac-kpi-row">
          <span class="ac-kpi-label" style="color:${CLR.engRate}">Eng. Rate</span>
          <span class="ac-kpi-value"><span style="color:${engColor(engagement.benchmark_tier)}">${engagement.current_value != null ? `${engagement.current_value.toFixed(2)}%` : '—'}</span>${engagement.benchmark_tier ? `<span style="margin-left:6px;font-size:13px;color:var(--color-text-muted)">${escapeHtml(engagement.benchmark_tier)}</span>` : ''}</span>
        </div>
        <div class="ac-kpi-row">
          <span class="ac-kpi-label" style="color:${CLR.release}">Release</span>
          <span style="font-family:var(--font-mono);font-size:15px;font-weight:600;color:${recencyColor(recency.current_value)}">${fmtRecencyDays(recency.current_value)}</span>
        </div>
      </div>
      ${alertsHtml()}
      ${expandedHtml()}
      <div class="ac-expand-hint"><span style="color:${tierColor}">${expanded ? '↑ Collapse' : '↓ All KPIs'}</span></div>
    `;

    // Prevent expand-panel clicks from toggling collapse
    const exp = article.querySelector('.ac-expanded');
    if (exp) exp.addEventListener('click', e => e.stopPropagation());
  }

  article.addEventListener('click', () => {
    expanded = !expanded;
    render();
  });

  render();
  return article;
}

const TIER_OPTIONS = [
  { value: 'all',      label: 'All Tiers', color: '#9ca3af' },
  { value: 'mega',     label: 'Mega',      color: '#fbbf24' },
  { value: 'major',    label: 'Major',     color: '#60a5fa' },
  { value: 'rising',   label: 'Rising',    color: '#a78bfa' },
  { value: 'emerging', label: 'Emerging',  color: '#34d399' },
];

function renderRosterGrid(roster, snapshotBySlug, state, setState) {
  const el = document.createElement('section');

  const header = document.createElement('div');
  header.className = 'anim-fade-up';
  header.style.animationDelay = '50ms';

  const q = state.searchQuery.trim().toLowerCase();
  const filtered = roster.artists.filter(a => {
    const tierOk = state.tierFilter === 'all' || snapshotBySlug[a.slug]?.tier === state.tierFilter;
    if (!tierOk) return false;
    if (!q) return true;
    if (a.name.toLowerCase().includes(q)) return true;
    if (a.aliases?.some(alias => alias.toLowerCase().includes(q))) return true;
    return false;
  });

  const activeTier = TIER_OPTIONS.find(t => t.value === state.tierFilter);
  const autoExpandSingle = q.length > 0 && filtered.length === 1;

  const tierBtnsHtml = TIER_OPTIONS.map(opt => {
    const isActive = state.tierFilter === opt.value;
    const count = opt.value !== 'all' ? roster.artists.filter(a => snapshotBySlug[a.slug]?.tier === opt.value).length : null;
    return `<button class="tier-btn" data-tier="${opt.value}" style="border-color:${isActive ? opt.color : opt.color + '44'};background:${isActive ? opt.color + '22' : 'transparent'};color:${isActive ? opt.color : opt.color + '88'}">${opt.label}${count !== null ? `<span class="count">${count}</span>` : ''}</button>`;
  }).join('');

  header.innerHTML = `
    <div class="roster-toolbar">
      <div>
        <h2 class="roster-title">ARTIST ROSTER</h2>
        <p class="roster-subtitle">${filtered.length} of ${roster.artist_count} artists${q && filtered.length === 1 ? ' · expanded below' : ''}${!q ? ' · click to expand KPIs' : ''}</p>
      </div>
      <div class="roster-controls">
        <div class="search-wrap">
          <span class="search-icon" aria-hidden="true">⌕</span>
          <input type="text" class="search-input" id="roster-search-input" placeholder="Search artist…" aria-label="Search artists by name" value="${escapeHtml(state.searchQuery)}">
          ${state.searchQuery ? `<button class="search-clear" id="roster-search-clear" aria-label="Clear search">×</button>` : ''}
        </div>
        <div class="tier-filter-row" id="roster-tier-row">${tierBtnsHtml}</div>
      </div>
    </div>
  `;
  el.appendChild(header);

  header.querySelector('#roster-search-input').addEventListener('input', e => {
    setState({ ...state, searchQuery: e.target.value });
  });
  const clearBtn = header.querySelector('#roster-search-clear');
  if (clearBtn) clearBtn.addEventListener('click', () => setState({ ...state, searchQuery: '' }));
  header.querySelector('#roster-tier-row').addEventListener('click', e => {
    const btn = e.target.closest('.tier-btn');
    if (!btn) return;
    setState({ ...state, tierFilter: btn.dataset.tier });
  });

  if (filtered.length === 0) {
    const empty = document.createElement('p');
    empty.className = 'empty-msg';
    empty.innerHTML = q
      ? `No artists match "<span style="color:var(--color-text-primary)">${escapeHtml(state.searchQuery)}</span>"${state.tierFilter !== 'all' ? ` in the <span style="color:${activeTier.color}">${activeTier.label}</span> tier` : ''}.`
      : `No artists in the <span style="color:${activeTier.color}">${activeTier.label}</span> tier.`;
    el.appendChild(empty);
  } else {
    const grid = document.createElement('div');
    grid.className = 'roster-grid';
    filtered.forEach((artist, i) => {
      const snap = snapshotBySlug[artist.slug];
      if (!snap) return;
      const wrap = document.createElement('div');
      wrap.className = 'anim-fade-up';
      wrap.style.animationDelay = `${100 + Math.min(i * 35, 900)}ms`;
      wrap.appendChild(renderArtistCard(artist, snap, autoExpandSingle));
      grid.appendChild(wrap);
    });
    el.appendChild(grid);
  }

  return el;
}
"""
