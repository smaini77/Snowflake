# SQL Skills Coach

Interactive SQL skills assessment and coaching agent (conversational, tool-less).

## Overview

| Property | Value |
|----------|-------|
| **Agent** | `SQL_SKILLS_COACH` |
| **Database** | `SANDEEP_MAINI_COGNIZANT_COM_DB` |
| **Schema** | `SQL_ASSESSMENT` |
| **Model** | `auto` |
| **Tools** | None (prompt-driven) |

## Purpose

An interactive assessment agent that:
- Generates scenario-based SQL questions at varying difficulty (EASY, MEDIUM, HARD)
- Evaluates user-submitted SQL logically (without execution)
- Provides structured coaching feedback with rubric scoring
- Offers hints and reveals reference solutions on request

## Schema Context

The agent is grounded to a fixed retail schema:

```sql
orders(order_id INT PK, customer_id INT, order_date DATE, total_amount DECIMAL(10,2))
order_items(item_id INT PK, order_id INT FK, product_id INT FK, quantity INT, unit_price DECIMAL(10,2))
products(product_id INT PK, product_name VARCHAR(100), category VARCHAR(50))
```

## Setup

### Prerequisites

- Snowflake account with Cortex AI enabled
- Role: `SANDEEP_MAINI_COGNIZANT_COM_ROLE`
- No data tables required (agent is purely conversational)

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
cortex agents describe SANDEEP_MAINI_COGNIZANT_COM_DB.SQL_ASSESSMENT.SQL_SKILLS_COACH
```

### Interaction Flow

1. User says: **"Start the SQL assessment"**
2. Agent generates a question with difficulty level
3. User submits their SQL answer
4. Agent grades and provides coaching
5. User says **"next"** for another question

### Commands During Assessment

| Command | Action |
|---------|--------|
| `Start the SQL assessment` | Begin a new assessment session |
| `next` | Get the next question |
| `hint` | Get a hint for the current question |
| `show solution` | Reveal the reference SQL solution |

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
pytest tests/test_coach_agent.py -v
```

## File Structure

```
sql-skills-coach/
├── spec/
│   └── agent_spec.yaml          # Agent specification
├── deploy/
│   ├── create_agent.sql         # CREATE AGENT DDL
│   └── deploy.ps1               # Deployment script
├── tests/
│   ├── sample_questions.json    # Test interaction fixtures
│   └── test_coach_agent.py       # Structural tests
├── .env.template                # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Design Notes

This agent is **tool-less** — it operates entirely through its system prompt without connecting to any Snowflake tools or semantic views. The assessment logic, schema context, and evaluation rubric are all embedded in the prompt itself.
