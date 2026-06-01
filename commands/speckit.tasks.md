---
description: "AIOA-enhanced tasks command — verify all TIPs in task decomposition"
scripts:
  - specify tasks
handoffs:
  - label: Validate AIOA Compliance
    agent: speckit.aioa-enforcement.validate
    prompt: "Run mandatory AIOA compliance validation before implementation"
    send: true
---

# speckit.tasks — AIOA Tasks Command

**Preset:** aioa (version 1.0.0)
**Reference:** [AIOA.md](../docs/AIOA.md) — Technical Implementation Patterns (TIP-002-TIP-008)

---

## Workflow

### Step 1: Load Plan with AIOA Context

Read the plan and extract architecture decisions, component boundaries, context flow, integrity checkpoints.

### Step 2: Design AIOA-Native Tasks

Every task embodies AIOA from the start — no separate checklist:

- **Task data** uses ADTO — typed + auditable (TIP-007)
- **Cross-component tasks** communicate via events, not direct calls (TIP-008)
- **Task boundaries** respect Pico/Nano/Micro levels (TIP-005)
- **No dead wrappers** in task implementation — call directly (TIP-004)
- **Retry/fallback/timeout** extracted into policies, not inline (TIP-006)
- **Task data** uses value objects, not primitives (TIP-002)
- **Context budget** max 7 files per task (TIP-003)

### Step 3: Decompose into Tasks

For each plan step, create tasks with AIOA annotations. Each task must reference AIOA.md for applicable TIPs.

Task annotation structure:
- Context budget (files to read/modify)
- AIOA TIPs applicable to this task
- Verification criteria

### Step 4: Order Tasks by Context Dependency

Group tasks sharing 50%+ of context files consecutively.

**Grouping Rules:**
1. Tasks sharing 50%+ context files should be consecutive
2. Tasks in same component boundary should be grouped
3. Tasks crossing multiple boundaries need context refresh before
4. Tasks with state tracking adjacent to their state changes

### Step 5: Generate AIOA-Native Tasks

Write each task using the AIOA task template. Tasks are AIOA-native — no separate compliance section needed.

---

## Task Generation Rules

### Rule 1: Context Budget Must Be Accurate
Every task must have a realistic context budget. 1-5 files acceptable; 6-7 consider splitting; 9+ split by architectural boundary.

### Rule 2: Tasks Are AIOA-Native
Each task embodies AIOA — no separate compliance validation.

### Rule 3: No Deployment Coupling
Tasks must not encode deployment assumptions (TIP-007: architectural independence).

### Rule 4: State Provenance Must Be Planned
Every stateful task needs TIP-007 (ADTO) provisions.

### Rule 5: Group Related Tasks
Tasks within same component should be sequential to minimize context reloading.

---

## Validation

- [ ] All tasks embody AIOA TIPs natively
- [ ] Every task has context budget
- [ ] Tasks ordered to minimize context reloading
- [ ] No violations documented
