---
description: "Mandatory AIOA validation — checks all .md files against TIP-002-TIP-008"
---

# speckit.aioa-enforcement.validate — AIOA TIP Validation

> **Mandatory pre-implementation check.** Called automatically by `before_implement` hook with `optional: false`. Cannot be skipped.

**Purpose:** Verify that ALL `.md` files in the project comply with AIOA TIPs (TIP-002 through TIP-008) before any code is written.

## Process

### Step 1: Load All Markdown Files

Scan the entire project directory recursively. Find ALL `*.md` files:
- Spec files (`spec.md`, `spec.aioa.md`, etc.)
- Plan files (`plan.md`, etc.)
- Tasks files (`tasks.md`, etc.)
- Constitution (`constitution.md`, etc.)
- Contracts (`contracts/*.md`)
- Any other `.md` documentation files

Do NOT hardcode a file list — discover all `.md` files dynamically.

### Step 2: Run TIP Checks

Check each TIP against all `.md` files. For every TIP:
- Record **Evidence** — what was found
- Record **Violations** (if any) — specific files/lines
- Assign **Verdict**: PASS or FAIL

#### TIP-002: Semantic Collision

> *"Distinct types for distinct concepts — no primitive obsession."*

| Check | Pass Criteria |
|-------|--------------|
| No Primitive IDs | Domain identifiers are value objects, not `str`/`int` |
| No Naming Collision | Same name not used for different concepts across files |
| Distinct Types | Each domain concept has its own type, even if same structure |

**Pass:** All domain concepts have distinct types, no primitive IDs.  
**Fail:** Primitive IDs, naming collisions, same type for different concepts.

#### TIP-003: Repository Search Bottleneck

> *"Responsibility distributed across narrow, specialized modules. No single-file bottleneck."*

| Check | Pass Criteria |
|-------|--------------|
| No Mega-Files | No `.md` file exceeds context budget (max 7 files to understand) |
| Distributed Responsibility | Related content is spread across focused files, not one monolithic doc |
| Clear Boundaries | Each file has a clear scope — agent knows where to look |

**Pass:** Files are focused, responsibility is distributed, no mega-files.  
**Fail:** Monolithic files, scattered responsibilities, unclear file scopes.

#### TIP-004: Code Crystallization

> *"No dead wrapper chains — call directly if no value added."*

| Check | Pass Criteria |
|-------|--------------|
| No Dead Indirection | No component/module that only forwards without adding logic |
| Justified Abstractions | Every abstraction has documented consumers |
| Flat Where Possible | A→C directly when B adds no value |

**Pass:** No dead wrapper layers, abstractions are justified.  
**Fail:** Pass-through layers, single-consumer abstractions, unnecessary indirection.

#### TIP-005: Quantum Spectrum

> *"Components named by their level — Pico, Nano, Micro, not 'Service'."*

| Check | Pass Criteria |
|-------|--------------|
| Leveled Naming | Components use Pico/Nano/Micro nomenclature, not generic "Service" |
| Level-Appropriate Complexity | Pico actors are pure functionality, Nano actors have state, Micro actors are services |
| No Misleading Names | Component name reflects actual complexity |

**Pass:** Components named by level, complexity matches naming.  
**Fail:** Everything called "Service", misleading generic names.

#### TIP-006: Declarative Straight-Line Code

> *"Execution mechanics extracted into policies. Business code stays linear."*

| Check | Pass Criteria |
|-------|--------------|
| Mechanics Extracted | Retry, timeout, fallback are in separate policies, not inline |
| Linear Business Logic | Business logic reads as a sequence of steps, not nested branches |
| No Boilerplate | No repeated try/except/retry patterns across functions |

**Pass:** Mechanics extracted, business logic is straight-line, no boilerplate.  
**Fail:** Inline retry/fallback, deeply nested business logic.

#### TIP-007: Auditable Data Transfer Objects (ADTO)

> *"All boundary data is ADTO — typed + auditable."*

| Check | Pass Criteria |
|-------|--------------|
| Typed Boundaries | All cross-boundary data has typed schemas (ADTO, Pydantic, JSON Schema) |
| No Raw Dicts | No `output: dict` or `list[dict]` in contracts or schemas |
| Provenance | State mutations have provenance tracking (who, when, what changed) |

**Pass:** All boundaries typed, no raw dicts, provenance tracked.  
**Fail:** Untyped boundaries, raw dicts, no provenance.

#### TIP-008: Event-Driven Integration

> *"All cross-component communication goes through an event bus (even in-memory)."*

| Check | Pass Criteria |
|-------|--------------|
| Event Bus | Cross-component communication uses events, not direct calls |
| In-Memory Default | If no external broker, use InMemoryEventBus |
| Typed Events | Event payloads are typed (ADTO) |

**Pass:** Cross-component via events, typed payloads, in-memory fallback documented.  
**Fail:** Direct cross-component calls, untyped events, no event bus.

### Step 3: Generate Validation Report

Format the report:

```
## AIOA Validation Report
{date}, Project: {project_name}

### TIP Results
| TIP | Verdict | Violations |
|-----|---------|------------|
| TIP-002: Semantic Collision | PASS/FAIL | {n} |
| TIP-003: Repository Search Bottleneck | PASS/FAIL | {n} |
| TIP-004: Code Crystallization | PASS/FAIL | {n} |
| TIP-005: Quantum Spectrum | PASS/FAIL | {n} |
| TIP-006: Declarative Straight-Line | PASS/FAIL | {n} |
| TIP-007: Auditable Data Transfer Objects (ADTO) | PASS/FAIL | {n} |
| TIP-008: Event-Driven Integration | PASS/FAIL | {n} |

### Violation Details

**TIP-{N}: {TIP Name} — FAIL**
- {file}:{line} — {description of violation}
- {file}:{line} — {description of violation}

### Summary
- Total TIPs: 7
- Passed: {n}
- Failed: {n}
- Blocking: {YES/NO}
```

### Step 4: Determine Verdict

- **ALL TIPs PASS** → Output:
  ```
  ## AIOA Compliance: PASS ✅
  Proceeding to implementation.
  ```
- **ANY TIP FAIL** → Output:
  ```
  ## AIOA Compliance: FAIL ❌
  **Implementation BLOCKED.** 
  Fix all violations listed above before proceeding.
  ```

### Important Rules

1. **Scan ALL .md files.** Do not hardcode file paths — glob for all markdown files.
2. **Be specific.** For each violation, include file path and line number.
3. **Be deterministic.** No "partial" verdicts — only PASS or FAIL per TIP.
4. **Do not skip.** This command runs with `optional: false`. Execute every TIP check completely.
5. **Document provenance.** Create or update `aioa-validation-report.md` in the project root with the full report.
