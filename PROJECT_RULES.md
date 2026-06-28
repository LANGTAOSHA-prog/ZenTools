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

---

AdSense 内容优化规则

目标：满足 Google AdSense "高品质独特内容"要求，避免"内容贫乏"拒绝。

核心原则：

1. 每篇内容必须提供独特价值（Unique Value）
2. 深度优先于数量（Depth over Quantity）
3. 实用性优于功能性（Practicality over Functionality）

内容质量标准（必须全部满足）：

✅ 字数要求：不少于 2000 字/篇
✅ 原创性：提供别人没有的见解或方法
✅ 深度分析：包含多个子主题和详细解释
✅ 实用案例：至少 2-3 个实际应用场景演示
✅ 视觉元素：至少 3-5 张示意图/截图
✅ 行动建议：明确的下一步操作指导
✅ 参考资料：引用权威来源或官方文档

内容类型优先级：

P0 - 核心指南（Guides）⭐⭐⭐⭐⭐
  位置：/guides/
  示例：
  - /guides/pdf-automation-guide.md (PDF 自动化工作流)
  - /guides/image-batch-processing.md (图片批量处理最佳实践)
  - /guides/ai-writing-workflow.md (AI 写作完整工作流)
  - /guides/seo-optimization-checklist.md (SEO 优化完整清单)
  
P1 - 案例研究（Case Studies）⭐⭐⭐⭐
  位置：/guides/case-study-*.md
  示例：
  - /guides/case-study-pdf-invoice.md (PDF 发票处理案例)
  - /guides/case-study-image-optimization.md (电商图片优化案例)
  - /guides/case-study-seo-audit.md (网站 SEO 审计实战)

P2 - 对比评测（Reviews）⭐⭐⭐
  位置：/guides/review-*.md
  示例：
  - /guides/review-pdf-tools-comparison.md (PDF 工具横向评测)
  - /guides/review-ai-writing-tools.md (AI 写作工具对比)
  - /guides/review-image-editors.md (在线图片编辑器对比)

P3 - 行业专题（Industry Topics）⭐⭐
  位置：/guides/industry-*.md
  示例：
  - /guides/education-online-learning-tools.md (在线教育工具合集)
  - /guides/ecommerce-product-image-guide.md (电商产品图处理指南)

实施计划：

第 1 周：创建 P0 核心指南（5 篇）
  [ ] PDF 自动化工作流指南 (2000+ 字)
  [ ] 图片批量处理最佳实践 (2000+ 字)
  [ ] AI 写作完整工作流 (2000+ 字)
  [ ] SEO 优化完整清单 (2000+ 字)
  [ ] 视频编辑入门指南 (2000+ 字)

第 2 周：创建 P1 案例研究（3 篇）
  [ ] PDF 发票处理案例 (2000+ 字)
  [ ] 电商图片优化案例 (2000+ 字)
  [ ] SEO 审计实战案例 (2000+ 字)

第 3 周：创建 P2 对比评测（3 篇）
  [ ] PDF 工具横向评测 (2500+ 字)
  [ ] AI 写作工具对比 (2500+ 字)
  [ ] 在线图片编辑器对比 (2500+ 字)

第 4 周：创建 P3 行业专题（2 篇）
  [ ] 在线教育工具合集 (2000+ 字)
  [ ] 远程办公效率工具 (2000+ 字)

预期效果：

- 新增 13 篇高质量长文（约 26,000 字）
- 总内容量提升 300%+
- 满足 AdSense "高品质独特内容"要求
- 预计 2-4 周后可重新申请 AdSense

教程扩展要求：

现有 223 个教程必须从"步骤说明"升级为"完整指南"：
  ✅ 添加使用场景说明
  ✅ 添加最佳实践建议
  ✅ 添加常见问题解答（FAQ 部分）
  ✅ 添加实际案例演示

禁止行为：

❌ 复制粘贴其他网站内容
❌ 生成无实质信息的短文本（<1000 字）
❌ 仅罗列功能而无实际使用指导
❌ 缺少图表和视觉元素
❌ 缺少具体案例和实操演示

参考资源：

- Google 站长质量指南：https://developers.google.com/search/docs/basics/site-quality
- 内容贫乏网站指南：https://support.google.com/webmasters/answer/937531
