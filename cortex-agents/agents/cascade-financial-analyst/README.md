# Cascade Financial Analyst

AI-powered client profitability analyst for Cascade Wealth Management.

## Overview

| Property | Value |
|----------|-------|
| **Agent** | `CASCADE_FINANCIAL_ANALYST` |
| **Database** | `SANDEEP_MAINI_COGNIZANT_COM_DB` |
| **Schema** | `CASCADE_DEMO` |
| **Model** | `claude-4-sonnet` |
| **Tools** | Cortex Analyst (text-to-sql), Visualizer |
| **Semantic View** | `CASCADE_DEMO.FINANCIAL_ANALYTICS` |

## Purpose

Helps Cascade Wealth Management executives ($500M AUM RIA, retirement-focused) understand:
- Client profitability (revenue vs. cost to serve)
- Revenue by product category and fee type
- AUM analysis and trends
- Cost allocation (direct vs. overhead)
- Regional and relationship manager performance

## Data Coverage

**February 2025 – February 2026**

## Setup

### Prerequisites

- Snowflake account with Cortex AI enabled
- Role: `SANDEEP_MAINI_COGNIZANT_COM_ROLE`
- Warehouse: `DEMO_WH`
- Required objects:
  - Semantic View: `CASCADE_DEMO.FINANCIAL_ANALYTICS`
  - Tables: `FACT_REVENUE`, `FACT_CLIENT_COSTS`, `DIM_CLIENT`, `DIM_PRODUCT`, `DIM_DATE`, `DIM_COST_CENTER`

### Environment Setup

```bash
cp .env.template .env
# Edit .env with your Snowflake credentials
```

### Install Dependencies (for testing)

```bash
pip install -r requirements.txt
```

## Usage

### Via Cortex Code CLI

```bash
# Describe the agent
cortex agents describe SANDEEP_MAINI_COGNIZANT_COM_DB.CASCADE_DEMO.CASCADE_FINANCIAL_ANALYST

# Query via semantic view
cortex analyst query "Which clients are most profitable?" \
  --view=SANDEEP_MAINI_COGNIZANT_COM_DB.CASCADE_DEMO.FINANCIAL_ANALYTICS
```

### Sample Questions

- "What is the total revenue for Cascade Wealth Management?"
- "Which clients are the most profitable?"
- "What is our total AUM?"
- "Break down costs by type"
- "Show revenue by product category"

## Deployment

### Deploy via Script

```powershell
.\deploy\deploy.ps1 -Environment prod
```

### Deploy via SQL (Manual)

```bash
snow sql -f deploy/create_agent.sql --connection COGNIZANT_INDIA
```

## Testing

```bash
pytest tests/test_cascade_agent.py -v
```

## File Structure

```
cascade-financial-analyst/
├── spec/
│   └── agent_spec.yaml          # Agent specification
├── semantic_view/
│   └── financial_analytics.yaml # Semantic view definition
├── deploy/
│   ├── create_agent.sql         # CREATE AGENT DDL
│   └── deploy.ps1               # Deployment script
├── tests/
│   ├── sample_questions.json    # Test fixtures
│   └── test_cascade_agent.py     # Structural tests
├── .env.template                # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```
