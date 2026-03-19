from __future__ import annotations

from xagent.adapters.base import AgentAdapter
from xagent.core.schemas import TaskRequest, TaskResult


class AutoGenAdapter(AgentAdapter):
    engine_name = "autogen"

    def run(self, request: TaskRequest) -> TaskResult:
        raise RuntimeError(
            "AutoGen adapter is a skeleton only. Install and wire the AutoGen SDK before use."
        )
