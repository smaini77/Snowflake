"""
Validate Agent Specifications
Ensures all agent_spec.yaml files have required structure and valid values.

Usage:
    python scripts/validate_specs.py
"""

import sys
import yaml
from pathlib import Path


REQUIRED_TOP_LEVEL_KEYS = {"models", "orchestration", "instructions"}
VALID_MODELS = {"auto", "claude-4-sonnet", "claude-4-haiku", "llama3.3-70b", "mistral-large2"}
VALID_TOOL_TYPES = {"cortex_analyst_text_to_sql", "cortex_search", "data_to_chart", "python"}


def validate_agent_spec(spec_path: Path) -> list[str]:
    """Validate a single agent spec file. Returns list of errors."""
    errors = []

    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]
    except FileNotFoundError:
        return [f"File not found: {spec_path}"]

    if not isinstance(spec, dict):
        return ["Spec must be a YAML mapping (dict)"]

    # Check required top-level keys
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in spec:
            errors.append(f"Missing required key: '{key}'")

    # Validate models section
    if "models" in spec:
        models = spec["models"]
        if "orchestration" in models:
            model_value = models["orchestration"]
            if model_value not in VALID_MODELS:
                errors.append(
                    f"Invalid model '{model_value}'. "
                    f"Valid: {', '.join(sorted(VALID_MODELS))}"
                )

    # Validate orchestration section
    if "orchestration" in spec:
        orch = spec["orchestration"]
        if "budget" in orch:
            budget = orch["budget"]
            if "seconds" in budget and not isinstance(budget["seconds"], (int, float)):
                errors.append("budget.seconds must be a number")
            if "tokens" in budget and not isinstance(budget["tokens"], int):
                errors.append("budget.tokens must be an integer")

    # Validate instructions section
    if "instructions" in spec:
        instructions = spec["instructions"]
        if not isinstance(instructions, dict):
            errors.append("instructions must be a mapping")

    # Validate tools section (optional)
    if "tools" in spec:
        tools = spec["tools"]
        if not isinstance(tools, list):
            errors.append("tools must be a list")
        else:
            for i, tool in enumerate(tools):
                if "tool_spec" not in tool:
                    errors.append(f"tools[{i}]: missing 'tool_spec'")
                else:
                    ts = tool["tool_spec"]
                    if "type" not in ts:
                        errors.append(f"tools[{i}].tool_spec: missing 'type'")
                    elif ts["type"] not in VALID_TOOL_TYPES:
                        errors.append(
                            f"tools[{i}].tool_spec: invalid type '{ts['type']}'"
                        )
                    if "name" not in ts:
                        errors.append(f"tools[{i}].tool_spec: missing 'name'")

    return errors


def main():
    """Find and validate all agent_spec.yaml files."""
    root = Path(__file__).parent.parent
    agents_dir = root / "agents"

    if not agents_dir.exists():
        print("ERROR: agents/ directory not found")
        sys.exit(1)

    spec_files = list(agents_dir.glob("*/spec/agent_spec.yaml"))

    if not spec_files:
        print("WARNING: No agent_spec.yaml files found")
        sys.exit(1)

    print(f"Validating {len(spec_files)} agent specification(s)...\n")

    total_errors = 0

    for spec_path in sorted(spec_files):
        agent_name = spec_path.parent.parent.name
        errors = validate_agent_spec(spec_path)

        if errors:
            print(f"  FAIL  {agent_name}")
            for err in errors:
                print(f"        - {err}")
            total_errors += len(errors)
        else:
            print(f"  PASS  {agent_name}")

    print(f"\n{'='*50}")
    print(f"Results: {len(spec_files)} specs checked, {total_errors} error(s)")
    print(f"{'='*50}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
