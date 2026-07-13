/* ============================================================
 * page-ask-ai.js — chat-style data Q&A over the loaded dashboard data
 * ------------------------------------------------------------
 * The LLM is given a system prompt injected with:
 *   - Last 7 days summary (totals, sentiment, top users/channels/keywords)
 *   - 30-day trend
 *   - Per-platform latest day breakdown
 *   - Top 10 hot messages from the last 7 days
 *   - Keyword-search results from all_messages (last 30 days), top 30
 *
 * This grounding prevents the LLM from hallucinating numbers and lets
 * it answer "what did X say about Y?" with actual quotes.
 *
 * Requires:
 *   - llm-client.js loaded BEFORE this file
 *   - state.js loaded (defines STATE, Utils, getDaysDataForDate)
 *   - The data/ JSONs already loaded via loadAllData() before the user
 *     navigates to this page
 * ============================================================ */
const PageAskAI = {
  history: [],
  displayHistory: [],
  STORAGE_KEY: 'ask_ai_history',

  _save() {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify({
        history: this.history,
        displayHistory: this.displayHistory,
      }));
    } catch (e) { /* quota exceeded, ignore */ }
  },

  _load() {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      if (raw) {
        const data = JSON.parse(raw);
        this.history = Array.isArray(data.history) ? data.history : [];
        this.displayHistory = Array.isArray(data.displayHistory) ? data.displayHistory : [];
      }
    } catch (e) {
      this.history = [];
      this.displayHistory = [];
    }
  },

  render(main) {
    main.innerHTML = `
      <div class="breadcrumb">控制台 / 数据问答</div>
      <h1>数据问答 <span class="badge-ai" style="font-size:11px;vertical-align:middle;">AI</span></h1>
      <div class="page-subtitle">对话式数据问答 · 基于站内真实数据 · 回答语言跟随提问</div>

      <div class="chat-wrap">
        <div class="chat-history" id="chat-history">
          <div class="chat-msg ai">
            <div class="chat-bubble">
              <strong>你好 👋 我是你的数据助手</strong><br/><br/>
              我可以基于站内数据回答你的问题，比如：<br/>
              • 最近一周消息量趋势如何？<br/>
              • 哪个频道最活跃？<br/>
              • 情感分布有什么变化？<br/>
              • 用户 X 都在聊什么？<br/>
              • 有没有异常波动？<br/><br/>
              <em style="color:var(--text-sub);font-size:12px;">你可以用中文或英文提问，我会用相同的语言回答。</em>
            </div>
          </div>
        </div>
        <div class="chat-suggestions" id="chat-suggestions">
          <div class="chat-suggestion" data-q="过去7天消息量趋势如何？">📊 过去7天消息量趋势如何？</div>
          <div class="chat-suggestion" data-q="Which channel is most active?">💬 Which channel is most active?</div>
          <div class="chat-suggestion" data-q="情感分布有什么变化？">❤️ 情感分布有什么变化？</div>
          <div class="chat-suggestion" data-q="有没有异常波动？">⚠ 有没有异常波动？</div>
        </div>
        <div class="chat-input-wrap">
          <input type="text" class="chat-input" id="chat-input" placeholder="问点什么…（Enter 发送）" autocomplete="off" />
          <button class="btn" id="chat-send">发送</button>
          <button class="btn ghost" id="chat-clear" title="清空对话">🗑</button>
        </div>
      </div>
    `;

    document.getElementById('chat-send').onclick = () => PageAskAI.send();
    document.getElementById('chat-clear').onclick = () => PageAskAI.clear();
    document.getElementById('chat-input').addEventListener('keydown', e => {
      if (e.key === 'Enter') PageAskAI.send();
    });
    document.querySelectorAll('.chat-suggestion').forEach(el => {
      el.addEventListener('click', () => {
        document.getElementById('chat-input').value = el.dataset.q;
        PageAskAI.send();
      });
    });

    PageAskAI._load();
    PageAskAI.displayHistory.forEach(m => PageAskAI._appendBubble(m.role, m.html, false));
    const h0 = document.getElementById('chat-history');
    if (h0) h0.scrollTop = h0.scrollHeight;
  },

  clear() {
    PageAskAI.history = [];
    PageAskAI.displayHistory = [];
    localStorage.removeItem(PageAskAI.STORAGE_KEY);
    const h = document.getElementById('chat-history');
    const welcome = h.querySelector('.chat-msg.ai');
    h.innerHTML = '';
    if (welcome) h.appendChild(welcome);
  },

  async send() {
    const input = document.getElementById('chat-input');
    const q = input.value.trim();
    if (!q) return;
    input.value = '';

    PageAskAI._appendBubble('user', Utils.esc(q));
    PageAskAI.history.push({ role: 'user', content: q });
    PageAskAI.displayHistory.push({ role: 'user', html: Utils.esc(q) });

    const thinkingBubble = PageAskAI._appendBubble('ai', '<span style="opacity:0.6">思考中…</span>');
    const bubbleEl = thinkingBubble.querySelector('.chat-bubble');

    try {
      const systemPrompt = PageAskAI.buildSystemPrompt(q);
      const messages = [
        { role: 'system', content: systemPrompt },
        ...PageAskAI.history.slice(-20)
      ];

      const result = await LLMClient.streamChat(messages, (chunk) => {
        bubbleEl.innerHTML = PageAskAI.renderMarkdown(chunk);
      });

      PageAskAI.history.push({ role: 'assistant', content: result });
      PageAskAI.displayHistory.push({ role: 'ai', html: PageAskAI.renderMarkdown(result) });
      PageAskAI._save();

      const metaEl = thinkingBubble.querySelector('.meta');
      const searchInfo = PageAskAI._lastSearchCount !== undefined
        ? ` · 检索到 ${PageAskAI._lastSearchCount} 条相关消息` : '';
      if (metaEl) metaEl.textContent = `由 AI 生成 · ${new Date().toLocaleTimeString()}${searchInfo}`;
      else {
        const meta = document.createElement('div');
        meta.className = 'meta';
        meta.textContent = `由 AI 生成 · ${new Date().toLocaleTimeString()}${searchInfo}`;
        thinkingBubble.appendChild(meta);
      }
    } catch (err) {
      console.error('Ask AI error:', err);
      bubbleEl.innerHTML = `<span style="color:#f87171;">请求失败：${Utils.esc(err.message || '未知错误')}</span>`;
    }

    const h = document.getElementById('chat-history');
    h.scrollTop = h.scrollHeight;
  },

  // ----- System prompt construction -----

  buildSystemPrompt(userQuery) {
    const idx = STATE.index;
    if (!idx || !idx.days) return '你是一个数据分析助手。暂无数据。';

    const days = idx.days;
    const latest = days[days.length - 1];
    const range7 = days.slice(-7);
    const range30 = days.slice(-30);
    const getData = (typeof getDaysDataForDate === 'function')
      ? getDaysDataForDate
      : (date) => STATE.daysData[date];

    const sumField = (arr, f) => arr.reduce((s, d) => s + (d[f] || 0), 0);

    // Aggregate 7-day summary
    let total7 = sumField(range7, 'total_messages');
    let pos7 = 0, neg7 = 0, neu7 = 0, fb7 = 0;
    const users7 = {}, channels7 = {}, keywords7 = {};
    const topMsgs7 = [];

    range7.forEach(meta => {
      const data = getData(meta.date);
      if (!data) return;
      pos7 += data.positive || 0;
      neg7 += data.negative || 0;
      neu7 += data.neutral || 0;
      fb7 += data.feedback || 0;
      Object.entries(data.active_users || {}).forEach(([u, c]) => users7[u] = (users7[u] || 0) + c);
      Object.entries(data.channels || {}).forEach(([ch, c]) => channels7[ch] = (channels7[ch] || 0) + c);
      Object.entries(data.keywords || {}).forEach(([kw, c]) => keywords7[kw] = (keywords7[kw] || 0) + c);
      if (data.top_messages && typeof data.top_messages === 'object') {
        Object.values(data.top_messages).forEach(arr => {
          if (Array.isArray(arr)) arr.forEach(m => topMsgs7.push({ ...m, date: meta.date, platform: data.platform }));
        });
      }
    });

    const topUsers = Object.entries(users7).sort((a, b) => b[1] - a[1]).slice(0, 15);
    const topChannels = Object.entries(channels7).sort((a, b) => b[1] - a[1]).slice(0, 15);
    const topKeywords = Object.entries(keywords7).sort((a, b) => b[1] - a[1]).slice(0, 20);
    const trend30 = range30.map(d => ({ date: d.date, msgs: d.total_messages }));

    // Per-platform latest
    const platformInfo = [];
    if (STATE.platformDaysData && latest) {
      const latestPlatforms = STATE.platformDaysData[latest.date] || {};
      Object.entries(latestPlatforms).forEach(([plat, data]) => {
        platformInfo.push({
          platform: plat,
          total_messages: data.total_messages || 0,
          positive: data.positive || 0,
          negative: data.negative || 0,
          neutral: data.neutral || 0,
          active_users: Object.keys(data.active_users || {}).length,
        });
      });
    }

    // Keyword search over all_messages, last 30 days
    let relevantSection = '';
    let searchResultCount = 0;
    if (userQuery) {
      const searchResults = PageAskAI.searchMessages(userQuery, 30);
      searchResultCount = searchResults.length;
      if (searchResults.length > 0) {
        relevantSection = `\n\n【与提问相关的消息检索（共${searchResults.length}条，请优先基于这些检索结果回答）】\n` +
          searchResults.map((m, i) => {
            const src = m.video_title_full ? `[video: ${Utils.truncate(m.video_title_full, 50)}]` :
                        m.post_title ? `[post: ${Utils.truncate(m.post_title, 50)}]` :
                        `[${m.channel || m.platform || '?'}]`;
            return `  ${i + 1}. [${m.date}] ${src} ${m.author || '匿名'}: "${Utils.truncate(m.content, 200)}"${m.likes ? ` (likes:${m.likes})` : ''}`;
          }).join('\n');
      } else {
        relevantSection = '\n\n【与提问相关的消息检索：未找到匹配消息】';
      }
    }
    PageAskAI._lastSearchCount = searchResultCount;

    return `你是一个社区数据分析师助手。基于以下站内真实数据回答用户问题。
重要规则：
1. 只基于提供的数据回答，不要编造数据
2. 如果数据不足以回答，明确说明缺什么数据
3. 回答语言跟随用户提问的语言
4. 可以做数据解读和趋势分析，但要标注是分析推断而非原始数据
5. 涉及具体消息内容时，引用原文（不要翻译）
6. **最重要**：如果"与提问相关的消息检索"部分有内容，你必须优先基于这些检索到的原始消息来回答，直接引用玩家原话

--- 数据摘要 ---

数据时间范围: ${days[0].date} ~ ${latest.date}（共 ${days.length} 天）
数据平台: ${(idx.platforms || []).join(', ') || 'unknown'}

【最近7天汇总】
总消息量: ${total7}
情感: 正面${pos7} / 中性${neu7} / 负面${neg7} / 反馈${fb7}
独立活跃用户: ${topUsers.length}

Top 15 活跃用户:
${topUsers.map(([u, c], i) => `  ${i + 1}. ${u}: ${c}条`).join('\n')}

Top 15 频道:
${topChannels.map(([ch, c], i) => `  ${i + 1}. ${ch}: ${c}条`).join('\n')}

Top 20 关键词:
${topKeywords.map(([kw, c], i) => `  ${i + 1}. ${kw}: ${c}次`).join('\n')}

精选消息（最近7天 Top 10）:
${topMsgs7.sort((a, b) => (b.likes || 0) - (a.likes || 0)).slice(0, 10).map((m, i) => `  ${i + 1}. [${m.date}] [${m.channel || m.platform || '?'}] ${m.author || '匿名'}: "${Utils.truncate(m.content, 120)}" (likes:${m.likes || 0})`).join('\n')}

【30天消息量趋势】
${trend30.map(d => `${d.date}: ${d.msgs}`).join(', ')}

【各平台最新日数据】
${platformInfo.length > 0 ? platformInfo.map(p => `${p.platform}: ${p.total_messages}消息, ${p.active_users}活跃用户, 正面${p.positive}/负面${p.negative}/中性${p.neutral}`).join('\n') : '暂无分平台数据'}
${relevantSection}`;
  },

  // ----- Keyword search over all_messages (last 30 days) -----

  searchMessages(query, limit = 30) {
    const idx = STATE.index;
    if (!idx || !idx.days) return [];

    const stopWords = new Set([
      '的','了','在','是','我','有','和','就','不','人','都','一','上','也','很','到','说','要','去','你','会','着','看','好','这','那','他','她','它','们','吗','呢','吧','啊','哦','什么','怎么','如何','有没有','能不能','最近','关于','情况',
      'the','a','an','is','are','was','were','be','been','have','has','had','do','does','did','will','would','could','should','can','may','might','to','of','in','for','on','with','at','by','from','as','into','through','and','but','or','not','so','very','just','about','how','what','which','who','when','where','why','this','that','i','me','my','we','our','you','your','he','she','it','its','they','them','their','like',
    ]);

    const words = query.toLowerCase()
      .replace(/[？?！!，,。.、；;：:""''（）()【】\[\]{}<>《》\/\\@#$%^&*+=~`|]/g, ' ')
      .split(/\s+/)
      .flatMap(w => {
        // Split CJK/Latin boundaries
        const parts = [];
        let buf = '';
        let lastIsCjk = null;
        for (const ch of w) {
          const isCjk = /[\u4e00-\u9fff\u3400-\u4dbf]/.test(ch);
          if (lastIsCjk !== null && isCjk !== lastIsCjk) {
            if (buf) parts.push(buf);
            buf = ch;
          } else {
            buf += ch;
          }
          lastIsCjk = isCjk;
        }
        if (buf) parts.push(buf);
        // Expand long CJK into 2-char windows for better recall
        const expanded = [];
        parts.forEach(p => {
          if (/[\u4e00-\u9fff]/.test(p) && p.length > 4) {
            expanded.push(p);
            for (let i = 0; i < p.length - 1; i++) expanded.push(p.slice(i, i + 2));
          } else {
            expanded.push(p);
          }
        });
        return expanded;
      })
      .filter(w => w.length >= 2 && !stopWords.has(w));

    const uniqueWords = [...new Set(words)];
    if (uniqueWords.length === 0) return [];

    const range = idx.days.slice(-30);
    const results = [];
    const seenKeys = new Set();

    range.forEach(meta => {
      const date = meta.date;
      if (!STATE.platformDaysData || !STATE.platformDaysData[date]) return;
      Object.entries(STATE.platformDaysData[date]).forEach(([plat, pData]) => {
        if (!pData || !Array.isArray(pData.all_messages)) return;
        pData.all_messages.forEach(m => {
          const text = ((m.content || '') + ' ' + (m.video_title_full || '') + ' ' + (m.post_title || '')).toLowerCase();
          let matchCount = 0;
          uniqueWords.forEach(w => { if (text.includes(w)) matchCount++; });
          if (matchCount > 0) {
            const dedupeKey = `${date}|${plat}|${(m.content || '').slice(0, 80)}`;
            if (seenKeys.has(dedupeKey)) return;
            seenKeys.add(dedupeKey);
            results.push({ ...m, date, platform: plat, _matchCount: matchCount });
          }
        });
      });
    });

    results.sort((a, b) => b._matchCount - a._matchCount || (b.likes || 0) - (a.likes || 0));
    return results.slice(0, limit);
  },

  // ----- Minimal Markdown rendering -----

  renderMarkdown(text) {
    if (!text) return '';
    let html = Utils.esc(text);
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    html = html.replace(/`([^`]+)`/g, '<code style="background:#f3f4f6;padding:1px 4px;border-radius:3px;font-size:12px;">$1</code>');
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/\n/g, '<br/>');
    return html;
  },

  // ----- DOM helpers -----

  _appendBubble(role, html, scroll = true) {
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.innerHTML = `<div class="chat-bubble">${html}</div>` +
      (role === 'ai' ? `<div class="meta">思考中…</div>` : '');
    const h = document.getElementById('chat-history');
    h.appendChild(div);
    if (scroll) h.scrollTop = h.scrollHeight;
    return div;
  },
};
