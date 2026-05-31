# Code Review: {{review_title}}

> **AIOA Preset Active** — This review enforces all 9 AIOA review gates.
> Generated: {{date}}

---

## 1. Review Overview

**Change being reviewed:** {{change_description}}

**Files changed:** {{files_changed}}

**Reviewer context budget:** {{context_budget}}

---

## 2. Review Gate 1: Crystallization Radius

### 2.1 Radius Impact Assessment

**Question:** *Does this change expand the Crystallization Radius of any component?*

| Component | Before Radius | After Radius | Regression? |
|-----------|--------------|--------------|-------------|
| {{component_1}} | {{before_1}} | {{after_1}} | 🟢 No / 🔴 Yes |
| {{component_2}} | {{before_2}} | {{after_2}} | 🟢 No / 🔴 Yes |

### 2.2 Context Expansion Check

- [ ] No new cross-module dependencies introduced
- [ ] No additional context files required to understand the change
- [ ] Dependencies are explicit (no implicit conventions or global state)
- [ ] Context budget annotations are accurate
- [ ] Change does not create "hidden context" (implicit coupling via shared mutable state, ambient conventions, etc.)

### 2.3 High-Crystallization-Risk Patterns

**Check for these anti-patterns:**

| Anti-pattern | Found? | Location |
|-------------|--------|----------|
| Global state mutation | 🟢 No / 🔴 Yes | {{global_state_location}} |
| Shared mutable data across modules | 🟢 No / 🔴 Yes | {{shared_mutable_location}} |
| Implicit dependency on convention | 🟢 No / 🔴 Yes | {{implicit_convention_location}} |
| Cross-cutting concern introduced without declaration | 🟢 No / 🔴 Yes | {{cross_cutting_location}} |
| Context hidden in configuration | 🟢 No / 🔴 Yes | {{config_hidden_location}} |

### 2.4 Gate 1 Verdict

- [ ] **PASS** — Crystallization Radius is maintained or improved
- [ ] **PARTIAL** — Minor increase with justification
- [ ] **FAIL** — Crystallization Radius has regressed; refactoring required before merge

---

## 3. Review Gate 2: Semantic Integrity

### 3.1 Boundary Integrity Check

**Question:** *Is meaning preserved as data/behavior crosses component boundaries?*

| Boundary | Data Crossing | Integrity Preserved? |
|----------|-------------|---------------------|
| {{boundary_1}} | {{data_1}} | 🟢 Yes / 🔴 No / ⚪ N/A |
| {{boundary_2}} | {{data_2}} | 🟢 Yes / 🔴 No / ⚪ N/A |

### 3.2 Semantic Violation Scan

- [ ] Shared types are used consistently across all boundaries
- [ ] No silent type casting or data reshaping across modules
- [ ] Boundary parsing follows "Parse, Don't Validate" pattern (TIP-007)
- [ ] Internal logic does not re-validate already-parsed data
- [ ] No semantic drift — the same concept has the same representation everywhere
- [ ] Versioned contracts are respected (no breaking changes without version bump)

### 3.3 Semantic Drift Detections

| Issue | Severity | Location | Remediation |
|-------|----------|----------|-------------|
| {{issue_1}} | {{severity_1}} | {{location_1}} | {{remediation_1}} |
| {{issue_2}} | {{severity_2}} | {{location_2}} | {{remediation_2}} |

### 3.4 Gate 2 Verdict

- [ ] **PASS** — Semantic Integrity is preserved across all boundaries
- [ ] **PARTIAL** — Minor drift with remediation plan
- [ ] **FAIL** — Semantic drift detected; must be resolved before merge

---

## 4. Review Gate 3: Local Reasoning

### 4.1 Local Understandability Check

**Question:** *Can the changed code be understood from local context alone?*

- [ ] Each modified function is understandable without reading callers or callees
- [ ] No external context required beyond immediate dependencies
- [ ] Side effects are declared at function signature level
- [ ] No global state or ambient conventions required for understanding

### 4.2 Hidden Context Scan

| Pattern | Found? | Location |
|---------|--------|----------|
| Function depends on module-level state | 🟢 No / 🔴 Yes | {{module_state_location}} |
| Side effects not declared in signature | 🟢 No / 🔴 Yes | {{side_effect_location}} |
| Implicit configuration dependency | 🟢 No / 🔴 Yes | {{implicit_config_location}} |
| "Magic" values without explanation | 🟢 No / 🔴 Yes | {{magic_value_location}} |

### 4.3 Gate 3 Verdict

- [ ] **PASS** — Code is locally understandable
- [ ] **PARTIAL** — Minor local reasoning issues
- [ ] **FAIL** — Code requires extensive external context to understand

---

## 5. Review Gate 4: Boundary Explicitness

### 5.1 Boundary Declaration Check

**Question:** *Are all component boundaries involved in this change explicitly declared?*

- [ ] Every component boundary crossed is declared with name and responsibility
- [ ] Cross-boundary access occurs through declared interfaces only
- [ ] No direct access to internal implementation of other components
- [ ] No implicit boundaries based on conventions or directory structure

### 5.2 Boundary Violations

| Violation | Component | Resolution |
|-----------|-----------|------------|
| {{violation_1}} | {{component_violated_1}} | {{resolution_1}} |
| {{violation_2}} | {{component_violated_2}} | {{resolution_2}} |

### 5.3 Gate 4 Verdict

- [ ] **PASS** — All boundaries are explicit
- [ ] **PARTIAL** — Minor boundary explicitness issues
- [ ] **FAIL** — Implicit boundaries detected; must be declared

---

## 6. Review Gate 5: Contract Determinism

### 6.1 Machine-Verifiability Check

**Question:** *Are all interfaces in this change machine-verifiable?*

- [ ] Every interface has a schema or type definition
- [ ] Schema validation is enforced at boundaries (TIP-007)
- [ ] No `any` or untyped data crossing boundaries
- [ ] Contract versioning is respected
- [ ] Consumer-driven contracts are satisfied

### 6.2 Non-Deterministic Patterns

| Pattern | Found? | Location |
|---------|--------|----------|
| Untyped boundary crossing | 🟢 No / 🔴 Yes | {{untyped_location}} |
| Missing input validation | 🟢 No / 🔴 Yes | {{missing_validation_location}} |
| Inconsistent error shapes | 🟢 No / 🔴 Yes | {{error_shape_location}} |
| Schema version mismatch | 🟢 No / 🔴 Yes | {{version_mismatch_location}} |

### 6.3 Gate 5 Verdict

- [ ] **PASS** — All interfaces are machine-verifiable
- [ ] **PARTIAL** — Minor verification gaps
- [ ] **FAIL** — Non-deterministic contracts detected

---

## 7. Review Gate 6: Control-Flow Simplicity

### 7.1 Complexity Assessment

**Question:** *Is the code straight-line and declarative?*

- [ ] No deeply nested conditionals (depth > 3)
- [ ] Complex loops replaced with declarative operations
- [ ] Mutable state is localized and minimized
- [ ] Control flow is linear (no long-range breaks, goto patterns)
- [ ] Async control flow uses async/await

### 7.2 Complexity Hotspots

| Location | Issue | Recommendation |
|----------|-------|----------------|
| {{complex_location_1}} | {{complex_issue_1}} | {{complex_recommendation_1}} |
| {{complex_location_2}} | {{complex_issue_2}} | {{complex_recommendation_2}} |

### 7.3 Gate 6 Verdict

- [ ] **PASS** — Code is simple and declarative
- [ ] **PARTIAL** — Minor complexity issues
- [ ] **FAIL** — Complex control flow must be simplified

---

## 8. Review Gate 7: Decomposition Quality

### 8.1 Granularity Assessment

**Question:** *Is the component granularity appropriate?*

- [ ] Components are neither god modules (too few, too broad) nor atomized (too many, too narrow)
- [ ] Each component has a clear, single responsibility
- [ ] No component requires understanding of the whole system
- [ ] Component size is appropriate for AI agent context windows

### 8.2 Decomposition Issues

| Issue | Component | Recommendation |
|-------|-----------|----------------|
| {{decomposition_issue_1}} | {{decomposition_component_1}} | {{decomposition_recommendation_1}} |
| {{decomposition_issue_2}} | {{decomposition_component_2}} | {{decomposition_recommendation_2}} |

### 8.3 Gate 7 Verdict

- [ ] **PASS** — Decomposition quality is appropriate
- [ ] **PARTIAL** — Minor decomposition issues
- [ ] **FAIL** — Decomposition needs restructuring

---

## 9. Review Gate 8: Integration Locality

### 9.1 Integration Assessment

**Question:** *Are integrations local and explicit?*

- [ ] Cross-component integrations are declared at the integration point
- [ ] No "spaghetti" integration (components connected in a tangled web)
- [ ] Integration contracts are versioned and documented
- [ ] No transitive integration coupling (A→B→C dependency chains)

### 9.2 Integration Issues

| Issue | Components | Recommendation |
|-------|-----------|----------------|
| {{integration_issue_1}} | {{integration_components_1}} | {{integration_recommendation_1}} |
| {{integration_issue_2}} | {{integration_components_2}} | {{integration_recommendation_2}} |

### 9.3 Gate 8 Verdict

- [ ] **PASS** — Integrations are local and explicit
- [ ] **PARTIAL** — Minor integration locality issues
- [ ] **FAIL** — Integration restructuring required

---

## 10. Review Gate 9: Runtime Explainability

### 10.1 Explainability Assessment

**Question:** *Can runtime state be explained?*

- [ ] State mutations have provenance tracking (who, what, when, why)
- [ ] State is inspectable without side effects
- [ ] ADTO pattern followed: DTOs carry `_provenance` field (TIP-009)
- [ ] Immutable event sourcing used where applicable
- [ ] State recovery paths are documented

### 10.2 Explainability Issues

| Issue | Location | Remediation |
|-------|----------|-------------|
| {{explainability_issue_1}} | {{explainability_location_1}} | {{explainability_remediation_1}} |
| {{explainability_issue_2}} | {{explainability_location_2}} | {{explainability_remediation_2}} |

### 10.3 Gate 9 Verdict

- [ ] **PASS** — Runtime state is explainable
- [ ] **PARTIAL** — Minor explainability gaps
- [ ] **FAIL** — State is not explainable; ADTO pattern must be applied

---

## 11. Component Boundary Review

### 11.1 Boundary Respect Check

- [ ] Changes respect defined component boundaries
- [ ] No unauthorized cross-boundary access
- [ ] Interfaces are respected (internal implementation details not exposed)
- [ ] Component responsibilities are maintained

---

## 12. Context Flow Review

### 12.1 Context Flow Impact

- [ ] Context flow is maintained or improved
- [ ] No new "context hotspots" created (areas where many files must be understood together)
- [ ] Data flow paths are clear and documented
- [ ] No unnecessary indirection that increases context requirements

### 12.2 Flow Optimization Opportunities

{{flow_optimization_opportunities}}

---

## 13. Overall AIOA Compliance Summary

### 13.1 Gate Scores

| Gate | Score | Notes |
|------|-------|-------|
| **Gate 1: Crystallization Radius** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cr_notes}} |
| **Gate 2: Semantic Integrity** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{si_notes}} |
| **Gate 3: Local Reasoning** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{lr_notes}} |
| **Gate 4: Boundary Explicitness** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{be_notes}} |
| **Gate 5: Contract Determinism** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cd_notes}} |
| **Gate 6: Control-Flow Simplicity** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{cfs_notes}} |
| **Gate 7: Decomposition Quality** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{dq_notes}} |
| **Gate 8: Integration Locality** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{il_notes}} |
| **Gate 9: Runtime Explainability** | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | {{re_notes}} |

### 13.2 Required Changes Before Approval

1. {{required_change_1}}
2. {{required_change_2}}
3. {{required_change_3}}

### 13.3 Recommendations

- {{recommendation_1}}
- {{recommendation_2}}

---

## 14. Final Verdict

- [ ] **APPROVED** — All 9 gates pass; change is AIOA-compliant
- [ ] **APPROVED WITH COMMENTS** — Minor issues noted, no gate failures
- [ ] **CHANGES REQUESTED** — One or more gates marked PARTIAL; issues must be addressed
- [ ] **REJECTED** — One or more gates marked FAIL; fundamental AIOA principle violation; architecture review required
