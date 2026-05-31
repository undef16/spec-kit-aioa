---
# AIOA Additions — Appended after core tasks-template.md
# This file contains ONLY AIOA-specific sections that are appended to the core Spec Kit tasks template.
---

> **AIOA Preset Active** — This task includes full AIOA principle verification (all 10 principles).

## AIOA Context Budget

| Context Item | Details |
|-------------|---------|
| Files to read | {{files_to_read}} |
| Files to modify | {{files_to_modify}} |
| Cross-module context | {{cross_module_context}} |
| Context budget | {{context_budget}} (Low / Medium / High) |

## AIOA Principle Checks

### P1: Local Reasoning
- [ ] Understandable from local context · [ ] External requirements documented · [ ] No global state/ambient conventions needed

### P2: Crystallization Radius
- [ ] All context files loaded ({{context_budget}} items) · [ ] Implicit dependencies identified · [ ] Radius of affected component(s) known · [ ] Change does NOT expand radius beyond current boundaries
| Current radius | {{current_radius}} | Expected | {{expected_radius}} | Delta | {{radius_delta}} |
| If expanding | {{radius_expansion_rationale}} |

```
{{context_surface_map}}
```

### P3: Semantic Integrity
| Boundary | Direction | Data Crossing | Integrity Risk |
|----------|-----------|--------------|----------------|
| {{boundary_1}} | {{direction_1}} | {{data_1}} | {{risk_1}} |
| {{boundary_2}} | {{direction_2}} | {{data_2}} | {{risk_2}} |

**Gate 1 — Shared Types:** [ ] Correct versions at boundaries · [ ] No casting without contract · [ ] Boundary parsing validated
**Gate 2 — Parse Don't Validate (TIP-007):** [ ] External data parsed at boundary · [ ] Internal logic on trusted types · [ ] No defensive checks in core
**Gate 3 — No Silent Transformations:** [ ] Every transformation explicit · [ ] Governed by semantic contract · [ ] Tested for meaning preservation

### P4: Boundaries Explicit
- [ ] Every boundary crossed declared · [ ] Access through declared interfaces · [ ] No implicit boundaries · [ ] Component responsibilities respected

### P5: Contracts Deterministic
- [ ] Machine-verifiable schemas · [ ] Schema enforced at boundaries · [ ] Breaking changes require version bump · [ ] Consumer-driven contracts satisfied

### P6: Control-Flow Complexity
- [ ] Linear/declarative where possible · [ ] No deeply nested conditionals (depth > 3) · [ ] Mutable state localized/minimized · [ ] Complex flow replaced with declarative ops

### P7: Reasoning Boundaries ≠ Deployment
- [ ] No infra deps in core logic · [ ] Interfaces deployment-agnostic · [ ] No topology assumptions · [ ] Infra isolated to deployment boundary

### P8: Extract Under Reuse
- [ ] New abstractions have ≥2 consumers · [ ] No speculative abstractions · [ ] Existing abstractions justified

### P9: Event Boundaries
- [ ] Event bus for cross-component communication (TIP-008) · [ ] Direct sync calls = exceptions with rationale · [ ] Event schemas versioned/shared · [ ] Handlers idempotent

### P10: Runtime State Explainability
- [ ] State mutations have provenance (who, what, when, why) · [ ] State inspectable without side effects · [ ] ADTO: DTOs carry `_provenance` (TIP-009) · [ ] Event sourcing considered

## AIOA Implementation Step Checks

| Step | Details | AIOA Check |
|------|---------|------------|
| 1: {{implementation_step_1}} | {{detail_1}}; {{detail_2}} | {{aioa_check_1}} |
| 2: {{implementation_step_2}} | {{detail_1}}; {{detail_2}} | {{aioa_check_2}} |
| 3: {{implementation_step_3}} | {{detail_1}}; {{detail_2}} | {{aioa_check_3}} |

## AIOA Compliance Checklist

| # | Principle | Verification |
|--:|-----------|-------------|
| P1 | Local Reasoning | [ ] Task understandable locally · [ ] External requirements documented |
| P2 | Crystallization Radius | [ ] Radius didn't regress · [ ] Budget annotations accurate · [ ] No implicit deps · [ ] Change self-contained |
| P3 | Semantic Integrity | [ ] Shared types consistent · [ ] Parse Don't Validate (TIP-007) · [ ] No silent transformations · [ ] Contracts versioned |
| P4 | Boundaries Explicit | [ ] All boundaries declared · [ ] No boundary violations |
| P5 | Contracts Deterministic | [ ] Machine-verifiable schemas · [ ] Validation enforced |
| P6 | Declarative Straight-Line | [ ] Linear/declarative · [ ] No complex control flow |
| P7 | Reasoning ≠ Deployment | [ ] No infra deps in core · [ ] Interfaces agnostic · [ ] No topology assumptions |
| P8 | Extract Under Reuse | [ ] No premature abstractions · [ ] Extracted based on reuse pressure only |
| P9 | Event Boundaries | [ ] Cross-component comm is event-driven · [ ] Direct calls justified |
| P10 | Runtime State Explainable | [ ] State auditable with provenance · [ ] ADTO pattern followed |

## AIOA Post-Completion

- [ ] **Context Budget:** Updated if changed; Crystallization Radius re-evaluated
- [ ] **Semantic Integrity:** All integrity gates passed; contracts satisfied
- [ ] **Principle Compliance:** All 10 AIOA principles verified; violations documented
