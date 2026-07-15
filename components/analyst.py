def get_analyst() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   AI Analyst chat panel + full-page analyst answer + footer
   (converted from src/components/chat-agent.tsx + analyst-page.tsx)
   ══════════════════════════════════════════════════════════════════════ */

const API_KEY_STORAGE = 'sml-pulse-api-key';
function getApiKey() { return window.INJECTED_API_KEY || localStorage.getItem(API_KEY_STORAGE) || ''; }
function setApiKey(key) { localStorage.setItem(API_KEY_STORAGE, key); }

// ── Markdown-ish answer renderer (from analyst-page.tsx) ────────────────

function inlineFormatted(text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map(part => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return `<strong>${escapeHtml(part.slice(2, -2))}</strong>`;
    }
    return escapeHtml(part);
  }).join('');
}

function renderAnswerHtml(text) {
  if (!text) return '';
  const lines = text.split('\n');
  return lines.map(line => {
    const trimmed = line.trim();
    if (!trimmed) return `<div style="height:8px"></div>`;

    const numMatch = trimmed.match(/^(\d+)[.)]\s+(.+)/);
    if (numMatch) {
      return `<div class="answer-li"><span class="answer-li-num">${numMatch[1]}.</span><p>${inlineFormatted(numMatch[2])}</p></div>`;
    }
    const bulletMatch = trimmed.match(/^[-•*]\s+(.+)/);
    if (bulletMatch) {
      return `<div class="answer-li"><span class="answer-li-bullet">▪</span><p>${inlineFormatted(bulletMatch[1])}</p></div>`;
    }
    if (trimmed.endsWith(':') && trimmed.length < 60) {
      return `<p class="answer-heading">${escapeHtml(trimmed.slice(0, -1))}</p>`;
    }
    return `<p class="answer-p">${inlineFormatted(trimmed)}</p>`;
  }).join('');
}

// ── Chat agent panel ──────────────────────────────────────────────────

function renderChatAgent(roster, snapshot, briefing, onQuestionNavigate) {
  let apiKey = getApiKey();
  let open = true;
  let messages = [];
  let loading = false;

  const systemPrompt = buildSystemPrompt(roster, snapshot, briefing);

  const el = document.createElement('div');
  el.className = 'chat-panel anim-fade-in';

  function send(question) {
    const q = question.trim();
    if (!q || loading || !apiKey) return;

    messages.push({ role: 'user', content: q });
    messages.push({ role: 'assistant', content: '' });
    loading = true;
    render();

    const textarea = el.querySelector('.chat-textarea');
    if (textarea) textarea.value = '';

    let accumulated = '';
    streamAnswer(
      apiKey, systemPrompt, messages.slice(0, -1),
      text => {
        accumulated += text;
        messages[messages.length - 1] = { role: 'assistant', content: accumulated };
        updateHistoryOnly();
      },
      () => { loading = false; render(); },
      errMsg => {
        messages[messages.length - 1] = { role: 'assistant', content: `⚠ ${errMsg}` };
        loading = false;
        render();
      },
    );
  }

  function updateHistoryOnly() {
    const historyEl = el.querySelector('.chat-history');
    if (!historyEl) return;
    historyEl.innerHTML = messages.map((msg, i) => chatMessageHtml(msg, i === messages.length - 1, loading)).join('');
    historyEl.scrollTop = historyEl.scrollHeight;
  }

  function chatMessageHtml(msg, isLatest, loading) {
    const isUser = msg.role === 'user';
    let bodyHtml;
    if (!isUser && isLatest && loading && msg.content === '') {
      bodyHtml = `<span style="display:inline-block;width:8px;height:12px;background:var(--color-text-muted)" class="anim-pulse"></span>`;
    } else {
      const contentHtml = isUser ? escapeHtml(msg.content) : renderAnswerHtml(msg.content);
      const cursorHtml = !isUser && isLatest && loading ? `<span style="margin-left:2px;display:inline-block;width:6px;height:12px;background:var(--color-text-muted)" class="anim-pulse"></span>` : '';
      bodyHtml = isUser ? `<p>${contentHtml}</p>` : `<div class="chat-answer-content">${contentHtml}${cursorHtml}</div>`;
    }
    return `
      <div class="chat-msg ${isUser ? 'user' : 'ai'}">
        <div class="chat-avatar ${isUser ? 'user' : 'ai'}"><span>${isUser ? 'YOU' : 'AI'}</span></div>
        <div class="chat-bubble ${isUser ? 'user' : 'ai'}">${bodyHtml}</div>
      </div>
    `;
  }

  function render() {
    const hasHistory = messages.length > 0;
    const questionsHtml = SUGGESTED_QUESTIONS.map((q, i) => `
      <button class="chat-q-chip" data-q-index="${i}" ${!apiKey ? 'disabled' : ''}
        style="border-color:${q.color}55;color:${q.color}cc"
        onmouseover="if(${!!apiKey}){this.style.borderColor='${q.color}';this.style.color='${q.color}';this.style.background='${q.color}12'}"
        onmouseout="this.style.borderColor='${q.color}55';this.style.color='${q.color}cc';this.style.background='transparent'">
        <span class="chat-q-num" style="color:${q.color}">${String(i + 1).padStart(2, '0')}</span>
        <span>${escapeHtml(q.text)}</span>
      </button>
    `).join('');

    el.innerHTML = `
      <div class="chat-header" id="chat-header-toggle">
        <div class="chat-header-left">
          <span class="chat-live-dot"><span class="chat-live-dot-ping"></span><span class="chat-live-dot-solid"></span></span>
          <span class="chat-title">AI Analyst</span>
          <span class="chat-subtitle">· Click a question for a full-page answer · type below for quick chat</span>
        </div>
        <div class="chat-header-right">
          ${!apiKey ? `<button class="chat-key-badge" id="chat-key-btn">SET API KEY</button>` : `<button class="chat-key-badge" id="chat-key-btn">API KEY SET</button>`}
          ${hasHistory ? `<button class="chat-clear-btn" id="chat-clear-btn">Clear</button>` : ''}
          <span class="chat-caret">${open ? '▲' : '▼'}</span>
        </div>
      </div>
      ${open ? `
        <div>
          ${!apiKey ? `
            <div class="chat-nokey-notice">
              <p>Enter your Anthropic API key to enable the AI analyst (stored only in this browser's local storage).</p>
              <input type="password" id="chat-key-input" placeholder="sk-ant-...">
            </div>
          ` : ''}
          <div class="chat-questions">
            <p class="chat-questions-label">Top questions — click for a dedicated full-page answer ↗</p>
            <div class="chat-q-grid">${questionsHtml}</div>
          </div>
          ${hasHistory ? `<div class="chat-history">${messages.map((m, i) => chatMessageHtml(m, i === messages.length - 1, loading)).join('')}</div>` : ''}
          <div class="chat-input-row">
            <textarea class="chat-textarea" id="chat-textarea" rows="1" placeholder="${apiKey ? 'Type a custom question for a quick inline answer… (Enter to send)' : 'API key required'}" ${!apiKey || loading ? 'disabled' : ''}></textarea>
            <button class="chat-send-btn" id="chat-send-btn" ${loading || !apiKey ? 'disabled' : ''}>${loading ? 'Wait' : 'Send ↵'}</button>
          </div>
        </div>
      ` : ''}
    `;

    el.querySelector('#chat-header-toggle').addEventListener('click', () => { open = !open; render(); });

    const keyBtn = el.querySelector('#chat-key-btn');
    if (keyBtn) keyBtn.addEventListener('click', e => {
      e.stopPropagation();
      const val = prompt('Enter your Anthropic API key (kept only in this browser):', apiKey);
      if (val !== null) { apiKey = val.trim(); setApiKey(apiKey); render(); }
    });

    const keyInput = el.querySelector('#chat-key-input');
    if (keyInput) keyInput.addEventListener('change', e => { apiKey = e.target.value.trim(); setApiKey(apiKey); render(); });

    const clearBtn = el.querySelector('#chat-clear-btn');
    if (clearBtn) clearBtn.addEventListener('click', e => { e.stopPropagation(); messages = []; render(); });

    el.querySelectorAll('.chat-q-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.qIndex, 10);
        onQuestionNavigate(SUGGESTED_QUESTIONS[idx].text);
      });
    });

    const ta = el.querySelector('#chat-textarea');
    if (ta) {
      ta.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(ta.value); }
      });
      ta.addEventListener('input', () => {
        ta.style.height = 'auto';
        ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
      });
    }
    const sendBtn = el.querySelector('#chat-send-btn');
    if (sendBtn) sendBtn.addEventListener('click', () => send(ta ? ta.value : ''));
  }

  render();
  return el;
}

// ── Analyst full-page answer ─────────────────────────────────────────

function renderAnalystPage(question, systemPrompt, snapshotDate, apiKeyGetter, onSelectQuestion) {
  const el = document.createElement('div');
  el.className = 'analyst-page';

  let answer = '';
  let loading = false;
  let error = '';
  let streamToken = 0;

  function startStream() {
    const apiKey = apiKeyGetter();
    if (!question || !apiKey) { render(); return; }

    const myToken = ++streamToken;
    answer = '';
    error = '';
    loading = true;
    render();

    let accumulated = '';
    streamAnswer(
      apiKey, systemPrompt, [{ role: 'user', content: question }],
      text => {
        if (myToken !== streamToken) return;
        accumulated += text;
        answer = accumulated;
        updateAnswerOnly();
      },
      () => { if (myToken === streamToken) { loading = false; render(); } },
      msg => { if (myToken === streamToken) { error = msg; loading = false; render(); } },
    );
  }

  function updateAnswerOnly() {
    const area = el.querySelector('.analyst-answer-area');
    if (area) area.innerHTML = answerAreaHtml();
  }

  function answerAreaHtml() {
    if (loading && !answer) {
      return `<div class="analyst-loading"><span class="analyst-loading-dot"></span><span class="analyst-loading-label">Analysing data…</span></div>`;
    }
    if (error) {
      return `<p class="analyst-error">⚠ ${escapeHtml(error)}</p>`;
    }
    if (answer) {
      return `<div>${renderAnswerHtml(answer)}${loading ? `<span class="analyst-cursor"></span>` : ''}</div>`;
    }
    return '';
  }

  function render() {
    if (!question) {
      el.innerHTML = `
        <div class="analyst-empty">
          <p>No question selected</p>
          <p>Click any question in the AI Analyst panel to see a full answer here.</p>
        </div>
      `;
      return;
    }

    const selectedIndex = SUGGESTED_QUESTIONS.findIndex(q => q.text === question);
    const trayHtml = SUGGESTED_QUESTIONS.map((q, i) => {
      const isActive = q.text === question;
      return `
        <button class="analyst-tray-chip" data-tray-index="${i}" ${loading ? 'disabled' : ''}
          style="border-color:${isActive ? q.color : q.color + '44'};background:${isActive ? q.color + '18' : 'transparent'};color:${isActive ? q.color : q.color + '99'}">
          <span class="analyst-tray-num" style="color:${q.color}">${String(i + 1).padStart(2, '0')}</span>
          <span class="analyst-tray-text">${escapeHtml(q.text)}</span>
        </button>
      `;
    }).join('');

    el.innerHTML = `
      <div class="analyst-header">
        <div>
          <p class="analyst-date-label">Data valid for</p>
          <p class="analyst-date-value">${escapeHtml(snapshotDate)}</p>
        </div>
      </div>
      <div class="analyst-question-block" style="border-color:${selectedIndex >= 0 ? SUGGESTED_QUESTIONS[selectedIndex].color + '66' : '#333'}">
        <p class="analyst-q-eyebrow">AI Analyst · Question ${selectedIndex >= 0 ? String(selectedIndex + 1).padStart(2, '0') : '—'} of ${SUGGESTED_QUESTIONS.length}</p>
        <h1 class="analyst-q-title" style="color:${selectedIndex >= 0 ? SUGGESTED_QUESTIONS[selectedIndex].color : '#ffffff'}">${escapeHtml(question)}</h1>
      </div>
      <div class="analyst-answer-area">${answerAreaHtml()}</div>
      <div class="analyst-tray">
        <p class="analyst-tray-label">Other questions — click to switch</p>
        <div class="analyst-tray-row">${trayHtml}</div>
      </div>
    `;

    el.querySelectorAll('.analyst-tray-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.trayIndex, 10);
        onSelectQuestion(SUGGESTED_QUESTIONS[idx].text);
      });
    });
  }

  render();
  if (question && apiKeyGetter()) startStream();

  el.refreshQuestion = function (newQuestion) {
    question = newQuestion;
    startStream();
  };

  return el;
}

// ── Footer ────────────────────────────────────────────────────────────

function renderFooter(roster, snapshot) {
  const el = document.createElement('footer');
  el.className = 'footer';
  el.innerHTML = `
    <div class="footer-row">
      <div>
        <p class="footer-label">Last Refreshed</p>
        <p class="footer-value">${escapeHtml(snapshot.snapshot_date)} · prev ${escapeHtml(snapshot.previous_snapshot_date)}</p>
      </div>
      <div>
        <p class="footer-label">Data Sources</p>
        <p class="footer-value small">Social aggregators · Spotify (direct) · YouTube · Press search</p>
      </div>
      <div>
        <p class="footer-label">Version</p>
        <p class="footer-value small">Sony Latin Pulse v0.1 · ${roster.artist_count} artists · 11 KPIs</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span class="footer-wordmark">SONY LATIN PULSE</span>
      <span class="footer-copyright">© Sony Music Entertainment</span>
    </div>
    <div class="footer-attribution">
      <span class="powered-by">Powered by</span>
      <span class="chromadata">CHROMADATA</span>
      <span class="powered-by">· Artist Intelligence Solutions</span>
    </div>
  `;
  return el;
}
"""
