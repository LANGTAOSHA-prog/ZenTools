// loader.js - ZenTools 2.1 core utilities (stable, crash‑proof)

/**
 * Theme handling (dark / light)
 */
function initTheme() {
  const theme = localStorage.getItem('zh_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('zh_theme', next);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = next === 'dark' ? '☀️' : '🌙';
}

/**
 * 最近使用记录（最多 5 条）
 */
function loadRecent() {
  const list = JSON.parse(localStorage.getItem('zentools_recent') || '[]');
  const container = document.getElementById('recentList');
  const section = document.getElementById('recentSection');
  if (!list.length) {
    if (section) section.classList.remove('visible');
    return;
  }
  if (section) section.classList.add('visible');
  if (container) {
    container.innerHTML = list
      .map(url => `<a href="${url}">${url.split('/').pop().replace('.html','')}</a>`)
      .join('');
  }
}
function addRecent(url) {
  let list = JSON.parse(localStorage.getItem('zentools_recent') || '[]');
  list = list.filter(item => item !== url);
  list.unshift(url);
  if (list.length > 5) list = list.slice(0, 5);
  localStorage.setItem('zentools_recent', JSON.stringify(list));
  loadRecent();
}

/**
 * 分类与工具渲染（统一数据驱动）
 */
const CATEGORY_ICONS = {
  'AI工具': '🤖',
  '图片工具': '🖼️',
  'PDF工具': '📄',
  '文本工具': '📝',
  '视频工具': '🎬',
  '音频工具': '🔊',
  '开发工具': '💻',
  'SEO工具': '🔍',
  '办公工具': '📎',
  '生活工具': '🌍',
  '金融工具': '💰',
  '教育工具': '📚'
};

function renderCategories(categories) {
  const ribbon = document.getElementById('categoryRibbon');
  if (!ribbon) return;
  let html = '';
  for (const cat of categories) {
    const icon = CATEGORY_ICONS[cat] || '🔧';
    let path = '';
    if (cat === 'AI工具') path = '/ai/index.html';
    else if (cat === '图片工具') path = '/image/index.html';
    else if (cat === 'PDF工具') path = '/pdf/index.html';
    else if (cat === '文本工具') path = '/text/index.html';
    else if (cat === '视频工具') path = '/video/index.html';
    else if (cat === '音频工具') path = '/audio/index.html';
    else if (cat === '开发工具') path = '/dev/index.html';
    else if (cat === '生活工具') path = '/life/index.html';
    else path = '/categories.html#' + encodeURIComponent(cat);
    html += `<a href="${path}"><span class="cat-icon">${icon}</span> ${cat}</a>`;
  }
  ribbon.innerHTML = html;
}

function renderTools(tools) {
  const grid = document.getElementById('toolsGrid');
  if (!grid) return;
  if (!tools || !tools.length) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:var(--muted);">暂无工具</div>';
    return;
  }
  const list = tools.filter(t => t.featured !== false).slice(0, 8);
  let html = '';
  for (const t of list) {
    const url = t.url && t.url !== '#' ? t.url : '#';
    const target = url !== '#' ? '_blank' : '';
    html += `<a class="tool-card" href="${url}" target="${target}" onclick="addRecent('${url}')"><span class="emoji">${t.icon || '🔧'}</span><div class="name">${t.name}</div><div class="desc">${t.description || ''}</div><span class="tag">${t.category || '工具'}</span></a>`;
  }
  grid.innerHTML = html;

  // 热门工具
  const hot = document.getElementById('hotScroll');
  if (!hot) return;
  const hotTools = tools.filter(t => t.featured === true).slice(0, 8);
  let hotHtml = '';
  for (const t of hotTools) {
    const url = t.url && t.url !== '#' ? t.url : '#';
    const target = url !== '#' ? '_blank' : '';
    hotHtml += `<a class="hot-item" href="${url}" target="${target}" onclick="addRecent('${url}')"><span class="emoji">${t.icon || '🔧'}</span><div class="name">${t.name}</div><span class="tag">${t.category || ''}</span></a>`;
  }
  hot.innerHTML = hotHtml || '<div style="text-align:center;padding:20px;color:var(--muted);width:100%;">暂无热门工具</div>';
}

/**
 * 加载全局数据（tools-data.json）
 */
function loadData() {
  fetch('/data/tools-data.json')
    .then(r => r.ok ? r.json() : Promise.reject('HTTP ' + r.status))
    .then(data => {
      if (data?.categories) renderCategories(data.categories);
      if (data?.tools) renderTools(data.tools);
    })
    .catch(() => {
      // 兜底示例数据，保证页面不崩溃
      renderTools([
        { name: 'PDF 合并', url: '/pdf/merge.html', icon: '📄', category: 'PDF工具', featured: true },
        { name: '图片压缩', url: '/image/compress.html', icon: '📦', category: '图片工具', featured: true },
        { name: '文字转语音', url: '#', icon: '🔊', category: '音频工具' }
      ]);
    });
}

/**
 * 页面初始化
 */
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  loadRecent();
  loadData();
});