from pathlib import Path

from my_agent_enterprise.core.schemas import TaskRequest
from my_agent_enterprise.factory import build_adapter


def test_mock_adapter_runs_default_task() -> None:
    config_dir = Path(__file__).resolve().parents[1] / "config"
    adapter = build_adapter("mock", config_dir)

    result = adapter.run(TaskRequest(task_name="analyze_topic", input={"topic": "CrewAI"}))

    assert result.status == "success"
    assert result.data["engine"] == "mock"
    assert result.data["task"] == "analyze_topic"
    assert result.data["tool_output"]["topic"] == "CrewAI"
