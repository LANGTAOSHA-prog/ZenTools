# -*- coding: utf-8 -*-
"""
P1 内容扩写生成器（模板 C：hero 成熟模板，中文正文）—— 已修复版
==============================================================
针对模板 C（173 页主力：PDF/AI/生活等）。这些页已有真实中文短描述+信息卡+步骤，
但缺独立的「长文介绍 + 可见 FAQ」，且部分页的 HowTo JSON-LD 是非法 JSON。

修复要点（相对初版）：
- B1 保留页面已有 FAQ JSON-LD：若有则渲染成可见 <details>（只补「有结构数据无可见 FAQ」
  的不一致，绝不覆盖好数据）；若无才从库生成并补 JSON-LD。
- B2 FAQ 选库按 name 优先（而非 description），修正 PDF解密→加密、扁平化→注释、
  PDF页码删除→合并 等错配；并加「转→转换」「解锁→解密」别名。
- B3 插入块与 JSON-LD 重序列化均用 CRLF（\r\n），与仓库约定一致。
- B4 FAQ 话术聚焦操作长尾（文件大小/批量/格式/移动端），去掉与页面隐私卡重复的套话。
- B5 每个 FAQ 库补到 ≥4 条。
- B6 顺手修复页内非法 JSON-LD（HowTo 步骤里 ASCII 双引号当中文引号），无法修复则删除该
  损坏 script（清 Search Console 错误），不波及 WebApplication/FAQPage。

用法：
  python _p1_expand_c.py --dry-run --limit=2
  python _p1_expand_c.py             # 处理试点分类全部模板 C 页
"""
import json, os, re, sys, html as htmlmod

BASE = os.path.dirname(os.path.abspath(__file__))
PILOT_CATEGORY = "PDF工具"
INSERT_MARK = "<!-- P1-EXPAND SEO CONTENT -->"
CRLF = "\r\n"

# 分类知识库（中文，真实有用，不与页面已有信息卡重复：聚焦操作长尾）
CATEGORY_MODULE = {
    "audiences": [
        "日常需要处理合同、报告、发票的办公与行政人员",
        "整理论文、课件与扫描资料的学生和教师",
        "涉及敏感文档合并、拆分与加密的法务和财务同事",
        "把资料转成图片或 PDF 做分享的自媒体与电商运营",
    ],
    "tips": [
        "批量操作前先规范文件命名，结果更容易区分",
        "处理超大文件时分批进行，避免浏览器长时间占用",
        "导出后核对一次页码顺序与书签，确保交付无误",
        "多步任务可串接使用，例如先压缩再合并、先拆分再分别处理",
    ],
}

# 按工具功能匹配的「专属 FAQ」（每页不同，聚焦长尾实操；去隐私套话）
FAQ_BANK = {
    "合并": [
        ("PDF 合并后还能搜索里面的文字吗？", "可以。合并只是按顺序拼接，原有文字内容保留，合并后的文件依然可以全文搜索与复制。"),
        ("合并时怎么调整页面顺序？", "在工具里拖拽文件即可调整先后，确认无误后再开始，最终文件会严格按你排列的顺序生成。"),
        ("一次能合并多少个 PDF？", "数量上没有硬性上限，但并行处理的文件数取决于浏览器与设备性能，文件很多时建议分批合并。"),
        ("合并后的文件体积会变大吗？", "会随页数累加。若体积过大，可先压缩再合并，整体处理会更顺畅。"),
    ],
    "拆分": [
        ("PDF 拆分后会丢失书签吗？", "按页拆出的单页文件不含原文档的书签结构；需要保留大纲时，建议先在原文件中整理好再拆分。"),
        ("可以只提取其中几页吗？", "可以。按页码范围提取即可，未选中的页面不会被导出，方便只发送需要的章节。"),
        ("拆分大文件会很慢吗？", "拆分在浏览器本地完成，速度主要取决于文件体积与设备性能，遇到超大文件可分多次处理。"),
        ("拆分后能分别保存成独立文件吗？", "可以。每一页或每一个范围都会生成独立文件，方便单独发送或归档。"),
    ],
    "压缩": [
        ("压缩后清晰度会明显下降吗？", "工具会在体积和清晰度之间取平衡，普通文档文字依然清晰可读；对画质要求高可适当调低压缩强度。"),
        ("压缩后还能打印吗？", "可以。压缩只减小文件体积，内容排版不变，打印效果与原始文件一致。"),
        ("单个文件最大能压缩多大？", "没有固定上限，但特别大的文件处理时间会更长，必要时可先拆分再分别压缩。"),
        ("压缩对扫描件有效吗？", "扫描件本身是图片，压缩主要减小图片体积；若清晰度不足，建议重新扫描更高分辨率。"),
    ],
    "转换": [
        ("转换后原来的排版会乱吗？", "工具会尽量保留原始排版、字体与图片；极少数复杂版式建议导出后快速核对一遍。"),
        ("转换出来的文件能在手机上打开吗？", "可以。生成的文件为标准格式，手机上的常见阅读器都能正常打开。"),
        ("转换需要联网吗？", "不需要联网，转换在你的浏览器本地完成，无需把文件传到任何服务器。"),
        ("转换对文件大小有限制吗？", "没有固定限制，但文件越大处理越久；遇到超大文件可先拆分再转换。"),
    ],
    "加密": [
        ("忘记密码还能打开吗？", "密码由你自己设定，工具不保存也不传输密码，请务必牢记；遗失后无法由我们找回。"),
        ("加密后还能搜索内容吗？", "加密主要用于限制打开与编辑，能否搜索取决于你设置的权限范围；如只需防篡改，可选择仅限制编辑。"),
        ("可以设置不同权限吗？", "可以。常见权限包括禁止打印、禁止复制、禁止编辑，按需要勾选即可。"),
        ("加密后文件还能正常打开吗？", "能。知道密码的设备与阅读器都可正常打开，只是未授权操作会受限制。"),
    ],
    "解密": [
        ("解密需要原来的密码吗？", "是的。合法解密需要你已知的正确密码，工具不会尝试绕过任何保护，仅用于你拥有权限的文件。"),
        ("解密后文件还会保留内容吗？", "会。解密只是移除打开限制，文档内容原样保留，不会丢失任何页面。"),
        ("解密后还能重新加密吗？", "可以。解密后随时可再次设置密码，切换不同的权限组合。"),
        ("解密对文件大小有限制吗？", "没有硬性限制，但文件越大处理越久，超大文件建议分批处理。"),
    ],
    "识别": [
        ("OCR 后图片里的文字能复制吗？", "可以。识别后文本会变成可选中的真实文字，方便搜索、复制与二次编辑。"),
        ("扫描版 PDF 识别准确率高吗？", "对清晰的正向扫描识别率很高；若原图倾斜、模糊或有水印，建议先裁剪校正再识别。"),
        ("识别支持哪些语言？", "取决于具体引擎，常见中英文均可；多语言混排建议在设置中勾选对应语种。"),
        ("识别后排版会保留吗？", "文字层会叠加在原图上，版面大致保留，复杂表格建议识别后人工核对。"),
    ],
    "水印": [
        ("水印能被去掉吗？", "作为所有者你可以随时重新生成不带水印的版本；对外分发的水印用于标识归属，普通阅读器不会自动去除。"),
        ("可以只在部分页面加水印吗？", "可以。设置覆盖范围即可，灵活控制哪些页需要标注。"),
        ("水印支持图片吗？", "支持。可上传 PNG 等透明背景图片作为 logo 水印，并调整大小与透明度。"),
        ("水印位置能自定义吗？", "能。常见的四角、居中、平铺等位置均可选择。"),
    ],
    "旋转": [
        ("旋转后清晰度会变化吗？", "不会。旋转只改变页面方向，不改变分辨率，导出后依然清晰。"),
        ("能只旋转其中几页吗？", "可以。选择需要调整的页面范围即可，其余页面保持不变。"),
        ("旋转支持 90/180 度吗？", "支持。可按 90 度步进或 180 度翻转，按预览效果选择。"),
        ("旋转后能批量处理吗？", "可以。对多页文件指定统一角度即可一次性旋转。"),
    ],
    "页码": [
        ("页码能从指定数字开始吗？", "可以。设置起始页码即可，适合接在已有文档之后继续编号。"),
        ("页码会盖住正文吗？", "不会。页码放在页边距区域，默认不会遮挡正文内容。"),
        ("页码支持罗马数字吗？", "支持。可在阿拉伯数字与罗马数字等格式之间选择，匹配不同文档规范。"),
        ("能只给部分页加页码吗？", "能。设置页码范围即可，封面或目录等可不编号。"),
    ],
    "签名": [
        ("电子签名具有法律效力吗？", "在符合当地电子签名法规的场景下可作为签署凭证；具体效力请以你所在地区的规定为准。"),
        ("签名后会改动原文吗？", "签名作为附加层附着在文档上，原有正文内容保持不变。"),
        ("可以上传手写签名图片吗？", "可以。上传 PNG 等图片作为签名外观，并定位到指定位置。"),
        ("签名后能验证完整性吗？", "通过数字签名可检测文档事后是否被篡改，适合正式文件流转。"),
    ],
    "修复": [
        ("修复一定会成功吗？", "不一定。修复能尝试重建结构并恢复可读内容，但严重损坏的文件可能无法完全复原，建议同时保留备份。"),
        ("修复过程安全吗？", "安全。修复在你的浏览器本地完成，文件不会上传。"),
        ("修复后排版会还原吗？", "尽量还原文字与图片，复杂版式可能仍需手动微调。"),
        ("修复对文件大小有限制吗？", "没有硬性限制，但文件越大处理越久。"),
    ],
    "注释": [
        ("批注会被保存进 PDF 吗？", "会。批注作为文档内容的一部分保存，对方打开即可看到你的评论与高亮。"),
        ("可以导出不含批注的干净版本吗？", "可以。需要时生成一份不带批注的副本即可。"),
        ("支持哪些批注类型？", "常见高亮、下划线、文本框、图形标注均支持，按场景选择。"),
        ("批注能修改或删除吗？", "能。已有批注可随时编辑内容或移除，不影响原正文。"),
    ],
    "填写": [
        ("填写的内容会泄露吗？", "不会。填写与保存都在本地浏览器完成，答案不会上传到服务器。"),
        ("填好的表单能打印吗？", "可以。填写完成后直接打印或另存为 PDF 即可。"),
        ("支持下拉与勾选项吗？", "支持。交互式表单的输入框、下拉、复选框均可正常填写。"),
        ("填写后能清空重填吗？", "能。一键重置表单即可重新填写，不影响原文件结构。"),
    ],
    "红抹": [
        ("被遮盖的内容还能恢复吗？", "遮盖后原内容被永久隐藏，无法从生成文件中恢复，适合在分享前去除敏感信息。"),
        ("遮盖会影响排版吗？", "不会。遮盖只覆盖指定区域，其余内容原样保留。"),
        ("支持矩形与自定义区域吗？", "支持。拖拽框选即可定义遮盖范围，可多次添加。"),
        ("遮盖后能导出吗？", "能。遮盖作为内容固化进文件，导出后他人无法移除。"),
    ],
    "对比": [
        ("对比能标出具体改了哪几行吗？", "可以。工具会高亮两个版本之间的差异，方便你快速定位改动位置。"),
        ("对比大文件会慢吗？", "对比在本地进行，文件越大耗时越长，建议在性能足够的设备上操作。"),
        ("支持图片版对比吗？", "部分工具支持；纯文本对比更准确，扫描件建议先 OCR 再对比。"),
        ("对比结果能导出吗？", "能。差异报告可导出，便于归档或交付审阅。"),
    ],
    "扁平": [
        ("扁平化后还能再编辑吗？", "扁平化会把表单与批注固定为页面内容，之后通常不可再编辑，适合定稿分发。"),
        ("扁平化会损失清晰度吗？", "不会。扁平化不改变分辨率，仅锁定可编辑元素。"),
        ("扁平化会移除批注吗？", "批注会被合并固化到页面，视觉保留但不再可单独编辑。"),
        ("何时适合扁平化？", "正式定稿、需要防止他人修改表单内容时最合适。"),
    ],
    "提取": [
        ("提取图片会损失画质吗？", "会尽量保持原图质量；若原图本身分辨率低，提取后不会变清晰。"),
        ("能只提取某几页吗？", "可以。指定页码范围即可，未选页面不会被导出。"),
        ("提取的文字能保存吗？", "可导出为 TXT 等文本，方便二次编辑。"),
        ("提取对文件大小有限制吗？", "没有硬性限制，但文件越大处理越久。"),
    ],
    "编辑": [
        ("轻量编辑会改动原排版吗？", "轻量编辑针对局部文字与小块内容，尽量保持整体排版不变。"),
        ("编辑需要上传文件吗？", "不需要。编辑在浏览器本地完成，文件不上传。"),
        ("能修改文字内容吗？", "能。可直接改写页面中的文本块，调整措辞与错字。"),
        ("编辑后还能继续其他操作吗？", "能。编辑结果可继续用于合并、压缩等后续处理。"),
    ],
}

# name/desc 中的别名 -> FAQ 库键
ALIAS = {"解锁": "解密", "批量": "合并"}


def load_tools():
    with open(os.path.join(BASE, "data", "tools-data.json"), encoding="utf-8") as f:
        return json.load(f)


def resolve_path(url):
    return url.lstrip("/")


def pick_faq_key(name, desc):
    """按 name 优先（修正初版按 description 误判），再 desc，再别名/转义，最后兜底 转换。"""
    name = name or ""
    desc = desc or ""
    # name 优先：具体键
    for key in FAQ_BANK:
        if key in name:
            return key
    # name 中的别名
    for a, k in ALIAS.items():
        if a in name:
            return k
    # desc 具体键
    for key in FAQ_BANK:
        if key in desc:
            return key
    for a, k in ALIAS.items():
        if a in desc:
            return k
    # 「转」视为转换（图片转PDF / PDF转Word 等）
    if "转" in (name + desc):
        return "转换"
    return "转换"


def extract_existing_faq(doc):
    """返回页面已有 FAQPage JSON-LD 的 [(q,a)...] 或 None"""
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
    if not m:
        return None
    if '"@type": "FAQPage"' not in m.group(1) and '"@type":"FAQPage"' not in m.group(1):
        return None
    try:
        obj = json.loads(m.group(1))
        ent = obj.get("mainEntity", [])
        pairs = [(e["name"], e["acceptedAnswer"]["text"]) for e in ent
                 if isinstance(e, dict) and "name" in e and "acceptedAnswer" in e]
        return pairs if pairs else None
    except Exception:
        return None


def gen_block(tool, existing_faq, has_visible_details):
    name = tool.get("name") or os.path.splitext(os.path.basename(tool.get("url", "")))[0]
    desc = tool.get("description", "").rstrip("。")
    mod = CATEGORY_MODULE
    scene = (f"{name}用于{desc}。它把繁琐的文档处理变成浏览器里的一步操作，"
             f"无需安装软件、无需注册，打开网页即可使用，所有计算都在本地完成，文件不会离开你的设备。"
             f"无论是日常办公、学习资料整理，还是把材料转成便于分享的格式，都能用它快速搞定。")
    who = "。".join(mod["audiences"][:4]) + "。简单来说，任何经常和文档打交道的人都能用上。"
    tips = mod["tips"][:4]
    tips_ul = "<ul>" + CRLF + CRLF.join(f"<li>{htmlmod.escape(t)}</li>" for t in tips) + CRLF + "</ul>"

    sections = [f'<h2>适用场景</h2>{CRLF}  <p>{htmlmod.escape(scene)}</p>',
                f'<h2>适合谁使用</h2>{CRLF}  <p>{htmlmod.escape(who)}</p>',
                f'<h2>进阶技巧</h2>{CRLF}  {tips_ul}']

    faq_jsonld = None
    if not has_visible_details:
        faqs = existing_faq if existing_faq else FAQ_BANK.get(pick_faq_key(name, desc), FAQ_BANK["转换"])[:4]
        faq_html = CRLF.join(
            f'<details open><summary>{htmlmod.escape(q)}</summary><p>{htmlmod.escape(a)}</p></details>'
            for q, a in faqs)
        sections.append(f'<h2>常见问题</h2>{CRLF}  <div class="faq">{CRLF}    {faq_html}{CRLF}  </div>')
        # 仅当页面原本没有任何 FAQ 时才补 JSON-LD；已有则保留原结构数据、不重复
        if existing_faq is None:
            faq_jsonld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in faqs]

    inner = CRLF + CRLF.join(sections) + CRLF
    block = f"{INSERT_MARK}{CRLF}<section class=\"section\">{inner}</section>"
    return block, faq_jsonld


def repair_jsonld(doc):
    """B6：修复页内非法 JSON-LD。规则：把被 CJK/字母夹住的 ASCII 双引号当作中文引号修正，
    再 json.loads；成功则重序列化（紧凑，保持 CRLF 安全）。无法修复则删除该损坏 script。"""
    def fix_one(raw):
        # 修复 ASCII 双引号被当作中文引号使用的情况（前后均为 CJK/字母数字）
        cjk = lambda ch: ("\u4e00" <= ch <= "\u9fff") or ch.isalnum()
        chars = list(raw)
        flip = False
        for i, ch in enumerate(chars):
            if ch == '"' and i > 0 and i < len(chars) - 1 and cjk(chars[i - 1]) and cjk(chars[i + 1]):
                chars[i] = "\u201c" if not flip else "\u201d"
                flip = not flip
        fixed = "".join(chars)
        try:
            obj = json.loads(fixed)
            return json.dumps(obj, ensure_ascii=False, separators=(",", ": ")), True
        except Exception:
            return None, False

    out = doc
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        raw = m.group(1).strip()
        try:
            json.loads(raw)
            continue  # 已合法，不动
        except Exception:
            new_raw, ok = fix_one(raw)
            if ok:
                repl = '<script type="application/ld+json">' + new_raw + '</script>'
                out = out[:m.start()] + repl + out[m.end():]
                # 重新计算后续偏移（这里直接用替换后的整体重扫更简单）
                return repair_jsonld(out)  # 递归处理剩余 script
            else:
                # 无法修复：删除损坏 script（清 SC 错误，不波及其他 schema）
                out = out[:m.start()] + "<!-- P1: removed invalid JSON-LD -->" + out[m.end():]
                return repair_jsonld(out)
    return out


def expand_page(path, tool):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None, "FILE_MISSING"
    with open(full, encoding="utf-8", newline="") as f:
        doc = f.read()
    if INSERT_MARK in doc:
        return None, "ALREADY_DONE"
    if "hero-gradient-text" not in doc:
        return None, "NOT_TEMPLATE_C"
    if "<footer" not in doc and "</body" not in doc:
        return None, "NO_ANCHOR"
    anchor = "<footer" if "<footer" in doc else "</body"

    doc = repair_jsonld(doc)  # B6：先修页内非法 JSON-LD

    has_visible_details = "<details" in doc
    existing_faq = extract_existing_faq(doc) if not has_visible_details else None
    block, faq_jsonld = gen_block(tool, existing_faq, has_visible_details)

    new_doc = doc.replace(anchor, block + CRLF + anchor, 1)

    if faq_jsonld is not None:  # 仅当本页无可见 FAQ 时才补 JSON-LD（不覆盖已有）
        new_doc = new_doc.replace("</body>",
            '<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                          "mainEntity": faq_jsonld}, ensure_ascii=False, separators=(",", ": "))
            + '</script>' + CRLF + "</body>", 1)

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
    tools = [t for t in data.get("tools", []) if t.get("category") == PILOT_CATEGORY]
    if limit:
        tools = tools[:limit]
    done = skip = 0
    for t in tools:
        path = resolve_path(t.get("url", ""))
        new_doc, status = expand_page(path, t)
        if status != "OK":
            if status not in ("NOT_TEMPLATE_C", "ALREADY_DONE"):
                print(f"[{status}] {path} ({t.get('name')})")
            skip += 1
            continue
        if dry:
            m = re.search(r"P1-EXPAND SEO CONTENT -->(.*?)</section>", new_doc, re.S)
            txt = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            txt = re.sub(r"\s+", " ", txt).strip()
            has_details = "<details" in new_doc
            print(f"\n===== {path} | chars={len(txt)} | visibleFAQ={has_details} =====\n{txt[:900]}\n")
            done += 1
            continue
        with open(os.path.join(BASE, path), "w", encoding="utf-8", newline="") as f:
            f.write(new_doc)
        done += 1
    print(f"\n[SUMMARY] template=C pilot={PILOT_CATEGORY} processed={done} skipped={skip} dry={dry}")


if __name__ == "__main__":
    main()
