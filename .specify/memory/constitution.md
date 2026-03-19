<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles:
- I. Stable Core, Replaceable Runtimes
- II. Configuration Defines Agent Behavior
- III. Contracts Must Be Tested and Validated
- IV. Observable, Safe, and Change-Controlled Execution
- V. Simplicity and Incremental Delivery
Added sections:
- None
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ⚠ pending .specify/templates/commands/*.md (directory not present in repository)
- ✅ docs/sdd-operations.md
- ✅ docs/github-setup-checklist.md
Follow-up TODOs:
- None
-->
# XAgent Constitution

## Core Principles

### I. Stable Core, Replaceable Runtimes
The core contract layer MUST remain framework-agnostic. Pydantic schemas, task
contracts, tool logic, and factory-facing interfaces MUST NOT depend on a
specific orchestration SDK. Runtime-specific imports, execution semantics, and
framework wiring MUST stay isolated inside thin adapter modules. No production
module outside `src/xagent/adapters/` MAY import a framework runtime package
unless the exception is documented in the feature plan and approved in review.
Rationale: XAgent exists to preserve business intent through framework churn.

### II. Configuration Defines Agent Behavior
Agent persona, task metadata, tool allowance, and runtime selection defaults
MUST be expressed in validated configuration before they are encoded in Python.
YAML is the primary operating surface for agent behavior; code MAY enforce,
compose, or validate configuration, but MUST NOT hide behavior that operators
need to change without a code rewrite. Any behavior that changes runtime
capability, task routing, tool access, or safety boundaries MUST have a
configuration representation or an explicitly documented reason why it cannot.
Rationale: configuration is the contract between product intent and runtime
execution.

### III. Contracts Must Be Tested and Validated
Every change to schemas, configuration loading, factory selection, tool
registration, or adapter behavior MUST include automated validation at the
appropriate level. Pydantic validation, config parsing, and adapter boundaries
MUST fail fast with actionable errors. A change is incomplete until the
relevant tests pass locally and in CI. Merged changes MUST NOT introduce or
retain unvalidated contract behavior. Rationale: the scaffold is only useful if
contract drift is caught early and deterministically.

### IV. Observable, Safe, and Change-Controlled Execution
Execution paths MUST produce enough structured evidence to explain what ran,
with which config, and why a task succeeded or failed. Safety boundaries for
tool use, filesystem access, network access, and code execution MUST be
explicitly defined in configuration or adapter policy. Any change that expands
capability, alters defaults, or weakens a boundary MUST be called out in spec,
plan, and review artifacts. Silent expansion of capability is prohibited.
Rationale: enterprise agents require traceability, auditability, and deliberate
change management.

### V. Simplicity and Incremental Delivery
The repository MUST prefer the smallest design that preserves the contract.
New abstractions, dependencies, and framework integrations MUST be justified by
an immediate delivery need, not anticipated future complexity. Features MUST be
shipped as independently testable increments through Spec Kit artifacts and
GitHub work tracking. Work that cannot be decomposed into a reviewable,
testable increment MUST be re-planned before implementation begins. Rationale:
a scaffold stays maintainable by proving value one thin slice at a time.

## Engineering Constraints

- Python with `uv` is the default development and execution environment; new
	tooling MUST work within that workflow or the feature plan MUST document a
	justified exception.
- Pydantic models are the source of truth for typed contracts and validated
	outputs; raw dictionaries at boundaries MUST be converted into typed models
	before crossing a public or adapter boundary.
- YAML under `config/` is the authoritative source for agent and task
	definitions; duplicated prompt or task metadata in code is not allowed unless
	generated directly from config.
- Adapters MUST remain thin. They may translate between XAgent contracts and a
	runtime SDK, but they MUST NOT become the home for business rules, prompt
	policy, or reusable tool logic.
- Core tools MUST be pure Python and independently testable without a live
	framework runtime. Any external service dependency in a core tool requires an
	explicitly documented exception and a testable abstraction boundary.
- Optional dependencies MUST be isolated to the adapter or feature that needs
	them and MUST fail clearly when unavailable.
- GitHub Projects and GitHub Issues are the delivery system of record. Specs,
	plans, and tasks define intent; issues and project state define execution.

## Workflow and Quality Gates

- Every non-trivial change MUST start from a Spec Kit artifact set that is
	proportionate to the change: spec for user-visible scope, plan for technical
	design, tasks for execution breakdown. Direct implementation without updated
	artifacts is prohibited for non-trivial work.
- The Constitution Check in each implementation plan MUST confirm compliance
	with all five principles before implementation begins and after design is
	finalized.
- Changes to contracts, config schema, adapter selection, tool boundaries, or
	safety policy MUST include explicit test tasks and review notes.
- Minimum local gate before merge: `uv run pytest` and `uv run ruff check .`
	for affected code, plus any added targeted validation commands. A PR that does
	not satisfy the minimum local gate is not review-ready.
- Pull requests MUST describe config impact, contract impact, observability or
	safety impact, and rollback or migration considerations when applicable.
- Work items MUST be decomposed so that each increment can be implemented,
	tested, and reviewed independently without requiring speculative follow-on
	architecture.
- If a proposed change violates the constitution, the plan MUST record the
	violation, explain why it is necessary now, and name the simpler rejected
	alternative before implementation proceeds. Undocumented exceptions are not
	permitted.

## Governance

- This constitution supersedes conflicting local habits, ad hoc design
	preferences, and undocumented workflow exceptions.
- Amendments require a documented change to this file, an explicit rationale,
	and synchronization of affected templates, guidance docs, and review checks.
- Versioning policy for this constitution follows semantic versioning:
	MAJOR for incompatible principle or governance changes, MINOR for new
	principles or materially expanded rules, PATCH for clarifications that do not
	change enforcement intent.
- Compliance review is mandatory in feature planning and pull request review.
	Reviewers MUST reject changes that do not satisfy the constitution or do not
	explicitly justify an approved exception.
- Ratification records the first adoption date of this constitution. Last
	amended records the most recent accepted content change.

**Version**: 1.1.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-03-20
