# ==============================================================================
# Deploy SQL Skills Coach Agent
# Usage: .\deploy.ps1 [-Environment prod|dev]
# ==============================================================================

param(
    [ValidateSet("prod", "dev")]
    [string]$Environment = "prod"
)

$ErrorActionPreference = "Stop"
$AgentDir = Split-Path -Parent $PSScriptRoot
$DeploySQL = Join-Path $PSScriptRoot "create_agent.sql"

# Load environment variables from .env if present
$EnvFile = Join-Path $AgentDir ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            [System.Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), "Process")
        }
    }
}

Write-Host "Deploying SQL Skills Coach..." -ForegroundColor Green
Write-Host "  SQL File: $DeploySQL" -ForegroundColor DarkGray
Write-Host "  Environment: $Environment" -ForegroundColor DarkGray

# Execute via Snowflake CLI
try {
    snow sql -f $DeploySQL --connection $env:SNOWFLAKE_CONNECTION
    Write-Host "  Agent deployed successfully!" -ForegroundColor Green
} catch {
    Write-Host "  Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
