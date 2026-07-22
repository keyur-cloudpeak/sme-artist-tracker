def get_analyst() -> str:
    return r"""/* ══════════════════════════════════════════════════════════════════════
   AI Analyst chat panel + full-page analyst answer + footer
   (converted from src/components/chat-agent.tsx + analyst-page.tsx)
   ══════════════════════════════════════════════════════════════════════ */

// ── FastAPI backend bridge ─────────────────────────────────────────────────
// Calls the FastAPI server running on http://localhost:8000/chat

function streamAnswer(proxyUrl, systemPrompt, messages, onChunk, onDone, onError) {
  const payload = {
    system_prompt: systemPrompt,
    messages: messages,
  };

  fetch('https://sme-scraper.vercel.app/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(async response => {
    if (!response.ok) {
      const err = await response.text();
      onError(err);
      return;
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      onChunk(decoder.decode(value, { stream: true }));
    }
    onDone();
  })
  .catch(err => {
    onError(err.toString());
  });
}

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

    const numMatch = trimmed.match(/^(\d+)[.)]\\s+(.+)/);
    if (numMatch) {
      return `<div class="answer-li"><span class="answer-li-num">${numMatch[1]}.</span><p>${inlineFormatted(numMatch[2])}</p></div>`;
    }
    const bulletMatch = trimmed.match(/^[-•*]\\s+(.+)/);
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

function renderChatAgent(roster, snapshot, briefing, onQuestionNavigate, title, questions, systemPrompt) {
  let open = true;
  let messages = [];
  let loading = false;

  const prompt = systemPrompt || buildSystemPrompt(roster, snapshot, briefing);
  const questionSet = questions || SUGGESTED_QUESTIONS;

  const el = document.createElement('div');
  el.className = 'chat-panel anim-fade-in';

  function send(question) {
    const q = question.trim();

    if (!q || loading) return;

    messages.push({ role: 'user', content: q });
    messages.push({ role: 'assistant', content: '' });
    loading = true;
    render();

    const textarea = el.querySelector('.chat-textarea');
    if (textarea) textarea.value = '';

    let accumulated = '';
    streamAnswer(
      '', prompt, messages.slice(0, -1),
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
    const questionsHtml = questionSet.map((q, i) => `
      <button class="chat-q-chip" data-q-index="${i}"
        style="border-color:${q.color}55;color:${q.color}cc"
        onmouseover="this.style.borderColor='${q.color}';this.style.color='${q.color}';this.style.background='${q.color}12'"
        onmouseout="this.style.borderColor='${q.color}55';this.style.color='${q.color}cc';this.style.background='transparent'">
        <span class="chat-q-num" style="color:${q.color}">${String(i + 1).padStart(2, '0')}</span>
        <span>${escapeHtml(q.text)}</span>
      </button>
    `).join('');

    el.innerHTML = `
      <div class="chat-header" id="chat-header-toggle">
        <div class="chat-header-left">
          <span class="chat-live-dot"><span class="chat-live-dot-ping"></span><span class="chat-live-dot-solid"></span></span>
          <span class="chat-title">${escapeHtml(title)}</span>
          <span class="chat-subtitle">· Click a question for a full-page answer · type below for quick chat</span>
        </div>
        <div class="chat-header-right">
          ${hasHistory ? `<button class="chat-clear-btn" id="chat-clear-btn">Clear</button>` : ''}
          <span class="chat-caret">${open ? '▲' : '▼'}</span>
        </div>
      </div>
      ${open ? `
        <div>
          <div class="chat-questions">
            <p class="chat-questions-label">Top questions — click for a dedicated full-page answer ↗</p>
            <div class="chat-q-grid">${questionsHtml}</div>
          </div>
          ${hasHistory ? `<div class="chat-history">${messages.map((m, i) => chatMessageHtml(m, i === messages.length - 1, loading)).join('')}</div>` : ''}
          <div class="chat-input-row">
            <textarea class="chat-textarea" id="chat-textarea" rows="1" placeholder="${loading ? 'Waiting…' : 'Type a custom question for a quick inline answer… (Enter to send)'}" ${loading ? 'disabled' : ''}></textarea>
            <button class="chat-send-btn" id="chat-send-btn" ${loading ? 'disabled' : ''}>${loading ? 'Wait' : 'Send ↵'}</button>
          </div>
        </div>
      ` : ''}
    `;

    el.querySelector('#chat-header-toggle').addEventListener('click', () => { open = !open; render(); });

    const clearBtn = el.querySelector('#chat-clear-btn');
    if (clearBtn) clearBtn.addEventListener('click', e => { e.stopPropagation(); messages = []; render(); });

    el.querySelectorAll('.chat-q-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.qIndex, 10);
        onQuestionNavigate(questionSet[idx].text);
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

function renderAnalystPage(question, systemPrompt, snapshotDate, onSelectQuestion, title, questions) {
  const el = document.createElement('div');
  el.className = 'analyst-page';

  let answer = '';
  let loading = false;
  let error = '';
  let streamToken = 0;

  function startStream() {
    if (!question) { render(); return; }

    const myToken = ++streamToken;
    answer = '';
    error = '';
    loading = true;
    render();

    let accumulated = '';
    streamAnswer(
      '', systemPrompt, [{ role: 'user', content: question }],
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

    const selectedIndex = questions.findIndex(q => q.text === question);
    const trayHtml = questions.map((q, i) => {
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
      <div class="analyst-question-block" style="border-color:${selectedIndex >= 0 ? questions[selectedIndex].color + '66' : '#333'}">
        <p class="analyst-q-eyebrow">${escapeHtml(title)} · Question ${selectedIndex >= 0 ? String(selectedIndex + 1).padStart(2, '0') : '—'} of ${questions.length}</p>
        <h1 class="analyst-q-title" style="color:${selectedIndex >= 0 ? questions[selectedIndex].color : '#ffffff'}">${escapeHtml(question)}</h1>
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
        onSelectQuestion(questions[idx].text);
      });
    });
  }

  render();
  if (question) startStream();

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