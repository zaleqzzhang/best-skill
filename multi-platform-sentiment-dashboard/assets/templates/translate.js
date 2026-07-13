/* ============================================================
 * translate.js — selection-based foreign text translation
 * ------------------------------------------------------------
 * User selects any text on the page, a small floating popup
 * appears near the cursor with the Chinese translation.
 *
 * Design notes:
 *   - LLM-agnostic: uses LLMClient.translate() from llm-client.js
 *   - Caches 200 most recent translations in a Map (FIFO eviction)
 *   - Skips selection if mostly Chinese / mostly numeric / >1000 chars
 *   - Edge-clamped popup position; flips above selection if no room below
 *   - Graceful error: shows a popup with the error, doesn't crash the page
 *   - Closes on outside mousedown or Esc
 *
 * Requires: llm-client.js loaded BEFORE this file.
 * ============================================================ */
(function () {
  let popup = null;
  let isTranslating = false;
  const cache = new Map();
  const MAX_CACHE = 200;

  // ----- Helpers -----

  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function isMostlyChinese(text) {
    const cjk = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/g) || []).length;
    return cjk / text.length > 0.3;
  }

  function isMostlyNumeric(text) {
    const alnum = (text.match(/[a-zA-Z\u00C0-\u024F\u4e00-\u9fff]/g) || []).length;
    return alnum / text.length < 0.2;
  }

  // ----- Popup DOM -----

  function ensurePopup() {
    if (popup) return;
    popup = document.createElement('div');
    popup.id = 'translate-popup';
    popup.className = 'translate-popup';
    document.body.appendChild(popup);
  }

  function positionPopup(rect) {
    if (!popup) return;
    popup.style.visibility = 'hidden';
    popup.style.display = 'block';
    const pw = popup.offsetWidth || 280;
    const ph = popup.offsetHeight || 100;
    let top = rect.bottom + window.scrollY + 10;
    let left = rect.left + window.scrollX + rect.width / 2 - pw / 2;
    const viewW = window.innerWidth;
    if (left + pw > viewW - 16) left = viewW - pw - 16;
    if (left < 8) left = 8;
    if (rect.bottom + ph + 20 > window.innerHeight) {
      top = rect.top + window.scrollY - ph - 10;
    }
    popup.style.top = top + 'px';
    popup.style.left = left + 'px';
    popup.style.visibility = '';
  }

  function showLoading(rect, text) {
    ensurePopup();
    popup.innerHTML =
      '<div class="translate-header">' +
        '<span class="translate-icon">🌐</span>' +
        '<span>翻译中…</span>' +
      '</div>' +
      '<div class="translate-original">' + escHtml(text.slice(0, 200)) + (text.length > 200 ? '…' : '') + '</div>' +
      '<div class="translate-loading"><div class="translate-spinner"></div></div>';
    popup.classList.add('visible');
    positionPopup(rect);
  }

  function showResult(rect, original, translation) {
    ensurePopup();
    popup.innerHTML =
      '<div class="translate-header">' +
        '<span class="translate-icon">🌐</span>' +
        '<span>中文翻译</span>' +
        '<button class="translate-close">&times;</button>' +
      '</div>' +
      '<div class="translate-original">' + escHtml(original.slice(0, 200)) + (original.length > 200 ? '…' : '') + '</div>' +
      '<div class="translate-result">' + escHtml(translation) + '</div>';
    popup.classList.add('visible');
    positionPopup(rect);
    popup.querySelector('.translate-close').addEventListener('click', () => popup.classList.remove('visible'));
  }

  function showError(rect, errMsg) {
    ensurePopup();
    popup.innerHTML =
      '<div class="translate-header">' +
        '<span class="translate-icon">⚠️</span>' +
        '<span>翻译失败</span>' +
        '<button class="translate-close">&times;</button>' +
      '</div>' +
      '<div class="translate-error">' + escHtml(errMsg || '请稍后重试') + '</div>';
    popup.classList.add('visible');
    positionPopup(rect);
    popup.querySelector('.translate-close').addEventListener('click', () => popup.classList.remove('visible'));
  }

  function hidePopup() {
    if (popup) popup.classList.remove('visible');
  }

  // ----- Cache -----

  function getCacheKey(text) {
    return text.trim().slice(0, 500);
  }

  function putCache(key, value) {
    if (cache.size >= MAX_CACHE) {
      const first = cache.keys().next().value;
      cache.delete(first);
    }
    cache.set(key, value);
  }

  // ----- Event listeners -----

  document.addEventListener('mouseup', function (e) {
    if (popup && popup.contains(e.target)) return;
    setTimeout(async function () {
      const selection = window.getSelection();
      const text = selection ? selection.toString().trim() : '';
      if (!text || text.length < 2) { hidePopup(); return; }
      if (isMostlyChinese(text)) { hidePopup(); return; }
      if (isMostlyNumeric(text)) { hidePopup(); return; }
      if (text.length > 1000) return;
      if (isTranslating) return;
      isTranslating = true;

      try {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        const cacheKey = getCacheKey(text);
        if (cache.has(cacheKey)) {
          showResult(rect, text, cache.get(cacheKey));
          return;
        }
        showLoading(rect, text);
        const translation = await LLMClient.translate(text);
        if (translation) {
          putCache(cacheKey, translation);
          showResult(rect, text, translation);
        } else {
          showError(rect, '翻译结果为空');
        }
      } catch (err) {
        console.error('Translate error:', err);
        try {
          const sel = window.getSelection();
          const r = sel.getRangeAt(0).getBoundingClientRect();
          showError(r, err.message || '翻译失败');
        } catch (_) {
          showError({ bottom: 100, top: 80, left: 200, width: 100 }, err.message || '翻译失败');
        }
      } finally {
        isTranslating = false;
      }
    }, 150);
  });

  document.addEventListener('mousedown', function (e) {
    if (popup && !popup.contains(e.target)) hidePopup();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hidePopup();
  });
})();
