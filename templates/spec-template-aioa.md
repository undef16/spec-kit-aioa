---
# AIOA Additions — Appended after core spec-template.md
# This file contains ONLY AIOA-specific sections that are appended to the core Spec Kit spec template.
---

> **AIOA Preset Active** — All specifications must include full AIOA compliance analysis (all 10 principles).

## AIOA Compliance — Principle Assessments

### P1: Local Reasoning
| Assessment | Value |
| Files required | {{local_reasoning_files}} |
| Cross-module knowledge | {{local_reasoning_cross_module}} |
| Verdict | 🟢 Self-contained / 🟡 Some external context / 🔴 Extensive external context |
| Mitigation | {{local_reasoning_mitigation_1}}; {{local_reasoning_mitigation_2}} |

### P2: Crystallization Radius Impact
| Assessment | Value |
| Files directly affected | {{files_directly_affected}} |
| Files requiring context | {{files_requiring_context}} |
| Cross-module deps | {{cross_module_dependencies}} |
| Radius | 🟢 Low / 🟡 Medium / 🔴 High |
| Surface area | {{context_surface_area_description}} |
| Mitigation | {{crystallization_radius_mitigation_1}}; {{crystallization_radius_mitigation_2}} |

### P3: Semantic Integrity
| Boundary | Data/Behavior | Integrity Requirement |
| {{boundary_1}} | {{data_behavior_1}} | {{integrity_requirement_1}} |
| {{boundary_2}} | {{data_behavior_2}} | {{integrity_requirement_2}} |
| Contracts | {{semantic_contract_1}}; {{semantic_contract_2}} |
| Validation (TIP-007) | {{boundary_validation_strategy}} |

### P4: Boundaries Explicit
| Boundary | Type | Responsibility | Interface |
| {{boundary_name_1}} | {{boundary_type_1}} | {{boundary_responsibility_1}} | {{boundary_interface_1}} |
| {{boundary_name_2}} | {{boundary_type_2}} | {{boundary_responsibility_2}} | {{boundary_interface_2}} |
- [ ] Every boundary declared with name/responsibility
- [ ] Cross-boundary access through declared interfaces only
- [ ] No implicit boundaries in this specification

### P5: Contracts Deterministic
| Interface | Schema | Runtime Verification | Version |
| {{interface_1}} | {{schema_1}} | {{verification_1}} | {{version_1}} |
| {{interface_2}} | {{schema_2}} | {{verification_2}} | {{version_2}} |
- [ ] Machine-readable schema for every interface
- [ ] Schema validation enforced at boundaries (TIP-007)
- [ ] Breaking changes require version bump
- [ ] Consumer-driven contracts defined

### P6: Control-Flow Complexity
| Aspect | Assessment |
| Control flow depth | {{control_flow_depth}} (acceptable / needs refactoring) |
| Mutation state | {{mutation_state}} (immutable / localized / scattered) |
| Declarative ratio | {{declarative_ratio}}% |
| Mitigation | {{complexity_mitigation_1}}; {{complexity_mitigation_2}} |

### P7: Reasoning Boundaries not Deployment
- [ ] No topology assumptions — Architecture is deployment-agnostic
- [ ] Topology assumption: {{topology_assumption}} → Resolution: {{topology_resolution}}
| Infra deps | {{infrastructure_dependency_1}}; {{infrastructure_dependency_2}} |
| Boundaries | [ ] Boundaries are semantic not deployment · [ ] Same components deployable as monolith, microservices, or serverless |

### P8: Extract Under Reuse Pressure
| Abstraction | Consumers | Justification | Verdict |
| {{abstraction_1}} | {{consumer_count_1}} | {{justification_1}} | 🟢 Justified / 🟡 Questionable / 🔴 Premature |
| {{abstraction_2}} | {{consumer_count_2}} | {{justification_2}} | 🟢 Justified / 🟡 Questionable / 🔴 Premature |

**Rule:** No abstraction with <2 confirmed consumers unless explicitly justified.

### P9: Event Boundaries
| Communication Path | Method | Rationale |
| {{path_1}} | {{method_1}} | {{rationale_1}} |
| {{path_2}} | {{method_2}} | {{rationale_2}} |
- [ ] Event bus for cross-component communication where feasible (TIP-008)
- [ ] Direct sync calls are exceptions with documented rationale
- [ ] Event schemas versioned and shared
- [ ] Event handlers idempotent

### P10: Runtime State Explainability
| State | Location | Provenance | Inspectable? |
| {{state_1}} | {{location_1}} | {{provenance_1}} | 🟢 Yes / 🔴 No |
| {{state_2}} | {{location_2}} | {{provenance_2}} | 🟢 Yes / 🔴 No |
- [ ] ADTO compliance (TIP-009): DTOs carry `_provenance` field
- [ ] State mutations logged with provenance records
- [ ] State inspectable without side effects
- [ ] Immutable event sourcing considered where applicable

## Context Budget

| Agent Role | Context Required | Estimated Budget |
| Specifying Agent | {{specifying_context}} | {{specifying_budget}} |
| Planning Agent | {{planning_context}} | {{planning_budget}} |
| Implementation Agent | {{implementation_context}} | {{implementation_budget}} |
| Review Agent | {{review_context}} | {{review_budget}} |

| External Dependency | Version | Context Impact |
| {{dependency_1}} | {{version_1}} | {{impact_1}} |
| {{dependency_2}} | {{version_2}} | {{impact_2}} |

## Context Flow Optimization

{{current_context_flow}}

| Optimization | Impact on Crystallization Radius |
| {{optimization_1}} | {{radius_impact_1}} |
| {{optimization_2}} | {{radius_impact_2}} |

## AIOA Principle Review Checklist

| # | Principle | Status |
|--:|-----------|--------|
| P1 | Local Reasoning | [ ] Feature understandable from local context |
| P2 | Crystallization Radius | [ ] Radius documented and within acceptable range |
| P3 | Semantic Integrity | [ ] Integrity requirements defined for all boundaries |
| P4 | Boundaries Explicit | [ ] All component boundaries declared |
| P5 | Contracts Deterministic | [ ] All interfaces have machine-verifiable contracts |
| P6 | Declarative Straight-Line | [ ] Design is linear and declarative |
| P7 | Reasoning ≠ Deployment | [ ] No topology assumptions |
| P8 | Extract Under Reuse | [ ] No premature abstractions |
| P9 | Event Boundaries | [ ] Cross-component communication is event-driven |
| P10 | Runtime State Explainable | [ ] State is auditable and inspectable |
