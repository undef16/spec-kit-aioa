---
# AIOA Wrap — Wraps around core tasks-template.md
# Reference: docs/AIOA.md — Technical Implementation Patterns (TIP-002-TIP-008)
---

> **AIOA Preset Active** — Tasks are AIOA-native by construction.
> No separate AIOA validation step — each task already embodies AIOA.

Task design rules — every task must respect:

- **Data** → ADTO for all task data — typed + auditable (TIP-007)
- **Communication** → cross-component via events, not direct calls (TIP-008)
- **Component Levels** → task boundaries respect Pico/Nano/Micro (TIP-005)
- **Indirection** → no dead wrapper layers in implementation (TIP-004)
- **Mechanics** → retry/fallback extracted into policies (TIP-006)
- **Types** → value objects, not primitives (TIP-002)
- **Context Budget** → max 7 files per task (TIP-003)

{{CORE_TEMPLATE}}
