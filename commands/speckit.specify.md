---
description: "Enhanced specify command with AIOA principle impact analysis"
scripts:
  - specify spec
---

# speckit.specify — AIOA-Enhanced Specification Command

**Preset:** aioa (version 1.0.0)

---

## Workflow

### Step 1: Gather Specification Details

> **What feature or behavior change are you specifying?**

Capture:
- Feature name and summary
- Problem being solved
- Proposed solution outline
- Scope boundaries

### Step 2: Apply All 10 AIOA Principle Assessments

For each principle, prompt the user and record the assessment.

#### P1: Local Reasoning
> Can this feature be understood from local context alone?
1. How many files must an agent read?
2. Is cross-module understanding required?
3. Are there global state or ambient conventions involved?
**Record:** Local Reasoning verdict (Self-contained / Some external / Extensive external)

#### P2: Crystallization Radius
> How much context must an agent consume to implement this safely?
1. Which existing files/modules will this affect?
2. What cross-module dependencies exist?
3. Are there implicit conventions or global state?
**Compute Radius:** Low (🟢 1-3 files) / Medium (🟡 4-8 files) / High (🔴 9+ files)
- **If High:** Flag for architecture review before proceeding.

#### P3: Semantic Integrity
> What meaning must be preserved across architectural boundaries?
1. What data types cross between components?
2. Are there existing shared type definitions to use?
3. What transformations happen at the boundary?
4. How do we verify meaning is preserved?
**Record:** Boundaries crossed, data/behavior per boundary, integrity requirements, shared contracts
**TIP-007:** Validate at boundaries with strict JSON schemas.

#### P4: Boundaries Explicit
> What component boundaries does this specification cross?
1. What components are involved?
2. Are their boundaries already declared?
3. Does this create new boundaries?
4. Do components access through declared interfaces or internal details?
**Record:** Boundary map with names, responsibilities, and interfaces.

#### P5: Contracts Deterministic
> Are all interfaces machine-verifiable?
1. What interfaces exist between components?
2. Does each have a schema (Zod, OpenAPI, JSON Schema)?
3. How is schema validation enforced at boundaries?
4. Are contracts versioned?
**Record:** Interface list with schema types and verification methods.
**TIP-007:** Use strict JSON schemas for deterministic contract enforcement.

#### P6: Declarative Straight-Line
> Is the proposed design linear and declarative?
1. Does the design have deeply nested conditional logic?
2. Can complex control flow be replaced with declarative operations?
3. Is mutable state localized and minimized?
4. Is control flow depth acceptable for AI agent reasoning?
**Record:** Control-flow complexity assessment.

#### P7: Reasoning Boundaries not Deployment
> Does this specification assume a specific deployment topology?
1. Does this feature require specific infrastructure?
2. Could it work in both monolith and microservices?
3. Are infrastructure concerns separated from business logic?
4. Are boundaries reasoning or deployment boundaries?
**If topology assumptions found:** Extract to deployment boundary section; keep core spec topology-agnostic.

#### P8: Extract Under Reuse Pressure
> Are any abstractions in this specification premature?
1. Does this propose new abstractions or shared utilities?
2. How many consumers will use each abstraction?
3. Is there concrete evidence of reuse, or is this speculative?
**Rule:** Flag abstractions with fewer than 2 confirmed consumers.

#### P9: Event Boundaries
> How does cross-component communication happen?
1. Do components communicate via event bus or direct calls?
2. Can cross-component communication be event-driven?
3. Are event schemas versioned and shared?
4. Are direct synchronous calls justified?
**Record:** Communication patterns and rationale.
**TIP-008:** Prefer event-driven integration over direct calls.

#### P10: Runtime State Explainable
> Can runtime state be explained and audited?
1. What runtime state does this feature maintain?
2. Is state mutation logged with provenance?
3. Can state be inspected without side effects?
4. Do DTOs follow the ADTO pattern with `_provenance` fields?
**Record:** State inventory with provenance tracking plan.
**TIP-009:** Use Auditable DTOs (ADTO) with provenance tracking.

### TIP-005: Quantum Spectrum Classification

Classify each component by Quantum Spectrum level:

| Level | Description | Example |
|-------|-------------|---------|
| **Micro Actor** | Primary business boundary | Billing, Inventory, Ordering |
| **Nano Actor** | Reusable business workflow | ApplyDiscount, ValidatePromotion |
| **Pico Actor** | Deterministic execution primitive | FindCustomerById, FormatInvoiceNumber |

**Rule:** Start large (Micro Actor). Extract downward only when reuse pressure appears.

### TIP-003: Dead Code Cleanliness

Before approving, verify no declared exports remain unused:
1. Check for components/functions declared and exported but never imported or consumed
2. Flag unused exports as dead code — remove or justify
3. Track dead export locations for cleanup

| Dead Export | Found? | Location |
|-------------|--------|---------|
| {{dead_export_1}} | 🟢 None / 🔴 Found | {{dead_export_location_1}} |
| {{dead_export_2}} | 🟢 None / 🔴 Found | {{dead_export_location_2}} |

### TIP-004: Code Crystallization — Indirection Audit

Before approving, verify no dead abstraction layers:

1. **Pass-through audit:** Count layers between interface and implementation
2. **Single-impl base classes:** Flag any base class with only one concrete implementation
3. **Zero-consumer components:** Flag any exported component with no importers

| Indirection Layer | Interface | Consumers | Implementations | Verdict |
|-------------------|-----------|-----------|-----------------|---------|
| {{layer_1}} | {{interface_1}} | {{consumers_1}} | {{impls_1}} | 🟢 Justified / 🔴 Dead |
| {{layer_2}} | {{interface_2}} | {{consumers_2}} | {{impls_2}} | 🟢 Justified / 🔴 Dead |

- [ ] All base classes have ≥2 implementations
- [ ] All exported components have ≥1 consumer
- [ ] No pass-through layers (A→B→C with B just forwarding)

### TIP-002: Semantic Collision Check

Before approving, verify domain semantics are preserved:
1. **Primitive types:** Are `str`/`int`/`dict` used where value objects should be?
2. **Naming collision:** Could similar names (`call_id` vs `trace_id`) be confused by an AI agent?
3. **Untyped structures:** Are there `dict` or `list[dict]` without schema definitions?
4. **Bounded contexts:** Is the same concept defined in multiple places?

| Domain Concept | Current Type | Should Be | Collision Risk |
|----------------|-------------|-----------|----------------|
| {{concept_1}} | {{type_1}} | {{value_object_1}} | 🟢 Safe / 🔴 Risk |
| {{concept_2}} | {{type_2}} | {{value_object_2}} | 🟢 Safe / 🔴 Risk |

### Step 3: Generate AIOA-Compliant Specification

Write the specification using the AIOA spec template with all section populated.
**Include:** All 10 principle assessments (P1-P10), context budget per agent role.

### Step 4: Validate Before Finalizing

- [ ] P1: Local Reasoning documented
- [ ] P2: Crystallization Radius documented and categorized
- [ ] P3: All boundaries have Semantic Integrity requirements defined
- [ ] P4: All boundaries explicitly declared with interfaces
- [ ] P5: All interfaces have machine-verifiable schemas
- [ ] P6: Control-Flow complexity assessed
- [ ] P7: No deployment topology assumptions in core spec
- [ ] P8: No premature abstractions
- [ ] P9: Cross-component communication patterns documented
- [ ] P10: Runtime state explainability plan exists
- [ ] Context budget estimated
- [ ] Shared semantic contracts identified
- [ ] TIPs referenced where appropriate
- [ ] TIP-002: No primitive types in domain-critical flows
- [ ] TIP-002: No naming collision risks
- [ ] TIP-002: No untyped structures (`dict`, `list[dict]`)

---

## Prompt Templates

### P1 — Local Reasoning
```
For [FEATURE_NAME], assess Local Reasoning:
How many files must an agent read?
Is cross-module knowledge required?
Are there global state or ambient conventions?
Local Reasoning: [SELF-CONTAINED / SOME EXTERNAL / EXTENSIVE EXTERNAL]
```

### P2 — Crystallization Radius
```
For [FEATURE_NAME]:
Files directly affected: [LIST]
Files requiring context: [LIST]
Cross-module dependencies: [LIST]
Crystallization Radius: [LOW / MEDIUM / HIGH]
```

### P3 — Semantic Integrity
```
For each boundary [BOUNDARY_LIST]:
1. What data/behavior crosses this boundary?
2. Is meaning preserved in both directions?
3. What shared contract governs the boundary?
4. How is integrity enforced (types, tests, validation)?
TIP-007: Use strict JSON schemas at boundaries.
```

### P4 — Boundaries Explicit
```
Map boundaries for [FEATURE_NAME]:
For each component: name, responsibility, boundary interface, declared explicitly, access through interfaces only.
```

### P5 — Contracts Deterministic
```
For each interface in [FEATURE_NAME]:
1. Does it have a machine-readable schema?
2. Is schema validation enforced at runtime?
3. What contract version is used?
4. Are consumer-driven contracts defined?
```

### P6 — Control-Flow Simplicity
```
Assess control flow for [FEATURE_NAME]:
1. Maximum nesting depth?
2. Can loops be replaced with declarative operations?
3. Is mutable state localized?
4. Is async using async/await?
```

### P7 — Reasoning Boundaries not Deployment
```
Check each component for deployment topology assumptions:
- References to HTTP, gRPC, queues, filesystems?
- Would it need changes for monolith vs microservices?
- Can infrastructure deps be replaced with interfaces?
- Are boundaries reasoning or deployment boundaries?
```

### P8 — Extract Under Reuse Pressure
```
Check proposed abstractions for [FEATURE_NAME]:
For each: how many consumers? Evidence of reuse? Could be inlined?
Flag if fewer than 2 confirmed consumers.
```

### P9 — Event Boundaries
```
Assess cross-component communication for [FEATURE_NAME]:
1. What communication paths exist?
2. Can they use event bus instead of direct calls?
3. Are event schemas versioned?
4. Are direct calls justified exceptions?
TIP-008: Prefer event-driven integration.
```

### P10 — Runtime State Explainability
```
Assess runtime state explainability for [FEATURE_NAME]:
1. What state does each component maintain?
2. Is state mutation logged with provenance?
3. Can state be inspected without side effects?
4. Do DTOs follow ADTO pattern with _provenance?
TIP-009: Use Auditable DTOs with provenance tracking.
```

---

## Output

**File:** `specs/{{spec_id}}.aioa.md`

The specification includes all standard fields plus all 10 AIOA principle metadata fields (`p1_local_reasoning:` through `p10_runtime_state_explainable:`) and `context_budget:` per-role context estimation.
