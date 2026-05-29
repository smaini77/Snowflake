# ==============================================================================
# Deploy All Cortex Agents
# Usage: .\scripts\deploy_all.ps1 [-Environment prod|dev] [-DryRun]
# ==============================================================================

param(
    [ValidateSet("prod", "dev")]
    [string]$Environment = "prod",

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $PSScriptRoot
$Agents = @(
    "pinnacle-financial-analyst",
    "cascade-financial-analyst",
    "sql-skills-coach"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Cortex Agents - Deployment Script" -ForegroundColor Cyan
Write-Host " Environment: $Environment" -ForegroundColor Cyan
Write-Host " Dry Run: $DryRun" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$SuccessCount = 0
$FailCount = 0

foreach ($agent in $Agents) {
    $deployScript = Join-Path $RootDir "agents\$agent\deploy\deploy.ps1"

    if (-Not (Test-Path $deployScript)) {
        Write-Host "[SKIP] $agent - deploy script not found" -ForegroundColor Yellow
        continue
    }

    Write-Host "[DEPLOYING] $agent..." -ForegroundColor Green

    try {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would execute: $deployScript" -ForegroundColor DarkGray
        } else {
            & $deployScript -Environment $Environment
        }
        $SuccessCount++
        Write-Host "  [SUCCESS] $agent deployed" -ForegroundColor Green
    } catch {
        $FailCount++
        Write-Host "  [FAILED] $agent - $($_.Exception.Message)" -ForegroundColor Red
    }

    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Results: $SuccessCount succeeded, $FailCount failed" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if ($FailCount -gt 0) {
    exit 1
}
