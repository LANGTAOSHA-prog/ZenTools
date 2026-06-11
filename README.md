# PDF Tools

本仓库包含一个小型 PDF 工具包，位于 `pdf_tools/` 目录，当前分支（演示分支）：`feat/pdf-tools`。

工具列表（实现于 `pdf_tools/pdf_tools.py`）：

- 合并 PDF（merge）
- 拆分 PDF（split）
- 提取页面（extract）
- 批量处理（batch）

快速使用示例：

```bash
# 生成示例 PDF
python pdf_tools/pdf_tools.py create-samples

# 合并
python pdf_tools/pdf_tools.py merge pdf_tools/samples/sample1.pdf pdf_tools/samples/sample2.pdf -o pdf_tools/out/merged.pdf

# 拆分
python pdf_tools/pdf_tools.py split pdf_tools/samples/sample2.pdf -d pdf_tools/out/split_sample2

# 提取页面（示例：提取第 2 和第 3 页）
python pdf_tools/pdf_tools.py extract pdf_tools/samples/sample2.pdf 2 3 -o pdf_tools/out/extracted.pdf

# 批量合并 samples 目录下所有 PDF
python pdf_tools/pdf_tools.py batch --op merge --input pdf_tools/samples --out pdf_tools/out
```

更多说明请参阅： `pdf_tools/README.md`
