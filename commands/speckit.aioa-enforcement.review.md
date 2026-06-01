---
description: "Run AIOA code review — checks all 9 gates (G1-G9) and TIP compliance on implemented code"
scripts:
  - speckit.aioa-enforcement.review
---

# speckit.aioa-enforcement.review — AIOA Code Review Command

**Extension:** aioa-enforcement (version 1.0.0)

> This command runs the full AIOA review suite. You can also use `/speckit.aioa-enforcement.review --quick` for a summary-only review.

---

## Workflow

### Step 1: Gather Context

- [ ] Read the completed implementation files
- [ ] Read the specification file (`specs/{{spec_id}}.aioa.md`)
- [ ] Read the implementation plan (`specs/{{spec_id}}/plan.md`)
- [ ] Identify the bounded context(s) involved

### Step 2: Run AIOA Review Gates

For each gate, check the implementation against AIOA criteria and record the verdict.

#### G1: Crystallization Radius
- [ ] No new cross-module dependencies added without justification
- [ ] Context budget annotations are still accurate
- [ ] No hidden context (shared mutable state, ambient conventions)
- [ ] Modification possible within 1-8 files
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g1_verdict}}

#### G2: Semantic Integrity
- [ ] All boundary crossings use typed contracts (no `dict`/`Any` leakage)
- [ ] No primitive types (`str`/`int`) in domain-critical flows (TIP-002)
- [ ] No semantic drift between implementation and specification
- [ ] Shared types are consistent across consumers
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g2_verdict}}

#### G3: Local Reasoning
- [ ] Each function/module is understandable without callers/callees
- [ ] No global state or ambient conventions needed for understanding
- [ ] Side effects declared at signature level
- [ ] Magic values are explained or replaced with constants
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g3_verdict}}

#### G4: Boundary Explicitness
- [ ] Every boundary crossed is declared with name and responsibility
- [ ] Access through declared interfaces only (no private member access)
- [ ] No implicit boundaries via directory structure or conventions
- [ ] No declared exports that are never consumed (dead code)
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g4_verdict}}

#### G5: Contract Determinism
- [ ] Every interface has a schema or type definition (Pydantic, Zod, JSON Schema)
- [ ] Schema validation enforced at boundaries (TIP-007)
- [ ] No `dict`/`Any` data crossing component boundaries
- [ ] Versioned contracts respected
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g5_verdict}}

#### G6: Control-Flow Simplicity
- [ ] No deeply nested control flow (depth <= 3)
- [ ] Complex loops replaced with declarative operations
- [ ] Mutable state localized and minimized
- [ ] Async/await used correctly
- [ ] No repeated try/except or retry boilerplate (TIP-006)
- [ ] Fallback chains use declarative pipeline, not procedural fallback
- [ ] Business code is straight-line; execution mechanics are in abstractions
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g6_verdict}}

#### G7: Decomposition Quality
- [ ] Components are not god modules or over-atomized
- [ ] Each component has a single clear responsibility
- [ ] No component requires whole-system understanding
- [ ] Size appropriate for AI context windows
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g7_verdict}}

#### G8: Integration Locality
- [ ] Cross-component integrations declared at integration point
- [ ] No spaghetti integration (A→B→C→A chains)
- [ ] Integration contracts versioned and documented
- [ ] No transitive coupling
- [ ] No component extracted without proven consumer (TIP-005 Quantum Spectrum)
- [ ] Pico Actors are deterministic primitives, not premature abstractions
- [ ] No centralized orchestrator that knows all component internals (TIP-008)
- [ ] Cross-component state passed via events, not private attributes
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g8_verdict}}

#### G9: Runtime Explainability
- [ ] State mutations have provenance (who, what, when, why) — TIP-009
- [ ] DTOs carry `_provenance` or extend ADTO base class
- [ ] State inspectable without side effects
- [ ] Event sourcing considered where applicable
**Verdict:** 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL — {{g9_verdict}}

### Step 3: Check TIP Compliance

| Check | Status |
|-------|--------|
| **TIP-002:** No primitive types in domain-critical flows; value objects for domain IDs; no naming collision | 🟢 / 🔴 |
| **TIP-006:** No manual loops where collection operators suffice; no hand-written retry/transactions | 🟢 / 🔴 |
| **TIP-007:** Input validated at boundaries; DTOs as typed contracts; no defensive boilerplate in core | 🟢 / 🔴 |
| **TIP-008:** Event-driven integration preferred; direct sync calls documented as exceptions | 🟢 / 🔴 |
| **TIP-009:** ADTO pattern with mutation history and provenance tracking | 🟢 / 🔴 |

### Step 4: Generate Review Report

Write the review report to `reviews/{{spec_id}}.review.md`:

```markdown
# AIOA Code Review: {{spec_id}}

**Review date:** {{date}}
**Reviewer:** {{agent_name}}

## Summary

| Gate | Status | Key Findings |
|------|--------|-------------|
| G1: Crystallization Radius | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G2: Semantic Integrity | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G3: Local Reasoning | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G4: Boundary Explicitness | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G5: Contract Determinism | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G6: Control-Flow Simplicity | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G7: Decomposition Quality | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G8: Integration Locality | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |
| G9: Runtime Explainability | 🟢 PASS / 🟡 PARTIAL / 🔴 FAIL | ... |

**Overall:** 🟢 APPROVED / 🟡 APPROVED WITH COMMENTS / 🔴 CHANGES REQUESTED / ❌ REJECTED

## Violations Found

| # | Severity | Gate | File | Issue | Remediation |
|---|----------|------|------|-------|-------------|
| 1 | 🔴 Critical | G2 | {{file}} | {{issue}} | {{remediation}} |
| 2 | 🟡 Major | G4 | {{file}} | {{issue}} | {{remediation}} |
| 3 | 🟠 Minor | G6 | {{file}} | {{issue}} | {{remediation}} |

## TIP Compliance Summary

- TIP-002 (Semantic Collision): {{pass/fail}} — {{details}}
- TIP-006 (Declarative Code): {{pass/fail}} — {{details}}
- TIP-007 (Strict JSON Gateways): {{pass/fail}} — {{details}}
- TIP-008 (Event-Driven Integration): {{pass/fail}} — {{details}}
- TIP-009 (Auditable DTOs): {{pass/fail}} — {{details}}

## Required Changes

1. {{required_change_1}}
2. {{required_change_2}}
3. {{required_change_3}}

## Recommendations

{{recommendations}}
```

---

## Output

**File:** `reviews/{{spec_id}}.review.md`

The review report includes:
- All 9 AIOA gate verdicts with key findings
- Violation list with severity, location, and remediation
- TIP compliance summary
- Required changes and recommendations
