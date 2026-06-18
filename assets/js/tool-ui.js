/* ========================================
   ZenTools 统一工具 UI — 共享 JS
   ======================================== */

(function() {
  'use strict';

  // ===== i18n 多语言引擎 =====

  window.ZT = window.ZT || {};

  /**
   * 应用当前语言到所有 [data-i18n] 元素
   * 页面的翻译数据需提前定义在 window.ZT_PAGE 中
   */
  ZT.applyLanguage = function(lang) {
    const dict = (window.ZT_PAGE && window.ZT_PAGE[lang]) || (window.ZT_PAGE && window.ZT_PAGE.zh);
    if (!dict) return;

    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang;

    // 更新 <title>
    if (dict.pageTitle) document.title = dict.pageTitle;

    // 更新所有 data-i18n 元素
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key] != null) {
        el.textContent = dict[key];
      }
    });

    localStorage.setItem('zentools_lang', lang);
  };

  // 语言选择器初始化
  function initLang() {
    const sel = document.getElementById('langSelect');
    if (!sel) return;

    const saved = localStorage.getItem('zentools_lang') || 'zh';
    sel.value = langNames[saved] ? saved : 'zh';

    sel.addEventListener('change', function() {
      ZT.applyLanguage(this.value);
    });

    ZT.applyLanguage(sel.value);
  }

  // ===== 语言选择器选项文本 =====
  const langNames = {
    zh: '中文',
    en: 'English',
    ja: '日本語',
    vi: 'Tiếng Việt'
  };

  // 填充语言选择器选项文本
  document.querySelectorAll('#langSelect option').forEach(opt => {
    const lang = opt.value;
    if (langNames[lang]) opt.textContent = langNames[lang];
  });

  // ===== 滚动渐入动画 =====
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => observer.observe(el));

  // ===== 浮动光晕动画 =====
  let t = 0;
  const b1 = document.querySelector('.blob-1');
  const b2 = document.querySelector('.blob-2');

  function animBlob() {
    t += 0.003;
    if (b1) b1.style.transform = `translate(${Math.sin(t) * 30}px,${Math.cos(t * 0.8) * 20}px)`;
    if (b2) b2.style.transform = `translate(${Math.cos(t * 0.9) * 25}px,${Math.sin(t) * 18}px)`;
    requestAnimationFrame(animBlob);
  }

  if (b1 || b2) animBlob();

  // ===== 启动 i18n（放在页面脚本定义 ZT_PAGE 之后加载）=====
  initLang();
})();
