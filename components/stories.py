def get_stories() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   News feed / story item card
   (converted from src/components/news-item.tsx)
   ══════════════════════════════════════════════════════════════════════ */

const SIGNAL_LABEL = {
  rapid_follower_surge: 'RAPID SURGE', platform_silence_breaking: 'SILENCE → ACTIVE',
  new_release: 'NEW RELEASE', declining_metrics: 'DECLINING', platform_silence: 'GOING DARK',
  viral_spike: 'VIRAL', milestone: 'MILESTONE', chart_movement: 'CHART MOVE',
  award: 'AWARD', collaboration: 'COLLAB', pr_event: 'PR EVENT', tour_announcement: 'TOUR',
};

const SIGNAL_STYLE = {
  milestone:                 { bg: '#fbbf2422', text: '#fbbf24', border: '#fbbf2466' },
  new_release:                { bg: '#4ade8022', text: '#4ade80', border: '#4ade8066' },
  chart_movement:             { bg: '#4ade8022', text: '#4ade80', border: '#4ade8066' },
  rapid_follower_surge:       { bg: '#60a5fa22', text: '#60a5fa', border: '#60a5fa66' },
  platform_silence_breaking:  { bg: '#60a5fa22', text: '#60a5fa', border: '#60a5fa66' },
  viral_spike:                { bg: '#f472b622', text: '#f472b6', border: '#f472b666' },
  collaboration:               { bg: '#a78bfa22', text: '#a78bfa', border: '#a78bfa66' },
  award:                       { bg: '#fbbf2422', text: '#fbbf24', border: '#fbbf2466' },
  pr_event:                    { bg: '#22d3ee22', text: '#22d3ee', border: '#22d3ee66' },
  tour_announcement:           { bg: '#fb923c22', text: '#fb923c', border: '#fb923c66' },
  declining_metrics:           { bg: '#f8717122', text: '#f87171', border: '#f8717166' },
  platform_silence:            { bg: '#f8717122', text: '#f87171', border: '#f8717166' },
};

function trendArrowHtml(dir, upClr, downClr, flatClr) {
  if (dir === 'up')   return `<span style="color:${upClr}">▲</span>`;
  if (dir === 'down') return `<span style="color:${downClr}">▼</span>`;
  return `<span style="color:${flatClr}">—</span>`;
}

function kpiImpactBadgeHtml(impact) {
  const dir = impact.direction ?? 'flat';
  const absVal = impact.delta_absolute ?? null;
  const pctVal = impact.delta_percent ?? null;
  const hasDelta = absVal != null || pctVal != null;

  const dirColor = dir === 'up' ? 'var(--color-accent-up)' : dir === 'down' ? 'var(--color-accent-down)' : 'var(--color-text-muted)';

  let deltaHtml = '';
  if (hasDelta) {
    deltaHtml = `<span style="color:${dirColor}">${trendArrowHtml(dir, 'var(--color-accent-up)', 'var(--color-accent-down)', 'var(--color-text-muted)')}`;
    if (absVal != null) deltaHtml += ` <span>${absVal > 0 ? '+' : ''}${fmtNumber(absVal)}</span>`;
    if (pctVal != null && Math.abs(pctVal) < 500) deltaHtml += ` <span style="opacity:.6">(${pctVal > 0 ? '+' : ''}${pctVal.toFixed(1)}%)</span>`;
    deltaHtml += `</span>`;
  } else if (impact.current_value != null) {
    deltaHtml = `<span style="color:var(--color-text-secondary)">${fmtNumber(impact.current_value)}`;
    if (impact.benchmark_tier) deltaHtml += ` <span style="opacity:.6">· ${escapeHtml(impact.benchmark_tier)}</span>`;
    deltaHtml += `</span>`;
  }

  return `<span class="kpi-impact"><span style="color:var(--color-text-muted)">${escapeHtml(impact.kpi_name)}</span>${deltaHtml}</span>`;
}

function confidenceDotsHtml(dots) {
  const filled = (dots.match(/●/g) ?? []).length;
  const unfilled = (dots.match(/○/g) ?? []).length;
  return `<span class="conf-dots" title="Data confidence: ${filled}/${filled + unfilled}"><span class="conf-filled">${'●'.repeat(filled)}</span><span class="conf-empty">${'○'.repeat(unfilled)}</span></span>`;
}

function renderStoryDetailsModal(item, imageUrl) {
  const signalLabel = SIGNAL_LABEL[item.signal_type] ?? item.signal_type.replace(/_/g, ' ').toUpperCase();
  const style = SIGNAL_STYLE[item.signal_type] ?? { bg: '#ffffff18', text: '#ffffff', border: '#ffffff44' };
  const fallbackSrc = `https://placehold.co/144x144/1A1A1A/444444?text=${encodeURIComponent(item.artist_slug)}`;
  const thumbUrl = item.image_url || imageUrl || fallbackSrc;

  const modal = document.createElement('div');
  modal.className = 'story-modal-overlay';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.innerHTML = `
    <div class="story-modal-panel">
      <button class="story-modal-close" aria-label="Close story details">×</button>
      <div class="story-modal-header">
        <img class="story-modal-thumb" src="${escapeHtml(thumbUrl)}" alt="${escapeHtml(item.artist_name)}" width="144" height="144" onerror="this.onerror=null;this.src='${fallbackSrc}'">
        <div class="story-modal-title-wrap">
          <div class="story-modal-badge" style="background:${style.bg};color:${style.text};border:1px solid ${style.border}">${escapeHtml(signalLabel)}</div>
          <h2 class="story-modal-title">${escapeHtml(item.headline)}</h2>
          <div class="story-modal-subtitle">${escapeHtml(item.artist_name)} · ${escapeHtml(item.artist_tier.toUpperCase())}</div>
        </div>
      </div>
      <div class="story-modal-meta">
        <span>${escapeHtml(item.priority ? `Priority ${item.priority}` : 'Priority N/A')}</span>
        <span>${escapeHtml(item.score ? `Score ${item.score}` : 'Score N/A')}</span>
        <span>${escapeHtml(fmtTimestamp(item.timestamp))}</span>
      </div>
      <div class="story-modal-body">
        <p>${escapeHtml(item.summary)}</p>
        <div class="story-modal-details">
          <div class="story-modal-detail-row"><span class="story-modal-label">Source</span><span>${escapeHtml(item.source)}</span></div>
          <div class="story-modal-detail-row"><span class="story-modal-label">Confidence</span><span>${escapeHtml(item.data_confidence)}</span></div>
        </div>
        <div class="story-modal-impact">
          <h3>Impact</h3>
          ${item.kpi_impact.length ? item.kpi_impact.map(impact => `
            <div class="story-modal-impact-item">
              <span class="story-modal-impact-name">${escapeHtml(impact.kpi_name)}</span>
              <span class="story-modal-impact-delta">${escapeHtml(impact.direction === 'up' ? '▲' : impact.direction === 'down' ? '▼' : '—')} ${impact.delta_absolute != null ? `${impact.delta_absolute > 0 ? '+' : ''}${fmtNumber(impact.delta_absolute)}` : ''}${impact.delta_percent != null ? ` (${impact.delta_percent.toFixed(1)}%)` : ''}</span>
            </div>`).join('') : '<p class="story-modal-empty">No KPI impact data available.</p>'}
        </div>
      </div>
    </div>
  `;

  const closeModal = () => {
    document.body.removeChild(modal);
    document.removeEventListener('keydown', onKeyDown);
  };

  const onKeyDown = (event) => {
    if (event.key === 'Escape') closeModal();
  };

  modal.querySelector('.story-modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (event) => {
    if (event.target === modal) closeModal();
  });
  document.addEventListener('keydown', onKeyDown);
  document.body.appendChild(modal);
  modal.querySelector('.story-modal-close').focus();
}

function renderNewsItem(item, imageUrl) {
  const signalLabel = SIGNAL_LABEL[item.signal_type] ?? item.signal_type.replace(/_/g, ' ').toUpperCase();
  const isTop3 = item.priority <= 3;
  const primaryImpact = item.kpi_impact[0] ?? null;
  const fallbackSrc = `https://placehold.co/144x144/1A1A1A/444444?text=${encodeURIComponent(item.artist_slug)}`;
  const style = SIGNAL_STYLE[item.signal_type] ?? { bg: '#ffffff18', text: '#ffffff', border: '#ffffff44' };
  const thumbUrl = item.image_url || imageUrl || fallbackSrc;

  const kpiRow = primaryImpact
    ? `<div class="kpi-impact-row">${item.kpi_impact.slice(0, 3).map(kpiImpactBadgeHtml).join('')}</div>`
    : '';

  const el = document.createElement('article');
  el.className = 'story-card' + (isTop3 ? ' top3' : '');
  el.tabIndex = 0;
  el.setAttribute('role', 'button');
  el.setAttribute('aria-label', `${escapeHtml(item.headline)} story details`);
  el.addEventListener('click', () => renderStoryDetailsModal(item, thumbUrl));
  el.addEventListener('keypress', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      renderStoryDetailsModal(item, thumbUrl);
    }
  });
  el.innerHTML = `
    <div class="story-priority${isTop3 ? ' top3' : ''}"><span>${item.priority}</span></div>
    <img class="story-thumb" src="${escapeHtml(thumbUrl)}" alt="${escapeHtml(item.artist_name)}" width="144" height="144" onerror="this.onerror=null;this.src='${fallbackSrc}'">
    <div class="story-body">
      <div class="story-top-row">
        <span class="signal-badge" style="background:${style.bg};color:${style.text};border:1px solid ${style.border}">${escapeHtml(signalLabel)}</span>
        <span class="story-artist-line">${escapeHtml(item.artist_name)}<span style="opacity:.4;margin:0 6px">·</span>${escapeHtml(item.artist_tier.toUpperCase())}</span>
      </div>
      <h3 class="story-headline${isTop3 ? ' top3' : ''}">${escapeHtml(item.headline)}</h3>
      ${kpiRow}
      <p class="story-summary">${escapeHtml(item.summary)}</p>
      <div class="story-footer">
        <span class="story-footer-item">${fmtTimestamp(item.timestamp)}</span>
        <span class="story-footer-sep">·</span>
        <span class="story-footer-item source" title="${escapeHtml(item.source)}">${escapeHtml(item.source.split(';')[0].trim())}</span>
        <span class="story-footer-sep">·</span>
        ${confidenceDotsHtml(item.data_confidence)}
      </div>
    </div>
  `;
  return el;
}

function renderNewsFeed(briefing, imageBySlug) {
  const el = document.createElement('section');
  const label = document.createElement('div');
  label.className = 'anim-fade-up';
  label.style.animationDelay = '50ms';
  label.innerHTML = `<div class="section-label-row"><h2 class="section-label">TOP STORIES</h2><span class="section-meta">${briefing.items.length} items · ${escapeHtml(briefing.news_date)}</span></div>`;
  el.appendChild(label);

  const list = document.createElement('div');
  list.className = 'story-list';
  briefing.items.forEach((item, i) => {
    const wrap = document.createElement('div');
    wrap.className = 'anim-fade-up';
    wrap.style.animationDelay = `${100 + Math.min(i * 35, 900)}ms`;
    wrap.appendChild(renderNewsItem(item, item.image_url || imageBySlug[item.artist_slug]));
    list.appendChild(wrap);
  });
  el.appendChild(list);
  return el;
}
"""
