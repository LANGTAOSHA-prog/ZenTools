# 用户指令记忆

本文件记录了用户的指令、偏好和教导，用于在未来的交互中提供参考。

## 格式

### 用户指令条目
用户指令条目应遵循以下格式：

[用户指令摘要]
- Date: [YYYY-MM-DD]
- Context: [提及的场景或时间]
- Instructions:
  - [用户教导或指示的内容，逐行描述]

### 项目知识条目
Agent 在任务执行过程中发现的条目应遵循以下格式：

[项目知识摘要]
- Date: [YYYY-MM-DD]
- Context: Agent 在执行 [具体任务描述] 时发现
- Category: [运维部署|构建方法|测试方法|排错调试|工作流协作|环境配置]
- Instructions:
  - [具体的知识点，逐行描述]

## 去重策略
- 添加新条目前，检查是否存在相似或相同的指令
- 若发现重复，跳过新条目或与已有条目合并
- 合并时，更新上下文或日期信息
- 这有助于避免冗余条目，保持记忆文件整洁

## 条目

[ZenTools 品牌规范已记录]
- Date: 2026-07-13
- Context: 用户提供了完整的 ZenTools 品牌开发守则 V1.0
- Instructions:
  - 品牌全称统一为 ZenTools，不得简写或改名
  - 完整品牌守则文档见 .monkeycode/docs/zen-tools-brand-guideline.md
  - 主品牌色：主蓝 #0066FF、科技青 #00C2B8
  - 核心调性：隐私优先、免费、本地处理、数据不上传服务器
  - 页脚版权格式：© [年份] ZenTools · https://zentools.xyz · All rights reserved
  - 海外文案：I built ZenTools — A Free Privacy-First Online Tools Website
  - 中文主标语：专业在线工具平台 · 免费 · 高效 · 安全
  - 所有开发工作需遵循品牌守则中的配色、字体、圆角、UI 组件规范
