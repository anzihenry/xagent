from __future__ import annotations

from xagent.adapters.base import AgentAdapter
from xagent.core.schemas import TaskRequest, TaskResult


class CrewAIAdapter(AgentAdapter):
    engine_name = "crewai"

    def run(self, request: TaskRequest) -> TaskResult:
        raise RuntimeError(
            "CrewAI adapter is a skeleton only. Install and wire the CrewAI SDK before use."
        )
