# ==============================================================================
# Deploy Pinnacle Financial Analyst Agent
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

# Validate required environment variable
if (-not $env:SNOWFLAKE_DATABASE) {
    Write-Host "  [ERROR] SNOWFLAKE_DATABASE is not set. Configure it in .env or environment." -ForegroundColor Red
    exit 1
}

Write-Host "Deploying Pinnacle Financial Analyst..." -ForegroundColor Green
Write-Host "  SQL File: $DeploySQL" -ForegroundColor DarkGray
Write-Host "  Database: $env:SNOWFLAKE_DATABASE" -ForegroundColor DarkGray
Write-Host "  Environment: $Environment" -ForegroundColor DarkGray

# Substitute ${SNOWFLAKE_DATABASE} placeholder in SQL template
$SqlContent = Get-Content $DeploySQL -Raw
$SqlContent = $SqlContent -replace '\$\{SNOWFLAKE_DATABASE\}', $env:SNOWFLAKE_DATABASE
$TempSQL = Join-Path $env:TEMP "deploy_pinnacle_agent.sql"
Set-Content $TempSQL -Value $SqlContent -NoNewline

# Execute via Snowflake CLI
try {
    snow sql -f $TempSQL --connection $env:SNOWFLAKE_CONNECTION
    Write-Host "  Agent deployed successfully!" -ForegroundColor Green
} catch {
    Write-Host "  Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    Remove-Item $TempSQL -ErrorAction SilentlyContinue
}
