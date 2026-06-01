---
# AIOA Wrap — Wraps around core constitution-template.md
# Reference: docs/AIOA.md — Technical Implementation Patterns (TIP-002-TIP-008)
---

> **What AIOA IS:** Patterns that make your codebase predictable and safe for AI coding assistants (Claude Code, Copilot, Cursor) to modify.
> **What AIOA IS NOT:** NOT about AI/LLM features inside your application. NOT about AI agents as components.
> 
> This constitution IS AIOA-native. Technical Implementation Patterns: [AIOA.md](../docs/AIOA.md)

The constitution is expressed through AIOA TIPs — no separate compliance section:

- **TIP-002: Semantic Collision** — every domain concept has a distinct type. No primitive obsession.
- **TIP-003: Repository Search Bottleneck** — no module exceeds 7 files. Responsibility is distributed.
- **TIP-004: Code Crystallization** — no dead wrapper chains. Call directly if no value is added.
- **TIP-005: Quantum Spectrum** — components are named by their level: Pico, Nano, Micro.
- **TIP-006: Declarative Straight-Line** — execution mechanics (retry, fallback) are extracted into policies.
- **TIP-007: Auditable Data Transfer Objects** — all boundary data is ADTO: typed + provenance.
- **TIP-008: Event-Driven Integration** — all cross-component communication goes through an event bus. One mechanism — InMemoryEventBus by default; external brokers (RabbitMQ) used directly if already present.

{{CORE_TEMPLATE}}
