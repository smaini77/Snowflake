"""
Structural tests for SQL Skills Coach agent.
Validates spec integrity without requiring Snowflake connectivity.

Usage:
    pytest agents/sql-skills-coach/tests/test_agent.py -v
"""

import json
import yaml
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
SPEC_FILE = AGENT_DIR / "spec" / "agent_spec.yaml"
SAMPLE_FILE = AGENT_DIR / "tests" / "sample_questions.json"


def load_spec():
    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestAgentSpec:
    """Test agent specification structure."""

    def test_spec_file_exists(self):
        assert SPEC_FILE.exists(), f"Agent spec not found: {SPEC_FILE}"

    def test_spec_is_valid_yaml(self):
        spec = load_spec()
        assert isinstance(spec, dict), "Spec must be a dict"

    def test_has_required_sections(self):
        spec = load_spec()
        assert "models" in spec, "Missing 'models' section"
        assert "orchestration" in spec, "Missing 'orchestration' section"
        assert "instructions" in spec, "Missing 'instructions' section"

    def test_model_is_valid(self):
        spec = load_spec()
        model = spec["models"]["orchestration"]
        valid_models = {"auto", "claude-4-sonnet", "claude-4-haiku", "llama3.3-70b", "mistral-large2"}
        assert model in valid_models, f"Invalid model: {model}"

    def test_budget_is_reasonable(self):
        spec = load_spec()
        budget = spec["orchestration"]["budget"]
        assert 10 <= budget["seconds"] <= 300, "Budget seconds out of range"
        assert 1000 <= budget["tokens"] <= 100000, "Budget tokens out of range"

    def test_is_toolless_agent(self):
        """SQL Skills Coach should have NO tools (prompt-only agent)."""
        spec = load_spec()
        tools = spec.get("tools", [])
        assert tools == [], f"Expected no tools but found: {tools}"

    def test_tool_resources_empty(self):
        """SQL Skills Coach should have empty tool_resources."""
        spec = load_spec()
        resources = spec.get("tool_resources", {})
        assert resources == {}, f"Expected empty tool_resources but found: {resources}"

    def test_system_prompt_contains_schema_context(self):
        """System prompt must define the grounding schema."""
        spec = load_spec()
        system = spec["instructions"]["system"]
        assert "orders" in system, "Schema context must include 'orders' table"
        assert "order_items" in system, "Schema context must include 'order_items' table"
        assert "products" in system, "Schema context must include 'products' table"

    def test_system_prompt_prevents_hallucination(self):
        """System prompt must have the grounding rule."""
        spec = load_spec()
        system = spec["instructions"]["system"]
        assert "GROUNDING RULE" in system or "Schema-Only" in system, (
            "System prompt must include schema grounding rule"
        )

    def test_instructions_have_system_prompt(self):
        spec = load_spec()
        instructions = spec["instructions"]
        assert "system" in instructions, "Missing system instruction"
        assert len(instructions["system"]) > 100, "System prompt too short for assessment agent"


class TestSampleQuestions:
    """Test sample questions fixture."""

    def test_sample_file_exists(self):
        assert SAMPLE_FILE.exists(), f"Sample questions not found: {SAMPLE_FILE}"

    def test_sample_file_is_valid_json(self):
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list), "Must be a JSON array"
        assert len(data) >= 3, "Need at least 3 sample interactions"

    def test_sample_entries_have_required_fields(self):
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, entry in enumerate(data):
            assert "question" in entry, f"Entry {i}: missing 'question'"
            assert "expected_behavior" in entry, f"Entry {i}: missing 'expected_behavior'"
