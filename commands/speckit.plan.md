---
description: "Plan command with Architecture Decision Records and principle checks"
scripts:
  - specify plan
---

# speckit.plan — AIOA-Enhanced Plan Command

**Preset:** aioa (version 1.0.0)

---

## Workflow

### Step 1: Load Specification with AIOA Context

Read the spec and extract: all 10 principle assessments, Crystallization Radius impact, Semantic Integrity requirements, boundary map, communication patterns, runtime state plans.

**Validate:** All AIOA sections present. If missing, run `speckit.specify` first.

### Step 2: Create Architecture Decision Records

For each significant architectural decision, document an ADR with analysis of all relevant AIOA principles:

```
# ADR-{N}: {Title}
## Status
[Proposed | Accepted | Deprecated | Superseded]
## Context
What is the architectural context? What alternatives? What forces?
## Decision
What was decided and why?
## Consequences
- Positive: Benefits
- Negative: Trade-offs

## P1 — Local Reasoning Analysis
Can this be understood from local context? What external context is required?

## P2 — Crystallization Radius Analysis
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Context files | {n} | {n} | {+/-n} |
| Cross-module deps | {n} | {n} | {+/-n} |
| Rating | {rating} | {rating} | {direction} |

## P3 — Semantic Integrity Impact
Does this affect boundary contracts? Shared types? Transformations?

## P4 — Boundaries Explicit Check
- [ ] All affected boundaries declared
- [ ] No implicit boundaries introduced

## P5 — Contracts Deterministic Check
- [ ] Interfaces have machine-verifiable schemas (TIP-007)

## P6 — Control-Flow Simplicity Check
- [ ] Design is linear and declarative
- [ ] No deeply nested control flow

## P7 — Reasoning Boundaries vs Deployment Check
- [ ] No topology assumptions introduced
- [ ] Infrastructure concerns isolated
- [ ] Interfaces remain deployment-agnostic

## P8 — Extract Under Reuse Pressure Check
- [ ] New abstractions have ≥2 consumers
- [ ] No speculative abstractions

## P9 — Event Boundaries Check
- [ ] Cross-component comms uses event bus (TIP-008)
- [ ] Direct calls are exceptions with rationale

## P10 — Runtime State Explainability Check
- [ ] State mutations have provenance tracking
- [ ] ADTO pattern followed (TIP-009)
```

**Validation Rules:**
- ADR with HIGH `After` Crystallization Radius requires architecture review approval
- Any radius increase must have explicit justification
- Semantic Integrity impact documented for every boundary touched
- All applicable principles must have an entry

### Step 3: Define Component Boundaries

For each component:

```
## Component: {name}
- Responsibility: {what does it own?}
- Crystallization Radius: {LOW | MEDIUM | HIGH}
- Context budget: {n files}
- Dependencies: {list}
- Published interfaces: {list}
- Consumed interfaces: {list}
- Boundary contract: {shared types, invariants}
- Boundary explicit: {YES | NO}
- Contract deterministic: {YES | NO}
- Runtime state: {explainability plan}
```

**Validation:**
- HIGH Crystallization Radius components need refactoring plan
- Every dependency must have explicit interface
- No circular dependencies
- Every boundary explicitly declared
- Every interface machine-verifiable

### Step 4: Map Context Flow

Show how context flows through the system:
```
External Input → Component A ──→ Component B
                         ↓
                    Component C ──→ External Output
```
For each flow: identify Crystallization Radius accumulation, flag hotspots, document optimization opportunities, label communication as event-driven or direct, mark state tracking points.

### Step 5: Establish Semantic Integrity Checkpoints

For each architectural boundary, define verification gates:

```
## Checkpoint: {name}
- Location: {where in workflow}
- Verification: {automated/review/test checks}
- Failure action: {what happens if integrity violated}
```

**Standard Checkpoints:**

| Checkpoint | When | What It Verifies |
|------------|------|------------------|
| **Input Parsing** | External boundary | Data parsed into trusted types (TIP-007) |
| **Cross-Component** | Component interface | Shared types used, no silent transformations |
| **Output Serialization** | External boundary | Internal ↔ external mapping correct |
| **State Mutation** | On state change | Provenance recorded (TIP-009) |
| **Event Publish** | On event emission | Event schema valid, idempotent |

### Step 6: Generate AIOA-Compliant Plan

Write the plan using the AIOA plan template, including: ADRs with all 10 principle analyses, component boundaries with context budgets, context flow diagrams, Semantic Integrity checkpoints, runtime state explainability plan, risk assessment, principle compliance summary.

### TIP-008: Event-Driven Integration Analysis

For each component interaction:
1. **Coupling type:** Synchronous (direct) or asynchronous (event)?
2. **Reasoning locality:** Does a component need another's internals?
3. **Event boundaries:** Can interaction become event-driven?

**Event Contract Requirements:**
- Events must be immutable and versioned
- Events describe business facts, not implementation details
- Handlers focus on local responsibilities
- Producers must not depend on consumers

---

## Plan Validation Checklist

- [ ] **P1:** Every step understandable from local context
- [ ] **P2:** Every component has documented Crystallization Radius
- [ ] **P3:** Every boundary has semantic contract with checkpoints
- [ ] **P4:** Every boundary declared (name, responsibility, interface)
- [ ] **P5:** Every interface has machine-verifiable schema (TIP-007)
- [ ] **P6:** Design is linear and declarative
- [ ] **P7:** All dependencies are interface-based
- [ ] **P8:** No premature abstractions
- [ ] **P9:** Cross-component comms uses event bus where feasible (TIP-008)
- [ ] **P10:** State is inspectable with provenance tracking (TIP-009)

---

## Prompt Templates

### ADR Creation Prompt
```
Document ADR for [DECISION]. Apply all applicable AIOA principles:
1. P1: Can this be understood locally?
2. P2: How does this affect Crystallization Radius?
3. P3: What semantic boundaries does it touch?
4. P4: Any new boundaries created?
5. P5: Are interfaces machine-verifiable?
6. P6: Is design linear and declarative?
7. P7: Does this lock us into a deployment topology?
8. P8: Any premature abstractions?
9. P9: Should this use event-driven communication?
10. P10: Is runtime state explainable?
```

### Component Boundary Prompt
```
Define boundary for [COMPONENT]:
1. Sole responsibility?
2. Context needed to work safely? (P2)
3. Interfaces published/consumed? (P4, P5)
4. Shared types governing boundaries? (P3)
5. Communication with other components? (P9)
6. Runtime state explainable? (P10)
```

### Context Flow Analysis Prompt
```
Analyze context flow for [FEATURE]:
1. Where does context enter the system?
2. Where does it accumulate (hotspots)?
3. How many files must an agent read at each step?
4. Can context flow be simplified?
5. Which paths are event-driven vs direct calls?
6. Where is state tracked and is it explainable?
```

### Runtime State Explainability Prompt
```
Plan runtime state explainability for [FEATURE]:
For each stateful component:
1. What state does it maintain?
2. How are mutations audited?
3. Can state be inspected without side effects?
4. Do DTOs carry _provenance fields? (TIP-009: ADTO)
5. Is event sourcing applicable?
```
