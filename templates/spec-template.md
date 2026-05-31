# Specification: {{spec_title}}

> **AIOA Preset Active** — All specifications must include full AIOA compliance analysis (all 10 principles).
> Generated: {{date}}

---

## 1. Overview

### 1.1 Problem Statement
{{problem_statement}}

### 1.2 Proposed Solution
{{proposed_solution}}

### 1.3 Scope
{{scope}}

---

## 2. AIOA Compliance — Principle Assessments

### 2.1 P1: Local Reasoning Assessment

**Question:** *Can this feature be understood from local context alone?*

| Assessment | Value |
|------------|-------|
| **Files required to understand this spec** | {{local_reasoning_files}} |
| **Cross-module knowledge required** | {{local_reasoning_cross_module}} |
| **Local Reasoning verdict** | 🟢 Self-contained / 🟡 Some external context needed / 🔴 Requires extensive external context |

**Mitigation:**
- {{local_reasoning_mitigation_1}}
- {{local_reasoning_mitigation_2}}

### 2.2 P2: Crystallization Radius Impact Assessment

**Question:** *How much additional context must an AI agent consume to implement this specification safely?*

| Assessment | Value |
|------------|-------|
| **Files directly affected** | {{files_directly_affected}} |
| **Files requiring context** | {{files_requiring_context}} |
| **Cross-module dependencies** | {{cross_module_dependencies}} |
| **Crystallization Radius** | 🟢 Low / 🟡 Medium / 🔴 High |
| **Context surface area** | {{context_surface_area_description}} |

**Mitigation:**
- {{crystallization_radius_mitigation_1}}
- {{crystallization_radius_mitigation_2}}

### 2.3 P3: Semantic Integrity Requirements

**Question:** *What meaning must be preserved across which architectural boundaries?*

| Boundary | Data/Behavior | Integrity Requirement |
|----------|--------------|----------------------|
| {{boundary_1}} | {{data_behavior_1}} | {{integrity_requirement_1}} |
| {{boundary_2}} | {{data_behavior_2}} | {{integrity_requirement_2}} |

**Shared semantic contracts required:**
- {{semantic_contract_1}}
- {{semantic_contract_2}}

**Boundary validation strategy (TIP-007):** {{boundary_validation_strategy}}

### 2.4 P4: Boundaries Explicit Map

**Question:** *What component boundaries does this specification cross?*

| Boundary | Type | Responsibility | Interface |
|----------|------|----------------|-----------|
| {{boundary_name_1}} | {{boundary_type_1}} | {{boundary_responsibility_1}} | {{boundary_interface_1}} |
| {{boundary_name_2}} | {{boundary_type_2}} | {{boundary_responsibility_2}} | {{boundary_interface_2}} |

**Boundary verification:**
- [ ] Every boundary above has a declared name and responsibility
- [ ] Cross-boundary access occurs only through declared interfaces
- [ ] No implicit boundaries exist in this specification

### 2.5 P5: Contracts Deterministic Check

**Question:** *Are all interfaces in this specification machine-verifiable?*

| Interface | Schema/Type System | Runtime Verification | Contract Version |
|-----------|-------------------|---------------------|-----------------|
| {{interface_1}} | {{schema_1}} | {{verification_1}} | {{version_1}} |
| {{interface_2}} | {{schema_2}} | {{verification_2}} | {{version_2}} |

**Contract determinism verification:**
- [ ] Every interface has a machine-readable schema
- [ ] Schema validation is enforced at boundaries (TIP-007)
- [ ] Breaking changes require version bump
- [ ] Consumer-driven contracts are defined

### 2.6 P6: Control-Flow Complexity Check

**Question:** *Is the proposed design linear and declarative?*

| Aspect | Assessment |
|--------|------------|
| **Control flow depth** | {{control_flow_depth}} (acceptable / needs refactoring) |
| **Mutation state** | {{mutation_state}} (immutable / localized / scattered) |
| **Declarative ratio** | {{declarative_ratio}} (% declarative vs imperative) |

**Complexity mitigation:**
- {{complexity_mitigation_1}}
- {{complexity_mitigation_2}}

### 2.7 P7: Reasoning Boundaries not Deployment Check (Architectural Independence)

**Question:** *Does this specification assume a particular deployment topology?*

- [ ] No topology assumptions — Architecture is deployment-agnostic
- [ ] Topology assumption identified: {{topology_assumption}}
  - **Resolution:** {{topology_resolution}}

**Infrastructure dependencies extracted:**
- {{infrastructure_dependency_1}}
- {{infrastructure_dependency_2}}

**Boundary verification:**
- [ ] Component boundaries are semantic reasoning boundaries, not deployment boundaries
- [ ] Same components could be deployed as monolith, microservices, or serverless

### 2.8 P8: Extract Under Reuse Pressure Assessment

**Question:** *Are any abstractions in this specification premature?*

| Proposed Abstraction | Consumer Count | Justification | Verdict |
|---------------------|----------------|---------------|---------|
| {{abstraction_1}} | {{consumer_count_1}} | {{justification_1}} | 🟢 Justified / 🟡 Questionable / 🔴 Premature |
| {{abstraction_2}} | {{consumer_count_2}} | {{justification_2}} | 🟢 Justified / 🟡 Questionable / 🔴 Premature |

**Rule:** No abstraction SHALL be created with fewer than 2 confirmed consumers unless explicitly justified.

### 2.9 P9: Event Boundaries Plan

**Question:** *How does cross-component communication happen?*

| Communication Path | Method (Event/Direct) | Rationale |
|--------------------|----------------------|-----------|
| {{path_1}} | {{method_1}} | {{rationale_1}} |
| {{path_2}} | {{method_2}} | {{rationale_2}} |

**Event-driven integration check (TIP-008):**
- [ ] Cross-component communication uses event bus where feasible
- [ ] Direct synchronous calls are exceptions with documented rationale
- [ ] Event schemas are versioned and shared
- [ ] Event handlers are idempotent

### 2.10 P10: Runtime State Explainability Plan

**Question:** *Can runtime state be explained and audited?*

| State | Location | Provenance Tracking | Inspectable? |
|-------|----------|---------------------|-------------|
| {{state_1}} | {{location_1}} | {{provenance_1}} | 🟢 Yes / 🔴 No |
| {{state_2}} | {{location_2}} | {{provenance_2}} | 🟢 Yes / 🔴 No |

**ADTO compliance (TIP-009):**
- [ ] All DTOs carry `_provenance` field with version, timestamp, origin
- [ ] State mutations are logged with provenance records
- [ ] State is inspectable without side effects
- [ ] Immutable event sourcing considered where applicable

---

## 3. Context Budget

### 3.1 Context Requirements by Agent Role

| Agent Role | Context Required | Estimated Budget |
|------------|-----------------|------------------|
| Specifying Agent | {{specifying_context}} | {{specifying_budget}} |
| Planning Agent | {{planning_context}} | {{planning_budget}} |
| Implementation Agent | {{implementation_context}} | {{implementation_budget}} |
| Review Agent | {{review_context}} | {{review_budget}} |

### 3.2 External Dependencies

| Dependency | Version | Context Impact |
|------------|---------|----------------|
| {{dependency_1}} | {{version_1}} | {{impact_1}} |
| {{dependency_2}} | {{version_2}} | {{impact_2}} |

---

## 4. Technical Design

### 4.1 Architecture Overview

{{architecture_overview}}

### 4.2 Component Diagram

```
{{component_diagram}}
```

### 4.3 Data Flow

{{data_flow_description}}

### 4.4 Interfaces

| Interface | Provider | Consumer | Contract |
|-----------|----------|----------|----------|
| {{interface_1}} | {{provider_1}} | {{consumer_1}} | {{contract_1}} |
| {{interface_2}} | {{provider_2}} | {{consumer_2}} | {{contract_2}} |

---

## 5. Semantic Contracts

### 5.1 Shared Types

```typescript
// {{shared_type_1}}
{{shared_type_definition_1}}

// {{shared_type_2}}
{{shared_type_definition_2}}
```

### 5.2 Invariants

- {{invariant_1}}
- {{invariant_2}}

---

## 6. Context Flow Optimization

### 6.1 Current Context Flow

{{current_context_flow}}

### 6.2 Optimizations Applied

| Optimization | Impact on Crystallization Radius |
|-------------|----------------------------------|
| {{optimization_1}} | {{radius_impact_1}} |
| {{optimization_2}} | {{radius_impact_2}} |

---

## 7. Decision Log

| Decision | Rationale | AIOA Principle Applied |
|----------|-----------|------------------------|
| {{decision_1}} | {{rationale_1}} | {{principle_1}} |
| {{decision_2}} | {{rationale_2}} | {{principle_2}} |

---

## 8. Review Checklist

### 8.1 All 10 Principles Checked

- [ ] **P1 Local Reasoning** — Feature is understandable from local context
- [ ] **P2 Crystallization Radius** — Radius is documented and within acceptable range
- [ ] **P3 Semantic Integrity** — Integrity requirements are defined for all boundaries
- [ ] **P4 Boundaries Explicit** — All component boundaries are declared
- [ ] **P5 Contracts Deterministic** — All interfaces have machine-verifiable contracts
- [ ] **P6 Declarative Straight-Line** — Design is linear and declarative
- [ ] **P7 Reasoning Boundaries not Deployment** — No topology assumptions
- [ ] **P8 Extract Under Reuse Pressure** — No premature abstractions
- [ ] **P9 Event Boundaries** — Cross-component communication is event-driven
- [ ] **P10 Runtime State Explainable** — State is auditable and inspectable

### 8.2 Standard Checks

- [ ] Context budget is estimated for each agent role
- [ ] External dependencies are assessed for context impact
- [ ] Component boundaries are explicitly defined
- [ ] Shared semantic contracts are versioned
- [ ] Data flows are documented with transformation points highlighted
