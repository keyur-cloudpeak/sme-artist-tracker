def get_leaderboards() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   KPI Leaderboards
   (converted from src/components/kpi-leaderboard.tsx)
   ══════════════════════════════════════════════════════════════════════ */

const LB_KPI_COLOR = {
  1: '#60a5fa', 2: '#60a5fa', 3: '#c084fc', 4: '#4ade80', 5: '#4ade80',
  6: '#22d3ee', 7: '#2dd4bf', 8: '#f472b6', 9: '#fbbf24', 10: '#fb923c', 11: '#f87171',
};

const KPI_META = {
  1:  { name: 'Total Social Reach',           shortName: 'Reach',       format: 'number',   invertSort: false },
  2:  { name: 'Social Reach Velocity',        shortName: 'Velocity',    format: 'percent',  invertSort: false },
  3:  { name: 'Engagement Rate',              shortName: 'Eng. Rate',   format: 'percent',  invertSort: false },
  4:  { name: 'Spotify Monthly Listeners',    shortName: 'Spotify',     format: 'number',   invertSort: false },
  5:  { name: 'Spotify Listener Trend',       shortName: 'Spotify Δ',   format: 'percent',  invertSort: false },
  6:  { name: 'Content Velocity',             shortName: 'Posts/wk',    format: 'posts',    invertSort: false },
  7:  { name: 'Platform Diversity Score',     shortName: 'Diversity',   format: 'ratio',    invertSort: false },
  8:  { name: 'YouTube Weekly Velocity',      shortName: 'YT Views',    format: 'number',   invertSort: false },
  9:  { name: 'Latest Release Recency',       shortName: 'Release',     format: 'recency',  invertSort: true  },
  10: { name: 'News & Press Mentions',        shortName: 'Press',       format: 'articles', invertSort: false },
  11: { name: 'Apple Music Catalog Activity', shortName: 'AM Releases', format: 'posts',    invertSort: false },
};

const KPI_NARRATIVE = {
  1: 'Total Social Reach is the headline number for label negotiations and brand partnerships. It represents the combined addressable audience across every platform — the larger the reach, the greater the leverage when pricing sync deals, sponsorships, and touring guarantees.',
  2: 'Reach Velocity is an early-warning signal. A sustained uptick of 2 %+ daily often precedes a breakout moment — an ideal time to increase marketing spend and pitch editorial playlists before the wave crests. A sustained decline signals audience fatigue or platform disengagement that needs A&R attention.',
  3: 'Engagement Rate separates authentic fanbases from inflated follower counts. A highly engaged smaller audience will convert to ticket sales and merchandise at far higher rates than a passive mega-following. Use this metric to identify artists who are ready for premium brand integrations.',
  4: "Spotify Monthly Listeners is the industry's de facto streaming power metric — used by promoters, labels, and sync agents to gauge real-time commercial relevance. Above 20 M qualifies an artist for headliner status on major festival circuits.",
  5: 'Spotify Listener Trend measures release impact and streaming momentum. A 20 %+ spike typically indicates a successful new drop or playlist addition. Sustained positive trend over multiple weeks signals genuine catalogue growth — a key argument for increased A&R investment.',
  6: 'Content Velocity tracks how actively an artist is feeding the algorithm. Consistent posting (7–14 pieces per week) sustains platform reach without paid promotion. A sudden drop in velocity is often the earliest observable signal of an artist going inactive or entering a contract dispute.',
  7: 'Platform Diversity Score measures distribution risk. An artist reliant on a single platform is vulnerable to algorithm changes or account issues. A score above 0.7 indicates a healthy multi-platform presence that protects revenue streams and reaches different demographic segments.',
  8: "YouTube Weekly Velocity captures the visual content engine — the primary driver of new fan acquisition. Average views across the artist's 5 most recent uploads signal whether music video investments are paying off and whether the artist's content is being pushed by YouTube's algorithm. Sustained high values predict streaming uplift weeks before it shows on Spotify.",
  9: 'Release Recency tracks how fresh the catalogue is in the streaming ecosystem. Artists beyond 120 days without a release see measurable audience retention decay. Cross-checked across Spotify and Apple Music — uses whichever platform indexed the latest drop first. Use this leaderboard in ascending order to identify artists urgently needing a content drop to re-enter the algorithm cycle.',
  10: 'News & Press Mentions quantify cultural relevance beyond owned channels. High press velocity amplifies all other KPIs — streaming, social growth, and engagement all lift when an artist is in the news cycle. Monitor this metric to time campaign activations with organic media momentum.',
  11: "Apple Music Catalog Activity counts the releases — singles, EPs, albums — that landed on iTunes / Apple Music in the last 90 days. Apple's ecosystem skews older and more affluent than Spotify, so a strong cadence here signals reach into the demographics that drive premium pricing for sync, sponsorship, and tour. Pair with KPI 5 (Spotify Listener Trend) to detect platform-asymmetric breakouts.",
};

function fmtRecencyLb(days) {
  if (days === 0) return 'today';
  if (days === 1) return '1d ago';
  if (days <= 60) return `${days}d ago`;
  if (days < 365) return `${Math.round(days / 30)}mo ago`;
  return `${(days / 365).toFixed(1)}yr ago`;
}

function fmtValueLb(val, format) {
  if (val == null) return '—';
  switch (format) {
    case 'number':   return fmtNumber(val);
    case 'percent':  return `${val.toFixed(2)}%`;
    case 'recency':  return fmtRecencyLb(val);
    case 'posts':    return `${val}`;
    case 'ratio':    return `${(val * 100).toFixed(0)}%`;
    case 'articles': return `${val}`;
  }
}

function buildLeaderRows(artists, kpiId, asc) {
  const rows = [];
  for (const a of artists) {
    const kpi = a.kpis.find(k => k.kpi_id === kpiId);
    if (!kpi) continue;
    rows.push({
      artistName: a.artist_name, artistSlug: a.artist_slug, tier: a.tier,
      currentValue: kpi.current_value, deltaPercent: kpi.delta_percent,
      trend: kpi.trend, benchmarkTier: kpi.benchmark_tier, alert: kpi.alert,
    });
  }
  rows.sort((a, b) => {
    const av = a.currentValue ?? (asc ? Infinity : -Infinity);
    const bv = b.currentValue ?? (asc ? Infinity : -Infinity);
    return asc ? av - bv : bv - av;
  });
  rows.forEach((r, i) => { r.rank = i + 1; });
  return rows.slice(0, 5);
}

function renderKpiLeaderboard(kpiId, artists, limit) {
  limit = limit || 5;
  const meta = KPI_META[kpiId];
  if (!meta) return document.createTextNode('');

  let asc = meta.invertSort;
  const accentColor = LB_KPI_COLOR[kpiId] ?? '#999';
  const showDelta = kpiId !== 6 && kpiId !== 7 && kpiId !== 9 && kpiId !== 10;

  const wrap = document.createElement('div');
  wrap.className = 'lb-card';
  wrap.style.borderTop = `2px solid ${accentColor}`;

  function render() {
    const rows = buildLeaderRows(artists, kpiId, asc).slice(0, limit);

    const rowsHtml = rows.map(row => {
      const dotColor = TIER_DOT_COLOR[row.tier] ?? '#444';
      const deltaColor = row.trend === 'up' ? 'var(--color-accent-up)' : row.trend === 'down' ? 'var(--color-accent-down)' : 'var(--color-text-muted)';
      const deltaCell = showDelta
        ? `<div class="lb-delta">${row.deltaPercent !== null && Math.abs(row.deltaPercent) < 500 ? `<span style="color:${deltaColor}">${trendArrowHtml(row.trend, 'var(--color-accent-up)', 'var(--color-accent-down)', 'var(--color-text-muted)')} ${fmtDelta(row.deltaPercent)}</span>` : ''}</div>`
        : `<div></div>`;
      const valueColor = row.rank === 1 ? accentColor : 'var(--color-text-primary)';

      return `
        <div class="lb-row">
          <span class="lb-rank" style="color:${row.rank === 1 ? 'var(--color-text-primary)' : 'var(--color-text-muted)'}">${row.rank}</span>
          <div class="lb-artist">
            <span class="lb-tier-dot" style="background:${dotColor}" title="${row.tier}"></span>
            <span class="lb-artist-name">${escapeHtml(row.artistName)}</span>
            ${row.alert ? `<span class="lb-alert-tag">${escapeHtml(row.alert.replace(/—.*/, '').trim())}</span>` : ''}
          </div>
          ${deltaCell}
          <div class="lb-value-wrap">
            <span class="lb-value" style="color:${valueColor}">${fmtValueLb(row.currentValue, meta.format)}</span>
            ${row.benchmarkTier ? `<p class="lb-benchmark">${escapeHtml(row.benchmarkTier)}</p>` : ''}
          </div>
        </div>
      `;
    }).join('');

    wrap.innerHTML = `
      <div class="lb-head">
        <div class="lb-head-top">
          <div>
            <p class="lb-kpi-num" style="color:${accentColor}">KPI ${kpiId.toString().padStart(2, '0')}</p>
            <h3 class="lb-title">${escapeHtml(meta.name)}</h3>
          </div>
          <button class="lb-sort-btn" id="lb-sort-${kpiId}" title="${asc ? 'Sort descending' : 'Sort ascending'}" aria-label="Sort ${asc ? 'descending' : 'ascending'}">${asc ? '↑ ASC' : '↓ DESC'}</button>
        </div>
        ${KPI_NARRATIVE[kpiId] ? `<p class="lb-narrative">${escapeHtml(KPI_NARRATIVE[kpiId])}</p>` : ''}
      </div>
      <div class="lb-colhead">
        <span>#</span><span>Artist</span>
        ${showDelta ? `<span class="right">Δ</span>` : `<span></span>`}
        <span class="right">${meta.shortName}</span>
      </div>
      ${rowsHtml}
    `;

    wrap.querySelector(`#lb-sort-${kpiId}`).addEventListener('click', () => {
      asc = !asc;
      render();
    });
  }

  render();
  return wrap;
}

function renderLeaderboards(snapshot) {
  const el = document.createElement('section');
  const label = document.createElement('div');
  label.className = 'anim-fade-up';
  label.style.animationDelay = '50ms';
  label.innerHTML = `<div class="section-label-row"><h2 class="section-label">KPI LEADERBOARDS</h2><span class="section-meta">top 5 per metric · click ↓↑ to sort</span></div>`;
  el.appendChild(label);

  const grid = document.createElement('div');
  grid.className = 'lb-grid';
  [1,2,3,4,5,6,7,8,9,10,11].forEach((id, i) => {
    const wrap = document.createElement('div');
    wrap.className = 'anim-fade-up';
    wrap.style.animationDelay = `${100 + Math.min(i * 35, 900)}ms`;
    wrap.appendChild(renderKpiLeaderboard(id, snapshot.artists));
    grid.appendChild(wrap);
  });
  el.appendChild(grid);
  return el;
}
"""
