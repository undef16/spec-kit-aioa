---
description: "Tasks command with AIOA annotations and context budgets"
scripts:
  - specify tasks
---

# speckit.tasks — AIOA-Enhanced Tasks Command

**Preset:** aioa (version 1.0.0)

This command overrides the standard `specify tasks` flow to generate AIOA-validated tasks with verification of all 10 AIOA principles built into every task.

---

## Overview

When invoked, this command:
1. Decomposes the plan into AIOA-annotated tasks
2. Includes verification checks for all 10 AIOA principles in every task
3. Adds integrity gates at every boundary crossing
4. Validates runtime state explainability requirements
5. Orders tasks to minimize context switching

---

## Workflow

### Step 1: Load Plan with AIOA Context

Read the plan and extract:
- ADRs with all AIOA principle analysis
- Component boundary definitions
- Semantic Integrity checkpoints
- Context flow maps
- Runtime state explainability plans
- Communication patterns (event vs direct)

### Step 2: Decompose into AIOA-Annotated Tasks

For each step in the plan, create a task with full AIOA annotations:

> **Each task includes checks for all 10 AIOA principles.**

**Task AIOA Annotation Structure:**

```
---
aioa:
  context_budget:
    files_to_read: [list]
    files_to_modify: [list]
    cross_module_context: [list]
    rating: LOW|MEDIUM|HIGH
  p1_local_reasoning:
    verdict: self_contained|some_external|extensive_external
    external_context: [list]
  p2_crystallization_radius:
    current: rating
    expected_after: rating
    delta: +n|-n|0
    regression_risk: true|false
  p3_semantic_integrity:
    boundaries_crossed:
      - boundary: name
        direction: inbound|outbound|internal
        data: description
        contract: contract_name
    gates:
      - shared_types_consistent: boolean
      - parse_dont_validate: boolean
      - no_silent_transformations: boolean
  p4_boundaries_explicit:
    boundaries_involved: [list]
    all_declared: boolean
  p5_contracts_deterministic:
    interfaces: [list]
    all_machine_verifiable: boolean
    schema_validation_enforced: boolean
  p6_control_flow_simplicity:
    max_nesting_depth: number
    declarative_ratio: percentage
    verdict: pass|partial|fail
  p7_reasoning_boundaries_not_deployment:
    topology_assumptions: [list]
    infrastructure_coupling: [list]
    verified: boolean
  p8_extract_under_reuse:
    new_abstractions: [list]
    consumer_counts: [map]
    premature_abstractions: [list]
  p9_event_boundaries:
    communication_methods: [map]
    uses_event_bus: boolean
    direct_call_justifications: [list]
  p10_runtime_state_explainable:
    state_tracking: [list]
    provenance_logged: boolean
    adto_compliant: boolean
    inspectable: boolean
---
```

### TIP-009: Auditable DTOs (ADTO) Pattern

For tasks that create or modify significant state, add these annotations:

#### State Provenance Requirements
- [ ] Significant state transitions documented
- [ ] Mutation history includes: what changed, who changed it, why, when
- [ ] Mutation slices focus on business transitions, not field-level noise
- [ ] State provenance travels with the object

#### ADTO Implementation Checklist
- [ ] Created or modified objects have mutation history
- [ ] History records business-significant transitions only
- [ ] Each caller method produces one mutation slice
- [ ] Provenance is accessible to debugging tools and AI agents

### Step 3: Generate Verification Steps for All Principles

For each task, generate explicit verification steps for all 10 principles:

**P1 — Local Reasoning Check:**
```
## Local Reasoning Check
- [ ] Task can be understood from local context alone
- [ ] All external context requirements are documented
- [ ] No global state or ambient conventions required
```

**P2 — Crystallization Radius Check:**
```
## Crystallization Radius Check
- [ ] Agent has loaded all context files (budget: {n})
- [ ] Task does not expand Crystallization Radius beyond component boundaries
- [ ] No new implicit dependencies introduced
- [ ] Context budget annotations remain accurate after change
```

**P3 — Semantic Integrity Check:**
```
## Semantic Integrity Check
- [ ] Shared types are used consistently at boundaries
- [ ] "Parse, Don't Validate" pattern is followed at boundaries (TIP-007)
- [ ] No silent data transformations introduced
- [ ] Semantic contracts are satisfied
```

**P4 — Boundaries Explicit Check:**
```
## Boundaries Explicit Check
- [ ] Every boundary crossed is explicitly declared
- [ ] Access occurs through declared interfaces only
- [ ] No implicit boundaries crossed
```

**P5 — Contracts Deterministic Check:**
```
## Contracts Deterministic Check
- [ ] All interfaces have machine-verifiable schemas
- [ ] Schema validation is enforced at boundaries (TIP-007)
- [ ] Contract versions are compatible
```

**P6 — Control-Flow Simplicity Check:**
```
## Control-Flow Simplicity Check
- [ ] Code is linear and declarative where possible
- [ ] No deeply nested conditionals (depth > 3)
- [ ] Mutable state is localized and minimized
```

**P7 — Reasoning Boundaries not Deployment Check:**
```
## Architecture Independence Check
- [ ] No infrastructure dependencies in core logic
- [ ] All interfaces remain deployment-agnostic
- [ ] No topology assumptions in implementation
```

**P8 — Extract Under Reuse Pressure Check:**
```
## Extract Under Reuse Pressure Check
- [ ] Any new abstractions have ≥2 confirmed consumers
- [ ] No speculative abstractions introduced
- [ ] Shared code extracted based on reuse pressure only
```

**P9 — Event Boundaries Check:**
```
## Event Boundaries Check
- [ ] Cross-component communication uses event bus where feasible (TIP-008)
- [ ] Direct synchronous calls are exceptions with documented rationale
- [ ] Event schemas are versioned and shared
```

**P10 — Runtime State Explainability Check:**
```
## Runtime State Explainability Check
- [ ] State mutations have provenance records (TIP-009: ADTO)
- [ ] State is inspectable without side effects
- [ ] DTOs carry _provenance field where applicable
```

### Step 4: Order Tasks by Context Dependency

Analyze task dependencies and order them to minimize context switching:

> **Tasks with overlapping context should be grouped to minimize reloading.**

**Grouping Rules:**
1. Tasks sharing 50%+ of context files should be consecutive
2. Tasks in the same component boundary should be grouped
3. Tasks crossing multiple boundaries should be preceded by context refresh
4. Tasks with state explainability requirements should be adjacent to their state tracking tasks

### Step 5: Generate AIOA-Compliant Tasks

Write each task using the AIOA task template.

**Each task includes:**
- AIOA context budget
- All 10 AIOA principle verification checks
- Semantic Integrity gates for boundary crossings
- Implementation steps with AIOA annotations
- AIOA compliance checklist for verification
- Standard task details (acceptance criteria, test criteria)

---

## Task Generation Rules

### Rule 1: Context Budget Must Be Accurate

Every task must have a realistic context budget. If a task requires more than 8 context files, it must be split into smaller tasks.

**Splitting Heuristic:**
- **9+ files:** Split by architectural boundary
- **6–8 files:** Consider splitting, document if not
- **1–5 files:** Acceptable as single task

### Rule 2: All 10 Principles Must Be Checked

Every task SHALL include verification checks for all applicable AIOA principles. At minimum:
- P1 (Local Reasoning) — always checked
- P2 (Crystallization Radius) — always checked
- P3 (Semantic Integrity) — checked if boundaries are crossed

### Rule 3: Semantic Integrity Gates Are Mandatory

Every task that crosses a component boundary must include Semantic Integrity gates.

**Boundary crossing detected when:**
- Task modifies files in multiple components
- Task reads data from another component
- Task adds a new interface between components
- Task changes a shared type

### Rule 4: No Deployment Coupling in Tasks

Tasks must not encode deployment assumptions.

**Flag for review if task mentions:**
- Specific hosting environment
- Network topology
- Specific infrastructure products (unless delegated to infrastructure boundary)

### Rule 5: State Explainability Must Be Planned

Every task that introduces or modifies stateful components must include runtime state explainability provisions (P10).

**State explainability required when:**
- Task creates new data structures that persist across requests
- Task introduces mutation logic
- Task creates new DTOs that cross boundaries
- Task adds caching or stateful middleware

### Rule 6: Group Related Tasks

Tasks within the same component should be sequential. Context retention reduces total context load.

---

## Validation

### Pre-Output Checks

- [ ] Every task has a context budget (files to read, files to modify)
- [ ] Every task has P1 (Local Reasoning) assessment
- [ ] Every task has P2 (Crystallization Radius) impact
- [ ] Every task crossing a boundary has P3 (Semantic Integrity) gates
- [ ] Every task has P4 (Boundaries Explicit) check
- [ ] Every task with interfaces has P5 (Contracts Deterministic) check
- [ ] Every task has P6 (Control-Flow Simplicity) check
- [ ] Every task has P7 (Deployment Independence) check
- [ ] Every task with abstractions has P8 (Extract Under Reuse) check
- [ ] Every task with cross-component communication has P9 (Event Boundaries) check
- [ ] Every task with state has P10 (Runtime Explainability) check
- [ ] Tasks are ordered to minimize context reloading

---

## Prompt Templates

### Task Decomposition Prompt

```
Decompose [PLAN_STEP] into AIOA-annotated tasks.

For each task, determine:
1. Context budget (files to read, files to modify) — P2
2. Local Reasoning assessment — P1
3. Boundaries crossed and Semantic Integrity requirements — P3, P4
4. Interface contracts and verifiability — P5
5. Control flow complexity — P6
6. Deployment independence — P7
7. Abstraction justification — P8
8. Communication patterns (event vs direct) — P9
9. State explainability requirements — P10
```

### Context Grouping Prompt

```
Group the following tasks by context overlap:
[TASK_LIST]

Tasks sharing 50%+ of their context files should be consecutive.
Tasks in the same component should be adjacent.
Tasks crossing shared boundaries should be ordered by dependency.
Tasks with state dependencies should be ordered by state flow.
```

### Integrity Gate Prompt

```
Define all AIOA principle gates for task [TASK_NAME].

Boundaries crossed: [LIST]
Data crossing each boundary: [LIST]
Interfaces: [LIST]
State involved: [LIST]

For each:
1. P3: What shared types govern boundaries?
2. P5: What machine-verifiable schemas exist?
3. P9: Is communication event-driven?
4. P10: Is state provenance tracked?
```
