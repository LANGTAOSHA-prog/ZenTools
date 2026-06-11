# PDF Tools

这个文件夹包含用于演示与测试的简单 PDF 工具：合并、拆分、提取页面与批量处理。

安装依赖：

```bash
pip install -r pdf_tools/requirements.txt
```

示例：

生成示例 PDF：
```bash
python pdf_tools/pdf_tools.py create-samples
```

合并：
```bash
python pdf_tools/pdf_tools.py merge pdf_tools/samples/sample1.pdf pdf_tools/samples/sample2.pdf -o pdf_tools/out/merged.pdf
```

拆分：
```bash
python pdf_tools/pdf_tools.py split pdf_tools/samples/sample2.pdf -d pdf_tools/out/split_sample2
```

提取页面：
```bash
python pdf_tools/pdf_tools.py extract pdf_tools/samples/sample2.pdf 2 3 -o pdf_tools/out/extracted.pdf
```

批量处理（示例：合并文件夹内所有 PDF）：
```bash
python pdf_tools/pdf_tools.py batch --op merge --input pdf_tools/samples --out pdf_tools/out
```
