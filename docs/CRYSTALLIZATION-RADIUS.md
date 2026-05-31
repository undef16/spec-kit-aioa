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

AI agents operate with **bounded context windows**. They cannot hold an entire large codebase in memory simultaneously. Every architectural decision that expands context requirements makes it harder for agents to work safely.

### The Cost of High Crystallization Radius

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

### Step-by-Step Measurement

#### Step 1: Identify the Component

```
Component: UserAuthentication
Files: src/auth/user-auth.ts
Responsibility: Handle user login, logout, session management
```

#### Step 2: Count Direct Dependencies

Files that the component directly imports or references:

```
src/auth/user-auth.ts
  imports:
    - src/auth/session.ts        (1)
    - src/auth/password.ts       (2)
    - src/user/user-repo.ts      (3)
    - src/shared/types/user.ts   (4)
    - src/config/auth.config.ts  (5)
Direct dependency count: 5
```

#### Step 3: Count Transitive Dependencies

Dependencies of dependencies that affect behavior:

```
src/auth/session.ts
  imports:
    - src/shared/crypto.ts       (6)
    - src/config/session.config.ts (7)

src/user/user-repo.ts
  imports:
    - src/db/connection.ts       (8)
    - src/shared/types/user.ts   (already counted)

Transitive new count: 3
```

#### Step 4: Identify Implicit Dependencies

Dependencies not visible in code but required for safe changes:

```
- Global event bus (emits auth events consumed elsewhere)  (9)
- Environment variables expected by auth config             (10)
- API contract with auth service (if deployed separately)  (11)
- Logging convention (format expected by monitoring)        (12)

Implicit dependency count: 4
```

#### Step 5: Calculate Total Context

```
Total Context = Direct + Transitive + Implicit
              = 5 + 3 + 4
              = 12 context units

Rating: HIGH (≥9)
```

### Context Surface Map

A visualization of the component's context surface:

```
┌─────────────────────────────────────────────────┐
│                UserAuthentication                │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ session  │  │ password │  │ user-repo    │   │
│  └────┬─────┘  └──────────┘  └──────┬───────┘   │
│       │                             │            │
│  ┌────▼─────┐                 ┌─────▼──────┐    │
│  │  crypto  │                 │  db conn   │    │
│  └──────────┘                 └────────────┘    │
│                                                  │
│  Implicit: [event bus] [env vars] [API][logging]│
└─────────────────────────────────────────────────┘
```

---

## The Three Rating Levels

### 🟢 LOW — Crystallization Radius: 1–3

**Characteristics:**
- Self-contained component with minimal external dependencies
- Agent can understand and modify with only the component's own code
- Changes have minimal risk of unintended side effects

**Typical candidates:**
- Pure utility functions
- Leaf components with no dependents
- Value objects and domain primitives

**Example:**
```
Component: EmailValidator
Context budget: 2 files
  - src/validation/email.ts (self)
  - src/shared/types/email.ts (shared type)
Radius: LOW
```

### 🟡 MEDIUM — Crystallization Radius: 4–8

**Characteristics:**
- Component has several dependencies but they are well-defined
- Agent needs moderate preparation to work safely
- Some cross-module understanding required

**Typical candidates:**
- Service components with injected dependencies
- Aggregate roots in domain-driven design
- Controllers with well-defined service dependencies

**Example:**
```
Component: OrderService
Context budget: 6 files
  - src/orders/order-service.ts (self)
  - src/orders/order.ts (domain model)
  - src/orders/order-repo.ts (dependency)
  - src/payments/payment-service.ts (dependency)
  - src/inventory/inventory-service.ts (dependency)
  - src/shared/types/order.ts (shared type)
Radius: MEDIUM
```

### 🔴 HIGH — Crystallization Radius: 9+

**Characteristics:**
- Component entangled with many other parts of the system
- Agent must load extensive context to work safely
- High risk of unintended side effects
- **Requires architectural review before any change**

**Typical candidates:**
- God classes and god modules
- Cross-cutting concerns (logging, metrics, audit) scattered through implementation
- Components with implicit dependencies and global state

**Example:**
```
Component: LegacyOrderManager
Context budget: 14 files
  - 6 direct dependencies
  - 4 transitive dependencies
  - 4 implicit dependencies
Radius: HIGH (REQUIRES ARCHITECTURE REVIEW)
```

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

**Problem:** Component depends on concrete implementations, pulling in their transitive dependencies.

**Solution:** Depend on interfaces, not implementations.

```typescript
// BAD: High Crystallization Radius
class OrderService {
  constructor(private db: PostgreSQLRepository) {}
  // Agent must understand PostgreSQLRepository to modify OrderService
}

// GOOD: Low Crystallization Radius
class OrderService {
  constructor(private orders: OrderRepository) {}
  // Agent only needs to understand the OrderRepository interface
}
```

**Radius reduction:** 30–50% by eliminating transitive dependencies from context.

### Technique 2: Narrow Interfaces

**Problem:** Wide interfaces expose many functions, each with its own context.

**Solution:** Narrow interfaces that expose only what's needed.

```typescript
// BAD: Wide interface — agent needs context for all 15 methods
interface UserService {
  createUser(): User;
  updateUser(): User;
  deleteUser(): void;
  getUser(): User;
  listUsers(): User[];
  banUser(): void;
  unbanUser(): void;
  // ... 8 more methods
}

// GOOD: Narrow interface — agent needs context for 3 methods
interface UserCreator {
  create(data: CreateUserInput): User;
}
interface UserQuery {
  findById(id: UserId): User | null;
}
interface UserAdmin {
  suspend(id: UserId): void;
}
```

**Radius reduction:** 40–60% by reducing the surface area an agent must understand.

### Technique 3: Explicit Dependency Declaration

**Problem:** Dependencies are implicit — discovered only through code reading or tribal knowledge.

**Solution:** Declare all dependencies explicitly.

```typescript
// BAD: Hidden dependencies
class PaymentProcessor {
  processPayment(amount: number): void {
    // Uses global logger — implicit dependency
    logger.info(`Processing payment: ${amount}`);
    // Expects environment variable — implicit dependency
    const apiKey = process.env.PAYMENT_API_KEY;
    // Emits event — implicit dependency for consumers
    eventBus.emit('payment.processed', { amount });
  }
}

// GOOD: Explicit dependencies
class PaymentProcessor {
  constructor(
    private readonly logger: Logger,
    private readonly config: PaymentConfig,
    private readonly events: EventPublisher
  ) {}

  processPayment(amount: number): void {
    this.logger.info(`Processing payment: ${amount}`);
    const apiKey = this.config.paymentApiKey;
    this.events.publish(new PaymentProcessed(amount));
  }
}
```

**Radius reduction:** 20–40% by making hidden context visible and bounded.

### Technique 4: Locality of Behavior

**Problem:** Related behavior is scattered across the codebase, requiring broad context.

**Solution:** Keep related behavior close together.

```typescript
// BAD: Scattered behavior
// src/validation/email.ts — email format validation
// src/notifications/email.ts — email sending logic
// src/user/email.ts — user email preferences
// src/templates/email.ts — email templates
// → Agent needs 4 files to understand "email"

// GOOD: Local behavior
// src/email/
//   email.ts — core types and validation
//   email-sender.ts — sending logic
//   email-preferences.ts — user preferences
//   email-templates.ts — templates
// → Agent needs 1 directory (4 related files) to understand "email"
```

**Radius reduction:** 50%+ by reducing search surface for related code.

### Technique 5: Context Budget Annotations

**Problem:** Agents don't know how much context is needed until they start working.

**Solution:** Annotate every module with its context budget.

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
export class UserService {
  // ...
}
```

**Radius reduction:** N/A (doesn't reduce radius, but makes it visible — preventing surprise context expansion).

---

## Tracking Over Time

### Crystallization Radius Registry

Maintain a registry of component Crystallization Radius measurements:

```yaml
# .aioa/radius-registry.yml
version: "1.0"
components:
  - name: UserAuthentication
    path: src/auth/user-auth.ts
    measured_radius: 12
    rating: HIGH
    trend: ↑ worsening
    last_measured: 2026-05-30
  - name: EmailValidator
    path: src/validation/email-validator.ts
    measured_radius: 2
    rating: LOW
    trend: → stable
    last_measured: 2026-05-28
```

### Trend Analysis

Track Crystallization Radius over time to detect architectural erosion:

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

### Budget Definition

Every component has a **context budget** — the maximum number of context units an agent should need to load to work on it safely.

```yaml
context_budget:
  max_units: 8           # Hard limit
  current: 5             # Current measurement
  warning_threshold: 6   # Triggers warning
  critical_threshold: 8  # Triggers blocking review
```

### Budget Allocation

When planning work, allocate context budget to each task:

| Task | Context Budget | Files | Rating |
|------|---------------|-------|--------|
| Add email validation | 2 units | `EmailValidator`, types | LOW |
| Add payment flow | 7 units | 7 files across 3 modules | MEDIUM |
| Refactor auth | 12 units | 12 files across 5 modules | HIGH (SPLIT) |

### Enforcing Budgets

Budgets are enforced during:
1. **Planning** — if a task exceeds budget, it must be split
2. **Code review** — if a change increases budget without justification, it's flagged
3. **CI pipeline** — automated checks compare budget deltas

---

## Tooling and Automation

### Automated Measurement

AIOA prescribes tools to automatically measure Crystallization Radius:

- **Import graph analysis** — map all import relationships
- **Dependency depth calculation** — measure transitive dependency chains
- **Implicit dependency detection** — flag global state, ambient context, conventions
- **Context budget validation** — compare measurements against declared budgets

### CI Integration

```yaml
# .github/workflows/aioa-checks.yml
name: AIOA Radius Check
on: [pull_request]
jobs:
  radius-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Measure Crystallization Radius
        run: aioa measure-radius --diff HEAD~1
      - name: Check Budgets
        run: aioa check-budgets
      - name: Flag Regressions
        run: aioa flag-regressions --threshold 2
```

### PR Comments

When a change increases Crystallization Radius, automated comments can flag it:

```
⚠️ **Crystallization Radius Warning**

Component `UserAuthentication` context budget:
- Before: 5 units (MEDIUM)
- After:  7 units (MEDIUM) 
- Delta:  +2 units

This is within acceptable range, but please ensure:
1. The new dependency is truly necessary
2. The context budget annotation is updated
3. No implicit dependencies were added

Review with AIOA principles in mind.
```

---

## Examples

### Example 1: Well-Isolated Component (LOW)

```typescript
/**
 * Validates email addresses according to RFC 5322.
 * 
 * @context-budget
 * - self: src/validation/email.ts
 * - shared type: src/shared/types/email.ts
 * 
 * Crystallization Radius: LOW (2 units)
 */
export class EmailValidator {
  validate(email: string): EmailAddress | ValidationError {
    // Implementation uses only string operations
    // No dependencies on other modules
    // No global state
    // No configuration files
  }
}
```

**Context surface:**
```
EmailValidator → EmailAddress (shared type)
     ↓
  (nothing else)
```

### Example 2: Well-Structured Service (MEDIUM)

```typescript
/**
 * Manages user registration workflow.
 * 
 * @context-budget
 * - self: src/users/registration.ts
 * - domain: src/users/user.ts
 * - repository: src/users/user-repository.ts (interface only)
 * - auth: src/auth/password-hasher.ts (interface only)
 * - notification: src/notifications/email-sender.ts (interface only)
 * - types: src/shared/types/user.ts
 * 
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

**Context surface:**
```
RegistrationService → UserRepository (interface)
                   → PasswordHasher (interface)
                   → EmailSender (interface)
                   → User (type)
                   → RegistrationInput (type)
     ↓
  (interfaces are narrow, no transitive leakage)
```

### Example 3: Entangled Legacy Module (HIGH) — Demonstrates Refactoring

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
     ↓
  (each dependency is a narrow interface)
```

---

## Anti-Patterns

### 1. The God Module

Every module ends up importing from the god module, creating high transitive context.

**Detection:** A single module appears in 50%+ of other modules' dependency lists.

**Fix:** Split into focused sub-modules. Extract unrelated functionality.

### 2. Implicit Context Ocean

"Everyone knows" conventions, global state, shared configuration files.

**Detection:** Changes to module X break module Y despite no visible dependency.

**Fix:** Make all dependencies explicit. Replace global state with injected dependencies.

### 3. Deep Inheritance Chains

Modifying a subclass requires understanding the entire ancestor chain.

**Detection:** Class hierarchies with depth > 3.

**Fix:** Prefer composition over inheritance. Flatten deep hierarchies.

### 4. Context-Free Interfaces

Interfaces that don't document their context requirements.

**Detection:** No `@context-budget` annotations in codebase.

**Fix:** Add context budget annotations to every public interface.

### 5. Happy-Path Architecture

Architecture optimized for the happy path only, with error handling and edge cases scattered as afterthoughts.

**Detection:** Error handling code far from the logic that produces errors.

**Fix:** Use result types, locate error handling near the producing logic.

---

## Conclusion

Crystallization Radius is the foundational AIOA principle because it directly addresses the core challenge of AI-assisted software development: **context comprehension**.

By measuring, tracking, and minimizing the context required to make safe changes, AIOA enables:

- Higher confidence AI code generation
- Lower regression rates
- Faster agent onboarding to existing codebases
- Clear architectural quality metrics
- Early detection of architectural erosion

**Start measuring today. Your AI agents will thank you.**
