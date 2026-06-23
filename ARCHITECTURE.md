ZenTools 项目架构

根目录

index.html
tools/
tutorials/
assets/
locales/

⸻

tools

工具页面目录

例如：

tools/pdf/
tools/image/
tools/text/

⸻

tutorials

教程页面目录

所有教程统一放这里。

禁止创建：

blog/
posts/
articles/

⸻

assets

静态资源

css/
js/
img/

⸻

locales

翻译文件

common.json
zh.json
en.json

⸻

开发流程

新增功能：

1. 搜索现有代码
2. 优先复用
3. 保持目录结构
4. 增加多语言
5. 测试后提交