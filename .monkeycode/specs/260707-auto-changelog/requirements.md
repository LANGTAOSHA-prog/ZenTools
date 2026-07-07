# 需求文档：首页更新目录自动同步

## 功能概述

当网站内新增工具页面、教程页面或指南页面时，主页的"更新日志"区块应自动反映变更内容，无需手动编辑 `data/site-info.json`。

## 背景

当前机制：
- 主页 (`index.html`) 有 `changelog-section` 区块，从 `data/site-info.json` 读取 changelog 数据动态渲染
- `changelog.html` 独立页面同样从 `site-info.json` 读取全部版本历史
- 添加新工具时，`_add_tool.py` 会自动更新 `tools-data.json` 的 `lastUpdated` 字段，但不会触碰 `site-info.json`
- `_add_tutorial.py` 和 `_add_guide.py` 生成内容页面后完全不涉及任何 changelog 数据
- `site-info.json` 中的 `version`、`toolCount`、`changelog[]` 需要人工手动维护

结果：新内容上线后，主页更新日志不会自动体现，造成内容与 changelog 不同步。

## EARS 需求

### REQ-1: 工具新增自动记录
**WHEN** 通过 `_add_tool.py` 成功创建新工具页面并更新 `tools-data.json` 后，**THEN** 系统应自动将本次变更记录到 `data/site-info.json` 的 `changelog` 数组中。

具体行为：
- `site-info.json` 的 `lastUpdated` 更新为当前日期
- `site-info.json` 的 `toolCount` 更新为当前工具总数
- 若当前日期已有当日 changelog 条目，则在对应 `items` 列表中追加新工具的变更项
- 若当前日期无对应 changelog 条目，则创建新条目（`version` 使用 `tools-data.json` 的 `version`）

### REQ-2: 教程新增自动记录
**WHEN** 通过 `_add_tutorial.py` 成功创建新教程页面后，**THEN** 系统应自动将本次变更记录到 `data/site-info.json`。

具体行为：
- `site-info.json` 的 `lastUpdated` 更新为当前日期
- 若当前日期已有 changelog 条目，追加教程变更项
- 若当前日期无对应条目，则创建新条目

### REQ-3: 指南新增自动记录
**WHEN** 通过 `_add_guide.py` 成功创建新指南/评测页面后，**THEN** 系统应自动将本次变更记录到 `data/site-info.json`。

具体行为：
- `site-info.json` 的 `lastUpdated` 更新为当前日期
- 若当前日期已有 changelog 条目，追加指南变更项
- 若当前日期无对应条目，则创建新条目

### REQ-4: 当日聚合
**WHEN** 同一日内通过多个脚本分别新增内容，**THEN** 所有变更应聚合到同一个 changelog 条目中，而不是创建多个独立条目。

### REQ-5: 四语言变更项
**WHEN** 创建 changelog 条目时，**THEN** 每个 `items` 对象必须包含 `zh`、`en`、`ja`、`vi` 四种语言的变更描述。

### REQ-6: 独立同步脚本
**THEN** 系统应提供一个独立的 `_sync_changelog.py` 脚本，允许手动触发 changelog 的重新同步（扫描 `tools-data.json` 和页面文件，对比 `site-info.json` 的差异进行修复）。

### REQ-7: 向后兼容
**WHEN** 现有 `site-info.json` 和 `tools-data.json` 格式不被修改，**THEN** 已有功能（首页渲染、changelog 页面、工具列表）不受影响。

### REQ-8: 变更项内容格式
**THEN** 每个工具变更项的内容格式为：`新增{分类}工具：{工具名称}（{简述}）` 及其多语言对应版本。

## 非功能需求

- 脚本执行时间增量不超过 1 秒
- 不引入新的外部依赖
- 变更项内容自动从脚本参数中提取，无需用户额外输入
- changelog 条目保留最近 10 条版本记录，超出自动归档
