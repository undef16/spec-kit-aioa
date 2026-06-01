---
# AIOA Wrap — Wraps around core spec-template.md
# Reference: docs/AIOA.md — Technical Implementation Patterns (TIP-002-TIP-008)
---

> **AIOA Preset Active** — All architecture descriptions must be AIOA-native.
> Do NOT create separate "AIOA Compliance" sections. AIOA IS the architecture.

When writing the specification, apply AIOA directly to each architecture layer:

- **Domain Entities** → extend ADTO (typed + auditable, TIP-007)
- **Value Objects** → distinct types per concept, no primitives (TIP-002)
- **Aggregates** → respect Crystallization Radius — max 7 files (TIP-003)
- **Services** → communicate via event bus, even in-memory (TIP-008)
- **Execution Mechanics** → extract retry/fallback into policies (TIP-006)
- **Component Naming** → use Pico/Nano/Micro levels, not "Service" (TIP-005)
- **Crossing Boundaries** → ADTO everywhere, no raw dicts (TIP-007)
- **Indirection** → no dead wrapper layers, call directly (TIP-004)

{{CORE_TEMPLATE}}
