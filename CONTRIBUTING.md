# Contributing to XAgent

## Development Setup

1. Fork the repository and clone your fork.
2. Create a feature branch from `main`.
3. Install dependencies:

```bash
uv sync
```

4. Copy environment variables if needed:

```bash
cp .env.example .env
```

## Development Workflow

1. Keep framework-specific code inside `src/xagent/adapters/`.
2. Keep the contract layer in `src/xagent/core/` free of runtime SDK dependencies.
3. Add or update tests for behavior changes.
4. Run validation before opening a pull request:

```bash
uv run pytest
uv run ruff check .
```

## Contribution Guidelines

- Prefer small, focused pull requests.
- Keep public APIs stable unless the change explicitly requires a breaking update.
- Update documentation when behavior, configuration, or project structure changes.
- Add new dependencies only when they are necessary for a concrete runtime or capability.
- Preserve the framework-agnostic design of the project.
- Follow the repository's SDD and delivery workflow in `docs/sdd-operations.md` for feature planning, project tracking, and issue usage.

## Pull Request Checklist

- The change is scoped and explained clearly.
- Tests pass locally.
- Lint checks pass locally.
- Documentation has been updated when needed.
- New configuration keys are documented.

## Reporting Issues

Please use the issue templates when reporting bugs or requesting features. Include reproduction steps, your environment details, and the expected behavior.
