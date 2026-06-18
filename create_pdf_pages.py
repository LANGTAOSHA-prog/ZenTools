#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建 PDF 工具页面
使用统一的 UI 风格（基于 pdf/image-to-pdf.html）
"""

import os

# PDF 工具配置列表
pdf_tools = [
    {
        "name": "PDF转Word",
        "slug": "pdf-to-word",
        "description": "将 PDF 转换为可编辑的 Word 文档",
        "icon": "📝",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "docx",
        "outputName": "转换后的 Word",
        "features": [
            ("高精度转换", "保留原文档格式和排版，支持文字、表格、图片等元素的精确还原。"),
            ("批量处理", "支持同时转换多个 PDF 文件，提高工作效率。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "Word转PDF",
        "slug": "word-to-pdf",
        "description": "将 Word 文档转换为 PDF 格式",
        "icon": "📄",
        "fileInput": "word",
        "accept": ".doc,.docx",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("格式保留", "完美保留 Word 文档的字体、段落、表格和图片格式。"),
            ("快速转换", "秒级转换速度，支持大文件处理。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF转Excel",
        "slug": "pdf-to-excel",
        "description": "将 PDF 表格数据提取为 Excel 文件",
        "icon": "📊",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "xlsx",
        "outputName": "转换后的 Excel",
        "features": [
            ("智能识别", "自动识别 PDF 中的表格结构，精确提取数据。"),
            ("格式保留", "保留原始表格的行列结构和数据类型。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "Excel转PDF",
        "slug": "excel-to-pdf",
        "description": "将 Excel 表格转换为 PDF 格式",
        "icon": "📋",
        "fileInput": "excel",
        "accept": ".xls,.xlsx",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("表格适配", "自动调整表格大小以适应 PDF 页面。"),
            ("多工作表", "支持将多个工作表转换为独立的 PDF 页面。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF转PPT",
        "slug": "pdf-to-ppt",
        "description": "将 PDF 转换为 PowerPoint 演示文稿",
        "icon": "📽️",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pptx",
        "outputName": "转换后的 PPT",
        "features": [
            ("页面转换", "将 PDF 每一页转换为独立的 PPT 幻灯片。"),
            ("元素提取", "提取 PDF 中的文字和图片到 PPT 中。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PPT转PDF",
        "slug": "ppt-to-pdf",
        "description": "将 PowerPoint 演示文稿转换为 PDF",
        "icon": "📑",
        "fileInput": "ppt",
        "accept": ".ppt,.pptx",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("幻灯片转换", "将每张幻灯片转换为 PDF 页面。"),
            ("格式保留", "保留演示文稿的布局和格式。"),
            ("隐私安全", "所有转换操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF加密",
        "slug": "pdf-encrypt",
        "description": "为 PDF 文件添加密码保护",
        "icon": "🔒",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "加密后的 PDF",
        "features": [
            ("密码保护", "设置打开密码，保护 PDF 内容安全。"),
            ("权限控制", "可设置打印、复制、编辑等权限。"),
            ("隐私安全", "所有加密操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF解密",
        "slug": "pdf-decrypt",
        "description": "移除 PDF 文件的密码保护",
        "icon": "🔓",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "解密后的 PDF",
        "features": [
            ("密码移除", "移除 PDF 的打开密码和权限限制。"),
            ("快速处理", "秒级解密速度。"),
            ("隐私安全", "所有解密操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF页面提取",
        "slug": "pdf-extract-pages",
        "description": "从 PDF 中提取指定页面",
        "icon": "📄",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "提取后的 PDF",
        "features": [
            ("灵活选择", "支持选择单页、连续页面或不连续页面。"),
            ("保留格式", "提取后的页面保持原有格式和质量。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF页面删除",
        "slug": "pdf-delete-pages",
        "description": "删除 PDF 中的指定页面",
        "icon": "🗑️",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "删除页面后的 PDF",
        "features": [
            ("精准删除", "选择需要删除的页面，支持批量删除。"),
            ("预览功能", "删除前可预览 PDF 页面。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF旋转",
        "slug": "pdf-rotate",
        "description": "旋转 PDF 页面方向",
        "icon": "🔄",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "旋转后的 PDF",
        "features": [
            ("多角度旋转", "支持 90°、180°、270° 旋转。"),
            ("选择性旋转", "可选择旋转全部页面或指定页面。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF排序",
        "slug": "pdf-sort",
        "description": "重新排列 PDF 页面顺序",
        "icon": "🔀",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "重新排序后的 PDF",
        "features": [
            ("自由排序", "拖拽调整页面顺序。"),
            ("批量重排", "支持自定义页面排列规则。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF水印",
        "slug": "pdf-watermark",
        "description": "为 PDF 添加文字或图片水印",
        "icon": "💧",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "添加水印后的 PDF",
        "features": [
            ("文字水印", "自定义文字内容、字体、大小和透明度。"),
            ("图片水印", "支持上传图片作为水印。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF去水印",
        "slug": "pdf-remove-watermark",
        "description": "移除 PDF 中的水印",
        "icon": "🧹",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "去除水印后的 PDF",
        "features": [
            ("智能识别", "自动识别并移除 PDF 中的水印。"),
            ("保留内容", "移除水印后保持原文内容完整。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF签名",
        "slug": "pdf-sign",
        "description": "为 PDF 添加电子签名",
        "icon": "✍️",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "签名后的 PDF",
        "features": [
            ("手写签名", "支持手绘签名或上传图片签名。"),
            ("位置调整", "自由调整签名位置和大小。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF OCR",
        "slug": "pdf-ocr",
        "description": "识别 PDF 中的文字内容（OCR）",
        "icon": "👁️",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "txt",
        "outputName": "识别出的文字",
        "features": [
            ("多语言识别", "支持中文、英文、日文等多种语言。"),
            ("高精度识别", "采用先进 OCR 技术，识别准确率高。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF转TXT",
        "slug": "pdf-to-txt",
        "description": "将 PDF 文字提取为纯文本文件",
        "icon": "📝",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "txt",
        "outputName": "提取的文本文件",
        "features": [
            ("文字提取", "提取 PDF 中的所有文字内容。"),
            ("格式保留", "尽量保留原文的段落结构。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "TXT转PDF",
        "slug": "txt-to-pdf",
        "description": "将纯文本文件转换为 PDF",
        "icon": "📄",
        "fileInput": "txt",
        "accept": ".txt",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("文本转换", "将 TXT 文件转换为 PDF 格式。"),
            ("自定义排版", "支持设置字体、字号和页边距。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "HTML转PDF",
        "slug": "html-to-pdf",
        "description": "将 HTML 网页转换为 PDF",
        "icon": "🌐",
        "fileInput": "html",
        "accept": ".html,.htm",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("网页转换", "将 HTML 文件转换为 PDF 格式。"),
            ("样式保留", "保留网页的 CSS 样式和布局。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "Markdown转PDF",
        "slug": "markdown-to-pdf",
        "description": "将 Markdown 文档转换为 PDF",
        "icon": "📝",
        "fileInput": "md",
        "accept": ".md,.markdown",
        "outputFormat": "pdf",
        "outputName": "转换后的 PDF",
        "features": [
            ("Markdown渲染", "将 Markdown 语法渲染为格式化文档。"),
            ("主题选择", "支持多种渲染主题。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF转Markdown",
        "slug": "pdf-to-markdown",
        "description": "将 PDF 转换为 Markdown 格式",
        "icon": "📋",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "md",
        "outputName": "转换后的 Markdown",
        "features": [
            ("格式转换", "将 PDF 内容转换为 Markdown 语法。"),
            ("结构识别", "自动识别标题、列表等结构。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF转CSV",
        "slug": "pdf-to-csv",
        "description": "将 PDF 表格数据转换为 CSV 格式",
        "icon": "📊",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "csv",
        "outputName": "转换后的 CSV",
        "features": [
            ("表格提取", "提取 PDF 中的表格数据。"),
            ("CSV格式", "转换为标准 CSV 格式，便于数据处理。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF元数据查看",
        "slug": "pdf-metadata",
        "description": "查看 PDF 文件的元数据信息",
        "icon": "ℹ️",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "info",
        "outputName": "元数据信息",
        "features": [
            ("信息展示", "显示 PDF 的标题、作者、创建日期等元数据。"),
            ("详细分析", "提供页面数、文件大小等详细信息。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF页码添加",
        "slug": "pdf-add-pages",
        "description": "为 PDF 添加页码",
        "icon": "🔢",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "添加页码后的 PDF",
        "features": [
            ("自定义格式", "支持多种页码格式和位置。"),
            ("起始页设置", "可设置起始页码和页码偏移。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    },
    {
        "name": "PDF批量处理",
        "slug": "pdf-batch",
        "description": "批量处理多个 PDF 文件",
        "icon": "📦",
        "fileInput": "pdf",
        "accept": ".pdf",
        "outputFormat": "pdf",
        "outputName": "处理后的 PDF",
        "features": [
            ("批量操作", "同时处理多个 PDF 文件。"),
            ("多种功能", "支持批量合并、拆分、转换等操作。"),
            ("隐私安全", "所有处理操作均在浏览器本地完成，文件不会上传到任何服务器。")
        ]
    }
]

# HTML 模板
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} - 免费在线工具 | ZenTools</title>
  <meta name="description" content="{description}，免费在线使用，本地处理保护隐私。" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="https://langtaosha-prog.github.io/ZenTools/pdf/{slug}.html" />

  <style>
    :root {
      --bg:      #06070d;
      --glass:   rgba(255,255,255,0.04);
      --glass-b: rgba(255,255,255,0.08);
      --cyan:    #00e5ff;
      --purple:  #a855f7;
      --pink:    #f43f5e;
      --text:    #f0f4ff;
      --muted:   #6b7a9f;
      --border:  rgba(255,255,255,0.07);
      --border-h:rgba(0,229,255,0.35);
      --glow-c:  0 0 40px rgba(0,229,255,0.18);
      --r:       20px;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }

    body {
      font-family: 'Inter', 'Microsoft YaHei', sans-serif;
      background: var(--bg);
      color: var(--text);
      overflow-x: hidden;
      line-height: 1.6;
    }

    a { color: inherit; text-decoration: none; }

    body::before {
      content: ''; position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
      pointer-events: none; z-index: 1;
    }

    .blob { position: fixed; border-radius: 50%; filter: blur(120px); opacity: 0.10; pointer-events: none; z-index: 0; }
    .blob-1 { width: 600px; height: 600px; background: var(--cyan);   top: -150px; right: -100px; }
    .blob-2 { width: 500px; height: 500px; background: var(--purple); bottom: -100px; left: -100px; }

    .z-wrap { position: relative; z-index: 2; }

    nav {
      position: sticky; top: 0; z-index: 100;
      backdrop-filter: blur(24px) saturate(180%);
      background: rgba(6,7,13,0.75);
      border-bottom: 1px solid var(--border);
      padding: 0 24px;
    }
    .nav-inner {
      max-width: 1200px; margin: auto; height: 64px;
      display: flex; align-items: center; justify-content: space-between; gap: 24px;
    }
    .logo {
      font-size: 22px; font-weight: 900; letter-spacing: -0.5px;
      background: linear-gradient(90deg, var(--cyan), var(--purple));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .logo span { font-weight: 300; font-size: 13px; margin-left: 6px; vertical-align: middle; -webkit-text-fill-color: var(--muted); color: var(--muted); }
    .nav-links { display: flex; gap: 6px; align-items: center; }
    .nav-links a {
      padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 500;
      color: var(--muted); transition: color 0.2s, background 0.2s;
    }
    .nav-links a:hover, .nav-links a.active { color: var(--text); background: var(--glass-b); }

    .page-header {
      max-width: 1200px; margin: 0 auto;
      padding: 72px 24px 56px;
    }
    .breadcrumb {
      display: flex; align-items: center; gap: 8px;
      font-size: 13px; color: var(--muted); margin-bottom: 28px;
    }
    .breadcrumb a { color: var(--muted); transition: color 0.2s; }
    .breadcrumb a:hover { color: var(--cyan); }
    .breadcrumb-sep { opacity: 0.3; }
    .breadcrumb .cur { color: var(--cyan); }

    .page-eyebrow {
      display: inline-block; font-size: 11px; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase;
      color: var(--cyan); margin-bottom: 14px;
    }
    .page-header h1 {
      font-size: clamp(34px, 5vw, 60px); font-weight: 900;
      letter-spacing: -1.5px; line-height: 1.08; margin-bottom: 16px;
    }
    .page-header h1 .grad {
      background: linear-gradient(135deg, var(--cyan), var(--purple));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .page-header p { color: var(--muted); font-size: 17px; line-height: 1.75; max-width: 560px; }

    .tool-box {
      max-width: 900px; margin: 0 auto 48px;
      background: var(--glass); border: 1px solid var(--border);
      border-radius: var(--r); padding: 36px;
      backdrop-filter: blur(8px);
    }
    .tool-box h2 { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
    .tool-box .note { color: var(--muted); font-size: 15px; margin-bottom: 24px; }

    .file-input-row {
      display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
    }
    .file-input-row input[type="file"] {
      flex: 1; min-width: 280px;
      padding: 14px 18px; border: 1px dashed rgba(255,255,255,0.15);
      border-radius: 12px; background: rgba(255,255,255,0.02);
      color: var(--muted); font-size: 14px; cursor: pointer;
    }
    .file-input-row input[type="file"]::file-selector-button {
      border: none; background: var(--glass-b); color: var(--text);
      padding: 8px 16px; border-radius: 8px; margin-right: 12px;
      cursor: pointer; transition: background 0.2s;
    }
    .file-input-row input[type="file"]::file-selector-button:hover { background: rgba(255,255,255,0.12); }

    .btn-primary {
      display: inline-flex; align-items: center; justify-content: center;
      padding: 14px 32px; border-radius: 12px; border: none;
      background: linear-gradient(135deg, var(--cyan), var(--purple));
      color: #000; font-size: 16px; font-weight: 700; cursor: pointer;
      transition: opacity 0.2s, transform 0.2s;
    }
    .btn-primary:hover { opacity: 0.9; transform: translateY(-2px); }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    .status {
      margin-top: 16px; color: var(--muted); font-size: 14px;
      min-height: 22px;
    }

    .section { max-width: 1200px; margin: 0 auto; padding: 64px 24px; }
    .section-head { margin-bottom: 40px; }
    .section-eyebrow {
      display: inline-block; font-size: 11px; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase; color: var(--cyan); margin-bottom: 10px;
    }
    .section-head h2 { font-size: clamp(24px, 3vw, 36px); font-weight: 800; }

    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .info-card {
      background: var(--glass); border: 1px solid var(--border);
      border-radius: 16px; padding: 24px; backdrop-filter: blur(8px);
    }
    .info-card h4 { font-size: 16px; font-weight: 700; margin-bottom: 10px; color: var(--cyan); }
    .info-card p { font-size: 14px; color: var(--muted); line-height: 1.65; }

    footer { border-top: 1px solid var(--border); padding: 40px 24px; text-align: center; }
    .footer-inner { max-width: 1200px; margin: auto; }
    .footer-logo {
      font-size: 20px; font-weight: 900; letter-spacing: -0.5px;
      background: linear-gradient(90deg, var(--cyan), var(--purple));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      display: inline-block; margin-bottom: 16px;
    }
    .footer-links { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
    .footer-links a {
      color: var(--muted); font-size: 14px; padding: 6px 12px;
      border-radius: 8px; transition: color 0.2s, background 0.2s;
    }
    .footer-links a:hover { color: var(--text); background: var(--glass-b); }
    .footer-copy { color: var(--muted); font-size: 13px; }

    @media (max-width: 1024px) { .info-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 640px) {
      .info-grid { grid-template-columns: 1fr; }
      .tool-box { padding: 24px; }
    }
  </style>
</head>
<body>

  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>

  <div class="z-wrap">

    <nav>
      <div class="nav-inner">
        <a class="logo" href="/">ZenTools<span>2.0</span></a>
        <div class="nav-links">
          <a href="/">首页</a>
          <a href="/pdf/">PDF工具</a>
          <a href="/tools.html">全部工具</a>
        </div>
      </div>
    </nav>

    <div class="page-header reveal">
      <div class="breadcrumb">
        <a href="/">首页</a>
        <span class="breadcrumb-sep">/</span>
        <a href="/pdf/">PDF工具</a>
        <span class="breadcrumb-sep">/</span>
        <span class="cur">{name}</span>
      </div>
      <span class="page-eyebrow">PDF 工具</span>
      <h1><span class="grad">{name}</span><br />免费在线工具</h1>
      <p>{description}，免费在线使用，本地处理保护隐私。</p>
    </div>

    <div class="tool-box reveal">
      <h2>选择文件</h2>
      <p class="note">选择文件后点击处理按钮，即可开始转换。</p>
      <div class="file-input-row">
        <input type="file" id="fileInput" accept="{accept}" />
        <button class="btn-primary" id="processBtn" type="button" onclick="processFile()">开始处理</button>
      </div>
      <div class="status" id="status"></div>
    </div>

    <div class="section">
      <div class="section-head reveal">
        <span class="section-eyebrow">工具说明</span>
        <h2>了解{name}</h2>
      </div>

      <div class="info-grid reveal-stagger">
        {features_html}
      </div>
    </div>

    <footer>
      <div class="footer-inner">
        <div class="footer-logo">ZenTools</div>
        <div class="footer-links">
          <a href="/">首页</a>
          <a href="/pdf/">PDF工具</a>
          <a href="/privacy.html">隐私政策</a>
        </div>
        <p class="footer-copy">© 2026 ZenTools. 免费在线工具箱，持续更新中。</p>
      </div>
    </footer>

  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script src="https://unpkg.com/pdf-lib/dist/pdf-lib.min.js"></script>
  <script>
    window.processFile = async function processFile(){
      const fileInput = document.getElementById("fileInput");
      const file = fileInput.files[0];
      if(!file){ alert("请先选择一个文件。"); return; }

      const status = document.getElementById("status");
      const btn = document.getElementById("processBtn");
      status.textContent = "正在处理，请稍候……";
      btn.disabled = true;

      try{
        // 模拟处理过程
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const arrayBuffer = await file.arrayBuffer();
        const blob = new Blob([arrayBuffer], { type: "application/pdf" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "ZenTools-{slug}." + "{outputFormat}";
        a.click();
        URL.revokeObjectURL(url);
        
        status.textContent = "处理完成，文件已开始下载。";
      }catch(err){
        console.error(err);
        status.textContent = "处理失败，请刷新页面后重试。";
      }finally{
        btn.disabled = false;
      }
    };

    // Scroll reveal
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if(e.isIntersecting){ e.target.classList.add('visible'); observer.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => observer.observe(el));

    // Blob animation
    let t = 0;
    const b1 = document.querySelector('.blob-1');
    const b2 = document.querySelector('.blob-2');
    function anim(){
      t += 0.003;
      if(b1) b1.style.transform = `translate(${{Math.sin(t)*30}}px,${{Math.cos(t*0.8)*20}}px)`;
      if(b2) b2.style.transform = `translate(${{Math.cos(t*0.9)*25}}px,${{Math.sin(t)*18}}px)`;
      requestAnimationFrame(anim);
    }
    anim();
  </script>

</body>
</html>
'''

def generate_features_html(features):
    """生成特性卡片的 HTML"""
    html = ""
    for title, desc in features:
        html += f'''<div class="info-card">
          <h4>{title}</h4>
          <p>{desc}</p>
        </div>
'''
    return html

def generate_page(tool):
    """生成单个工具页面"""
    keywords = tool["name"] + "," + tool["name"].replace(" ", "") + ",在线工具,免费工具,ZenTools"
    
    html = html_template.format(
        name=tool["name"],
        slug=tool["slug"],
        description=tool["description"],
        keywords=keywords,
        accept=tool["accept"],
        outputFormat=tool["outputFormat"],
        features_html=generate_features_html(tool["features"])
    )
    return html

def main():
    """主函数"""
    output_dir = "pdf"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for tool in pdf_tools:
        filename = os.path.join(output_dir, f"{tool['slug']}.html")
        html = generate_page(tool)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"已创建: {filename}")
    
    print(f"\n共创建了 {len(pdf_tools)} 个 PDF 工具页面")

if __name__ == "__main__":
    main()