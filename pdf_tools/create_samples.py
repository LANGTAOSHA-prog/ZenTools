"""生成示例 PDF 文件，用于测试 PDF 工具。
生成几个简单的 PDF: sample1.pdf, sample2.pdf, sample3.pdf
"""
from fpdf import FPDF
from pathlib import Path

OUT = Path(__file__).parent / "samples"
OUT.mkdir(exist_ok=True)

def make_pdf(path: Path, title: str, pages: int = 2):
    pdf = FPDF()
    for i in range(1, pages+1):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, f'This is page {i} of {title}.')
    pdf.output(str(path))

def main():
    make_pdf(OUT / 'sample1.pdf', 'Sample A', pages=2)
    make_pdf(OUT / 'sample2.pdf', 'Sample B', pages=3)
    make_pdf(OUT / 'sample3.pdf', 'Sample C', pages=1)
    print('Created sample PDFs in', OUT)

if __name__ == '__main__':
    main()
