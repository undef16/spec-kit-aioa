---
# AIOA Additions — Appended after core constitution-template.md
# This file contains ONLY AIOA-specific sections that are appended to the core Spec Kit constitution template.
---

> This constitution is governed by the AIOA (AI-Oriented Architecture) preset.
> All 10 AIOA principles are non-negotiable. Additional project-specific principles may be added below.

---

## Core Constraints (AIOA — Non-Negotiable)

### C1: Minimize Crystallization Radius

Every architectural decision SHALL minimize the context an AI agent must consume before making a safe change. Crystallization Radius is the primary measurable metric of architectural quality.

### C2: Preserve Semantic Integrity

Every architectural decision SHALL preserve meaning across component boundaries. Data and behavior that cross boundaries must retain their full semantic fidelity.

---

## The 10 Principles (AIOA — Non-Negotiable)

> Full definitions, obligations, and techniques: [AIOA-PRINCIPLES.md](../docs/AIOA-PRINCIPLES.md)

### P1: Local Reasoning
> *"Code should be understandable from local context alone."*

### P2: Crystallization Radius
> *"Minimize the context an agent must consume before making a safe change."*

### P3: Semantic Integrity
> *"Preserve meaning across architectural boundaries."*

### P4: Boundaries Explicit
> *"All component boundaries must be clearly declared."*

### P5: Contracts Deterministic
> *"Interfaces must have deterministic, machine-verifiable contracts."*

### P6: Declarative Straight-Line
> *"Prefer linear, declarative code over complex control flow."*

### P7: Reasoning Boundaries not Deployment (Architectural Independence)
> *"Logical architecture is orthogonal to deployment topology."*

### P8: Extract Under Reuse Pressure
> *"Don't abstract until reuse pressure exists."*

### P9: Event Boundaries
> *"Use event bus for cross-component communication, not direct calls."*

### P10: Runtime State Explainable
> *"Runtime state must be explainable and auditable."*

---

## Review Gates (AIOA — Non-Negotiable)

> Full gate definitions: [AIOA-PRINCIPLES.md §Review Gates](../docs/AIOA-PRINCIPLES.md#the-9-review-gates)

---

## Decision Framework (AIOA — Non-Negotiable)

Every architectural decision SHALL answer three questions:

### Question 1: Context Surface Area
> *"How much context must an agent consume before making a safe change to this component?"*

| Rating | Threshold | Action |
|--------|-----------|--------|
| **Low** | 1–3 files, 0–1 cross-module dependencies | No action required |
| **Medium** | 4–8 files, 2–3 cross-module dependencies | Document context budget, consider refactor |
| **High** | 9+ files, 4+ cross-module dependencies | Mandatory architecture review, plan refactor |

### Question 2: Semantic Drift Risk
> *"Does this decision risk meaning being lost or transformed across boundaries?"*

If the answer is "yes" or "uncertain," the decision SHALL be deferred until shared semantic types are defined, boundary parsing is documented, and integrity gates are specified.

### Question 3: Deployment Coupling
> *"Does this decision assume a particular deployment topology?"*

If the answer is "yes," the decision SHALL be restructured to extract infrastructure concerns to the deployment boundary and define topology-agnostic interfaces.

---

## TIPs (Technical Implementation Patterns)

> Full TIP definitions: [AIOA-PRINCIPLES.md §TIPs](../docs/AIOA-PRINCIPLES.md#key-tips)

- **TIP-007**: Strict JSON Gateways
- **TIP-008**: Event-Driven Integration
- **TIP-009**: Auditable DTOs
