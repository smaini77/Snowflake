# Solution Architecture

## Overview

This repository manages three Snowflake Cortex AI Agents for Cognizant's financial services demonstrations. Each agent is self-contained with its own specification, deployment scripts, and test fixtures.

## Architecture Diagram

```mermaid
graph TD
    subgraph "Cortex Agents"
        A1[Pinnacle Financial Analyst]
        A2[Cascade Financial Analyst]
        A3[SQL Skills Coach]
    end

    subgraph "Tools Layer"
        T1[cortex_analyst_text_to_sql]
        T2[data_to_chart]
    end

    subgraph "Semantic Views"
        SV1[ANALYTICS.FINANCIAL_ANALYTICS]
        SV2[CASCADE_DEMO.FINANCIAL_ANALYTICS]
    end

    subgraph "Data Layer - Pinnacle"
        P1[FACT_REVENUE]
        P2[FACT_EXPENSES]
        P3[DIM_CLIENT]
        P4[DIM_PRODUCT]
        P5[DIM_DATE]
        P6[DIM_EXPENSE_CATEGORY]
        P7[DIM_COST_CENTER]
    end

    subgraph "Data Layer - Cascade"
        C1[FACT_REVENUE]
        C2[FACT_CLIENT_COSTS]
        C3[DIM_CLIENT]
        C4[DIM_PRODUCT]
        C5[DIM_DATE]
        C6[DIM_COST_CENTER]
    end

    A1 --> T1
    A1 --> T2
    A2 --> T1
    A2 --> T2
    A3 -.->|No tools| A3

    T1 --> SV1
    T1 --> SV2

    SV1 --> P1
    SV1 --> P2
    SV1 --> P3
    SV1 --> P4
    SV1 --> P5
    SV1 --> P6
    SV1 --> P7

    SV2 --> C1
    SV2 --> C2
    SV2 --> C3
    SV2 --> C4
    SV2 --> C5
    SV2 --> C6
```

## Component Details

### Agent Layer

| Component | Orchestration Model | Budget |
|-----------|-------------------|--------|
| Pinnacle Financial Analyst | auto | 60s / 16K tokens |
| Cascade Financial Analyst | claude-4-sonnet | 60s / 16K tokens |
| SQL Skills Coach | auto | 60s / 16K tokens |

### Tools Layer

| Tool | Type | Description |
|------|------|-------------|
| cortex_analyst_text_to_sql | Built-in | Converts natural language to SQL via semantic views |
| data_to_chart | Built-in | Generates visualizations from query results |

### Semantic View Layer

Semantic views provide a business-friendly abstraction over raw fact/dimension tables:

- **Metrics**: Pre-defined calculations (TOTAL_REVENUE, BUDGET_VARIANCE, etc.)
- **Dimensions**: Filterable attributes (CLIENT_SEGMENT, PRODUCT_CATEGORY, etc.)
- **Relationships**: Join paths between tables (foreign key mappings)

### Data Layer

All data resides in `<YOUR_DATABASE>` under schema-specific namespaces:
- `ANALYTICS` schema — Pinnacle Financial Services data
- `CASCADE_DEMO` schema — Cascade Wealth Management data

## Deployment Flow

```
1. Developer updates agent_spec.yaml
2. CI validates YAML structure + SQL syntax
3. PR merged to main
4. Deploy script executes CREATE OR REPLACE AGENT
5. Agent is live in Snowflake
```

## Security Considerations

- Agent specs do NOT contain credentials
- Deployment uses Snowflake CLI authentication (key-pair or SSO)
- Role-based access: agents execute under `<YOUR_ROLE>`
- Semantic views enforce column-level access control
