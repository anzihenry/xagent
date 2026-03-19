from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any

from my_agent_enterprise.core.schemas import AgentDefinition, TaskDefinition, TaskRequest, TaskResult


class AgentAdapter(ABC):
    engine_name = "base"

    def __init__(
        self,
        agents: Mapping[str, AgentDefinition],
        tasks: Mapping[str, TaskDefinition],
        tools: Mapping[str, Callable[..., Any]],
    ) -> None:
        self.agents = agents
        self.tasks = tasks
        self.tools = tools

    @abstractmethod
    def run(self, request: TaskRequest) -> TaskResult:
        raise NotImplementedError

    def _resolve_task(self, task_name: str) -> TaskDefinition:
        if task_name not in self.tasks:
            raise KeyError(f"Unknown task: {task_name}")
        return self.tasks[task_name]

    def _resolve_agent(self, agent_name: str) -> AgentDefinition:
        if agent_name not in self.agents:
            raise KeyError(f"Unknown agent: {agent_name}")
        return self.agents[agent_name]
