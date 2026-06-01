---
# AIOA Wrap — Wraps around core plan-template.md
# Reference: docs/AIOA.md — Technical Implementation Patterns (TIP-002-TIP-008)
---

> **AIOA Preset Active** — Every architecture decision IS AIOA-native.
> Do NOT add separate "AIOA Verification" to each ADR — AIOA is expressed IN the decision itself.

For each ADR, apply AIOA directly to the decision:

- **Contracts** → ADTO — typed + auditable (TIP-007)
- **Integration** → event-driven, one mechanism (TIP-008) — InMemoryEventBus by default; use existing broker directly if already present
- **Component Levels** → Pico/Nano/Micro, not "Service" (TIP-005)
- **Crystallization Radius** → each component max 7 files (TIP-003)
- **Abstraction** → no dead wrapper layers (TIP-004)
- **Mechanics** → retry/fallback/timeout extracted into policies (TIP-006)
- **Types** → value objects, not primitives (TIP-002)

{{CORE_TEMPLATE}}
