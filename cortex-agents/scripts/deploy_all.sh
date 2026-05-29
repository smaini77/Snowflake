#!/usr/bin/env bash
# ==============================================================================
# Deploy All Cortex Agents
# Usage: ./scripts/deploy_all.sh [--env prod|dev] [--dry-run]
# Requires: SNOWFLAKE_DATABASE and SNOWFLAKE_CONNECTION environment variables
# ==============================================================================

set -euo pipefail

ENVIRONMENT="prod"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --env) ENVIRONMENT="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS=("pinnacle-financial-analyst" "cascade-financial-analyst" "sql-skills-coach")

# Validate required environment variable
if [[ -z "${SNOWFLAKE_DATABASE:-}" ]]; then
    echo "[ERROR] SNOWFLAKE_DATABASE is not set. Export it or define in .env"
    exit 1
fi

echo "============================================"
echo " Cortex Agents - Deployment Script"
echo " Environment: $ENVIRONMENT"
echo " Database:    $SNOWFLAKE_DATABASE"
echo " Dry Run:     $DRY_RUN"
echo "============================================"
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

for agent in "${AGENTS[@]}"; do
    DEPLOY_SQL="$ROOT_DIR/agents/$agent/deploy/create_agent.sql"

    if [[ ! -f "$DEPLOY_SQL" ]]; then
        echo "[SKIP] $agent - SQL file not found"
        continue
    fi

    echo "[DEPLOYING] $agent..."

    # Substitute ${SNOWFLAKE_DATABASE} placeholder
    TEMP_SQL=$(mktemp)
    sed "s/\${SNOWFLAKE_DATABASE}/${SNOWFLAKE_DATABASE}/g" "$DEPLOY_SQL" > "$TEMP_SQL"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "  [DRY RUN] Would execute: $DEPLOY_SQL (with DB=$SNOWFLAKE_DATABASE)"
        ((SUCCESS_COUNT++))
    else
        if snow sql -f "$TEMP_SQL" 2>/dev/null; then
            ((SUCCESS_COUNT++))
            echo "  [SUCCESS] $agent deployed"
        else
            ((FAIL_COUNT++))
            echo "  [FAILED] $agent"
        fi
    fi

    rm -f "$TEMP_SQL"
    echo ""
done

echo "============================================"
echo " Results: $SUCCESS_COUNT succeeded, $FAIL_COUNT failed"
echo "============================================"

[[ $FAIL_COUNT -gt 0 ]] && exit 1 || exit 0
