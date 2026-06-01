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

### TIP-005: Quantum Spectrum
Components at different abstraction levels are indistinguishable by name — everything is called "service" despite different complexity.
**Pattern:** Pico Actor — deterministic pure function, Nano Actor — component with state, Micro Actor — independent service. Different levels, different names.
```text
// Pattern: named by level
pico actor FormatPostalCode(input: string): string
nano actor ApplyDiscount(order, customer): Order
micro actor BillingService: manages invoices, payments
```
**Anti-Pattern:** Everything called "Service" regardless of whether it is a pure function or a distributed microservice.
```text
// Anti-Pattern: everything is "Service"
class FormatService        // actually: formatPostalCode(a, b): string
class DiscountService      // actually: applyDiscount(order): Order
class BillingService       // actually: microservice with DB, queue, API
// AI cannot distinguish simple functions from complex subsystems
```

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
**Pattern:** Every boundary-crossing object extends ADTO base class. ADTO uses __init_subclass__ to auto-register all typed fields — no manual setters. Every property change is captured with caller context, merged into a single TraceEntry when multiple changes come from the same caller, and stored as deep-cloned snapshots. Tracing is config-gated via ADTO_TRACE_ENABLED.
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

// Nano actor (stateful component) subscribes and publishes
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



## Usage

Each template and command in this preset references AIOA.md as the single source of truth for all TIP definitions.
