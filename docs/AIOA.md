# AIOA — AI-Oriented Architecture

AIOA is an architectural discipline for codebases that are read, reviewed, modified, tested, and verified by AI coding agents.

AIOA does not replace existing architectural styles. It constrains their implementation so an AI agent can make safe changes with minimal context traversal and without losing domain meaning.

This document is the canonical AIOA contract for specifications, plans, implementation tasks, reviews, and generated code.


## 1. Core Objective

### 1.1 Crystallization Radius

**Crystallization Radius** is the amount of system context an AI agent must inspect before it can safely understand, modify, test, or verify a component.

AIOA optimizes every design decision for a smaller Crystallization Radius while preserving domain meaning.

A design increases Crystallization Radius when it forces the agent to traverse:

- broad repository searches;
- unrelated modules or bounded contexts;
- deep dependency chains;
- pass-through abstraction layers;
- hidden runtime behavior;
- global utilities or shared helper modules;

A design reduces Crystallization Radius when it enables:

- local reasoning;
- isolated modification;
- explicit contracts;
- predictable dependency traversal;
- observable state transitions;
- lower token and context-window usage.

Every architectural decision MUST answer:

> What additional context must an AI agent consume before making a safe change?

If the answer expands the radius without protecting domain meaning, a real boundary, or an unavoidable integration constraint, the decision violates AIOA.

### 1.2 Semantic Integrity

**Semantic Integrity** means that domain concepts remain explicit, distinct, and protected in names, types, contracts, boundaries, and state transitions.

AIOA has two inseparable constraints:

1. Minimize Crystallization Radius.
2. Preserve Semantic Integrity.

Reducing traversal while collapsing domain concepts creates **Semantic Collision**.

Preserving semantics while scattering behavior creates context explosion.

A design is AIOA-aligned only when both constraints are satisfied.

### 1.3 Omission Principle

AIOA treats every written symbol as a future reasoning cost.

If it can be omitted — it must be omitted.

If it can be not passed — don't pass it.

If you can not write it — don't write it.

Omission is not minimalism for style. It is an operational constraint for AI coding agents.

Every extra parameter, layer, interface, wrapper, provider, factory, re-export, nullable override, injected collaborator, global registration, or configuration hop expands the Crystallization Radius unless it preserves necessary domain meaning or protects a real boundary.

The default architectural action is deletion, not abstraction.

Code must earn its presence by carrying business meaning, enforcing a boundary, preserving semantic integrity, proving state transition, or reducing total traversal.

A construct that exists only because a pattern expects it is crystallization noise.


## 2. Conformance Model

AIOA conformance is evidence-based.

A system is not AIOA-conformant because it uses names such as `Actor`, `Gateway`, `Policy`, `Handler`, `Service`, `DTO`, or `Event`.

A system is AIOA-conformant only when the implementation proves:

- explicit ownership boundaries;
- typed or schema-validated contracts;
- semantic domain types for domain-significant values;
- deterministic local behavior;
- observable state transitions;
- cross-actor communication through events;

### 2.1 Intent vs Implementation

Reviews MUST score two layers separately:

1. **Architecture Intent** — whether the selected architecture minimizes Crystallization Radius while preserving Semantic Integrity.
2. **Implementation Conformance** — whether the produced artifacts actually follow that architecture.

A solution MAY have correct intent and incomplete implementation conformance. The review MUST state this explicitly.

### 2.2 Crystallization Radius Budget

Every feature MUST declare a Crystallization Radius budget before implementation.

The budget MUST identify:

- the owning business boundary;
- files, modules, packages, services, or bounded contexts the agent is expected to inspect;
- allowed dependency directions;
- boundaries ordinary changes MUST NOT cross;
- tests in the project's defined test location that prove the behavior;
- external context intentionally excluded from ordinary reasoning.

If implementation requires reading outside the budget, the implementation MUST explain why.

A wider radius is allowed only when it preserves domain meaning, protects a real boundary, or reflects an unavoidable integration constraint.

## 3. Architectural Scope

AIOA is orthogonal to deployment topology.

It applies to:

- modular monoliths;
- layered monoliths;
- microservice systems;
- distributed systems;
- event-driven platforms;
- hybrid enterprise systems.

Deployment shape does not prove AIOA conformance.

A well-structured modular application can have a smaller Crystallization Radius than a poorly structured microservice ecosystem.

AIOA evaluates how software is understood and safely modified, not where it is deployed.

## 4. AIOA Design Rules

### Rule 1 — Measure Outcomes, Not AI Usage (TIP-001)

AI usage is not a productivity KPI.

Teams MUST NOT measure prompt count, token count, AI session count, or time spent in AI tools as success metrics.

Teams SHOULD measure:

- customer impact;
- delivery throughput;
- defect rate;
- maintainability;
- decision quality;
- verification speed;
- reduction in required context traversal.

Token efficiency is an architectural property, not a vanity metric.

### Rule 2 — Protect Domain Concepts with Semantic Types (TIP-002)

Any domain-significant value MUST use a semantic type instead of a raw primitive.

This includes:

- user IDs;
- order IDs;
- account IDs;
- payment IDs;
- strategy names;
- instrument symbols;
- workflow IDs;
- business timestamps;
- any value whose meaning changes system behavior.

A semantic type MUST:

1. be distinct from its underlying primitive;
2. encode the business meaning in its type name;
3. validate construction when invalid values are possible.

Example:

```text
type UserId wraps string
type PaymentId wraps string

function getUser(id: UserId): User
function getPayment(id: PaymentId): Payment
```

Violation:

```text
function getUser(id: string): User
function getPayment(id: string): Payment

getUser(paymentId)
```

Syntactic correctness does not protect semantic correctness.

### Rule 3 — Preserve Repository Locality (TIP-003)

Code MUST be organized so ordinary changes are discoverable through narrow, explicit structural paths.

Prefer boundary-oriented structure:

```text
payment/
  contracts/
  actors/
  policies/
  gateways/

billing/
  contracts/
  actors/
  policies/
  gateways/
```

A change in one business boundary SHOULD NOT require reading unrelated boundaries unless the change explicitly crosses them.

The repository MUST avoid:

- global utility dumping grounds;
- mixed-purpose `services` modules;
- cross-domain helper modules;
- wildcard imports;
- files imported by most of the repository;

Shared code is allowed only when it is cohesive, explicitly owned, and does not erase domain meaning.

### Rule 4 — Remove Crystallization Noise (TIP-004)

An abstraction is valid only when it owns meaning.

A layer, class, function, file, adapter, wrapper, or re-export MUST provide at least one of:

- invariant enforcement;
- boundary validation;
- contract preservation, including ADTO continuity when Rule 8 applies;
- policy decision;
- lifecycle state;
- side-effect isolation;
- dependency inversion for a real boundary;
- integration contract enforcement;
- observability of a meaningful state transition;
- a documented public API boundary while the inner implementation remains internal.

A pass-through abstraction that forwards work without owning meaning MUST be removed.

Violation:

```text
PaymentController
  -> PaymentRouter
  -> PaymentHandler
  -> PaymentService
  -> PaymentRepository
  -> Gateway
```

Valid layers are justified by responsibility, not by architectural vocabulary.
A class, file, or layer named `Actor`, `Service`, `Handler`, `Gateway`, `Policy`, or `Manager` still violates AIOA when it only forwards work.


### Rule 5 — Use Actor Granularity Deliberately (TIP-005)

AIOA uses three actor levels as reasoning boundaries.

#### Micro Actor

A **Micro Actor** owns a primary business boundary or bounded context.

Examples:

- Billing;
- Inventory;
- Ordering;
- Customer Management.

A task SHOULD start at the owning Micro Actor.

#### Nano Actor

A **Nano Actor** owns a reusable business workflow inside or across Micro Actors.

Examples:

- ApplyDiscount;
- ValidatePromotion;
- CalculateTax;
- DetermineShippingMethod.

#### Pico Actor

A **Pico Actor** owns a business deterministic execution primitive.

Examples:

- FindCustomerById;
- FormatInvoiceNumber;
- PublishTelemetryEvent;
- SerializeContract.

#### Extraction Rule

Implementation MUST start in the owning Micro Actor.

Extract downward only when there is real reuse or isolation pressure:

1. reusable business workflow → Nano Actor;
2. reusable business deterministic primitive → Pico Actor.

Premature extraction violates AIOA when it increases traversal without adding meaning.

### Rule 6 — Keep Business Logic Declarative and Straight-Line (TIP-006)

Business code SHOULD describe business intent in a linear path.

Recurring execution mechanics MUST be moved into explicit policies, boundaries, libraries, or prepared primitives.

Good candidates:

- validation pipelines;
- retry policies;
- timeout policies;
- transaction boundaries;
- resource scopes;
- concurrency limits;
- result types;
- collection pipelines;
- event dispatch and handler binding.

Preferred:

```text
retryPolicy = RetryPolicy(maxAttempts=3, backoff="exponential")

function chargeCustomer(amount):
    return retryPolicy.execute(() => gateway.charge(amount))
```

Violation:

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

Guard clauses for visible business preconditions are allowed. Manual procedural machinery scattered through business methods is not.

### Rule 7 — Kill Loose Input at the Boundary (TIP-007)

Loose external input MUST NOT enter business logic.

A Strict Gateway MUST:

1. accept loose input;
2. validate shape, required fields, primitive types, enum membership, nullability, ID format, normalization, range checks, and schema version;
3. reject malformed payloads immediately;
4. convert valid input into typed DTO or ADTO contracts;
5. pass only trusted DTOs or ADTOs to business logic.

Example:

```text
gateway PromoRequestGateway:
    accepts json
    validates PromoRequestSchema
    returns PromoRequest
```

After the gateway, remaining checks MUST be business checks, such as:

- entity existence;
- eligibility;
- authorization;
- discount compatibility;
- workflow transition validity.

Violation:

```text
function process(data: dict): Result
```

If validated input becomes an ADTO, Rule 8 governs the rest of the execution chain.


### Rule 8 — Use Auditable DTOs When State Provenance Matters (TIP-007)

A DTO that carries important mutable runtime state MUST be an Auditable DTO.

An ADTO MUST provide:

- a deterministic typed contract;
- immutable snapshots or controlled transition methods;
- mutation recording for meaningful business transitions;
- ordered mutation history retrieval;
- optional provenance such as caller, reason, timestamp, trace ID, or source component.

ADTOs MUST record meaningful business transitions, not every setter call.

Good mutation slice:

```text
operation: ApplyPaymentFailurePolicy
reason: Failed payment threshold exceeded
changes:
  status: Active -> Suspended
  riskScore: 20 -> 95
```

The purpose is explainability. Compliance noise violates AIOA when it obscures meaningful state change.

#### ADTO Continuity Rule

A consumer that receives an ADTO MUST continue the chain with an ADTO.

If the consumer needs additional context, that context MUST be added at a boundary by creating a more specific ADTO, preferably through inheritance or an equivalent language-native extension mechanism.

Do not unpack an ADTO into primitive parameter chains.

Do not convert an ADTO into loose dictionaries, raw JSON, generic maps, or unrelated DTOs mid-chain.

Do not load configuration, runtime context, or external state mid-chain to compensate for missing ADTO context.

The ADTO is the execution context. Preserve it until the workflow reaches a real boundary, terminal state, or event emission.

Use plain DTOs instead of ADTOs only when thousands of instances are created and audit tracking creates a proven performance cost. In all other cases, important mutable runtime state MUST use ADTO.


### Rule 9 — Communicate Across Actors Through Events (TIP-008)

Micro Actors, Nano Actors, and Pico Actors MUST NOT call each other's internal methods directly.

All cross-actor communication MUST go through the selected event mechanism.

Events MUST be:

- explicit contracts;
- immutable;
- typed or schema-validated;
- business-oriented;
- implementation-independent;
- versioned when crossing durable or external boundaries.

Examples:

```text
PaymentRequested
PaymentCompleted
InventoryReserved
OrderCancelled
```

Violation:

```text
class OrderService:
    function placeOrder(cart):
        billingService.applyCharge(amount)
        notificationService.sendEmail(user)
```

Required shape:

```text
class OrderActor:
    function placeOrder(cart):
        return OrderPlaced(orderId, customerId, total)

class BillingActor:
    @handler(OrderPlaced, PaymentRequested)
    function requestPayment(event: OrderPlaced): PaymentRequested:
        return PaymentRequested(event.orderId, event.total)

class NotificationActor:
    @handler(OrderPlaced, EmailRequested)
    function requestEmail(event: OrderPlaced): EmailRequested:
        return EmailRequested(event.customerId, "order placed")
```

Returned events SHOULD be auto-published when the selected event mechanism supports it. Otherwise, explicit dispatch MUST be visible in code and covered by tests. Lists of returned events SHOULD be published item by item when supported by the selected mechanism.

### Rule 10 — Use One Event Mechanism per Boundary (TIP-008)

Each boundary MUST use one selected event mechanism.

For a single-process system, the default mechanism SHOULD be an in-process event bus or dispatcher.

If the project already uses Kafka, RabbitMQ, an actor runtime, a framework-native domain-event dispatcher, a command bus, a message dispatcher, or another broker, the project SHOULD use that mechanism directly.

The project MUST NOT add a second bus wrapper only to satisfy AIOA vocabulary.

The selected mechanism MUST prove:

- producers do not call consumer internals;
- consumers are bound through handlers, subscribers, receivers, or equivalent local dispatch points;
- contracts are explicit and typed or schema-validated;
- derived events or state transitions are observable;
- failure behavior is defined;
- tests prove the event chain.

A dependency-injected interface call is not an event mechanism unless it dispatches explicit contracts between independently owned actors.

### Rule 11 — Keep Synchronous Calls Inside the Local Ownership Boundary (TIP-008)

The event-only rule applies only to actor-to-actor communication.

An actor MAY synchronously call a dependency only when that dependency is owned by the same local boundary and does not own independent business behavior.

A dependency is locally owned only when:

1. it is colocated with the actor or declared in the actor's local boundary;
2. it serves the actor's responsibility directly;
3. understanding ordinary behavior does not require global container wiring, runtime profile lookup, or unrelated boundary traversal;
4. it does not make business decisions for another actor;
5. it does not hide cross-boundary workflow behavior.

Examples of local dependencies include actor-owned repositories, gateways, policies, validators, mappers, transaction boundaries, retry policies, and telemetry clients.

The category name does not make a dependency local. Ownership does.

If a dependency owns independent business behavior, cross-boundary state, or another actor's policy, it is an actor and MUST be reached through an event.

Synchronous execution is allowed inside the local ownership boundary.

Direct actor coupling is not.

#### Preferred

```text
class OrderActor:
    function processOrder(order):
        OrderValidator().validate(order)
        OrderPolicy().apply(order)
        OrderRepository().save(order)
```

#### Violation

```text
class OrderActor:
    function processOrder(order):
        CustomerPolicy().checkCustomerStatus(order.customerId)
        BillingRepository().reserveCredit(order.customerId, order.total)
        NotificationGateway().sendOrderEmail(order.customerId)
```

### Rule 12 — Define Event Failure Semantics Explicitly (TIP-008)

The event mechanism MUST define failure behavior.

Allowed strategies include:

- log and continue;
- retry;
- dead-letter;
- fail the command;
- compensate.

The selected strategy MUST match business semantics.

Implicit event failure behavior violates AIOA.


### Rule 13 — Omit What Does Not Carry Meaning (TIP-009)

AIOA uses omission as an architectural rule.

If it can be omitted — it must be omitted.

If it can be not passed — don't pass it.

If you can not write it — don't write it.

An agent MUST treat every additional symbol, parameter, object, layer, interface, factory, provider, wrapper, configuration key, dependency, and file as Crystallization Radius expansion until proven otherwise.

A component MUST NOT receive what it can own locally.

A method MUST NOT accept what its owner already knows.

A workflow MUST NOT pass what can be derived from the active DTO, ADTO, event, actor state, or local boundary.

An interface MUST NOT be introduced when there is no real boundary, independent implementation, or semantic contract to protect.

A factory, provider, builder, or dependency-injection mechanism MUST NOT be introduced when direct local construction is sufficient.

A wrapper MUST NOT be introduced when it only forwards.

A parameter MUST NOT exist only for speculative reuse, testing convenience, pattern conformity, or future flexibility.

The only valid reasons to add structure are:

1. preserve domain meaning;
2. enforce a real boundary;
3. protect a contract;
4. make state transition observable;
5. isolate external infrastructure;
6. reduce total Crystallization Radius.

If none apply, omit it.


## 5. Required Proof Artifacts

These proof artifacts MUST be applied to every class, function, module, actor, gateway, policy, DTO, ADTO, event, handler, adapter, and test touched by the current change inside the active codebase; partial application to only the entry point or generated files is not AIOA-conformant.

Every AIOA-aligned spec, plan, task, review, or implementation MUST provide the following proof artifacts:

| Artifact | Required evidence |
| --- | --- |
| [Rule 1] Outcome metrics | Customer impact, delivery throughput, defect rate, maintainability measured — not AI usage counts. |
| [Rule 2] Contracts | DTOs, events, schemas, gateways, and versions when needed. |
| [Rule 2] Semantic types | Domain-significant identifiers and values are not raw primitives. |
| [Core] Radius budget | Files, modules, boundaries, dependencies, exclusions. |
| [Rule 4] Abstraction justification | Each layer, class, or function owns meaning — no pass-through wrappers. |
| [Rule 5] Boundary ownership | Which Micro Actor owns the behavior. |
| [Rule 6] Declarative proof | Business logic is straight-line intent — retry, timeout, transaction mechanics are in policies or boundaries. |
| [Rule 7] Input perimeter | Where loose input is validated and converted. |
| [Rule 8] State observability | Events, ADTO mutation history, or focused telemetry. |
| [Rule 9] Cross-actor communication | Event contracts and handlers, with no direct actor method calls. |
| [Rule 10] Event mechanism selection | One real event mechanism per boundary — producers do not call consumer internals. |
| [Rule 11] Local dependency scope | Synchronous calls are limited to dependencies owned by the same local boundary; dependency category alone is not proof of locality. |
| [Rule 12] Failure behavior | Retry, dead-letter, fail, compensate, or continue strategy. |
| [Rule 13] Omission proof | Every added parameter, object, layer, interface, factory, provider, wrapper, dependency, configuration key, and file is justified by domain meaning, boundary protection, contract preservation, observable state transition, external infrastructure isolation, or reduced total traversal. |

Without these artifacts, the work is AIOA-inspired at most. It is not AIOA-conformant.

## 6. Review Checklist

| Rule | Review question | Common violation |
| --- | --- | --- |
| [Core] Core | Is Crystallization Radius minimized without losing domain meaning? | Small code change requires broad repository traversal. |
| [Rule 1] Outcomes | Are outcomes measured instead of AI usage counts? | Prompt count, token count, or AI session count used as success metrics. |
| [Core] Budget | Is the radius budget explicit and respected? | Implementation reads outside the budget without explanation. |
| [Rule 2] Semantics | Are domain concepts represented by semantic types? | IDs, names, timestamps, symbols, or workflow keys passed as raw strings. |
| [Rule 3] Locality | Can relevant behavior be found through the owning boundary? | Global `utils`, mixed `services`, shared helper dumping grounds. |
| [Rule 4] Abstraction | Does each abstraction own meaning? | Pass-through wrappers, forwarding chains, pattern-shaped files. |
| [Rule 5] Actors | Are Micro, Nano, and Pico responsibilities distinguishable? | Everything named `Service`, `Manager`, or `Helper`. |
| [Rule 5] Extraction | Was behavior extracted only after real reuse or isolation pressure? | Premature Nano/Pico actors increase traversal. |
| [Rule 6] Declarative flow | Is business logic intent-focused and straight-line? | Manual retry, lock, timeout, transaction, or callback mechanics in business methods. |
| [Rule 7] Gateway | Does loose input die at the perimeter? | Raw JSON, `dict`, nullable blobs, or loose payloads in business logic. |
| [Rule 8] ADTO | Is important mutable state explainable? | DTOs mutate without ordered transition history. |
| [Rule 9] Events | Do actors communicate only through events? | Actor calls another actor's method directly or through an interface. |
| [Rule 10] Event mechanism | Is there one real event mechanism per boundary? | Second bus wrapper over an existing broker with no added meaning. |
| [Rule 11] Local dependencies | Are synchronous calls limited to locally owned dependencies? | A repository/gateway object hides independent business behavior. |
| [Rule 12] Failure semantics | Is event failure behavior explicit? | Handler failures are implicit or framework-defaulted without business decision. |
| [Rule 13] Omission | Does every added symbol, parameter, object, layer, interface, factory, provider, wrapper, dependency, configuration key, and file carry meaning or reduce total traversal? | Pattern scaffolding, speculative flexibility, redundant parameters, unnecessary interfaces, provider/factory noise, optional overrides, or dependency passing where local ownership is sufficient. |
| [Rule 8] ADTO chain | Does ADTO survive the full execution path? | ADTO unpacked to primitives for internal component. |
| [General] Conformance | Are claims backed by proof artifacts? | Naming folders after AIOA concepts without evidence. |

## 7. Agent Operating Contract

When acting as an AI coding agent under AIOA, the agent MUST:

1. **[Rule 1]** measure outcomes — customer impact, throughput, defect rate — not AI usage counts;
2. **[Rule 2]** preserve semantic types and domain vocabulary;
3. **[Rule 2]** use semantic types for all domain-significant values instead of raw primitives;
4. **[Core]** declare or verify the Crystallization Radius budget;
5. **[Core]** inspect only the files inside the budget unless expansion is justified;
6. **[Core]** report any required radius expansion explicitly;
7. **[Rule 4]** avoid pass-through abstractions — each layer must own meaning;
8. **[Rule 5]** identify the owning Micro Actor before planning changes;
9. **[Rule 6]** keep business logic declarative and straight-line;
10. **[Rule 7]** reject loose input at gateways — validate, convert, pass only typed DTOs;
11. **[Rule 8]** use Auditable DTOs when mutable state requires provenance;
12. **[Rule 9]** use events for cross-actor communication — no direct method calls between actors;
13. **[Rule 10]** use one real event mechanism per boundary;
14. **[Rule 11]** allow synchronous calls only to locally owned dependencies;
15. **[Rule 12]** define failure behavior for event chains;
16. **[Rule 13]** omit everything that does not carry meaning — do not add parameters, wrappers, interfaces, factories, providers, dependencies, config hops, or files unless they preserve semantics, protect a boundary, prove state, isolate external infrastructure, or reduce total traversal;

The agent MUST NOT claim AIOA conformance from naming alone.

The agent MUST treat AIOA as a constraint system: smaller context, stronger semantics, explicit boundaries, observable state, and local proof.

## 8. Usage

Templates, commands, skills, and generated tasks MUST treat this file as the canonical AIOA definition.

Use the project's existing language, framework, and runtime capabilities, but do not weaken AIOA constraints.
