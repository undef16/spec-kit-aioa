---
description: "Mandatory AIOA compliance validation — enforces all 9 review gates before implementation"
scripts:
  - aioa validate
---

# speckit.aioa-enforcement.validate — AIOA Compliance Validation

> **Mandatory pre-implementation check.** Called automatically by `before_implement` hook with `optional: false`. Cannot be skipped.

**Purpose:** Verify that implementation artifacts (spec, plan, tasks, constitution) and code comply with all 9 AIOA review gates before any code is written.

## Process

### Step 1: Load Artifacts

Read these files from the project (if they exist):
- `spec.md` (or equivalent) — specification
- `plan.md` (or equivalent) — implementation plan
- `tasks.md` (or equivalent) — task breakdown
- `constitution.md` (or equivalent) — project constitution
- `data-model.md` — data model / contracts

Scan all source code files in the project.

### Step 2: Run Gate Checks

Check each gate. For every gate:
- Record **Evidence** — what was found
- Record **Violations** (if any) — specific files/lines
- Assign **Verdict**: PASS or FAIL

#### G1 — Crystallization Radius

> *"Minimize the context an agent must consume before making a safe change."*

| Check | Pass Criteria |
|-------|--------------|
| Context Budget | Every module/component has `context_budget` annotation in tasks.md |
| Budget Compliance | Implementation does not exceed declared budgets |
| R(C) Rating | No file requires understanding >8 files to modify safely |

**Pass:** All modules have budgets, code stays within bounds, no high R(C).  
**Fail:** Missing budgets, exceeded budgets, or high R(C) without justification.

#### G2 — Semantic Integrity

> *"Preserve meaning across architectural boundaries."*

| Check | Pass Criteria |
|-------|--------------|
| Shared Contracts | All cross-boundary data has typed contracts (Pydantic, JSON Schema, dataclass, etc.) |
| Boundary Parsers | Each boundary parses/validates at entry (Parse Don't Validate) |
| No Silent Reshapes | Data is not silently transformed between boundaries |
| Consistent Naming | The same concept has the same name everywhere |

**Pass:** All boundaries have contracts, parsers exist, no silent transformations.  
**Fail:** Missing contracts, untyped boundary crossings, naming inconsistencies.

#### G3 — Local Reasoning

> *"Code should be understandable from local context alone."*

| Check | Pass Criteria |
|-------|--------------|
| Explicit Dependencies | All imports/dependencies are declared (no global state, no implicit conventions) |
| Self-Contained Units | Each function/class can be understood without reading external code |
| No Hidden State | No global variables, mutable singletons, or thread-local state |
| Clear Interfaces | Function signatures are complete (typed params, typed returns) |

**Pass:** All code units are self-contained, no globals, clear signatures.  
**Fail:** Global state, implicit dependencies, unclear interfaces.

#### G4 — Boundaries Explicit

> *"All component boundaries must be clearly declared."*

| Check | Pass Criteria |
|-------|--------------|
| Boundary Map | All module/component boundaries are declared in plan.md |
| Boundary Annotations | Every cross-boundary call is annotated in code |
| Access Control | Cross-boundary access uses public interfaces, not internals |
| No Backdoors | No private member access across boundaries |

**Pass:** All boundaries declared, cross-boundary calls documented.  
**Fail:** Undeclared boundaries, private access across modules.

#### G5 — Contracts Deterministic

> *"Interfaces must have deterministic, machine-verifiable contracts."*

| Check | Pass Criteria |
|-------|--------------|
| Typed Interfaces | All interfaces use typed parameters and return values |
| Schema Validation | Data contracts have machine-readable schemas (JSON Schema, Pydantic, OpenAPI) |
| No `Any` | No untyped parameters, no `Any`/`object` on public interfaces |
| Idempotency | Side-effect-free functions are idempotent where required |

**Pass:** All interfaces typed, schema-validated, no Any.  
**Fail:** Untyped interfaces, missing schemas, Any used publicly.

#### G6 — Declarative Straight-Line

> *"Prefer linear, declarative code over complex control flow."*

| Check | Pass Criteria |
|-------|--------------|
| Nesting Depth | Maximum nesting ≤ 3 levels |
| Complex Flow | No deeply nested conditionals, no goto/label, no spaghetti |
| Declarative Style | Business logic reads as a sequence of steps, not nested branches |
| Early Returns | Functions use early exit pattern, not deep nesting |

**Pass:** Max nesting ≤3, straight-line flow, early returns.  
**Fail:** Deep nesting (>3), complex control flow, convoluted logic.

#### G7 — Decompose by Reasoning Not Deployment

> *"Logical architecture is orthogonal to deployment topology."*

| Check | Pass Criteria |
|-------|--------------|
| No Infra Coupling | Components do not reference deployment infrastructure (Docker, K8s, cloud) |
| Interface-Based | Components depend on interfaces, not on specific implementations |
| Config Separate | Deployment configuration is external (env vars, config files), not hardcoded |
| Topology Neutral | Same components work in monolith or microservices without changes |

**Pass:** No deployment coupling, interface-based dependencies, topology-neutral.  
**Fail:** Hardcoded infrastructure, deployment-specific logic in components.

#### G8 — Extract Under Reuse Pressure

> *"Don't abstract until reuse pressure exists."*

| Check | Pass Criteria |
|-------|--------------|
| Abstraction Justification | Every new abstraction has documented reuse or isolation pressure |
| No Premature Extraction | No abstractions created "just in case" or "for future use" |
| Consumer Count | Abstractions with a single consumer are not extracted (inline instead) |

**Pass:** All abstractions justified by real reuse/isolation pressure.  
**Fail:** Premature abstractions, "just in case" extractions, single-use abstractions.

#### G9 — Event Boundaries

> *"Use event bus for cross-component communication, not direct calls."*

| Check | Pass Criteria |
|-------|--------------|
| Event Bus for Cross-Component | Cross-component communication uses events, not direct method calls |
| Direct Call Justification | Any direct cross-component call has documented justification |
| No Sync Coupling | Components are not synchronously coupled across module boundaries |
| Event Contracts | Events have typed contracts (schema, routing, payload) |

**Pass:** Cross-component events, no sync coupling, all contracts typed.  
**Fail:** Direct cross-component calls without justification, sync coupling.

### Step 3: Generate Validation Report

Format the report:

```
## AIOA Validation Report
{date}, Project: {project_name}

### Gate Results
| Gate | Verdict | Violations |
|------|---------|------------|
| G1: Crystallization Radius | PASS/FAIL | {n} |
| G2: Semantic Integrity | PASS/FAIL | {n} |
| G3: Local Reasoning | PASS/FAIL | {n} |
| G4: Boundaries Explicit | PASS/FAIL | {n} |
| G5: Contracts Deterministic | PASS/FAIL | {n} |
| G6: Declarative Straight-Line | PASS/FAIL | {n} |
| G7: Reasoning ≠ Deployment | PASS/FAIL | {n} |
| G8: Extract Under Reuse | PASS/FAIL | {n} |
| G9: Event Boundaries | PASS/FAIL | {n} |

### Violation Details

**G{n}: {Gate Name} — FAIL**
- {file}:{line} — {description of violation}
- {file}:{line} — {description of violation}

### Summary
- Total Gates: 9
- Passed: {n}
- Failed: {n}
- Blocking: {YES/NO}
```

### Step 4: Determine Verdict

- **ALL gates PASS** → Output:
  ```
  ## AIOA Compliance: PASS ✅
  Proceeding to implementation.
  ```
- **ANY gate FAIL** → Output:
  ```
  ## AIOA Compliance: FAIL ❌
  **Implementation BLOCKED.** 
  Fix all violations listed above before proceeding.
  ```

### Important Rules

1. **Be thorough.** Scan ALL source files, not just artifacts.
2. **Be specific.** For each violation, include file path and line number.
3. **Be deterministic.** No "partial" verdicts — only PASS or FAIL per gate.
4. **Do not skip.** This command runs with `optional: false`. Execute every gate check completely.
5. **Document provenance.** Create or update `aioa-validation-report.md` in the project root with the full report.
