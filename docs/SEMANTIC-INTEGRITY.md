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

### The Context Window Constraint

AI agents process code and data through context windows. They see files one at a time, or in small groups. This creates a fundamental challenge:

> **An agent modifying module B may never see module A's interpretation of the shared `User` type.**

If the semantic contract between A and B is implicit, the agent will:
1. Read module B's code
2. See a `User` type with certain fields
3. Make changes assuming this is the canonical representation
4. Break module A in the process

### The Silent Drift Problem

Human developers can detect semantic drift through:
- Long-term familiarity with the codebase
- Conversations with other developers
- Pull request discussions

AI agents lack these channels. They see only the code. Semantic drift that is obvious to a human may be invisible to an AI:

**Human:** "Wait, why is the Order ID an integer here? We moved to UUIDs last year."

**AI:** *Sees only the current file with integer ID, makes changes consistent with integer ID.*

### Semantic Integrity as Guard Rails

Semantic Integrity principles serve as guard rails for AI agents:

1. **Explicit boundaries** — Agents know where one component ends and another begins
2. **Shared contracts** — Agents find the authoritative type definition
3. **Boundary parsing** — Agents know where validation happens and where trust begins
4. **Versioned interfaces** — Agents detect when contracts change

---

## The Four Layers of Semantic Integrity

### Layer 1: Type Integrity

> *"Data has the same shape and structure across boundaries."*

**What it protects:** Data serialization/deserialization compatibility.

**Enforcement:**
- Shared type definitions across boundaries
- Schema validation at boundary entry/exit points
- Automated type compatibility checks

**Example violation:**
```typescript
// Module A defines:
interface User { id: string; name: string; }

// Module B defines (drifted):
interface User { id: number; fullName: string; }
// → Same concept, different shape → Semantic drift
```

### Layer 2: Behavioral Integrity

> *"Operations produce the same effects across boundaries."*

**What it protects:** Contractual behavior — calling a function produces the expected side effects.

**Enforcement:**
- Interface contracts with pre/post conditions
- Contract testing (consumer-driven contracts)
- Behavioral equivalence tests

**Example violation:**
```typescript
// Module A expects: saveUser(user) creates or updates
// Module B implements: saveUser(user) only creates (throws on duplicate)
// → Same interface, different behavior → Semantic drift
```

### Layer 3: Conceptual Integrity

> *"Domain concepts mean the same thing everywhere."*

**What it protects:** Ubiquitous language — the same terms mean the same things everywhere.

**Enforcement:**
- Shared glossary/vocabulary
- Domain concept maps
- Conceptual consistency reviews

**Example violation:**
```typescript
// Module A: "Activation" = email verified + first login complete
// Module B: "Activation" = license key entered
// → Same term, different concept → Conceptual drift
```

### Layer 4: Invariant Integrity

> *"System-wide rules hold true across all boundaries."*

**What it protects:** Global invariants — rules that must be true for the system to function correctly.

**Enforcement:**
- Invariant documentation and testing
- Property-based testing
- Architectural tests

**Example violation:**
```typescript
// Invariant: A user can have at most one active session
// Module A checks this before creating sessions
// Module B (bypasses check in "emergency override"): creates duplicate session
// → Invariant violated across boundary → Integrity breach
```

### Layer Interaction

The layers build on each other:

```
Type Integrity      (data shape)
        ↓
Behavioral Integrity (data operations)
        ↓
Conceptual Integrity (domain meaning)
        ↓
Invariant Integrity  (system rules)
```

A violation at a lower layer typically breaks all higher layers. If types don't match (Layer 1), behavior, concepts, and invariants cannot be preserved.

---

## Common Semantic Integrity Violations

### Violation 1: Silently Reshaped Data

```typescript
// Sending component
function sendUser(user: User) {
  queue.send({
    id: user.id,
    name: `${user.firstName} ${user.lastName}` // reshape: concatenated
  });
}

// Receiving component
function handleUser(data: any) {
  const user = {
    id: data.id,
    firstName: data.name.split(' ')[0], // reverse engineer
    lastName: data.name.split(' ')[1]    // fragile!
  };
}
```

**Problem:** Data is silently reshaped. The receiving component reverse-engineers the transformation, creating fragility and hidden coupling.

**AIOA solution:** Send the canonical User representation. Transform at the boundary only with explicit documentation.

### Violation 2: Different Validation Rules

```typescript
// Module A validates email as:
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  // Accepts: "user@example" (no TLD)
}

// Module B validates email as:
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/.test(email);
  // Rejects: "user@example"
}
```

**Problem:** The same concept has different validation rules in different modules. Data accepted by A may be rejected by B.

**AIOA solution:** A single shared validation function used by both modules.

### Violation 3: Type System Mismatch

```typescript
// Module A (TypeScript)
interface OrderId { value: string; }

// Module B (serialized JSON)
// "orderId": "abc-123"  ← plain string, not wrapped type

// Module C (database)
// order_id: UUID  ← different field name
```

**Problem:** The same concept has different representations (typed vs untyped, different field names, different formats).

**AIOA solution:** Define the canonical representation once. All modules use the same type definition. Serialization/deserialization happens at boundaries only.

### Violation 4: Concept Overload

```typescript
// "Status" means different things in different contexts:
// - Order.status: "pending" | "confirmed" | "shipped" | "delivered"
// - Payment.status: "pending" | "authorized" | "captured" | "refunded"
// - User.status: "active" | "inactive" | "suspended" | "deleted"

// Problem: Different concepts share the same name ("status")
// An AI agent may confuse them
```

**AIOA solution:** Use distinct names for distinct concepts: `OrderStatus`, `PaymentStatus`, `UserAccountStatus`.

### Violation 5: Implicit Temporal Coupling

```typescript
// Module A sets user state, then emits event
function activateUser(id: string) {
  user.state = "active";
  events.emit("user-activated", { id });
}

// Module B listens for event and reads user state
events.on("user-activated", async ({ id }) => {
  const user = await userRepo.findById(id);
  // BUG: user.state may still be "inactive" if event fires before DB commit
});
```

**Problem:** The semantic contract includes an implicit assumption about timing. Module B assumes A has persisted the change before emitting, but A hasn't.

**AIOA solution:** Make temporal contracts explicit. Use well-defined event ordering (e.g., emit after commit).

---

## Preserving Semantic Integrity

### 1. Parse at Boundaries, Trust Internally

The most important pattern for preserving Semantic Integrity.

```
[External World] ──raw data──→ [Boundary Parser] ──trusted data──→ [Internal Logic]
```

**Rules:**
1. All external input is parsed at the system boundary
2. Parsing validates, transforms, and types the data
3. Once parsed, data is "trusted" — internal logic does not re-validate
4. Internal logic operates on the trusted representation only

**Implementation:**
```typescript
// BOUNDARY: UserRegistrationController
class UserRegistrationController {
  constructor(private readonly service: RegistrationService) {}

  async handle(request: HttpRequest): Promise<HttpResponse> {
    // PARSE at boundary
    const input = RegisterUserInput.parse(request.body);
    // input is now typed, validated, and trusted

    // INTERNAL: operate on trusted data
    const result = await this.service.register(input);

    // SERIALIZE at boundary
    return { status: 201, body: result.toJSON() };
  }
}

// INTERNAL: RegistrationService works with trusted types
class RegistrationService {
  async register(input: RegisterUserInput): Promise<User> {
    // No validation needed — input is already trusted
    const user = User.create(input.email, input.name);
    await this.users.save(user);
    return user;
  }
}
```

### 2. Define Shared Contracts

Every boundary between components is governed by a **semantic contract** — a formal definition of what data and behavior cross the boundary.

```typescript
// shared/contracts/user-contract.ts
// This file is the AUTHORITATIVE definition of user data across boundaries.

export interface UserContract {
  id: string;        // UUID v4
  email: string;     // Validated email (RFC 5322 compliant)
  displayName: string; // Human-readable name, no more than 100 chars
  status: UserStatus;
  createdAt: string;  // ISO 8601 UTC timestamp
  updatedAt: string;  // ISO 8601 UTC timestamp
}

export enum UserStatus {
  Active = "active",
  Inactive = "inactive",
  Suspended = "suspended",
}

export function parseUserContract(data: unknown): UserContract {
  // Validation happens HERE, at the boundary
  const parsed = userSchema.parse(data);
  return parsed; // Now trusted
}
```

### 3. Version Contracts Explicitly

When a contract changes, version it. Both sides must be updated together.

```typescript
// Version 1: Initial contract
// shared/contracts/user-contract-v1.ts

// Version 2: Added phoneNumber field
// shared/contracts/user-contract-v2.ts

// Migration strategy:
// - Both sides upgrade simultaneously during a transition period
// - V1 consumers continue to work with V2 producers (backward compatible)
// - Breaking changes require a new endpoint or interface version
```

### 4. Test Semantic Integrity

**Contract tests** verify that producers and consumers agree on semantics:

```typescript
// Contract test: UserContract
describe('UserContract semantic integrity', () => {
  it('parses valid user data correctly', () => {
    const input = {
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'test@example.com',
      displayName: 'Test User',
      status: 'active',
      createdAt: '2026-01-15T10:00:00Z',
      updatedAt: '2026-01-15T10:00:00Z',
    };

    const user = parseUserContract(input);
    expect(user.id).toBe(input.id);
    expect(user.email).toBe(input.email);
    // ... verify all fields
  });

  it('rejects invalid status values', () => {
    const input = {
      id: '550e8400-e29b-41d4-a716-446655440000',
      email: 'test@example.com',
      displayName: 'Test User',
      status: 'banned', // Invalid status
      createdAt: '2026-01-15T10:00:00Z',
      updatedAt: '2026-01-15T10:00:00Z',
    };

    expect(() => parseUserContract(input)).toThrow();
  });

  it('preserves meaning through round-trip serialization', () => {
    const original = createTestUser();
    const json = serialize(original);
    const restored = deserialize(json);
    expect(restored).toEqual(original); // Semantic equivalence
  });
});
```

### 5. Monitor for Semantic Drift

Automated monitoring can detect drift:

- **Schema comparison** — compare serialized data shapes across boundaries
- **Type compatibility checks** — verify shared types are consistent
- **Behavioral tests** — verify that operations produce consistent effects
- **Cross-boundary log analysis** — detect data anomalies at boundaries

---

## The Boundary Parser Pattern

The Boundary Parser Pattern is the primary implementation mechanism for Semantic Integrity. It's an application of the "Parse, Don't Validate" philosophy applied at the architectural level.

### Pattern Structure

```
┌──────────────┐     raw data      ┌──────────────────┐    trusted data    ┌──────────────┐
│ External     │ ────────────────→ │ Boundary Parser  │ ────────────────→ │ Internal     │
│ World        │                   │                  │                    │ Logic        │
│ (HTTP, Queue,│                   │ • Validates       │                    │ (Pure domain  │
│  DB, File)   │                   │ • Transforms      │                    │  functions)   │
└──────────────┘                   │ • Types           │                    └──────────────┘
                                   │ • Trusts          │                           │
                                   └──────────────────┘                           │
                                          │                                       │
                                          │                                       │
                                   ┌──────▼──────┐                       ┌───────▼───────┐
                                   │ Schema/Zod  │                       │ Shared Types  │
                                   │ Validation  │                       │ & Contracts   │
                                   └─────────────┘                       └───────────────┘
```

### Rules for Boundary Parsers

1. **One parser per boundary** — Each component boundary has exactly one parser that converts external data to internal trusted types.

2. **Parser is the single source of truth** — All validation logic lives in the parser. Internal logic never validates.

3. **Parser produces trusted types** — The output of a parser is always a typed, validated representation that internal logic can trust.

4. **Parser fails fast** — If data cannot be parsed, the parser throws or returns an error result. Invalid data never enters internal logic.

### Boundary Parser vs. Internal Logic

```typescript
// ✅ BOUNDARY: ParseController parses external data
class OrderController {
  constructor(private readonly service: OrderService) {}

  async createOrder(rawBody: unknown): Promise<OrderResponse> {
    const command = CreateOrderCommand.parse(rawBody); // Validation HERE
    const order = await this.service.createOrder(command); // Trusted
    return order.toResponse();
  }
}

// ✅ INTERNAL: OrderService uses trusted types
class OrderService {
  constructor(private readonly repo: OrderRepository) {}

  async createOrder(command: CreateOrderCommand): Promise<Order> {
    // command is already validated — no checks needed
    const order = Order.create(command.customerId, command.items);
    return this.repo.save(order);
  }
}

// ❌ BAD: Validation leaked into internal logic
class OrderService {
  async createOrder(data: any): Promise<Order> {
    if (!data.customerId) throw new Error("Missing customerId"); // Re-validation
    if (!data.items?.length) throw new Error("No items");          // Re-validation
    // Internal logic is polluted with defensive checks
  }
}
```

---

## Semantic Contracts

A **semantic contract** is a formal definition of the agreement between two components at a boundary. It specifies:

- **What data** crosses the boundary (types, shapes, formats)
- **What it means** (domain interpretation, invariants)
- **How it behaves** (operations, side effects, order)
- **What is guaranteed** (preconditions, postconditions, invariants)

### Contract Template

```typescript
/**
 * SEMANTIC CONTRACT: OrderPaymentContract
 * Version: 1.0.0
 * 
 * Governing boundary: OrderService → PaymentService
 * 
 * PURPOSE:
 *   Communicate payment requests from OrderService to PaymentService.
 *   PaymentService processes the payment and returns the result.
 * 
 * DATA:
 *   PaymentRequest:
 *     - orderId: string (UUID v4, must exist in OrderService)
 *     - amount: number (positive, 2 decimal places, in USD cents)
 *     - currency: "USD" | "EUR" | "GBP" (ISO 4217)
 *     - customerId: string (UUID v4, must exist in CustomerService)
 *   
 *   PaymentResult:
 *     - transactionId: string (UUID v4, generated by PaymentService)
 *     - status: "success" | "declined" | "error"
 *     - processedAt: string (ISO 8601, UTC)
 * 
 * INVARIANTS:
 *   1. A PaymentRequest always produces exactly one PaymentResult
 *   2. PaymentResult.transactionId is globally unique
 *   3. PaymentResult.status is never "pending" — result is always final
 * 
 * BEHAVIOR:
 *   - PaymentService is idempotent: same PaymentRequest returns same PaymentResult
 *   - PaymentService does NOT modify OrderService data
 *   - PaymentService may call external payment gateway
 * 
 * VERSION HISTORY:
 *   1.0.0 — Initial contract
 */
```

### Contract Governance

- **Contract owner** — Each contract has an owner responsible for its integrity
- **Contract review** — Changes to a contract require review from both sides (producer and consumer)
- **Contract testing** — Automated tests verify both sides adhere to the contract
- **Contract versioning** — Breaking changes require a new contract version

---

## Integrity Testing

### Round-Trip Testing

Verify that data survives a full cycle across a boundary:

```typescript
function testRoundTrip(original: TrustedType) {
  const serialized = serialize(original);         // Outbound
  const parsed = deserialize(serialized);          // Inbound
  expect(parsed).toDeepEqual(original);            // Semantic equivalence
}
```

### Consumer-Driven Contract Testing

Each consumer defines the contract it expects, and the producer is tested against all consumer contracts:

```typescript
// Consumer A's contract
const consumerAContract = {
  provider: 'OrderService',
  consumer: 'PaymentService',
  interface: 'getOrder',
  input: { orderId: string() },
  output: { id: string(), amount: number(), status: string() },
};

// Test: OrderService meets all consumer contracts
describe('Consumer-driven contract tests', () => {
  it('satisfies PaymentService contract', async () => {
    const result = await orderService.getOrder({ orderId: testOrderId });
    expect(result).toMatchContract(consumerAContract.output);
  });
});
```

### Property-Based Testing for Invariants

Verify that invariants hold for a wide range of inputs:

```typescript
describe('Payment semantic invariants', () => {
  it('payment result is never pending', () => {
    fc.assert(
      fc.property(fc.anyPaymentRequest(), async (request) => {
        const result = await paymentService.process(request);
        expect(result.status).not.toBe('pending');
      })
    );
  });

  it('same request returns same result (idempotency)', async () => {
    const request = makePaymentRequest();
    const result1 = await paymentService.process(request);
    const result2 = await paymentService.process(request);
    expect(result1).toEqual(result2);
  });
});
```

---

## Tooling and Automation

### Automated Semantic Integrity Checks

| Check | Tooling | What It Detects |
|-------|---------|-----------------|
| **Type consistency** | TypeScript compiler, schema comparison | Type mismatches across boundaries |
| **Contract compliance** | Pact, Spring Cloud Contract | Producer/consumer contract violations |
| **Schema diff** | json-schema-diff, openapi-diff | Breaking schema changes |
| **Round-trip fidelity** | Custom tests | Data degradation through boundaries |
| **Invariant enforcement** | Property-based testing (fast-check) | Invariant violations |
| **Cross-boundary drift** | Custom linting rules | Silent transformations, implicit coupling |

### CI Pipeline Integration

```yaml
# .github/workflows/semantic-integrity.yml
name: Semantic Integrity Checks
on: [pull_request]
jobs:
  integrity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check shared type consistency
        run: aioa check-types --diff HEAD~1
        
      - name: Verify boundary contracts
        run: aioa verify-contracts
        
      - name: Run round-trip tests
        run: aioa roundtrip-test --boundaries all
        
      - name: Check for semantic drift
        run: aioa detect-drift --since=last-pass
```

### Linting Rules

```typescript
// ESLint rule: No silent type assertions at boundaries
// BAD: const user = data as User;  // Type assertion without parsing
// GOOD: const user = parseUser(data);  // Parsed at boundary

// ESLint rule: Shared types must be imported, not redefined
// BAD: interface User { ... }  // Local redefinition
// GOOD: import { User } from '@shared/types';
```

---

## Examples

### Example 1: Clean Boundary with Semantic Integrity

```typescript
// ========================================
// SHARED CONTRACT (owned by both modules)
// ========================================
// contracts/payment-contract.ts
export interface PaymentRequest {
  orderId: string;       // UUID v4
  amount: number;         // USD cents
  currency: 'USD' | 'EUR';
  customerId: string;    // UUID v4
}

export interface PaymentResult {
  transactionId: string; // UUID v4
  status: 'completed' | 'declined' | 'failed';
  processedAt: string;   // ISO 8601 UTC
}

// Zod schema for runtime validation
const PaymentRequestSchema = z.object({
  orderId: z.string().uuid(),
  amount: z.number().positive().int(),
  currency: z.enum(['USD', 'EUR']),
  customerId: z.string().uuid(),
});

export function parsePaymentRequest(data: unknown): PaymentRequest {
  return PaymentRequestSchema.parse(data);
}

// ========================================
// MODULE A: OrderService (producer)
// ========================================
// Uses the shared contract. Parses at external boundaries only.
// Sends PaymentRequest to PaymentService.

// ========================================
// MODULE B: PaymentService (consumer)
// ========================================
import { PaymentRequest, parsePaymentRequest } from '../contracts/payment-contract';

class PaymentController {
  async handlePayment(rawData: unknown): Promise<PaymentResult> {
    // PARSE at boundary
    const request = parsePaymentRequest(rawData);
    // request is now typed, validated, and trusted

    // INTERNAL: operate on trusted data
    const result = await this.paymentService.process(request);
    return result;
  }
}

class PaymentService {
  async process(request: PaymentRequest): Promise<PaymentResult> {
    // No validation — request is trusted
    // Pure business logic
    const gatewayResult = await this.gateway.charge(request.amount, request.currency);
    return {
      transactionId: gatewayResult.id,
      status: this.mapStatus(gatewayResult.status),
      processedAt: new Date().toISOString(),
    };
  }
}
```

### Example 2: Semantic Drift Detected and Fixed

**Before (drift detected):**

```typescript
// Module A (CRM Service)
interface Customer {
  id: string;          // CRM's internal ID (UUID)
  email: string;
  status: string;      // "lead" | "active" | "churned"
}

// Module B (Billing Service)
interface Customer {
  id: number;          // Billing's internal ID (auto-increment)
  email_address: string; // Different field name
  status: string;      // "active" | "past_due" | "cancelled"  // Different values
  crm_id: string;      // CRM ID stored separately (fragile mapping)
}

// Problem: Same concept, completely different representations
// Changes in A silently break B
```

**After (integrity restored):**

```typescript
// shared/contracts/customer-contract.ts
export interface CustomerContract {
  id: string;            // UUID — canonical customer ID
  email: string;         // Canonical field name
  status: CustomerStatus;
}

export enum CustomerStatus {
  Lead = "lead",
  Active = "active",
  PastDue = "past_due",
  Churned = "churned",
  Cancelled = "cancelled",
}

// Module A uses shared contract + its own extensions
// Module B uses shared contract + its own extensions
// Both agree on the canonical representation of a "Customer"
```

### Example 3: Cross-Boundary Invariant

```typescript
// shared/invariants/account-invariants.ts
/**
 * INVARIANT: An account can have at most one active subscription.
 * 
 * This invariant applies across ALL modules that modify subscriptions:
 * - BillingService (creates/cancels subscriptions)
 * - AdminService (manually overrides subscriptions)
 * - SelfService (user upgrades/downgrades)
 * 
 * All modules MUST check this invariant before modifying subscriptions.
 */

export function assertNoActiveSubscription(
  subscriptions: Subscription[]
): void {
  const activeSubscriptions = subscriptions.filter(s => s.isActive());
  if (activeSubscriptions.length > 1) {
    throw new InvariantViolationError(
      `Found ${activeSubscriptions.length} active subscriptions. ` +
      'Maximum is 1.'
    );
  }
}

// This invariant is tested in every module:
// BillingService tests
it('enforces single active subscription invariant', async () => {
  const customer = await createCustomerWithActiveSubscription();
  await expect(
    subscriptionService.createSubscription(customer.id)
  ).rejects.toThrow(InvariantViolationError);
});

// AdminService tests
it('enforces single active subscription invariant', async () => {
  const customer = await createCustomerWithActiveSubscription();
  await expect(
    adminService.overrideSubscription(customer.id, 'premium')
  ).rejects.toThrow(InvariantViolationError);
});
```

---

## Anti-Patterns

### 1. Validation Scattered Everywhere

**Symptoms:** Each layer validates the same data, but with potentially different rules.

**Detection:** `if (!data.field)` or similar checks appear in multiple files for the same data.

**Fix:** Centralize validation at the boundary with a single parser. Internal code trusts parsed data.

### 2. Copy-and-Paste Types

**Symptoms:** Each module has its own copy of shared types, and they drift apart over time.

**Detection:** Grep for `interface User` across the codebase — if it appears in more than one place, drift is likely.

**Fix:** Define shared types once in a shared package. All modules import from there.

### 3. Implicit Data Transformations

**Symptoms:** Data flows between components with undocumented transformations (field name changes, format changes, value mappings).

**Detection:** Search for `data.* = otherData.*` patterns at module boundaries.

**Fix:** Make all transformations explicit with named functions. Document the semantic reason for each transformation.

### 4. The "Works on My Machine" Contract

**Symptoms:** Contracts are documented in human conversation or README files but not in code.

**Detection:** Knowledge about data format at boundaries lives only in developer's heads.

**Fix:** Express every contract in code (types, schemas, parsers). Enforce them with automated checks.

### 5. Cross-Boundary Reach-Through

**Symptoms:** Component A reaches through Component B to access Component C's data directly, bypassing B's public interface.

**Detection:** Import paths that go 2+ levels deep: `import X from 'b/internal/deep/c'`.

**Fix:** Each component should only interact with its immediate neighbor's public interface. If C's data is needed, B should expose it.

### 6. Silent Error Handling

**Symptoms:** Errors at boundaries are silently caught, logged, or swallowed, hiding semantic issues.

**Detection:** Empty catch blocks, `console.error` without re-throw, default values that mask errors.

**Fix:** Errors at boundaries are semantic integrity violations. Fail fast. Surface them immediately.

---

## Conclusion

Semantic Integrity is the principle that ensures AI agents can work across component boundaries without accidentally breaking the system. By making contracts explicit, parsing at boundaries, and verifying meaning is preserved, AIOA enables safe, distributed AI development.

**Key takeaways:**
1. Every boundary needs an explicit semantic contract
2. Parse at boundaries, trust internally ("Parse, Don't Validate")
3. Version contracts when they change
4. Test semantic integrity with round-trip and contract tests
5. Monitor for drift with automated tooling

**Remember:** If an AI agent can't determine whether its change preserves meaning, it can't make that change safely.
