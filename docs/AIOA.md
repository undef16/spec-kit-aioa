# AIOA - AI-Oriented Architecture

> AIOA ≠ replacement for existing architectures. AIOA **refines** architecture for AI coding assistants (Claude Code, Copilot, Cursor). Each TIP answers: "How AI engineer sees code first time? How to change safely?"

## Technical Implementation Patterns (TIPs)

### TIP-002: Semantic Collision
Same name or type for different concepts. AI agent cannot distinguish entities without deep context.
**Pattern:** Each entity owns distinct type, even if same primitive structure underneath. `UserId` and `PaymentId` - different types.
```text
// Pattern: distinct types for distinct concepts
type UserId = string    // "usr_xxx"
type PaymentId = string // "pay_xxx"

function getUser(id: UserId): User
function getPayment(id: PaymentId): Payment
```
**Anti-Pattern:** All identifiers = `str`. AI cannot distinguish `user_id` from `payment_id` without reading full call chain.
```text
// Anti-Pattern: everything is string
function getUser(id: string): User
function getPayment(id: string): Payment
// compiler cannot catch: getUser(paymentId) // BUG
```

#### Domain Identifier Rule

Field representing domain identifier (user ID, order ID, strategy name, etc.) must use value type. NOT primitive. Applies even when all IDs structurally same primitive.

Value type must:
1. Be distinct from underlying primitive - type system prevents accidental interchange
2. Optionally validate value at construction (e.g. 'this strategy name is registered')

Pseudo example - wrapper type delegates to primitive but typed as distinct concept:
```text
// Pseudo - domain identifier as a value type
type UserId wraps string      // distinct from primitive
type OrderId wraps string     // compiler prevents accidental interchange

function createUser(id: UserId): User
// createUser(orderId)  ← compiler error, type mismatch
```

Mechanism per-language. Principle universal.

### TIP-003: Repository Search Bottleneck
Single file or module becomes bottleneck. AI must read it to understand anything in system.
**Pattern:** Responsibility distributed across narrow specialized modules. Each module solves one task.
```text
// Pattern: narrow modules, single responsibility
import payment/
import billing/
import notification/
// AI reads only payment/ to understand payment logic
```
**Anti-Pattern:** 2000-line `utils.py` imported by half codebase. AI reads entire file for any change.
```text
// Anti-Pattern: everything in one file
from utils import *         // 2000 lines, 50 unrelated functions
// AI must read all 2000 lines - cannot know what's needed
```

### TIP-004: Code Crystallization
Chain of wrappers. Each element forwards control. Zero value added.
**Pattern:** Direct A→C call. Intermediate B adds nothing - no transformation, no validation.
```text
// Pattern: call directly
class PaymentProcessor:
    function charge(amount):
        return Gateway.charge(amount)  // direct call
```
**Anti-Pattern:** A→Router→Handler→Service→Repository. Every step forwards. Zero logic.
```text
// Anti-Pattern: dead indirection chain
PaymentController → PaymentRouter → PaymentHandler
    → PaymentService → PaymentRepository → Gateway
// each layer just forwards - zero value added
// AI must read ALL 5 files to understand "charge"
```

#### Pass-Through Wrapping Rule

Function, method, or class existing only to invoke another with same signature = pass-through. Adds zero value. Remove.

Pass-throughs allowed ONLY if providing at least one of:
1. Validation or invariant enforcement
2. Logging or telemetry
3. Meaningful signature transformation
4. Acts as documented public API boundary - inner function internal

If none of (1)–(4) apply, caller invokes inner function directly. Wrapper = dead indirection. Anti-pattern of TIP-004.

Rule applies to:
- Functions calling other functions with identical signatures
- Wrapper classes forwarding to inner class only
- Re-exports under different name without transformation
- Files containing docstring-redirector only - no executable code

Pattern universal: layer whose sole purpose = forward to another layer. Language mechanism irrelevant.

### TIP-005: Quantum Spectrum
Components at different abstraction levels indistinguishable by name. Everything called 'service' despite different complexity.
**Pattern:** Pico Actor - deterministic primitive. Nano Actor - reusable business workflow. Micro Actor - primary business boundary. Different levels. Different names. Prefer stateless - ADTO (TIP-007) handles state when needed.
```text
// Pattern: named by level
pico actor FormatPostalCode(input: string): string     // deterministic primitive
nano actor ApplyDiscount(order, customer): Order        // reusable business workflow
micro actor BillingService: manages invoices, payments   // primary business boundary
```
**Anti-Pattern:** Everything called 'Service' - pure function OR distributed microservice. No distinction.
```text
// Anti-Pattern: everything is "Service"
class FormatService        // actually: formatPostalCode(a, b): string
class DiscountService      // actually: applyDiscount(order): Order
class BillingService       // actually: microservice with DB, queue, API
// AI cannot distinguish simple functions from complex subsystems
```

#### Extraction Rule

Quantum Spectrum follows simple principle:

**Start large. Extract downward only when reuse pressure appears.**

Workflow:

**Step 1:** Implement new behavior inside parent Micro Actor.

**Step 2:** Business behavior reusable? Extract into Nano Actor.

**Step 3:** Deterministic technical behavior reusable? Extract into Pico Actor.

Prevents premature abstraction. Preserves future flexibility.

### TIP-006: Declarative Straight-Line Code
Business logic mixed with execution mechanics (retry, fallback, timeout). Creates deep nesting.
**Pattern:** Execution mechanics extracted into separate abstractions (RetryPolicy, TimeoutPolicy). Business code - linear, declarative.
```text
// Pattern: retry policy extracted with ADTO config
struct RetryConfig(ADTO):
    maxAttempts: int
    backoff: string

retryPolicy = RetryPolicy(config=RetryConfig(maxAttempts=3, backoff="exponential"))

function chargeCustomer(amount):
    return retryPolicy.execute(() => gateway.charge(amount))
// business logic is ONE line - retry mechanic is abstracted
```
**Anti-Pattern:** try/except/retry boilerplate repeated in every function. Business logic buried under 3 levels of error handling.
```text
// Anti-Pattern: hand-written retry in every function
function chargeCustomer(amount):
    for attempt in 1..3:
        try:
            return gateway.charge(amount)
        except NetworkError:
            if attempt == 3: throw
            sleep(2^attempt)
// business logic hidden inside error handling - AI reads 10 lines for 1 intent
```

### TIP-007: Auditable Data Transfer Objects (ADTO)
Data crossing boundaries must be typed AND auditable. ADTO combines strict type safety + automatic mutation history.

#### ADTO Contract (language-agnostic)

Object claiming ADTO status must satisfy 3 requirements. Language-independent:

1. **Immutability** - object state cannot mutate after construction. By any means available in host language (frozen data classes, readonly fields, immutable interfaces, persistent data structures, etc.). Mechanism per-language. Requirement universal.
2. **Auditability** - object must provide:
   - Method to record state transition (operation name, reason, before-value, after-value)
   - Method to retrieve transition history as ordered sequence
3. **Optional provenance** - object may record which class/method created it. End-to-end traceability.

Contract universal. Mechanism (framework, base class, code generation, annotation, etc.) per-language. Implementer's choice.

**Pattern:** Every boundary-crossing object satisfies ADTO contract. Mechanism per-language.
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
**Anti-Pattern:** Raw `dict` crossing boundaries. Or manual `_provenance` field. AI must read implementation to understand structure. Provenance forgotten or incomplete.
```text
// Anti-Pattern: raw dict + manual provenance
function createOrder(data: dict) -> dict:
    // what keys does 'data' need? what keys does output have?
    // AI must read the entire function body to find out
    return {"status": "ok", "order_id": id}

class Order:
    _provenance: list  // manually maintained - forgotten, wrong, incomplete
```

### TIP-008: Event-Driven Integration
Components coupled through direct calls. Creates tight coupling.
**Pattern:** All cross-actor communication through event bus. Choose ONE event bus mechanism. Technology choice = implementation decision. NOT architectural pattern. Default: in-process InMemoryEventBus (zero infrastructure). RabbitMQ/Kafka/other broker already present? Use it directly. Do NOT add second bus. Pico actors, Nano actors, Micro actors must NEVER talk directly.
```text
// Rule: ALL cross-actor communication via event bus
// Choose ONE mechanism. Default: InMemoryEventBus. If RabbitMQ already present, use that.

// In-memory event bus - simple publish/subscribe within process
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

**Key rule:** Event bus technology = implementation decision. NOT architectural pattern. Default: InMemoryEventBus (zero infrastructure). RabbitMQ/Kafka already present in deployment? Components emit events to it directly. No second bus needed. Choice stays within same component boundary.

**Anti-Pattern:** `ComponentA` calls `B.internal_method()` directly. Coupling grows. Changing one component requires changing other.
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

Workflow satisfies choreography-only when holding all 3 properties:

1. Pico entry point emits single command event and exits. Does NOT invoke any other actor's methods.
2. Each actor subscribes to one or more events. Actor's method invocations target only own dependencies. Never another actor.
3. State transitions observable as event emissions. No state transition implemented as direct call between actors.

Workflow violates rule as soon as actor invokes method on another actor. Presence of "Orchestrator", "Coordinator", or "Controller" driving workflow = strong violation signal. But rule itself is structural (look at call sites). Does not depend on naming.

All events valid. Forbidden: direct method calls between actors.

ADTO (TIP-007) makes event-driven workflows transparent: each event carries typed, auditable payload. Allows tracking all state transitions, understanding process chains, finding bugs by reading event history without reading actor internals.

#### Concrete Implementation Patterns

##### Pattern 1: Event-as-ADTO Pattern

Events inherit from ADTO (TIP-007). First-class data objects with full provenance:

* mutation audit trail via PropertyChange and TraceEntry;
* caller detection on every mutation;
* `extra="forbid"` prevents accidental fields;
* baked-in `trace_id: UUID` and `timestamp: datetime`.

```text
class PaymentRequested(ADTO):
    order_id: UUID
    amount: Decimal
    currency: str
    # trace_id and timestamp come from ADTO
    # extra="forbid" is inherited
    # every mutation writes a TraceEntry
```

##### Pattern 2: Declarative Handler Binding

`@handler` decorator declares what handler consumes and produces:

```text
@handler(OrderPlaced, InventoryReserved)
def reserve_inventory(event: OrderPlaced) -> InventoryReserved:
    ...
```

PipelineBuilder introspects these decorators to wire actors to bus automatically. Type annotations validated against declared input type. Mismatches caught at wiring time. NOT at runtime.

##### Pattern 3: Handler Auto-Publish

Handler returns value? PipelineBuilder wraps it. Return automatically published to bus:

```text
@handler(OrderPlaced, InventoryReserved)
def reserve_inventory(event: OrderPlaced) -> InventoryReserved:
    return InventoryReserved(order_id=event.order_id)
```

Handler returns list? Each item published individually. Eliminates boilerplate of manual publish calls inside every handler.

##### Pattern 4: Pipeline Wiring

PipelineBuilder.build(actors, bus) iterates actors. Finds @handler-decorated methods. Subscribes each to bus based on declared input type:

```text
bus = InMemoryEventBus()
pipeline = PipelineBuilder.build([checkout_actor, inventory_actor, notification_actor], bus)
```

Actor order in list determines registration order. Bus becomes pure routing layer. Does not know which handlers exist until wiring.

##### Pattern 5: Error Isolation with Continuation

Handler raises? Error logged. Other handlers for same event type continue executing:

```text
# both handle OrderPlaced
# if inventory_actor raises, notification_actor still runs
```

One failed handler does not crash pipeline. Bus logs failure. Continues dispatching to remaining subscribers.

### Anti-Patterns by Principle

Principles below universal. Each shown with pseudo-code example. Linter under each language encodes detection.

---

**TIP-002 - Untyped IDs**

Domain identifier = concept. NOT primitive. Its type must be distinct from primitive it wraps. Type system prevents accidental interchange of IDs from different concepts.

Typical violation:
```text
// Violation: domain identifier stored as a raw primitive
type UserId = string    // bare primitive - compiler cannot distinguish
type OrderId = string   // UserId and OrderId are the same type
```

Typical fix:
```text
// Fix: distinct value type wrapping the primitive
type UserId wraps string    // distinct type - compiler catches misuse
type OrderId wraps string   // UserId and OrderId are different types
```

---

**TIP-004 - Dead indirection**

Pass-through layer adding no behavior. Remove. Not reduce.

Typical violation:
```text
// Violation: wrapper that adds no behavior - pure forwarding
function handleRequest(data): Response {
    return inner.handleRequest(data)  // zero transformation
}

// The language mechanism varies (struct embedding, class extension, interface delegation).
// The pattern is the same: a layer whose sole purpose is to forward to another.
```

---

**TIP-006 - Control flow in business code**

Execution mechanics (retries, locks, logging severity, error branching) belong in policies. NOT in business methods.

Typical violations:
- Runtime branch on environment flags for severity policy (`if dev_mode: ... else: ...` deciding between `logger.warning` and `logger.error`)
- Nested `for/try/except/if` more than 3 levels deep in single method
- Manual retry loops inside business logic when retry policy available
- Inline environment-flag branching for any execution concern (timeout, retry, fallback, severity)

---

**TIP-007 - Untyped data crossing boundaries**

Data structure passing across actor boundary must have defined type. Generic maps defeat static analysis. Force consumer to read producer's code to understand data.

Typical violation:
```text
// Violation: untyped dictionary crossing a boundary
function process(data: Dict): Result
// consumer must read the entire function body to understand the data shape
```

Fix: typed object with named fields. ADTOs without `record_mutation` / history = also violation of auditable half of contract (see Section A).

---

**TIP-008 - Direct calls between actors**

Actor's method invocations target only own dependencies. Invoking another actor's method = structural violation. Language irrelevant.

Typical violations:
- `MicroActor.run()` method calling `NanoActor.do_thing()` directly
- `pico_actor_main()` function calling `micro_actor.run()` directly
- "orchestrator" / "coordinator" / "controller" class driving workflow through method calls

In all cases, fix same: caller emits command event and exits. Callee subscribes to that event and reacts. See Event Choreography structural rule above.

## Usage

Each template and command in this preset references AIOA.md as single source of truth for all TIP definitions.
