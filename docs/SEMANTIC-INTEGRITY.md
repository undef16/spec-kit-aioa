# Semantic Integrity — Complete Guide

> *"Preserving meaning across architectural boundaries."*

**Version:** 1.0.0

---

## Table of Contents

1. [What is Semantic Integrity?](#what-is-semantic-integrity)
2. [Why Semantic Integrity Matters for AI Agents](#why-semantic-integrity-matters-for-ai-agents)
3. [The Four Layers of Semantic Integrity](#the-four-layers-of-semantic-integrity)
4. [Common Semantic Integrity Violations](#common-semantic-integrity-violations)
5. [Preserving Semantic Integrity](#preserving-semantic-integrity)
6. [The Boundary Parser Pattern](#the-boundary-parser-pattern)
7. [Semantic Contracts](#semantic-contracts)
8. [Integrity Testing](#integrity-testing)
9. [Tooling and Automation](#tooling-and-automation)
10. [Examples](#examples)
11. [Anti-Patterns](#anti-patterns)

---

## What is Semantic Integrity?

**Semantic Integrity** is the property that meaning is preserved as data and behavior cross architectural boundaries. When data leaves one component and enters another, the receiving component must interpret it exactly as the sending component intended.

### Core Idea

> *"A `User` created in module A has the same properties, invariants, and lifecycle in module B."*

Semantic Integrity is violated when:
- Module A's `User` has `id: string` (a UUID) but Module B's `User` has `id: number` (a database sequence)
- Module A uses `status: "active"` but Module B uses `status: 1` (mapping is undocumented)
- Module A sends a `firstName` field but Module B expects `first_name` (silent transformation)

### Why "Integrity"?

The word "integrity" is deliberate — like referential integrity in databases, semantic integrity is a **constraint that must hold true**. A system with poor semantic integrity is like a database with broken foreign keys: data exists, but relationships and meanings are unreliable.

---

## Why Semantic Integrity Matters for AI Agents

### Semantic Integrity as Guard Rails

Semantic Integrity principles serve as guard rails for AI agents:

1. **Explicit boundaries** — Agents know where one component ends and another begins
2. **Shared contracts** — Agents find the authoritative type definition
3. **Boundary parsing** — Agents know where validation happens and where trust begins
4. **Versioned interfaces** — Agents detect when contracts change

---

## The Four Layers of Semantic Integrity

| Layer | What It Protects | Enforcement | Example Violation |
|-------|-----------------|-------------|-------------------|
| **Type Integrity** | Data serialization/deserialization compatibility | Shared type definitions, schema validation at boundaries, automated type compatibility checks | Module A has `User { id: string; name: string; }`, Module B has `User { id: number; fullName: string; }` |
| **Behavioral Integrity** | Contractual behavior — operations produce expected side effects | Interface contracts with pre/post conditions, consumer-driven contract testing, behavioral equivalence tests | Module A expects `saveUser(user)` creates or updates; Module B implements `saveUser(user)` as create-only (throws on duplicate) |
| **Conceptual Integrity** | Ubiquitous language — same terms mean same things everywhere | Shared glossary, domain concept maps, conceptual consistency reviews | Module A: "Activation" = email verified + first login; Module B: "Activation" = license key entered |
| **Invariant Integrity** | Global invariants — rules that must be true system-wide | Invariant documentation and testing, property-based testing, architectural tests | Module A checks "one active session per user" before creating sessions; Module B bypasses check |

### Layer Interaction

The layers build on each other:
```
Type Integrity → Behavioral Integrity → Conceptual Integrity → Invariant Integrity
```
A violation at a lower layer typically breaks all higher layers.

---

## Common Semantic Integrity Violations

| Violation | Symptom | AIOA Solution |
|-----------|---------|---------------|
| **Silently Reshaped Data** | `send({ name: f + " " + l })` → receiver splits `name` (fragile reverse-engineering) | Send canonical representation. Transform at boundary with explicit documentation. |
| **Different Validation Rules** | Module A accepts `user@example`, Module B rejects it (stricter regex) | Single shared validation function used by both modules |
| **Type System Mismatch** | Same concept: `OrderId { value: string }` in TS, plain `"abc"` in JSON, `order_id` in DB | Define canonical representation once. All modules use same type definition. |
| **Concept Overload** | `Status` = pending/confirmed/shipped (Order) vs active/inactive (User) vs pending/authorized (Payment) | Use distinct names: `OrderStatus`, `PaymentStatus`, `UserAccountStatus` |
| **Implicit Temporal Coupling** | Module A: `user.state = "active"` then `events.emit()` before DB commit. Module B reads stale state. | Make temporal contracts explicit. Emit after commit. |

---

## Preserving Semantic Integrity

### 1. Parse at Boundaries, Trust Internally

```
[External World] ──raw data──→ [Boundary Parser] ──trusted data──→ [Internal Logic]
```

**Rules:**
1. All external input is parsed at the system boundary
2. Parsing validates, transforms, and types the data
3. Once parsed, data is "trusted" — internal logic does not re-validate

```typescript
// BOUNDARY: parse at boundary
class UserController {
  async handle(request: HttpRequest): Promise<HttpResponse> {
    const input = RegisterUserInput.parse(request.body); // PARSE
    const result = await this.service.register(input);   // trusted
    return { status: 201, body: result.toJSON() };
  }
}

// INTERNAL: operate on trusted data
class RegistrationService {
  async register(input: RegisterUserInput): Promise<User> {
    const user = User.create(input.email, input.name); // No validation needed
    await this.users.save(user);
    return user;
  }
}
```

### 2. Define Shared Contracts

Every boundary between components is governed by a **semantic contract** — a formal definition of what data and behavior cross the boundary.

```typescript
// shared/contracts/user-contract.ts — AUTHORITATIVE definition
export interface UserContract {
  id: string;          // UUID v4
  email: string;       // RFC 5322 compliant
  displayName: string; // max 100 chars
  status: UserStatus;
  createdAt: string;   // ISO 8601 UTC
  updatedAt: string;   // ISO 8601 UTC
}

export function parseUserContract(data: unknown): UserContract {
  return userSchema.parse(data); // Validation here, at boundary
}
```

### 3. Version Contracts Explicitly

```typescript
// Version 1: Initial contract  →  shared/contracts/user-contract-v1.ts
// Version 2: Added phoneNumber →  shared/contracts/user-contract-v2.ts
// Migration: Both sides upgrade simultaneously; V1 works with V2 producers (backward compatible)
// Breaking changes require a new endpoint or interface version
```

### 4. Test Semantic Integrity

**Contract tests** verify producers and consumers agree on semantics:
```typescript
describe('UserContract semantic integrity', () => {
  it('parses valid user data correctly', () => { /* ... */ });
  it('rejects invalid status values', () => {
    expect(() => parseUserContract({ ...valid, status: 'banned' })).toThrow();
  });
  it('preserves meaning through round-trip serialization', () => {
    const original = createTestUser();
    expect(deserialize(serialize(original))).toEqual(original);
  });
});
```

### 5. Monitor for Semantic Drift

- **Schema comparison** — compare serialized data shapes across boundaries
- **Type compatibility checks** — verify shared types are consistent
- **Behavioral tests** — verify operations produce consistent effects
- **Cross-boundary log analysis** — detect data anomalies at boundaries

---

## The Boundary Parser Pattern

The Boundary Parser Pattern is the primary implementation mechanism for Semantic Integrity — an application of "Parse, Don't Validate" at the architectural level.

```
┌──────────────┐  raw data  ┌──────────────────┐  trusted data  ┌──────────────┐
│ External     │ ────────→ │ Boundary Parser   │ ─────────────→ │ Internal     │
│ World        │            │ • Validates       │                │ Logic        │
│ (HTTP, Queue)│            │ • Transforms/     │                │ (Pure domain)│
└──────────────┘            │ • Types/Trusts    │                └──────────────┘
                            └──────────────────┘
```

**Rules:**
1. **One parser per boundary** — Each component boundary has exactly one parser
2. **Parser is the single source of truth** — All validation logic lives in the parser
3. **Parser produces trusted types** — Output is always typed and validated
4. **Parser fails fast** — Invalid data never enters internal logic

```typescript
// ✅ BOUNDARY: parses external data
class OrderController {
  async createOrder(rawBody: unknown): Promise<OrderResponse> {
    const command = CreateOrderCommand.parse(rawBody); // Validation HERE
    return this.service.createOrder(command);           // Trusted
  }
}

// ❌ BAD: Validation leaked into internal logic
class OrderService {
  async createOrder(data: any): Promise<Order> {
    if (!data.customerId) throw new Error("Missing customerId"); // Re-validation
    if (!data.items?.length) throw new Error("No items");          // Re-validation
  }
}
```

---

## Semantic Contracts

A **semantic contract** is a formal definition of the agreement between two components at a boundary. It specifies data types, domain interpretation, behavior, and guarantees.

### Contract Template

```typescript
/**
 * SEMANTIC CONTRACT: OrderPaymentContract
 * Version: 1.0.0
 * Governing boundary: OrderService → PaymentService
 *
 * PURPOSE: Communicate payment requests from OrderService to PaymentService.
 *
 * DATA:
 *   PaymentRequest:
 *     - orderId: string (UUID v4, must exist in OrderService)
 *     - amount: number (positive, 2 decimal places, in USD cents)
 *     - currency: "USD" | "EUR" | "GBP" (ISO 4217)
 *     - customerId: string (UUID v4, must exist in CustomerService)
 *   PaymentResult:
 *     - transactionId: string (UUID v4)
 *     - status: "success" | "declined" | "error"
 *     - processedAt: string (ISO 8601, UTC)
 *
 * INVARIANTS:
 *   1. A PaymentRequest always produces exactly one PaymentResult
 *   2. PaymentResult.transactionId is globally unique
 *   3. PaymentResult.status is never "pending"
 *
 * BEHAVIOR:
 *   - PaymentService is idempotent: same request returns same result
 *   - PaymentService does NOT modify OrderService data
 *
 * VERSION HISTORY:
 *   1.0.0 — Initial contract
 */
```

### Contract Governance

- **Contract owner** — Each contract has an owner responsible for its integrity
- **Contract review** — Changes require review from both producer and consumer
- **Contract testing** — Automated tests verify both sides adhere to the contract
- **Contract versioning** — Breaking changes require a new contract version

---

## Integrity Testing

### Round-Trip Testing

Verify data survives a full cycle across a boundary:

```typescript
function testRoundTrip(original: TrustedType) {
  const serialized = serialize(original);         // Outbound
  const parsed = deserialize(serialized);          // Inbound
  expect(parsed).toDeepEqual(original);            // Semantic equivalence
}
```

### Consumer-Driven Contract Testing

Each consumer defines the contract it expects; the producer is tested against all consumer contracts:

```typescript
const consumerContract = {
  provider: 'OrderService', consumer: 'PaymentService',
  interface: 'getOrder',
  input: { orderId: string() },
  output: { id: string(), amount: number(), status: string() },
};

describe('Consumer-driven contract tests', () => {
  it('satisfies PaymentService contract', async () => {
    const result = await orderService.getOrder({ orderId: testOrderId });
    expect(result).toMatchContract(consumerContract.output);
  });
});
```

### Property-Based Testing for Invariants

```typescript
describe('Payment semantic invariants', () => {
  it('payment result is never pending', () => {
    fc.assert(fc.property(fc.anyPaymentRequest(), async (request) => {
      const result = await paymentService.process(request);
      expect(result.status).not.toBe('pending');
    }));
  });

  it('same request returns same result (idempotency)', async () => {
    const request = makePaymentRequest();
    expect(await paymentService.process(request))
      .toEqual(await paymentService.process(request));
  });
});
```

---

## Tooling and Automation

### Check Types

- **Type consistency** — TypeScript compiler, schema comparison for type mismatches across boundaries
- **Contract compliance** — Pact, Spring Cloud Contract for producer/consumer contract violations
- **Schema diff** — json-schema-diff, openapi-diff for breaking schema changes
- **Round-trip fidelity** — Custom tests for data degradation through boundaries
- **Invariant enforcement** — Property-based testing (fast-check) for invariant violations
- **Cross-boundary drift** — Custom linting rules for silent transformations, implicit coupling

### Linting Rules

```typescript
// ESLint: No silent type assertions at boundaries
// BAD: const user = data as User;
// GOOD: const user = parseUser(data);

// ESLint: Shared types must be imported, not redefined
// BAD: interface User { ... }  // Local redefinition
// GOOD: import { User } from '@shared/types';
```

---

## Examples

### Example 1: Clean Boundary with Semantic Integrity

```typescript
// SHARED CONTRACT: contracts/payment-contract.ts
export interface PaymentRequest {
  orderId: string;       // UUID v4
  amount: number;        // USD cents
  currency: 'USD' | 'EUR';
  customerId: string;    // UUID v4
}
export interface PaymentResult {
  transactionId: string; // UUID v4
  status: 'completed' | 'declined' | 'failed';
  processedAt: string;   // ISO 8601 UTC
}

const PaymentRequestSchema = z.object({
  orderId: z.string().uuid(),
  amount: z.number().positive().int(),
  currency: z.enum(['USD', 'EUR']),
  customerId: z.string().uuid(),
});

export function parsePaymentRequest(data: unknown): PaymentRequest {
  return PaymentRequestSchema.parse(data);
}

// MODULE B: PaymentService (consumer)
class PaymentController {
  async handlePayment(rawData: unknown): Promise<PaymentResult> {
    const request = parsePaymentRequest(rawData); // PARSE at boundary
    return this.paymentService.process(request);   // Trusted
  }
}

class PaymentService {
  async process(request: PaymentRequest): Promise<PaymentResult> {
    const gatewayResult = await this.gateway.charge(request.amount, request.currency);
    return {
      transactionId: gatewayResult.id,
      status: this.mapStatus(gatewayResult.status),
      processedAt: new Date().toISOString(),
    };
  }
}
```

### Example 2: Cross-Boundary Invariant

```typescript
// shared/invariants/account-invariants.ts
/**
 * INVARIANT: An account can have at most one active subscription.
 * Applies across: BillingService, AdminService, SelfService.
 */
export function assertNoActiveSubscription(subscriptions: Subscription[]): void {
  const active = subscriptions.filter(s => s.isActive());
  if (active.length > 1) {
    throw new InvariantViolationError(
      `Found ${active.length} active subscriptions. Maximum is 1.`
    );
  }
}

// Tested in every module:
it('enforces single active subscription invariant', async () => {
  const customer = await createCustomerWithActiveSubscription();
  await expect(subscriptionService.createSubscription(customer.id))
    .rejects.toThrow(InvariantViolationError);
});
```

---

## Anti-Patterns

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| **Validation Scattered Everywhere** | `if (!data.field)` checks in multiple files for the same data | Centralize validation at boundary with single parser |
| **Copy-and-Paste Types** | `interface User` appears in more than one file | Define shared types once in a shared package; all modules import from there |
| **Implicit Data Transformations** | Undocumented field name/format changes at boundaries | Make all transformations explicit with named functions |
| **The "Works on My Machine" Contract** | Contract knowledge lives only in developer's heads | Express every contract in code; enforce with automated checks |
| **Cross-Boundary Reach-Through** | Import paths 2+ levels deep: `import X from 'b/internal/deep/c'` | Each component interacts only with its immediate neighbor's public interface |
| **Silent Error Handling** | Empty catch blocks, `console.error` without re-throw | Errors at boundaries are integrity violations — fail fast |
