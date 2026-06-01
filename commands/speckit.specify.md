---
description: "AIOA-enhanced specify command — verify all TIPs against specification"
scripts:
  - specify spec
---

# speckit.specify — AIOA Specification Command

**Preset:** aioa (version 1.0.0)
**Reference:** [AIOA.md](../docs/AIOA.md) — Technical Implementation Patterns (TIP-002-TIP-008)

---

## Workflow

### Step 1: Gather Specification Details

> **What feature or behavior change are you specifying?**

Capture:
- Feature name and summary
- Problem being solved
- Proposed solution outline
- Scope boundaries

### Step 2: Apply AIOA to Architecture

AIOA is not a separate check — it IS the architecture. Apply TIPs directly when designing each layer:

- **Domain Entities** → ADTO base class for all entities (TIP-007)
- **Value Objects** → distinct types per domain concept, no `str`/`int` for IDs (TIP-002)
- **Services** → communicate via event bus, even in-process (TIP-008)
- **Component Naming** → Pico actor (pure func), Nano actor (stateful), Micro actor (service) — never just "Service" (TIP-005)
- **Execution Mechanics** → extract retry, timeout, fallback into named policies (TIP-006)
- **Crystallization Radius** → each component max 7 files to understand (TIP-003)
- **Dead Wrappers** → if A→B→C and B adds no value, call A→C directly (TIP-004)

### Step 3: Generate Specification

Write the specification using the AIOA spec template. The template is AIOA-native — no separate compliance section needed.

### Step 4: Validate

- [ ] All architecture layers integrate AIOA TIPs
- [ ] No separate AIOA compliance sections created

---

## Output

**File:** `specs/{{spec_id}}.aioa.md`

The specification includes standard fields. All architecture is AIOA-native — no separate compliance section created.
