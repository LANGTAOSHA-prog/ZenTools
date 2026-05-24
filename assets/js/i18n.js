const translations = {
  en:{navTools:'Tools',navCategories:'Categories',navArticles:'Articles',navAbout:'About',badge:'Free · Fast · Multilingual',heroTitle:'Free Online Tools & AI Tools Directory',heroDesc:'Find useful tools for images, PDF, text, video, office work, SEO, development and AI productivity.',searchPlaceholder:'Search free online tools...',popularTools:'Popular Tools',viewAll:'View all',categoriesTitle:'Tool Categories',faqTitle:'Frequently Asked Questions',faq1q:'Is ZenTools free to use?',faq1a:'Yes. Most tools are free online tools that work directly in your browser.',faq2q:'Does ZenTools support mobile devices?',faq2a:'Yes. The website is designed for both desktop and mobile users.'},
  zh:{navTools:'工具',navCategories:'分类',navArticles:'教程文章',navAbout:'关于',badge:'免费 · 快速 · 多语言',heroTitle:'免费在线工具与 AI 工具导航',heroDesc:'查找图片、PDF、文本、视频、办公、SEO、开发和 AI 效率工具。',searchPlaceholder:'搜索免费在线工具...',popularTools:'热门工具',viewAll:'查看全部',categoriesTitle:'工具分类',faqTitle:'常见问题',faq1q:'ZenTools 可以免费使用吗？',faq1a:'可以。大部分工具都是直接在浏览器中运行的免费在线工具。',faq2q:'ZenTools 支持手机吗？',faq2a:'支持。网站针对电脑和手机都做了自适应设计。'},
  ja:{navTools:'ツール',navCategories:'カテゴリー',navArticles:'記事',navAbout:'概要',badge:'無料 · 高速 · 多言語',heroTitle:'無料オンラインツールとAIツールナビ',heroDesc:'画像、PDF、テキスト、動画、オフィス、SEO、開発、AI生産性ツールを探せます。',searchPlaceholder:'無料オンラインツールを検索...',popularTools:'人気ツール',viewAll:'すべて見る',categoriesTitle:'ツールカテゴリー',faqTitle:'よくある質問',faq1q:'ZenToolsは無料ですか？',faq1a:'はい。多くのツールはブラウザで直接使える無料オンラインツールです。',faq2q:'ZenToolsはスマホ対応ですか？',faq2a:'はい。PCとスマホの両方に対応しています。'},
  vi:{navTools:'Công cụ',navCategories:'Danh mục',navArticles:'Bài viết',navAbout:'Giới thiệu',badge:'Miễn phí · Nhanh · Đa ngôn ngữ',heroTitle:'Công cụ online miễn phí & danh bạ công cụ AI',heroDesc:'Tìm công cụ cho ảnh, PDF, văn bản, video, văn phòng, SEO, lập trình và AI.',searchPlaceholder:'Tìm kiếm công cụ online miễn phí...',popularTools:'Công cụ phổ biến',viewAll:'Xem tất cả',categoriesTitle:'Danh mục công cụ',faqTitle:'Câu hỏi thường gặp',faq1q:'ZenTools có miễn phí không?',faq1a:'Có. Hầu hết công cụ miễn phí và chạy trực tiếp trên trình duyệt.',faq2q:'ZenTools có hỗ trợ điện thoại không?',faq2a:'Có. Website được thiết kế cho cả máy tính và điện thoại.'}
};

function applyLanguage(lang){
  const dict = translations[lang] || translations.en;
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el=>{const key=el.getAttribute('data-i18n'); if(dict[key]) el.textContent=dict[key];});
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{const key=el.getAttribute('data-i18n-placeholder'); if(dict[key]) el.placeholder=dict[key];});
  localStorage.setItem('zentools_lang', lang);
}
