def get_frontend() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   App entry point — data loading + tab orchestration
   (converted from src/App.tsx + src/main.tsx + src/data/loader.ts)
   ══════════════════════════════════════════════════════════════════════ */

(async function main() {
  const root = document.getElementById('root');

  // ── Load data (equivalent to src/data/loader.ts) ──────────────────
  let roster, snapshot, briefing, kpiSample;
  try {
    [roster, snapshot, briefing, kpiSample] = await Promise.all([
      window.INJECTED_ROSTER ? Promise.resolve(window.INJECTED_ROSTER) : fetch('data/roster.json').then(r => r.json()),
      window.INJECTED_SNAPSHOT ? Promise.resolve(window.INJECTED_SNAPSHOT) : fetch('data/snapshot.json').then(r => r.json()),
      window.INJECTED_NEWS ? Promise.resolve(window.INJECTED_NEWS) : fetch('data/news.json').then(r => r.json()),
      window.INJECTED_KPI_SAMPLE ? Promise.resolve(window.INJECTED_KPI_SAMPLE) : fetch('data/kpi_12_20_sample.json').then(async r => {
        if (!r.ok) return null;
        const t = await r.text();
        try { return JSON.parse(t); } catch (e) { return null; }
      }),
    ]);
  } catch (err) {
    root.innerHTML = `<div style="padding:2rem;font-family:monospace;color:#f87171">Failed to load data files: ${escapeHtml(err.message)}</div>`;
    return;
  }

  // Merge optional external KPI sample into snapshot artists (add or replace KPIs by id)
  if (kpiSample && Array.isArray(kpiSample.artists)) {
    const sampleBySlug = Object.fromEntries(kpiSample.artists.map(a => [a.artist_slug, a]));
    snapshot.artists = snapshot.artists.map(a => {
      const s = sampleBySlug[a.artist_slug];
      if (!s || !Array.isArray(s.kpis)) return a;
      const existing = Object.fromEntries(a.kpis.map(k => [k.kpi_id, k]));
      s.kpis.forEach(sk => { existing[sk.kpi_id] = sk; });
      a.kpis = Object.values(existing).sort((x, y) => x.kpi_id - y.kpi_id);
      return a;
    });
  }

  const snapshotBySlug = Object.fromEntries(snapshot.artists.map(a => [a.artist_slug, a]));
  const imageBySlug = Object.fromEntries(roster.artists.map(a => [a.slug, a.image_url]));
  const systemPrompt = buildSystemPrompt(roster, snapshot, briefing);

  // ── App state ───────────────────────────────────────────────────
  const state = {
    activeTab: 'stories',
    selectedQuestion: '',
    theme: getInitialTheme(),
    roster: { tierFilter: 'all', searchQuery: '' },
  };
  applyTheme(state.theme);

  function setActiveTab(tab) { state.activeTab = tab; renderApp(); }
  function setRosterState(next) { state.roster = next; renderApp(); }
  function handleQuestionNavigate(question) {
    state.selectedQuestion = question;
    state.activeTab = 'analyst';
    renderApp();
  }

  // ── Layout skeleton ─────────────────────────────────────────────
  root.innerHTML = '';
  const container = document.createElement('div');
  container.className = 'min-h-screen';
  root.appendChild(container);

  const mastheadSlot = document.createElement('div');
  container.appendChild(mastheadSlot);

  const tickerSlot = document.createElement('div');
  container.appendChild(tickerSlot);

  const tabContentWrap = document.createElement('div');
  tabContentWrap.className = 'tab-content';
  container.appendChild(tabContentWrap);

  const tabNavSlot = document.createElement('div');
  tabContentWrap.appendChild(tabNavSlot);

  const bodySlot = document.createElement('div');
  tabContentWrap.appendChild(bodySlot);

  const divider = document.createElement('div');
  divider.className = 'divider';
  tabContentWrap.appendChild(divider);

  const footerSlot = document.createElement('div');
  tabContentWrap.appendChild(footerSlot);

  // ── Static-ish sections (masthead / ticker / footer don't change) ──
  function renderStatic() {
    mastheadSlot.innerHTML = '';
    const masthead = renderMasthead(snapshot);
    mastheadSlot.appendChild(masthead);
    const toggleSlot = masthead.querySelector('#theme-toggle-slot');
    toggleSlot.appendChild(renderThemeToggle(state.theme, () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(state.theme);
      renderStatic();
    }));

    tickerSlot.innerHTML = '';
    tickerSlot.appendChild(renderNewsTicker(briefing, imageBySlug));

    footerSlot.innerHTML = '';
    footerSlot.appendChild(renderFooter(roster, snapshot));
  }

  // ── Tab body ────────────────────────────────────────────────────
  function renderApp() {
    tabNavSlot.innerHTML = '';
    tabNavSlot.appendChild(renderTabNav(state.activeTab, {
      stories: briefing.items.length,
      roster: roster.artist_count,
      leaderboards: getKpiCount(),
    }, setActiveTab));

    bodySlot.innerHTML = '';

    if (state.activeTab === 'overview') {
      bodySlot.appendChild(renderOverview(roster, snapshot, briefing));
    } else if (state.activeTab === 'stories') {
      bodySlot.appendChild(renderNewsFeed(briefing, imageBySlug));
    } else if (state.activeTab === 'roster') {
      bodySlot.appendChild(renderRosterGrid(roster, snapshotBySlug, state.roster, setRosterState));
    } else if (state.activeTab === 'leaderboards') {
      bodySlot.appendChild(renderLeaderboards(snapshot));
    } else if (state.activeTab === 'analyst') {
      const chat = renderChatAgent(roster, snapshot, briefing, handleQuestionNavigate);
      bodySlot.appendChild(chat);
      const analyst = renderAnalystPage(
        state.selectedQuestion, systemPrompt, snapshot.snapshot_date,
        handleQuestionNavigate,
      );
      bodySlot.appendChild(analyst);
    }
  }

  renderStatic();
  renderApp();
})();
"""
