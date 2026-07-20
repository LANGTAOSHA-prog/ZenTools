/* ============================================================
 * ZenTools 统一工具标签 & 多维度筛选模块
 * 暴露全局 window.ZT，供 index.html / tools.html 复用。
 * 依赖：每个工具含 t.ai = { free, processing, languages, batch, export }
 * ============================================================ */
(function () {
  'use strict';
  var ZT = (window.ZT = window.ZT || {});

  /* 五类统一标签定义（四语） */
  var TAG = {
    local:  { zh: '本地处理', en: 'Local', ja: 'ローカル', vi: 'Local', icon: '🖥️', cls: 'zt-local' },
    free:   { zh: '免费',     en: 'Free',  ja: '無料',     vi: 'Miễn phí', icon: '🆓', cls: 'zt-free' },
    multi:  { zh: '多语种',   en: 'Multi', ja: '多言語',   vi: 'Đa ngôn', icon: '🌐', cls: 'zt-multi' },
    export: { zh: '导出格式', en: 'Export', ja: '書出し', vi: 'Xuất', icon: '📤', cls: 'zt-export' },
    batch:  { zh: '批量支持', en: 'Batch', ja: '一括',     vi: 'Hàng loạt', icon: '🗂️', cls: 'zt-batch' }
  };

  function aiOf(t) { return t.ai || {}; }
  function langs(t) { var a = aiOf(t); return a.languages || []; }

  /* 返回该工具应展示的标签数组 [{label, icon, cls}] */
  ZT.tagsFor = function (t, lang) {
    lang = lang || 'zh';
    var a = aiOf(t);
    var out = [];
    if (a.processing === 'browser-local') out.push(TAG.local);
    if (a.free === true) out.push(TAG.free);
    if (langs(t).length >= 2) out.push(TAG.multi);
    if (a.export && a.export.length) out.push(TAG.export);
    if (a.batch === true) out.push(TAG.batch);
    return out.map(function (d) {
      return { label: d[lang] || d.zh, icon: d.icon, cls: d.cls };
    });
  };

  /* 直接生成标签 HTML 片段（无标签时返回空串） */
  ZT.tagHtml = function (t, lang) {
    var ts = ZT.tagsFor(t, lang);
    if (!ts.length) return '';
    var html = '<div class="zt-tags">';
    for (var i = 0; i < ts.length; i++) {
      html += '<span class="zt-tag ' + ts[i].cls + '">' + ts[i].icon + ' ' + ts[i].label + '</span>';
    }
    return html + '</div>';
  };

  /* 导出格式标签（用于卡片副信息，如 "PDF · Word"） */
  ZT.exportLabel = function (t, lang) {
    var a = aiOf(t);
    if (!a.export || !a.export.length) return '';
    return a.export.join(' · ');
  };

  /* 多维度筛选匹配
   * filters = { price:'all'|'free'|'paid',
   *             local:'all'|'local'|'cloud',
   *             type:'all'|'<category>',
   *             batch:'all'|'yes'|'no' }
   * 返回 true 表示命中（应展示）。
   */
  ZT.matchFilters = function (t, filters) {
    filters = filters || {};
    var a = aiOf(t);
    if (filters.price && filters.price !== 'all') {
      if (filters.price === 'free' && a.free !== true) return false;
      if (filters.price === 'paid' && a.free === true) return false;
    }
    if (filters.local && filters.local !== 'all') {
      var isLocal = a.processing === 'browser-local';
      if (filters.local === 'local' && !isLocal) return false;
      if (filters.local === 'cloud' && isLocal) return false;
    }
    if (filters.type && filters.type !== 'all') {
      if (t.category !== filters.type) return false;
    }
    if (filters.batch && filters.batch !== 'all') {
      var isBatch = a.batch === true;
      if (filters.batch === 'yes' && !isBatch) return false;
      if (filters.batch === 'no' && isBatch) return false;
    }
    return true;
  };

  /* 关键词命中（用于搜索与场景预筛）
   * - 单串：任一字段包含完整 q 即命中
   * - 多词（空格分隔）：任一 token(>=2字) 命中即命中（OR）
   */
  ZT.kwHit = function (t, q, lang) {
    if (!q) return true;
    q = (q || '').toLowerCase().trim();
    if (!q) return true;
    var a = aiOf(t);
    var fields = [t.name, t['name__' + (lang || 'zh')], t.description, t.keywords || '', t.category || ''];
    if (a.export) fields = fields.concat(a.export);
    for (var i = 0; i < fields.length; i++) {
      if (fields[i] && fields[i].toLowerCase().indexOf(q) >= 0) return true;
    }
    var toks = q.split(/\s+/).filter(function (x) { return x.length >= 2; });
    if (toks.length > 1) {
      for (var j = 0; j < toks.length; j++) {
        for (var k = 0; k < fields.length; k++) {
          if (fields[k] && fields[k].toLowerCase().indexOf(toks[j]) >= 0) return true;
        }
      }
    }
    return false;
  };

  /* 场景预设：首页 → tools.html?scenario=xxx
   * slugs（若提供）优先用于精确精选；否则用 type+kw 兜底。
   */
  ZT.SCENARIOS = {
    media: {
      title: { zh: '自媒体素材', en: 'Creator Kit', ja: 'メディア素材', vi: 'Nguyên liệu' },
      slugs: ['image-compress', 'image-resize', 'image-watermark', 'remove-bg', 'collage',
              'mp4-to-gif', 'video-to-audio', 'image-convert', 'ocr', 'text-to-speech',
              'ai-writing', 'imgtopdf', 'pdf-watermark', 'pdf-split']
    },
    resume: {
      title: { zh: '简历 PDF', en: 'Resume PDF', ja: '履歴書PDF', vi: 'CV PDF' },
      slugs: ['ai-resume', 'pdf-merge', 'pdf-compress', 'pdf-to-word', 'pdf-split',
              'imgtopdf', 'ocr', 'image-compress']
    },
    frontend: {
      title: { zh: '前端开发工具', en: 'Frontend Dev', ja: 'フロント開発', vi: 'Dev Frontend' },
      type: '开发工具', kw: ''
    },
    thesis: {
      title: { zh: '学生论文格式处理', en: 'Thesis Format', ja: '論文フォーマット', vi: 'Định dạng luận văn' },
      type: 'PDF工具', kw: '论文 格式 页码 页眉 目录 排版'
    }
  };

  ZT.getScenario = function (key) { return ZT.SCENARIOS[key] || null; };
  ZT.scenarioSlugs = function (key) { var s = ZT.SCENARIOS[key]; return s && s.slugs ? s.slugs : null; };
})();
