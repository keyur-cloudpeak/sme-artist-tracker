"""
Auto-generated from utils.js.

Usage:
    from utils import get_utils_js

    html = f\"\"\"
    <script>
    {get_utils_js()}
    </script>
    \"\"\"
"""

def get_utils() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   Shared formatters, colour tokens, and AI utilities
   (converted from src/lib/ai-utils.ts + inline helpers in each component)
   ══════════════════════════════════════════════════════════════════════ */

// ── Colour tokens ─────────────────────────────────────────────────────
const CLR = {
  up:        '#4ade80',
  down:      '#f87171',
  flat:      '#6b7280',

  mega:      '#fbbf24',
  major:     '#60a5fa',
  rising:    '#a78bfa',
  emerging:  '#34d399',

  reach:     '#60a5fa',
  spotify:   '#4ade80',
  engRate:   '#c084fc',
  release:   '#fbbf24',

  engExcellent: '#4ade80',
  engGood:      '#a3e635',
  engAverage:   '#fbbf24',
  engLow:       '#f87171',

  fresh:  '#4ade80',
  recent: '#fbbf24',
  aging:  '#fb923c',
  dark:   '#f87171',

  alertNeg:  '#f87171',
  alertWarn: '#fbbf24',
  alertPos:  '#4ade80',
};

const KPI_COLOR = {
  1: CLR.reach, 2: CLR.reach, 3: CLR.engRate, 4: CLR.spotify, 5: CLR.spotify,
  6: '#22d3ee', 7: '#2dd4bf', 8: '#f472b6', 9: CLR.release, 10: '#fb923c', 11: '#f87171',
};

const TIER_LABEL = { mega: 'MEGA', major: 'MAJOR', rising: 'RISING', emerging: 'EMERGING' };
const TIER_COLOR = { mega: CLR.mega, major: CLR.major, rising: CLR.rising, emerging: CLR.emerging };
const TIER_DOT_COLOR = { mega: '#fff', major: '#999', rising: '#666', emerging: '#444' };

const DOMAIN_REGISTRY = [
  { id: 'audience', label: 'Audience', description: 'Fan growth, engagement, and audience distribution signals.', color: '#60a5fa' },
  { id: 'streaming', label: 'Streaming', description: 'Streaming consumption and listener momentum.', color: '#4ade80' },
  { id: 'content', label: 'Content', description: 'Publishing cadence, platform mix, and creator activity.', color: '#2dd4bf' },
  { id: 'video', label: 'Video', description: 'Visual content performance and algorithmic reach.', color: '#f472b6' },
  { id: 'catalog', label: 'Catalog', description: 'Release recency and catalog activity signals.', color: '#fbbf24' },
  { id: 'media', label: 'Media', description: 'Press attention and cultural relevance.', color: '#fb923c' },
  { id: 'financial', label: 'Financial', description: 'Revenue, margin, and internal business performance.', color: '#a78bfa' },
  { id: 'contracts', label: 'Contracts', description: 'Deal terms, renewals, obligations, and risk signals.', color: '#34d399' },
];

const DOMAIN_BY_ID = Object.fromEntries(DOMAIN_REGISTRY.map(d => [d.id, d]));

// ── KPI registry ───────────────────────────────────────────────────────

const KPI_REGISTRY = [
  {
    id: 1,
    name: 'Total Social Reach',
    shortName: 'Reach',
    domain: 'audience',
    format: 'number',
    color: CLR.reach,
    invertSort: false,
    narrative: 'Total Social Reach is the headline number for label negotiations and brand partnerships. It represents the combined addressable audience across every platform — the larger the reach, the greater the leverage when pricing sync deals, sponsorships, and touring guarantees.',
    description: 'Sum of followers across all platforms — raw audience size and label leverage.',
  },
  {
    id: 2,
    name: 'Reach Velocity',
    shortName: 'Velocity',
    domain: 'audience',
    format: 'percent',
    color: CLR.reach,
    invertSort: false,
    narrative: 'Reach Velocity is an early-warning signal. A sustained uptick of 2 %+ daily often precedes a breakout moment — an ideal time to increase marketing spend and pitch editorial playlists before the wave crests. A sustained decline signals audience fatigue or platform disengagement that needs A&R attention.',
    description: '% change in total reach vs. prior snapshot — early signal of a breakout or decline.',
  },
  {
    id: 3,
    name: 'Engagement Rate',
    shortName: 'Eng. Rate',
    domain: 'audience',
    format: 'percent',
    color: CLR.engRate,
    invertSort: false,
    narrative: 'Engagement Rate separates authentic fanbases from inflated follower counts. A highly engaged smaller audience will convert to ticket sales and merchandise at far higher rates than a passive mega-following. Use this metric to identify artists who are ready for premium brand integrations.',
    description: 'Likes + comments on recent posts ÷ total followers — quality of audience connection.',
  },
  {
    id: 4,
    name: 'Spotify Monthly Listeners',
    shortName: 'Spotify',
    domain: 'streaming',
    format: 'number',
    color: CLR.spotify,
    invertSort: false,
    narrative: "Spotify Monthly Listeners is the industry's de facto streaming power metric — used by promoters, labels, and sync agents to gauge real-time commercial relevance. Above 20 M qualifies an artist for headliner status on major festival circuits.",
    description: "Industry's standard streaming power metric, pulled directly from Spotify.",
  },
  {
    id: 5,
    name: 'Spotify Listener Trend',
    shortName: 'Spotify Δ',
    domain: 'streaming',
    format: 'percent',
    color: CLR.spotify,
    invertSort: false,
    narrative: 'Spotify Listener Trend measures release impact and streaming momentum. A 20 %+ spike typically indicates a successful new drop or playlist addition. Sustained positive trend over multiple weeks signals genuine catalogue growth — a key argument for increased A&R investment.',
    description: '% change in monthly listeners — measures release impact and streaming momentum.',
  },
  {
    id: 6,
    name: 'Content Velocity',
    shortName: 'Posts/wk',
    domain: 'content',
    format: 'posts',
    color: '#22d3ee',
    invertSort: false,
    narrative: 'Content Velocity tracks how actively an artist is feeding the algorithm. Consistent posting (7–14 pieces per week) sustains platform reach without paid promotion. A sudden drop in velocity is often the earliest observable signal of an artist going inactive or entering a contract dispute.',
    description: 'Posts published across all platforms in the last 7 days — artist activity level.',
  },
  {
    id: 7,
    name: 'Platform Diversity Score',
    shortName: 'Diversity',
    domain: 'content',
    format: 'ratio',
    color: '#2dd4bf',
    invertSort: false,
    narrative: 'Platform Diversity Score measures distribution risk. An artist reliant on a single platform is vulnerable to algorithm changes or account issues. A score above 0.7 indicates a healthy multi-platform presence that protects revenue streams and reaches different demographic segments.',
    description: 'Active platforms ÷ total platforms — flags single-platform dependency risk.',
  },
  {
    id: 8,
    name: 'YouTube Weekly Velocity',
    shortName: 'YT Views',
    domain: 'video',
    format: 'number',
    color: '#f472b6',
    invertSort: false,
    narrative: "YouTube Weekly Velocity captures the visual content engine — the primary driver of new fan acquisition. Average views across the artist's 5 most recent uploads signal whether music video investments are paying off and whether the artist's content is being pushed by YouTube's algorithm. Sustained high values predict streaming uplift weeks before it shows on Spotify.",
    description: 'Average views across the 5 most recent YouTube videos — visual content performance and algorithmic push.',
  },
  {
    id: 9,
    name: 'Latest Release Recency',
    shortName: 'Release',
    domain: 'catalog',
    format: 'recency',
    color: CLR.release,
    invertSort: true,
    narrative: 'Release Recency tracks how fresh the catalogue is in the streaming ecosystem. Artists beyond 120 days without a release see measurable audience retention decay. Cross-checked across Spotify and Apple Music — uses whichever platform indexed the latest drop first. Use this leaderboard in ascending order to identify artists urgently needing a content drop to re-enter the algorithm cycle.',
    description: 'Days since last release on Spotify or Apple Music — flags artists going dark on new material.',
  },
  {
    id: 10,
    name: 'News & Press Mentions',
    shortName: 'Press',
    domain: 'media',
    format: 'articles',
    color: '#fb923c',
    invertSort: false,
    narrative: 'News & Press Mentions quantify cultural relevance beyond owned channels. High press velocity amplifies all other KPIs — streaming, social growth, and engagement all lift when an artist is in the news cycle. Monitor this metric to time campaign activations with organic media momentum.',
    description: 'Unique articles mentioning the artist in the last 7 days — cultural relevance signal.',
  },
  {
    id: 11,
    name: 'Apple Music Catalog Activity',
    shortName: 'AM Releases',
    domain: 'catalog',
    format: 'posts',
    color: '#f87171',
    invertSort: false,
    narrative: "Apple Music Catalog Activity counts the releases — singles, EPs, albums — that landed on iTunes / Apple Music in the last 90 days. Apple's ecosystem skews older and more affluent than Spotify, so a strong cadence here signals reach into the demographics that drive premium pricing for sync, sponsorship, and tour. Pair with KPI 5 (Spotify Listener Trend) to detect platform-asymmetric breakouts.",
    description: "Count of singles / EPs / albums on iTunes in the last 90 days — release cadence on Apple's platform.",
  },
];

const KPI_BY_ID = Object.fromEntries(KPI_REGISTRY.map(k => [k.id, k]));

function getKpiMeta(kpiId) {
  return KPI_BY_ID[kpiId] ?? {
    id: kpiId,
    name: `KPI ${String(kpiId).padStart(2, '0')}`,
    shortName: 'Value',
    domain: 'custom',
    format: 'text',
    color: '#9ca3af',
    invertSort: false,
    narrative: '',
    description: '',
  };
}

function getKpiCount() {
  return KPI_REGISTRY.length;
}

function getDomainMeta(domainId) {
  return DOMAIN_BY_ID[domainId] ?? { id: domainId, label: String(domainId).toUpperCase(), description: '', color: '#9ca3af' };
}

function getKpiColor(kpiId) {
  return getKpiMeta(kpiId).color ?? '#9ca3af';
}

function getDomainCounts() {
  const counts = Object.fromEntries(DOMAIN_REGISTRY.map(d => [d.id, 0]));
  KPI_REGISTRY.forEach(k => { counts[k.domain] = (counts[k.domain] ?? 0) + 1; });
  return counts;
}

function formatKpiValue(kpi) {
  if (!kpi) return '—';
  const meta = getKpiMeta(kpi.kpi_id);
  const v = kpi.current_value;
  if (v === null || v === undefined) return '—';

  switch (meta.format) {
    case 'number':
      return fmtNumber(v);
    case 'percent':
      return `${Number(v).toFixed(2)}%`;
    case 'posts':
      return `${v}`;
    case 'ratio':
      return `${(v * 100).toFixed(0)}%`;
    case 'recency':
      return fmtRecencyDays(v);
    case 'articles':
      return `${v}`;
    default:
      return v.toString();
  }
}

function formatKpiPromptValue(kpi) {
  if (!kpi) return '—';
  const meta = getKpiMeta(kpi.kpi_id);
  const value = formatKpiValue(kpi);
  const parts = [value];
  if (kpi.delta_percent !== null && kpi.delta_percent !== undefined && Math.abs(kpi.delta_percent) < 500) {
    parts.push(`Δ ${fmtDelta(kpi.delta_percent)}`);
  }
  if (kpi.trend) {
    parts.push(`trend ${kpi.trend}`);
  }
  if (kpi.benchmark_tier) {
    parts.push(`[${kpi.benchmark_tier}]`);
  }
  return `${meta.name}: ${parts.join(' ')}`;
}

// ── Formatters ─────────────────────────────────────────────────────────

function fmtNumber(n) {
  if (n === null || n === undefined) return '—';
  if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}B`;
  if (n >= 1_000_000)     return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)         return `${(n / 1_000).toFixed(0)}K`;
  return n.toString();
}

function fmtDelta(pct) {
  if (pct === null || pct === undefined) return '';
  const sign = pct >= 0 ? '+' : '';
  return `${sign}${pct.toFixed(1)}%`;
}

function fmtRecencyDays(days) {
  if (days === null || days === undefined) return '—';
  if (days === 0) return 'today';
  if (days === 1) return '1d ago';
  if (days <= 60) return `${days}d ago`;
  if (days < 365) return `${Math.round(days / 30)}mo ago`;
  return `${(days / 365).toFixed(1)}yr ago`;
}

function recencyColor(days) {
  if (days === null || days === undefined) return '#6b7280';
  if (days <= 14)  return CLR.fresh;
  if (days <= 60)  return CLR.recent;
  if (days <= 180) return CLR.aging;
  return CLR.dark;
}

function engColor(tier) {
  if (!tier) return '#9ca3af';
  const t = tier.toLowerCase();
  if (t === 'excellent') return CLR.engExcellent;
  if (t === 'good')      return CLR.engGood;
  if (t === 'average')   return CLR.engAverage;
  if (t === 'low')       return CLR.engLow;
  return '#9ca3af';
}

function alertColors(label) {
  const l = label.toLowerCase();
  const isNeg  = l.includes('dark') || l.includes('decline') || l.includes('freefall') || l.includes('silence');
  const isWarn = l.includes('caution') || l.includes('overdue') || l.includes('aging');
  if (isNeg)  return { bg: 'rgba(248,113,113,0.12)', text: CLR.alertNeg,  border: 'rgba(248,113,113,0.4)' };
  if (isWarn) return { bg: 'rgba(251,191,36,0.12)',  text: CLR.alertWarn, border: 'rgba(251,191,36,0.4)' };
  return       { bg: 'rgba(74,222,128,0.12)',        text: CLR.alertPos,  border: 'rgba(74,222,128,0.4)' };
}

function fmtTimestamp(iso) {
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffH  = Math.round(diffMs / 3_600_000);
  if (diffH < 1)  return 'just now';
  if (diffH < 24) return `${diffH}h ago`;
  return `${Math.round(diffH / 24)}d ago`;
}

function escapeHtml(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ── Narrative interpreter (from artist-card.tsx) ────────────────────────

function buildNarrative(snapshot) {
  const kpi = Object.fromEntries(snapshot.kpis.map(k => [k.kpi_id, k]));
  const vel     = kpi[2];
  const eng     = kpi[3];
  const spTrend = kpi[5];
  const recency = kpi[9];
  const press   = kpi[10];

  const velPct  = vel?.current_value ?? 0;
  const spPct   = spTrend?.current_value ?? 0;
  const engTier = (eng?.benchmark_tier ?? '').toLowerCase();
  const recDays = recency?.current_value ?? 999;
  const pressN  = press?.current_value ?? 0;
  const tier    = snapshot.tier;

  if (velPct >= 2 && spPct >= 2) {
    return `Dual momentum: social reach and streaming both accelerating. Prioritize marketing spend — the audience is primed for a major campaign.`;
  }
  if (velPct >= 2) {
    return `Social audience growing rapidly. Strong window for brand partnerships and content amplification to capitalise on rising visibility.`;
  }
  if (spPct >= 5) {
    return `Spotify listeners surging. Lean into playlist pitching and editorial outreach now while streaming momentum is at its peak.`;
  }
  if (velPct <= -2 && recDays > 120) {
    return `Declining reach with no recent release. Schedule A&R check-in — artist may need content strategy intervention to reverse audience attrition.`;
  }
  if (spPct <= -5) {
    return `Spotify listeners dropping sharply. Investigate post-release decay or playlist removal; a new single could stabilise streaming performance.`;
  }
  if (engTier === 'excellent' && (tier === 'rising' || tier === 'emerging')) {
    return `Exceptional engagement for their audience size — highly loyal fanbase. Ideal candidate for direct-to-fan campaigns and merchandise activations.`;
  }
  if (engTier === 'low' && (tier === 'mega' || tier === 'major')) {
    return `Audience size is large but engagement is weak, signalling passive fandom. Invest in interactive content and community-building to deepen connection.`;
  }
  if (recDays <= 14) {
    return `New release in active window. Maximise DSP promotion, sync placements, and press coverage while first-week streaming momentum is highest.`;
  }
  if (recDays > 180) {
    return `No new music in over six months. Release pipeline urgency is high — audience retention risk increases significantly beyond the 180-day mark.`;
  }
  if (pressN >= 10) {
    return `High press momentum this week. Amplify PR activity with social content and partner placements to convert media attention into streaming gains.`;
  }
  if (tier === 'mega') {
    return `Performing at expected Mega-tier baseline. Monitor for relative shifts; even modest velocity changes represent significant absolute audience movement.`;
  }
  if (tier === 'major') {
    return `Stable Major-tier performance. Target specific KPI improvements — an engagement or streaming push could trigger breakthrough to Mega status.`;
  }
  if (tier === 'rising') {
    return `Rising-tier artist holding steady. Consistent content output and a new release could accelerate the trajectory toward Major-tier reach.`;
  }
  return `Emerging artist with a developing baseline. Focus on platform consistency and a strong debut release to establish measurable momentum.`;
}

// ── Suggested questions (from ai-utils.ts) ──────────────────────────────

const SUGGESTED_QUESTIONS = [
  { text: 'Who has the highest total social reach on the roster today?',             color: '#60a5fa' },
  { text: 'Which artists are growing fastest right now — and by how much?',          color: '#4ade80' },
  { text: 'Who leads in Spotify monthly listeners, and who is trending up the most?',color: '#fbbf24' },
  { text: 'Are any artists going silent on social media? Should we be concerned?',    color: '#f472b6' },
  { text: "What's the most important story in today's briefing and why?",            color: '#a78bfa' },
  { text: 'Which artists released new music in the past 2 weeks?',                   color: '#22d3ee' },
  { text: 'Who has the best engagement rate — and what does that signal about their fanbase?', color: '#fb923c' },
  { text: 'Which emerging or rising-tier artists have the strongest momentum right now?',       color: '#34d399' },
  { text: 'If you had to flag 3 artists for an urgent A&R conversation, who and why?',          color: '#e879f9' },
  { text: 'Which artists have multiple active KPI alerts — give me the full picture.',           color: '#f87171' },
];

// ── System prompt builder ────────────────────────────────────────────────

function buildSystemPrompt(roster, snapshot, briefing) {
  const artistLines = snapshot.artists.map(a => {
    const kpiById = Object.fromEntries(a.kpis.map(k => [k.kpi_id, k]));
    const summaryKpis = KPI_REGISTRY.map(meta => {
      const kpi = kpiById[meta.id];
      if (!kpi) return `  ${meta.name}: —`;
      return `  ${formatKpiPromptValue(kpi)}`;
    });
    const alerts = a.kpis.filter(k => k.alert).map(k => k.alert).join(', ');

    return [
      `${a.artist_name} [${a.tier.toUpperCase()}]`,
      ...summaryKpis,
      alerts ? `  ALERTS: ${alerts}` : `  Alerts: none`,
    ].join('\n');
  });

  const newsLines = briefing.items.map(item =>
    `  #${item.priority} ${item.artist_name} [${item.signal_type}] — ${item.headline}\n  → ${item.summary}`,
  );

  const megaArtists   = snapshot.artists.filter(a => a.tier === 'mega').map(a => a.artist_name);
  const majorArtists  = snapshot.artists.filter(a => a.tier === 'major').map(a => a.artist_name);
  const risingArtists = snapshot.artists.filter(a => a.tier === 'rising').map(a => a.artist_name);
  const domainSummary = DOMAIN_REGISTRY.map(d => `${d.label}: ${getDomainCounts()[d.id] ?? 0} KPIs`).join(' · ');
  const kpiNames = KPI_REGISTRY.map(k => `${k.id.toString().padStart(2, '0')}. ${k.name} [${getDomainMeta(k.domain).label}]`).join(', ');

  return `You are an embedded AI analyst inside the Sony Music Latin Artist Intelligence Dashboard.
You have access to today's live KPI snapshot for all ${roster.artist_count} artists on the roster.

Snapshot date: ${snapshot.snapshot_date}
Previous snapshot: ${snapshot.previous_snapshot_date}
Total artists: ${roster.artist_count}
Total active alerts: ${snapshot.artists.reduce((n, a) => n + a.kpis.filter(k => k.alert).length, 0)}
KPI registry: ${KPI_REGISTRY.length} metrics (${kpiNames})
Domain registry: ${DOMAIN_REGISTRY.length} business areas (${domainSummary})

ARTIST TIERS:
  Mega (>50M total reach): ${megaArtists.join(', ')}
  Major (10M–50M): ${majorArtists.join(', ')}
  Rising (1M–10M): ${risingArtists.join(', ')}
  Emerging (<1M): remaining artists

═══════════════════════════════════════════
FULL KPI DATA — ALL ARTISTS
═══════════════════════════════════════════
${artistLines.join('\n\n')}

═══════════════════════════════════════════
TODAY'S NEWS BRIEFING (${briefing.news_date})
═══════════════════════════════════════════
${newsLines.join('\n\n')}

INSTRUCTIONS:
- Answer using the real data above — always cite specific numbers.
- Be thorough and detailed. Lead with the most interesting finding.
- When comparing artists, always include tier context.
- Structure answers clearly: use bullet points, numbered lists, or short paragraphs.
- Bold key names and numbers in your answer using **bold** markdown.
- If data is missing (—), acknowledge it rather than guessing.
- You are speaking to Sony Music Latin A&R / marketing staff — use industry language.
- For the dedicated answer page, write a comprehensive answer (300–500 words minimum).`;
}

// streamAnswer is defined in analyst.py — routes via Streamlit postMessage bridge.
"""
