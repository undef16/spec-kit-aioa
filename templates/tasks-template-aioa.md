---
# AIOA Wrap — Wraps around core tasks-template.md
# Reference: docs/AIOA.md — Technical Implementation Patterns
---

> **AIOA Preset Active** — Tasks are AIOA-native by construction.
> No separate AIOA validation step — each task already embodies AIOA.

Task design rules:
- Every task must respect AIOA TIPs
- Every task MUST include `.signatures:` listing all classes, methods (with parameters), types, and functions it introduces
- Code review syncs these signatures with actual implementation
- For the full list of TIPs and their definitions, see [AIOA.md](../docs/AIOA.md)

Language-specific examples:
- **Python**: Reference `docs/py_examples/` — concrete implementations of all TIPs (ADTO, event bus, fee policies, typed identifiers)
- For other languages: create `docs/<language>_examples/` with equivalent implementations following the same TIP structure

{{CORE_TEMPLATE}}
