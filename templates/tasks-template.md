# Task: {{task_title}}

> **AIOA Preset Active** — This task includes full AIOA principle verification (all 10 principles).
> Generated: {{date}}

---

## 1. Task Overview

### 1.1 Description
{{task_description}}

### 1.2 Acceptance Criteria
- {{acceptance_criterion_1}}
- {{acceptance_criterion_2}}

### 1.3 AIOA Context Budget

| Context Item | Details |
|-------------|---------|
| **Files to read** | {{files_to_read}} |
| **Files to modify** | {{files_to_modify}} |
| **Cross-module context needed** | {{cross_module_context}} |
| **Context budget** | {{context_budget}} (Low / Medium / High) |

---

## 2. AIOA Principle Checks

### 2.1 P1: Local Reasoning Check

- [ ] Task can be understood from local context alone
- [ ] All external context requirements are explicitly documented
- [ ] No global state or ambient conventions required for understanding

### 2.2 P2: Crystallization Radius Verification

**Pre-Implementation Check:**
- [ ] Agent has loaded all context files listed above ({{context_budget}} items)
- [ ] All implicit dependencies are identified and understood
- [ ] The Crystallization Radius of the affected component(s) is known
- [ ] This task does NOT expand the Crystallization Radius beyond the current component boundaries

**Radius Impact Analysis:**

**Current Crystallization Radius:** {{current_radius}}
**Expected after change:** {{expected_radius}}
**Delta:** {{radius_delta}}

**If expanding:** {{radius_expansion_rationale}}

**Context Surface Map:**

```
{{context_surface_map}}
```

### 2.3 P3: Semantic Integrity Validation

**Boundaries Crossed:**

| Boundary | Direction | Data/Behavior Crossing | Integrity Risk |
|----------|-----------|----------------------|----------------|
| {{boundary_1}} | {{direction_1}} | {{data_1}} | {{risk_1}} |
| {{boundary_2}} | {{direction_2}} | {{data_2}} | {{risk_2}} |

**Integrity Gates:**

**Gate 1 — Shared Types Consistent:**
- [ ] All shared types used at boundaries are the correct version
- [ ] No type casting or transformation without explicit contract
- [ ] Boundary parsing is validated

**Gate 2 — Parse Don't Validate (TIP-007):**
- [ ] External data is parsed into trusted types at the boundary
- [ ] Internal logic operates on trusted types only
- [ ] No defensive checks in core logic for data that has already been parsed

**Gate 3 — No Silent Transformations:**
- [ ] Every data transformation at a boundary is explicit
- [ ] Transformation logic is governed by a semantic contract
- [ ] Transformations are tested for meaning preservation

### 2.4 P4: Boundaries Explicit Check

- [ ] Every boundary crossed is explicitly declared
- [ ] Cross-boundary access occurs only through declared interfaces
- [ ] No implicit boundaries are crossed
- [ ] Component responsibilities are respected

### 2.5 P5: Contracts Deterministic Check

- [ ] All interfaces in this task have machine-verifiable schemas
- [ ] Schema validation is enforced at boundaries
- [ ] Breaking changes to contracts require version bump
- [ ] Consumer-driven contracts are satisfied

### 2.6 P6: Control-Flow Complexity Check

- [ ] Code is linear and declarative where possible
- [ ] No deeply nested conditionals (depth > 3)
- [ ] Mutable state is localized and minimized
- [ ] Complex control flow is replaced with declarative operations

### 2.7 P7: Reasoning Boundaries not Deployment Check

- [ ] No infrastructure dependencies in core logic
- [ ] All interfaces remain deployment-agnostic
- [ ] No topology assumptions in implementation
- [ ] Infrastructure concerns isolated to deployment boundary

### 2.8 P8: Extract Under Reuse Pressure Check

- [ ] Any new abstractions have sufficient reuse pressure (≥2 consumers)
- [ ] No speculative abstractions introduced
- [ ] Existing abstractions are justified

### 2.9 P9: Event Boundaries Check

- [ ] Cross-component communication uses event bus where feasible (TIP-008)
- [ ] Direct synchronous calls are exceptions with documented rationale
- [ ] Event schemas are versioned and shared
- [ ] Event handlers are idempotent

### 2.10 P10: Runtime State Explainability Check

- [ ] State mutations have provenance records (who, what, when, why)
- [ ] State is inspectable without side effects
- [ ] ADTO pattern followed: DTOs carry `_provenance` field (TIP-009)
- [ ] Immutable event sourcing considered

---

## 3. Implementation Steps

### Step 1: {{implementation_step_1}}
- {{detail_1}}
- {{detail_2}}
- **AIOA check:** {{aioa_check_1}}

### Step 2: {{implementation_step_2}}
- {{detail_1}}
- {{detail_2}}
- **AIOA check:** {{aioa_check_2}}

### Step 3: {{implementation_step_3}}
- {{detail_1}}
- {{detail_2}}
- **AIOA check:** {{aioa_check_3}}

---

## 4. Verification

### 4.1 AIOA Compliance Checklist

**P1 Local Reasoning:**
- [ ] Task is understandable from local context
- [ ] External context requirements are documented

**P2 Crystallization Radius:**
- [ ] Crystallization Radius did not regress
- [ ] Context budget annotations are accurate
- [ ] No new implicit dependencies introduced
- [ ] Change is self-contained within its context budget

**P3 Semantic Integrity:**
- [ ] Shared types are used consistently across boundaries
- [ ] Boundary parsing follows the "Parse, Don't Validate" pattern (TIP-007)
- [ ] No silent data transformations introduced
- [ ] Semantic contracts are versioned and compatible

**P4 Boundaries Explicit:**
- [ ] All boundaries are explicitly declared
- [ ] No boundary violations introduced

**P5 Contracts Deterministic:**
- [ ] All interfaces have machine-verifiable schemas
- [ ] Schema validation is enforced

**P6 Declarative Straight-Line:**
- [ ] Code is linear and declarative
- [ ] No complex control flow introduced

**P7 Reasoning Boundaries not Deployment:**
- [ ] No infrastructure dependencies leaked into core logic
- [ ] Component interfaces remain deployment-agnostic
- [ ] No topology assumptions encoded in implementation

**P8 Extract Under Reuse Pressure:**
- [ ] No premature abstractions
- [ ] Shared code extracted based on reuse pressure only

**P9 Event Boundaries:**
- [ ] Cross-component communication is event-driven
- [ ] Direct calls are justified exceptions

**P10 Runtime State Explainable:**
- [ ] State is auditable with provenance records
- [ ] ADTO pattern is followed

### 4.2 Test Criteria
- {{test_criterion_1}}
- {{test_criterion_2}}
- {{test_criterion_3}}

---

## 5. Post-Completion

### 5.1 Context Budget Update
- [ ] Context budget documentation updated (if changed)
- [ ] Crystallization Radius re-evaluated and documented

### 5.2 Semantic Integrity Sign-off
- [ ] All integrity gates passed
- [ ] Semantic contracts are satisfied

### 5.3 Principle Compliance Sign-off
- [ ] All 10 AIOA principles verified
- [ ] Any principle violations documented and addressed

---

## 6. Dependencies

### 6.1 Required Context
- {{required_context_1}}
- {{required_context_2}}

### 6.2 Prerequisite Tasks
- {{prerequisite_1}}
- {{prerequisite_2}}

### 6.3 Blocked By
- {{blocked_by}}
