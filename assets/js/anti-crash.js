/* ========================================
   ZenTools 防崩 1.0 — 核心防崩引擎
   ========================================
   加载顺序：此脚本须放在 <head> 中最先加载
   功能：
     1. 全局错误捕获（onerror + unhandledrejection）
     2. JSON 自动校验（拦截 fetch/XMLHttpRequest）
     3. 备用模式自动切换
     4. 页面健康监控
     5. localStorage 备份与恢复
     6. 恢复控制台 API
   ======================================== */

(function() {
  'use strict';

  // ============================================================
  //  命名空间
  // ============================================================
  window.ZT_CRASH = window.ZT_CRASH || {};

  const C = window.ZT_CRASH;

  C.VERSION = '1.0.0';
  C.fallbackMode = false;
  C.errorCount = 0;
  C.errorLog = [];
  C.healthy = true;
  C.recoveryUrl = '/recovery-console.html';

  // ============================================================
  //  配置
  // ============================================================
  const CONFIG = {
    MAX_ERRORS_BEFORE_FALLBACK: 5,       // 连续 N 个错误自动切备用
    ERROR_LOG_LIMIT: 50,                 // 错误日志保留条数
    HEALTH_CHECK_INTERVAL: 30000,        // 健康检查间隔（ms）
    JSON_CHECK_URLS: [                   // 需要校验的 JSON URL
      '/data/tools-data.json',
      '/data/tools.json',
      '/data/translations.json',
      '/data/categories.json'
    ],
    CRITICAL_ELEMENTS: [                 // 首页关键元素选择器
      '#toolsContainer', '#statsBar',
      '#megaMenu', 'nav .logo'
    ],
    BACKUP_KEY: 'zt_backup_data',
    FALLBACK_KEY: 'zt_fallback_active'
  };

  // ============================================================
  //  备用数据（硬编码，保证即使 JSON 全崩也能显示）
  // ============================================================
  C.FALLBACK_DATA = {
    categories: ['PDF工具', '图片工具', '文本工具', '视频工具', '音频工具', '开发工具', '生活工具', 'AI工具'],
    tools: [
      { name: 'PDF 合并', slug: 'pdf-merge', category: 'PDF工具', url: '/pdf/pdf-merge.html', description: '合并多个 PDF 文件', icon: '📄', featured: true },
      { name: '图片压缩', slug: 'image-compress', category: '图片工具', url: '/image/compress.html', description: '压缩 JPG/PNG/WebP', icon: '🖼️', featured: true },
      { name: '文字转语音', slug: 'text-to-speech', category: '音频工具', url: '/audio/text-to-speech.html', description: '文字转语音朗读', icon: '🔊', featured: true },
      { name: 'JSON 格式化', slug: 'json-formatter', category: '开发工具', url: '/json/json-formatter.html', description: '格式化与校验 JSON', icon: '{ }', featured: true },
      { name: '密码生成器', slug: 'password', category: '生活工具', url: '/life/password.html', description: '生成安全随机密码', icon: '🔑', featured: true },
      { name: '汇率换算', slug: 'currency', category: '生活工具', url: '/life/currency.html', description: '实时汇率换算', icon: '💱', featured: true },
      { name: '二维码生成', slug: 'qr-generator', category: '开发工具', url: '/qr/qr-generator.html', description: '生成二维码', icon: '📱', featured: true },
      { name: '视频转 MP3', slug: 'video-to-mp3', category: '视频工具', url: '/video/video-to-mp3.html', description: '从视频提取音频', icon: '🎵', featured: true }
    ]
  };

  // ============================================================
  //  工具函数
  // ============================================================
  function _now() {
    return new Date().toLocaleString('zh-CN', { hour12: false });
  }

  function _safeStr(v) {
    try { return String(v).slice(0, 200); } catch(e) { return '(unknown)'; }
  }

  // ============================================================
  //  1. 全局错误捕获
  // ============================================================
  function _setupErrorHandler() {
    // 同步错误
    window.onerror = function(msg, source, line, col, error) {
      C.errorCount++;
      const record = {
        time: _now(),
        type: 'sync',
        msg: _safeStr(msg),
        source: _safeStr(source),
        line: line || 0,
        col: col || 0
      };
      C.errorLog.push(record);
      if (C.errorLog.length > CONFIG.ERROR_LOG_LIMIT) C.errorLog.shift();

      // 记录到 localStorage 供控制台查看
      _saveErrorLog();
      _checkFallback();
      return true; // 阻止默认浏览器错误提示
    };

    // 异步错误
    window.addEventListener('unhandledrejection', function(e) {
      C.errorCount++;
      let msg = '';
      if (e.reason) {
        msg = e.reason.message || e.reason.statusText || _safeStr(e.reason);
      }
      const record = {
        time: _now(),
        type: 'async',
        msg: msg || 'Unhandled Promise rejection',
        source: '',
        line: 0,
        col: 0
      };
      C.errorLog.push(record);
      if (C.errorLog.length > CONFIG.ERROR_LOG_LIMIT) C.errorLog.shift();
      _saveErrorLog();
      _checkFallback();
      e.preventDefault();
    });

    console.log('[防崩] 全局错误捕获已就绪');
  }

  function _saveErrorLog() {
    try {
      localStorage.setItem('zt_error_log', JSON.stringify(C.errorLog.slice(-30)));
    } catch(e) { /* localStorage 可能满 */ }
  }

  function _checkFallback() {
    if (!C.fallbackMode && C.errorCount >= CONFIG.MAX_ERRORS_BEFORE_FALLBACK) {
      C.fallbackMode = true;
      _activateFallbackMode('连续错误超过阈值 (' + C.errorCount + ' 次)');
    }
  }

  // ============================================================
  //  2. 备用模式
  // ============================================================
  function _activateFallbackMode(reason) {
    console.warn('[防崩] ⚠️ 切换到备用模式，原因:', reason);
    C.fallbackMode = true;

    // 标记到 localStorage 供其他脚本读取
    try {
      localStorage.setItem(CONFIG.FALLBACK_KEY, 'true');
      localStorage.setItem('zt_fallback_reason', _safeStr(reason));
      localStorage.setItem('zt_fallback_time', _now());
    } catch(e) { /* ignore */ }

    // 在页面顶部显示备用模式提示条
    _showFallbackBanner(reason);

    // 替换 window.fetch 使数据加载返回备用数据
    _patchFetchForFallback();

    // 触发自定义事件让其他脚本感知
    window.dispatchEvent(new CustomEvent('zt-fallback-mode', {
      detail: { reason: reason, data: C.FALLBACK_DATA }
    }));
  }

  function _showFallbackBanner(reason) {
    // 避免重复插入
    if (document.getElementById('zt-fallback-banner')) return;

    var banner = document.createElement('div');
    banner.id = 'zt-fallback-banner';
    banner.style.cssText =
      'position:fixed;top:0;left:0;right:0;z-index:99999;' +
      'background:linear-gradient(135deg,#f43f5e,#e11d48);color:#fff;' +
      'padding:10px 16px;text-align:center;font-size:14px;font-weight:600;' +
      'box-shadow:0 4px 20px rgba(244,63,94,0.3);' +
      'display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;';
    banner.innerHTML =
      '⚠️ <span>备用模式已激活 — 部分功能使用内置数据</span>' +
      '<button onclick="ZT_CRASH.dismissFallback()" style="' +
      'background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);' +
      'color:#fff;padding:4px 14px;border-radius:8px;cursor:pointer;font-size:13px;">我知道了</button>' +
      ''; // 恢复控制台已移至本地保留

    // 调整 body padding-top 避免被遮挡
    document.body.prepend(banner);
    document.body.style.paddingTop = '52px';
  }

  C.dismissFallback = function() {
    var banner = document.getElementById('zt-fallback-banner');
    if (banner) {
      banner.style.transition = 'opacity 0.3s';
      banner.style.opacity = '0';
      setTimeout(function() { banner.remove(); document.body.style.paddingTop = ''; }, 300);
    }
  };

  function _patchFetchForFallback() {
    var origFetch = window.fetch;
    window.fetch = function(input, init) {
      var url = typeof input === 'string' ? input : (input.url || '');
      // 拦截 JSON 数据请求，返回备用数据
      for (var i = 0; i < CONFIG.JSON_CHECK_URLS.length; i++) {
        if (url.indexOf(CONFIG.JSON_CHECK_URLS[i]) !== -1) {
          console.warn('[防崩] fetch 被拦截:', url, '→ 返回备用数据');
          return Promise.resolve(new Response(JSON.stringify(C.FALLBACK_DATA), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          }));
        }
      }
      // 其他请求正常发起
      return origFetch.apply(this, arguments);
    };
  }

  // ============================================================
  //  3. 恢复备用模式
  // ============================================================
  C.deactivateFallback = function() {
    // 恢复原始 fetch
    if (window.__origFetch) {
      window.fetch = window.__origFetch;
    }
    C.fallbackMode = false;
    try {
      localStorage.removeItem(CONFIG.FALLBACK_KEY);
      localStorage.removeItem('zt_fallback_reason');
      localStorage.removeItem('zt_fallback_time');
    } catch(e) { /* ignore */ }
    C.dismissFallback();
    console.log('[防崩] 备用模式已关闭，请刷新页面以加载正常数据');
  };

  // ============================================================
  //  4. JSON 数据校验
  // ============================================================
  C.validateJSON = function(jsonStr, name) {
    try {
      var parsed = JSON.parse(jsonStr);
      // 基本结构校验
      if (name && name.indexOf('tools-data') !== -1) {
        if (!parsed.tools || !Array.isArray(parsed.tools)) {
          throw new Error('tools-data.json: 缺少 tools 数组');
        }
        if (!parsed.categories || !Array.isArray(parsed.categories)) {
          throw new Error('tools-data.json: 缺少 categories 数组');
        }
        // 校验每个 tool 的必要字段
        for (var i = 0; i < parsed.tools.length; i++) {
          var t = parsed.tools[i];
          if (!t.name || !t.url) {
            console.warn('[防崩] tools-data.json 中工具 #' + i + ' 缺少 name 或 url');
          }
        }
      }
      if (name && name.indexOf('translations') !== -1) {
        if (!parsed.zh || !parsed.en) {
          throw new Error('translations.json: 缺少 zh 或 en 语言数据');
        }
      }
      return { valid: true, data: parsed, error: null };
    } catch (e) {
      console.error('[防崩] JSON 校验失败:', name, e.message);
      return { valid: false, data: null, error: e.message };
    }
  };

  C.validateAllJSON = function() {
    var results = [];
    var urls = CONFIG.JSON_CHECK_URLS;
    for (var i = 0; i < urls.length; i++) {
      // 只能用同步 xhr 因为在控制台使用
      // 这里返回 Promise 供外部调用
      results.push(
        fetch(urls[i])
          .then(function(r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.text();
          })
          .then(function(text) {
            var name = urls[i].split('/').pop();
            return C.validateJSON(text, name);
          })
          .catch(function(err) {
            return { valid: false, data: null, error: err.message, url: urls[i] };
          })
      );
    }
    return Promise.all(results);
  };

  // ============================================================
  //  5. 页面健康监控
  // ============================================================
  function _checkHealth() {
    if (C.fallbackMode) return; // 已备用模式无需检查

    var allOk = true;
    var selectors = CONFIG.CRITICAL_ELEMENTS;

    for (var i = 0; i < selectors.length; i++) {
      var el = document.querySelector(selectors[i]);
      if (!el) {
        allOk = false;
        console.warn('[防崩] 健康检查: 未找到关键元素', selectors[i]);
      }
    }

    C.healthy = allOk;

    if (!allOk && !C.fallbackMode) {
      console.warn('[防崩] 页面健康检查失败，关键元素缺失');
      // 不自动切换备用，只记录（因为可能是页面还没渲染完）
      // 如果多次检查都失败，再切换
      C._unhealthyCount = (C._unhealthyCount || 0) + 1;
      if (C._unhealthyCount >= 3) {
        _activateFallbackMode('健康检查连续失败 (' + C._unhealthyCount + ' 次)');
      }
    } else {
      C._unhealthyCount = 0;
    }
  }

  // ============================================================
  //  6. localStorage 备份与恢复
  // ============================================================
  C.backupLocalStorage = function() {
    var keys = [
      'zentools_lang', 'zentools_theme',
      'zt_error_log', CONFIG.FALLBACK_KEY,
      'zt_fallback_reason', 'zt_fallback_time'
    ];
    var backup = {};
    for (var i = 0; i < keys.length; i++) {
      try {
        var val = localStorage.getItem(keys[i]);
        if (val !== null) backup[keys[i]] = val;
      } catch(e) { /* ignore */ }
    }
    try {
      localStorage.setItem(CONFIG.BACKUP_KEY, JSON.stringify(backup));
      return { success: true, count: Object.keys(backup).length };
    } catch(e) {
      return { success: false, error: e.message };
    }
  };

  C.restoreLocalStorage = function() {
    try {
      var raw = localStorage.getItem(CONFIG.BACKUP_KEY);
      if (!raw) return { success: false, error: '没有找到备份' };
      var backup = JSON.parse(raw);
      var count = 0;
      for (var key in backup) {
        if (backup.hasOwnProperty(key)) {
          localStorage.setItem(key, backup[key]);
          count++;
        }
      }
      return { success: true, count: count };
    } catch(e) {
      return { success: false, error: e.message };
    }
  };

  C.clearAllData = function() {
    var keys = [
      'zt_error_log', CONFIG.FALLBACK_KEY,
      'zt_fallback_reason', 'zt_fallback_time',
      CONFIG.BACKUP_KEY
    ];
    var count = 0;
    for (var i = 0; i < keys.length; i++) {
      try {
        localStorage.removeItem(keys[i]);
        count++;
      } catch(e) { /* ignore */ }
    }
    return { success: true, count: count };
  };

  // ============================================================
  //  7. 获取系统状态（供控制台使用）
  // ============================================================
  C.getStatus = function() {
    return {
      version: C.VERSION,
      fallbackMode: C.fallbackMode,
      healthy: C.healthy,
      errorCount: C.errorCount,
      errorLog: C.errorLog.slice(-10),
      localStorageBackup: (function() {
        try { return localStorage.getItem(CONFIG.BACKUP_KEY) ? true : false; } catch(e) { return false; }
      })(),
      userAgent: navigator.userAgent.slice(0, 80),
      url: window.location.href
    };
  };

  // ============================================================
  //  8. 友好的控制台命令
  // ============================================================
  C.help = function() {
    console.log('%c=== ZenTools 防崩 1.0 ===', 'font-size:18px;font-weight:bold;color:#00e5ff');
    console.log('可用命令:');
    console.log('  ZT_CRASH.getStatus()          查看系统状态');
    console.log('  ZT_CRASH.validateJSON(str, name)  校验 JSON 字符串');
    console.log('  ZT_CRASH.validateAllJSON()     校验所有 JSON 数据文件');
    console.log('  ZT_CRASH.backupLocalStorage()  备份 localStorage');
    console.log('  ZT_CRASH.restoreLocalStorage() 恢复 localStorage 备份');
    console.log('  ZT_CRASH.clearAllData()        清除防崩系统缓存');
    console.log('  ZT_CRASH.deactivateFallback()  关闭备用模式');
    console.log('  ZT_CRASH.dismissFallback()     关闭备用模式提示条');
    console.log('  ZT_CRASH.errorLog              查看完整错误日志');
    console.log('  ZT_CRASH.FALLBACK_DATA         查看备用数据');
    console.log('  恢复控制台: ' + window.location.origin + C.recoveryUrl);
  };

  console.log('%c[防崩] ZenTools 防崩 ' + C.VERSION + ' 已加载', 'color:#00e5ff;font-weight:bold');

  // ============================================================
  //  初始化
  // ============================================================
  function init() {
    // 检查是否上次处于备用模式
    try {
      if (localStorage.getItem(CONFIG.FALLBACK_KEY) === 'true') {
        console.warn('[防崩] 检测到上次为备用模式退出，恢复备用数据');
        C.fallbackMode = true;
      }
    } catch(e) { /* ignore */ }

    _setupErrorHandler();

    // 保存原始 fetch（供 deactivateFallback 恢复）
    window.__origFetch = window.fetch;

    // 延迟执行健康检查（等页面渲染）
    setTimeout(function() {
      _checkHealth();
    }, 3000);

    // 定期健康检查
    setInterval(_checkHealth, CONFIG.HEALTH_CHECK_INTERVAL);

    // 页面关闭前备份重要状态
    window.addEventListener('beforeunload', function() {
      // 只备份非敏感数据
      C.backupLocalStorage();
    });
  }

  // DOM 就绪后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
