# Versioning Strategy

## Agent Versioning

Snowflake Cortex Agents support built-in versioning via `VERSION$N` identifiers. This repository uses a **dual versioning** approach:

### 1. Git Tags (Source of Truth)

```
v<major>.<minor>.<patch>-<agent-short-name>
```

Examples:
- `v1.0.0-pinnacle` — Initial production release of Pinnacle agent
- `v1.1.0-cascade` — Minor feature addition to Cascade agent
- `v2.0.0-coach` — Breaking change to SQL Skills Coach

### 2. Snowflake Agent Versions

Each `CREATE OR REPLACE AGENT` creates a new `VERSION$N` in Snowflake. The deploy script logs the mapping:

```
Git Tag              → Snowflake Version
v1.0.0-pinnacle      → VERSION$1
v1.1.0-pinnacle      → VERSION$2
```

## When to Increment

| Change Type | Version Bump | Examples |
|-------------|-------------|----------|
| New tool added / tool removed | MAJOR | Adding cortex_search tool |
| Model change | MAJOR | auto → claude-4-sonnet |
| Prompt refinement | MINOR | Better response formatting |
| Budget adjustment | MINOR | 60s → 120s timeout |
| Sample question update | PATCH | New example in sample_questions |
| Documentation only | PATCH | README clarification |

## Changelog

Maintain a `CHANGELOG.md` per agent (optional) or track via Git tag annotations:

```bash
git tag -a v1.1.0-pinnacle -m "feat: add expense trend analysis to system prompt"
```

## Rollback Strategy

To rollback a Snowflake agent to a previous version:

```sql
-- List available versions
DESCRIBE AGENT SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.PINNACLE_FINANCIAL_ANALYST;

-- Set default to previous version
ALTER AGENT SANDEEP_MAINI_COGNIZANT_COM_DB.ANALYTICS.PINNACLE_FINANCIAL_ANALYST
  SET DEFAULT_VERSION = 'VERSION$1';
```

## Release Process

1. Create a feature branch from `develop`
2. Make changes and update spec version comment
3. Open PR → CI validates
4. Merge to `develop` → deploy to staging (if applicable)
5. Merge `develop` to `main` → deploy to production
6. Tag the release: `git tag -a v1.x.0-<agent> -m "description"`
7. Push tags: `git push origin --tags`
