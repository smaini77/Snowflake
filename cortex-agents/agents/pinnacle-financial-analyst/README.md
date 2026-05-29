# Pinnacle Financial Analyst

AI-powered financial analytics agent for Pinnacle Financial Services executives.

## Overview

| Property | Value |
|----------|-------|
| **Agent** | `PINNACLE_FINANCIAL_ANALYST` |
| **Database** | `SANDEEP_MAINI_COGNIZANT_COM_DB` |
| **Schema** | `ANALYTICS` |
| **Model** | `auto` |
| **Tools** | Cortex Analyst (text-to-sql), Data Visualizer |
| **Semantic View** | `ANALYTICS.FINANCIAL_ANALYTICS` |

## Purpose

Helps Pinnacle Financial Services executives ($2B AUM asset management firm) understand:
- Revenue analysis (management fees, performance fees, advisory fees)
- Expense tracking with budget variance
- Client profitability by segment (Individual, Institutional, Family Office)
- Product performance (Equity, Fixed Income, Alternative, Multi-Asset)

## Data Coverage

**July 2025 – January 2026**

## Setup

### Prerequisites

- Snowflake account with Cortex AI enabled
- Role: `SANDEEP_MAINI_COGNIZANT_COM_ROLE`
- Warehouse: `DEMO_WH` (or any available warehouse)
- Required objects:
  - Semantic View: `ANALYTICS.FINANCIAL_ANALYTICS`
  - Tables: `FACT_REVENUE`, `FACT_EXPENSES`, `DIM_CLIENT`, `DIM_PRODUCT`, `DIM_DATE`, `DIM_EXPENSE_CATEGORY`, `DIM_COST_CENTER`

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
cortex agents describe SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.PINNACLE_FINANCIAL_ANALYST

# Query the agent (interactive)
cortex analyst query "What was our total revenue last quarter?" \
  --view=SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.FINANCIAL_ANALYTICS
```

### Via Snowflake SQL

```sql
-- Describe the agent
DESCRIBE AGENT SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.PINNACLE_FINANCIAL_ANALYST;

-- List versions
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### Sample Questions

- "What was our total revenue last quarter?"
- "Which clients generated the most revenue?"
- "What expense categories are over budget?"
- "Show me revenue by product type"
- "What is our revenue trend by month?"

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
pytest tests/test_pinnacle_agent.py -v
```

## File Structure

```
pinnacle-financial-analyst/
├── spec/
│   └── agent_spec.yaml          # Agent specification (source of truth)
├── semantic_view/
│   └── financial_analytics.yaml # Semantic view definition
├── deploy/
│   ├── create_agent.sql         # CREATE AGENT DDL
│   └── deploy.ps1               # Deployment script
├── tests/
│   ├── sample_questions.json    # Test fixtures
│   └── test_pinnacle_agent.py    # Structural tests
├── .env.template                # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```
