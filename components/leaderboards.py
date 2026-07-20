def get_leaderboards() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   KPI Leaderboards
   (converted from src/components/kpi-leaderboard.tsx)
   ══════════════════════════════════════════════════════════════════════ */

const LB_KPI_COLOR = Object.fromEntries(KPI_REGISTRY.map(k => [k.id, k.color]));
const KPI_META = Object.fromEntries(KPI_REGISTRY.map(k => [k.id, k]));

function fmtNumber(n) {
  if (n === null || n === undefined) return '—';
  if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}B`;
  if (n >= 1_000_000)     return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)         return `${(n / 1_000).toFixed(0)}K`;
  return n.toString();
}

function fmtCurrency(n) {
  if (n === null || n === undefined) return '—';
  const num = Number(n);
  return `$${fmtNumber(num)}`;
}

function fmtRecencyLb(days) {
  if (days === 0) return 'today';
  if (days === 1) return '1d ago';
  if (days <= 60) return `${days}d ago`;
  if (days < 365) return `${Math.round(days / 30)}mo ago`;
  return `${(days / 365).toFixed(1)}yr ago`;
}

function fmtExpiryLb(days) {
  if (days === null || days === undefined) return '—';
  if (days < 0) return 'Expired';
  return fmtRecencyLb(days).replace(' ago', '');
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
    case 'currency': return fmtCurrency(val);
    case 'expiry':   return fmtExpiryLb(val);
    default:         return val.toString();
  }
}

function renderKpiDetails(meta) {
  const domain = getDomainMeta(meta.domain);
  return `
    <details open class="lb-details" style="margin-top:0.75rem;padding-top:0.6rem;border-top:1px solid rgba(255,255,255,0.08)">
      <summary class="lb-details-summary" style="cursor:pointer;list-style:none;font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--color-text-primary);display:flex;align-items:center;justify-content:space-between;gap:0.5rem;font-weight:700">
        <span>Details</span>
        <span style="font-size:0.7rem;opacity:0.75">Open</span>
      </summary>
      <div class="lb-details-body" style="margin-top:0.65rem;display:grid;gap:0.5rem">
        <p style="margin:0;display:flex;justify-content:space-between;gap:0.75rem"><span class="lb-details-label" style="color:var(--color-text-muted);font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase">Domain</span><span class="lb-details-value" style="color:${domain.color};font-weight:700">${escapeHtml(domain.label)}</span></p>
        <p style="margin:0;line-height:1.45"><span class="lb-details-label" style="display:block;color:var(--color-text-muted);font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.25rem">Why it matters</span><span class="lb-details-value" style="color:var(--color-text-secondary)">${escapeHtml(meta.description || meta.narrative || 'No detail available yet.')}</span></p>
      </div>
    </details>
  `;
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
  const accentColor = meta.color ?? '#999';
  const showDelta = ![6, 7, 9, 10, 13, 15].includes(kpiId);

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
        ${meta.narrative ? `<p class="lb-narrative">${escapeHtml(meta.narrative)}</p>` : ''}
        ${renderKpiDetails(meta)}
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
  KPI_REGISTRY.forEach((meta, i) => {
    const id = meta.id;
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
