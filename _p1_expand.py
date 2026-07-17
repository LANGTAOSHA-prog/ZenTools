# -*- coding: utf-8 -*-
"""
P1 内容扩写生成器（试点版：PDF 分类，英文正文）
白帽策略：
- 正文英文（站点实质英文索引页；.xyz+Google 全球受众；与现有英文骨架一致）。
- 每页内容 = 工具真实功能专属要点(name__en + 手写 per-tool bullets) + 分类知识库(真实用法/技巧/FAQ)。
  由此保证每页独有且有信息量，避免旋转/套话。
- 结构升级：Main Features -> <ul>，How to Use -> <ol>，FAQ 扩到 4 条并同步 JSON-LD FAQPage。
- 保留 CRLF 与全部 DOM/脚本。
"""
import json, os, re, sys, html as htmlmod

BASE = os.path.dirname(os.path.abspath(__file__))
PILOT_CATEGORY = "PDF工具"

# ---------- 分类知识库（手写真实内容） ----------
CATEGORY_MODULE = {
    "audiences": [
        "Office and admin staff who organize contracts, reports, and invoices every day",
        "Students and teachers handling theses, courseware, and scanned materials",
        "Legal and finance teams working with sensitive documents that need encryption",
        "Creators and e-commerce operators who turn materials into shareable PDFs or images",
    ],
    "tips": [
        "Name your files clearly before a batch job so the output stays easy to tell apart.",
        "For sensitive files, prefer tools that process everything locally and support encryption.",
        "Compress before merging large files to keep the whole process fast.",
        "After export, check page order and bookmarks once so the delivery is correct.",
    ],
    "faqs": [
        ("Will my PDF files be uploaded to a server?",
         "No. Every operation runs locally in your browser, so your files never leave your device. This is safe for contracts, invoices, and other confidential documents."),
        ("Do I need to install software or create an account?",
         "Neither. The tool runs entirely in the browser, opens instantly, and is free to use."),
        ("Will a very large file make it slow?",
         "Because computation happens on your device, speed depends on its performance. For huge files, split or compress first, then process."),
        ("Does the layout break after conversion?",
         "The tool keeps the original layout, fonts, and images as much as possible. For a few complex layouts, do a quick check after export."),
    ],
}

# ---------- 每工具专属英文要点（基于真实功能，互不雷同） ----------
# key = url 路径; value = (name_en, [核心功能 bullet 3-5 条], 使用场景句子)
PDF_TOOL_NOTES = {
    "/pdf/pdf-merge.html": ("PDF Merge", [
        "Combine multiple PDFs into a single document in any order you set",
        "Drag to reorder pages before merging, so the final file reads correctly",
        "Keep the original formatting, fonts, and images of every source file",
        "Batch merge dozens of files at once without quality loss",
    ], "Ideal for assembling contracts, reports, and ebooks into one deliverable."),
    "/pdf/pdf-split.html": ("PDF Split", [
        "Split a PDF into separate files by page range or every N pages",
        "Extract a single chapter or page without keeping the rest",
        "Keep selected pages and drop the ones you don't need",
        "Process long documents into manageable parts for sharing",
    ], "Handy when you only need to send one section of a large report."),
    "/pdf/image-to-pdf.html": ("Image to PDF", [
        "Turn JPG, PNG, and other images into a clean PDF",
        "Arrange multiple photos into one document in your chosen order",
        "Set page size to fit screens or print layouts",
        "Build photo albums, scanned archives, and report inserts",
    ], "Great for turning phone photos of documents into a shareable PDF."),
    "/pdf/pdf-to-image.html": ("PDF to Image", [
        "Convert every PDF page into JPG or PNG images",
        "Batch export all pages at once for fast sharing",
        "Keep text sharp enough to read and embed",
        "Drop images straight into slides, social posts, or web pages",
    ], "Useful when you need a page as an image for a presentation or post."),
    "/pdf/pdf-compress.html": ("PDF Compress", [
        "Shrink PDF size while keeping text and images clear",
        "Cut down storage and make email or cloud uploads faster",
        "Batch compress many files in one go",
        "Choose a balance between size and visual quality",
    ], "Perfect before attaching a big PDF to an email or uploading it."),
    "/pdf/pdf-to-word.html": ("PDF to Word", [
        "Convert PDF into an editable Word document",
        "Preserve the original layout, tables, and images",
        "Edit text and rewrite sections after conversion",
        "Avoid retyping a whole document from scratch",
    ], "Saves hours when you must update a finalized PDF."),
    "/pdf/word-to-pdf.html": ("Word to PDF", [
        "Export a Word file to a fixed-layout PDF",
        "Lock the formatting so it looks the same on any device",
        "Keep tables, images, and styling intact",
        "Produce a file that is easy to share and print",
    ], "Best when sending a document that must not be edited."),
    "/pdf/pdf-to-ppt.html": ("PDF to PPT", [
        "Turn PDF pages into editable PowerPoint slides",
        "Keep the visual structure for quick rework",
        "Recover content from a static PDF into a deck",
        "Reuse existing material in a new presentation",
    ], "Helpful when a report needs to become a slide deck."),
    "/pdf/ppt-to-pdf.html": ("PPT to PDF", [
        "Convert PowerPoint slides into a portable PDF",
        "Freeze animations into clean static pages",
        "Keep layout consistent across devices",
        "Share a deck that opens anywhere without PowerPoint",
    ], "Useful for distributing a read-only version of a talk."),
    "/pdf/pdf-to-excel.html": ("PDF to Excel", [
        "Extract tables from a PDF into Excel",
        "Turn scanned or native tables into editable rows",
        "Keep numbers and structure for further analysis",
        "Skip manual data entry from reports",
    ], "Saves time when figures are trapped inside a PDF."),
    "/pdf/excel-to-pdf.html": ("Excel to PDF", [
        "Export spreadsheets to a tidy PDF",
        "Keep grids and charts readable",
        "Fix the layout so it prints cleanly",
        "Share a snapshot that cannot be accidentally edited",
    ], "Good for sending statements or schedules."),
    "/pdf/pdf-encrypt.html": ("PDF Encrypt", [
        "Add a password to protect a PDF",
        "Block opening or editing without the key",
        "Keep confidential files safe on any device",
        "Process locally so the password never travels online",
    ], "Essential before sending sensitive documents."),
    "/pdf/pdf-decrypt.html": ("PDF Decrypt", [
        "Remove a known password from a PDF",
        "Make a locked file editable again",
        "Keep the content intact during unlocking",
        "Works locally for full privacy",
    ], "Useful when you legitimately own a locked file."),
    "/pdf/pdf-ocr.html": ("PDF OCR", [
        "Recognize text inside scanned PDFs",
        "Make images of pages searchable and selectable",
        "Turn paper scans into editable digital text",
        "Keep everything on your device for privacy",
    ], "Brings old scans into a searchable, reusable form."),
    "/pdf/pdf-watermark.html": ("PDF Watermark", [
        "Add text or image watermarks to PDF pages",
        "Mark drafts, ownership, or confidentiality",
        "Place the mark across all pages at once",
        "Adjust position and opacity to taste",
    ], "Protects and labels shared documents."),
    "/pdf/pdf-rotate.html": ("PDF Rotate", [
        "Rotate one or all PDF pages to the correct orientation",
        "Fix sideways scans in a click",
        "Apply the same angle to every page",
        "Keep the rest of the content untouched",
    ], "Quick fix for mis-scanned pages."),
    "/pdf/pdf-page-number.html": ("PDF Page Numbers", [
        "Add page numbers to a PDF",
        "Choose position, format, and starting number",
        "Number the whole document in one pass",
        "Keep the body text clear of the numbers",
    ], "Makes long documents easier to navigate."),
    "/pdf/pdf-sign.html": ("PDF Sign", [
        "Add a signature to a PDF",
        "Place your sign or stamp on any page",
        "Mark a document as approved or signed",
        "Do it locally without uploading the file",
    ], "Finalizes agreements without printing."),
    "/pdf/pdf-unlock.html": ("PDF Unlock", [
        "Remove restrictions from a PDF you own",
        "Allow copying and printing again",
        "Keep the document content intact",
        "Runs in the browser for privacy",
    ], "Restores full use of a locked file."),
    "/pdf/pdf-repair.html": ("PDF Repair", [
        "Attempt to fix a corrupted or unopenable PDF",
        "Recover readable content from a broken file",
        "Rebuild the structure so it opens again",
        "Handle the file locally, no upload needed",
    ], "Last resort before re-creating a lost document."),
    "/pdf/pdf-to-html.html": ("PDF to HTML", [
        "Convert a PDF into an HTML web page",
        "Keep text and layout for the browser",
        "Publish PDF content online without a viewer",
        "Make the text selectable and indexable",
    ], "Turns a static file into a web-ready page."),
    "/pdf/html-to-pdf.html": ("HTML to PDF", [
        "Save a web page as a PDF",
        "Keep the layout close to the original",
        "Capture articles or receipts for archive",
        "Produce a portable, printable copy",
    ], "Archives a page exactly as shown."),
    "/pdf/pdf-to-txt.html": ("PDF to TXT", [
        "Extract plain text from a PDF",
        "Strip layout to get just the words",
        "Feed text into other tools or notes",
        "Keep the extraction on your device",
    ], "Grab the content when only the text matters."),
    "/pdf/pdf-to-jpg.html": ("PDF to JPG", [
        "Save each PDF page as a JPG image",
        "Pick quality and page range",
        "Use the images in designs or posts",
        "Batch export without losing sharpness",
    ], "A focused variant of PDF-to-image for JPG only."),
    "/pdf/pdf-to-png.html": ("PDF to PNG", [
        "Save each PDF page as a PNG image",
        "Keep lossless quality for screens",
        "Choose the pages you need",
        "Export in a batch with one click",
    ], "Best when you need lossless page images."),
    "/pdf/merge-pdf.html": ("Merge PDF", [
        "Another fast way to combine PDFs into one",
        "Reorder files before the final merge",
        "Keep every source page intact",
        "Handle the job fully in the browser",
    ], "A streamlined entry point for combining files."),
    "/pdf/split-pdf.html": ("Split PDF", [
        "A quick path to split a PDF by range",
        "Pull out the pages you actually need",
        "Drop the rest in the same step",
        "All processing stays local",
    ], "A focused tool for extracting pages."),
    "/pdf/compress-pdf.html": ("Compress PDF", [
        "Shrink a PDF for easier sharing",
        "Balance size against readable quality",
        "Batch compress several files",
        "Run locally for privacy",
    ], "A dedicated compress entry for everyday use."),
    "/pdf/protect-pdf.html": ("Protect PDF", [
        "Add a password and restrictions to a PDF",
        "Stop unwanted opening or editing",
        "Keep the file on your device during the step",
        "Designed for confidential documents",
    ], "Focused on locking down a file."),
    "/pdf/unlock-pdf.html": ("Unlock PDF", [
        "Open a PDF you own by removing its lock",
        "Restore copy and print permissions",
        "Keep content unchanged",
        "Private, browser-based processing",
    ], "Focused on freeing a locked file."),
    "/pdf/rotate-pdf.html": ("Rotate PDF", [
        "Rotate selected or all pages",
        "Fix scans that landed sideways",
        "Apply one angle across the file",
        "Local and private",
    ], "A dedicated rotation entry."),
    "/pdf/watermark-pdf.html": ("Watermark PDF", [
        "Stamp text or images across pages",
        "Mark drafts or ownership",
        "Adjust placement and opacity",
        "Process every page at once",
    ], "A focused watermarking tool."),
    "/pdf/page-number-pdf.html": ("Page Number PDF", [
        "Number a PDF in one pass",
        "Set position, style, and start number",
        "Keep body text clear",
        "Local processing",
    ], "A dedicated page-numbering entry."),
    "/pdf/sign-pdf.html": ("Sign PDF", [
        "Place a signature on any page",
        "Approve documents without printing",
        "Keep the file local",
        "Quick and private",
    ], "A focused signing tool."),
    "/pdf/ocr-pdf.html": ("OCR PDF", [
        "Make scanned PDFs searchable",
        "Turn images of text into real text",
        "Keep the scan on your device",
        "Recover old documents",
    ], "A dedicated OCR entry."),
    "/pdf/repair-pdf.html": ("Repair PDF", [
        "Try to fix a broken PDF",
        "Recover content you can still read",
        "Rebuild a file that won't open",
        "Local and private",
    ], "A focused repair entry."),
    "/pdf/convert-pdf.html": ("Convert PDF", [
        "Convert a PDF to Word, images, or other formats",
        "Pick the target format you need",
        "Keep layout where possible",
        "One-stop conversion in the browser",
    ], "A general conversion hub for PDFs."),
    "/pdf/edit-pdf.html": ("Edit PDF", [
        "Make light edits to a PDF",
        "Adjust text and small layout issues",
        "Avoid installing a heavy editor",
        "Keep the file local",
    ], "For quick fixes without desktop software."),
    "/pdf/annotate-pdf.html": ("Annotate PDF", [
        "Add notes and highlights to a PDF",
        "Mark up a document for review",
        "Keep comments with the file",
        "Private, local processing",
    ], "Good for feedback and review rounds."),
    "/pdf/fill-pdf.html": ("Fill PDF", [
        "Fill in PDF forms in the browser",
        "Type into fields without printing",
        "Save the completed form locally",
        "No upload of your answers",
    ], "Fills forms without paper."),
    "/pdf/redact-pdf.html": ("Redact PDF", [
        "Black out sensitive parts of a PDF",
        "Remove private details before sharing",
        "Permanently hide the covered text",
        "Local processing for safety",
    ], "Cleans a file before it leaves your hands."),
    "/pdf/extract-pdf.html": ("Extract PDF", [
        "Pull pages or images out of a PDF",
        "Grab just what you need",
        "Keep the extracted part intact",
        "All local",
    ], "A focused extraction tool."),
    "/pdf/compare-pdf.html": ("Compare PDF", [
        "Spot differences between two PDF versions",
        "Highlight what changed between drafts",
        "Review contracts and revisions fast",
        "Files stay on your device",
    ], "Useful for version control of documents."),
    "/pdf/flatten-pdf.html": ("Flatten PDF", [
        "Flatten forms and annotations into a fixed page",
        "Stop further edits to a finalized file",
        "Keep the visual result intact",
        "Local and private",
    ], "Locks a document after signing."),
}

SECTION_KEYS = ["h_tool_intro", "h_who_is_thi", "h_main_featu", "h_how_to_use"]


def load_tools():
    with open(os.path.join(BASE, "data", "tools-data.json"), encoding="utf-8") as f:
        return json.load(f)


def resolve_path(url):
    return url.lstrip("/")


def gen_intro(name_en, scenario):
    return (f"{name_en} is a free online tool that {scenario.lower()[0] if False else ''}"
            f"{scenario} "
            f"Everything runs locally in your browser, so your files never leave your device.")


def gen_introduction(name_en, bullets, scenario, module):
    feat_line = "; ".join(bullets[:2]).lower().rstrip(".")
    return (f"{name_en} gives you a fast, private way to handle PDFs without installing anything. "
            f"{scenario} "
            f"It keeps your original layout and quality, works on Windows, macOS, and mobile browsers, "
            f"and never uploads your files to a server. {feat_line.capitalize()}.")


def gen_audience(module):
    return " ".join(module["audiences"][:4]) + " In short, anyone who works with documents regularly will find it useful."


def gen_howto(name_en):
    return [
        f"Open {name_en} in your browser — no install, no sign-up.",
        "Add your PDF using the upload area on the page.",
        "Adjust the options if needed, then start with one click.",
        "Preview the result and download it straight to your device.",
    ]


def gen_faq_html(module):
    return "\n".join(
        f'<details open><summary>{htmlmod.escape(q)}</summary><p>{htmlmod.escape(a)}</p></details>'
        for q, a in module["faqs"][:4])


def gen_faq_jsonld(module):
    return [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in module["faqs"][:4]]


def expand_page(path, tool):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None, "FILE_MISSING"
    with open(full, encoding="utf-8", newline="") as f:
        doc = f.read()

    notes = PDF_TOOL_NOTES.get(tool.get("url"))
    if not notes:
        return None, "NO_NOTES"
    name_en, bullets, scenario = notes

    intro = gen_intro(name_en, scenario)
    intro = f"{name_en} is a free online tool. {scenario} Everything runs locally in your browser, so your files never leave your device."
    introduction = gen_introduction(name_en, bullets, scenario, CATEGORY_MODULE)
    audience = gen_audience(CATEGORY_MODULE)
    ul = "<ul>\n" + "\n".join(f"<li>{htmlmod.escape(b)}</li>" for b in bullets) + "\n</ul>"
    steps = gen_howto(name_en)
    ol = "<ol>\n" + "\n".join(f"<li>{htmlmod.escape(s)}</li>" for s in steps) + "\n</ol>"
    faq_html = gen_faq_html(CATEGORY_MODULE)
    faq_jsonld = gen_faq_jsonld(CATEGORY_MODULE)

    new_doc = doc
    new_doc = re.sub(r"(<h1[^>]*>.*?</h1>\s*)<p>.*?</p>",
                     lambda m: m.group(1) + f"<p>{htmlmod.escape(intro)}</p>",
                     new_doc, count=1, flags=re.S)
    for key in SECTION_KEYS:
        repl = ul if key == "h_main_featu" else (ol if key == "h_how_to_use" else None)
        if repl is None:
            txt = introduction if key == "h_tool_intro" else audience
            new_doc = re.sub(
                rf'(<h2[^>]*data-i18n="{re.escape(key)}"[^>]*>.*?</h2>\s*)<p>.*?</p>',
                lambda m, t=txt: m.group(1) + f"<p>{htmlmod.escape(t)}</p>",
                new_doc, count=1, flags=re.S)
        else:
            new_doc = re.sub(
                rf'(<h2[^>]*data-i18n="{re.escape(key)}"[^>]*>.*?</h2>\s*)<p>.*?</p>',
                lambda m, r=repl: m.group(1) + r,
                new_doc, count=1, flags=re.S)
    new_doc = re.sub(
        r'(<h2[^>]*data-i18n="h_faq"[^>]*>.*?</h2>\s*)<div class="faq">.*?</div>',
        lambda m: m.group(1) + f'<div class="faq">{faq_html}</div>',
        new_doc, count=1, flags=re.S)
    new_doc = re.sub(
        r'<script type="application/ld\+json">(.*?"@type":\s*"FAQPage".*?)</script>',
        lambda m: '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_jsonld}, ensure_ascii=False) + '</script>',
        new_doc, count=1, flags=re.S)

    if new_doc == doc:
        return None, "NO_CHANGE"
    return new_doc, "OK"


def main():
    dry = "--dry-run" in sys.argv
    limit = None
    for a in sys.argv[1:]:
        if a.startswith("--limit="):
            limit = int(a.split("=")[1])
    data = load_tools()
    tools = [t for t in data.get("tools", []) if t.get("category") == PILOT_CATEGORY
             and t.get("url") in PDF_TOOL_NOTES]
    if limit:
        tools = tools[:limit]
    done = skip = 0
    for t in tools:
        path = resolve_path(t.get("url", ""))
        new_doc, status = expand_page(path, t)
        if status != "OK":
            print(f"[{status}] {path} ({t.get('name')})")
            skip += 1
            continue
        if dry:
            m = re.search(r"<main>(.*?)</main>", new_doc, re.S)
            txt = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            txt = re.sub(r"\s+", " ", txt).strip()
            wc = len(txt.split())
            print(f"\n===== {path} | words={wc} =====\n{txt[:1100]}\n")
            done += 1
            continue
        with open(os.path.join(BASE, path), "w", encoding="utf-8", newline="") as f:
            f.write(new_doc)
        done += 1
    print(f"\n[SUMMARY] pilot={PILOT_CATEGORY} processed={done} skipped={skip} dry={dry}")


if __name__ == "__main__":
    main()
