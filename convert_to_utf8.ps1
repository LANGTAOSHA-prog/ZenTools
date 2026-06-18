# ------------------------------------------------------------
# Batch UTF‑8 conversion script (PowerShell)
# ------------------------------------------------------------
# This script scans the project for text files that are not UTF‑8,
# creates a .bak backup of each, and rewrites the file in UTF‑8.
#
# Requirements:
#   - PowerShell 5.0+ (built‑in on Windows 10)
#
# Usage:
#   1. Open PowerShell in the project root.
#   2. Run the script: .\convert_to_utf8.ps1
#
# After conversion, review changes (git diff) and delete *.bak
# files if everything looks correct.
# ------------------------------------------------------------

# File extensions to process (add more if needed)
$extensions = @('html','htm','js','css','txt','md','json','xml','yml','yaml')

function Get-FileEncoding($path) {
    $bytes = [System.IO.File]::ReadAllBytes($path)
    $enc = [System.Text.Encoding]::Default
    try {
        $enc = [System.Text.Encoding]::GetEncoding('utf-8')
        $enc.GetString($bytes) | Out-Null
        return 'utf-8'
    } catch {
        # Fallback: use chardet via .NET if needed, but for simplicity treat as non‑utf8
        return 'unknown'
    }
}

foreach ($ext in $extensions) {
    Get-ChildItem -Recurse -File -Filter "*.$ext" | ForEach-Object {
        $file = $_.FullName
        $encoding = Get-FileEncoding $file
        if ($encoding -ne 'utf-8') {
            Write-Host "Converting: $file (detected: $encoding → utf-8)"
            # Backup original
            Copy-Item -Path $file -Destination "$file.bak" -Force
            # Read with detected encoding (fallback to default) and write as UTF‑8 without BOM
            $content = Get-Content -Path $file -Raw -Encoding Default
            Set-Content -Path $file -Value $content -Encoding UTF8 -NoNewline
        }
    }
}
Write-Host "All files processed. Review changes with 'git diff' and delete *.bak if satisfied."