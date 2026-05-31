---
# AIOA Additions — Appended after core code-review-template.md
# This file contains ONLY AIOA-specific sections that are appended to the core Spec Kit code review template.
---

> **AIOA Preset Active** — This review enforces all 9 AIOA review gates.

## AIOA Review Gates

### G1: Crystallization Radius
| Component | Before | After | Regression? |
|-----------|--------|-------|-------------|
| {{component_1}} | {{before_1}} | {{after_1}} | 🟢 No / 🔴 Yes |
| {{component_2}} | {{before_2}} | {{after_2}} | 🟢 No / 🔴 Yes |
- [ ] No new cross-module deps · [ ] No additional context files needed · [ ] Dependencies explicit · [ ] Budget annotations accurate · [ ] No hidden context (shared mutable state, ambient conventions)
| Anti-pattern | Found? | Location |
| Global state mutation | 🟢 No / 🔴 Yes | {{global_state_location}} |
| Shared mutable cross-module | 🟢 No / 🔴 Yes | {{shared_mutable_location}} |
| Implicit convention dependency | 🟢 No / 🔴 Yes | {{implicit_convention_location}} |
| Cross-cutting concern undeclared | 🟢 No / 🔴 Yes | {{cross_cutting_location}} |
| Context hidden in config | 🟢 No / 🔴 Yes | {{config_hidden_location}} |
**Verdict:** [ ] PASS — Radius maintained/improved · [ ] PARTIAL — Minor increase justified · [ ] FAIL — Radius regressed; refactor required

### G2: Semantic Integrity
| Boundary | Data Crossing | Integrity Preserved? |
|----------|-------------|---------------------|
| {{boundary_1}} | {{data_1}} | 🟢 Yes / 🔴 No / ⚪ N/A |
| {{boundary_2}} | {{data_2}} | 🟢 Yes / 🔴 No / ⚪ N/A |
- [ ] Shared types consistent · [ ] No silent casting/reshaping · [ ] Parse Don't Validate (TIP-007) · [ ] Internal logic doesn't re-validate · [ ] No semantic drift · [ ] Versioned contracts respected
| Semantic Drift | Severity | Location | Remediation |
| {{issue_1}} | {{severity_1}} | {{location_1}} | {{remediation_1}} |
| {{issue_2}} | {{severity_2}} | {{location_2}} | {{remediation_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor drift, remediation plan · [ ] FAIL — Semantic drift; resolve before merge

### G3: Local Reasoning
- [ ] Functions understandable without callers/callees · [ ] No external context beyond immediate deps · [ ] Side effects declared at signature · [ ] No global state/ambient conventions needed
| Hidden Context | Found? | Location |
| Module-level state dependency | 🟢 No / 🔴 Yes | {{module_state_location}} |
| Undeclared side effects | 🟢 No / 🔴 Yes | {{side_effect_location}} |
| Implicit config dependency | 🟢 No / 🔴 Yes | {{implicit_config_location}} |
| Magic values unexplained | 🟢 No / 🔴 Yes | {{magic_value_location}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor issues · [ ] FAIL — Requires extensive external context

### G4: Boundary Explicitness
- [ ] Every boundary crossed declared with name/responsibility · [ ] Access through declared interfaces only · [ ] No direct internal access · [ ] No implicit boundaries via conventions/directory structure
| Violation | Component | Resolution |
| {{violation_1}} | {{component_violated_1}} | {{resolution_1}} |
| {{violation_2}} | {{component_violated_2}} | {{resolution_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor issues · [ ] FAIL — Implicit boundaries; must be declared

### G5: Contract Determinism
- [ ] Every interface has schema/type definition · [ ] Schema validation enforced at boundaries (TIP-007) · [ ] No `any`/untyped data crossing · [ ] Contract versioning respected · [ ] Consumer-driven contracts satisfied
| Non-Deterministic Pattern | Found? | Location |
| Untyped boundary crossing | 🟢 No / 🔴 Yes | {{untyped_location}} |
| Missing input validation | 🟢 No / 🔴 Yes | {{missing_validation_location}} |
| Inconsistent error shapes | 🟢 No / 🔴 Yes | {{error_shape_location}} |
| Schema version mismatch | 🟢 No / 🔴 Yes | {{version_mismatch_location}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor gaps · [ ] FAIL — Non-deterministic contracts

### G6: Control-Flow Simplicity
- [ ] No deep nesting (depth > 3) · [ ] Complex loops → declarative ops · [ ] Mutable state localized/minimized · [ ] Linear control flow · [ ] Async uses async/await
| Hotspot | Issue | Recommendation |
| {{complex_location_1}} | {{complex_issue_1}} | {{complex_recommendation_1}} |
| {{complex_location_2}} | {{complex_issue_2}} | {{complex_recommendation_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor issues · [ ] FAIL — Complex flow must be simplified

### G7: Decomposition Quality
- [ ] Components neither god modules nor atomized · [ ] Clear single responsibility · [ ] No component requires whole-system understanding · [ ] Size appropriate for AI context windows
| Issue | Component | Recommendation |
| {{decomposition_issue_1}} | {{decomposition_component_1}} | {{decomposition_recommendation_1}} |
| {{decomposition_issue_2}} | {{decomposition_component_2}} | {{decomposition_recommendation_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor issues · [ ] FAIL — Needs restructuring

### G8: Integration Locality
- [ ] Cross-component integrations declared at integration point · [ ] No spaghetti integration · [ ] Integration contracts versioned/documented · [ ] No transitive coupling (A→B→C chains)
| Issue | Components | Recommendation |
| {{integration_issue_1}} | {{integration_components_1}} | {{integration_recommendation_1}} |
| {{integration_issue_2}} | {{integration_components_2}} | {{integration_recommendation_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor issues · [ ] FAIL — Restructuring required

### G9: Runtime Explainability
- [ ] State mutations have provenance (who, what, when, why) · [ ] State inspectable without side effects · [ ] ADTO: DTOs carry `_provenance` (TIP-009) · [ ] Event sourcing used where applicable · [ ] State recovery paths documented
| Issue | Location | Remediation |
| {{explainability_issue_1}} | {{explainability_location_1}} | {{explainability_remediation_1}} |
| {{explainability_issue_2}} | {{explainability_location_2}} | {{explainability_remediation_2}} |
**Verdict:** [ ] PASS · [ ] PARTIAL — Minor gaps · [ ] FAIL — Apply ADTO pattern

## TIP Checks

| TIP | Checks |
|-----|--------|
| **TIP-002:** Semantic Collision | [ ] No conflatable domain concepts · [ ] Value objects over primitives in domain-critical flows · [ ] Naming = architecture, not cosmetics |
| **TIP-006:** Declarative Code | [ ] No manual loops where collection operators suffice · [ ] No hand-written retry · [ ] No inline transaction plumbing · [ ] Business code expresses intent, not machinery |
| **TIP-007:** Strict JSON Gateways | [ ] Input validated at boundary · [ ] DTOs as typed contracts · [ ] Technical validation ≠ business validation · [ ] No defensive boilerplate in core methods |
| **TIP-009:** Auditable DTOs | [ ] State transitions self-documenting · [ ] Mutation history recorded · [ ] Provenance: what, who, why, when |

## Component Boundary Review

- [ ] Changes respect defined component boundaries
- [ ] No unauthorized cross-boundary access
- [ ] Interfaces respected (internals not exposed)
- [ ] Component responsibilities maintained

## Context Flow Review

- [ ] Context flow maintained or improved
- [ ] No new "context hotspots" (many files must be understood together)
- [ ] Data flow paths clear and documented
- [ ] No unnecessary indirection increasing context requirements

**Flow optimization opportunities:** {{flow_optimization_opportunities}}

## Overall AIOA Compliance Summary

| Gate | Score | Notes |
|------|-------|-------|
| G1: Crystallization Radius | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cr_notes}} |
| G2: Semantic Integrity | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{si_notes}} |
| G3: Local Reasoning | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{lr_notes}} |
| G4: Boundary Explicitness | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{be_notes}} |
| G5: Contract Determinism | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cd_notes}} |
| G6: Control-Flow Simplicity | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cfs_notes}} |
| G7: Decomposition Quality | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{dq_notes}} |
| G8: Integration Locality | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{il_notes}} |
| G9: Runtime Explainability | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{re_notes}} |

**Required changes:**
1. {{required_change_1}}
2. {{required_change_2}}
3. {{required_change_3}}

**Recommendations:** {{recommendation_1}}; {{recommendation_2}}

## Final Verdict

- [ ] **APPROVED** — All 9 gates pass; AIOA-compliant
- [ ] **APPROVED WITH COMMENTS** — Minor issues, no gate failures
- [ ] **CHANGES REQUESTED** — Gate(s) marked PARTIAL; must be addressed
- [ ] **REJECTED** — Gate(s) marked FAIL; fundamental AIOA violation; architecture review required
