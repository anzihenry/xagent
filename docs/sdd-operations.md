# SDD Operations Guide

This document defines how XAgent uses Spec Kit, GitHub Projects, and GitHub Issues together.

## Objective

The workflow is designed to keep three concerns separate:

- `spec-kit` is the source of truth for requirements, design intent, and task decomposition.
- GitHub Projects is the management surface for backlog, priorities, schedule, and progress.
- GitHub Issues is the execution surface for bugs and implementation work items.

This separation is intentional. Specifications should remain structured documents, while progress and delivery status should remain native to GitHub.

## Tool Responsibilities

### Spec Kit

Use Spec Kit for:

- project constitution
- feature specifications
- implementation plans
- task breakdown
- consistency analysis before implementation

Do not use GitHub Issues as the primary source of feature requirements when a feature already has Spec Kit artifacts.

### GitHub Projects

Use GitHub Projects for:

- feature backlog
- release and iteration planning
- work-in-progress visibility
- roadmap and status reporting
- bug triage views

Projects should aggregate work items. It should not replace specification documents.

### GitHub Issues

Use GitHub Issues for:

- bug reports
- feature implementation work items
- technical chores and follow-ups
- discussion tied to executable work

Bug issues live directly in GitHub Issues. Feature implementation issues are typically created from `tasks.md`.

## Canonical Workflow

### 1. Define operating rules

At project start or when the engineering policy changes:

1. Run `/speckit.constitution`
2. Record quality, testing, architecture, and review constraints
3. Treat the constitution as the governing rulebook for all future features
4. Keep Spec Kit templates and workflow docs synchronized when the constitution changes

### 2. Create a feature specification

For each new feature:

1. Create a feature branch using a numeric feature prefix, such as `001-auth-bootstrap`
2. Run `/speckit.specify`
3. Focus on user outcomes, constraints, and scope boundaries
4. Run `/speckit.clarify` if the feature still has ambiguity

Expected artifact location:

- `specs/001-auth-bootstrap/spec.md`

### 3. Create a technical plan

After the feature spec is accepted:

1. Run `/speckit.plan`
2. Capture architecture, tech stack, file structure, and implementation constraints
3. Keep runtime-specific choices aligned with XAgent's core rule: framework-specific code belongs in `src/xagent/adapters/`
4. Complete the Constitution Check before research and again after design

Expected artifacts:

- `plan.md`
- optional `research.md`
- optional `data-model.md`
- optional `contracts/`

### 4. Break down into tasks

1. Run `/speckit.tasks`
2. Review generated `tasks.md`
3. Ensure tasks are grouped by user story and contain exact file paths where possible
4. Run `/speckit.analyze` before implementation when the feature is non-trivial
5. Ensure tasks include required validation, observability, and change-control work for config, contract, and adapter changes

Expected artifact:

- `tasks.md`

### 5. Convert implementation tasks into GitHub Issues

Once `tasks.md` is stable:

1. Use `/speckit.taskstoissues` if available in the active agent environment
2. Create one issue per actionable task or per logical task bundle
3. Link each issue back to the feature spec identifier in the title or body
4. Use the optional `after_tasks` hook in `.specify/extensions.yml` to surface issue publication immediately after task generation

Recommended issue title format:

- `[001-auth-bootstrap][US1] Add adapter factory validation`

Recommended issue body metadata:

- Spec: `specs/001-auth-bootstrap/spec.md`
- Story: `US1`
- Task ID: `T012`
- Phase: `User Story 1`

### 6. Track execution in GitHub Projects

After issues exist:

1. Automatically add new issues to the project
2. Use Project fields to represent priority, status, iteration, and feature identity
3. Let repository automation sync `Type`, `Priority`, `Area`, and `Change Scope` from issue labels
4. Move work through the Project instead of maintaining a second manual tracker

### 7. Implement and close

1. Reference the issue in the branch or PR
2. Use PR keywords such as `fixes #123` where appropriate
3. When PRs merge, allow linked implementation issues to close automatically
4. Keep spec artifacts updated if implementation changes the agreed design
5. Verify PR review covers config impact, contract impact, safety impact, and rollback considerations when applicable

## Feature Naming Convention

Each feature should have a stable feature key.

Recommended pattern:

- `001-auth-bootstrap`
- `002-crewai-adapter`
- `003-memory-abstraction`

Use the same identifier in all three layers:

- Spec Kit directory name
- GitHub Project `Feature` field
- issue titles or labels

## GitHub Project Design

Create one main project for delivery management.

Recommended project name:

- `XAgent Delivery`

### Required Fields

Create these fields in the project:

1. `Type` (`single select`)
   - `Feature`
   - `Task`
   - `Bug`
   - `Chore`
2. `Status` (built-in GitHub Project field)
   - `Todo`
   - `In Progress`
   - `Done`
   - Use this as the only execution-state field; do not create a second custom status field
3. `Priority` (`single select`)
   - `P0`
   - `P1`
   - `P2`
   - `P3`
4. `Feature` (`text`)
   - Example: `001-auth-bootstrap`
5. `Story` (`single select` or `text`)
   - `US1`
   - `US2`
   - `US3`
6. `Area` (`single select`)
   - `core`
   - `adapters`
   - `config`
   - `tooling`
   - `docs`
   - `ci`
   - `observability`
7. `Iteration` (`iteration`)
8. `Target Release` (`text` or `single select`)
   - Example: `0.0.2`
9. `Spec Link` (`text`)
   - Example: `specs/001-auth-bootstrap/spec.md`
10. `Change Scope` (`single select`)
   - `None`
   - `Config`
   - `Contract`
   - `Safety`
   - `Observability`
   - `Multiple`

### Recommended Views

Create these saved views:

1. `Backlog`
   - Layout: table
   - Filter: `Status:Todo`
2. `Execution Board`
   - Layout: board
   - Group by: `Status`
   - Filter: `Type is not Bug`
3. `Bug Triage`
   - Layout: table or board
   - Filter: `Type:Bug`
4. `Change Control Review`
   - Layout: table
   - Filter: `Change Scope is not None` or label `change-control`
5. `Review Queue`
   - Layout: table
   - Filter: `Status is In Progress` and linked pull requests exist
6. `Current Iteration`
   - Layout: board
   - Filter: current `Iteration`
7. `Roadmap`
   - Layout: roadmap
   - Group by: `Feature` or `Target Release`

### Recommended Automations

Enable built-in or custom automation for:

1. auto-add new issues from `anzihenry/xagent`
2. default `Status = Todo`
3. archive closed items automatically
4. repository workflow `.github/workflows/project-field-sync.yml` with a `PROJECT_AUTOMATION_TOKEN` secret to sync issue labels into Project fields

Optional later automation:

1. infer `Feature` and `Story` from issue title conventions or body metadata
2. add new PRs to project and surface them in the `Review Queue` view

### Status Convention

Use only the built-in GitHub Project `Status` field as the canonical execution
state.

- `Todo`: triaged and not started
- `In Progress`: actively being implemented or reviewed
- `Done`: completed and merged or otherwise closed out

Use labels and linked pull requests for supplemental state instead of a second
status field.

- `blocked` label: work cannot currently proceed
- linked pull request present: item is in active review flow
- `change-control` label or `Change Scope != None`: constitution-sensitive review required

## GitHub Issue Model

### Issue Types

Use issues for three categories only:

1. `bug`
2. `task`
3. `feature` or `chore`

Keep bugs separate from feature tasks. Do not turn every design discussion into an issue.

### Labels

Recommended label set:

1. Type labels
   - `bug`
   - `task`
   - `feature`
   - `chore`
2. Priority labels
   - `p0`
   - `p1`
   - `p2`
   - `p3`
3. Area labels
   - `area:core`
   - `area:adapters`
   - `area:config`
   - `area:tooling`
   - `area:docs`
   - `area:ci`
   - `area:observability`
4. Scope labels
   - `scope:config`
   - `scope:contract`
   - `scope:safety`
   - `scope:observability`
5. Workflow labels
   - `blocked`
   - `needs-spec`
   - `needs-clarification`
   - `change-control`

### Issue Content Rules

For implementation issues created from Spec Kit tasks, include:

1. feature key
2. story identifier
3. task identifier
4. acceptance criteria
5. relevant file paths or planned modules

For bugs, include:

1. reproduction steps
2. expected behavior
3. actual behavior
4. environment details
5. linked spec or feature issue when relevant

### Dependencies and Hierarchy

Use GitHub issue relationships when available:

1. large feature issue as parent
2. task issues as sub-issues
3. `blocked by` relationships for cross-task dependencies

Do not model every line in `tasks.md` as a separate issue if the granularity becomes noisy. Bundle very small tasks into one implementation issue.

## Rules for Bugs

Bug handling is intentionally separate from the feature-spec pipeline.

### When to Create a Bug Issue

Create a bug issue when:

1. current behavior violates expected functionality
2. there is a regression from a previous working state
3. the implementation differs from an accepted spec or contract

### When a Bug Should Trigger Spec Updates

Update Spec Kit artifacts only if the bug reveals one of these conditions:

1. the accepted requirement was ambiguous
2. the plan was internally inconsistent
3. the implementation changed the intended behavior and that change should become the new standard

If the bug is purely implementation-level, do not rewrite the spec.

## Branch and PR Rules

### Branch Naming

Recommended branch patterns:

- `feature/001-auth-bootstrap`
- `task/001-auth-bootstrap-t012-factory-validation`
- `bug/123-cli-json-parse-error`

### PR Rules

Each PR should:

1. link one primary issue
2. describe the scope clearly
3. mention the feature key when part of a larger spec
4. update docs or specs if behavior changed

Use the existing pull request template as the enforcement surface.

## Traceability Rules

This repository should preserve end-to-end traceability:

1. `constitution` defines the engineering rules
2. `spec.md` defines the feature intent
3. `plan.md` defines the implementation approach
4. `tasks.md` defines execution units
5. GitHub Issues track execution and bugs
6. GitHub Project visualizes state and delivery progress
7. PRs and commits implement the work

Minimum traceability rule:

- every merged feature PR should reference an issue
- every non-trivial implementation issue should map back to a Spec Kit feature key

## Recommended Repository Additions

These are not mandatory on day one, but they are the next logical improvements:

1. add a lightweight `specs/README.md` explaining feature directory naming
2. add label setup automation or a one-time bootstrap script
3. extend the Project sync workflow if `Feature` and `Story` should also be derived automatically

## Repository Automation Additions

The repository now includes two automation entry points that reduce manual handoff work:

1. `.github/workflows/project-field-sync.yml`
   - listens to issue events
   - adds issues to `XAgent Delivery` if needed
   - synchronizes `Type`, `Priority`, `Area`, and `Change Scope` from labels
2. `.specify/extensions.yml`
   - registers an optional `after_tasks` hook
   - surfaces `/speckit.taskstoissues` immediately after `tasks.md` is generated

These automations do not eliminate the need for human review. They reduce repeated metadata entry and make the Spec Kit to GitHub handoff easier to execute consistently.

The concrete GitHub setup checklist for labels, Project fields, and recommended views lives in `docs/github-setup-checklist.md`.

## Minimal Day-One Operating Model

If you want the smallest workable process, use this:

1. create a feature with `/speckit.specify`
2. generate `plan.md` and `tasks.md`
3. convert tasks into GitHub Issues
4. auto-add those issues into `XAgent Delivery`
5. manage progress in Projects
6. keep bug reporting separate through issue forms

This gives XAgent a clean SDD workflow without forcing GitHub Projects to act as the specification store.