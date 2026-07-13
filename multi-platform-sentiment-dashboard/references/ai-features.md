# AI-Enhanced Features

Once the data layer (fetchers + ETL + dashboard rendering) is stable, two LLM-powered features multiply the dashboard's value. Both are designed to be **LLM-agnostic** — they call any OpenAI-compatible chat-completions endpoint. The CFL reference implementation uses DeepSeek (`https://api.deepseek.com/v1/chat/completions`), but the same code works against:

- **DeepSeek** — cheap, fast, Chinese/English both strong, OpenAI-compatible
- **OpenAI** (`api.openai.com/v1/chat/completions`) — gold standard, most expensive
- **Anthropic** — requires a small adapter (different request shape)
- **Local Ollama / vLLM** — fully private, no quota, weaker quality
- **Internal LLM gateway** (most companies have one) — preferred for production
- **Cloudflare Worker / SCF proxy** wrapping any of the above — preferred for hiding the API key

The only contract your LLM must satisfy: `POST {endpoint}` with `Authorization: Bearer <key>`, body `{model, messages, stream?, temperature?, max_tokens?}`, and respond with either SSE `data: {json}\n\n` chunks (for streaming) or a single JSON `choices[0].message.content` (non-streaming).

## Feature 1 — Selection-based translation (`translate.js`)

**User experience:** user selects any foreign text in the dashboard (e.g., a Spanish Facebook comment, a Korean Discord message). A small floating popup appears near the cursor showing the Chinese translation. No button, no extra clicks.

### Why this matters for community ops

- **Multilingual communities are normal.** Discord and Facebook content routinely mixes 3–5 languages.
- **Translation-on-demand is faster than translation-always.** Translating everything doubles your data and adds noise. Letting the user pick what to read keeps the raw data intact.
- **Cheap to implement, high perceived value.** One file, ~270 lines, one API call per selection (with a 200-entry cache).

### Implementation outline

1. Listen to `mouseup` on the document. After 150 ms (so the selection settles), get `window.getSelection().toString()`.
2. **Skip if:** empty, < 2 chars, > 1000 chars, mostly Chinese (CJK > 30%), mostly numeric/symbols, or a request is already in flight.
3. Compute a popup position from the selection's `getBoundingClientRect()`. Edge-clamp to viewport.
4. If a cache hit, show result immediately. Otherwise show a spinner, call the LLM, cache the result, then show.
5. On error, show a friendly error bubble; don't break the page.
6. Hide on `mousedown` outside the popup or `Esc` key.

### LLM call

```text
System: "You are a translator. Translate the given text to Simplified Chinese.
         Only output the translation, nothing else. If the text is already in
         Chinese, output it unchanged. Keep the original formatting and line breaks."
User:   <selected text>
Model:  deepseek-chat (or any)
temperature: 0.1     (deterministic)
max_tokens: 1024
```

Temperature 0.1 is important — translation should be consistent, not creative.

### Caching strategy

Keep a `Map<string, string>` in memory, max 200 entries, simple FIFO eviction. The cache key is the trimmed text (first 500 chars). For multi-session caching, swap to `sessionStorage` or `localStorage` with the same key strategy.

### Security

Same as everywhere else: the API key is in JS, so it's visible. Mitigation options:
- **Restrict the key by domain** if your LLM provider supports it (e.g., HTTP referer allowlist on Cloudflare Worker)
- **Quota / spend cap** on the LLM account
- **Rate-limit by IP** on your proxy

See the full code in `assets/templates/translate.js`.

---

## Feature 2 — Data Q&A chat (`page-ask-ai.js`)

**User experience:** a chat page where the user types natural-language questions ("which channel had the most complaints yesterday?", "what were people saying about the new weapon?"). The LLM answers with markdown rendering, citing real data from the dashboard. Supports Chinese and English, matches the user's question language.

### The grounding problem (and how this skill solves it)

A naive "ask the LLM about our data" fails: the LLM hallucinates numbers. The fix is **injecting a system prompt that contains the actual data**. Concretely:

1. Build a system prompt that summarizes the loaded data: last 7 days totals, sentiment distribution, top 15 users, top 15 channels, top 20 keywords, last 30 days trend, per-platform breakdown.
2. For every user question, also do a **keyword search** over the last 30 days of `all_messages` and inject the top 30 matching raw messages into the system prompt. This lets the LLM answer concrete "what did X say?" questions.
3. Tell the LLM explicitly: "If the search-retrieved messages contain an answer, quote the original. If the data is insufficient, say so."

### System prompt skeleton

```text
You are a <your_product> community data analyst assistant. Answer the user's
question based on the real data below. Rules:
1. Only use the provided data; never invent numbers.
2. If data is insufficient, explicitly say what's missing.
3. Reply in the same language as the user's question.
4. You may interpret and analyze trends, but label interpretations as such.
5. When quoting messages, quote the original text (no translation).
6. CRITICAL: if the "search results" section has matches, you MUST ground
   your answer in those raw messages and quote the players directly.

--- DATA SUMMARY ---
Date range: <earliest> to <latest> (<N> days)
Platforms: discord, facebook, youtube

【Last 7 days】
Total messages: <N>
Sentiment: positive <N> / neutral <N> / negative <N> / feedback <N>
Distinct active users: <N>

Top 15 users: ...
Top 15 channels: ...
Top 20 keywords: ...
Top 10 hot messages: ...
【30-day trend】 <date>: <msgs>, <date>: <msgs>, ...
【Per-platform latest】 ...

【Search results for: <user query>】 (<N> matches)
  1. [date] [platform] author: "<content>" (likes: N)
  ...
```

### Keyword search implementation

A few important details that took multiple iterations to get right:

1. **Stop-word list** must include both Chinese (`的/了/在/是/我...`) and English (`the/a/is/are/of/...`) high-frequency words. Otherwise almost every search matches everything.
2. **CJK + Latin boundary splitting.** A query like "mode玩家评价如何" should be split into `["mode", "玩家评价如何"]` and then the CJK part into 2-character windows for better recall (`["玩家评价", "家评价如", "评价如何"]`).
3. **Search over the last 30 days only** — older messages are too stale for Q&A.
4. **De-duplicate** by `date + platform + content[:80]` so the same retweet/repost doesn't dominate.
5. **Sort by match count, then by likes** — so the most relevant + most-engaged messages come first.

### Streaming UX

Stream the LLM response (SSE `data: {json}\n\n` chunks) and append to a markdown bubble. The CFL code uses a simple text decoder buffer that handles partial lines. While the stream is active, show "思考中…" then the rolling text. When done, append a meta line ("由 DeepSeek 生成 · 14:32 · 检索到 12 条相关消息").

### Markdown rendering

Don't pull in a 100 KB library. A 5-line replacement handles 95% of cases: fenced code blocks, inline code, bold, italic, newlines. Use `Utils.esc(text)` first, then apply the regex replacements.

### History persistence

Save to `localStorage` with two parallel arrays:
- `history` — raw `[{role, content}]` for the LLM context (don't HTML-escape, send raw)
- `displayHistory` — `[{role, html}]` for re-rendering on page load

Restore on `render()` and append each as a bubble. Limit the LLM context to the last 20 messages to keep tokens bounded.

### Security and quota

Same as translate: API key in JS is visible. For internal team tools this is usually acceptable. For external-facing tools, proxy through a serverless function.

---

## LLM client template (`llm-client.js`)

The CFL code currently has the LLM call inline in both `translate.js` and `page-ask-ai.js`, with the API key duplicated. The recommended refactor (and what this skill ships as a template) is to extract a single `llm-client.js` module:

```js
const LLMClient = {
  ENDPOINT: 'https://api.deepseek.com/v1/chat/completions',
  API_KEY: '<your-key>',
  MODEL: 'deepseek-chat',

  // Streaming chat completion
  async streamChat(messages, onChunk, opts = {}) {
    const body = {
      model: this.MODEL,
      messages,
      stream: true,
      temperature: opts.temperature ?? 0.3,
      max_tokens: opts.max_tokens ?? 2048,
    };
    const response = await fetch(this.ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + this.API_KEY,
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new Error('LLM API ' + response.status + ': ' + (await response.text()).slice(0, 200));
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let full = '';
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        const t = line.trim();
        if (!t.startsWith('data:')) continue;
        const data = t.slice(5).trim();
        if (data === '[DONE]') continue;
        try {
          const json = JSON.parse(data);
          const delta = json.choices?.[0]?.delta;
          if (delta?.content) {
            full += delta.content;
            onChunk(full);
          }
        } catch (_) { /* ignore parse errors, keep reading */ }
      }
    }
    return full;
  },

  // Non-streaming chat completion
  async chat(messages, opts = {}) {
    let result = '';
    return await this.streamChat(messages, (chunk) => { result = chunk; }, opts);
  },
};
```

To swap LLM providers, change `ENDPOINT`, `API_KEY`, and `MODEL` only:

| Provider | ENDPOINT | MODEL |
|---|---|---|
| DeepSeek | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` |
| Ollama local | `http://localhost:11434/v1/chat/completions` | `llama3.1` |
| Internal gateway | `https://llm.internal.company.com/v1/chat/completions` | `internal-7b` |
| Your Cloudflare Worker proxy | `https://llm-proxy.your-domain.workers.dev/v1/chat/completions` | (proxied) |

---

## End-to-end checklist for AI features

- [ ] Pick an LLM provider, obtain API key
- [ ] Decide: ship key in JS (prototype OK) vs. proxy through serverless (production)
- [ ] Drop `llm-client.js` into `assets/`, fill in `ENDPOINT` / `API_KEY` / `MODEL`
- [ ] Drop `translate.js` into `assets/`, add `<script src="assets/translate.js">` to `dashboard.html`
- [ ] Drop `page-ask-ai.js` into `assets/`, add `<script>` tag and a nav item, add `'ask-ai'` to the router
- [ ] Test translation: select a foreign message in the dashboard, verify popup appears
- [ ] Test Q&A: ask "上个月最热的话题是什么？", verify LLM grounds answer in real data
- [ ] Test language matching: ask in English, verify English response
- [ ] Test cache: select the same text twice, second time should be instant
- [ ] Verify error UX: kill the LLM endpoint, select text, verify graceful error popup
