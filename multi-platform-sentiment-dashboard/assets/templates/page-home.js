/* ============================================================
 * page-home.js — Reference Aggregate Page
 * ============================================================
 * Cross-platform overview: KPIs + trend + channels + keywords + top messages.
 * This is the page everyone sees first.
 * ============================================================ */

const PageHome = {
  async render(main) {
    main.innerHTML = `
      <div class="breadcrumb">舆情分析 / 舆情总览</div>
      <h1>舆情总览</h1>
      <div class="page-subtitle">跨平台社区舆情聚合分析</div>

      <div id="home-kpi-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;"></div>

      <div class="card" style="margin-top:14px;padding:18px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
          <span style="font-size:18px;">📈</span>
          <span style="font-weight:600;">消息量趋势</span>
          <span class="meta-info" id="home-trend-range"></span>
        </div>
        <div style="height:300px;"><canvas id="home-trend-chart"></canvas></div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
        <div class="card" style="padding:18px;">
          <div style="font-weight:600;margin-bottom:12px;">🔥 热门频道</div>
          <div id="home-channels-list"></div>
        </div>
        <div class="card" style="padding:18px;">
          <div style="font-weight:600;margin-bottom:12px;">🏷️ 热门关键词</div>
          <div id="home-keywords-cloud"></div>
        </div>
      </div>

      <div class="card" style="padding:18px;margin-top:14px;">
        <div style="font-weight:600;margin-bottom:12px;">💬 精选消息</div>
        <div id="home-recent-list"></div>
      </div>
    `;

    this._renderKPIs();
    this._renderTrend();
    this._renderChannelsAndKeywords();
    this._renderRecent();
  },

  _renderKPIs() {
    const data = getDaysDataForDate(STATE.currentDate);
    const dayItem = STATE.index.days.find(d => d.date === STATE.currentDate) || {};

    let totalMsg = 0, pos = 0, neg = 0, fb = 0, neu = 0, users = 0;
    for (const platform of Object.keys(data)) {
      const d = data[platform];
      totalMsg += d.total_messages || 0;
      pos += d.positive || 0;
      neg += d.negative || 0;
      fb += d.feedback || 0;
      neu += d.neutral || 0;
      users += d.active_users || 0;
    }

    const grid = document.getElementById('home-kpi-grid');
    grid.innerHTML = `
      ${this._kpiCard('💬', '今日消息', totalMsg, '条')}
      ${this._kpiCard('👥', '活跃用户', users, '人')}
      ${this._kpiCard('😊', '正面情感', pos, `条 (${this._pct(pos, totalMsg)})`)}
      ${this._kpiCard('😟', '负面情感', neg, `条 (${this._pct(neg, totalMsg)})`)}
    `;
  },

  _kpiCard(icon, label, value, suffix) {
    return `
      <div class="card" style="padding:16px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
          <span style="font-size:20px;">${icon}</span>
          <span style="font-size:12px;color:var(--text-sub);">${label}</span>
        </div>
        <div style="font-size:28px;font-weight:700;">${value}</div>
        <div style="font-size:11px;color:var(--text-sub);margin-top:2px;">${suffix}</div>
      </div>`;
  },

  _pct(n, total) {
    if (!total) return '0%';
    return ((n / total) * 100).toFixed(1) + '%';
  },

  _renderTrend() {
    // Stacked bar: total messages per day, split by platform
    const days = STATE.index.days.slice(-30);  // last 30 days
    const platforms = STATE.index.platforms;

    const labels = days.map(d => d.date.slice(5));  // MM-DD
    const datasets = platforms.map((p, i) => {
      const colors = ['#6366f1', '#ef4444', '#22c55e', '#f59e0b', '#3b82f6', '#8b5cf6'];
      return {
        label: p,
        data: days.map(d => (d.platforms[p] && d.platforms[p].total_messages) || 0),
        backgroundColor: colors[i % colors.length],
        borderRadius: 3,
      };
    });

    const ctx = document.getElementById('home-trend-chart').getContext('2d');
    if (this._chart) this._chart.destroy();
    this._chart = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          x: { stacked: true },
          y: { stacked: true, beginAtZero: true },
        },
      },
    });

    document.getElementById('home-trend-range').textContent = `近 ${days.length} 天`;
  },

  _renderChannelsAndKeywords() {
    const data = getDaysDataForDate(STATE.currentDate);

    // Aggregate channels across platforms
    const channelCounter = {};
    for (const platform of Object.keys(data)) {
      for (const ch of (data[platform].channels || [])) {
        channelCounter[ch.name] = (channelCounter[ch.name] || 0) + ch.count;
      }
    }
    const topChannels = Object.entries(channelCounter)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    // Aggregate keywords
    const kwCounter = {};
    for (const platform of Object.keys(data)) {
      for (const k of (data[platform].keywords || [])) {
        kwCounter[k.word] = (kwCounter[k.word] || 0) + k.count;
      }
    }
    const topKeywords = Object.entries(kwCounter)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20);

    document.getElementById('home-channels-list').innerHTML = topChannels.length
      ? topChannels.map(([name, count], i) => `
          <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);">
            <span><span style="color:var(--text-sub);margin-right:8px;">${i + 1}.</span>${Utils.esc(name)}</span>
            <span style="font-weight:600;">${count}</span>
          </div>
        `).join('')
      : '<div class="empty-state">无数据</div>';

    document.getElementById('home-keywords-cloud').innerHTML = topKeywords.length
      ? topKeywords.map(([word, count]) => `
          <span style="display:inline-block;margin:3px;padding:4px 10px;background:var(--bg-2);border-radius:12px;font-size:${Math.min(16, 11 + count / 5)}px;">
            ${Utils.esc(word)} <span style="color:var(--text-sub);font-size:0.85em;">${count}</span>
          </span>
        `).join('')
      : '<div class="empty-state">无数据</div>';
  },

  _renderRecent() {
    const data = getDaysDataForDate(STATE.currentDate);
    const all = [];
    for (const platform of Object.keys(data)) {
      for (const m of (data[platform].top_messages || [])) {
        all.push({ ...m, platform });
      }
    }
    all.sort((a, b) => (b.likes || 0) - (a.likes || 0));

    document.getElementById('home-recent-list').innerHTML = all.length
      ? all.slice(0, 8).map(m => `
          <div style="padding:10px 0;border-bottom:1px solid var(--border);">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
              <span style="font-size:10px;padding:2px 6px;background:var(--bg-2);border-radius:3px;">${m.platform}</span>
              <span style="font-size:10px;color:var(--text-sub);">${Utils.esc(m.user || '匿名')}</span>
              <span style="font-size:10px;color:${this._sentimentColor(m.sentiment)};">${this._sentimentLabel(m.sentiment)}</span>
              ${m.likes ? `<span style="font-size:10px;color:var(--text-sub);">👍 ${m.likes}</span>` : ''}
            </div>
            <div style="font-size:13px;line-height:1.5;">${Utils.esc(m.content || '')}</div>
          </div>
        `).join('')
      : '<div class="empty-state">无精选消息</div>';
  },

  _sentimentColor(s) {
    return { positive: '#22c55e', negative: '#ef4444', feedback: '#f59e0b', neutral: '#9ca3af' }[s] || '#9ca3af';
  },

  _sentimentLabel(s) {
    return { positive: '😊 正面', negative: '😟 负面', feedback: '💡 建议', neutral: '😐 中性' }[s] || s;
  },

  cleanup() {
    if (this._chart) this._chart.destroy();
  },
};
