# 需求实施计划

- [ ] 1. 创建 changelog 公共模块 `_changelog_utils.py`
  - 实现 `load_site_info()` 读取 `data/site-info.json`（REQ-7 向后兼容）
  - 实现 `save_site_info(data)` 写入 `data/site-info.json`
  - 实现 `build_tool_entry(name_zh, name_en, name_ja, name_vi, slug, cat_zh, desc_zh, desc_en, desc_ja, desc_vi)` 构建工具变更项四语言字典（REQ-5, REQ-8）
  - 实现 `build_tutorial_entry(title_zh, title_en, title_ja, title_vi, cat_zh, slug)` 构建教程变更项四语言字典（REQ-5）
  - 实现 `build_guide_entry(title_zh, title_en, title_ja, title_vi, guide_type, slug)` 构建指南变更项四语言字典（REQ-5）
  - 实现 `append_changelog(data, entries)` 核心聚合逻辑：当日有条目则追加 items，无条目则创建新条目（REQ-4, REQ-6）
  - 实现 `sync_metadata(data)` 同步 `lastUpdated` 和 `toolCount`（REQ-1）
  - 文件路径：`/workspace/_changelog_utils.py`

  - [ ]* 1.1 为 `_changelog_utils.py` 编写单元测试
    - 测试 `build_tool_entry` 输出包含四语言 key
    - 测试 `append_changelog` 当日聚合行为（同一天追加到同一条目）
    - 测试 `append_changelog` 跨日创建新条目行为
    - 测试 `load_site_info` 对不存在文件返回默认结构

- [ ] 2. 修改 `_add_tool.py` 集成 changelog 自动更新
  - 在 `main()` 中 `update_tools_data_json()` 成功后调用 changelog 更新（REQ-1）
  - 传入工具名称（zh/en/ja/vi）、分类、slug、描述（zh/en/ja/vi）
  - 使用 try/except 包裹 changelog 更新，失败时打印警告但不中断主流程
  - 文件路径：`/workspace/_add_tool.py`

- [ ] 3. 检查点 - 验证工具新增流程完整
  - 确保 `_add_tool.py` 运行时 `site-info.json` 正确更新
  - 确保 `lastUpdated`、`toolCount`、`changelog` 三项均更新
  - 如有疑问请询问用户

- [ ] 4. 修改 `_add_tutorial.py` 集成 changelog 自动更新
  - 在 HTML 文件写入成功后追加 changelog 更新（REQ-2）
  - 传入教程标题（zh/en/ja/vi）、分类、slug
  - 使用 try/except 包裹，失败时打印警告但不中断
  - 文件路径：`/workspace/_add_tutorial.py`

- [ ] 5. 修改 `_add_guide.py` 集成 changelog 自动更新
  - 在 HTML 文件写入成功后追加 changelog 更新（REQ-3）
  - 传入指南标题（zh/en/ja/vi）、类型（review/core/case/industry）、slug
  - 使用 try/except 包裹，失败时打印警告但不中断
  - 文件路径：`/workspace/_add_guide.py`

- [ ] 6. 检查点 - 验证全流程集成
  - 确保三种脚本互不干扰
  - 确保同一日内多次运行正确聚合
  - 如有疑问请询问用户

- [ ] 7. 创建 `_sync_changelog.py` 独立同步脚本
  - 实现 `--scan` 模式：扫描 `tools-data.json` 中 `new: true` 标记的工具，将缺失项追加到 changelog（REQ-6）
  - 实现 `--reset` 模式：以 `tools-data.json` 为基准完全重建 `site-info.json` 的元数据（`version`、`lastUpdated`、`toolCount`），保留已有 changelog 条目
  - 使用 argparse 支持 `--scan` 和 `--reset` 两种运行模式
  - 文件路径：`/workspace/_sync_changelog.py`

  - [ ]* 7.1 为 `_sync_changelog.py` 编写单元测试
    - 测试 `--scan` 模式检测到缺失工具时正确追加
    - 测试 `--reset` 模式 rebuild 后元数据与 `tools-data.json` 一致
