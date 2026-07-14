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
    const kpi = Object.fromEntries(a.kpis.map(k => [k.kpi_id, k]));
    const alerts = a.kpis.filter(k => k.alert).map(k => k.alert).join(', ');
    const reach = kpi[1], velocity = kpi[2], eng = kpi[3], spotify = kpi[4],
          spotifyTrend = kpi[5], content = kpi[6], diversity = kpi[7],
          video = kpi[8], recency = kpi[9], press = kpi[10];

    return [
      `${a.artist_name} [${a.tier.toUpperCase()}]`,
      `  Social Reach: ${fmtNumber(reach?.current_value)} (velocity ${velocity?.current_value?.toFixed(1) ?? '—'}% ${velocity?.trend ?? ''})`,
      `  Engagement Rate: ${eng?.current_value?.toFixed(2) ?? '—'}% [${eng?.benchmark_tier ?? '—'}]`,
      `  Spotify Listeners: ${fmtNumber(spotify?.current_value)} (trend ${spotifyTrend?.current_value?.toFixed(1) ?? '—'}%)`,
      `  Content Velocity: ${content?.current_value ?? '—'} posts/week`,
      `  Platform Diversity: ${diversity?.current_value != null ? (diversity.current_value * 100).toFixed(0) : '—'}%`,
      `  Video View Momentum: ${fmtNumber(video?.current_value)}`,
      `  Release Recency: ${recency?.current_value ?? '—'} days ago [${recency?.benchmark_tier ?? '—'}]`,
      `  Press Mentions: ${press?.current_value ?? '—'} articles/week`,
      alerts ? `  ALERTS: ${alerts}` : `  Alerts: none`,
    ].join('\n');
  });

  const newsLines = briefing.items.map(item =>
    `  #${item.priority} ${item.artist_name} [${item.signal_type}] — ${item.headline}\n  → ${item.summary}`,
  );

  const megaArtists   = snapshot.artists.filter(a => a.tier === 'mega').map(a => a.artist_name);
  const majorArtists  = snapshot.artists.filter(a => a.tier === 'major').map(a => a.artist_name);
  const risingArtists = snapshot.artists.filter(a => a.tier === 'rising').map(a => a.artist_name);

  return `You are an embedded AI analyst inside the Sony Music Latin Artist Intelligence Dashboard.
You have access to today's live KPI snapshot for all ${roster.artist_count} artists on the roster.

Snapshot date: ${snapshot.snapshot_date}
Previous snapshot: ${snapshot.previous_snapshot_date}
Total artists: ${roster.artist_count}
Total active alerts: ${snapshot.artists.reduce((n, a) => n + a.kpis.filter(k => k.alert).length, 0)}

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

// ── Streaming API call (browser → Anthropic API directly) ──────────────

async function streamAnswer(apiKey, systemPrompt, messages, onChunk, onDone, onError) {
  let response;
  try {
    response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 2048,
        stream: true,
        system: systemPrompt,
        messages: messages.map(m => ({ role: m.role, content: m.content })),
      }),
    });
  } catch {
    onError('Network error — check your connection.');
    return;
  }

  if (!response.ok) {
    const errText = await response.text().catch(() => response.statusText);
    onError(`API error ${response.status}: ${errText.slice(0, 120)}`);
    return;
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  if (!reader) { onError('No response stream.'); return; }

  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      const raw = line.slice(6).trim();
      if (!raw || raw === '[DONE]') continue;
      try {
        const parsed = JSON.parse(raw);
        if (parsed.type === 'content_block_delta' && parsed.delta?.type === 'text_delta') {
          onChunk(parsed.delta.text);
        }
      } catch { /* ignore malformed SSE lines */ }
    }
  }
  onDone();
}
"""
