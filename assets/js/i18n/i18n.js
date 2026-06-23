(function () {
  const LANG_KEY = 'zentools_lang';
  const SUPPORTED = ['zh', 'en', 'ja', 'vi'];
  const DEFAULT_LANG = 'zh';

  function getLang() {
    const fromUrl = new URLSearchParams(location.search).get('lang');
    if (fromUrl && SUPPORTED.includes(fromUrl)) return fromUrl;
    return localStorage.getItem(LANG_KEY) || DEFAULT_LANG;
  }

  function applyLang(lang) {
    if (!SUPPORTED.includes(lang)) lang = DEFAULT_LANG;
    const dict = (window.I18N_DATA && window.I18N_DATA[lang]) || {};
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang;

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const k = el.getAttribute('data-i18n');
      if (dict[k] !== undefined) el.textContent = dict[k];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const k = el.getAttribute('data-i18n-placeholder');
      if (dict[k] !== undefined) el.placeholder = dict[k];
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const k = el.getAttribute('data-i18n-title');
      if (dict[k] !== undefined) el.title = dict[k];
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
      const k = el.getAttribute('data-i18n-aria');
      if (dict[k] !== undefined) el.setAttribute('aria-label', dict[k]);
    });

    localStorage.setItem(LANG_KEY, lang);
    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
  }

  function bindUI() {
    // 4 个 a 链接
    document.querySelectorAll('[data-lang]').forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        applyLang(a.dataset.lang);
      });
    });
    // 下拉框（可选）
    const sel = document.getElementById('langSelect');
    if (sel) {
      sel.value = getLang();
      sel.addEventListener('change', () => applyLang(sel.value));
    }
    // 高亮当前语言
    const cur = getLang();
    document.querySelectorAll('[data-lang]').forEach(a => {
      a.classList.toggle('is-active', a.dataset.lang === cur);
    });
  }

  window.I18N = { apply: applyLang, get: getLang };
  document.addEventListener('DOMContentLoaded', () => {
    applyLang(getLang());
    bindUI();
  });
})();
