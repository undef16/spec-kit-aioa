# [PROJECT_NAME] Constitution

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

### P1: Local Reasoning

> *"Code should be understandable from local context alone."*

A module SHOULD be understandable by reading only that module and its immediate dependencies. An AI agent SHOULD NOT need to load unrelated parts of the codebase to understand what a module does or how to modify it.

**Obligations:**
1. Every function SHALL be understandable without reading callers or callees across module boundaries.
2. Dependencies that require loading more than one level deep SHALL be justified with a documented rationale.
3. No module SHALL require understanding of global state, ambient conventions, or runtime configuration to be understood locally.
4. Side effects SHOULD be declared at the function signature level (return types or effect types).

---

### P2: Crystallization Radius

> *"Minimize the context an agent must consume before making a safe change."*

Every component has a measurable Crystallization Radius — the amount of additional context an AI agent must load beyond the immediate code being changed before that change can be made safely.

**Obligations:**
1. Every public interface SHALL be annotated with its context budget.
2. No change SHALL increase the Crystallization Radius of any component without explicit architectural review.
3. Components with High Crystallization Radius (>8 files context) SHALL be refactored until Medium or Low.
4. Cross-cutting concerns SHALL be explicitly declared, never implicit.
5. Context budgets SHALL be tracked over time to detect architectural erosion.

---

### P3: Semantic Integrity

> *"Preserve meaning across architectural boundaries."*

Data and behavior that cross component boundaries must retain their meaning. A `User` in module A is the same `User` in module B — with the same properties, invariants, and lifecycle.

**Obligations:**
1. All data crossing component boundaries SHALL use shared, versioned semantic types.
2. No component SHALL silently reinterpret, reshape, or transform data from another component.
3. Validation SHALL happen at boundaries only (Parse, Don't Validate — see TIP-007).
4. Semantic contracts SHALL be enforced by automated gates.
5. Cross-boundary invariants SHALL be documented and tested.

---

### P4: Boundaries Explicit

> *"All component boundaries must be clearly declared."*

Every architectural boundary SHALL be explicitly declared with a name, responsibility, and interface contract. No implicit boundaries based on conventions, directory structure, or tribal knowledge.

**Obligations:**
1. Every component SHALL have a declared boundary with a clear responsibility statement.
2. Cross-boundary access SHALL only occur through declared interfaces, never through internal implementation details.
3. No implicit boundaries — conventions, naming patterns, or directory structures SHALL NOT be used as substitutes for explicit boundary declarations.
4. Boundary violations SHALL be detected and flagged in code review.
5. Each boundary SHALL document its context cost (files an agent must load to cross it safely).

---

### P5: Contracts Deterministic

> *"Interfaces must have deterministic, machine-verifiable contracts."*

Every interface between components SHALL be defined with a contract that can be verified automatically — not just by human code review. Contracts include types, preconditions, postconditions, and invariant guarantees.

**Obligations:**
1. Every interface SHALL have a schema or type definition that can be validated at runtime.
2. Contract violations SHALL be detected at CI time or at boundary crossing time, never silently ignored.
3. Interfaces SHOULD use runtime-verifiable schemas (Zod, TypeBox, OpenAPI, etc.) — see TIP-007.
4. Breaking changes to contracts SHALL require a version bump and coordinated migration.
5. Consumer-driven contracts SHOULD be used to verify providers satisfy consumer expectations.

---

### P6: Declarative Straight-Line

> *"Prefer linear, declarative code over complex control flow."*

Code SHOULD be written as straight-line, declarative logic rather than deeply nested conditional branches, complex loops, or mutation-heavy control flow. This makes code easier for AI agents to reason about.

**Obligations:**
1. Deeply nested conditionals (depth > 3) SHALL be refactored into guard clauses or early returns.
2. Complex loop logic SHOULD be replaced with declarative operations (map, filter, reduce, flatMap).
3. Mutable state SHOULD be localized and minimized; prefer immutable data structures.
4. Control flow SHOULD be linear — avoid `goto`-like patterns, long-range breaks, and deep callback chains.
5. Asynchronous control flow SHOULD use async/await rather than raw promises or callbacks.

---

### P7: Reasoning Boundaries not Deployment (Architectural Independence)

> *"Logical architecture is orthogonal to deployment topology."*

This project's logical architecture SHALL NOT depend on or assume any specific deployment topology (monolith, microservices, serverless, etc.). Components are defined by reasoning boundaries, not deployment boundaries.

**Obligations:**
1. Components SHALL depend on interfaces, not infrastructure.
2. No component SHALL reference network protocols, message queues, or deployment infrastructure in its core logic.
3. Deployment topology SHALL be a configuration concern managed at the deployment boundary.
4. Module boundaries SHALL be semantic, not physical.
5. The same logical components SHALL be deployable in different topologies by changing configuration, not code.

---

### P8: Extract Under Reuse Pressure

> *"Don't abstract until reuse pressure exists."*

Abstractions, shared utilities, and common modules SHALL NOT be created proactively. They SHALL only be extracted when concrete reuse pressure exists — at least three independent consumers or clear evidence of duplication causing maintenance burden.

**Obligations:**
1. No abstraction SHALL be created speculatively ("we might need this later").
2. Extraction to a shared module SHALL require at minimum two independent consumers, with a third identified as likely.
3. Premature abstractions SHALL be flagged in code review and inlined.
4. Shared modules extracted under pressure SHALL document their reuse context.
5. Monoculture (everyone depending on a single shared module) SHALL be avoided — prefer focused, purpose-built abstractions.

---

### P9: Event Boundaries

> *"Use event bus for cross-component communication, not direct calls."*

Components SHOULD communicate through an event bus or message passing, not through direct function calls across component boundaries. This preserves the ability to deploy components independently and maintains loose coupling — see TIP-008.

**Obligations:**
1. Cross-component communication SHOULD use an event bus or message broker, not direct imports.
2. Events SHALL be versioned and governed by semantic contracts (see P3, P5).
3. Synchronous cross-component calls SHALL be justified with documented rationale.
4. Event schemas SHALL be defined in shared contract packages.
5. Event handlers SHALL be idempotent where possible.

---

### P10: Runtime State Explainable

> *"Runtime state must be explainable and auditable."*

Every component's runtime state SHALL be explainable — able to answer "what is the current state and how did it get here?" and auditable — able to trace state changes back to their origin. This follows the **Auditable DTO (ADTO)** pattern — see TIP-009.

**Obligations:**
1. Every state mutation SHALL be logged with a provenance record (who, what, when, why).
2. Runtime state SHALL be inspectable without side effects.
3. State transitions SHALL follow the ADTO pattern: each DTO carries a `_provenance` field with version, timestamp, and origin.
4. Immutable event sourcing SHOULD be preferred over mutable state where feasible.
5. State inspection endpoints or tools SHALL be available in all environments.

---

## Project-Specific Principles

### [PRINCIPLE_11_NAME]
[PRINCIPLE_11_DESCRIPTION]
<!-- Project-specific principle placeholder. Add your own principles here. Examples: KISS, DRY, OOP, TDD, etc. -->

### [PRINCIPLE_12_NAME]
[PRINCIPLE_12_DESCRIPTION]
<!-- Project-specific principle placeholder. -->

---

## Review Gates (AIOA — Non-Negotiable)

Every architectural decision, spec, plan, task, and code review SHALL be evaluated against these 9 review gates:

| Gate | Check | Pass/Fail Criteria |
|------|-------|-------------------|
| **Gate 1: Crystallization Radius** | Context budget check | Context budget is documented and within acceptable range |
| **Gate 2: Semantic Integrity** | Shared types and boundary contracts | Meaning is preserved across all boundaries |
| **Gate 3: Local Reasoning** | Can code be understood without external context? | Module is understandable from local context alone |
| **Gate 4: Boundary Explicitness** | Are all boundaries declared? | Every boundary has a name, responsibility, and interface |
| **Gate 5: Contract Determinism** | Are interfaces machine-verifiable? | All interfaces have runtime-verifiable schemas |
| **Gate 6: Control-Flow Simplicity** | Is code straight-line and declarative? | No deeply nested conditionals or complex control flow |
| **Gate 7: Decomposition Quality** | Appropriate granularity? | Components are neither too few (god modules) nor too many (microscopic) |
| **Gate 8: Integration Locality** | Are integrations local and explicit? | Cross-component integrations are declared at the integration point |
| **Gate 9: Runtime Explainability** | Can runtime state be explained? | State is inspectable, auditable, and has provenance tracking |

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

## TIPs Reference

### TIP-007: Strict JSON Gateways
All component boundaries SHALL validate data using strict, runtime-verifiable schemas (Zod, TypeBox, OpenAPI, JSON Schema). No unvalidated data SHALL cross a component boundary. Parse at the gateway, trust internally.

### TIP-008: Event-Driven Integration
Cross-component communication SHOULD use an event bus with versioned event schemas. Direct synchronous calls between components SHALL be exceptions with documented rationale.

### TIP-009: Auditable DTOs (ADTO)
Every DTO that crosses a component boundary or represents persisted state SHALL carry a `_provenance` field containing:
- `version` — schema version of this DTO
- `timestamp` — ISO 8601 timestamp of creation/last mutation
- `origin` — component or service that created this DTO
- `trace_id` — correlation ID linking this DTO to its originating operation

---

## Governance

[GOVERNANCE_RULES]

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
