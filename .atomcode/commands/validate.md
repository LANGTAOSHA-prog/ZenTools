# /validate — 运行项目验证

运行 ZenTools 项目所有数据校验和 HTML 结构审查。

## 执行步骤

1. 运行 `_check_json.py` 验证所有 JSON 数据文件
2. 运行 `_check_paths.py` 验证工具页面路径是否完整
3. 运行 `_check_data.py` 验证 tools-data.json 与实际文件是否一致
4. 如使用 html-reviewer skill，可选择对指定页面执行 HTML 结构审查

## 用法

```
/validate                    # 运行所有校验
/validate pages              # 只检查页面路径
/validate json               # 只检查 JSON 数据
/validate <file.html>        # 对指定页面执行 HTML 审查
```
