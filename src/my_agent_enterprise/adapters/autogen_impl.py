from __future__ import annotations

from my_agent_enterprise.adapters.base import AgentAdapter
from my_agent_enterprise.core.schemas import TaskRequest, TaskResult


class AutoGenAdapter(AgentAdapter):
    engine_name = "autogen"

    def run(self, request: TaskRequest) -> TaskResult:
        raise RuntimeError(
            "AutoGen adapter is a skeleton only. Install and wire the AutoGen SDK before use."
        )
