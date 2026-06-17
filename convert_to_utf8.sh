#!/usr/bin/env bash
# ------------------------------------------------------------
# Batch UTF‑8 conversion script
# ------------------------------------------------------------
# This script scans the entire project for text files that are
# NOT encoded in UTF‑8, creates a .bak backup of each original
# file, and rewrites the file in UTF‑8 (without BOM).
#
# Requirements:
#   - Git Bash / Cygwin / WSL (any Bash environment)
#   - `iconv` utility (usually available in the above shells)
#
# Usage:
#   1. Open Git Bash in the project root.
#   2. Make the script executable: chmod +x convert_to_utf8.sh
#   3. Run it: ./convert_to_utf8.sh
#
# After conversion, verify the changes (git diff) and remove
# the .bak files if everything looks correct.
# ------------------------------------------------------------

# File extensions to check (add more if needed)
EXTENSIONS="html htm js css txt md json xml yml yaml"

# Function to detect encoding and convert if needed
convert_file() {
  local file="$1"
  # Detect current encoding (ignore case)
  local enc=$(file -b --mime-encoding "$file" | tr '[:upper:]' '[:lower:]')
  if [[ "$enc" != "utf-8" && "$enc" != "us-ascii" ]]; then
    echo "Converting: $file (detected: $enc → utf-8)"
    # Backup original
    cp "$file" "$file.bak"
    # Convert to UTF-8 (strip BOM if present)
    iconv -f "$enc" -t utf-8 "$file.bak" > "$file"
  fi
}

# Iterate over all files with the given extensions
for ext in $EXTENSIONS; do
  find . -type f -name "*.$ext" -print0 | while IFS= read -r -d '' f; do
    convert_file "$f"
  done
done

echo "All files processed. Review changes with 'git diff' and delete *.bak if satisfied."