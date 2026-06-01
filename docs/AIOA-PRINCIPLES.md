# AI-Oriented Architecture (AIOA) — Full Principles Reference

**Version:** 2.0.0  
**Author:** undef16

---

## Table of Contents

1. [What is AIOA?](#what-is-aioa)
2. [Core Constraints](#core-constraints)
3. [The 10 Principles](#the-10-principles)
   - [P1: Local Reasoning](#p1-local-reasoning)
   - [P2: Crystallization Radius](#p2-crystallization-radius)
   - [P3: Semantic Integrity](#p3-semantic-integrity)
   - [P4: Boundaries Explicit](#p4-boundaries-explicit)
   - [P5: Contracts Deterministic](#p5-contracts-deterministic)
   - [P6: Declarative Straight-Line](#p6-declarative-straight-line)
   - [P7: Reasoning Boundaries not Deployment](#p7-reasoning-boundaries-not-deployment)
   - [P8: Extract Under Reuse Pressure](#p8-extract-under-reuse-pressure)
   - [P9: Event Boundaries](#p9-event-boundaries)
   - [P10: Runtime State Explainable](#p10-runtime-state-explainable)
4. [The 9 Review Gates](#the-9-review-gates)
5. [Key TIPs](#key-tips)
6. [Common Anti-Patterns](#common-anti-patterns)
7. [Case Studies](#case-studies)

---

## What is AIOA?

**AI-Oriented Architecture (AIOA)** is an architectural approach designed for a world where AI agents write, review, and maintain code alongside humans. Traditional architecture patterns optimize for human comprehension — reading code, understanding intent, navigating complexity through human intuition. AIOA optimizes for **predictable, safe AI intervention** — where every architectural decision is measured by how easily an AI agent can understand, modify, and verify it. AIOA makes context comprehension a first-class architectural concern through **10 principles**, **2 core constraints**, and **9 review gates**.

## Core Constraints

### C1: Minimize Crystallization Radius

> *"Every architectural decision SHALL minimize the context an AI agent must consume before making a safe change."*

Crystallization Radius is the primary measurable metric of architectural quality in AIOA. It is the foundation upon which all other principles rest. A system with low Crystallization Radius is inherently more AI-safe than one with high Crystallization Radius, regardless of other qualities.

### C2: Preserve Semantic Integrity

> *"Every architectural decision SHALL preserve meaning across component boundaries."*

Semantic Integrity ensures that data and behavior that cross boundaries retain their full semantic fidelity. Without this constraint, components can drift apart silently, breaking the system in ways that are invisible to AI agents operating within bounded context windows.

These two constraints are universal — they apply to every decision, every component, every boundary.

---

## The 10 Principles

### P1: Local Reasoning

> *"Code should be understandable from local context alone."*

#### Definition

A module SHOULD be understandable by reading only that module and its immediate dependencies. An AI agent SHOULD NOT need to load unrelated parts of the codebase to understand what a module does or how to modify it.

#### Obligations

1. Every function SHALL be understandable without reading callers or callees across module boundaries.
2. Dependencies that require loading more than one level deep SHALL be justified with a documented rationale.
3. No module SHALL require understanding of global state, ambient conventions, or runtime configuration to be understood locally.
4. Side effects SHOULD be declared at the function signature level (return types or effect types).

#### Techniques

- **Avoid module-level state** — State at module level forces readers to understand the entire module lifecycle.
- **Declare all inputs** — A function that reads from environment variables, global caches, or thread-local storage without declaring them breaks local reasoning.
- **Pure functions first** — Pure functions are the gold standard for local reasoning. Everything needed to understand them is in their signature.
- **Limit cross-module references** — If a function references types or functions from other modules, those references should be obvious from the import statements alone.

#### Anti-Patterns

- **Tentacle function** — Reaches deep into other modules' internals
- **Runtime config deep in logic** — `process.env.X` in business logic
- **Callback hell** — Deeply nested callbacks obscuring control flow

---

### P2: Crystallization Radius

> *"Minimize the context an agent must consume before making a safe change."*

#### Formal Definition

For the formal definition of Crystallization Radius `R(C)`, its measurement methodology, rating system, and minimization techniques, see [CRYSTALLIZATION-RADIUS.md](./CRYSTALLIZATION-RADIUS.md).

**Key metric:** `R(C) ≤ 8` for all components (MEDIUM threshold).

#### Obligations

1. Every public interface SHALL be annotated with its context budget.
2. No change SHALL increase the Crystallization Radius of any component without explicit architectural review.
3. Components with a **HIGH** Crystallization Radius rating (>8 context units) SHALL be refactored until they achieve a **MEDIUM** or **LOW** rating. See the [rating system](./CRYSTALLIZATION-RADIUS.md#the-three-rating-levels).
4. Cross-cutting concerns SHALL be explicitly declared, never implicit.
5. Context budgets SHALL be tracked over time to detect architectural erosion.

#### Techniques

1. **Narrow, Deep Interfaces** — Expose 3 focused functions instead of 15 shallow ones.
2. **Explicit Dependency Declaration** — Every dependency is declared in machine-readable form.
3. **Context Budget Annotations** — Every module documents its context cost.
4. **Locality of Behavior** — Related behavior lives close together in the codebase.
5. **Implicit Context Elimination** — Global state, ambient conventions, shared mutable data are replaced with explicit alternatives.

---

### P3: Semantic Integrity

> *"Preserve meaning across architectural boundaries."*

#### Definition

Data and behavior that cross component boundaries must retain their meaning. A `User` in module A is the same `User` in module B — with the same properties, invariants, and lifecycle.

#### The Problem of Semantic Drift

Semantic drift occurs when:
- The same concept has different representations in different modules
- Data is silently transformed between components
- Validation or interpretation is applied inconsistently
- Contracts change in one module without corresponding updates in consumers

#### Obligations

1. All data crossing component boundaries SHALL use shared, versioned semantic types.
2. No component SHALL silently reinterpret, reshape, or transform data from another component.
3. Validation SHALL happen at boundaries only (Parse, Don't Validate).
4. Semantic contracts SHALL be enforced by automated gates.
5. Cross-boundary invariants SHALL be documented and tested.

#### Layers of Semantic Integrity

| Layer | What It Protects | Enforcement |
|-------|-----------------|-------------|
| **Type Integrity** | Data shape | Shared type definitions, schema validation |
| **Behavioral Integrity** | Operations & effects | Interface contracts, pre/post conditions |
| **Conceptual Integrity** | Domain meaning | Ubiquitous language, shared vocabulary |
| **Invariant Integrity** | System-wide rules | Architectural tests, property-based testing |

#### Key Pattern: Boundary Parser

```
External World → [Parse] → Trusted Internal State → [Business Logic] → [Serialize] → External World
```

Parse at the boundary, trust internally. See TIP-007 for implementation guidance.

---

### P4: Boundaries Explicit

> *"All component boundaries must be clearly declared."*

#### Definition

Every architectural boundary SHALL be explicitly declared with a name, responsibility, and interface contract. No implicit boundaries based on conventions, directory structure, or tribal knowledge.

#### Obligations

1. Every component SHALL have a declared boundary with a clear responsibility statement.
2. Cross-boundary access SHALL only occur through declared interfaces, never through internal implementation details.
3. No implicit boundaries — conventions, naming patterns, or directory structures SHALL NOT be used as substitutes for explicit boundary declarations.
4. Boundary violations SHALL be detected and flagged in code review.
5. Each boundary SHALL document its context cost (files an agent must load to cross it safely).

#### Implementation

```yaml
# Example boundary declaration
boundaries:
  - name: "UserManagement"
    responsibility: "Create, read, update, and deactivate user accounts"
    context_cost: 4
    interfaces:
      - name: "UserRepository"
        file: "src/user/user-repository.ts"
      - name: "UserAuthService"
        file: "src/user/user-auth-service.ts"
    dependencies:
      - "AuthService"
      - "NotificationService"
```

#### Anti-Patterns

- **Invisible boundary** — Boundaries exist only in developer docs, not code
- **Convention boundary** — "All files in `src/services/` are a module" with no explicit declaration
- **Leaky boundary** — Components access each other's internal files directly

---

### P5: Contracts Deterministic

> *"Interfaces must have deterministic, machine-verifiable contracts."*

#### Definition

Every interface between components SHALL be defined with a contract that can be verified automatically — not just by human code review. Contracts include types, preconditions, postconditions, and invariant guarantees.

#### Obligations

1. Every interface SHALL have a schema or type definition that can be validated at runtime.
2. Contract violations SHALL be detected at CI time or at boundary crossing time, never silently ignored.
3. Interfaces SHOULD use runtime-verifiable schemas (Zod, TypeBox, OpenAPI, JSON Schema).
4. Breaking changes to contracts SHALL require a version bump and coordinated migration.
5. Consumer-driven contracts SHOULD be used to verify providers satisfy consumer expectations.

#### Implementation Patterns

**Runtime-verifiable schemas (see TIP-007):**

```typescript
import { z } from 'zod';

// Deterministic contract — machine-verifiable
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  displayName: z.string().min(1).max(100),
  status: z.enum(['active', 'inactive', 'suspended']),
});

export type User = z.infer<typeof UserSchema>;

// Validation at boundary — deterministic, no human judgment needed
export function parseUser(data: unknown): User {
  return UserSchema.parse(data);
}
```

**Consumer-driven contracts:**

Each consumer defines the contract it expects, and the provider is tested against all consumer contracts. This ensures that no provider change breaks a consumer without detection.

---

### P6: Declarative Straight-Line

> *"Prefer linear, declarative code over complex control flow."*

#### Definition

Code SHOULD be written as straight-line, declarative logic rather than deeply nested conditional branches, complex loops, or mutation-heavy control flow. This makes code easier for AI agents to reason about.

#### Obligations

1. Deeply nested conditionals (depth > 3) SHALL be refactored into guard clauses or early returns.
2. Complex loop logic SHOULD be replaced with declarative operations (map, filter, reduce, flatMap).
3. Mutable state SHOULD be localized and minimized; prefer immutable data structures.
4. Control flow SHOULD be linear — avoid `goto`-like patterns, long-range breaks, and deep callback chains.
5. Asynchronous control flow SHOULD use async/await rather than raw promises or callbacks.

#### Examples

**Before — deeply nested imperative:**
```typescript
function processOrders(orders: Order[]): ProcessedOrder[] {
  const result = [];
  for (let i = 0; i < orders.length; i++) {
    if (orders[i].status === 'pending') {
      if (orders[i].amount > 100) {
        if (orders[i].customer.tier === 'premium') {
          result.push(/* premium processing */);
        } else {
          result.push(/* standard processing */);
        }
      }
    }
  }
  return result;
}
```

**After — straight-line declarative:**
```typescript
function processOrders(orders: Order[]): ProcessedOrder[] {
  return orders
    .filter(order => order.status === 'pending')
    .map(order => order.amount > 100 && order.customer.tier === 'premium'
      ? processPremium(order)
      : processStandard(order)
    );
}
```

---

### P7: Reasoning Boundaries not Deployment (Architectural Independence)

> *"Logical architecture is orthogonal to deployment topology."*

#### Definition

This project's logical architecture SHALL NOT depend on or assume any specific deployment topology (monolith, microservices, serverless, etc.). Components are defined by reasoning boundaries — the amount of context needed to understand them — not by deployment boundaries.

#### Why It Matters

Conflating logical architecture with deployment topology creates lock-in (hard to migrate between monolith, microservices, serverless), testing difficulty, and AI confusion. Components defined by semantic responsibility rather than infrastructure topology can migrate between deployment models by changing configuration alone.

#### Obligations

1. Components SHALL depend on interfaces, not infrastructure.
2. No component SHALL reference network protocols, message queues, or deployment infrastructure in its core logic.
3. Deployment topology SHALL be a configuration concern managed at the deployment boundary.
4. Module boundaries SHALL be semantic, not physical.
5. The same logical components SHALL be deployable in different topologies by changing configuration, not code.

#### Verification

For each component, ask:
1. "Would this component change if we moved from monolith to microservices?" → If yes, deployment topology is leaking into the component.
2. "Does this component reference any infrastructure library directly?" → If yes, infrastructure is coupled into logic.
3. "Could this component's tests run without infrastructure?" → If no, the component depends on deployment-specific resources.
4. "Are interfaces defined by the consumer or by the infrastructure?" → If by infrastructure, the component is coupled to deployment concerns.

---

### P8: Extract Under Reuse Pressure

> *"Don't abstract until reuse pressure exists."*

#### Definition

Abstractions, shared utilities, and common modules SHALL NOT be created proactively. They SHALL only be extracted when concrete reuse pressure exists — proven reuse or isolation pressure from multiple independent use cases.

#### Obligations

1. No abstraction SHALL be created speculatively ("we might need this later").
2. Extraction to a shared module SHALL require proven reuse or isolation pressure from multiple independent use cases.
3. Premature abstractions SHALL be flagged in code review and inlined.
4. Shared modules extracted under pressure SHALL document their reuse context.
5. Monoculture (everyone depending on a single shared module) SHALL be avoided — prefer focused, purpose-built abstractions.

#### Decision Framework

```
Is there reuse pressure?
├── No → Keep code inlined. Duplication is acceptable.
├── Yes, proven reuse or isolation pressure → Consider extraction.
│   ├── Are the consumers truly independent?
│   │   ├── Yes → Extract with clear interface.
│   │   └── No → Keep inlined (shared context may change together).
│   └── Is the abstraction stable?
│       ├── Yes → Extract and freeze interface.
│       └── No → Defer extraction until stability emerges.
└── Yes, emerging reuse or isolation pressure → Document as "pending extraction."
```

#### Anti-Patterns

- **Shared utils module** — Everything imports from `src/shared/utils.ts`
- **Premature interface** — Single-implementation interface "for flexibility"
- **Speculative generics** — Unused generic type parameters "just in case"
- **Framework fetish** — Abstraction frameworks adopted before concrete reuse exists

---

### P9: Event Boundaries

> *"Use event bus for cross-component communication, not direct calls."*

#### Definition

Components SHOULD communicate through an event bus or message passing, not through direct function calls across component boundaries. This preserves the ability to deploy components independently and maintains loose coupling.

#### Why It Matters

Direct cross-component calls increase Crystallization Radius, create implicit temporal dependencies, and force agents to trace execution across boundaries. Event-driven communication makes interactions explicit, reduces context requirements by letting agents work on one side of the boundary, and enables independent evolution.

#### Obligations

1. Cross-component communication SHOULD use an event bus or message broker, not direct imports.
2. Events SHALL be versioned and governed by semantic contracts (see P3, P5).
3. Synchronous cross-component calls SHALL be justified with documented rationale.
4. Event schemas SHALL be defined in shared contract packages.
5. Event handlers SHALL be idempotent where possible.

#### Implementation (see TIP-008)

```
┌──────────────┐   publish    ┌──────────────┐   handle    ┌──────────────┐
│ Component A  │ ──────────→ │  Event Bus   │ ──────────→ │ Component B  │
│              │             │              │             │              │
│ (producer)   │             │ (broker)     │             │ (consumer)   │
└──────────────┘             └──────────────┘             └──────────────┘
```

Event schemas are defined in shared contracts:

```typescript
// shared/events/user-events.ts
export interface UserCreatedEvent {
  eventType: 'user.created';
  version: 1;
  payload: {
    userId: string;
    email: string;
    createdAt: string;
  };
}
```

#### When Direct Calls Are Acceptable

Direct synchronous calls between components may be acceptable when:
- The call is within the same reasoning boundary (same component, internal call)
- Latency requirements preclude event bus overhead
- The operation is query-only (no mutation)
- Documented rationale exists for the exception

---

### P10: Runtime State Explainable

> *"Runtime state must be explainable and auditable."*

#### Definition

Every component's runtime state SHALL be explainable — able to answer "what is the current state and how did it get here?" — and auditable — able to trace state changes back to their origin. This follows the **Auditable DTO (ADTO)** pattern.

> **In practice:** ADTO with provenance tracking has reduced state-related debugging time by 70% and enabled AI agents to reason about system state from code alone.

#### Obligations

1. Every state mutation SHALL be logged with a provenance record (who, what, when, why).
2. Runtime state SHALL be inspectable without side effects.
3. State transitions SHALL follow the ADTO pattern: each DTO carries a `_provenance` field with version, timestamp, and origin.
4. Immutable event sourcing SHOULD be preferred over mutable state where feasible.
5. State inspection endpoints or tools SHALL be available in all environments.

#### The ADTO Pattern (see TIP-009)

Every DTO that crosses a component boundary or represents persisted state carries a `_provenance` field:

```typescript
interface AuditableDTO {
  // Business data
  userId: string;
  email: string;
  displayName: string;

  // Provenance (ADTO)
  _provenance: {
    version: 1;            // Schema version
    createdAt: string;     // ISO 8601
    updatedAt: string;     // ISO 8601
    createdBy: string;     // Component or user
    traceId: string;       // Correlation ID
    mutations: Array<{     // Change history
      field: string;
      from: unknown;
      to: unknown;
      timestamp: string;
      reason: string;
    }>;
  };
}
```

#### Techniques

- **Event sourcing** — Store state changes as an immutable event log. Current state is derived from replaying events.
- **State inspection endpoints** — Expose `GET /state` endpoints that return current state without side effects.
- **Provenance logging** — Every state mutation records its origin, timestamp, and rationale.
- **Snapshot with history** — For performance, maintain state snapshots with pointers to historical events.

---

## The 9 Review Gates

Every change in an AIOA-governed system passes through 9 review gates. Each gate produces a score: **Pass**, **Partial**, or **Fail**.

| # | Gate | Question | Pass Criteria |
|---|------|----------|---------------|
| 1 | **Crystallization Radius** | Did context budget increase? | No regression, or regression with justification |
| 2 | **Semantic Integrity** | Is meaning preserved? | Shared types consistent, no silent transformations |
| 3 | **Local Reasoning** | Can code be understood locally? | Functions understandable without external context |
| 4 | **Boundary Explicitness** | Are all boundaries declared? | Every boundary has name, responsibility, interface |
| 5 | **Contract Determinism** | Are interfaces machine-verifiable? | Every interface has runtime-verifiable schema |
| 6 | **Control-Flow Simplicity** | Is code straight-line? | No nesting >3, declarative over imperative |
| 7 | **Decomposition Quality** | Is granularity appropriate? | Components neither god modules nor atomized |
| 8 | **Integration Locality** | Are integrations local/explicit? | Integrations declared at point, no transitive chains |
| 9 | **Runtime Explainability** | Can state be explained? | Provenance tracked, state inspectable |

### Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| **PASS** | Gate satisfied | No action needed |
| **PARTIAL** | Minor issue | Document and address |
| **FAIL** | Gate violated | Must fix before merge |

A change with any **FAIL** gate score is **REJECTED**. A change with more than 2 **PARTIAL** scores requires architecture review.

---

## Key TIPs

### TIP-002: Semantic Collision

When multiple domain concepts are linguistically similar, AI agents silently collapse them into a single identifier. The code remains syntactically correct, type-safe, and passing tests — but business semantics are gone.

**Rules:**
- Never expose primitive types (`str`, `int`, `dict`) in domain-critical flows — use value objects
- Treat naming as architecture, not cosmetics — similar names cause silent logic corruption
- Add semantic validation to AI-generated code — the compiler protects syntax, not meaning
- Strictly separate bounded contexts — no duplicate definitions of the same concept

**Example violation:**
```python
# WRONG — three concepts collapsed into one type
call_id: str      # could be "C001"
trace_id: str     # could also be "C001" — collision!
customer_id: str  # could also be "C001" — collision!

# CORRECT — value objects prevent collision
class CallId(str): ...
class TraceId(str): ...
class CustomerId(str): ...
```

### TIP-007: Strict JSON Gateways

All component boundaries SHALL validate data using strict, runtime-verifiable schemas (Zod, TypeBox, OpenAPI, JSON Schema). No unvalidated data SHALL cross a component boundary. Parse at the gateway, trust internally.

**Implementation:**
- Every boundary has a schema-defined gateway
- Gateway validates all incoming and outgoing data
- Internal logic operates on trusted types only
- Schema changes are treated as contract changes (bump version)

### TIP-008: Event-Driven Integration

Cross-component communication SHOULD use an event bus with versioned event schemas. Direct synchronous calls between components SHALL be exceptions with documented rationale.

**Implementation:**
- Define event schemas in shared contract packages
- Components publish and subscribe through an event bus
- Event handlers are idempotent
- Direct calls are documented exceptions

### TIP-009: Auditable DTOs (ADTO)

Every DTO that crosses a component boundary or represents persisted state SHALL carry a `_provenance` field containing:
- `version` — schema version of this DTO
- `timestamp` — ISO 8601 timestamp of creation/last mutation
- `origin` — component or service that created this DTO
- `trace_id` — correlation ID linking this DTO to its originating operation

**Implementation:**
- Add `_provenance` to all boundary DTOs
- Mutations append to provenance history
- State inspection tools expose provenance
- Tests verify provenance completeness

## Common Anti-Patterns

| Anti-Pattern | Symptom | Violated Principles | AIOA Solution |
|-------------|---------|-------------------|---------------|
| God Module | One file/module handles everything, `R(C) > 15` | P1, P2, P4, P7 | Decompose by reasoning boundaries, budget ≤8 |
| Silent Coupling | Modules share global state via registry/singleton | P1, P4 | Replace global state with explicit DI |
| Topology-First Design | Component boundaries match deployment boundaries exactly | P7 | Design by semantic cohesion, not topology |
| Semantic Drift | Same concept represented differently across modules | P3, P5 | Shared types, parse at boundaries (TIP-007) |
| Context Hoarding | All modules depend on shared "utils" | P1, P2 | Split into focused libraries, invert deps |
| Premature Abstraction | Interfaces with single implementation "for flexibility" | P8 | Keep concrete until reuse pressure exists |
| Synchronous Spaghetti | A→B→C→A circular cross-component calls | P6, P9 | Break with events (TIP-008) |
| Black Box State | Runtime state not inspectable, mutations not logged | P10 | ADTO pattern with provenance (TIP-009) |
| Semantic Collision | Primitive types in domain flows, similar naming causes silent corruption | P3, P5 | Value objects for domain IDs, typed structures over `dict` |

---

## Case Studies

### Case Study 1: Refactoring toward Low Crystallization Radius

**Before:** A monolithic user management module with `R(C) = 18`
- 12 direct file dependencies
- 6 implicit dependencies (global event bus, shared config, convention-based routing)
- Any change required understanding 18 related files
- Violations: P1 (not locally understandable), P2 (high radius), P4 (boundaries not explicit)

**After AIOA Refactoring:**
- Split into 3 components: `UserCore (R=3)`, `UserAuth (R=4)`, `UserProfile (R=3)`
- Implicit dependencies made explicit via interface injection
- Boundaries declared for each component
- Context budget reduced from 18 to average of 3.3

**Result:** 5.5× reduction in context requirements for AI agents

### Case Study 2: Semantic Integrity Rescue

**Before:** An e-commerce system where `Order` had different meanings in 4 services:
- Order Service: full order with line items, pricing, status
- Payment Service: order = payment transaction reference
- Shipping Service: order = shipment destination + items
- Analytics: order = completed transaction record

Changes frequently broke downstream consumers. Violations: P3 (semantic drift), P5 (no deterministic contracts)

**After AIOA Implementation:**
- Shared `Order` schema defined once, imported across services
- Each service parsed the shared order into its own trusted representation
- Semantic integrity tests verified round-trip preservation
- Interfaces gained machine-verifiable contracts

**Result:** Cross-service breakage reduced by 90%
