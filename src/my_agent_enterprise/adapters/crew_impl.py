from __future__ import annotations

from my_agent_enterprise.adapters.base import AgentAdapter
from my_agent_enterprise.core.schemas import TaskRequest, TaskResult


class CrewAIAdapter(AgentAdapter):
    engine_name = "crewai"

    def run(self, request: TaskRequest) -> TaskResult:
        raise RuntimeError(
            "CrewAI adapter is a skeleton only. Install and wire the CrewAI SDK before use."
        )
