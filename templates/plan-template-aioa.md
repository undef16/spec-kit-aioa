---
# AIOA Additions — Appended after core plan-template.md
# This file contains ONLY AIOA-specific sections that are appended to the core Spec Kit plan template.
---

> **AIOA Preset Active** — All plan steps include full AIOA principle analysis (all 10 principles).

## Architecture Decision Records

### ADR-{{number}}: {{decision_title}}

**Status:** {{status}} | **Context:** {{context}} | **Decision:** {{decision}}
**Consequences:** + {{positive_consequence}} | - {{negative_consequence}}

**P1-P10 Compass:**
| P | Assessment | Verification |
|---|-----------|-------------|
| P1 | {{local_reasoning_verdict}} | Mitigation: {{local_reasoning_mitigation}} |
| P2 | Before: {{before_files}}/{{before_deps}}/{{before_rating}} → After: {{after_files}}/{{after_deps}}/{{after_rating}} |
| P3 | {{semantic_integrity_impact}} | |
| P4 | [ ] Boundaries declared · [ ] No implicit · [ ] Cross-boundary via interfaces |
| P5 | [ ] Machine-verifiable schemas · [ ] Schema validation (TIP-007) · [ ] Versioning documented |
| P6 | [ ] Linear/declarative · [ ] No deep nesting · [ ] Localized mutation |
| P7 | [ ] No topology assumptions · [ ] Infra isolated · [ ] Interfaces agnostic |
| P8 | [ ] ≥2 consumers · [ ] No speculative abstractions · [ ] Premature flagged |
| P9 | [ ] Event bus (TIP-008) · [ ] Direct = exceptions · [ ] Schemas versioned |
| P10 | [ ] Provenance tracking · [ ] Inspectable · [ ] ADTO pattern (TIP-009) |

## Component Boundaries with Crystallization Radius

```
{{boundary_map_diagram}}
```

| Component | Responsibility | Radius | Dependencies | Boundary Explicit? |
|-----------|--------------|--------|--------------|-------------------|
| {{component_1}} | {{responsibility_1}} | {{radius_1}} | {{dependencies_1}} | 🟢 Yes / 🔴 No |
| {{component_2}} | {{responsibility_2}} | {{radius_2}} | {{dependencies_2}} | 🟢 Yes / 🔴 No |
| {{component_3}} | {{responsibility_3}} | {{radius_3}} | {{dependencies_3}} | 🟢 Yes / 🔴 No |

| Boundary | Interface | Contract | Context Cost | Deterministic? |
|----------|-----------|----------|-------------|----------------|
| {{boundary_a}} | {{interface_a}} | {{contract_a}} | {{cost_a}} | 🟢 Yes / 🔴 No |
| {{boundary_b}} | {{interface_b}} | {{contract_b}} | {{cost_b}} | 🟢 Yes / 🔴 No |

## Context Flow with Optimization

```
{{context_flow_diagram}}
```

{{context_flow_description}}

| Hot Flow | Context Cost | Optimization Opportunity |
|----------|-------------|------------------------|
| {{flow_1}} | {{cost_1}} | {{optimization_1}} |
| {{flow_2}} | {{cost_2}} | {{optimization_2}} |

## Pre-Implementation AIOA Principle Checks

### Step {{step_number}}: {{step_title}} | Budget: {{context_budget}}

| P | Checks |
|---|--------|
| P1 Local Reasoning | [ ] Understandable from local context · [ ] External requirements documented |
| P2 Radius | [ ] Budget reviewed ({{context_budget}} files) · [ ] Dependencies documented · [ ] No implicit context |
| P3 Semantic | [ ] Shared types consistent · [ ] Parse Don't Validate (TIP-007) · [ ] No silent transformations |
| P4 Boundaries | [ ] All boundaries declared · [ ] Access through declared interfaces only |
| P5 Contracts | [ ] Machine-verifiable schemas · [ ] Schema enforced at boundaries |
| P6 Declarative | [ ] Code is linear/declarative · [ ] No deeply nested control flow |
| P7 Arch Indep | [ ] No deployment topology assumptions · [ ] Infra isolated to boundary |
| P8 Extract Reuse | [ ] Sufficient reuse demand · [ ] No speculative abstractions |
| P9 Events | [ ] Event-driven (TIP-008) · [ ] Direct calls are exceptions with rationale |
| P10 Explainability | [ ] State changes have provenance · [ ] ADTO pattern (TIP-009) |

## Semantic Integrity Checkpoints

### {{checkpoint_title_1}} | Location: {{workflow_location_1}}
- **Verify:** {{verification_1}}; {{verification_2}}
- **On failure:** {{failure_action_1}}

### {{checkpoint_title_2}} | Location: {{workflow_location_2}}
- **Verify:** {{verification_1}}; {{verification_2}}
- **On failure:** {{failure_action_2}}

## AIOA Risk Assessment

| Risk Type | Risk | Likelihood | Impact | Mitigation |
|-----------|------|-----------|--------|------------|
| Radius | {{risk_1}} | {{likelihood_1}} | {{impact_1}} | {{mitigation_1}} |
| Radius | {{risk_2}} | {{likelihood_2}} | {{impact_2}} | {{mitigation_2}} |
| Semantic | {{risk_1}} | Boundary: {{boundary_1}} | Detection: {{detection_1}} |
| Semantic | {{risk_2}} | Boundary: {{boundary_2}} | Detection: {{detection_2}} |
| Other (P{{principle_number_1}}) | {{risk_1}} | {{impact_1}} | {{mitigation_1}} |
| Other (P{{principle_number_2}}) | {{risk_2}} | {{impact_2}} | {{mitigation_2}} |

## Architecture Independence Verification (P7)

- [ ] Interface-based dependencies (not infrastructure-based)
- [ ] No deployment topology assumed in component design
- [ ] Network boundaries not encoded in interfaces
- [ ] Infrastructure concerns configurable at deployment boundary

## AIOA Principle Compliance Summary

| Principle | Status | Notes |
|-----------|--------|-------|
| P1 Local Reasoning | 🟢 / 🟡 / 🔴 | {{p1_notes}} |
| P2 Crystallization Radius | 🟢 / 🟡 / 🔴 | {{p2_notes}} |
| P3 Semantic Integrity | 🟢 / 🟡 / 🔴 | {{p3_notes}} |
| P4 Boundaries Explicit | 🟢 / 🟡 / 🔴 | {{p4_notes}} |
| P5 Contracts Deterministic | 🟢 / 🟡 / 🔴 | {{p5_notes}} |
| P6 Declarative Straight-Line | 🟢 / 🟡 / 🔴 | {{p6_notes}} |
| P7 Reasoning ≠ Deployment | 🟢 / 🟡 / 🔴 | {{p7_notes}} |
| P8 Extract Under Reuse | 🟢 / 🟡 / 🔴 | {{p8_notes}} |
| P9 Event Boundaries | 🟢 / 🟡 / 🔴 | {{p9_notes}} |
| P10 Runtime State Explainable | 🟢 / 🟡 / 🔴 | {{p10_notes}} |
