---
description: "Tasks command with AIOA annotations and context budgets"
scripts:
  - specify tasks
handoffs:
  - label: Validate AIOA Compliance
    agent: speckit.aioa-enforcement.validate
    prompt: "Run mandatory AIOA compliance validation before implementation"
    send: true
---

# speckit.tasks — AIOA-Enhanced Tasks Command

**Preset:** aioa (version 1.0.0)

---

## Workflow

### Step 1: Load Plan with AIOA Context

Read the plan and extract: ADRs, component boundaries, Semantic Integrity checkpoints, context flow maps, runtime state explainability plans, communication patterns.

### Step 2: Decompose into AIOA-Annotated Tasks

For each plan step, create a task with full AIOA annotations:

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

For tasks modifying significant state:

**State Provenance Requirements:**
- [ ] Significant state transitions documented
- [ ] Mutation history includes: what, who, why, when
- [ ] Mutation slices focus on business transitions, not field-level noise
- [ ] State provenance travels with the object

**ADTO Implementation Checklist:** (see [ADTO-EXAMPLE.md](../docs/ADTO-EXAMPLE.md) for full example with anti-patterns)
- [ ] Created/modified objects have mutation history
- [ ] History records business-significant transitions only
- [ ] Each caller produces one mutation slice
- [ ] Provenance accessible to debugging and AI agents

### Step 3: Generate Verification Steps for All Principles

For each task, generate verification checks:

**P1 — Local Reasoning Check:**
- [ ] Task understandable from local context alone
- [ ] External context requirements documented
- [ ] No global state or ambient conventions required

**P2 — Crystallization Radius Check:**
- [ ] Agent has loaded all context files (budget: {n})
- [ ] Task does not expand radius beyond component boundaries
- [ ] No new implicit dependencies introduced
- [ ] Context budget annotations remain accurate after change

**P3 — Semantic Integrity Check:**
- [ ] Shared types used consistently at boundaries
- [ ] "Parse, Don't Validate" at boundaries (TIP-007)
- [ ] No silent data transformations introduced
- [ ] Semantic contracts satisfied

**P4 — Boundaries Explicit Check:**
- [ ] Every boundary crossed is explicitly declared
- [ ] Access through declared interfaces only
- [ ] No implicit boundaries crossed

**P5 — Contracts Deterministic Check:**
- [ ] All interfaces have machine-verifiable schemas
- [ ] Schema validation enforced at boundaries (TIP-007)
- [ ] Contract versions compatible

**P6 — Control-Flow Simplicity Check:**
- [ ] Code is linear and declarative where possible
- [ ] No deeply nested conditionals (depth > 3)
- [ ] Mutable state localized and minimized

**P7 — Architecture Independence Check:**
- [ ] No infrastructure dependencies in core logic
- [ ] All interfaces deployment-agnostic
- [ ] No topology assumptions in implementation

**P8 — Extract Under Reuse Pressure Check:**
- [ ] New abstractions have ≥2 confirmed consumers
- [ ] No speculative abstractions introduced
- [ ] Shared code extracted only under reuse pressure

**P9 — Event Boundaries Check:**
- [ ] Cross-component comms uses event bus where feasible (TIP-008)
- [ ] Direct calls are exceptions with documented rationale
- [ ] Event schemas versioned and shared

**P10 — Runtime State Explainability Check:**
- [ ] State mutations have provenance records (TIP-009: ADTO)
- [ ] State is inspectable without side effects
- [ ] DTOs carry _provenance field where applicable

### Step 4: Order Tasks by Context Dependency

Group tasks sharing 50%+ of context files consecutively.

**Grouping Rules:**
1. Tasks sharing 50%+ context files should be consecutive
2. Tasks in same component boundary should be grouped
3. Tasks crossing multiple boundaries need context refresh before
4. Tasks with state explainability adjacent to their state tracking tasks

### Step 5: Generate AIOA-Compliant Tasks

Write each task using the AIOA task template. Each includes: AIOA context budget, all 10 principle verification checks, Semantic Integrity gates, implementation steps with AIOA annotations, compliance checklist, acceptance/test criteria.

---

## Task Generation Rules

### Rule 1: Context Budget Must Be Accurate
Every task must have a realistic context budget. **Splitting:** 1-5 files acceptable; 6-8 consider splitting; 9+ split by architectural boundary.

### Rule 2: All 10 Principles Must Be Checked
At minimum: P1 (always), P2 (always), P3 (if boundaries crossed).

### Rule 3: Semantic Integrity Gates Mandatory
Every task crossing a component boundary must include Semantic Integrity gates. Crossing detected when: modifying files in multiple components, reading data from another component, adding new interfaces, changing shared types.

### Rule 4: No Deployment Coupling
Tasks must not encode deployment assumptions. Flag if mentioning specific hosting, network topology, infrastructure products (unless delegated to infrastructure boundary).

### Rule 5: State Explainability Must Be Planned
Every stateful task needs P10 provisions. Required when: creating persistent data structures, introducing mutation, creating cross-boundary DTOs, adding caching/stateful middleware.

### Rule 6: Group Related Tasks
Tasks within same component should be sequential. Context retention reduces total context load.

---

## Validation

- [ ] Every task has context budget (files to read/modify)
- [ ] Every task has P1 (Local Reasoning) assessment
- [ ] Every task has P2 (Crystallization Radius) impact
- [ ] Every task crossing boundary has P3 (Semantic Integrity) gates
- [ ] Every task has P4 (Boundaries Explicit) check
- [ ] Every task with interfaces has P5 (Contracts Deterministic) check
- [ ] Every task has P6 (Control-Flow Simplicity) check
- [ ] Every task has P7 (Deployment Independence) check
- [ ] Every task with abstractions has P8 (Extract Under Reuse) check
- [ ] Every task with cross-component comms has P9 (Event Boundaries) check
- [ ] Every task with state has P10 (Runtime Explainability) check
- [ ] Tasks ordered to minimize context reloading

---

## Prompt Templates

### Task Decomposition Prompt
```
Decompose [PLAN_STEP] into AIOA-annotated tasks.
For each task determine:
1. Context budget (files to read/modify) — P2
2. Local Reasoning assessment — P1
3. Boundaries crossed and Semantic Integrity — P3, P4
4. Interface contracts and verifiability — P5
5. Control flow complexity — P6
6. Deployment independence — P7
7. Abstraction justification — P8
8. Communication patterns (event vs direct) — P9
9. State explainability requirements — P10
```

### Context Grouping Prompt
```
Group tasks by context overlap: [TASK_LIST]
Tasks sharing 50%+ context files should be consecutive.
Tasks in same component should be adjacent.
Tasks crossing shared boundaries ordered by dependency.
Tasks with state dependencies ordered by state flow.
```

### Integrity Gate Prompt
```
Define AIOA principle gates for task [TASK_NAME]:
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
