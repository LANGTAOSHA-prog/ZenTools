@echo off
chcp 65001 >nul
echo 开始创建 PDF 工具页面...
python create_pdf_pages.py
if errorlevel 1 (
    echo Python 执行失败，尝试使用完整路径...
    "C:\Users\taojiang\AppData\Local\Microsoft\WindowsApps\python.exe" create_pdf_pages.py
)
if errorlevel 1 (
    echo 所有尝试都失败了。请检查 Python 是否正确安装。
    pause
) else (
    echo 页面创建完成！
    pause
)