const translations = {
  zh: {
    navTools: "工具",
    navAI: "AI工具",
    navGuides: "教程",
    navFAQ: "常见问题",
    eyebrow: "免费 · 在线 · 即开即用",
    heroTitle: "一个网页解决日常工具需求",
    heroDesc: "ZenTools 提供 PDF、图片、AI、视频、音频、文字、开发、生活和营销工具，适合办公、学习、创作和网站运营。",
    startUse: "开始使用",
    viewGuides: "查看教程",
    toolsTitle: "热门在线工具",
    toolsDesc: "常用工具快速入口，适合办公、学习、创作和网站运营。",
    aiTitle: "AI 工具专区",
    aiDesc: "收录 AI 写作、AI PPT、AI 图片、AI 视频和 AI 办公工具。",
    guidesTitle: "工具图文教程",
    guidesDesc: "不会用也没关系，跟着教程一步一步操作。",
    faqTitle: "常见问题",
    faqDesc: "关于 ZenTools 的使用、安全和功能说明。"
  },
  en: {
    navTools: "Tools",
    navAI: "AI Tools",
    navGuides: "Guides",
    navFAQ: "FAQ",
    eyebrow: "Free · Online · Ready to Use",
    heroTitle: "One page for everyday online tools",
    heroDesc: "ZenTools provides PDF, image, AI, video, audio, text, developer, life and marketing tools for work, study, creation and website operation.",
    startUse: "Start Now",
    viewGuides: "View Guides",
    toolsTitle: "Popular Online Tools",
    toolsDesc: "Quick access to useful tools for work, study, creation and website management.",
    aiTitle: "AI Tools",
    aiDesc: "AI writing, AI PPT, AI image, AI video and AI office tools.",
    guidesTitle: "Tool Guides",
    guidesDesc: "Follow step-by-step guides to use each tool easily.",
    faqTitle: "FAQ",
    faqDesc: "Questions about usage, safety and features."
  },
  ja: {
    navTools: "ツール",
    navAI: "AIツール",
    navGuides: "ガイド",
    navFAQ: "よくある質問",
    eyebrow: "無料 · オンライン · すぐ使える",
    heroTitle: "日常ツールを1つのページで",
    heroDesc: "ZenTools は PDF、画像、AI、動画、音声、文字、開発、生活、マーケティング向けの便利なオンラインツールを提供します。",
    startUse: "使い始める",
    viewGuides: "ガイドを見る",
    toolsTitle: "人気オンラインツール",
    toolsDesc: "仕事、学習、制作、サイト運営に役立つツールをすぐに使えます。",
    aiTitle: "AIツール",
    aiDesc: "AI文章作成、AI PPT、AI画像、AI動画、AIオフィスツールを掲載。",
    guidesTitle: "ツールガイド",
    guidesDesc: "手順に沿って簡単に使えます。",
    faqTitle: "よくある質問",
    faqDesc: "ZenTools の使い方、安全性、機能について。"
  },
  vi: {
    navTools: "Công cụ",
    navAI: "Công cụ AI",
    navGuides: "Hướng dẫn",
    navFAQ: "FAQ",
    eyebrow: "Miễn phí · Trực tuyến · Dễ sử dụng",
    heroTitle: "Một trang cho các công cụ hằng ngày",
    heroDesc: "ZenTools cung cấp công cụ PDF, hình ảnh, AI, video, âm thanh, văn bản, lập trình, đời sống và marketing.",
    startUse: "Bắt đầu",
    viewGuides: "Xem hướng dẫn",
    toolsTitle: "Công cụ phổ biến",
    toolsDesc: "Truy cập nhanh các công cụ hữu ích cho công việc, học tập và sáng tạo.",
    aiTitle: "Khu công cụ AI",
    aiDesc: "AI viết nội dung, AI PPT, AI hình ảnh, AI video và công cụ văn phòng AI.",
    guidesTitle: "Hướng dẫn sử dụng",
    guidesDesc: "Làm theo từng bước để sử dụng dễ dàng.",
    faqTitle: "Câu hỏi thường gặp",
    faqDesc: "Thông tin về cách dùng, bảo mật và chức năng."
  }
};

async function loadJSON(path, fallback) {
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error("JSON load failed");
    return await res.json();
  } catch (err) {
    console.warn(path + " 加载失败，使用备用数据。");
    return fallback;
  }
}

const fallbackCategories = [
  { name: "PDF 工具", slug: "pdf", icon: "PDF", color: "#f43145", desc: "合并、压缩、转换 PDF" },
  { name: "图片工具", slug: "image", icon: "IMG", color: "#27c27b", desc: "压缩、裁剪、格式转换" },
  { name: "AI 工具", slug: "ai", icon: "AI", color: "#8b4cff", desc: "AI写作、PPT、图片、视频" },
  { name: "视频工具", slug: "video", icon: "▶", color: "#8a45ff", desc: "视频转换、压缩、提取" },
  { name: "音频工具", slug: "audio", icon: "♪", color: "#3278ff", desc: "音频转换、裁剪、提取" },
  { name: "文字工具", slug: "text", icon: "T", color: "#2d8cff", desc: "字数统计、文本处理" },
  { name: "开发工具", slug: "dev", icon: "</>", color: "#22b978", desc: "JSON、Base64、代码工具" },
  { name: "生活工具", slug: "life", icon: "☁", color: "#ffb324", desc: "换算、时间、计算器" }
];

const fallbackTools = [
  { name: "PDF 合并工具", slug: "pdf-merge", category: "pdf", description: "将多个 PDF 文件快速合并成一个文件。", url: "./tools/pdf-merge.html", featured: true },
  { name: "图片压缩工具", slug: "image-compress", category: "image", description: "压缩 JPG、PNG、WebP 图片，减少文件体积。", url: "./tools/image-compress.html", featured: true },
  { name: "视频转 MP3", slug: "video-to-mp3", category: "video", description: "从视频中提取音频，适合剪辑和素材整理。", url: "./tools/video-to-mp3.html", featured: true },
  { name: "JSON 格式化", slug: "json-format", category: "dev", description: "格式化、压缩和检查 JSON 数据。", url: "./tools/json-format.html", featured: true },
  { name: "Base64 编码解码", slug: "base64", category: "dev", description: "快速进行 Base64 编码和解码。", url: "./tools/base64.html", featured: true },
  { name: "字数统计", slug: "word-counter", category: "text", description: "统计文字数量、字符数和段落数量。", url: "./tools/word-counter.html", featured: true },
  { name: "二维码生成器", slug: "qr-code", category: "marketing", description: "快速生成链接、文本、联系方式二维码。", url: "./tools/qr-code.html", featured: true },
  { name: "汇率换算", slug: "currency", category: "life", description: "适合旅行、购物和跨境结算参考。", url: "./tools/currency.html", featured: true },

  { name: "AI 写作工具", slug: "ai-writing", category: "ai", description: "适合文章、标题、文案和邮件写作。", url: "./tools/ai-writing.html", featured: true },
  { name: "AI PPT 工具", slug: "ai-ppt", category: "ai", description: "快速生成演示文稿和汇报大纲。", url: "./tools/ai-ppt.html", featured: true },
  { name: "AI 图片工具", slug: "ai-image", category: "ai", description: "生成图片、海报、插画和封面图。", url: "./tools/ai-image.html", featured: true },
  { name: "AI 视频工具", slug: "ai-video", category: "ai", description: "生成短视频、广告视频和素材片段。", url: "./tools/ai-video.html", featured: true }
];

function applyLanguage(lang) {
  const dict = translations[lang] || translations.zh;
  document.documentElement.lang = lang === "zh" ? "zh-CN" : lang;
  document.documentElement.dataset.lang = lang;

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) el.textContent = dict[key];
  });

  const search = document.getElementById("toolSearch");
  if (search) {
    search.placeholder =
      lang === "zh"
        ? "搜索工具，例如：PDF、图片压缩、AI写作"
        : "Search tools, e.g. PDF, image compress, AI writing";
  }
}

function getLangFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("lang") || localStorage.getItem("zentools_lang") || "zh";
}

function renderCategories(categories) {
  const box = document.getElementById("categoryPreview");
  if (!box) return;

  box.innerHTML = categories.map(item => `
    <a href="./tools/${item.slug}-tools.html" class="category-card">
      <div class="category-icon" style="background:${item.color}">${item.icon}</div>
      <h3>${item.name}</h3>
      <p>${item.desc}</p>
    </a>
  `).join("");
}

function renderTools(tools) {
  const toolsGrid = document.getElementById("toolsGrid");
  const aiGrid = document.getElementById("aiGrid");

  if (toolsGrid) {
    toolsGrid.innerHTML = tools
      .filter(tool => tool.category !== "ai")
      .slice(0, 8)
      .map(toolCard)
      .join("");
  }

  if (aiGrid) {
    aiGrid.innerHTML = tools
      .filter(tool => tool.category === "ai")
      .slice(0, 8)
      .map(toolCard)
      .join("");
  }
}

function toolCard(tool) {
  return `
    <a href="${tool.url}" class="tool-card" data-name="${tool.name}" data-category="${tool.category}">
      <span class="badge">${tool.category.toUpperCase()}</span>
      <h3>${tool.name}</h3>
      <p>${tool.description}</p>
    </a>
  `;
}

function setupSearch() {
  const input = document.getElementById("toolSearch");
  if (!input) return;

  input.addEventListener("input", () => {
    const keyword = input.value.trim().toLowerCase();

    document.querySelectorAll(".tool-card").forEach(card => {
      const text = card.textContent.toLowerCase();
      card.classList.toggle("hidden", keyword && !text.includes(keyword));
    });
  });
}

async function init() {
  const categories = await loadJSON("./data/categories.json", fallbackCategories);
  const tools = await loadJSON("./data/tools.json", fallbackTools);

  renderCategories(categories);
  renderTools(tools);
  setupSearch();

  const lang = getLangFromURL();
  const langSelect = document.getElementById("langSelect");

  if (langSelect) {
    langSelect.value = translations[lang] ? lang : "zh";
    langSelect.addEventListener("change", e => {
      const selected = e.target.value;
      localStorage.setItem("zentools_lang", selected);
      applyLanguage(selected);

      const url = new URL(window.location.href);
      url.searchParams.set("lang", selected);
      window.history.replaceState({}, "", url);
    });
  }

  applyLanguage(translations[lang] ? lang : "zh");
}

init();
