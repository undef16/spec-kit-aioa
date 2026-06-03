# AIOA — AI-Oriented Architecture

> AIOA does not replace existing architectures. AIOA is a **refinement** for AI coding assistants (Claude Code, Copilot, Cursor) that read, review, and modify your codebase. Each TIP answers: "how would an AI engineer see this code for the first time and safely change it?"

## Technical Implementation Patterns (TIPs)

### TIP-002: Semantic Collision
The same name or type for different concepts — an AI agent cannot distinguish entities without deep context.
**Pattern:** Each entity has its own type, even if technically the same primitive structure. `UserId` and `PaymentId` are distinct types.
```text
// Pattern: distinct types for distinct concepts
type UserId = string    // "usr_xxx"
type PaymentId = string // "pay_xxx"

function getUser(id: UserId): User
function getPayment(id: PaymentId): Payment
```
**Anti-Pattern:** All identifiers are `str`. AI cannot tell `user_id` from `payment_id` without reading the entire call chain.
```text
// Anti-Pattern: everything is string
function getUser(id: string): User
function getPayment(id: string): Payment
// compiler cannot catch: getUser(paymentId) // BUG
```

#### Domain Identifier Rule

A field representing a domain identifier (user ID, order ID, strategy name, etc.) must use a value type, not a primitive. This applies even when all IDs are structurally the same primitive.

The value type must:
1. Be distinct from the underlying primitive (so accidental interchange is prevented by the type system)
2. Optionally validate the value at construction (e.g., "this strategy name is registered")

Pseudo example — the wrapper type delegates to a primitive but is typed as a distinct concept:
```text
// Pseudo — domain identifier as a value type
type UserId wraps string      // distinct from primitive
type OrderId wraps string     // compiler prevents accidental interchange

function createUser(id: UserId): User
// createUser(orderId)  ← compiler error, type mismatch
```

The mechanism is per-language. The principle is universal.

### TIP-003: Repository Search Bottleneck
A single file or module becomes a bottleneck — AI must read it to understand anything in the system.
**Pattern:** Responsibility distributed across narrow, specialized modules. Each module solves one task.
```text
// Pattern: narrow modules, single responsibility
import payment/
import billing/
import notification/
// AI reads only payment/ to understand payment logic
```
**Anti-Pattern:** A 2000-line `utils.py` imported by half the codebase. AI reads it entirely for any change.
```text
// Anti-Pattern: everything in one file
from utils import *         // 2000 lines, 50 unrelated functions
// AI must read all 2000 lines — cannot know what's needed
```

### TIP-004: Code Crystallization
A chain of wrappers where each element only forwards control without adding value.
**Pattern:** Direct A→C call when intermediate B adds no transformation or validation.
```text
// Pattern: call directly
class PaymentProcessor:
    function charge(amount):
        return Gateway.charge(amount)  // direct call
```
**Anti-Pattern:** A→Router→Handler→Service→Repository where every step is forwarding without logic.
```text
// Anti-Pattern: dead indirection chain
PaymentController → PaymentRouter → PaymentHandler
    → PaymentService → PaymentRepository → Gateway
// each layer just forwards — zero value added
// AI must read ALL 5 files to understand "charge"
```

#### Pass-Through Wrapping Rule

A function, method, or class that exists only to invoke another function, method, or class with the same signature is a pass-through. It adds no value and should be removed.

Pass-throughs are allowed only if they provide at least one of:
1. Validation or invariant enforcement
2. Logging or telemetry
3. Meaningful signature transformation
4. Acts as a documented public API boundary, with the inner function being internal

If none of (1)–(4) apply, the caller should invoke the inner function directly. The wrapper is dead indirection and an anti-pattern of TIP-004.

This rule applies to:
- Functions that call other functions with identical signatures
- Wrapper classes that only forward to an inner class
- Re-exports under a different name without transformation
- Files containing only a docstring-redirector and no executable code

The pattern is universal: a layer whose sole purpose is to forward to another layer, regardless of the language mechanism used to implement it.

### TIP-005: Quantum Spectrum
Components at different abstraction levels are indistinguishable by name — everything is called "service" despite different complexity.
**Pattern:** Pico Actor — deterministic primitive, Nano Actor — reusable business workflow, Micro Actor — primary business boundary. Different levels, different names. Prefer stateless — ADTO (TIP-007) handles state when needed.
```text
// Pattern: named by level
pico actor FormatPostalCode(input: string): string     // deterministic primitive
nano actor ApplyDiscount(order, customer): Order        // reusable business workflow
micro actor BillingService: manages invoices, payments   // primary business boundary
```
**Anti-Pattern:** Everything called "Service" regardless of whether it is a pure function or a distributed microservice.
```text
// Anti-Pattern: everything is "Service"
class FormatService        // actually: formatPostalCode(a, b): string
class DiscountService      // actually: applyDiscount(order): Order
class BillingService       // actually: microservice with DB, queue, API
// AI cannot distinguish simple functions from complex subsystems
```

#### Extraction Rule

The Quantum Spectrum follows a simple principle:

**Start large. Extract downward only when reuse pressure appears.**

Workflow:

**Step 1:** Implement new behavior inside the parent Micro Actor.

**Step 2:** If business behavior becomes reusable, extract it into a Nano Actor.

**Step 3:** If deterministic technical behavior becomes reusable, extract it into a Pico Actor.

This prevents premature abstraction while preserving future flexibility.

### TIP-006: Declarative Straight-Line Code
Business logic mixed with execution mechanics (retry, fallback, timeouts) creating deep nesting.
**Pattern:** Execution mechanics extracted into separate abstractions (RetryPolicy, TimeoutPolicy). Business code stays linear and declarative.
```text
// Pattern: retry policy extracted with ADTO config
struct RetryConfig(ADTO):
    maxAttempts: int
    backoff: string

retryPolicy = RetryPolicy(config=RetryConfig(maxAttempts=3, backoff="exponential"))

function chargeCustomer(amount):
    return retryPolicy.execute(() => gateway.charge(amount))
// business logic is ONE line — retry mechanic is abstracted
```
**Anti-Pattern:** try/except/retry boilerplate repeated in every function. Business logic buried under three levels of error handling.
```text
// Anti-Pattern: hand-written retry in every function
function chargeCustomer(amount):
    for attempt in 1..3:
        try:
            return gateway.charge(amount)
        except NetworkError:
            if attempt == 3: throw
            sleep(2^attempt)
// business logic hidden inside error handling — AI reads 10 lines for 1 intent
```

### TIP-007: Auditable Data Transfer Objects (ADTO)
Data crossing boundaries must be typed AND auditable. ADTO combines strict type safety with automatic mutation history.

#### ADTO Contract (language-agnostic)

An object claimed to be an ADTO must satisfy three requirements, independent of language or implementation:

1. **Immutability** — the object's state cannot be modified after construction by any means available in the host language (frozen data classes, readonly fields, immutable interfaces, persistent data structures, etc.). The mechanism is per-language; the requirement is universal.
2. **Auditability** — the object must provide:
   - A method to record a state transition (operation name, reason, before-value, after-value)
   - A method to retrieve the history of transitions as an ordered sequence
3. **Optional provenance** — the object may record which class/method created it, for end-to-end traceability.

The contract is universal. The mechanism (framework, base class, code generation, annotation, etc.) is per-language and is the implementer's choice.

**Pattern:** Every boundary-crossing object satisfies the ADTO contract. The mechanism is per-language.
```text
// Pattern: typed boundary data with audit trail
// ADTO Contract: immutable, auditable, optionally traceable
// The mechanism is per-language; the contract is universal.
```

```text
structure PropertyChange {
    property_name: String
    new_value: Any
}

structure TraceEntry {
    timestamp: Datetime
    caller_class: String
    caller_method: String
    changes: List[PropertyChange]
    snapshot: Object
}

abstract class ADTO {
    private history: List[TraceEntry] = []
    private trace_enabled: Boolean = Config.get("ADTO_TRACE_ENABLED")

    constructor() {
        if trace_enabled {
            bind_property_triggers(this)
        }
    }

    private on_property_changed(property_name: String, new_value: Any) {
        if !trace_enabled {
            return
        }

        caller = StackTrace.get_external_caller()
        last = history.last_or_null()

        change = PropertyChange(
            property_name = property_name,
            new_value = deep_clone(new_value)
        )

        if last != null
           and last.caller_class == caller.class
           and last.caller_method == caller.method {

            last.changes.upsert_by_property(property_name, change)
            last.snapshot = deep_clone(this)
            return
        }

        history.add(
            TraceEntry(
                timestamp = Clock.utc_now(),
                caller_class = caller.class,
                caller_method = caller.method,
                changes = [change],
                snapshot = deep_clone(this)
            )
        )
    }

    function mutation_history(): List[TraceEntry] {
        return history
    }
}
```
**Anti-Pattern:** Raw `dict` crossing boundaries, or manual `_provenance` field. AI must read implementation to understand structure; provenance is forgotten or incomplete.
```text
// Anti-Pattern: raw dict + manual provenance
function createOrder(data: dict) -> dict:
    // what keys does 'data' need? what keys does output have?
    // AI must read the entire function body to find out
    return {"status": "ok", "order_id": id}

class Order:
    _provenance: list  // manually maintained — forgotten, wrong, incomplete
```

### TIP-008: Event-Driven Integration
Components coupled through direct calls, creating tight coupling.
**Pattern:** All cross-actor communication goes through an event bus. Choose ONE event bus mechanism — the technology choice is an implementation decision, not an architectural pattern. By default, use an in-process InMemoryEventBus (zero infrastructure). If RabbitMQ, Kafka, or another broker is already present, use it directly — do NOT add a second bus. Pico actors, Nano actors, and Micro actors must never talk directly to each other.
```text
// Rule: ALL cross-actor communication via event bus
// Choose ONE mechanism. Default: InMemoryEventBus. If RabbitMQ already present, use that.

// In-memory event bus — simple publish/subscribe within process
class InMemoryEventBus:
    handlers = Map<Type, List<Handler>>()

    function publish<T>(event: T):
        for handler in handlers[type(event)]:
            handler(event)

    function subscribe<T>(handler: Handler<T>):
        handlers[type(event)].add(handler)

// All actors communicate ONLY through the bus:
// Pico → event → Nano → event → Micro

// Pico actor (pure function) publishes result
pico actor ValidateAddress(addr: RawAddress):
    // validate logic
    bus.publish(AddressValidated(address, valid))

// Nano actor (shared functionality) subscribes and publishes
nano actor ShippingManager:
    bus.subscribe<AddressValidated>(onAddressValidated)
    function onAddressValidated(event):
        if event.valid:
            bus.publish(ShipmentPrepared(orderId, address))
        else:
            bus.publish(ValidationFailed(orderId, reason))

// Micro actor (independent service) subscribes
micro actor LogisticsService:
    bus.subscribe<ShipmentPrepared>(onShipmentPrepared)
    function onShipmentPrepared(event):
        // call external logistics API
```

**Key rule:** The event bus technology is an implementation decision, not an architectural pattern. By default, use InMemoryEventBus (zero infrastructure). If RabbitMQ/Kafka is already present in the deployment, components emit events to it directly — no second bus needed. The choice stays within the same component boundary.

**Anti-Pattern:** `ComponentA` calls `B.internal_method()` directly. Coupling grows — changing one component requires changing the other.
```text
// Anti-Pattern: direct call to actor internal method
class OrderService:
    function placeOrder(cart):
        // ...
        billingService.applyCharge(amount)  // direct call to Nano actor
        notificationService.sendEmail(user)  // direct call to Pico actor
// AI must read billing + notification internals to understand order placement
// Changing billing.interface breaks OrderService
```

#### Event Choreography

A workflow satisfies choreography-only when it has all three properties:

1. The Pico entry point emits a single command event and exits. It does not invoke any other actor's methods.
2. Each actor subscribes to one or more events. An actor's method invocations target only its own dependencies, never another actor.
3. State transitions are observable as event emissions. No state transition is implemented as a direct call from one actor to another.

A workflow violates this rule as soon as an actor invokes a method on another actor. The presence of an "Orchestrator", "Coordinator", or "Controller" that drives the workflow is a strong signal of violation, but the rule itself is structural (look at call sites) and does not depend on naming.

All events are valid. What is forbidden is direct method calls between actors.

ADTO (TIP-007) makes event-driven workflows transparent: each event carries a typed, auditable payload. This allows tracking all state transitions, understanding process chains, and finding bugs by reading the event history without reading actor internals.

### Anti-Patterns by Principle

The principles below are universal. Each is shown with a pseudo-code example. The linter under each language encodes the detection.

---

**TIP-002 — Untyped IDs**

A domain identifier is a concept, not a primitive. Its type must be distinct from the primitive it wraps, so the type system can prevent accidental interchange of IDs from different concepts.

Typical violation:
```text
// Violation: domain identifier stored as a raw primitive
type UserId = string    // bare primitive — compiler cannot distinguish
type OrderId = string   // UserId and OrderId are the same type
```

Typical fix:
```text
// Fix: distinct value type wrapping the primitive
type UserId wraps string    // distinct type — compiler catches misuse
type OrderId wraps string   // UserId and OrderId are different types
```

---

**TIP-004 — Dead indirection**

A pass-through layer that adds no behavior should be removed, not reduced.

Typical violation:
```text
// Violation: wrapper that adds no behavior — pure forwarding
function handleRequest(data): Response {
    return inner.handleRequest(data)  // zero transformation
}

// The language mechanism varies (struct embedding, class extension, interface delegation).
// The pattern is the same: a layer whose sole purpose is to forward to another.
```

---

**TIP-006 — Control flow in business code**

Execution mechanics (retries, locks, logging severity, error branching) belong in policies, not in business methods.

Typical violations:
- A runtime branch on environment flags for severity policy (`if dev_mode: ... else: ...` deciding between `logger.warning` and `logger.error`)
- Nested `for/try/except/if` more than three levels deep in a single method
- Manual retry loops inside business logic when a retry policy is available
- Inline environment-flag branching for any execution concern (timeout, retry, fallback, severity)

---

**TIP-007 — Untyped data crossing boundaries**

A data structure passing across an actor boundary must have a defined type. Generic maps defeat static analysis and force the consumer to read the producer's code to understand the data.

Typical violation:
```text
// Violation: untyped dictionary crossing a boundary
function process(data: Dict): Result
// consumer must read the entire function body to understand the data shape
```

The fix is a typed object with named fields. ADTOs without `record_mutation` / history are also a violation of the auditable half of the contract (see Section A).

---

**TIP-008 — Direct calls between actors**

An actor's method invocations target only its own dependencies. Invoking another actor's method is a structural violation, regardless of language.

Typical violations:
- A `MicroActor.run()` method that calls `NanoActor.do_thing()` directly
- A `pico_actor_main()` function that calls `micro_actor.run()` directly
- An "orchestrator" / "coordinator" / "controller" class that drives the workflow through method calls

In all cases, the fix is the same: the caller emits a command event and exits; the callee subscribes to that event and reacts. See the Event Choreography structural rule above.

## Usage

Each template and command in this preset references AIOA.md as the single source of truth for all TIP definitions.
