# GitHub Setup Checklist

This document turns the repository's SDD workflow into concrete GitHub configuration steps.

## Objective

Use this checklist to configure GitHub so that:

- Spec Kit remains the source of truth for specs and task breakdown
- GitHub Projects manages backlog, progress, and reporting
- GitHub Issues handles bugs and actionable implementation work

## Current Label State

The repository currently has the default GitHub labels:

- `bug`
- `documentation`
- `duplicate`
- `enhancement`
- `good first issue`
- `help wanted`
- `invalid`
- `question`
- `wontfix`

These are not enough for the proposed delivery workflow.

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

### Workflow Labels

Add these labels:

| Label | Purpose |
| --- | --- |
| `blocked` | Work cannot continue due to dependency or decision |
| `needs-spec` | Work is requested but not yet specified in Spec Kit |
| `needs-clarification` | Spec or issue is underspecified |

## Label Rollout Order

Recommended rollout order:

1. Type labels
2. Priority labels
3. Area labels
4. Workflow labels

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

- `Single select`

Options:

- `Inbox`
- `Ready`
- `In Progress`
- `Blocked`
- `In Review`
- `Done`

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

## Recommended Project Views

### 1. Backlog

Configuration:

- Layout: `Table`
- Filter: `Status` is `Inbox` or `Ready`
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

### 4. Current Iteration

Configuration:

- Layout: `Board`
- Filter: current `Iteration`

### 5. Roadmap

Configuration:

- Layout: `Roadmap`
- Group by: `Feature` or `Target Release`

## Recommended Project Automations

### Built-In Automations

Configure these first:

1. auto-add issues from repository `anzihenry/xagent`
2. default new items to `Status = Inbox`
3. archive closed items automatically

### Optional Follow-Up Automations

Add later with Actions or API if needed:

1. set `Type = Bug` when label `bug` is present
2. set `Area = docs` when label `documentation` is present
3. set `Status = In Review` when linked PR is open
4. sync issue labels into Project fields

## Issue Creation Rules

### Bugs

Create bugs through the existing bug issue form.

Required metadata:

- label `bug`
- `Type = Bug`
- `Status = Inbox`

Optional metadata:

- `Priority`
- `Area`
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

## Optional Future Enhancements

1. bootstrap labels using `gh label create`
2. create issue templates for `task` and `feature`
3. automate Project field assignment with GitHub Actions or GraphQL
4. add a small script that validates issue titles against the feature key convention