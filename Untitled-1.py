"""命令行 PDF 工具：合并、拆分、提取页面、批量处理

依赖：pypdf, fpdf2 (用于生成示例)
用法示例：
  python pdf_tools.py create-samples
  python pdf_tools.py merge samples/sample1.pdf samples/sample2.pdf -o merged.pdf
  python pdf_tools.py split samples/sample2.pdf -d out/split
  python pdf_tools.py extract samples/sample2.pdf 2 3 -o out/extracted.pdf
  python pdf_tools.py batch --op split --input samples --out out/batch_split
"""
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import sys


def merge_pdfs(inputs, output):
    writer = PdfWriter()
    for p in inputs:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    writer.write(str(output))
    print('Merged', len(inputs), 'files ->', output)


def split_pdf(input_path, out_dir):
    reader = PdfReader(str(input_path))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_file = out_dir / f'{Path(input_path).stem}_page_{i}.pdf'
        writer.write(str(out_file))
    print('Split into', len(reader.pages), 'pages in', out_dir)


def extract_pages(input_path, pages, output):
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    num_pages = len(reader.pages)
    for p in pages:
        if p < 1 or p > num_pages:
            print(f'Warning: page {p} out of range (1-{num_pages}), skipping')
            continue
        writer.add_page(reader.pages[p-1])
    writer.write(str(output))
    print('Extracted pages', pages, '->', output)


def batch_process(op, input_dir, out_dir):
    input_dir = Path(input_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = sorted(input_dir.glob('*.pdf'))
    if not pdf_files:
        print('No PDF files found in', input_dir)
        return
    if op == 'merge':
        # merge all into single file
        merge_pdfs(pdf_files, out_dir / f'{input_dir.name}_merged.pdf')
    elif op == 'split':
        # split each pdf into its own folder
        for p in pdf_files:
            target = out_dir / p.stem
            split_pdf(p, target)
    else:
        print('Unknown batch op:', op)


def build_cli():
    ap = argparse.ArgumentParser(prog='pdf_tools')
    sub = ap.add_subparsers(dest='cmd')

    sub.add_parser('create-samples')

    m = sub.add_parser('merge')
    m.add_argument('inputs', nargs='+')
    m.add_argument('-o', '--output', required=True)

    s = sub.add_parser('split')
    s.add_argument('input')
    s.add_argument('-d', '--outdir', required=True)

    e = sub.add_parser('extract')
    e.add_argument('input')
    e.add_argument('pages', nargs='+', type=int)
    e.add_argument('-o', '--output', required=True)

    b = sub.add_parser('batch')
    b.add_argument('--op', choices=['merge', 'split'], required=True)
    b.add_argument('--input', required=True)
    b.add_argument('--out', required=True)

    return ap


def main():
    ap = build_cli()
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        sys.exit(1)
    if args.cmd == 'create-samples':
        # lazy import
        from create_samples import main as cs
        cs()
    elif args.cmd == 'merge':
        inputs = [Path(p) for p in args.inputs]
        merge_pdfs(inputs, Path(args.output))
    elif args.cmd == 'split':
        split_pdf(Path(args.input), Path(args.outdir))
    elif args.cmd == 'extract':
        extract_pages(Path(args.input), args.pages, Path(args.output))
    elif args.cmd == 'batch':
        batch_process(args.op, args.input, args.out)


if __name__ == '__main__':
    main()