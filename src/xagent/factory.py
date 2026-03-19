from __future__ import annotations

from pathlib import Path

import yaml

from xagent.adapters.autogen_impl import AutoGenAdapter
from xagent.adapters.base import AgentAdapter
from xagent.adapters.crew_impl import CrewAIAdapter
from xagent.adapters.mock_impl import MockAdapter
from xagent.core.schemas import AgentDefinition, TaskDefinition
from xagent.core.tools import TOOL_REGISTRY


def _load_yaml(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_agent_definitions(config_dir: Path) -> dict[str, AgentDefinition]:
    raw = _load_yaml(config_dir / "agents.yaml")
    return {
        item["name"]: AgentDefinition.model_validate(item)
        for item in raw.get("agents", [])
    }


def load_task_definitions(config_dir: Path) -> dict[str, TaskDefinition]:
    raw = _load_yaml(config_dir / "tasks.yaml")
    return {
        item["name"]: TaskDefinition.model_validate(item)
        for item in raw.get("tasks", [])
    }


def build_adapter(adapter_name: str, config_dir: Path) -> AgentAdapter:
    agents = load_agent_definitions(config_dir)
    tasks = load_task_definitions(config_dir)

    adapter_registry = {
        "mock": MockAdapter,
        "crewai": CrewAIAdapter,
        "autogen": AutoGenAdapter,
    }

    if adapter_name not in adapter_registry:
        supported = ", ".join(sorted(adapter_registry))
        raise ValueError(f"Unsupported adapter '{adapter_name}'. Supported: {supported}")

    adapter_cls = adapter_registry[adapter_name]
    return adapter_cls(agents=agents, tasks=tasks, tools=TOOL_REGISTRY)
