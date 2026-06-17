// app.js - ZenTools 2.1 UI enhancements & performance tweaks
// 此文件用于后续功能扩展，当前保持轻量级，确保不影响页面渲染性能。

// 示例：返回顶部按钮的淡入淡出（已在 index.html 中实现，此处提供统一实现）
(function() {
  const backTop = document.getElementById('backTop');
  if (!backTop) return;
  window.addEventListener('scroll', () => {
    const show = window.scrollY > 300;
    backTop.style.opacity = show ? '1' : '0';
    backTop.style.pointerEvents = show ? 'all' : 'none';
  });
})();