# Crystallization Radius — Complete Guide

> *"The amount of additional context an AI agent must consume before making a safe change."*

**Version:** 1.0.0

---

## Table of Contents

1. [What is Crystallization Radius?](#what-is-crystallization-radius)
2. [Why It Matters for AI Agents](#why-it-matters-for-ai-agents)
3. [Measuring Crystallization Radius](#measuring-crystallization-radius)
4. [The Three Rating Levels](#the-three-rating-levels)
5. [Minimization Techniques](#minimization-techniques)
6. [Tracking Over Time](#tracking-over-time)
7. [Context Budget System](#context-budget-system)
8. [Tooling and Automation](#tooling-and-automation)
9. [Examples](#examples)
10. [Anti-Patterns](#anti-patterns)

---

## What is Crystallization Radius?

**Crystallization Radius** is a formal measure of how much additional context an AI agent must consume before making a safe change to a component. It is a property of the **interface between a component and the rest of the system**.

### Formal Definition

For any component `C`, let:

- `Context(C)` = The set of source files, documentation, type definitions, configuration, and architectural knowledge an agent must load to modify `C` without breaking the system.
- `Surface(C)` = The public interface of `C` — its exported types, functions, and behaviors that consumers depend on.

The Crystallization Radius `R(C)` is the ratio:

```
R(C) = |Context(C)| / |Surface(C)|
```

In practice, since `|Context(C)|` is easier to reason about as an absolute count, we measure it in **context units**.

### Measurement Unit

**1 Context Unit (CU)** = one source file (≤500 lines) + its associated documentation.

| File Type | CU Weight |
|-----------|-----------|
| Source code (>500 lines) | 1 CU per 500 lines (rounded up) |
| Test files | 0.5 CU |
| Configuration files | 0.25 CU |
| Documentation files | 0.25 CU |

### Intuitive Understanding

Think of a component as a crystal in a solution. The "radius" is how far you must look from the crystal to understand its environment:

- **Small radius:** The crystal is isolated. You understand it by looking at it alone.
- **Large radius:** The crystal is entangled. You must understand much of the surrounding solution to touch it safely.

---

## Why It Matters for AI Agents

| Cost Factor | Low Radius (1–3) | Medium Radius (4–8) | High Radius (9+) |
|------------|------------------|---------------------|------------------|
| **Context loading time** | Seconds | Minutes | May hit context limits |
| **Risk of missed context** | Very low | Moderate | High |
| **Regression probability** | <1% | 5–15% | 30%+ |
| **Human review needed** | Optional | Recommended | Mandatory |
| **Agent confidence** | High | Moderate | Low |

### The Problem of Cascading Context

High Crystallization Radius has a compounding effect: when an agent must understand module A, which requires understanding module B, which requires understanding module C, the context chain grows exponentially with each dependency.

AIOA's Crystallization Radius principle breaks these chains by:
1. Making dependencies explicit so the chain is visible
2. Minimizing transitive context through narrow interfaces
3. Enforcing context budgets per component

---

## Measuring Crystallization Radius

```
Component: UserAuthentication  (src/auth/user-auth.ts)

Direct dependencies (5):
  src/auth/session.ts, src/auth/password.ts, src/user/user-repo.ts,
  src/shared/types/user.ts, src/config/auth.config.ts

Transitive dependencies (3):
  session.ts → src/shared/crypto.ts, src/config/session.config.ts
  user-repo.ts → src/db/connection.ts

Implicit dependencies (4):
  global event bus, environment variables, API contract, logging convention

Total Context = Direct(5) + Transitive(3) + Implicit(4) = 12 CU
Rating: HIGH (≥9)
```

**Context surface:** 3 dependency layers (direct → transitive → implicit). Agent loads 12 files before safely modifying this component.

---

## The Three Rating Levels

| Rating | Radius | Characteristics | Example |
|--------|--------|----------------|---------|
| 🟢 LOW | 1–3 | Self-contained, minimal ext. deps, changes have low side-effect risk | `EmailValidator` — 2 files: self + shared type |
| 🟡 MEDIUM | 4–8 | Several well-defined deps, moderate preparation, some cross-module understanding | `OrderService` — 6 files across 3 modules |
| 🔴 HIGH | 9+ | Entangled with many parts, extensive context, **architecture review required** | `LegacyOrderManager` — 14 files, 3 dep layers |

### Typical Candidates

| Rating | Candidates |
|--------|-----------|
| LOW | Pure utility functions, leaf components, value objects, domain primitives |
| MEDIUM | Services with injected dependencies, aggregate roots, controllers with well-defined deps |
| HIGH | God classes/modules, cross-cutting concerns, components with implicit deps and global state |

### Rating Migration Rules

| Current | New Change | Recommended Action |
|---------|-----------|-------------------|
| 🟢 LOW | Stays LOW | No action needed |
| 🟢 LOW → 🟡 MEDIUM | Document new context budget |
| 🟡 MEDIUM | Stays MEDIUM | No action needed |
| 🟡 MEDIUM → 🔴 HIGH | Architecture review required |
| 🔴 HIGH | Stays HIGH | Plan refactoring to reduce |
| 🔴 HIGH → 🟡 MEDIUM | Verify no regression |

---

## Minimization Techniques

### Technique 1: Dependency Inversion

Reduction: 30–50%

```typescript
// Problem: concrete deps pull in transitive chains. Solution: depend on interfaces.
// BAD:
class OrderService { constructor(private db: PostgreSQLRepository) {} }

// GOOD:
class OrderService { constructor(private orders: OrderRepository) {} }
```

### Technique 2: Narrow Interfaces

Reduction: 40–60%

```typescript
// Problem: wide interface exposes 15 methods, each with its own context.
// Solution: split by role into small interfaces.
// BAD:
interface UserService { createUser(); updateUser(); deleteUser(); getUser(); listUsers(); banUser(); unbanUser(); /* 8 more */ }
// GOOD:
interface UserCreator { create(data: CreateUserInput): User; }
interface UserQuery   { findById(id: UserId): User | null; }
interface UserAdmin   { suspend(id: UserId): void; }
```

### Technique 3: Explicit Dependency Declaration

Reduction: 20–40%

```typescript
// Problem: implicit deps (global logger, env vars, event bus) require tribal knowledge.
// Solution: inject all dependencies via constructor.
// BAD:
class PaymentProcessor {
  processPayment(amount: number): void {
    logger.info(`Processing payment: ${amount}`);
    const apiKey = process.env.PAYMENT_API_KEY;
    eventBus.emit('payment.processed', { amount });
  }
}
// GOOD:
class PaymentProcessor {
  constructor(
    private readonly logger: Logger,
    private readonly config: PaymentConfig,
    private readonly events: EventPublisher
  ) {}
  processPayment(amount: number): void {
    this.logger.info(`Processing payment: ${amount}`);
    this.events.publish(new PaymentProcessed(amount));
  }
}
```

### Technique 4: Locality of Behavior

Reduction: 50%+

```typescript
// Problem: related behavior scattered across codebase (4 dirs for "email").
// Solution: keep related files in one directory.
// BAD: src/validation/email.ts, src/notifications/email.ts, src/user/email.ts, src/templates/email.ts
// GOOD: src/email/ { email.ts, email-sender.ts, email-preferences.ts, email-templates.ts }
```

### Technique 5: Context Budget Annotations

Reduction: N/A (makes radius visible — prevents surprise expansion)

```typescript
/**
 * @context-budget
 * To modify this module, also read:
 * - src/shared/types/user.ts
 * - src/auth/session.ts
 * - src/config/auth.config.ts
 *
 * Crystallization Radius: MEDIUM (5 files)
 */
export class UserService { /* ... */ }
```

---

## Tracking Over Time

### Trend Analysis

```
Component: UserAuthentication
Date       | Radius | Rating | Event
2026-01-15 | 8      | MEDIUM | Initial measurement
2026-02-20 | 9      | HIGH   | Added payment integration
2026-03-10 | 11     | HIGH   | Added notification hooks
2026-04-05 | 12     | HIGH   | Added audit logging (implicit)
2026-05-01 | 10     | HIGH   | Refactored: extracted audit
2026-05-30 | 12     | HIGH   | Added ML scoring dependency

Trend: WORSENING — requires architectural intervention
```

### Regression Alerts

Any change that increases a component's Crystallization Radius should trigger:

1. **🟢 GREEN** (+0): Acceptable — no change
2. **🟡 YELLOW** (+1–2): Warning — document why increase was necessary
3. **🔴 RED** (+3+): Blocking — requires architecture review

---

## Context Budget System

Every component has a **context budget** — the maximum CU an agent needs to work safely.

Example: `max_units: 8, current: 5, warning_at: 6, critical_at: 8`

### Budget Allocation

| Task | Context Budget | Files | Rating |
|------|---------------|-------|--------|
| Add email validation | 2 units | `EmailValidator`, types | LOW |
| Add payment flow | 7 units | 7 files across 3 modules | MEDIUM |
| Refactor auth | 12 units | 12 files across 5 modules | HIGH (SPLIT) |

### Enforcing Budgets

Budgets enforced during: **Planning** (split if exceeded), **Code review** (flag unjustified increases), **CI pipeline** (automated delta checks).

---

## Tooling and Automation

### Automated Measurement

AIOA prescribes tools to automatically measure Crystallization Radius:

- **Import graph analysis** — map all import relationships
- **Dependency depth calculation** — measure transitive dependency chains
- **Implicit dependency detection** — flag global state, ambient context, conventions
- **Context budget validation** — compare measurements against declared budgets

### CI Integration

- `aioa measure-radius --diff HEAD~1` on every pull request
- `aioa check-budgets` to validate against declared budgets
- `aioa flag-regressions --threshold 2` to catch increases ≥2 CU
- Block merges exceeding critical thresholds (🔴 RED alerts)

---

## Examples

### Example 1: Well-Structured Service (MEDIUM)

```typescript
/**
 * Manages user registration workflow.
 * @context-budget
 * - self: src/users/registration.ts
 * - domain: src/users/user.ts
 * - repository: src/users/user-repository.ts (interface)
 * - auth: src/auth/password-hasher.ts (interface)
 * - notification: src/notifications/email-sender.ts (interface)
 * - types: src/shared/types/user.ts
 * Crystallization Radius: MEDIUM (6 units)
 */
export class RegistrationService {
  constructor(
    private readonly users: UserRepository,
    private readonly hasher: PasswordHasher,
    private readonly mailer: EmailSender
  ) {}

  async register(input: RegistrationInput): Promise<User> {
    // Depends on interfaces, not implementations
    // No transitive dependency leakage
    // All dependencies explicit via constructor
  }
}
```

**Context surface:** All dependencies are narrow interfaces — no transitive leakage.

### Example 2: Entangled Legacy Module (HIGH) — Demonstrates Refactoring

```typescript
/**
 * Manages orders (too many responsibilities).
 *
 * @context-budget
 * - self: src/orders/order-manager.ts
 * - model: src/orders/order.ts
 * - db: src/db/postgres-connection.ts
 * - payment: src/payments/stripe-client.ts
 * - inventory: src/inventory/stock-checker.ts
 * - shipping: src/shipping/shipping-calculator.ts
 * - notification: src/notifications/email-builder.ts
 * - audit: src/audit/audit-logger.ts
 * - config: src/config/order.config.ts
 * - events: src/events/event-bus.ts
 * - types: src/shared/types/order.ts
 * - caching: src/cache/redis-cache.ts
 *
 * Crystallization Radius: HIGH (12 units)
 *
 * Refactoring plan:
 * 1. Extract payment processing → PaymentService (3 units)
 * 2. Extract shipping logic → ShippingService (3 units)
 * 3. Extract notification → NotificationService (2 units)
 * 4. Keep core order logic → OrderService (4 units)
 * Target: 4 components, average radius 3 units
 */
export class OrderManager {
  // ... too many responsibilities
}
```

**Context surface (before):**
```
OrderManager → PostgreSQL → (connection config, queries)
             → Stripe → (API client, webhooks)
             → StockChecker → (database, caching)
             → ShippingCalculator → (rates API, rules)
             → EmailBuilder → (templates, sending)
             → AuditLogger → (database, schema)
             → EventBus → (event types, handlers)
             → Redis → (connection, serialization)
             → Config → (env vars, secrets)
```

**Context surface (after refactoring):**
```
OrderService → OrderRepository (interface)
             → PaymentService (interface)
             → ShippingService (interface)
             → NotificationService (interface)
```

---

## Anti-Patterns

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| **The God Module** — everything imports from it | Module appears in 50%+ of dependency lists | Split into focused sub-modules |
| **Implicit Context Ocean** — "everyone knows" conventions, global state | Module X breaks Y with no visible dependency | Make all deps explicit; inject instead of global state |
| **Deep Inheritance Chains** — subclass requires understanding entire ancestor chain | Class hierarchies with depth > 3 | Prefer composition; flatten hierarchies |
| **Context-Free Interfaces** — no documented context requirements | No `@context-budget` annotations | Add annotations to every public interface |
| **Happy-Path Architecture** — error handling scattered as afterthought | Error handling far from producing logic | Use result types; locate error handling near source |
