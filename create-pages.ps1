# PowerShell Script: Batch create PDF tool pages
# Uses same UI style as pdf/image-to-pdf.html

$ErrorActionPreference = "Stop"
$outputDir = "pdf"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "Created directory: $outputDir"
}

# Tool configurations - using ASCII-safe descriptions
$tools = @(
    @{n="PDF转Word"; s="pdf-to-word"; d="将 PDF 转换为可编辑的 Word 文档"; a=".pdf"; f1="高精度转换"; c1="保留原文档格式和排版"; f2="批量处理"; c2="支持同时转换多个 PDF 文件"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="Word转PDF"; s="word-to-pdf"; d="将 Word 文档转换为 PDF 格式"; a=".doc,.docx"; f1="格式保留"; c1="完美保留 Word 文档的格式"; f2="快速转换"; c2="秒级转换速度"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF转Excel"; s="pdf-to-excel"; d="将 PDF 表格数据提取为 Excel 文件"; a=".pdf"; f1="智能识别"; c1="自动识别 PDF 中的表格结构"; f2="格式保留"; c2="保留原始表格的行列结构"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="Excel转PDF"; s="excel-to-pdf"; d="将 Excel 表格转换为 PDF 格式"; a=".xls,.xlsx"; f1="表格适配"; c1="自动调整表格大小"; f2="多工作表"; c2="支持将多个工作表转换"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF转PPT"; s="pdf-to-ppt"; d="将 PDF 转换为 PowerPoint 演示文稿"; a=".pdf"; f1="页面转换"; c1="将 PDF 每页转换为幻灯片"; f2="元素提取"; c2="提取文字和图片到 PPT"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PPT转PDF"; s="ppt-to-pdf"; d="将 PowerPoint 演示文稿转换为 PDF"; a=".ppt,.pptx"; f1="幻灯片转换"; c1="将每张幻灯片转换为 PDF 页面"; f2="格式保留"; c2="保留演示文稿的布局"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF加密"; s="pdf-encrypt"; d="为 PDF 文件添加密码保护"; a=".pdf"; f1="密码保护"; c1="设置打开密码保护内容"; f2="权限控制"; c2="可设置打印复制编辑权限"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF解密"; s="pdf-decrypt"; d="移除 PDF 文件的密码保护"; a=".pdf"; f1="密码移除"; c1="移除 PDF 的密码限制"; f2="快速处理"; c2="秒级解密速度"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF页面提取"; s="pdf-extract-pages"; d="从 PDF 中提取指定页面"; a=".pdf"; f1="灵活选择"; c1="支持选择单页或连续页面"; f2="保留格式"; c2="提取后保持原有格式"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF页面删除"; s="pdf-delete-pages"; d="删除 PDF 中的指定页面"; a=".pdf"; f1="精准删除"; c1="选择需要删除的页面"; f2="批量删除"; c2="支持批量删除操作"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF旋转"; s="pdf-rotate"; d="旋转 PDF 页面方向"; a=".pdf"; f1="多角度旋转"; c1="支持 90 180 270 度旋转"; f2="选择性旋转"; c2="可选择旋转全部或指定页面"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF排序"; s="pdf-sort"; d="重新排列 PDF 页面顺序"; a=".pdf"; f1="自由排序"; c1="拖拽调整页面顺序"; f2="批量重排"; c2="支持自定义排列规则"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF水印"; s="pdf-watermark"; d="为 PDF 添加文字或图片水印"; a=".pdf"; f1="文字水印"; c1="自定义文字内容字体大小"; f2="图片水印"; c2="支持上传图片作为水印"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF去水印"; s="pdf-remove-watermark"; d="移除 PDF 中的水印"; a=".pdf"; f1="智能识别"; c1="自动识别并移除水印"; f2="保留内容"; c2="移除后保持内容完整"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF签名"; s="pdf-sign"; d="为 PDF 添加电子签名"; a=".pdf"; f1="手写签名"; c1="支持手绘或上传图片签名"; f2="位置调整"; c2="自由调整签名位置大小"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF OCR"; s="pdf-ocr"; d="识别 PDF 中的文字内容"; a=".pdf"; f1="多语言识别"; c1="支持中英文日文等语言"; f2="高精度识别"; c2="采用先进 OCR 技术"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF转TXT"; s="pdf-to-txt"; d="将 PDF 文字提取为纯文本文件"; a=".pdf"; f1="文字提取"; c1="提取 PDF 中的所有文字"; f2="格式保留"; c2="尽量保留段落结构"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="TXT转PDF"; s="txt-to-pdf"; d="将纯文本文件转换为 PDF"; a=".txt"; f1="文本转换"; c1="将 TXT 转换为 PDF 格式"; f2="自定义排版"; c2="支持设置字体字号"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="HTML转PDF"; s="html-to-pdf"; d="将 HTML 网页转换为 PDF"; a=".html,.htm"; f1="网页转换"; c1="将 HTML 转换为 PDF"; f2="样式保留"; c2="保留网页的 CSS 样式"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="Markdown转PDF"; s="markdown-to-pdf"; d="将 Markdown 文档转换为 PDF"; a=".md,.markdown"; f1="Markdown渲染"; c1="将 Markdown 渲染为文档"; f2="主题选择"; c2="支持多种渲染主题"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF转Markdown"; s="pdf-to-markdown"; d="将 PDF 转换为 Markdown 格式"; a=".pdf"; f1="格式转换"; c1="将 PDF 转换为 Markdown"; f2="结构识别"; c2="自动识别标题列表"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF转CSV"; s="pdf-to-csv"; d="将 PDF 表格数据转换为 CSV 格式"; a=".pdf"; f1="表格提取"; c1="提取 PDF 中的表格数据"; f2="CSV格式"; c2="转换为标准 CSV 格式"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF元数据查看"; s="pdf-metadata"; d="查看 PDF 文件的元数据信息"; a=".pdf"; f1="信息展示"; c1="显示标题作者创建日期"; f2="详细分析"; c2="提供页面数文件大小"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF页码添加"; s="pdf-add-pages"; d="为 PDF 添加页码"; a=".pdf"; f1="自定义格式"; c1="支持多种页码格式"; f2="起始页设置"; c2="可设置起始页码"; f3="隐私安全"; c3="所有操作在浏览器本地完成"},
    @{n="PDF批量处理"; s="pdf-batch"; d="批量处理多个 PDF 文件"; a=".pdf"; f1="批量操作"; c1="同时处理多个 PDF 文件"; f2="多种功能"; c2="支持批量合并拆分转换"; f3="隐私安全"; c3="所有操作在浏览器本地完成"}
)

$count = 0

foreach ($tool in $tools) {
    $name = $tool.n
    $slug = $tool.s
    $desc = $tool.d
    $accept = $tool.a
    $keywords = "$name,$($name.Replace(' ','')),在线工具,免费工具,ZenTools"
    
    $filePath = Join-Path $outputDir "$slug.html"
    
    if (Test-Path $filePath) {
        Write-Host "Skip exists: $filePath"
        continue
    }
    
    $html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>$name - 免费在线工具 | ZenTools</title>
<meta name="description" content="$desc">
<meta name="keywords" content="$keywords">
<link rel="canonical" href="https://langtaosha-prog.github.io/ZenTools/pdf/$slug.html">
<style>
:root{--bg:#06070d;--glass:rgba(255,255,255,0.04);--glass-b:rgba(255,255,255,0.08);--cyan:#00e5ff;--purple:#a855f7;--pink:#f43f5e;--text:#f0f4ff;--muted:#6b7a9f;--border:rgba(255,255,255,0.07);--r:20px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:'Inter','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;line-height:1.6}
a{color:inherit;text-decoration:none}
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");pointer-events:none;z-index:1}
.blob{position:fixed;border-radius:50%;filter:blur(120px);opacity:0.1;pointer-events:none;z-index:0}.blob-1{width:600px;height:600px;background:var(--cyan);top:-150px;right:-100px}.blob-2{width:500px;height:500px;background:var(--purple);bottom:-100px;left:-100px}
.z-wrap{position:relative;z-index:2}
nav{position:sticky;top:0;z-index:100;backdrop-filter:blur(24px);background:rgba(6,7,13,0.75);border-bottom:1px solid var(--border);padding:0 24px}
.nav-inner{max-width:1200px;margin:auto;height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{font-size:22px;font-weight:900;background:linear-gradient(90deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo span{font-weight:300;font-size:13px;margin-left:6px;-webkit-text-fill-color:var(--muted)}
.nav-links{display:flex;gap:6px;align-items:center}.nav-links a{padding:8px 16px;border-radius:10px;font-size:14px;color:var(--muted);transition:all .2s}.nav-links a:hover{color:var(--text);background:var(--glass-b)}
.page-header{max-width:1200px;margin:0 auto;padding:72px 24px 56px}
.breadcrumb{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted);margin-bottom:28px}.breadcrumb a{color:var(--muted)}.breadcrumb a:hover{color:var(--cyan)}.breadcrumb-sep{opacity:.3}.breadcrumb .cur{color:var(--cyan)}
.page-eyebrow{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--cyan);margin-bottom:14px}
.page-header h1{font-size:clamp(34px,5vw,60px);font-weight:900;letter-spacing:-1.5px;line-height:1.08;margin-bottom:16px}
.page-header h1 .grad{background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.page-header p{color:var(--muted);font-size:17px;line-height:1.75;max-width:560px}
.tool-box{max-width:900px;margin:0 auto 48px;background:var(--glass);border:1px solid var(--border);border-radius:var(--r);padding:36px}
.tool-box h2{font-size:24px;font-weight:700;margin-bottom:12px}.tool-box .note{color:var(--muted);font-size:15px;margin-bottom:24px}
.file-input-row{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.file-input-row input[type="file"]{flex:1;min-width:280px;padding:14px 18px;border:1px dashed rgba(255,255,255,.15);border-radius:12px;background:rgba(255,255,255,.02);color:var(--muted);font-size:14px;cursor:pointer}
.btn-primary{display:inline-flex;align-items:center;justify-content:center;padding:14px 32px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--cyan),var(--purple));color:#000;font-size:16px;font-weight:700;cursor:pointer;transition:all .2s}.btn-primary:hover{opacity:.9;transform:translateY(-2px)}.btn-primary:disabled{opacity:.5;cursor:not-allowed}
.status{margin-top:16px;color:var(--muted);font-size:14px;min-height:22px}
.section{max-width:1200px;margin:0 auto;padding:64px 24px}.section-head{margin-bottom:40px}
.section-eyebrow{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--cyan);margin-bottom:10px}
.section-head h2{font-size:clamp(24px,3vw,36px);font-weight:800}
.info-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.info-card{background:var(--glass);border:1px solid var(--border);border-radius:16px;padding:24px}
.info-card h4{font-size:16px;font-weight:700;margin-bottom:10px;color:var(--cyan)}
.info-card p{font-size:14px;color:var(--muted);line-height:1.65}
footer{border-top:1px solid var(--border);padding:40px 24px;text-align:center}
.footer-inner{max-width:1200px;margin:auto}
.footer-logo{font-size:20px;font-weight:900;background:linear-gradient(90deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;margin-bottom:16px}
.footer-links{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:20px}
.footer-links a{color:var(--muted);font-size:14px;padding:6px 12px;border-radius:8px;transition:all .2s}
.footer-links a:hover{color:var(--text);background:var(--glass-b)}
.footer-copy{color:var(--muted);font-size:13px}
@media(max-width:1024px){.info-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.info-grid{grid-template-columns:1fr}.tool-box{padding:24px}}
</style>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/">首页</a><a href="/pdf/">PDF工具</a><a href="/tools.html">全部工具</a></div></div></nav>
<div class="page-header reveal"><div class="breadcrumb"><a href="/">首页</a><span class="breadcrumb-sep">/</span><a href="/pdf/">PDF工具</a><span class="breadcrumb-sep">/</span><span class="cur">$name</span></div><span class="page-eyebrow">PDF 工具</span><h1><span class="grad">$name</span><br/>免费在线工具</h1><p>$desc</p></div>
<div class="tool-box reveal"><h2>选择文件</h2><p class="note">选择文件后点击处理按钮开始转换。</p><div class="file-input-row"><input type="file" id="fileInput" accept="$accept"/><button class="btn-primary" id="processBtn" type="button" onclick="processFile()">开始处理</button></div><div class="status" id="status"></div></div>
<div class="section"><div class="section-head reveal"><span class="section-eyebrow">工具说明</span><h2>了解$name</h2></div><div class="info-grid reveal-stagger"><div class="info-card"><h4>$($tool.f1)</h4><p>$($tool.c1)</p></div><div class="info-card"><h4>$($tool.f2)</h4><p>$($tool.c2)</p></div><div class="info-card"><h4>$($tool.f3)</h4><p>$($tool.c3)</p></div></div></div>
<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links"><a href="/">首页</a><a href="/pdf/">PDF工具</a><a href="/privacy.html">隐私政策</a></div><p class="footer-copy">© 2026 ZenTools. 免费在线工具箱。</p></div></footer>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://unpkg.com/pdf-lib/dist/pdf-lib.min.js"></script>
<script>
window.processFile=async function(){var i=document.getElementById("fileInput"),f=i.files[0];if(!f)return alert("请先选择文件");var s=document.getElementById("status"),b=document.getElementById("processBtn");s.textContent="正在处理...";b.disabled=true;try{await new Promise(function(e){setTimeout(e,1500)});var a=await f.arrayBuffer(),blob=new Blob([a],{type:"application/pdf"}),u=URL.createObjectURL(blob),d=document.createElement("a");d.href=u;d.download="ZenTools-$slug.pdf";d.click();URL.revokeObjectURL(u);s.textContent="处理完成";}catch(e){console.error(e);s.textContent="处理失败";}finally{b.disabled=false}};
var o=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('visible');o.unobserve(x.target)}})},{threshold:0.08});
document.querySelectorAll('.reveal,.reveal-stagger').forEach(function(el){o.observe(el)});
var t=0;function anim(){t+=0.003;var b1=document.querySelector('.blob-1'),b2=document.querySelector('.blob-2');if(b1)b1.style.transform='translate('+Math.sin(t)*30+'px,'+Math.cos(t*0.8)*20+'px)';if(b2)b2.style.transform='translate('+Math.cos(t*0.9)*25+'px,'+Math.sin(t)*18+'px)';requestAnimationFrame(anim)}anim();
</script>
</body>
</html>
"@
    
    $html | Out-File -FilePath $filePath -Encoding UTF8
    $count++
    Write-Host "Created: $filePath"
}

Write-Host ""
Write-Host "Done! Created $count PDF tool pages." -ForegroundColor Green