param()

$ErrorActionPreference = "Continue"

$targetDir = "D:\Users\taojiang\Documents\GitHub\ZenTools"

if (-not (Test-Path $targetDir)) {
    Write-Host "Directory not found: $targetDir"
    exit 1
}

Set-Location $targetDir

Write-Host "Current directory: $(Get-Location)"
Write-Host "Git status:"
git status --short

Write-Host "Adding files..."
git add -A

Write-Host "Committing..."
git commit -m "feat(pdf): add 8 new PDF tools" -m "- PDF Edit, Repair, Remove Page Numbers, Diff, Annotate, Grayscale, to HTML, Bookmarks" -m "All tools support 4 languages and use PDF.js + PDF-Lib."

Write-Host "Pushing..."
git push

Write-Host "Done!"