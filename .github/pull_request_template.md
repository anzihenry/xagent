# Summary

Describe the change in one or two sentences.

## What Changed

- 

## Why

Explain the problem this pull request solves and any important context or tradeoffs.

## Config Impact

State which files, values, or defaults changed under `config/` or environment configuration. Write `None` if not applicable.

## Contract Impact

State any schema, factory, adapter, tool registration, or public execution contract changes. Write `None` if not applicable.

## Observability / Safety Impact

State any changes to logs, traces, auditability, tool access, filesystem access, network access, or code execution boundaries. Write `None` if not applicable.

## Rollout / Rollback

Describe how this change is verified, introduced safely, and rolled back if needed.

## Validation

- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] Targeted validation commands added when config, contracts, adapters, or safety boundaries changed
- [ ] Documentation updated when needed

## Checklist

- [ ] The change is scoped and focused
- [ ] Framework-specific code stays inside `src/xagent/adapters/` when applicable
- [ ] Core contracts remain free of runtime SDK dependencies
- [ ] New configuration or environment changes are documented
- [ ] Constitution-impacting changes are reflected in linked issue or Project metadata
- [ ] Any constitutional exception is explicitly documented and justified

## Related Issues

Link related issues, discussions, or follow-up work.

## Notes for Reviewers

Call out any areas that need extra attention during review.