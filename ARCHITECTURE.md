ZenTools 项目架构

根目录

index.html         首页
tools/             工具页面目录
tutorials/         教程页面目录
assets/            静态资源
data/              工具数据（JSON）
pdf/               PDF 工具页面目录
contact            联系我们页面

---

tools

工具页面目录

例如：

tools/pdf/
tools/image/
tools/text/

---

tutorials

教程页面目录

所有教程统一放这里。

禁止创建：

blog/
posts/
articles/

---

assets

静态资源

css/      样式文件
js/       JavaScript 文件
img/      图片资源

assets/js 重要文件说明：

common-i18n.js      公共翻译数据（zh/en/ja/vi）
common-i18n.min.js  上述文件的压缩版
tool-ui.js          工具页面共享组件（含 i18n 引擎 ZT.applyLanguage）
tool-ui.min.js      上述文件的压缩版
anti-crash.js       防崩兜底脚本
anti-crash.min.js   上述文件的压缩版

---

多语言系统

翻译数据统一存放在 assets/js/common-i18n.js（window.ZT_COMMON）。

页面专属翻译通过内联 window.ZT_PAGE 定义，与公共数据合并后生效。

翻译引擎为 tool-ui.js 中的 ZT.applyLanguage() 函数。

支持语言：zh（中文）, en（English）, ja（日本語）, vi（Tiếng Việt）

---

开发流程

新增功能：

1. 搜索现有代码（components / tools / assets/js）
2. 优先复用已有实现
3. 保持目录结构
4. 增加多语言支持（common-i18n.js 或 ZT_PAGE）
5. 测试后提交
