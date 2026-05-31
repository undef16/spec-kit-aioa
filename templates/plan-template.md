# Plan: {{plan_title}}

> **AIOA Preset Active** — All plan steps include full AIOA principle analysis (all 10 principles).
> Generated: {{date}}

---

## 1. Plan Overview

### 1.1 Goal
{{plan_goal}}

### 1.2 Success Criteria
- {{success_criterion_1}}
- {{success_criterion_2}}

### 1.3 Architecture Context

```
{{architecture_context_diagram}}
```

---

## 2. Architecture Decision Records

### ADR-{{number}}: {{decision_title}}

**Status:** {{status}} (Proposed / Accepted / Deprecated / Superseded)

**Context:**
{{context}}

**Decision:**
{{decision}}

**Consequences:**
- Positive: {{positive_consequence}}
- Negative: {{negative_consequence}}

**P1 — Local Reasoning Analysis:**
- Can this decision be understood from local context? {{local_reasoning_verdict}}
- External context required: {{local_reasoning_external_context}}
- Mitigation: {{local_reasoning_mitigation}}

**P2 — Crystallization Radius Analysis:**

| Metric | Before ADR | After ADR | Delta |
|--------|-----------|-----------|-------|
| Context files needed | {{before_files}} | {{after_files}} | {{delta_files}} |
| Cross-module deps | {{before_deps}} | {{after_deps}} | {{delta_deps}} |
| Surface area rating | {{before_rating}} | {{after_rating}} | {{delta_rating}} |

**P3 — Semantic Integrity Impact:**
- {{semantic_integrity_impact}}

**P4 — Boundaries Explicit Check:**
- [ ] All component boundaries affected are declared
- [ ] No implicit boundaries introduced
- [ ] Cross-boundary access is through declared interfaces

**P5 — Contracts Deterministic Check:**
- [ ] Interfaces affected have machine-verifiable schemas
- [ ] Schema validation enforced at boundaries (TIP-007)
- [ ] Contract versioning strategy documented

**P6 — Control-Flow Simplicity Check:**
- [ ] Design is linear and declarative
- [ ] No deeply nested control flow introduced
- [ ] Mutable state is localized and minimized

**P7 — Reasoning Boundaries not Deployment Check (Architectural Independence):**
- [ ] No topology assumptions introduced
- [ ] Infrastructure concerns isolated to boundary
- [ ] Interfaces remain deployment-agnostic

**P8 — Extract Under Reuse Pressure Check:**
- [ ] Any new abstractions have ≥2 confirmed consumers
- [ ] No speculative abstractions introduced
- [ ] Premature abstractions flagged and inlined

**P9 — Event Boundaries Check:**
- [ ] Cross-component communication uses event bus where feasible
- [ ] Direct synchronous calls are exceptions (TIP-008)
- [ ] Event schemas are versioned and shared

**P10 — Runtime State Explainability Check:**
- [ ] State mutations have provenance tracking
- [ ] State is inspectable without side effects
- [ ] ADTO pattern followed for DTOs (TIP-009)

---

## 3. Component Boundaries

### 3.1 Boundary Map

```
{{boundary_map_diagram}}
```

### 3.2 Component Definitions

| Component | Responsibility | Crystallization Radius | Dependencies | Boundary Explicit? |
|-----------|--------------|------------------------|--------------|-------------------|
| {{component_1}} | {{responsibility_1}} | {{radius_1}} | {{dependencies_1}} | 🟢 Yes / 🔴 No |
| {{component_2}} | {{responsibility_2}} | {{radius_2}} | {{dependencies_2}} | 🟢 Yes / 🔴 No |
| {{component_3}} | {{responsibility_3}} | {{radius_3}} | {{dependencies_3}} | 🟢 Yes / 🔴 No |

### 3.3 Boundary Contracts

| Boundary | Interface | Semantic Contract | Context Cost | Contract Deterministic? |
|----------|-----------|-------------------|--------------|------------------------|
| {{boundary_a}} | {{interface_a}} | {{contract_a}} | {{cost_a}} | 🟢 Yes / 🔴 No |
| {{boundary_b}} | {{interface_b}} | {{contract_b}} | {{cost_b}} | 🟢 Yes / 🔴 No |

---

## 4. Context Flow Diagram

### 4.1 Data/Control Flow

```
{{context_flow_diagram}}
```

### 4.2 Context Flow Description

{{context_flow_description}}

### 4.3 Hot Paths (High-Context Flows)

| Flow | Context Cost | Optimization Opportunity |
|------|-------------|------------------------|
| {{flow_1}} | {{cost_1}} | {{optimization_1}} |
| {{flow_2}} | {{cost_2}} | {{optimization_2}} |

---

## 5. Steps

### Step {{step_number}}: {{step_title}}

**Estimated effort:** {{effort}}

**Context budget for implementation agent:** {{context_budget}}

**Dependencies:**
- {{dependency_1}}
- {{dependency_2}}

**AIOA Principle Checks — Pre-Implementation:**

**P1 — Local Reasoning:**
- [ ] Agent can understand this step from local context alone
- [ ] All external context requirements are documented

**P2 — Crystallization Radius check before implementation:**
- [ ] Agent has reviewed context budget ({{context_budget}} files)
- [ ] All cross-module dependencies are explicitly documented
- [ ] No implicit context exists (global state, ambient conventions)

**P3 — Semantic Integrity checkpoint:**
- [ ] Shared types are used consistently
- [ ] Boundary parsing follows "Parse, Don't Validate" (TIP-007)
- [ ] No silent transformations exist

**P4 — Boundaries Explicit:**
- [ ] All boundaries crossed in this step are declared
- [ ] Access occurs through declared interfaces only

**P5 — Contracts Deterministic:**
- [ ] All interfaces in this step have machine-verifiable schemas
- [ ] Schema validation is enforced at boundaries

**P6 — Declarative Straight-Line:**
- [ ] Code in this step is linear and declarative
- [ ] No deeply nested control flow

**P7 — Reasoning Boundaries not Deployment:**
- [ ] No deployment topology assumptions in implementation
- [ ] Infrastructure concerns isolated to boundary

**P8 — Extract Under Reuse Pressure:**
- [ ] Any abstractions extracted have sufficient reuse demand
- [ ] No speculative abstractions

**P9 — Event Boundaries:**
- [ ] Cross-component communication is event-driven (TIP-008)
- [ ] Direct calls are exceptions with rationale

**P10 — Runtime State Explainable:**
- [ ] State changes have provenance records
- [ ] ADTO pattern followed (TIP-009)

**Implementation details:**
{{implementation_details}}

**Validation criteria:**
- {{validation_1}}
- {{validation_2}}

---

## 6. Semantic Integrity Checkpoints

### Checkpoint 1: {{checkpoint_title_1}}

**Location in workflow:** {{workflow_location_1}}

**Verification:**
- {{verification_1}}
- {{verification_2}}

**Failure action:** {{failure_action_1}}

### Checkpoint 2: {{checkpoint_title_2}}

**Location in workflow:** {{workflow_location_2}}

**Verification:**
- {{verification_1}}
- {{verification_2}}

**Failure action:** {{failure_action_2}}

---

## 7. Risk Assessment

### 7.1 Crystallization Radius Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {{risk_1}} | {{likelihood_1}} | {{impact_1}} | {{mitigation_1}} |
| {{risk_2}} | {{likelihood_2}} | {{impact_2}} | {{mitigation_2}} |

### 7.2 Semantic Integrity Risks

| Risk | Boundary Affected | Detection Strategy |
|------|------------------|-------------------|
| {{risk_1}} | {{boundary_1}} | {{detection_1}} |
| {{risk_2}} | {{boundary_2}} | {{detection_2}} |

### 7.3 Other Principle Risks

| Risk | Principle | Impact | Mitigation |
|------|-----------|--------|------------|
| {{risk_1}} | P{{principle_number_1}} | {{impact_1}} | {{mitigation_1}} |
| {{risk_2}} | P{{principle_number_2}} | {{impact_2}} | {{mitigation_2}} |

---

## 8. Architecture Independence Verification (P7)

- [ ] All component dependencies are interface-based, not infrastructure-based
- [ ] No deployment topology assumed in any component design
- [ ] Network boundaries are not encoded in component interfaces
- [ ] All infrastructure concerns are configurable at deployment boundary

---

## 9. Plan Validation

### Prerequisites
- {{prerequisite_1}}
- {{prerequisite_2}}

### Post-conditions
- {{post_condition_1}}
- {{post_condition_2}}

### Rollback strategy
{{rollback_strategy}}

### AIOA Principle Compliance Summary

| Principle | Status | Notes |
|-----------|--------|-------|
| P1 Local Reasoning | 🟢 / 🟡 / 🔴 | {{p1_notes}} |
| P2 Crystallization Radius | 🟢 / 🟡 / 🔴 | {{p2_notes}} |
| P3 Semantic Integrity | 🟢 / 🟡 / 🔴 | {{p3_notes}} |
| P4 Boundaries Explicit | 🟢 / 🟡 / 🔴 | {{p4_notes}} |
| P5 Contracts Deterministic | 🟢 / 🟡 / 🔴 | {{p5_notes}} |
| P6 Declarative Straight-Line | 🟢 / 🟡 / 🔴 | {{p6_notes}} |
| P7 Reasoning Boundaries vs Deployment | 🟢 / 🟡 / 🔴 | {{p7_notes}} |
| P8 Extract Under Reuse Pressure | 🟢 / 🟡 / 🔴 | {{p8_notes}} |
| P9 Event Boundaries | 🟢 / 🟡 / 🔴 | {{p9_notes}} |
| P10 Runtime State Explainable | 🟢 / 🟡 / 🔴 | {{p10_notes}} |
