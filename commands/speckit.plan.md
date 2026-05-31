---
description: "Plan command with Architecture Decision Records and principle checks"
scripts:
  - specify plan
---

# speckit.plan — AIOA-Enhanced Plan Command

**Preset:** aioa (version 1.0.0)

This command overrides the standard `specify plan` flow to enforce all 10 AIOA principles during planning, including Architecture Decision Records with full principle analysis.

---

## Overview

When invoked, this command:
1. Enforces Architecture Decision Records (ADRs) for every significant design choice
2. Validates all 10 AIOA principles in design decisions
3. Creates ADR entries for every principle affected
4. Generates principle compliance summary for the plan

---

## Workflow

### Step 1: Load Specification with AIOA Context

Read the specification and extract:
- All 10 principle assessments from the spec
- Crystallization Radius impact assessment
- Semantic Integrity requirements
- Boundary map
- Communication patterns
- Runtime state plans

**Validate:** All AIOA sections from the spec are present. If not, run `speckit.specify` first.

### Step 2: Create Architecture Decision Records

For each significant architectural decision in the plan:

> **Document an ADR with analysis of all relevant AIOA principles.**

**ADR Structure:**

```
# ADR-{N}: {Title}

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the architectural context for this decision?
What alternatives were considered?
What forces are at play?

## Decision
What was decided and why?

## Consequences
- Positive: What benefits does this bring?
- Negative: What trade-offs are accepted?

## P1 — Local Reasoning Analysis
Can this decision be understood from local context?
What external context is required?

## P2 — Crystallization Radius Analysis
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Context files | {n} | {n} | {+/-n} |
| Cross-module deps | {n} | {n} | {+/-n} |
| Rating | {rating} | {rating} | {direction} |

## P3 — Semantic Integrity Impact
Does this decision affect any boundary contracts?
What shared types are impacted?
Are there any transformation concerns?

## P4 — Boundaries Explicit Check
- [ ] All affected boundaries are declared
- [ ] No implicit boundaries introduced

## P5 — Contracts Deterministic Check
- [ ] Interfaces affected have machine-verifiable schemas
- [ ] Schema validation enforced at boundaries (TIP-007)

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
- [ ] Cross-component communication uses event bus (TIP-008)
- [ ] Direct calls are exceptions with rationale

## P10 — Runtime State Explainability Check
- [ ] State mutations have provenance tracking
- [ ] ADTO pattern followed (TIP-009)
```

**Validation Rules:**
- Every ADR where `After` Crystallization Radius is HIGH requires architecture review approval
- Any increase in Crystallization Radius must have an explicit justification
- Semantic Integrity impact must be documented for every boundary touched
- All applicable principles must have an entry in each ADR

### Step 3: Define Component Boundaries

For each component identified:

> **Document its boundaries, context cost, and AIOA principle compliance.**

**Component Boundary Entry:**

```
## Component: {name}
- Responsibility: {what does it own?}
- Crystallization Radius: {LOW | MEDIUM | HIGH}
- Context budget: {n files}
- Dependencies: {list of dependents}
- Published interfaces: {list}
- Consumed interfaces: {list}
- Boundary contract: {shared types, invariants}
- Boundary explicit: {YES | NO}
- Contract deterministic: {YES | NO}
- Runtime state: {explainability plan}
```

**Validation Rules:**
- Components with HIGH Crystallization Radius must have a refactoring plan
- Every dependency must have an explicit interface
- No circular dependencies between components
- Every boundary must be explicitly declared
- Every interface must have a machine-verifiable contract

### Step 4: Map Context Flow

Generate a context flow description showing:

> **How does context flow through the system?**

```
External Input → Boundary Parser → Component A ──→ Component B
                                      ↓
                                 Component C ──→ Boundary Serializer → External Output
```

For each flow:
- Identify where Crystallization Radius accumulates
- Flag context hotspots (areas requiring many files to understand)
- Document optimization opportunities
- Label each communication path as event-driven or direct call
- Mark state tracking points for explainability

### Step 5: Establish Semantic Integrity Checkpoints

For each architectural boundary:

> **Define verification gates that ensure meaning is preserved.**

**Checkpoint Structure:**

```
## Checkpoint: {name}
- Location: {where in the workflow}
- Verification:
  1. {automated check}
  2. {review check}
  3. {test check}
- Failure action: {what happens if integrity is violated}
```

**Standard Checkpoints:**

| Checkpoint | When | What It Verifies |
|------------|------|------------------|
| **Input Parsing** | At external boundary | Data parsed into trusted types (TIP-007) |
| **Cross-Component** | At component interface | Shared types used, no silent transformations |
| **Output Serialization** | At external boundary | Internal types mapped correctly to external representation |
| **State Mutation** | On state change | Provenance recorded (TIP-009) |
| **Event Publish** | On event emission | Event schema valid, idempotent |

### Step 6: Generate AIOA-Compliant Plan

Write the plan using the AIOA plan template with all sections populated.

**The plan includes:**
- ADRs with all 10 AIOA principle analyses
- Component boundary definitions with context budgets
- Context flow diagrams with communication pattern labels
- Semantic Integrity checkpoints
- Runtime state explainability plan
- Risk assessment for all principles
- Principle compliance summary matrix

### TIP-008: Event-Driven Integration Analysis

For each component interaction in the plan, assess:

1. **Coupling type**: Is the interaction synchronous (direct call) or asynchronous (event)?
2. **Reasoning locality**: Does the component need to understand another component's internals?
3. **Event boundaries**: Can the interaction be replaced with an event-driven pattern?

Prefer event boundaries when they reduce reasoning complexity without violating business requirements.

#### Event Contract Requirements
- Events must be immutable and versioned
- Events must describe business facts, not implementation details
- Handlers must focus on local responsibilities
- Producers must not depend on consumers

---

## Plan Validation Checklist

Before finalizing the plan, run these checks:

### All 10 Principles

- [ ] **P1 — Local Reasoning:** Every step is understandable from local context
- [ ] **P2 — Crystallization Radius:** Every component has a documented Crystallization Radius
- [ ] **P3 — Semantic Integrity:** Every boundary has a semantic contract with checkpoints
- [ ] **P4 — Boundaries Explicit:** Every boundary is declared with name, responsibility, interface
- [ ] **P5 — Contracts Deterministic:** Every interface has a machine-verifiable schema (TIP-007)
- [ ] **P6 — Declarative Straight-Line:** Design is linear and declarative
- [ ] **P7 — Reasoning Boundaries not Deployment:** All component dependencies are interface-based
- [ ] **P8 — Extract Under Reuse Pressure:** No premature abstractions
- [ ] **P9 — Event Boundaries:** Cross-component communication uses event bus where feasible (TIP-008)
- [ ] **P10 — Runtime State Explainable:** State is inspectable with provenance tracking (TIP-009)

---

## Prompt Templates

### ADR Creation Prompt

```
Document an Architecture Decision Record for [DECISION].

Apply all applicable AIOA principles:
1. P1: Can this be understood locally?
2. P2: How does this affect Crystallization Radius?
3. P3: What semantic boundaries does it touch?
4. P4: Are any new boundaries created?
5. P5: Are all interfaces machine-verifiable?
6. P6: Is the design linear and declarative?
7. P7: Could this decision lock us into a deployment topology?
8. P8: Are any abstractions premature?
9. P9: Should this use event-driven communication?
10. P10: Is runtime state explainable?
```

### Component Boundary Prompt

```
Define the boundary for [COMPONENT].

Questions to answer:
1. What is this component's sole responsibility?
2. What context does an agent need to work on it safely? (P2)
3. What interfaces does it publish and consume? (P4, P5)
4. What shared types govern its boundaries? (P3)
5. How does it communicate with other components? (P9)
6. Is its runtime state explainable? (P10)
```

### Context Flow Analysis Prompt

```
Analyze the context flow for [FEATURE].

Identify:
1. Where does context enter the system?
2. Where does context accumulate (hotspots)?
3. How many files must an agent read at each step?
4. Can context flow be simplified?
5. Which paths are event-driven vs direct calls?
6. Where is state tracked and is it explainable?
```

### Runtime State Explainability Prompt

```
Plan runtime state explainability for [FEATURE].

For each stateful component:
1. What state does it maintain?
2. How are state mutations audited?
3. Can state be inspected without side effects?
4. Do DTOs carry _provenance fields? (TIP-009: ADTO)
5. Is event sourcing applicable?
```
