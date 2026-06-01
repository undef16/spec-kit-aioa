---
description: "AIOA-enhanced plan command — verify all TIPs in architecture decisions"
scripts:
  - specify plan
---

# speckit.plan — AIOA Plan Command

**Preset:** aioa (version 1.0.0)
**Reference:** [AIOA.md](../docs/AIOA.md) — Technical Implementation Patterns (TIP-002-TIP-008)

---

## Workflow

### Step 1: Load Specification

Read the spec and extract AIOA compliance context. Verify spec references AIOA.md and all TIPs are checked.

### Step 2: Create AIOA-Native Architecture Decisions

For each ADR, apply AIOA directly to the decision — NO separate AIOA compliance section:

- **Decision contracts** are ADTO (TIP-007)
- **Cross-component integration** is event-driven (TIP-008)
- **Component levels** are declared: Pico/Nano/Micro (TIP-005)
- **Crystallization Radius** is bounded — max 7 files per component (TIP-003)
- **No dead abstraction** — single-use components are inlined (TIP-004)
- **Execution mechanics** are extracted into policies, not inline (TIP-006)
- **Domain types** are value objects, not primitives (TIP-002)

### Step 3: Define Component Boundaries

For each component, document boundaries and verify against AIOA.md TIPs:
- Component name and sole responsibility
- Interfaces and contracts
- Communication patterns (event vs direct)
- State management and provenance

### Step 4: Map Context Flow

Show how context flows through the system. Identify context accumulation hotspots and verify against AIOA.md TIP-003 (no single-file bottlenecks).

### Step 5: Establish Integrity Checkpoints

For each boundary, define verification gates. Reference AIOA.md for TIP-007 (typed, auditable boundaries).

### Step 6: Generate Plan

Write the plan using the AIOA plan template. The plan IS AIOA-native — no separate compliance section needed.

---

## Validation

- [ ] All ADRs integrate AIOA TIPs natively
- [ ] No separate AIOA compliance sections created
- [ ] All component boundaries documented
- [ ] Context flow mapped with hotspots identified
