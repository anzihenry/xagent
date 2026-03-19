# GitHub Setup Checklist

This document turns the repository's SDD workflow into concrete GitHub configuration steps.

## Objective

Use this checklist to configure GitHub so that:

- Spec Kit remains the source of truth for specs and task breakdown
- GitHub Projects manages backlog, progress, and reporting
- GitHub Issues handles bugs and actionable implementation work

## Current Label State

The repository now includes the delivery labels required by this workflow,
including:

- type labels: `task`, `feature`, `chore`
- priority labels: `p0`, `p1`, `p2`, `p3`
- area labels: `area:core`, `area:adapters`, `area:config`, `area:tooling`, `area:docs`, `area:ci`, `area:observability`
- scope labels: `scope:config`, `scope:contract`, `scope:safety`, `scope:observability`
- workflow labels: `blocked`, `needs-spec`, `needs-clarification`, `change-control`

Keep the default GitHub labels that remain useful for triage, but use the
workflow-specific labels above as the operating taxonomy for delivery.

## Recommended Label Taxonomy

### Keep Existing Labels

Keep these labels:

- `bug`
- `documentation`
- `enhancement`
- `good first issue`
- `help wanted`

### Type Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `task` | Implementation work item derived from `tasks.md` |
| `feature` | Feature-level issue or parent tracking issue |
| `chore` | Operational or maintenance work |

### Priority Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `p0` | Critical and urgent |
| `p1` | High priority |
| `p2` | Normal priority |
| `p3` | Low priority |

### Area Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `area:core` | Pydantic contracts, internal abstractions, business logic |
| `area:adapters` | CrewAI, AutoGen, LangGraph, runtime wrappers |
| `area:config` | YAML config, environment, runtime settings |
| `area:tooling` | package management, scripts, developer workflow |
| `area:docs` | docs, contribution guides, process docs |
| `area:ci` | GitHub Actions, release automation, repo governance |
| `area:observability` | logging, tracing, auditability, runtime safety controls |

### Workflow Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `blocked` | Work cannot continue due to dependency or decision |
| `needs-spec` | Work is requested but not yet specified in Spec Kit |
| `needs-clarification` | Spec or issue is underspecified |
| `change-control` | Reviewer attention required for config, contract, or safety-impacting changes |

### Scope Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `scope:config` | Change affects YAML or environment configuration semantics |
| `scope:contract` | Change affects schema, factory, adapter, or tool contracts |
| `scope:safety` | Change affects tool, filesystem, network, or code execution boundaries |
| `scope:observability` | Change affects logs, tracing, auditability, or runtime evidence |

## Label Rollout Order

Recommended rollout order:

1. Type labels
2. Priority labels
3. Area labels
4. Scope labels
5. Workflow labels

This keeps issue triage usable even if the full Project setup is not complete yet.

## GitHub Project Definition

Create one main project for engineering delivery.

Recommended name:

- `XAgent Delivery`

Recommended description:

- `Delivery board for Spec Kit features, implementation tasks, and bug triage for XAgent.`

## Project Fields

Create these fields.

### 1. Type

Field type:

- `Single select`

Options:

- `Feature`
- `Task`
- `Bug`
- `Chore`

### 2. Status

Field type:

- Built-in GitHub Project field

Options:

- `Todo`
- `In Progress`
- `Done`

Usage rule:

- Use `Status` as the only execution-state field in the Project.
- Do not create a second custom status field such as `Delivery Status`.
- Represent blocked work with the `blocked` label while keeping `Status = In Progress`.
- Represent review activity through linked pull requests and saved views rather than a second state field.

### 3. Priority

Field type:

- `Single select`

Options:

- `P0`
- `P1`
- `P2`
- `P3`

### 4. Feature

Field type:

- `Text`

Example values:

- `001-auth-bootstrap`
- `002-crewai-adapter`

### 5. Story

Field type:

- `Single select` or `Text`

Recommended values:

- `US1`
- `US2`
- `US3`

### 6. Area

Field type:

- `Single select`

Options:

- `core`
- `adapters`
- `config`
- `tooling`
- `docs`
- `ci`
- `observability`

### 7. Iteration

Field type:

- `Iteration`

Use this for sprint-style tracking only if you actually work in iterations. If not, leave it available but optional.

### 8. Target Release

Field type:

- `Text` or `Single select`

Example values:

- `0.0.2`
- `0.1.0`

### 9. Spec Link

Field type:

- `Text`

Example values:

- `specs/001-auth-bootstrap/spec.md`

### 10. Change Scope

Field type:

- `Single select`

Options:

- `None`
- `Config`
- `Contract`
- `Safety`
- `Observability`
- `Multiple`

Use this field to surface constitution-sensitive changes that require explicit
review of config impact, contract impact, safety boundaries, or rollback.

## Recommended Project Views

### 1. Backlog

Configuration:

- Layout: `Table`
- Filter: `Status` is `Todo`
- Sort: `Priority` ascending, then `Type`

### 2. Execution Board

Configuration:

- Layout: `Board`
- Group by: `Status`
- Filter: `Type` is not `Bug`

### 3. Bug Triage

Configuration:

- Layout: `Board` or `Table`
- Filter: `Type` is `Bug`
- Group by: `Status`

### 4. Change Control Review

Configuration:

- Layout: `Table`
- Filter: `Change Scope` is not `None` or label is `change-control`
- Sort: `Priority` ascending, then `Updated`

### 5. Review Queue

Configuration:

- Layout: `Table`
- Filter: `Status` is `In Progress` and `Linked pull requests` is not empty
- Sort: `Updated` descending

### 6. Current Iteration

Configuration:

- Layout: `Board`
- Filter: current `Iteration`

### 7. Roadmap

Configuration:

- Layout: `Roadmap`
- Group by: `Feature` or `Target Release`

## Recommended Project Automations

### Built-In Automations

Configure these first:

1. auto-add issues from repository `anzihenry/xagent`
2. default new items to `Status = Todo`
3. archive closed items automatically
4. add repository secret `PROJECT_AUTOMATION_TOKEN` with `repo` and `project` scopes

### Optional Follow-Up Automations

Add later with Actions or API if needed:

1. run `.github/workflows/project-field-sync.yml` to sync `Type`, `Priority`, `Area`, and `Change Scope` from issue labels
2. apply `scope:*` labels during issue triage so `Change Scope` can be filled automatically
3. surface linked-PR work in the `Review Queue` view

## Issue Creation Rules

### Bugs

Create bugs through the existing bug issue form.

Required metadata:

- label `bug`
- `Type = Bug`
- `Status = Todo`

Optional metadata:

- `Priority`
- `Area`
- one or more `scope:*` labels when config, contract, safety, or observability is affected
- `Target Release`

### Feature Parent Issues

Create a parent issue for larger features when one feature produces multiple implementation tasks.

Required metadata:

- label `feature`
- `Type = Feature`
- `Feature = <feature-key>`
- `Spec Link = specs/<feature-key>/spec.md`

### Task Issues

Create task issues from `tasks.md`.

Required metadata:

- label `task`
- one `area:*` label
- one priority label
- `scope:*` labels when config, contract, safety, or observability is affected
- `Type = Task`
- `Feature = <feature-key>`
- `Story = <US#>` when applicable

## Suggested Issue Title Patterns

### Feature Issue

- `[001-auth-bootstrap] Build CrewAI adapter integration plan`

### Task Issue

- `[001-auth-bootstrap][US1][T012] Add adapter factory validation`

### Bug Issue

- `[bug] CLI fails on malformed input JSON`

## One-Time Rollout Checklist

Complete these in order:

1. create missing labels
2. create project `XAgent Delivery`
3. create project fields
4. create saved views
5. enable auto-add and archive automation
6. verify bug issues land in `Bug Triage`
7. verify task issues land in `Backlog`
8. document the Project URL in the repository README if useful

## Ongoing Operating Rules

1. every non-trivial feature starts in Spec Kit
2. every implementation PR should reference a GitHub issue
3. every implementation issue should reference a feature key
4. bugs do not bypass the issue form
5. Projects reflects status; spec documents reflect intent
6. issue labels are the source of truth for automated `Type`, `Priority`, `Area`, and `Change Scope` field sync

## Status Convention

Use only the built-in GitHub Project `Status` field for execution state.

- `Todo`: triaged and not yet started
- `In Progress`: actively being implemented or reviewed
- `Done`: completed and closed out

Use labels and linked pull requests for supplemental state instead of creating a
second status field.

- add label `blocked` when work cannot proceed
- use the `Review Queue` view to see items with linked pull requests
- use `Change Scope` and `change-control` for constitution-sensitive review

## Optional Future Enhancements

1. bootstrap labels using `gh label create`
2. create issue templates for `task` and `feature`
3. extend Project sync automation to infer `Feature` and `Story` from issue titles or body metadata
4. add a small script that validates issue titles against the feature key convention