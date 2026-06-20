---
name: project-conventions
description: ZenTools 项目代码规范和开发约定
user_invocable: false
disable_model_invocation: false
---

# ZenTools 项目约定

## 开发流程
- 工具代码修改 → 验证正确性后 → 直接提交并推送到远程仓库
- 无需每次询问是否推送

## 代码规范
- HTML: UTF-8, 统一暗色主题 UI（CSS 变量: --bg, --card, --border, --blue 等）
- CSS: 内联 `<style>` 方式，统一使用 `:root{--bg:#0f172a;...}` 变量体系
- i18n: 支持 zh/ja/en/vi 四种语言，使用 `data-i18n` 属性 + 翻译对象 T
- AdSense: 使用占位符 `data-ad-slot="YOUR_AD_SLOT_ID"`（审核中）

## 图片工具规范
- 所有工具使用 Canvas API 处理，浏览器本地运行
- 统一布局：top-bar → card → ad-box → 控件 → 预览 → info → footer
- 滑动控件使用 `.slider-group` 结构
- 按钮颜色：默认 `--blue`，下载 `--green`，清空 `--red`

## Git 规范
- 推送远程：`origin` → `https://github.com/LANGTAOSHA-prog/ZenTools.git`
- 提交信息：中文描述，清晰说明修改内容
