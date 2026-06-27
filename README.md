# [AI-Oriented Architecture (AIOA)](https://github.com/undef16/AI-Oriented-Architecture) — Spec Kit Preset



> **Makes your codebase safe for AI coding assistants.**  
> Every architectural decision is guided by Technical Implementation Patterns (TIP-002-TIP-009).

---

## What is AIOA?

[**AI-Oriented Architecture (AIOA)**](https://github.com/undef16/AI-Oriented-Architecture) is an architectural approach designed for a world where AI coding assistants (Claude Code, Copilot, Cursor) write, review, and maintain code alongside humans. Traditional architecture patterns optimize for human comprehension; AIOA optimizes for **predictable, safe AI intervention**.

### Core Constraints

| Constraint | Description |
|------------|-------------|
| **C1: Minimize Crystallization Radius** | Minimize the context an AI agent must consume before making a safe change |
| **C2: Preserve Semantic Integrity** | Preserve meaning across all architectural boundaries |

### Technical Implementation Patterns (TIPs)

| TIP | Pattern | Concern |
|-----|---------|---------|
| TIP-002 | **Semantic Collision - The Erasure of Domain Boundaries** | Every domain-significant value has a distinct type - no primitive obsession |
| TIP-003 | **Repository Search Is the Real Bottleneck in AI Coding Agents** | Ordinary changes are discoverable through narrow, explicit structural paths |
| TIP-004 | **Code Crystallization - Reducing Architectural Indirection** | No dead wrappers, forwarding chains, or pattern-shaped layers without meaning |
| TIP-005 | **The Quantum Spectrum — Controlling Component Crystallization Radius** | Use Micro, Nano, and Pico actors deliberately as reasoning boundaries |
| TIP-006 | **Declarative Straight-Line Code - Reducing Control-Flow Crystallization Radius** | Extract retry, timeout, transaction, callback, and concurrency mechanics into named policies or boundaries |
| TIP-007 | **Strict JSON Gateways and Auditable DTOs - Stop Defensive Programming in Business Logic** | Loose input dies at gateways and enters business logic only as typed DTO/ADTO contracts |
| TIP-008 | **Event-Driven Integration — Reducing Cross-Boundary Reasoning** | Components communicate through explicit business events to reduce cross-boundary reasoning |
| TIP-009 (Draft) | **Omission** | Omit parameters, wrappers, providers, config hops, dependencies, and files that do not carry meaning |

---

## Installation

```bash
specify preset add --from https://github.com/undef16/spec-kit-aioa/archive/refs/heads/main.zip
```

### From local folder (development)

```bash
specify preset add --dev D:\Work\spec-kit-aioa
```

### Prerequisites

- **Spec Kit** version `>=0.8.0`
- A project already initialized with `specify init`

### Verify installation

```bash
# Verify installation
specify preset info aioa

# List installed presets
specify preset list
```

### Extension (AIOA Enforcement)

For mandatory pre-implementation AIOA compliance validation, install the companion extension:

```bash
specify extension add aioa --from https://github.com/undef16/spec-kit-aioa/archive/refs/heads/main.zip
```

### From local folder (development)
```bash
specify extension add --dev D:\Work\spec-kit-aioa
```

The extension adds a mandatory `before_implement` hook that automatically runs AIOA compliance validation (`/speckit.aioa-enforcement.validate`) every time `/speckit.implement` is called. The hook has `optional: false` — it **cannot be skipped**.

What it does:
- Loads all project artifacts (spec, plan, tasks, constitution)
- Scans all source code
- Validates all .md files against TIP-002-TIP-009 with deterministic pass/fail criteria
- **Blocks implementation** if any TIP fails
- Generates `aioa-validation-report.md` with full violation details

---

## How It Modifies the SDD Workflow

The AIOA preset overlays architectural guardrails on top of the standard Spec-Driven Development workflow:

### 1. Specification (`/speckit.specify`)
AIOA integrates TIP checks directly into the specification process. Each architecture layer is described using applicable TIPs — semantic types (TIP-002), context locality (TIP-003), crystallization noise removal (TIP-004), actor granularity (TIP-005), execution mechanics (TIP-006), strict input boundaries and ADTOs (TIP-007), event-driven integration (TIP-008), omission (TIP-009 Draft). No separate compliance section — TIPs ARE the architecture.

### 2. Planning (`/speckit.plan`)
Every plan includes **Architecture Decision Records (ADRs)** with AIOA TIPs applied directly to each decision — strict input contracts and ADTOs (TIP-007), event-driven integration (TIP-008), Pico/Nano/Micro levels (TIP-005), context locality (TIP-003), no dead abstraction (TIP-004), extracted mechanics (TIP-006), and semantic types (TIP-002).

### 3. Task Generation (`/speckit.tasks`)
Each task is annotated with:
- Context budget (maximum files the agent needs to load)
- AIOA TIPs applicable to this task
- Verification criteria
### 4. AIOA Validation (`/speckit.aioa-enforcement.validate`)

Mandatory pre-implementation check. Runs automatically via `before_implement` hook (cannot be skipped). Validates all AIOA TIPs and generates `aioa-validation-report.md`.

---

## Key Concepts

### Crystallization Radius

> *"The amount of additional context an AI agent must consume before making a safe change to a given component."*

**Measure it:**
- **Low** (👍 ideal): 1–3 files, no cross-module understanding needed
- **Medium** (⚠️ caution): 4–7 files, some module interdependence
- **High** (🚨 toxic): 9+ files, cross-cutting concerns, implicit dependencies

**Minimize it:**
- Favor narrow, deep modules over wide, shallow ones
- Explicitly declare all dependencies
- Avoid "hidden context" (global state, implicit conventions, shared mutable data)
- Use `context_budget` annotations in every component

### Semantic Integrity

> *"The property that meaning is preserved as data and behavior cross architectural boundaries."*

Data that means one thing in module A should mean the same thing in module B. Violations occur when:
- Two modules interpret the same field differently
- The same concept is represented in incompatible ways across boundaries
- Validation or transformation is applied inconsistently

**Preserve it:**
- Define shared semantic contracts (types, vocabularies, invariants)
- Parse at boundaries, trust internally ("Parse, Don't Validate")
- Never silently reshape data between components

### Reasoning Boundaries not Deployment (Architectural Independence)

> *"The property that logical architecture is orthogonal to deployment architecture."*

Your components should not know or care whether they run in a monolith, microservices, or serverless environment. Violations occur when:
- Components depend on specific deployment infrastructure
- Network boundaries are assumed in component design
- Deployment topology dictates logical module boundaries

**Enforce it:**
- Components depend on interfaces, not infrastructure
- Deployment is a configuration concern, not an architectural one
- Boundaries are semantic, not physical

---

## Usage Examples

### Slash Commands (AI Assistant)

These commands are typed inside an AI coding assistant (GitHub Copilot, Claude Code, Cursor, Windsurf, etc.) — they are **not** CLI commands. Both the full form (`/speckit.specify`) and short form (`/specify`) are supported.

| Command | Description |
|---------|-------------|
| `/speckit.constitution` | Create or update project constitution with AIOA TIPs |
| `/speckit.specify` | Define feature requirements with full AIOA TIP analysis |
| `/speckit.clarify` | Interactive Q&A to fix under-specification |
| `/speckit.plan` | Generate an implementation plan with ADRs and TIP checks |
| `/speckit.tasks` | Decompose tasks with AIOA annotations and context budgets |
| `/speckit.analyze` | Cross-artifact consistency check |
| `/speckit.implement` | Execute implementation tasks |
| `/speckit.checklist` | Generate quality checklists |
| `/speckit.taskstoissues` | Convert tasks to GitHub issues |
| `/speckit.aioa-enforcement.validate` | Pre-implementation AIOA compliance validation (mandatory hook, requires extension) |

### ⚠️ Important: Mentioning TIPs in `/speckit.constitution`

When running `/speckit.constitution`, you **must** mention the TIPs you want in your prompt. The agent needs explicit instruction to include them.

**Correct:**
```
/speckit.constitution
AIOA project. Follow AIOA Technical Implementation Patterns (TIP-002-TIP-009). Also use OOP, DRY, KISS.
```

**Wrong (TIPs will be missing):**
```
/speckit.constitution
My project description here...
```

The AIOA preset template references the canonical AIOA TIPs, but the agent will only fill them in if you explicitly ask. Include any additional principles (OOP, DRY, KISS, SOLID, TDD, etc.) in the same prompt.

### Create a new specification with AIOA compliance

```
/speckit.specify
Add user authentication with email+password, JWT tokens, works in monolith and microservices.
```

The AIOA preset will guide architecture through TIPs:
- **TIP-002: Semantic Collision - The Erasure of Domain Boundaries** — distinct Value Objects for Email, PasswordHash, JwtToken
- **TIP-003: Repository Search Is the Real Bottleneck in AI Coding Agents** — keep auth changes discoverable through focused boundary files
- **TIP-004: Code Crystallization - Reducing Architectural Indirection** — no wrapper layers that only forward auth calls
- **TIP-005: The Quantum Spectrum — Controlling Component Crystallization Radius** — Pico actors for hashing, Nano actors for session workflows, Micro actors for auth boundary ownership
- **TIP-006: Declarative Straight-Line Code - Reducing Control-Flow Crystallization Radius** — extract retry/rate-limit into AuthPolicy
- **TIP-007: Strict JSON Gateways and Auditable DTOs - Stop Defensive Programming in Business Logic** — validate login payloads at gateways, pass typed contracts inward, and preserve provenance for important mutable state
- **TIP-008: Event-Driven Integration — Reducing Cross-Boundary Reasoning** — UserLoggedIn event for cross-actor communication
- **TIP-009 (Draft): Omission** — omit speculative providers, factories, wrappers, and config hops

### Generate a plan with architecture decisions

```
/speckit.plan
```

Each plan step includes:
- ADRs with AIOA TIPs applied to each decision
- Component boundary map
- Context budget per step

### Validate code against AIOA TIPs

```
/speckit.aioa-enforcement.validate
```

Validates against all AIOA TIPs:
- TIP-002: Semantic Collision - The Erasure of Domain Boundaries — distinct types, no primitive obsession
- TIP-003: Repository Search Is the Real Bottleneck in AI Coding Agents — narrow, explicit structural paths
- TIP-004: Code Crystallization - Reducing Architectural Indirection — no dead wrapper chains
- TIP-005: The Quantum Spectrum — Controlling Component Crystallization Radius — deliberate Micro/Nano/Pico boundaries
- TIP-006: Declarative Straight-Line Code - Reducing Control-Flow Crystallization Radius — extracted execution mechanics
- TIP-007: Strict JSON Gateways and Auditable DTOs - Stop Defensive Programming in Business Logic — loose input dies at gateways and important mutable state is explainable through ADTOs
- TIP-008: Event-Driven Integration — Reducing Cross-Boundary Reasoning — event-driven integration across boundaries
- TIP-009 (Draft): Omission — omit what does not carry meaning

---

## Preset Structure

```
spec-kit-aioa-preset/
├── preset.yml                          # Preset manifest (strategy: append)
├── README.md                           # This file
├── LICENSE                             # MIT License
├── CHANGELOG.md                        # Version history
├── templates/                          # AIOA additions (appended to core templates)
│   ├── constitution-template-aioa.md   # AIOA TIP wrap (TIP-002-TIP-009)
│   ├── spec-template-aioa.md           # AIOA TIP wrap for specification
│   ├── plan-template-aioa.md           # AIOA TIP wrap for planning ADRs
│   └── tasks-template-aioa.md          # AIOA TIP wrap for task decomposition
├── commands/                           # Command overrides
│   ├── speckit.specify.md              # Specify command with AIOA TIP guidance
│   ├── speckit.plan.md                 # Plan command with AIOA TIP guidance
│   └── speckit.tasks.md                # Tasks command with AIOA TIP guidance
└── docs/                               # AIOA reference documentation
    └── AIOA.md                         # Technical Implementation Patterns — single source of truth for TIP-002-TIP-009
```


### Extension Structure

The AIOA Enforcement Extension adds:

```
aioa-enforcement/
├── extension.yml                       # Extension manifest with mandatory before_implement hook
└── commands/
    ├── speckit.aioa-enforcement.validate.md        # AIOA TIP validation command (TIP-002-TIP-009)

```

Install alongside the preset for comprehensive AIOA enforcement.

---

## License

MIT — see [LICENSE](./LICENSE).

---

## Author

**undef16**
