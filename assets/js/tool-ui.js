/* ========================================
   ZenTools 统一工具 UI — 共享 JS
   ======================================== */

(function() {
  'use strict';

  window.ZT = window.ZT || {};

  // ===== 站点分析（Google Analytics 4）=====
  // 如需启用，在下方设置你的 GA4 Measurement ID
  // 获取方式：https://analytics.google.com → 管理 → 数据流 → 选择网站 → 测量 ID
  var GA_ID = 'G-V3MP20S9Z3';
  if (GA_ID && !window.gtag) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https:' + '/www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);
  }

  // ===== 简单页面浏览统计（自托管，无第三方依赖）=====
  (function() {
    var key = 'zt_pageviews';
    try {
      var pv = JSON.parse(localStorage.getItem(key)) || {};
      var today = new Date().toISOString().slice(0, 10);
      if (!pv[today]) pv[today] = 0;
      pv[today]++;
      // Keep last 30 days
      var dates = Object.keys(pv).sort();
      while (dates.length > 30) {
        delete pv[dates.shift()];
      }
      localStorage.setItem(key, JSON.stringify(pv));
    } catch(e) {}
  })();

  // ===== i18n 多语言引擎 (公共翻译 + 页面翻译 合并) =====
  ZT.applyLanguage = function(lang) {
    const common = (window.ZT_COMMON && window.ZT_COMMON[lang]) || {};
    const page = (window.ZT_PAGE && window.ZT_PAGE[lang]) || (window.ZT_PAGE && window.ZT_PAGE.zh) || {};
    var dict = {};
    var k;
    for (k in common) { if (common.hasOwnProperty(k)) dict[k] = common[k]; }
    for (k in page) { if (page.hasOwnProperty(k)) dict[k] = page[k]; }
    if (!Object.keys(dict).length) return;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang;
    if (dict.pageTitle) document.title = dict.pageTitle;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key] != null) el.textContent = dict[key];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-placeholder');
      if (dict[key] != null) el.placeholder = dict[key];
    });
    localStorage.setItem('zentools_lang', lang);
    // 更新语言选择器选项文本
    var sel = document.getElementById('langSelect');
    if (sel) {
      sel.value = lang;
      var opts = sel.querySelectorAll('option');
      for (var i = 0; i < opts.length; i++) {
        var key = 'lang' + opts[i].value.charAt(0).toUpperCase() + opts[i].value.slice(1);
        if (dict[key] != null) opts[i].textContent = dict[key];
      }
    }
    window.dispatchEvent(new CustomEvent('zt-langchange', { detail: { lang: lang, dict: dict } }));
  };

  function initLang() {
    var sel = document.getElementById('langSelect');
    if (!sel) return;
    var saved = localStorage.getItem('zentools_lang') || 'zh';
    sel.value = saved;
    sel.addEventListener('change', function() { ZT.applyLanguage(this.value); });
    ZT.applyLanguage(sel.value);
  }

  // ===== 滚动渐入动画 =====
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
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

  // ===== #7 工具点击统计 =====
  ZT.clickTrack = function(url, name) {
    try {
      const key = 'zt_clicks';
      let clicks = JSON.parse(localStorage.getItem(key)) || {};
      clicks[url] = (clicks[url] || 0) + 1;
      localStorage.setItem(key, JSON.stringify(clicks));
    } catch(e) {}
  };
  // Track clicks on tool cards
  document.addEventListener('click', function(e) {
    const card = e.target.closest('.tool-card, .mini-card, .fav-item, .mega-item');
    if (card) {
      const href = card.getAttribute('href');
      if (href) ZT.clickTrack(href, card.textContent.trim().slice(0, 30));
    }
  });

  // ===== #8 回到顶部按钮 =====
  var backTop = document.createElement('button');
  backTop.className = 'zt-backtop';
  backTop.innerHTML = '↑';
  backTop.title = '回到顶部';
  backTop.onclick = function() { window.scrollTo({ top: 0, behavior: 'smooth' }); };
  document.body.appendChild(backTop);
  window.addEventListener('scroll', function() {
    backTop.classList.toggle('show', window.scrollY > 400);
  });

  // ===== #10 暗色/亮色主题切换 =====
  (function() {
    var btn = document.createElement('button');
    btn.className = 'zt-theme-toggle';
    var currentTheme = localStorage.getItem('zentools_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    btn.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';
    btn.title = currentTheme === 'dark' ? '亮色模式' : '暗色模式';
    btn.onclick = function() {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      btn.innerHTML = next === 'dark' ? '☀️' : '🌙';
      btn.title = next === 'dark' ? '亮色模式' : '暗色模式';
      localStorage.setItem('zentools_theme', next);
    };
    document.body.appendChild(btn);
  })();

  // ===== #11 键盘快捷键 =====
  document.addEventListener('keydown', function(e) {
    // Escape 关闭下拉菜单
    if (e.key === 'Escape') {
      document.querySelectorAll('.mega-menu').forEach(function(m) { m.style.opacity = '0'; m.style.visibility = 'hidden'; });
      document.querySelectorAll('.mobile-overlay').forEach(function(o) { o.classList.remove('active'); });
    }
  });

  // ===== #12 骨架屏（替换加载文字） =====
  document.querySelectorAll('.tools-grid, .dev-grid, .cat-grid').forEach(function(grid) {
    var empty = grid.querySelector('.empty-state');
    if (empty && empty.textContent.trim().startsWith('⏳')) {
      var skeleton = '';
      for (var i = 0; i < 6; i++) {
        skeleton += '<div class="skeleton-card"><div class="skeleton-icon"></div><div class="skeleton-line"></div><div class="skeleton-line short"></div></div>';
      }
      empty.outerHTML = skeleton;
    }
  });

  // ===== #6 最近使用 & 收藏 =====
  ZT.track = {
    _recent: [],
    _fav: [],
    _key_recent: 'zt_recent',
    _key_fav: 'zt_favorites',
    init() {
      try {
        this._recent = JSON.parse(localStorage.getItem(this._key_recent)) || [];
        this._fav = JSON.parse(localStorage.getItem(this._key_fav)) || [];
      } catch(e) { this._recent = []; this._fav = []; }
      const toolName = this._getToolName();
      if (toolName) this.add(toolName);
    },
    _getToolName() {
      const title = document.title.replace(/\s*[-|]\s*(免费在线工具|ZenTools|SEO工具|金融工具).*$/, '').trim();
      return title || null;
    },
    _getPageUrl() { return window.location.pathname; },
    add(name) {
      const url = this._getPageUrl();
      this._recent = this._recent.filter(r => r.url !== url);
      this._recent.unshift({ name, url, time: Date.now() });
      if (this._recent.length > 20) this._recent = this._recent.slice(0, 20);
      localStorage.setItem(this._key_recent, JSON.stringify(this._recent));
    },
    toggleFav(name) {
      const url = this._getPageUrl();
      const idx = this._fav.findIndex(f => f.url === url);
      if (idx >= 0) {
        this._fav.splice(idx, 1);
        localStorage.setItem(this._key_fav, JSON.stringify(this._fav));
        return false;
      } else {
        this._fav.unshift({ name, url, time: Date.now() });
        localStorage.setItem(this._key_fav, JSON.stringify(this._fav));
        return true;
      }
    },
    isFav() { return this._fav.some(f => f.url === this._getPageUrl()); },
    addFavBtn() {
      const name = this._getToolName();
      if (!name) return;
      var btn = document.createElement('button');
      btn.className = 'fav-btn';
      btn.innerHTML = this.isFav() ? '★' : '☆';
      btn.title = this.isFav() ? '取消收藏' : '收藏此工具';
      btn.onclick = function() {
        var added = ZT.track.toggleFav(name);
        btn.innerHTML = added ? '★' : '☆';
        btn.title = added ? '取消收藏' : '收藏此工具';
      };
      var header = document.querySelector('.page-header');
      if (header) header.appendChild(btn);
    }
  };
  ZT.track.init();
  ZT.track.addFavBtn();

  // ===== #9 工具间快捷跳转（互补工具推荐） =====
  (function() {
    var relatedMap = {
      'pdf-merge': ['pdf-split', 'pdf-compress'],
      'pdf-split': ['pdf-merge', 'pdf-extract-pages'],
      'pdf-compress': ['pdf-merge', 'image-to-pdf'],
      'pdf-to-word': ['word-to-pdf', 'pdf-to-excel'],
      'word-to-pdf': ['pdf-to-word', 'excel-to-pdf'],
      'pdf-to-excel': ['excel-to-pdf', 'pdf-to-csv'],
      'excel-to-pdf': ['pdf-to-excel', 'word-to-pdf'],
      'pdf-to-ppt': ['ppt-to-pdf'],
      'ppt-to-pdf': ['pdf-to-ppt'],
      'image-to-pdf': ['pdf-to-image', 'imgtopdf'],
      'pdf-to-image': ['image-to-pdf'],
      'image-compress': ['image-convert', 'image-resize'],
      'image-convert': ['image-compress', 'image-resize'],
      'image-resize': ['image-crop', 'image-compress'],
      'image-crop': ['image-resize', 'image-rotate'],
      'audio-cutter': ['audio-merger', 'audio-speed'],
      'audio-merger': ['audio-cutter'],
      'video-compress': ['video-to-gif', 'video-to-mp3'],
      'video-to-gif': ['video-to-mp3', 'video-compress'],
      'text-to-speech': ['speech-to-text'],
      'speech-to-text': ['text-to-speech'],
      'currency-converter': ['cny-jpy'],
      'cny-jpy': ['currency-converter'],
      'json-formatter': ['json-diff', 'json-viewer'],
      'json-diff': ['json-formatter'],
      'hash-generator': ['regex-tester'],
      'loan-calculator': ['deposit-interest', 'stock-fee'],
      'deposit-interest': ['loan-calculator'],
      'stock-fee': ['loan-calculator']
    };
    var path = window.location.pathname;
    var slug = path.replace(/^[/]/, '').replace(/\.html$/, '').split('/').join('-');
    // Try to match from various patterns
    var related = null;
    for (var key in relatedMap) {
      if (path.indexOf(key) >= 0) {
        related = relatedMap[key];
        break;
      }
    }
    if (related && related.length) {
      // Try loading tools data to get names
      fetch('/data/tools-data.json').then(function(r) { return r.json(); }).then(function(data) {
        var tools = data.tools || [];
        var html = '<div class="related-tools"><h3 style="font-size:16px;font-weight:700;margin-bottom:12px;color:var(--muted);">🔗 相关工具推荐</h3><div style="display:flex;gap:10px;flex-wrap:wrap;">';
        var count = 0;
        related.forEach(function(s) {
          var t = tools.find(function(t2) { return t2.slug === s || t2.url.indexOf(s) >= 0; });
          if (t && count < 4) {
            html += '<a class="mini-card" href="' + t.url + '" style="padding:12px 16px;"><div class="mc-icon">' + (t.icon || '🔧') + '</div><div class="mc-name">' + t.name + '</div></a>';
            count++;
          }
        });
        html += '</div></div>';
        if (count) {
          var container = document.querySelector('.tool-box') || document.querySelector('.container');
          if (container) container.insertAdjacentHTML('afterend', html);
        }
      }).catch(function() {});
    }
  })();

  // ===== 全局导航搜索（注入到导航栏） =====
  (function() {
    var navInner = document.querySelector('.nav-inner');
    if (!navInner) return;

    // 如果当前页面已存在 #toolSearch（如 tools.html），不重复注入
    if (document.getElementById('toolSearch')) return;

    var ph = '搜索工具';
    var common = window.ZT_COMMON;
    if (common) {
      var lang = localStorage.getItem('zentools_lang') || 'zh';
      var dict = common[lang] || common.zh || {};
      ph = dict.searchPlaceholder || ph;
    }

    var wrap = document.createElement('div');
    wrap.className = 'nav-search';
    wrap.innerHTML = '<input type="text" id="toolSearch" class="nav-search-input" placeholder="' + ph + '" autocomplete="off"><div class="nav-search-dropdown" id="searchDropdown"></div>';
    navInner.appendChild(wrap);

    var input = document.getElementById('toolSearch');
    var dd = document.getElementById('searchDropdown');
    var allTools = [];
    var highlightIdx = -1;

    function tName(t, lang) {
      return t['name__' + lang] || t['name__en'] || t.name;
    }
    function tDesc(t, lang) {
      return t['description__' + lang] || t['description__en'] || t.description;
    }

    function loadTools(cb) {
      if (allTools.length) { cb(allTools); return; }
      fetch('/data/tools-data.json').then(function(r) { return r.ok ? r.json() : Promise.reject(); }).then(function(d) {
        if (d && d.tools && d.tools.length) { allTools = d.tools; cb(allTools); }
        else cb([]);
      }).catch(function() { cb([]); });
    }

    function renderDropdown(query) {
      var lang = localStorage.getItem('zentools_lang') || 'zh';
      query = query.trim().toLowerCase();
      if (!query) { dd.classList.remove('show'); return; }

      loadTools(function(tools) {
        var matched = tools.filter(function(t) {
          var name = (tName(t, lang) || '').toLowerCase();
          var desc = (tDesc(t, lang) || '').toLowerCase();
          var cat = (t.category || '').toLowerCase();
          return name.indexOf(query) >= 0 || desc.indexOf(query) >= 0 || cat.indexOf(query) >= 0;
        }).slice(0, 10);

        if (!matched.length) {
          dd.innerHTML = '<div class="nsd-empty">没有找到匹配的工具</div>';
          dd.classList.add('show');
          highlightIdx = -1;
          return;
        }

        highlightIdx = -1;
        dd.innerHTML = matched.map(function(t) {
          var name = tName(t, lang) || t.name;
          var desc = tDesc(t, lang) || '';
          var icon = t.icon || '🔧';
          var cat = t.category || '';
          return '<a class="nsd-item" href="' + t.url + '"><span class="nsd-icon">' + icon + '</span><div class="nsd-info"><div class="nsd-name">' + name + '</div><div class="nsd-desc">' + desc + '</div></div><span class="nsd-cat">' + cat + '</span></a>';
        }).join('');
        dd.classList.add('show');
      });
    }

    input.addEventListener('input', function() {
      renderDropdown(input.value);
    });

    input.addEventListener('keydown', function(e) {
      var items = dd.querySelectorAll('.nsd-item');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlightIdx = Math.min(highlightIdx + 1, items.length - 1);
        items.forEach(function(el, i) { el.classList.toggle('nsd-highlight', i === highlightIdx); });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlightIdx = Math.max(highlightIdx - 1, -1);
        items.forEach(function(el, i) { el.classList.toggle('nsd-highlight', i === highlightIdx); });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (highlightIdx >= 0 && items[highlightIdx]) {
          window.location.href = items[highlightIdx].getAttribute('href');
        }
      } else if (e.key === 'Escape') {
        dd.classList.remove('show');
        input.blur();
      }
    });

    input.addEventListener('blur', function() {
      setTimeout(function() { dd.classList.remove('show'); }, 200);
    });

    input.addEventListener('focus', function() {
      if (input.value.trim()) renderDropdown(input.value);
    });

    document.addEventListener('click', function(e) {
      if (!wrap.contains(e.target)) dd.classList.remove('show');
    });

    // 搜索快捷键 Ctrl+K 或 /
    document.addEventListener('keydown', function(e) {
      if ((e.key === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !e.ctrlKey && !e.metaKey && !['INPUT', 'TEXTAREA'].includes(e.target.tagName))) {
        e.preventDefault();
        input.focus();
        input.select();
      }
    });

    // 语言切换时更新 placeholder
    window.addEventListener('zt-langchange', function(e) {
      if (e.detail && e.detail.dict && e.detail.dict.searchPlaceholder) {
        input.placeholder = e.detail.dict.searchPlaceholder;
      }
    });
  })();

  // ===== 启动 i18n =====
  initLang();
})();
