# XAgent Framework

XAgent is a framework-agnostic AI agent scaffold designed to keep core contracts stable while letting execution engines evolve independently.

## Design Goal

XAgent Framework is intended to be an enterprise-ready starting point for AI agent systems where the business contract should survive framework churn.

The key design constraint is simple: your task schema, tool logic, and configuration should not need to be rewritten because you switch from one orchestration runtime to another.

That is why XAgent separates the system into:

- a stable core contract layer
- a YAML-based configuration layer
- thin framework adapters
- a small factory that binds configuration to a concrete runtime

## Architecture

- `config/`: YAML-driven agent personas and task definitions.
- `src/xagent/core/`: framework-independent contracts and pure Python tools.
- `src/xagent/adapters/`: thin wrappers for specific agent runtimes.
- `src/xagent/factory.py`: configuration loading and adapter selection.
- `src/xagent/main.py`: CLI entrypoint.
- `logs/`: runtime traces and step logs.

## Repository Layout

```text
xagent/
├── .env.example
├── .github/
│   └── copilot-instructions.md
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── logs/
├── src/
│   └── xagent/
│       ├── __main__.py
│       ├── factory.py
│       ├── main.py
│       ├── adapters/
│       │   ├── autogen_impl.py
│       │   ├── base.py
│       │   ├── crew_impl.py
│       │   └── mock_impl.py
│       └── core/
│           ├── schemas.py
│           └── tools/
│               └── research.py
├── tests/
│   └── test_factory.py
├── pyproject.toml
└── uv.lock
```

## Why this shape

This scaffold keeps business intent decoupled from orchestration engines:

- The `core` layer defines the stable data contracts.
- The `config` layer stores prompt and task metadata outside code.
- The `adapters` layer isolates framework-specific SDK usage.
- The `factory` layer lets you swap engines without rewriting task logic.

## Current Runtime Model

The scaffold ships with three adapter entry points:

- `mock`: fully runnable default adapter for local verification
- `crewai`: skeleton placeholder for future CrewAI integration
- `autogen`: skeleton placeholder for future AutoGen integration

Only `mock` is executable today. The other two intentionally fail fast until their framework SDK wiring is implemented.

## Technology Choices

| Area | Current choice | Reason |
| --- | --- | --- |
| Environment and package management | `uv` | Fast dependency resolution and reproducible local environments |
| Schema validation | `pydantic` | Stable task contracts and typed config loading |
| Config format | `YAML` | Keeps prompt and role metadata out of Python code |
| Model gateway | `litellm` | Prepares the project for multi-model routing without vendor lock-in |
| Environment loading | `python-dotenv` | Keeps local secrets out of source control |
| Testing | `pytest` | Fast validation for factory, adapter, and tool behavior |

## Quick Start

1. Install dependencies:

```bash
uv sync
```

2. Prepare environment variables:

```bash
cp .env.example .env
```

3. Run the default mock adapter:

```bash
uv run xagent --adapter mock --task analyze_topic --input-json '{"topic": "LangGraph migration"}'
```

4. Run tests:

```bash
uv run pytest
```

5. Optional quality check:

```bash
uv run ruff check .
```

## Example CLI Commands

Run the default task with the mock adapter:

```bash
uv run xagent --adapter mock --task analyze_topic --input-json '{"topic": "CrewAI migration strategy"}'
```

Point the CLI at a custom config directory:

```bash
uv run xagent --adapter mock --config-dir config --task analyze_topic --input-json '{"topic": "multi-agent observability"}'
```

## How Configuration Works

### Agent Definitions

`config/agents.yaml` defines agent identity and operating boundaries.

The current example includes:

- `role`: the agent's primary responsibility
- `goal`: the expected outcome bias
- `backstory`: narrative context for prompt shaping
- `llm_model`: the model name to associate with the agent
- `reasoning`: whether the runtime should enable reflective behavior
- `boundaries`: allowed tools, path scope, network access, and code execution policy

### Task Definitions

`config/tasks.yaml` maps a task name to its execution metadata.

The current example includes:

- the task description
- the expected output description
- the agent assigned to the task
- the tools the task may call
- the output schema name

This split makes prompt evolution a configuration concern rather than a code rewrite.

## Core Execution Flow

The current execution path is intentionally small:

1. `main.py` parses CLI arguments and loads environment variables.
2. `factory.py` reads YAML files and validates them into Pydantic models.
3. The factory selects an adapter implementation.
4. The adapter resolves the configured task and agent.
5. The adapter invokes one or more pure Python tools.
6. The adapter returns a normalized `TaskResult` object.

That same flow is expected to remain stable even when a real framework runtime replaces the mock adapter.

## Extending the scaffold

### Add a new tool

1. Create a pure function under `src/xagent/core/tools/`.
2. Register it in the tool registry.
3. Reference it from `config/tasks.yaml`.
4. Expose it inside a concrete adapter when framework wrapping is required.

### Add a new adapter

1. Implement the adapter under `src/xagent/adapters/`.
2. Inherit from the shared adapter base class.
3. Keep framework imports isolated to that adapter module.
4. Register the adapter in `build_adapter`.

### Add a new task

1. Add the task definition to `config/tasks.yaml`.
2. Ensure the referenced agent exists in `config/agents.yaml`.
3. Ensure the tool names referenced by the task exist in the tool registry.
4. Add or update tests for the new execution path.

## Engineering Conventions

- Keep `core/` free of framework SDK dependencies.
- Keep runtime-specific imports inside `adapters/` only.
- Prefer structured outputs through Pydantic models over raw strings.
- Treat YAML as the prompt and persona configuration boundary.
- Add optional dependencies only when a concrete adapter needs them.
- Keep the mock adapter healthy so the scaffold remains runnable in CI.

## Testing Strategy

The current test suite validates the adapter factory and the default mock execution path.

Recommended next additions:

- contract tests for invalid YAML input
- unit tests for each pure tool
- adapter-specific smoke tests once CrewAI or AutoGen is wired in
- CLI tests for invalid adapter or task names

## Git Workflow

This repository is initialized as a Git project.

Typical local workflow:

```bash
git status
uv run pytest
uv run ruff check .
git add .
git commit -m "Describe change"
```

## Planned integrations

This skeleton is prepared for:

- LiteLLM-backed model routing
- ReAct-style execution loops
- CrewAI, AutoGen, or LangGraph adapters
- ChromaDB and SQLite memory layers
- Langfuse or AgentOps observability hooks
- Docker-based code execution sandboxes

## Recommended Next Steps

1. Implement a real CrewAI or AutoGen adapter behind the existing base interface.
2. Add memory abstractions before choosing a concrete vector store.
3. Add tracing hooks at the adapter boundary so observability remains framework-agnostic.
4. Add policy enforcement for tool, network, and filesystem boundaries.

## Delivery Workflow

The repository's recommended Spec-Driven Development and GitHub operations model is documented in [docs/sdd-operations.md](docs/sdd-operations.md).

## Spec Kit

Spec Kit has been initialized in this repository for GitHub Copilot.

Key project-local assets now include:

- `.specify/` for Spec Kit scripts, templates, and project state
- `.github/prompts/` for Spec Kit prompt entry points
- `.github/agents/` for Spec Kit agent definitions

Primary commands available in the Copilot workflow:

- `/speckit.constitution`
- `/speckit.specify`
- `/speckit.plan`
- `/speckit.tasks`
- `/speckit.implement`

Optional quality commands:

- `/speckit.clarify`
- `/speckit.analyze`
- `/speckit.checklist`
- `/speckit.taskstoissues`
