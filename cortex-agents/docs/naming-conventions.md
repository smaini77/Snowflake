# Naming Conventions

## Directory Names

| Pattern | Example | Rule |
|---------|---------|------|
| Agent folders | `pinnacle-financial-analyst/` | Lowercase, hyphen-separated |
| Subfolders | `spec/`, `deploy/`, `tests/` | Lowercase, singular noun |

## File Names

| Type | Pattern | Example |
|------|---------|---------|
| Agent spec | `agent_spec.yaml` | Always `agent_spec.yaml` |
| Semantic view | `<view_name>.yaml` | `financial_analytics.yaml` |
| Deploy SQL | `create_agent.sql` | Verb_noun pattern |
| Deploy script | `deploy.ps1` / `deploy.sh` | Verb only |
| Test file | `test_agent.py` | `test_` prefix (pytest) |
| Sample data | `sample_questions.json` | `sample_` prefix |
| Environment | `.env.template` | Dot-prefix, `.template` suffix |

## Snowflake Object Names

| Object | Convention | Example |
|--------|------------|---------|
| Agent | UPPER_SNAKE_CASE | `PINNACLE_FINANCIAL_ANALYST` |
| Database | UPPER_SNAKE_CASE | `<YOUR_DATABASE>` |
| Schema | UPPER_SNAKE_CASE | `ANALYTICS` |
| Semantic View | UPPER_SNAKE_CASE | `FINANCIAL_ANALYTICS` |
| Tables | UPPER_SNAKE_CASE with prefix | `FACT_REVENUE`, `DIM_CLIENT` |

## Git Branch Names

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<agent>/<description>` | `feature/pinnacle/add-budget-metric` |
| Bugfix | `fix/<agent>/<description>` | `fix/cascade/cost-query-error` |
| Release | `release/v<major>.<minor>.<patch>` | `release/v1.2.0` |

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

feat(pinnacle): add quarterly revenue breakdown metric
fix(cascade): correct cost allocation join logic
docs(root): update deployment instructions
ci: add sqlfluff linting step
```

### Types

- `feat` — New feature or capability
- `fix` — Bug fix
- `docs` — Documentation changes
- `ci` — CI/CD pipeline changes
- `refactor` — Code restructuring without behaviour change
- `test` — Test additions or modifications
