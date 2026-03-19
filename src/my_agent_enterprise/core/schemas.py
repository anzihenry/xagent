from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class BoundaryRule(BaseModel):
    allowed_tools: list[str] = Field(default_factory=list)
    allowed_paths: list[str] = Field(default_factory=list)
    network_access: bool = False
    code_execution: bool = False


class AgentDefinition(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str = ""
    llm_model: str = "gpt-4.1-mini"
    reasoning: bool = True
    boundaries: BoundaryRule = Field(default_factory=BoundaryRule)


class TaskDefinition(BaseModel):
    name: str
    description: str
    expected_output: str
    agent: str
    tools: list[str] = Field(default_factory=list)
    output_schema: str = "TaskResult"


class TaskRequest(BaseModel):
    task_name: str
    input: dict[str, Any] = Field(default_factory=dict)


class TaskResult(BaseModel):
    status: Literal["success", "error"] = "success"
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)
    reasoning: list[str] = Field(default_factory=list)
