from __future__ import annotations

from xagent.adapters.base import AgentAdapter
from xagent.core.schemas import TaskRequest, TaskResult


class MockAdapter(AgentAdapter):
    engine_name = "mock"

    def run(self, request: TaskRequest) -> TaskResult:
        task = self._resolve_task(request.task_name)
        agent = self._resolve_agent(task.agent)
        reasoning = [
            f"Loaded task '{task.name}' from YAML configuration.",
            f"Selected agent '{agent.name}' with model '{agent.llm_model}'.",
        ]

        tool_output = {}
        if task.tools:
            tool_name = task.tools[0]
            tool = self.tools[tool_name]
            tool_output = tool(**request.input)
            reasoning.append(f"Executed pure Python tool '{tool_name}'.")

        return TaskResult(
            status="success",
            summary=f"Mock adapter completed task '{task.name}'.",
            data={
                "engine": self.engine_name,
                "agent": agent.name,
                "task": task.name,
                "tool_output": tool_output,
            },
            reasoning=reasoning,
        )
