import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

def minify_css(text):
    text = re.sub(r'/\*[\s\S]*?\*/', '', text)  # remove comments
    text = re.sub(r'\s+', ' ', text)              # collapse whitespace
    text = re.sub(r'\s*([{};,:])\s*', r'\1', text) # remove space around operators
    text = re.sub(r';}', '}', text)                # remove last semicolon
    return text.strip()

def _skip_string(text, i):
    """Skip past a string literal (single/double/template). Returns new index, None if unterminated."""
    quote = text[i]
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            i += 2  # skip escaped char
        elif ch == quote:
            return i + 1  # past closing quote
        elif quote == '`' and ch == '$' and i+1 < len(text) and text[i+1] == '{':
            return i  # template interpolation — caller must handle '}'
        elif ch == '\n' and quote != '`':
            return None  # unterminated single/double string
        else:
            i += 1
    return None

def minify_js(text):
    """Minify JS: remove comments safely without breaking regex literals or strings."""
    # Step 1: Safely remove comments using a state machine.
    # We track: in_single_quote, in_double_quote, in_backtick, in_regex, in_line_comment, in_block_comment
    out = []
    i = 0
    n = len(text)

    # Heuristic: a '/' starts a regex if the previous non-whitespace char is one of:
    REGEX_PREV = set('=(,![:;&|^?{}')

    while i < n:
        c = text[i]
        rest = text[i+1:] if i+1 < n else ''

        # ----- Handle strings (single, double, backtick) -----
        if c in '"\'':
            start = i
            i += 1
            while i < n:
                if text[i] == '\\':
                    i += 2
                elif text[i] == c:
                    i += 1
                    break
                elif text[i] == '\n':  # unterminated
                    break
                else:
                    i += 1
            out.append(text[start:i])
            continue

        if c == '`':
            start = i
            i += 1
            depth = 0
            while i < n:
                if text[i] == '\\':
                    i += 2
                elif text[i] == '`' and depth == 0:
                    i += 1
                    break
                elif text[i] == '$' and i+1 < n and text[i+1] == '{':
                    depth += 1
                    i += 2
                elif text[i] == '}':
                    if depth > 0:
                        depth -= 1
                    i += 1
                else:
                    i += 1
            out.append(text[start:i])
            continue

        # ----- Handle line comment // -----
        if c == '/' and rest and rest[0] == '/':
            # Skip to end of line
            while i < n and text[i] != '\n':
                i += 1
            # Don't append anything (comment removed)
            continue

        # ----- Handle block comment /* */ -----
        if c == '/' and rest and rest[0] == '*':
            i += 2
            while i < n:
                if text[i] == '*' and i+1 < n and text[i+1] == '/':
                    i += 2
                    break
                i += 1
            # Don't append anything (comment removed)
            continue

        # ----- Handle regex literal /pattern/flags -----
        if c == '/' and (i == 0 or text[i-1] in REGEX_PREV or (text[i-1] in ' \t' and any(
            p in ''.join(out[-6:]) for p in REGEX_PREV))):
            # Be more precise: look backwards past whitespace for the previous token
            j = len(out) - 1
            while j >= 0 and out[j] in ' \t\n\r':
                j -= 1
            prev = out[j] if j >= 0 else ''
            if prev == '' or prev in REGEX_PREV or prev in '({[':
                # This is likely a regex
                start = i
                i += 1
                while i < n:
                    if text[i] == '\\':
                        i += 2
                    elif text[i] == '/':
                        i += 1
                        # Collect flags (optional)
                        while i < n and text[i].isalpha():
                            i += 1
                        break
                    else:
                        i += 1
                out.append(text[start:i])
                continue

        # ----- Everything else: just emit -----
        out.append(c)
        i += 1

    text = ''.join(out)

    # Step 2: Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*([{}();,:=+\-*/!<>])\s*', r'\1', text)
    return text.strip()


# Minify CSS files
css_files = ['assets/css/style.css', 'assets/css/tool-ui.css']
for path in css_files:
    with open(path, encoding='utf-8') as f:
        orig = f.read()
    minified = minify_css(orig)
    base, ext = os.path.splitext(path)
    min_path = base + '.min' + ext
    with open(min_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    savings = (1 - len(minified) / len(orig)) * 100
    print(f"{path}: {len(orig):,} -> {len(minified):,} chars ({savings:.0f}% savings)")
    print(f"  -> {min_path}")

# Minify JS files
js_files = ['assets/js/tool-ui.js', 'assets/js/anti-crash.js', 'assets/js/common-i18n.js']
for path in js_files:
    if not os.path.exists(path):
        print(f"SKIP: {path} not found")
        continue
    with open(path, encoding='utf-8') as f:
        orig = f.read()
    minified = minify_js(orig)
    base, ext = os.path.splitext(path)
    min_path = base + '.min' + ext
    with open(min_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    savings = (1 - len(minified) / len(orig)) * 100
    print(f"{path}: {len(orig):,} -> {len(minified):,} chars ({savings:.0f}% savings)")
    print(f"  -> {min_path}")

print("\nDone!")
