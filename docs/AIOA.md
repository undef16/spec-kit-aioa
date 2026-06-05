# AIOA - AI-Oriented Architecture

> AIOA does not replace existing architecture styles. It refines them for codebases that are read, reviewed, and modified by AI coding agents. The optimization target is simple: reduce how much context an agent must traverse before it can safely change the system.

This document is the single source of truth for AIOA principles used by this Spec Kit preset.

## Core Objective

### Minimize Crystallization Radius

**Crystallization Radius** is the amount of system context an AI agent must traverse before it can safely understand, modify, test, or verify a component.

Large radius creates:

- broad repository searches;
- dependency-chain traversal;
- excessive abstraction reading;
- context-window inflation;
- expensive debugging cycles;
- higher risk of incorrect patches.

Small radius creates:

- local reasoning;
- isolated modifications;
- deterministic testing;
- predictable retrieval;
- lower token consumption;
- safer code generation.

Every architectural decision should be evaluated by one question:

> How much additional context must an AI agent consume before making a safe change?

If a decision expands the Crystallization Radius without preserving important domain meaning, it carries an operational cost.

### Preserve Semantic Integrity

AIOA has two constraints:

1. **Minimize Crystallization Radius** - reduce traversal cost.
2. **Preserve Semantic Integrity** - keep domain meaning explicit and protected.

Reducing traversal without semantic integrity causes **Semantic Collision**: distinct business concepts collapse into the same names, primitives, or contracts.

Preserving semantics without controlling traversal causes context explosion.

Both constraints must evolve together.

## Architectural Position

AIOA is orthogonal to deployment topology.

It applies to:

- modular applications;
- monoliths;
- microservice systems;
- distributed systems;
- event-driven platforms;
- hybrid enterprise environments.

A poorly structured microservice ecosystem can have a larger Crystallization Radius than a well-structured modular application. A distributed platform can remain highly local when boundaries, contracts, and reasoning paths are explicit.

AIOA evaluates how software is understood and safely modified. It does not prescribe where software is deployed.

## Design Bias

AIOA favors:

- local reasoning;
- explicit boundaries;
- context isolation;
- atomic components;
- deterministic contracts;
- observable state transitions;
- minimal traversal requirements.

AIOA disfavors:

- hidden dependencies;
- deep abstraction chains;
- architectural glue layers;
- context scattering;
- runtime ambiguity;
- excessive orchestration;
- primitive domain data crossing boundaries.

## Technical Implementation Patterns

### TIP-001: AI Usage Is Not a KPI

**Problem:** Teams measure prompt count, token usage, AI session count, or time spent in AI tools as productivity metrics.

**Why it matters:** This rewards token burning, not engineering outcomes. Good AI-assisted work often means fewer prompts, smaller context, faster verification, and cleaner decisions.

**Rule:** Measure outcomes, decision quality, customer impact, delivery speed, defect rate, and maintainability. Do not measure AI usage itself as a performance target.

**AIOA interpretation:** Token efficiency is an architecture concern, not a vanity metric. The goal is to make work require less AI traversal, not to make people use more AI.

### TIP-002: Semantic Collision

**Problem:** Different domain concepts share the same primitive type, generic name, or structural shape. An AI agent starts treating them as interchangeable.

Example failure:

- `TradingDayTime`
- `TuningDayTime`
- `EvalDayTime`

If these collapse into `day_time`, the code can remain syntactically correct, type-safe, deployable, and test-green while business semantics are destroyed.

**Pattern:** Represent each domain concept with its own type, even if the underlying representation is identical.

```text
type UserId wraps string
type PaymentId wraps string

function getUser(id: UserId): User
function getPayment(id: PaymentId): Payment
```

**Anti-pattern:**

```text
function getUser(id: string): User
function getPayment(id: string): Payment

getUser(paymentId)  // compiler cannot catch the semantic bug
```

#### Domain Identifier Rule

A field representing a domain identifier must use a value type, not a primitive.

This applies to:

- user IDs;
- order IDs;
- strategy names;
- account IDs;
- instrument symbols;
- workflow IDs;
- any domain-significant identifier.

The value type must:

1. Be distinct from the underlying primitive.
2. Optionally validate the value at construction.
3. Encode business meaning in the type name.

The mechanism is language-specific. The rule is universal.

### TIP-003: Repository Search Bottleneck

**Problem:** AI agents spend a large share of execution time searching, reading, and reconstructing repository context before writing a small patch.

Source code is not a flat text corpus. It is a dependency graph.

Agents need:

- caller/callee relationships;
- blast-radius analysis;
- dependency tracing;
- test relationship awareness;
- architectural impact mapping.

**Pattern:** Organize code so relevant behavior is discoverable through narrow, explicit modules and structural relationships.

```text
payment/
  contracts/
  actors/
  policies/
  tests/

billing/
  contracts/
  actors/
  policies/
  tests/
```

An agent changing payment logic should not need to read billing, notification, and a global utility module unless the change truly crosses those boundaries.

**Anti-pattern:**

```text
utils.py       // 2000 lines, 50 unrelated functions
services.py    // mixed billing, payment, notification, auth
helpers.py     // imported by half the repository
```

#### Repository Locality Rule

Prefer:

- cohesive directories around business boundaries;
- small modules with one reason to change;
- explicit contracts near the boundary they protect;
- tests close to the behavior they verify;
- structural graph tooling for impact analysis.

Avoid:

- global utility dumping grounds;
- wildcard imports;
- cross-domain helper modules;
- files that every change requires reading.

### TIP-004: Code Crystallization

**Problem:** Architecture accumulates pass-through layers, mediator chains, factory chains, interface wrappers, and forwarding classes that add traversal but no meaning.

**Goal:** Maximize business-logic density while minimizing Crystallization Radius.

**Pattern:** Keep behavior close to its owning boundary. Use abstractions only when they reduce real complexity, protect a real contract, or encode a meaningful policy.

```text
class PaymentProcessor:
    function charge(amount):
        return gateway.charge(amount)
```

**Anti-pattern:**

```text
PaymentController
  -> PaymentRouter
  -> PaymentHandler
  -> PaymentService
  -> PaymentRepository
  -> Gateway

// each layer forwards without validation, transformation, policy, or ownership
```

#### Pass-Through Wrapping Rule

A function, method, class, file, or re-export that exists only to invoke another function, method, class, file, or symbol with the same signature is a pass-through.

Pass-throughs are allowed only when they provide at least one of:

1. Validation or invariant enforcement.
2. Logging, telemetry, or policy enforcement.
3. Meaningful signature or contract transformation.
4. A documented public API boundary while the inner function remains internal.

If none apply, remove the wrapper and call the real behavior directly.

### TIP-005: Quantum Spectrum

**Problem:** Components at different abstraction levels are indistinguishable. Everything becomes a "service", "manager", "helper", or "utility" regardless of size, responsibility, and reuse pressure.

**Pattern:** Use explicit actor levels as reasoning boundaries.

```text
Micro Actor: Billing
  Primary business boundary and bounded context.

Nano Actor: ApplyDiscount
  Reusable business workflow.

Pico Actor: FormatInvoiceNumber
  Deterministic execution primitive.
```

#### Micro Actors

Micro Actors define primary business boundaries.

Examples:

- Billing;
- Inventory;
- Ordering;
- Customer Management.

Responsibilities:

- own business capabilities;
- define bounded contexts;
- contain local business workflows.

An AI task should usually begin at the owning Micro Actor.

#### Nano Actors

Nano Actors encapsulate reusable business workflows.

Examples:

- `ApplyDiscount`;
- `ValidatePromotion`;
- `CalculateTax`;
- `DetermineShippingMethod`.

Responsibilities:

- coordinate business rules;
- support reuse across features;
- prevent meaningful logic duplication.

#### Pico Actors

Pico Actors encapsulate deterministic execution primitives.

Examples:

- `FindCustomerById`;
- `FormatInvoiceNumber`;
- `PublishTelemetryEvent`;
- `SerializeContract`.

Responsibilities:

- perform one explicit operation;
- expose minimal ambiguity;
- contain little or no branching logic.

#### Extraction Rule

Start large. Extract downward only when reuse pressure appears.

1. Implement new behavior inside the owning Micro Actor.
2. If business behavior becomes reusable, extract it into a Nano Actor.
3. If deterministic technical behavior becomes reusable, extract it into a Pico Actor.

This prevents premature abstraction while preserving future flexibility.

### TIP-006: Declarative Straight-Line Code

**Problem:** Business logic is buried inside manual execution mechanics: nested branching, loops, retries, locks, transactions, resource scopes, callback chains, and exception tunnels.

The agent must track execution state before it can safely change business behavior.

**Pattern:** Move recurring execution mechanics into explicit reusable constructs. Business code should describe intent in a linear path.

```text
retryPolicy = RetryPolicy(maxAttempts=3, backoff="exponential")

function chargeCustomer(amount):
    return retryPolicy.execute(() => gateway.charge(amount))
```

**Anti-pattern:**

```text
function chargeCustomer(amount):
    for attempt in 1..3:
        try:
            return gateway.charge(amount)
        except NetworkError:
            if attempt == 3:
                throw
            sleep(2 ^ attempt)
```

#### Execution Policy Rule

Execution mechanics belong in policies, boundaries, libraries, or prepared primitives, not scattered through business methods.

Good candidates for declarative primitives:

- validation pipelines;
- retry policies;
- timeout policies;
- transaction boundaries;
- resource scopes;
- concurrency limits;
- result types;
- event handlers;
- collection pipelines.

Guard clauses are still useful for visible business preconditions. They solve conditional nesting. TIP-006 targets the broader problem of manual procedural machinery.

### TIP-007: Strict JSON Gateways and Auditable DTOs

**Problem:** Loose JSON, raw dictionaries, nullable structures, and ambiguous payloads leak into business logic. AI agents respond by generating defensive boilerplate everywhere.

**Core rule:** Loose JSON must die at the boundary.

#### Strict JSON Gateway

A Strict JSON Gateway:

1. Accepts loose external input.
2. Validates it against a strict schema.
3. Rejects malformed payloads immediately.
4. Converts valid input into typed DTO contracts.
5. Passes only trusted DTOs into business logic.

```text
gateway PromoRequestGateway:
    accepts json
    validates PromoRequestSchema
    returns PromoRequest
```

After the gateway:

```text
function applyPromo(request: PromoRequest):
    promo = database.findPromo(request.code)

    if promo not found:
        throw PromoNotFound

    apply(promo, request.customerId)
```

The remaining checks are business validation, not technical sanitation.

#### Perimeter Validation Rule

Validate at the perimeter:

- required fields;
- JSON shape;
- primitive types;
- enum membership;
- ID format;
- string normalization;
- basic range checks;
- schema version compatibility.

Keep in business logic:

- whether an entity exists;
- whether a customer is eligible;
- whether a discount is combinable;
- whether an account may perform an action;
- whether a workflow transition is valid.

The gateway protects structure. The business layer protects meaning.

#### ADTO Contract

When runtime state provenance matters, use an Auditable DTO (ADTO).

An ADTO is a typed DTO that also records meaningful business state transitions.

An object claimed to be an ADTO must provide:

1. **A deterministic typed contract** - required fields, allowed types, nullability, and structural guarantees are explicit.
2. **Controlled mutation semantics** - either immutable snapshots or controlled transition methods. The object must not allow untracked state changes.
3. **Auditability** - a method to record a business-significant state transition.
4. **History retrieval** - a method to retrieve ordered mutation history.
5. **Optional provenance** - caller, operation, reason, timestamp, trace ID, or source component when useful.

Example:

```text
structure PropertyChange:
    propertyName: String
    oldValue: Any
    newValue: Any

structure TraceEntry:
    timestamp: Datetime
    operation: String
    callerClass: String
    callerMethod: String
    reason: String
    changes: List[PropertyChange]
    snapshot: Object

abstract class ADTO:
    private history: List[TraceEntry] = []

    function recordMutation(operation, reason, changes):
        history.add(
            TraceEntry(
                timestamp = Clock.utcNow(),
                operation = operation,
                callerClass = StackTrace.externalClass(),
                callerMethod = StackTrace.externalMethod(),
                reason = reason,
                changes = deepClone(changes),
                snapshot = deepClone(this)
            )
        )

    function mutationHistory(): List[TraceEntry]:
        return history
```

#### Mutation Slice Rule

ADTOs should record meaningful business transitions, not every setter call.

Good mutation slice:

```text
operation: ApplyPaymentFailurePolicy
reason: Failed payment threshold exceeded

changes:
  status: Active -> Suspended
  riskScore: 20 -> 95
```

The goal is explainability, not compliance noise.

**Anti-patterns:**

```text
function process(data: dict): Result
```

```text
class Order:
    _provenance: list  // manually maintained, easy to forget, incomplete
```

### TIP-008: Event-Driven Integration

**Problem:** Workflows are coupled through direct cross-component calls. A simple business change forces the agent to understand callers, receivers, ordering, retries, side effects, and distributed failure behavior.

**Goal:** Reduce cross-boundary reasoning by communicating through explicit business events.

**Core rule:** Micro Actors, Nano Actors, and Pico Actors must not call each other's methods directly. All cross-actor communication goes through one event mechanism.

Events are contracts. They should be:

- immutable;
- typed;
- versioned when crossing durable or external boundaries;
- business-oriented;
- implementation-independent.

Examples:

```text
PaymentRequested
PaymentCompleted
InventoryReserved
OrderCancelled
```

#### Locality Principle

A component should not need to understand how another component performs its work.

It should understand:

- the event it emits;
- the event it consumes;
- its own local business rules.

#### Event Choreography Rule

A workflow is choreography-oriented when:

1. The entry point emits a command or fact event and exits.
2. Each actor subscribes to one or more events.
3. Actor method calls target only the actor's own dependencies, not another actor's internal behavior.
4. State transitions are observable as event emissions or ADTO mutation history.

This rule is structural. A workflow violates TIP-008 as soon as one actor invokes another actor's method, regardless of whether the class is named `Service`, `Controller`, `Coordinator`, `Orchestrator`, `Manager`, or `Actor`.

Violation:

```text
class OrderService:
    function placeOrder(cart):
        billingService.applyCharge(amount)
        notificationService.sendEmail(user)
```

Required actor-to-actor form:

```text
class OrderActor:
    function placeOrder(cart):
        return OrderPlaced(orderId, customerId, total)

class BillingActor:
    @handler(OrderPlaced, PaymentRequested)
    function requestPayment(event):
        return PaymentRequested(event.orderId, event.total)

class NotificationActor:
    @handler(OrderPlaced, EmailRequested)
    function requestEmail(event):
        return EmailRequested(event.customerId, "order placed")
```

#### Event Bus Rule

Use one event mechanism inside a boundary.

Default for a single-process system:

- an in-process event bus or dispatcher.

If Kafka, RabbitMQ, an actor runtime, or another broker is already the system's event mechanism:

- use it directly;
- do not add a second bus layer only to satisfy the pattern.

The technology is an implementation decision. The architectural pattern is explicit event contracts and local handlers.

#### Scope and Allowed Synchronous Calls

The "event bus only" rule applies to actor-to-actor communication.

It does not forbid an actor from synchronously calling its own local dependencies, such as:

- repositories owned by that actor;
- gateways to external systems;
- policy objects;
- validators;
- mappers;
- transaction boundaries;
- retry policies;
- telemetry clients.

Those calls are implementation dependencies of the actor, not communication with another actor.

If a dependency owns independent business behavior, it is an actor and must be reached through an event.

Event-Driven Integration does not require every event mechanism to be distributed or asynchronous. An in-process event bus is valid. The strict requirement is actor decoupling through explicit event contracts.

#### Concrete Implementation Patterns

**Event-as-ADTO**

Events that cross meaningful boundaries should be typed DTOs. When provenance matters, make them ADTOs.

```text
class PaymentRequested extends ADTO:
    orderId: OrderId
    amount: Money
    currency: Currency
    traceId: TraceId
    timestamp: Datetime
```

**Declarative Handler Binding**

```text
@handler(OrderPlaced, InventoryReserved)
function reserveInventory(event: OrderPlaced): InventoryReserved
```

The pipeline builder validates that the declared event type and method annotation match.

**Handler Auto-Publish**

```text
@handler(OrderPlaced, InventoryReserved)
function reserveInventory(event: OrderPlaced): InventoryReserved:
    return InventoryReserved(orderId=event.orderId)
```

Returned events are published automatically. Lists are published item by item.

**Error Isolation with Continuation**

One failed handler should not silently corrupt the whole pipeline. The event mechanism must define failure behavior explicitly:

- log and continue;
- retry;
- dead-letter;
- fail the command;
- compensate.

Choose based on business semantics. Do not leave it implicit.

## Review Checklist

Use this checklist when reviewing specs, plans, tasks, and code changes.

| Principle | Review question | Common violation |
| --- | --- | --- |
| TIP-001 | Are AI metrics outcome-oriented? | Measuring prompts, tokens, or AI session count as productivity. |
| TIP-002 | Are domain concepts represented by semantic types? | User IDs, order IDs, strategy names, or workflow IDs passed as raw strings. |
| TIP-003 | Can relevant behavior be found locally? | Global `utils`, `helpers`, or mixed `services` modules imported across domains. |
| TIP-004 | Does each layer add meaning, policy, transformation, or a real boundary? | Pass-through wrappers and forwarding chains. |
| TIP-005 | Are Micro, Nano, and Pico responsibilities distinguishable? | Everything named `Service`, `Manager`, or `Helper` regardless of abstraction level. |
| TIP-006 | Is business logic linear and intent-focused? | Manual retry, timeout, transaction, lock, fallback, or nested error mechanics in business methods. |
| TIP-007 | Does loose input die at a strict boundary? | Raw `dict` / loose JSON crossing into business logic. |
| TIP-007 | Is important state provenance explainable? | DTOs with important mutable state but no mutation history. |
| TIP-008 | Do actors communicate only through events? | Micro/Nano/Pico actors calling each other's methods directly. |
| TIP-008 | Is one event mechanism used per boundary? | Adding a second bus wrapper over an existing broker without architectural value. |
| Cross-cutting | Are state transitions observable? | Hidden state changes with no event, ADTO history, or focused telemetry. |

## Usage

Templates and commands in this preset reference this file as the canonical AIOA definition.

When a project-specific decision conflicts with a generic pattern, document the reason explicitly in the spec or plan. AIOA is an optimization framework, not a substitute for business constraints.
