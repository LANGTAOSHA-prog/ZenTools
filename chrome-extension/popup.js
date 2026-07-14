const tools = [
  { cat: 'PDF', icon: '📄', name: 'PDF 合并', url: 'https://zentools.xyz/pdf/pdf-merge.html' },
  { cat: 'PDF', icon: '🗜️', name: 'PDF 压缩', url: 'https://zentools.xyz/pdf/pdf-compress.html' },
  { cat: 'PDF', icon: '📝', name: 'PDF 转 Word', url: 'https://zentools.xyz/pdf/pdf-to-word.html' },
  { cat: 'PDF', icon: '🖼️', name: '图片转 PDF', url: 'https://zentools.xyz/pdf/image-to-pdf.html' },
  { cat: 'PDF', icon: '📸', name: 'PDF 转图片', url: 'https://zentools.xyz/pdf/pdf-to-image.html' },
  { cat: 'PDF', icon: '📊', name: 'PDF 转 Excel', url: 'https://zentools.xyz/pdf/pdf-to-excel.html' },

  { cat: '图片', icon: '🖼️', name: '图片压缩', url: 'https://zentools.xyz/image/image-compress.html' },
  { cat: '图片', icon: '🔄', name: '格式转换', url: 'https://zentools.xyz/image/image-convert.html' },
  { cat: '图片', icon: '✂️', name: '图片裁剪', url: 'https://zentools.xyz/image/image-crop.html' },
  { cat: '图片', icon: '🔍', name: '图片 OCR', url: 'https://zentools.xyz/image/ocr.html' },

  { cat: '文本', icon: '🔢', name: '字数统计', url: 'https://zentools.xyz/text/word-count.html' },
  { cat: '文本', icon: '📋', name: '文本对比', url: 'https://zentools.xyz/text/text-diff.html' },
  { cat: '文本', icon: 'Aa', name: '大小写转换', url: 'https://zentools.xyz/text/case-convert.html' },

  { cat: '开发', icon: '🔧', name: 'JSON 格式化', url: 'https://zentools.xyz/dev/json-formatter.html' },
  { cat: '开发', icon: '⏰', name: '时间戳转换', url: 'https://zentools.xyz/dev/timestamp.html' },
  { cat: '开发', icon: '🔐', name: 'Base64 编解码', url: 'https://zentools.xyz/dev/base64.html' },
  { cat: '开发', icon: '🔑', name: '哈希计算', url: 'https://zentools.xyz/dev/hash-generator.html' },

  { cat: 'AI', icon: '🤖', name: 'AI 写作', url: 'https://zentools.xyz/ai/ai-writer.html' },
  { cat: 'AI', icon: '📄', name: 'AI 智能问答', url: 'https://zentools.xyz/ai/ai-chat.html' },

  { cat: '音视频', icon: '🎬', name: '视频转 GIF', url: 'https://zentools.xyz/video/video-to-gif.html' },
  { cat: '音视频', icon: '🗜️', name: '视频压缩', url: 'https://zentools.xyz/video/video-compress.html' },
  { cat: '音视频', icon: '🎵', name: '音频转换', url: 'https://zentools.xyz/audio/audio-convert.html' },

  { cat: '日常', icon: '📐', name: '单位换算', url: 'https://zentools.xyz/life/unit-converter.html' },
  { cat: '日常', icon: '🔑', name: '密码生成器', url: 'https://zentools.xyz/life/password-generator.html' },
  { cat: '日常', icon: '📱', name: '二维码生成', url: 'https://zentools.xyz/qr/qr-generator.html' },
  { cat: '日常', icon: '💰', name: '货币汇率', url: 'https://zentools.xyz/finance/currency-converter.html' },
];

const content = document.getElementById('content');
const search = document.getElementById('search');

function render(filter) {
  const q = (filter || '').toLowerCase().trim();
  const cats = {};
  tools.forEach(t => {
    if (q && !t.name.toLowerCase().includes(q) && !t.cat.toLowerCase().includes(q)) return;
    if (!cats[t.cat]) cats[t.cat] = [];
    cats[t.cat].push(t);
  });

  const keys = Object.keys(cats);
  if (!keys.length) {
    content.innerHTML = '<div class="empty">没有找到匹配的工具</div>';
    return;
  }

  content.innerHTML = keys.map(cat => `
    <div class="cat">
      <div class="cat-title">${cat}</div>
      <div class="grid">
        ${cats[cat].map(t => `
          <a class="tool" href="${t.url}" target="_blank">
            <span class="icon">${t.icon}</span>
            <span class="name">${t.name}</span>
          </a>
        `).join('')}
      </div>
    </div>
  `).join('');
}

render('');
search.addEventListener('input', () => render(search.value));