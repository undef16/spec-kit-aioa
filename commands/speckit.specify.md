---
description: "AIOA-enhanced specify command — verify all TIPs against specification"
scripts:
  - specify spec
---

# speckit.specify — AIOA Specification Command

**Preset:** aioa (version 1.0.0)
**Reference:** [AIOA.md](../docs/AIOA.md) — Technical Implementation Patterns

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

- Apply AIOA TIPs directly to the specification. For the full list of TIPs and their definitions, see [AIOA.md](../docs/AIOA.md).

- Reference language-specific examples when designing architecture:
  - **Python**: `docs/py_examples/` — shows concrete TIP implementations (ADTO base class, typed event bus, strategy pattern, domain identifiers)
  - **Other languages**: `docs/<language>_examples/` — create equivalent examples following the same TIP structure

### Step 3: Generate Specification

Write the specification using the AIOA spec template. The template is AIOA-native — no separate compliance section needed.

### Step 4: Validate

- [ ] All architecture layers integrate AIOA TIPs
- [ ] No separate AIOA compliance sections created

---

## Output

**File:** `specs/{{spec_id}}.aioa.md`

The specification includes standard fields. All architecture is AIOA-native — no separate compliance section created.
