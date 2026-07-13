/* ============================================================
 * llm-client.js — LLM-agnostic chat completion client
 * ------------------------------------------------------------
 * Single point of integration for ANY OpenAI-compatible
 * chat-completions endpoint:
 *   - DeepSeek      (https://api.deepseek.com/v1/chat/completions)
 *   - OpenAI        (https://api.openai.com/v1/chat/completions)
 *   - Ollama local  (http://localhost:11434/v1/chat/completions)
 *   - Internal LLM gateway
 *   - A Cloudflare Worker / SCF proxy that hides the real key
 *
 * To switch providers, change ENDPOINT / API_KEY / MODEL.
 * No other code needs to change.
 *
 * IMPORTANT — security:
 *   Shipping the API key in browser JS means anyone can read
 *   it from DevTools and use your quota. For prototype / internal
 *   team use this is acceptable. For production, point ENDPOINT
 *   at a serverless proxy you control and put the real key in
 *   that proxy's environment.
 * ============================================================ */
const LLMClient = {
  // ↓↓↓ Configure these three constants for your provider ↓↓↓
  ENDPOINT: 'https://api.deepseek.com/v1/chat/completions',
  API_KEY: '<your-llm-api-key>',
  MODEL: 'deepseek-chat',

  /** Streaming chat completion. `onChunk(fullText)` fires on every delta. */
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
      const errBody = await response.text();
      throw new Error('LLM API ' + response.status + ': ' + errBody.slice(0, 200));
    }
    if (!response.body) {
      throw new Error('LLM API response has no body (streaming unsupported?)');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = '';
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // keep last partial line for next iteration

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data:')) continue;
        const data = str_after(trimmed, 'data:').trim();
        if (data === '[DONE]') continue;
        try {
          const json = JSON.parse(data);
          const delta = json.choices && json.choices[0] && json.choices[0].delta;
          if (delta && delta.content) {
            fullText += delta.content;
            onChunk(fullText);
          }
        } catch (_) {
          // Ignore JSON parse errors on partial chunks, keep reading
        }
      }
    }
    return fullText;
  },

  /** Non-streaming chat completion. */
  async chat(messages, opts = {}) {
    let result = '';
    await this.streamChat(messages, (chunk) => { result = chunk; }, opts);
    return result;
  },

  /** Quick translation helper, used by translate.js. */
  async translate(text, targetLang = 'Simplified Chinese') {
    return await this.chat([
      {
        role: 'system',
        content: `You are a translator. Translate the given text to ${targetLang}. ` +
                 'Only output the translation, nothing else. If the text is already ' +
                 'in the target language, output it unchanged. Keep the original ' +
                 'formatting and line breaks.',
      },
      { role: 'user', content: text },
    ], { temperature: 0.1, max_tokens: 1024 });
  },
};

function str_after(s, prefix) {
  return s.startsWith(prefix) ? s.slice(prefix.length) : s;
}
