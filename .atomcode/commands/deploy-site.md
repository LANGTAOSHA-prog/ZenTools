# /deploy-site — 标准部署流程

执行标准部署：提交并推送 ZenTools 项目到远程仓库。

## 执行步骤

1. 运行 `_check_json.py` 验证数据完整性
2. 运行 `_check_paths.py` 验证所有工具页面存在
3. 如果有修改，执行 `git add .`
4. 使用中文明细执行 `git commit -m "<描述>"`
5. 执行 `git push origin main`

## 用法

```
/deploy-site                  # 标准部署（需确认后执行）
/deploy-site "更新内容"        # 带提交信息的部署
```
