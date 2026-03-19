from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from xagent.core.schemas import TaskRequest
from xagent.factory import build_adapter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the enterprise AI agent scaffold.")
    parser.add_argument("--adapter", default="mock", help="Adapter to use: mock, crewai, autogen")
    parser.add_argument("--task", default="analyze_topic", help="Task name from config/tasks.yaml")
    parser.add_argument(
        "--input-json",
        default='{"topic": "Framework-agnostic agent architecture"}',
        help="JSON payload passed to the selected task",
    )
    parser.add_argument("--config-dir", default="config", help="Path to YAML config directory")
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    payload = json.loads(args.input_json)
    adapter = build_adapter(args.adapter, Path(args.config_dir))
    result = adapter.run(TaskRequest(task_name=args.task, input=payload))
    print(json.dumps(result.model_dump(), indent=2))
    return 0
