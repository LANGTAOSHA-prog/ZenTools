# 贡献指南

感谢你对 ZenTools 的关注！欢迎以任何方式参与项目。

## 如何贡献

### 报告问题

- 在 [Issues](https://github.com/LANGTAOSHA-prog/ZenTools/issues) 中搜索是否已有相同问题
- 使用 Issue 模板提交 Bug 报告或功能建议
- 描述尽量详细：复现步骤、预期行为、实际行为、截图

### 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-feature`
3. 提交更改：`git commit -m "feat: 添加 XXX 功能"`
4. 推送到你的 Fork：`git push origin feat/your-feature`
5. 发起 Pull Request 到 `main` 分支

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

| 前缀 | 用途 |
|:-----|:-----|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响功能） |
| `refactor` | 重构（不新增功能也不修复 Bug） |
| `perf` | 性能优化 |
| `chore` | 构建/工具/依赖等杂项 |
| `i18n` | 国际化翻译 |

示例：`feat: 添加 PDF 水印去除工具`

## 开发须知

### 技术栈

- 纯前端：HTML5 + CSS3 + Vanilla JavaScript（无框架依赖）
- 数据驱动：`data/tools-data.json` 驱动全站工具列表
- 国际化：`[data-i18n]` + `[data-i18n-page]` 属性配合 `ZT_COMMON` / `ZT_PAGE` 字典

### 本地运行

本项目为纯静态站点，无需构建：

```bash
# 克隆仓库
git clone https://github.com/LANGTAOSHA-prog/ZenTools.git
cd ZenTools

# 任意静态服务器即可
python -m http.server 8080
# 或
npx serve .
```

浏览器访问 `http://localhost:8080`

### 新增工具

1. 在 `data/tools-data.json` 中添加工具元数据
2. 创建工具页面 HTML（参考同类工具页面结构）
3. 如需国际化，在对应语言的翻译文件中添加键值
4. 确保工具在浏览器本地完成所有处理（不上传文件）

### 行尾约定

本项目源文件使用 CRLF (`\r\n`) 行尾。提交时请保持一致，避免整文件 diff。

## 行为准则

参与本项目即表示你同意遵守 [行为准则](CODE_OF_CONDUCT.md)。请保持友善和尊重。

## License

提交的代码将在 [MIT License](LICENSE) 下发布。
