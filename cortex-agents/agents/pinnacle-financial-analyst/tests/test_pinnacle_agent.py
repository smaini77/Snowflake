"""
Structural tests for Pinnacle Financial Analyst agent.
Validates spec integrity without requiring Snowflake connectivity.

Usage:
    pytest agents/pinnacle-financial-analyst/tests/test_agent.py -v
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
        assert "tools" in spec, "Missing 'tools' section"

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

    def test_tools_have_required_fields(self):
        spec = load_spec()
        for i, tool in enumerate(spec["tools"]):
            assert "tool_spec" in tool, f"tools[{i}]: missing tool_spec"
            ts = tool["tool_spec"]
            assert "type" in ts, f"tools[{i}]: missing type"
            assert "name" in ts, f"tools[{i}]: missing name"
            assert "description" in ts, f"tools[{i}]: missing description"

    def test_tool_resources_reference_valid_tools(self):
        spec = load_spec()
        tool_names = {t["tool_spec"]["name"] for t in spec["tools"]}
        for resource_name in spec.get("tool_resources", {}):
            assert resource_name in tool_names, (
                f"tool_resources references '{resource_name}' but no tool with that name exists"
            )

    def test_semantic_view_reference(self):
        spec = load_spec()
        resources = spec.get("tool_resources", {})
        analyst_resource = resources.get("FinancialAnalyst", {})
        assert "semantic_view" in analyst_resource, "Missing semantic_view in tool_resources"
        sv = analyst_resource["semantic_view"]
        assert sv.count(".") == 2, f"Semantic view must be fully qualified (DB.SCHEMA.NAME): {sv}"

    def test_instructions_have_system_prompt(self):
        spec = load_spec()
        instructions = spec["instructions"]
        assert "system" in instructions, "Missing system instruction"
        assert len(instructions["system"]) > 50, "System prompt too short"

    def test_sample_questions_exist(self):
        spec = load_spec()
        questions = spec["instructions"].get("sample_questions", [])
        assert len(questions) >= 3, "Need at least 3 sample questions"


class TestSampleQuestions:
    """Test sample questions fixture."""

    def test_sample_file_exists(self):
        assert SAMPLE_FILE.exists(), f"Sample questions not found: {SAMPLE_FILE}"

    def test_sample_file_is_valid_json(self):
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list), "Must be a JSON array"
        assert len(data) >= 3, "Need at least 3 sample questions"

    def test_sample_entries_have_required_fields(self):
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, entry in enumerate(data):
            assert "question" in entry, f"Entry {i}: missing 'question'"
            assert "expected_behavior" in entry, f"Entry {i}: missing 'expected_behavior'"
