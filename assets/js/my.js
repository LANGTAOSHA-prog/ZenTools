// my.js - ZenTools 用户中心逻辑
(function() {
  'use strict';

  var currentTab = 'favorites';
  var currentGroup = 'all';
  var currentHotType = 'editor';
  var toolsData = null;
  var currentLang = localStorage.getItem('zentools_lang') || 'zh';

  // 分类图标映射
  var CAT_ICONS = {
    'PDF工具':'📄','图片工具':'🖼️','AI工具':'🤖','视频工具':'🎬','音频工具':'🎵',
    '文本工具':'📝','开发工具':'💻','生活工具':'🌍','金融工具':'💰','SEO工具':'🔍',
    '设计工具':'🎨','办公工具':'💼','教育工具':'📚'
  };

  function tName(t, l) { return t['name__'+l] || t.name; }
  function tDesc(t, l) { return t['description__'+l] || t.description || ''; }
  function getI18n(key) { return (window.ZT_PAGE[currentLang] || window.ZT_PAGE.zh)[key] || key; }

  function loadToolsData(cb) {
    if (toolsData) { cb(); return; }
    fetch('/data/tools-data.json').then(function(r) {
      return r.ok ? r.json() : Promise.reject();
    }).then(function(d) { toolsData = (d && d.tools) ? d.tools : []; cb(); })
      .catch(function() { toolsData = []; cb(); });
  }

  function findTool(url) {
    return toolsData.find(function(t) { return t.url === url; });
  }

  // ===== Tab 切换 =====
  document.querySelectorAll('.my-tab').forEach(function(btn) {
    btn.addEventListener('click', function() {
      currentTab = this.getAttribute('data-tab');
      document.querySelectorAll('.my-tab').forEach(function(t) { t.classList.remove('active'); });
      this.classList.add('active');
      document.querySelectorAll('.my-panel').forEach(function(p) { p.classList.remove('active'); });
      var panel = document.getElementById('panel' + currentTab.charAt(0).toUpperCase() + currentTab.slice(1));
      if (panel) panel.classList.add('active');
      renderCurrentPanel();
    });
  });

  // ===== 收藏面板 =====
  function renderFavorites() {
    loadToolsData(function() {
      var favs = ZT.track._fav;
      var groups = ZT.user.getFavGroups();
      var filtered = currentGroup === 'all' ? favs : favs.filter(function(f) { return (f.group||'默认') === currentGroup; });

      // 分组按钮
      var groupBar = document.getElementById('favGroupBar');
      if (groupBar) {
        var html = '<button class="my-group-btn ' + (currentGroup==='all'?'active':'') + '" data-group="all">' + getI18n('groupAll') + '</button>';
        groups.forEach(function(g) {
          html += '<button class="my-group-btn ' + (currentGroup===g?'active':'') + '" data-group="' + g + '">' + g + '</button>';
        });
        groupBar.innerHTML = html;
        groupBar.querySelectorAll('.my-group-btn').forEach(function(b) {
          b.addEventListener('click', function() {
            currentGroup = this.getAttribute('data-group');
            renderFavorites();
          });
        });
      }

      var list = document.getElementById('favList');
      var empty = document.getElementById('favEmpty');
      if (!filtered.length) {
        if (list) list.innerHTML = '';
        if (empty) empty.style.display = 'block';
        return;
      }
      if (empty) empty.style.display = 'none';
      if (!list) return;

      list.innerHTML = filtered.map(function(f) {
        var t = findTool(f.url);
        var name = t ? tName(t, currentLang) : f.name;
        var icon = t ? (t.icon || '🔧') : '🔧';
        var group = f.group || '默认';
        var timeStr = new Date(f.time).toLocaleDateString();
        return '<a class="my-item" href="' + f.url + '">' +
          '<span class="mi-icon">' + icon + '</span>' +
          '<div class="mi-info"><div class="mi-name">' + name + '</div>' +
          '<div class="mi-meta">' + timeStr + '</div></div>' +
          '<span class="mi-group-tag">' + group + '</span>' +
          '<div class="mi-actions">' +
          '<button class="mi-btn" title="' + getI18n('moveFavTo') + '" data-move="' + f.url + '">📁</button>' +
          '<button class="mi-btn" title="' + getI18n('removeFav') + '" data-remove="' + f.url + '">✕</button>' +
          '</div></a>';
      }).join('');

      // 绑定按钮
      list.querySelectorAll('[data-remove]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          var url = this.getAttribute('data-remove');
          ZT.track.toggleFav(findTool(url) ? ZT.track._getToolName() : '');
          // 直接从 _fav 中移除
          ZT.track._fav = ZT.track._fav.filter(function(f) { return f.url !== url; });
          localStorage.setItem(ZT.track._key_fav, JSON.stringify(ZT.track._fav));
          renderFavorites();
        });
      });
      list.querySelectorAll('[data-move]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          var url = this.getAttribute('data-move');
          showMoveDialog(url);
        });
      });
    });
  }

  function showMoveDialog(url) {
    var groups = ZT.user.getFavGroups();
    var lang = currentLang;
    var title = getI18n('moveFavTo');
    var overlay = document.createElement('div');
    overlay.className = 'my-modal-overlay';
    var html = '<div class="my-modal"><h3>' + title + '</h3><div class="my-modal-list">';
    groups.forEach(function(g) {
      html += '<button class="my-modal-item" data-group="' + g + '">' + g + '</button>';
    });
    html += '</div>';
    html += '<div class="my-modal-add"><input type="text" id="newGroupName" placeholder="' + getI18n('addGroupPlaceholder') + '"><button id="addAndMove">' + getI18n('addGroup') + '</button></div>';
    html += '<button class="my-modal-close">' + getI18n('cancel') + '</button></div>';
    overlay.innerHTML = html;
    document.body.appendChild(overlay);
    overlay.querySelectorAll('[data-group]').forEach(function(b) {
      b.addEventListener('click', function() {
        ZT.user.moveFavToGroup(url, this.getAttribute('data-group'));
        document.body.removeChild(overlay);
        renderFavorites();
      });
    });
    var addBtn = overlay.querySelector('#addAndMove');
    if (addBtn) {
      addBtn.addEventListener('click', function() {
        var input = overlay.querySelector('#newGroupName');
        var name = input.value.trim();
        if (name) {
          ZT.user.addFavGroup(name);
          ZT.user.moveFavToGroup(url, name);
          document.body.removeChild(overlay);
          renderFavorites();
        }
      });
    }
    var closeBtn = overlay.querySelector('.my-modal-close');
    if (closeBtn) closeBtn.addEventListener('click', function() { document.body.removeChild(overlay); });
  }

  // ===== 历史面板 =====
  function renderHistory() {
    var list = document.getElementById('historyList');
    var empty = document.getElementById('historyEmpty');
    if (!list) return;

    if (!ZT.track._recent.length) {
      list.innerHTML = '';
      if (empty) empty.style.display = 'block';
      return;
    }
    if (empty) empty.style.display = 'none';

    loadToolsData(function() {
      var grouped = ZT.user.getRecentGrouped();
      var days = Object.keys(grouped).sort().reverse();
      list.innerHTML = days.map(function(day) {
        var dayLabel = formatDateLabel(day);
        var items = grouped[day].map(function(r) {
          var t = findTool(r.url);
          var name = t ? tName(t, currentLang) : r.name;
          var icon = t ? (t.icon || '🔧') : '🔧';
          var timeStr = new Date(r.time).toLocaleTimeString(currentLang==='zh'?'zh-CN':currentLang, {hour:'2-digit',minute:'2-digit'});
          return '<a class="my-item" href="' + r.url + '">' +
            '<span class="mi-icon">' + icon + '</span>' +
            '<div class="mi-info"><div class="mi-name">' + name + '</div>' +
            '<div class="mi-meta">' + timeStr + '</div></div></a>';
        }).join('');
        return '<div class="my-date-group"><div class="my-date-label">' + dayLabel + '</div>' + items + '</div>';
      }).join('');
    });
  }

  function formatDateLabel(dateStr) {
    var today = new Date().toISOString().slice(0,10);
    var yesterday = new Date(Date.now()-86400000).toISOString().slice(0,10);
    if (dateStr === today) return getI18n('today');
    if (dateStr === yesterday) return getI18n('yesterday');
    var d = new Date(dateStr);
    return d.toLocaleDateString(currentLang==='zh'?'zh-CN':currentLang==='ja'?'ja-JP':currentLang==='vi'?'vi-VN':'en-US');
  }

  // ===== 订阅面板 =====
  function renderSubscriptions() {
    loadToolsData(function() {
      var subs = ZT.user.getSubscriptions();
      var cats = {};
      toolsData.forEach(function(t) { cats[t.category] = (cats[t.category]||0)+1; });

      var grid = document.getElementById('subsGrid');
      if (!grid) return;
      var catNames = Object.keys(cats);
      grid.innerHTML = catNames.map(function(cat) {
        var count = cats[cat];
        var isSubbed = subs.categories.indexOf(cat) >= 0;
        var icon = CAT_ICONS[cat] || '🔧';
        return '<div class="my-subs-card ' + (isSubbed?'subscribed':'') + '" data-cat="' + cat + '">' +
          '<div class="msc-icon">' + icon + '</div>' +
          '<div class="msc-name">' + cat + '</div>' +
          '<div class="msc-count">' + count + ' ' + getI18n('cntTools') + '</div>' +
          (isSubbed ? '<span class="msc-check">✓</span>' : '') +
          '</div>';
      }).join('');

      grid.querySelectorAll('.my-subs-card').forEach(function(card) {
        card.addEventListener('click', function() {
          var cat = this.getAttribute('data-cat');
          ZT.user.toggleCategorySubscription(cat);
          renderSubscriptions();
        });
      });

      // 新工具提醒
      renderNewToolsReminder(subs);
    });
  }

  function renderNewToolsReminder(subs) {
    var section = document.getElementById('newToolsSection');
    var list = document.getElementById('newToolsList');
    if (!section || !list) return;

    if (!subs.categories.length) {
      section.style.display = 'none';
      return;
    }
    var newTools = toolsData.filter(function(t) {
      return t.new === true && subs.categories.indexOf(t.category) >= 0 && subs.dismissed.indexOf(t.slug) < 0;
    });
    if (!newTools.length) {
      section.style.display = 'none';
      return;
    }
    section.style.display = 'block';
    list.innerHTML = newTools.map(function(t) {
      return '<a class="my-item" href="' + t.url + '">' +
        '<span class="mi-icon">' + (t.icon||'🔧') + '</span>' +
        '<div class="mi-info"><div class="mi-name">' + tName(t, currentLang) +
        ' <span class="my-new-badge">' + getI18n('newBadge') + '</span></div>' +
        '<div class="mi-meta">' + tDesc(t, currentLang) + '</div></div>' +
        '<button class="mi-btn" data-dismiss="' + t.slug + '">✕</button></a>';
    }).join('');

    list.querySelectorAll('[data-dismiss]').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        ZT.user.dismissNewTool(this.getAttribute('data-dismiss'));
        renderSubscriptions();
      });
    });
  }

  // ===== 热门榜单面板 =====
  function renderHotlist() {
    loadToolsData(function() {
      var list = document.getElementById('hotList');
      if (!list) return;

      if (currentHotType === 'editor') {
        var featured = toolsData.filter(function(t) { return t.featured === true; });
        list.innerHTML = featured.slice(0,20).map(function(t, i) {
          return '<a class="my-item" href="' + t.url + '">' +
            '<span class="hot-rank ' + (i<3?'r'+(i+1):'r4to10') + '">' + (i+1) + '</span>' +
            '<span class="mi-icon">' + (t.icon||'🔧') + '</span>' +
            '<div class="mi-info"><div class="mi-name">' + tName(t, currentLang) + '</div>' +
            '<div class="mi-meta">' + tDesc(t, currentLang) + '</div></div></a>';
        }).join('');
      } else {
        var myTop = ZT.user.getMyTop(20);
        if (!myTop.length) {
          list.innerHTML = '<div class="my-empty" style="display:block">' + getI18n('noClicks') + '</div>';
          return;
        }
        list.innerHTML = myTop.map(function(e, i) {
          var t = findTool(e.url);
          var name = t ? tName(t, currentLang) : e.url.split('/').pop();
          var icon = t ? (t.icon||'🔧') : '🔧';
          return '<a class="my-item" href="' + e.url + '">' +
            '<span class="hot-rank ' + (i<3?'r'+(i+1):'r4to10') + '">' + (i+1) + '</span>' +
            '<span class="mi-icon">' + icon + '</span>' +
            '<div class="mi-info"><div class="mi-name">' + name + '</div>' +
            '<div class="mi-meta">' + e.count + ' ' + getI18n('clicksUnit') + '</div></div></a>';
        }).join('');
      }
    });
  }

  // 热门子 Tab
  document.querySelectorAll('.my-hot-tab').forEach(function(btn) {
    btn.addEventListener('click', function() {
      currentHotType = this.getAttribute('data-type');
      document.querySelectorAll('.my-hot-tab').forEach(function(t) { t.classList.remove('active'); });
      this.classList.add('active');
      renderHotlist();
    });
  });

  // ===== 操作按钮 =====
  var clearFavsBtn = document.getElementById('clearFavsBtn');
  if (clearFavsBtn) clearFavsBtn.addEventListener('click', function() {
    if (confirm(getI18n('clearFavsConfirm'))) { ZT.user.clearAllFavs(); renderFavorites(); }
  });
  var clearHistoryBtn = document.getElementById('clearHistoryBtn');
  if (clearHistoryBtn) clearHistoryBtn.addEventListener('click', function() {
    if (confirm(getI18n('clearHistoryConfirm'))) { ZT.user.clearRecent(); renderHistory(); }
  });
  var exportBtn = document.getElementById('exportBtn');
  if (exportBtn) exportBtn.addEventListener('click', function() { ZT.user.exportAll(); });
  var importBtn = document.getElementById('importBtn');
  if (importBtn) importBtn.addEventListener('click', function() {
    var input = document.createElement('input');
    input.type = 'file'; input.accept = '.json';
    input.addEventListener('change', function(e) {
      var file = e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(ev) {
        if (ZT.user.importAll(ev.target.result)) { renderCurrentPanel(); alert(getI18n('importSuccess')); }
        else { alert(getI18n('importFail')); }
      };
      reader.readAsText(file);
    });
    input.click();
  });

  function renderCurrentPanel() {
    switch(currentTab) {
      case 'favorites': renderFavorites(); break;
      case 'history': renderHistory(); break;
      case 'subscriptions': renderSubscriptions(); break;
      case 'hotlist': renderHotlist(); break;
    }
  }

  // 语言切换
  window.addEventListener('zt-langchange', function(e) {
    currentLang = e.detail.lang;
    renderCurrentPanel();
  });

  // URL hash 跳转到指定 Tab
  var hash = window.location.hash.replace('#','');
  if (hash && ['favorites','history','subscriptions','hotlist'].indexOf(hash) >= 0) {
    var tabBtn = document.querySelector('.my-tab[data-tab="' + hash + '"]');
    if (tabBtn) tabBtn.click();
  }

  // 初始化
  renderCurrentPanel();
})();
