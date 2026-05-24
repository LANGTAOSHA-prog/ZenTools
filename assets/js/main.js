function renderTools(list){
  const box = document.getElementById('featuredTools');
  if(!box) return;
  box.innerHTML = list.map(tool => `
    <a class="tool-card" href="${tool.url}">
      <div class="icon">${tool.icon || '🧰'}</div>
      <h3>${tool.name}</h3>
      <p>${tool.description}</p>
      <span class="tag">${tool.category}</span>
    </a>
  `).join('');
}

function renderCategories(){
  const box = document.getElementById('categoryGrid');
  if(!box) return;
  box.innerHTML = categoriesData.map(cat => `<a class="category-card" href="categories.html#${encodeURIComponent(cat)}">${cat}</a>`).join('');
}

function initSearch(){
  const input = document.getElementById('searchInput');
  if(!input) return;
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    const filtered = toolsData.filter(t => `${t.name} ${t.category} ${t.description} ${t.keywords || ''}`.toLowerCase().includes(q));
    renderTools(filtered.length ? filtered : toolsData.filter(t=>t.featured));
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const lang = localStorage.getItem('zentools_lang') || 'zh';
  const langSelect = document.getElementById('langSelect');
  if(langSelect){ langSelect.value = lang; langSelect.addEventListener('change', e => applyLanguage(e.target.value)); }
  if(typeof applyLanguage === 'function') applyLanguage(lang);
  renderTools(toolsData.filter(t=>t.featured));
  renderCategories();
  initSearch();
});
