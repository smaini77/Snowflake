# Cortex Agents - Snowflake AI Agent Repository

Production-ready repository for Snowflake Cortex AI Agents developed by Sandeep Maini.

## Solution Architecture

```
+------------------------------------------------------------------+
|                    SNOWFLAKE CORTEX PLATFORM                       |
+------------------------------------------------------------------+
|                                                                    |
|  +---------------------+  +---------------------+  +------------+ |
|  | PINNACLE FINANCIAL  |  | CASCADE FINANCIAL   |  | SQL SKILLS | |
|  | ANALYST             |  | ANALYST             |  | COACH      | |
|  +----------+----------+  +----------+----------+  +------+-----+ |
|             |                        |                     |       |
|  +----------v----------+  +----------v----------+         |       |
|  | Cortex Analyst      |  | Cortex Analyst      |  (No tools)    |
|  | (text-to-sql)       |  | (text-to-sql)       |         |       |
|  +----------+----------+  +----------+----------+         |       |
|             |                        |                     |       |
|  +----------v----------+  +----------v----------+         |       |
|  | Semantic View:      |  | Semantic View:      |  Prompt-only   |
|  | ANALYTICS.          |  | CASCADE_DEMO.       |  Conversation  |
|  | FINANCIAL_ANALYTICS |  | FINANCIAL_ANALYTICS |         |       |
|  +----------+----------+  +----------+----------+         |       |
|             |                        |                     |       |
|  +----------v----------+  +----------v----------+         |       |
|  | Fact/Dim Tables     |  | Fact/Dim Tables     |         |       |
|  | (Revenue, Expenses, |  | (Revenue, Costs,    |         |       |
|  |  Clients, Products) |  |  Clients, Products) |         |       |
|  +---------------------+  +---------------------+         |       |
|                                                            |       |
+------------------------------------------------------------------+
```

## Agents Overview

| Agent | Purpose | Model | Tools |
|-------|---------|-------|-------|
| [Pinnacle Financial Analyst](agents/pinnacle-financial-analyst/) | Executive financial analytics for $2B AUM asset management firm | auto | Cortex Analyst + Data Visualizer |
| [Cascade Financial Analyst](agents/cascade-financial-analyst/) | Client profitability analysis for $500M AUM wealth management RIA | claude-4-sonnet | Cortex Analyst + Visualizer |
| [SQL Skills Coach](agents/sql-skills-coach/) | Interactive SQL assessment and coaching (conversational) | auto | None (prompt-driven) |

## Repository Structure

```
cortex-agents/
├── .github/workflows/ci.yml    # CI pipeline (lint + validate)
├── docs/                        # Architecture & conventions
├── scripts/                     # Deployment & validation utilities
└── agents/
    ├── pinnacle-financial-analyst/
    ├── cascade-financial-analyst/
    └── sql-skills-coach/
```

## Prerequisites

- Snowflake account with Cortex AI enabled
- Snowflake CLI (`snow`) or Cortex Code CLI (`cortex`)
- Python 3.10+ (for validation scripts)
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/<your-org>/cortex-agents.git
cd cortex-agents
```

### 2. Configure Environment

```bash
# Copy the template for the agent you want to deploy
cp agents/pinnacle-financial-analyst/.env.template agents/pinnacle-financial-analyst/.env
# Edit .env with your Snowflake credentials
```

### 3. Deploy an Agent

```powershell
# PowerShell (Windows)
.\agents\pinnacle-financial-analyst\deploy\deploy.ps1

# Or deploy all agents at once
.\scripts\deploy_all.ps1
```

### 4. Test an Agent

```bash
# Via Cortex Code CLI
cortex agents describe SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.PINNACLE_FINANCIAL_ANALYST
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_ROLE` | Role with agent privileges |
| `SNOWFLAKE_WAREHOUSE` | Compute warehouse |
| `SNOWFLAKE_DATABASE` | Target database |

## Contributing

1. Create a feature branch: `feature/<agent-name>/<change>`
2. Make changes and validate: `python scripts/validate_specs.py`
3. Submit a pull request with description of changes

## License

Internal use only - Cognizant / Snowflake
