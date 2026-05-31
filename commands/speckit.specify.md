---
description: "Enhanced specify command with AIOA principle impact analysis"
scripts:
  - specify spec
---

# speckit.specify — AIOA-Enhanced Specification Command

**Preset:** aioa (version 1.0.0)

This command overrides the standard `specify spec` flow to guide the agent through AIOA-compliant specification covering all 10 AIOA principles.

---

## Overview

When invoked, this command:
1. Guides users through specification with full AIOA principle impact analysis
2. Prompts for all 10 AIOA principle assessments
3. Generates an AIOA-compliant specification with all assessments populated

---

## Workflow

### Step 1: Gather Specification Details

Ask the user (or extract from context):

> **What feature or behavior change are you specifying?**

Capture:
- Feature name and summary
- Problem being solved
- Proposed solution outline
- Scope boundaries

### Step 2: Apply All 10 AIOA Principle Assessments

For each principle, prompt the user and record the assessment.

#### Principle P1: Local Reasoning

> **Can this feature be understood from local context alone?**

**Prompt the user:**
1. "How many files must an agent read to understand this feature?"
2. "Is any cross-module understanding required beyond the immediate files?"
3. "Are there global state or ambient conventions involved?"

**Record:** Local Reasoning verdict (Self-contained / Some external context / Extensive external context)

#### Principle P2: Crystallization Radius

> **How much additional context must an AI agent consume to implement this safely?**

**Prompt the user:**
1. "Which existing files/modules will this specification affect?"
2. "What cross-module dependencies exist?"
3. "Are there any implicit conventions or global state involved?"

**Compute Crystallization Radius:**
- **Low (🟢):** 1–3 files, no cross-module context needed
- **Medium (🟡):** 4–8 files, some cross-module dependencies
- **High (🔴):** 9+ files, extensive cross-module context

**If High:** Flag for architecture review before proceeding.

#### Principle P3: Semantic Integrity

> **What meaning must be preserved across architectural boundaries?**

**Prompt the user:**
1. "What data types cross between components?"
2. "Are there existing shared type definitions that should be used?"
3. "What transformations happen at the boundary?"
4. "How do we verify meaning is preserved?"

**Record:**
- Boundaries crossed
- Data/behavior crossing each boundary
- Integrity requirements at each boundary
- Shared semantic contracts needed

**TIP-007 reference:** Validate at boundaries with strict JSON schemas.

#### Principle P4: Boundaries Explicit

> **What component boundaries does this specification cross?**

**Prompt the user:**
1. "What components are involved in this feature?"
2. "Are their boundaries already declared?"
3. "Does this specification create new boundaries?"
4. "How do components access each other — through declared interfaces or internal details?"

**Record:** Boundary map with names, responsibilities, and interfaces.

#### Principle P5: Contracts Deterministic

> **Are all interfaces machine-verifiable?**

**Prompt the user:**
1. "What interfaces exist between components?"
2. "Does each interface have a schema (Zod, OpenAPI, JSON Schema)?"
3. "How is schema validation enforced at boundaries?"
4. "Are contracts versioned?"

**Record:** Interface list with schema types and verification methods.

**TIP-007 reference:** Use strict JSON schemas for deterministic contract enforcement.

#### Principle P6: Declarative Straight-Line

> **Is the proposed design linear and declarative?**

**Prompt the user:**
1. "Does the design have deeply nested conditional logic?"
2. "Can complex control flow be replaced with declarative operations?"
3. "Is mutable state localized and minimized?"
4. "Is the control flow depth acceptable for AI agent reasoning?"

**Record:** Control-flow complexity assessment.

#### Principle P7: Reasoning Boundaries not Deployment (Architectural Independence)

> **Does this specification assume a specific deployment topology?**

**Prompt the user:**
1. "Does this feature require specific infrastructure (queues, databases, network config)?"
2. "Could this work in both a monolith and microservices deployment?"
3. "Are infrastructure concerns separated from business logic?"
4. "Are component boundaries reasoning boundaries or deployment boundaries?"

**If topology assumptions are found:**
- Extract them to a deployment boundary section
- Ensure core specification remains topology-agnostic

#### Principle P8: Extract Under Reuse Pressure

> **Are any abstractions in this specification premature?**

**Prompt the user:**
1. "Does this specification propose any new abstractions or shared utilities?"
2. "How many consumers will use each abstraction?"
3. "Is there concrete evidence of reuse, or is this speculative?"

**Rule:** Flag any abstraction with fewer than 2 confirmed consumers.

#### Principle P9: Event Boundaries

> **How does cross-component communication happen?**

**Prompt the user:**
1. "How do components communicate — through an event bus or direct calls?"
2. "Can cross-component communication be event-driven?"
3. "Are event schemas versioned and shared?"
4. "Are direct synchronous calls justified?"

**Record:** Communication patterns and rationale.

**TIP-008 reference:** Prefer event-driven integration over direct calls.

#### Principle P10: Runtime State Explainable

> **Can runtime state be explained and audited?**

**Prompt the user:**
1. "What runtime state does this feature maintain?"
2. "Is state mutation logged with provenance?"
3. "Can state be inspected without side effects?"
4. "Are DTOs following the ADTO pattern with `_provenance` fields?"

**Record:** State inventory with provenance tracking plan.

**TIP-009 reference:** Use Auditable DTOs (ADTO) with provenance tracking.

### TIP-004: Code Crystallization Analysis

Before approving the specification, assess the Architectural Crystallization Radius:

1. **Indirection layers**: How many pass-through interfaces, factory chains, or mediator layers must be traversed?
2. **Business logic density**: Is business logic directly visible or hidden behind abstractions?
3. **Modification path**: Can the feature be modified by changing 1-3 files, or does it require 9+ files?

Target: Reduce Architectural Crystallization Radius to LOW (1-3 files).

### TIP-005: Quantum Spectrum Classification

Classify each component in the specification by Quantum Spectrum level:

| Level | Description | Example |
|-------|-------------|---------|
| **Micro Actor** | Primary business boundary | Billing, Inventory, Ordering |
| **Nano Actor** | Reusable business workflow | ApplyDiscount, ValidatePromotion |
| **Pico Actor** | Deterministic execution primitive | FindCustomerById, FormatInvoiceNumber |

Rule: Start large (Micro Actor). Extract downward only when reuse pressure appears.

### Step 3: Generate AIOA-Compliant Specification

Write the specification using the AIOA spec template with all sections populated.

**Include:**
- `spec-template-aioa.md` with all 10 principle assessments filled
- P1 Local Reasoning assessment
- P2 Crystallization Radius impact assessment table
- P3 Semantic Integrity requirements per boundary
- P4 Boundaries Explicit map
- P5 Contracts Deterministic check
- P6 Control-Flow Complexity check
- P7 Reasoning Boundaries vs Deployment check
- P8 Extract Under Reuse Pressure assessment
- P9 Event Boundaries plan
- P10 Runtime State Explainability plan
- Context budget for each agent role

### Step 4: Validate Before Finalizing

Run the following checks:

- [ ] P1: Local Reasoning is documented
- [ ] P2: Crystallization Radius is documented and categorized
- [ ] P3: All boundaries have Semantic Integrity requirements defined
- [ ] P4: All boundaries are explicitly declared with interfaces
- [ ] P5: All interfaces have machine-verifiable schemas
- [ ] P6: Control-Flow complexity is assessed
- [ ] P7: No deployment topology assumptions in core spec
- [ ] P8: No premature abstractions
- [ ] P9: Cross-component communication patterns documented
- [ ] P10: Runtime state explainability plan exists
- [ ] Context budget is estimated
- [ ] Shared semantic contracts are identified
- [ ] TIPs referenced where appropriate

---

## Prompt Templates

### P1 — Local Reasoning Prompt

```
For [FEATURE_NAME], assess Local Reasoning:

How many files must an agent read to understand this feature?
Is cross-module knowledge required?
Are there global state or ambient conventions involved?

Local Reasoning: [SELF-CONTAINED / SOME EXTERNAL CONTEXT / EXTENSIVE EXTERNAL CONTEXT]
```

### P2 — Crystallization Radius Prompt

```
The Crystallization Radius of a feature is the amount of context an AI agent
must consume before making a safe change. For [FEATURE_NAME]:

Files directly affected: [LIST]
Files requiring context: [LIST]
Cross-module dependencies: [LIST]

Crystallization Radius: [LOW / MEDIUM / HIGH]

To minimize this radius, consider:
- Can any dependencies be inverted?
- Can cross-cutting concerns be extracted?
- Can the surface area be reduced by narrowing the interface?
```

### P3 — Semantic Integrity Prompt

```
For each boundary [BOUNDARY_LIST], identify:
1. What data/behavior crosses this boundary?
2. Is meaning preserved in both directions?
3. What shared contract governs the boundary?
4. How is integrity enforced (types, tests, validation)?

Semantic Integrity violations occur when:
- The same concept has different representations
- Data is silently transformed
- Validation is applied inconsistently

TIP-007: Use strict JSON schemas at boundaries.
```

### P4 — Boundaries Explicit Prompt

```
Map the boundaries for [FEATURE_NAME]:

For each component:
1. What is its name and responsibility?
2. What boundary interface does it expose?
3. Is the boundary explicitly declared?
4. Is access through declared interfaces only?
```

### P5 — Contracts Deterministic Prompt

```
For each interface in [FEATURE_NAME]:

1. Does it have a machine-readable schema?
2. Is schema validation enforced at runtime?
3. What contract version is used?
4. Are consumer-driven contracts defined?
```

### P6 — Control-Flow Simplicity Prompt

```
Assess control flow complexity for [FEATURE_NAME]:

1. What is the maximum nesting depth?
2. Can complex loops be replaced with declarative operations?
3. Is mutable state localized?
4. Is async control flow using async/await?
```

### P7 — Reasoning Boundaries not Deployment Prompt

```
Check each component involved for deployment topology assumptions:
- Does it reference HTTP, gRPC, message queues, or filesystems directly?
- Would it need changes to deploy as a monolith vs microservices?
- Can infrastructure dependencies be replaced with interfaces?
- Are boundaries reasoning boundaries or deployment boundaries?
```

### P8 — Extract Under Reuse Pressure Prompt

```
Check proposed abstractions for [FEATURE_NAME]:

For each new abstraction:
1. How many consumers exist?
2. Is there evidence of reuse pressure?
3. Could this be inlined instead?

Flag if fewer than 2 confirmed consumers.
```

### P9 — Event Boundaries Prompt

```
Assess cross-component communication for [FEATURE_NAME]:

1. What communication paths exist?
2. Can they use event bus instead of direct calls?
3. Are event schemas versioned?
4. Are direct calls justified exceptions?

TIP-008: Prefer event-driven integration.
```

### P10 — Runtime State Explainability Prompt

```
Assess runtime state explainability for [FEATURE_NAME]:

1. What state does each component maintain?
2. Is state mutation logged with provenance?
3. Can state be inspected without side effects?
4. Do DTOs follow the ADTO pattern with _provenance?

TIP-009: Use Auditable DTOs with provenance tracking.
```

---

## Output

The command produces an AIOA-compliant specification file at the standard spec location, with all AIOA principle metadata embedded.

**File:** `specs/{{spec_id}}.aioa.md`

**The specification includes all standard fields plus:**
- `p1_local_reasoning:` — Local Reasoning verdict
- `p2_crystallization_radius:` — the computed radius and breakdown
- `p3_semantic_integrity:` — boundaries, requirements, and contracts
- `p4_boundaries_explicit:` — boundary map
- `p5_contracts_deterministic:` — interface schemas and verification
- `p6_control_flow_simplicity:` — complexity assessment
- `p7_reasoning_boundaries_not_deployment:` — topology check results
- `p8_extract_under_reuse:` — abstraction justification
- `p9_event_boundaries:` — communication patterns
- `p10_runtime_state_explainable:` — state provenance plan
- `context_budget:` — per-role context estimation
