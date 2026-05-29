-- ==============================================================================
-- Cascade Financial Analyst - Agent DDL
-- Database: ${SNOWFLAKE_DATABASE} (substituted at deploy time)
-- Schema:   CASCADE_DEMO
-- ==============================================================================

USE DATABASE ${SNOWFLAKE_DATABASE};
USE SCHEMA CASCADE_DEMO;

CREATE OR REPLACE AGENT CASCADE_FINANCIAL_ANALYST
  COMMENT = 'Cascade Wealth Management Financial Analyst - POC Demo for client profitability analysis'
  PROFILE = '{"display_name": "Cascade Financial Analyst", "color": "blue"}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-4-sonnet

  orchestration:
    budget:
      seconds: 60
      tokens: 16000

  instructions:
    system: |
      You are a financial analyst for Cascade Wealth Management, a $500M AUM RIA
      focused on retirement planning. Help executives understand client profitability
      and financial performance.

    response: |
      Provide clear, executive-ready responses. Format currency with $ and commas.
      Include specific numbers and highlight key profitability insights.

    orchestration: |
      Use Analyst for all financial questions. For profitability analysis, query
      revenue and costs by client.

  tools:
    - tool_spec:
        type: cortex_analyst_text_to_sql
        name: Analyst
        description: >
          Analyzes Cascade Wealth Management financial data including client revenue,
          AUM, costs, and profitability metrics.

    - tool_spec:
        type: data_to_chart
        name: Visualizer
        description: >
          Creates charts and visualizations from financial data.

  tool_resources:
    Analyst:
      semantic_view: ${SNOWFLAKE_DATABASE}.CASCADE_DEMO.FINANCIAL_ANALYTICS
  $$;
