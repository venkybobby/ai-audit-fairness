# Use Git when it's installed but not in PATH (e.g. C:\Program Files\Git\bin)
$gitExe = "C:\Program Files\Git\bin\git.exe"
if (-not (Test-Path $gitExe)) {
    Write-Host "Git not found at $gitExe. Install from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

& $gitExe init
& $gitExe add .
& $gitExe status
& $gitExe commit -m "Initial commit: AI fairness audit with Fairlearn"

Write-Host ""
Write-Host "Next: Create a new repo at https://github.com/new (name: ai-audit-fairness), then run:" -ForegroundColor Cyan
Write-Host '  & $gitExe = "C:\Program Files\Git\bin\git.exe"; & $gitExe remote add origin https://github.com/YOUR_USERNAME/ai-audit-fairness.git; & $gitExe branch -M main; & $gitExe push -u origin main' -ForegroundColor Yellow
Write-Host "(Replace YOUR_USERNAME with your GitHub username)" -ForegroundColor Gray
