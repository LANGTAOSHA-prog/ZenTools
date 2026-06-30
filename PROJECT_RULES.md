ZenTools 项目规则

项目说明

ZenTools 是一个免费在线工具箱和 AI 工具导航网站。

主要功能：

* AI 工具导航
* PDF 工具
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
  - /guides/pdf-automation-guide.html (PDF 自动化工作流)
  - /guides/image-batch-processing.html (图片批量处理最佳实践)
  - /guides/ai-writing-workflow.html (AI 写作完整工作流)
  - /guides/seo-optimization-checklist.html (SEO 优化完整清单)
  
P1 - 案例研究（Case Studies）⭐⭐⭐⭐
  位置：/guides/case-study-*.html
  示例：
  - /guides/case-study-pdf-invoice.html (PDF 发票处理案例)
  - /guides/case-study-image-optimization.html (电商图片优化案例)
  - /guides/case-study-seo-audit.html (网站 SEO 审计实战)

P2 - 对比评测（Reviews）⭐⭐⭐
  位置：/guides/review-*.html
  示例：
  - /guides/review-pdf-tools-comparison.html (PDF 工具横向评测)
  - /guides/review-ai-writing-tools.html (AI 写作工具对比)
  - /guides/review-image-editors.html (在线图片编辑器对比)

P3 - 行业专题（Industry Topics）⭐⭐
  位置：/guides/industry-*.html
  示例：
  - /guides/education-online-learning-tools.html (在线教育工具合集)
  - /guides/ecommerce-product-image-guide.html (电商产品图处理指南)

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

---

E-E-A-T 品牌权威性建设规则

目标：建立专业、可信、有权威的品牌形象，提升 Google 信任度。

核心要素：

1. 经验（Experience）- 展示实际操作经验
2. 专业性（Expertise）- 展现专业知识深度
3. 权威性（Authoritativeness）- 建立行业影响力
4. 可信度（Trustworthiness）- 确保内容真实可靠

必需页面：

✅ 关于我们页面（/about/index.html）
   - 团队介绍
   - 使命愿景
   - 发展历程
   - 联系方式

✅ 作者信息页面（/authors/）
   - 作者头像
   - 专业背景
   - 擅长领域
   - 个人简介

✅ 隐私政策页面（/privacy/）
   - 数据收集说明
   - Cookie 使用政策
   - 用户权利
   - 联系我们

✅ 免责声明页面（/disclaimer/）
   - 内容准确性声明
   - 第三方链接说明
   - 使用责任限制
   - 版权信息

✅ 更新时间戳
   - 每篇文章显示最后更新时间
   - 定期更新标记
   - 版本历史记录

内容规范：

✅ 每篇深度指南必须包含：
   - 作者署名
   - 发布日期
   - 最后更新时间
   - 阅读时间估算
   - 难度等级标识

✅ 技术内容必须：
   - 引用官方文档
   - 提供代码示例
   - 包含测试验证
   - 注明适用版本

✅ 商业内容必须：
   - 披露合作关系
   - 说明推荐标准
   - 提供客观评价
   - 标注广告内容

禁止行为：

❌ 匿名发布重要内容
❌ 隐藏更新时间
❌ 虚假宣传专业能力
❌ 未披露利益关系
❌ 传播未经核实信息

参考标准：

- Google E-E-A-T 指南：https://developers.google.com/search/docs/fundamentals/create-helpful-reliable-yelp-pages
- 内容营销协会标准：https://www.contentmarketinginstitute.com/

---

结构化知识密度规则

目标：提升内容知识密度，打造 AI 可引用的结构化知识库。

必备知识模块：

✅ 定义说明（Definition）
   - 清晰的概念解释
   - 专业术语说明
   - 适用范围界定

✅ 操作步骤（Step-by-step）
   - 分步骤详细说明
   - 每个步骤配截图
   - 注意事项标注

✅ 注意事项（Important Notes）
   - 常见错误提示
   - 安全警告
   - 性能影响说明

✅ 对比表格（Comparison Table）
   - 多维度参数对比
   - 优缺点分析
   - 适用场景建议

✅ 优缺点分析（Pros & Cons）
   - 优势列表
   - 局限性说明
   - 改进建议

✅ 决策树（Decision Tree）
   - 场景选择逻辑
   - 条件判断流程
   - 推荐方案指引

内容格式规范：

✅ 必须使用以下 HTML 标签：
   - <details><summary> 用于折叠内容
   - <table> 用于对比表格
   - <code> 用于代码片段
   - <blockquote> 用于引用说明
   - <div class="note"> 用于注意事项
   - <div class="tip"> 用于技巧提示

✅ 知识卡片格式：
   ```html
   <div class="knowledge-card">
     <h3>📌 关键要点</h3>
     <ul>
       <li>要点 1</li>
       <li>要点 2</li>
     </ul>
   </div>
   ```

禁止行为：

❌ 纯文字无结构
❌ 缺少关键信息
❌ 模糊不清的描述
❌ 无依据的主观判断
❌ 过时的技术信息

参考模板：

- MDN Web Docs 风格指南
- Google Developers Documentation Guidelines

---

外链建设与影响力规则

目标：建立自然外链网络，提升域名权威性和搜索排名。

外链建设策略：

✅ GitHub 生态
   - 开源项目 README 引用
   - 技术博客文章发布
   - Issue/PR 讨论参与
   - 项目文档完善

✅ 技术社区
   - Medium 专栏文章
   - 知乎优质回答
   - Stack Overflow 解答
   - Reddit 技术分享

✅ 社交媒体
   - Twitter 技术 Thread
   - LinkedIn 专业文章
   - 微信公众号原创
   - 掘金专栏投稿

✅ 行业论坛
   - V2EX 技术讨论
   - 少数派专栏
   - 思否（SegmentFault）
   - CSDN 技术博客

外链质量要求：

✅ 必须满足：
   - 高 DA/PA 值域名
   - 相关技术领域
   - 自然流量入口
   - 长期稳定存在

✅ 禁止行为：
   - 购买链接
   - 垃圾评论
   - 交换链接农场
   - 隐藏链接

内容分发策略：

✅ 每次发布新内容时：
   1. 在 GitHub 仓库同步
   2. 发布到 Medium/知乎
   3. 分享到社交媒体
   4. 参与相关讨论

✅ 持续维护：
   - 定期更新旧内容
   - 修复失效链接
   - 监控外链状态
   - 分析引流效果

参考工具：

- Ahrefs Backlink Checker
- Moz Link Explorer
- Google Search Console
- UTM 参数追踪

---

工具生态扩展规则

目标：持续丰富工具库，提升用户体验和搜索覆盖。

分类优化：

✅ 主分类（13 个）
   - PDF 工具
   - 图片工具
   - 文本工具
   - 开发工具
   - 音视频工具
   - 生活工具
   - 金融工具
   - AI 工具
   - SEO 工具
   - QR 码工具
   - 通用工具
   - 云创资源
   - 深度指南

✅ 子分类系统
   - 每个主分类下细分 5-10 个子类
   - 支持标签化分类
   - 跨分类关联

搜索功能增强：

✅ 必须实现：
   - 关键词搜索
   - 分类筛选
   - 标签过滤
   - 智能推荐
   - 热门搜索

✅ 搜索优化：
   - 模糊匹配
   - 拼音搜索
   - 同义词识别
   - 搜索结果排序

标签系统设计：

✅ 标签类型：
   - 难度等级（入门/进阶/专家）
   - 适用场景（办公/开发/设计）
   - 文件格式（PDF/JPG/MP4）
   - 技术栈（Python/JavaScript）
   - 免费/付费

多语言本地化：

✅ 支持语言：
   - 简体中文（zh-CN）
   - 繁体中文（zh-TW）
   - 英语（en-US）
   - 日语（ja-JP）
   - 越南语（vi-VN）

✅ 本地化要求：
   - UI 界面完整翻译
   - 工具描述翻译
   - 教程内容翻译
   - 元数据翻译

工具收录标准：

✅ 必须满足：
   - 功能独立完整
   - 用户体验良好
   - 无恶意广告
   - 移动端适配
   - 加载速度快

✅ 禁止收录：
   - 抄袭复制工具
   - 含恶意代码
   - 频繁崩溃
   - 侵犯版权
   - 违规内容

更新维护机制：

✅ 定期审查：
   - 每月检查工具可用性
   - 每季度更新分类
   - 半年清理无效工具
   - 年度全面重构

✅ 用户反馈：
   - 收集使用反馈
   - 快速响应问题
   - 持续优化体验
   - 公开更新日志

参考标准：

- Product Hunt 新品标准
- AlternativeTo 工具评估
- G2 Crowd 软件评分

---

内容创作检查清单

每次发布新内容前，必须完成以下检查：

✅ 内容质量
   - [ ] 字数达到 2000+
   - [ ] 提供独特见解
   - [ ] 包含实际案例
   - [ ] 配有视觉元素
   - [ ] 有明确行动建议

✅ 技术准确性
   - [ ] 引用官方文档
   - [ ] 代码经过测试
   - [ ] 版本信息准确
   - [ ] 兼容性已验证

✅ SEO 优化
   - [ ] Title 包含关键词
   - [ ] Meta Description 完整
   - [ ] 内部链接合理
   - [ ] 图片 ALT 标签齐全
   - [ ] URL 结构友好

✅ 多语言支持
   - [ ] 中文翻译完整
   - [ ] 英文翻译准确
   - [ ] 日文翻译正确
   - [ ] 越南文翻译到位
   - [ ] 切换功能正常

✅ E-E-A-T 要素
   - [ ] 作者信息完整
   - [ ] 发布时间明确
   - [ ] 更新时间可见
   - [ ] 参考资料引用
   - [ ] 免责声明齐全

✅ 结构化数据
   - [ ] Schema.org 标记
   - [ ] FAQ 结构化数据
   - [ ] Breadcrumb 导航
   - [ ] Open Graph 标签
   - [ ] Twitter Card 标签

---

持续改进机制

✅ 每周回顾
   - 分析页面访问数据
   - 收集用户反馈
   - 识别改进点
   - 制定优化计划

✅ 月度总结
   - 内容发布统计
   - SEO 排名变化
   - 外链增长情况
   - 转化率分析

✅ 季度规划
   - 内容策略调整
   - 新功能开发
   - 技术架构优化
   - 团队建设计划

✅ 年度复盘
   - 整体目标达成
   - 市场竞争分析
   - 技术趋势预判
   - 战略规划调整

---

本守则版本：v2.0
最后更新：2026 年 6 月 30 日
维护团队：ZenTools 开发组

