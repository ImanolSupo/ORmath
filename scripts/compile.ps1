# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

param(
  [ValidateSet('all', 'pdflatex', 'xelatex', 'lualatex')]
  [string]$Engine = 'pdflatex'
)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
  $enginesToRun = if ($Engine -eq 'all') { @('pdflatex','xelatex','lualatex') } else { @($Engine) }
  $sourcesToCompile = @(Get-ChildItem -LiteralPath examples -Filter '*.tex' | Sort-Object Name)
  $sourcesToCompile += Get-Item -LiteralPath docs/ormath.tex
  foreach ($texEngine in $enginesToRun) {
    if (-not (Get-Command $texEngine -ErrorAction SilentlyContinue)) {
      throw "TeX engine unavailable: $texEngine"
    }
    $outputDirectory = "output/pdf/$texEngine"
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    foreach ($sourceToCompile in $sourcesToCompile) {
      for ($passNumber = 1; $passNumber -le 2; $passNumber++) {
        $compilerOutput = & $texEngine -interaction=nonstopmode -halt-on-error -no-shell-escape `
          "-output-directory=$outputDirectory" $sourceToCompile.FullName 2>&1
        if ($LASTEXITCODE -ne 0) {
          $compilerOutput | Write-Output
          throw "Compilation failed: $texEngine $($sourceToCompile.Name)"
        }
      }
      $logPath = Join-Path $outputDirectory ($sourceToCompile.BaseName + '.log')
      $logText = Get-Content -LiteralPath $logPath -Raw
      $unwantedDiagnostics = '(?m)^!|Undefined control sequence|Overfull|Underfull|LaTeX Warning:|Package .+ Warning:|Font shape .+ undefined|Missing character:'
      if ($logText -match $unwantedDiagnostics) {
        Select-String -LiteralPath $logPath -Pattern $unwantedDiagnostics | Write-Output
        throw "Review compiler diagnostics: $logPath"
      }
      Write-Output "PASS $texEngine $($sourceToCompile.Name)"
    }
  }
} finally {
  Pop-Location
}
