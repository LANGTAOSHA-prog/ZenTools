ZenTools 项目规则

项目说明

ZenTools 是一个免费在线工具箱和 AI 工具导航网站。

主要功能：

* AI工具导航
* PDF工具
* 图片工具
* 文本工具
* 开发工具
* 教程系统
* 多语言支持

---

开发原则

1. 优先复用已有代码
2. 不允许重复实现功能
3. 不允许创建同功能页面
4. 不允许创建临时测试文件
5. 保持现有目录结构

---

多语言规则

所有新增页面必须支持多语言。

必须使用：

* assets/js/common-i18n.js（公共翻译数据）
* 内联 window.ZT_PAGE（页面专属翻译）
* tool-ui.js 中的 ZT.applyLanguage() 引擎

数据合并规则：ZT_PAGE 的 key 会覆盖 ZT_COMMON 的同名 key。

禁止：

* 页面内硬编码文本
* 创建新的翻译系统

---

教程规则

所有教程统一放在：

/tutorials/

禁止：

/article/
/blog/
/posts/

---

修改代码前

必须先搜索：

* components
* tools
* tutorials
* assets/js

确认是否已有实现。

发现已有功能：

优先扩展。

禁止重写。

---

输出要求

修改前：

先说明发现了哪些相关代码。

修改后：

说明修改文件和原因。
