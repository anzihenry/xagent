from __future__ import annotations

from typing import Any


def build_research_brief(topic: str, lens: str = "architecture") -> dict[str, Any]:
    normalized_topic = topic.strip() or "unspecified topic"
    return {
        "topic": normalized_topic,
        "lens": lens,
        "recommendation": (
            "Stabilize the contract layer first, then make each framework adapter "
            "a thin integration boundary."
        ),
        "risks": [
            "Framework-specific abstractions leaking into the core layer",
            "Tool implementations depending on orchestration SDKs",
            "Memory and tracing concerns coupled to a single runtime",
        ],
        "next_steps": [
            "Define pydantic contracts for task IO",
            "Keep prompts and agent metadata in YAML",
            "Add runtime adapters only behind a common interface",
        ],
    }


TOOL_REGISTRY = {
    "build_research_brief": build_research_brief,
}
