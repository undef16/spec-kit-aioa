# AI-Oriented Architecture (AIOA) — Spec Kit Preset

> **Makes AIOA principles executable by AI agents.**  
> Every architectural decision is guided by the 10 AIOA principles, 2 core constraints, and 9 review gates.

---

## What is AIOA?

**AI-Oriented Architecture (AIOA)** is an architectural approach designed for a world where AI agents write, review, and maintain code alongside humans. Traditional architecture patterns optimize for human comprehension; AIOA optimizes for **predictable, safe AI intervention**.

### Core Constraints

| Constraint | Description |
|------------|-------------|
| **C1: Minimize Crystallization Radius** | Minimize the context an AI agent must consume before making a safe change |
| **C2: Preserve Semantic Integrity** | Preserve meaning across all architectural boundaries |

### The 10 Principles

| # | Principle | Core Question |
|---|-----------|--------------|
| P1 | **Local Reasoning** | Can code be understood from local context alone? |
| P2 | **Crystallization Radius** | How much context must an agent consume before making a safe change? |
| P3 | **Semantic Integrity** | Is meaning preserved across architectural boundaries? |
| P4 | **Boundaries Explicit** | Are all component boundaries clearly declared? |
| P5 | **Contracts Deterministic** | Are interfaces machine-verifiable? |
| P6 | **Declarative Straight-Line** | Is code linear and declarative over complex control flow? |
| P7 | **Reasoning Boundaries not Deployment** | Is logical architecture orthogonal to deployment topology? |
| P8 | **Extract Under Reuse Pressure** | Are abstractions deferred until reuse pressure exists? |
| P9 | **Event Boundaries** | Is cross-component communication event-driven? |
| P10 | **Runtime State Explainable** | Can runtime state be explained and audited? |

### Key TIPs

- **TIP-007: Strict JSON Gateways** — validate at boundaries
- **TIP-008: Event-Driven Integration** — event bus for cross-component communication
- **TIP-009: Auditable DTOs (ADTO)** — runtime state provenance tracking

---

## Installation

```bash
specify preset add https://github.com/undef16/spec-kit-aioa/releases/download/v1.0.0/aioa-preset.zip
```

### From local folder (development)

```bash
specify preset add --dev "D:\Work\spec-kit-aioa\spec-kit-aioa-preset"
```

### Prerequisites

- **Spec Kit** version `>=0.8.0`
- A project already initialized with `specify init`

---

## Publishing to GitHub

Spec Kit provides a built-in command to publish your preset as a GitHub release:

```bash
specify preset publish
```

**Steps:**

1. **Ensure `preset.yml` is valid** — Run `specify preset validate` to check for errors.
2. **Run `specify preset publish`** — This creates a GitHub release with the preset packaged as a ZIP archive.
3. **Done** — Users can now install via the release URL.

### Manual alternative

If you prefer not to use the built-in command, create a GitHub release manually and upload the ZIP archive of the preset directory.

---



## How It Modifies the SDD Workflow

The AIOA preset overlays architectural guardrails on top of the standard Spec-Driven Development workflow:

### 1. Specification (`/speckit.specify`)
AIOA adds **full principle impact analysis** to every specification. Before a spec is approved, the agent completes assessments for all 10 AIOA principles (P1–P10), ensuring compliance with both core constraints (C1, C2).

### 2. Planning (`/speckit.plan`)
Every plan includes **Architecture Decision Records (ADRs)** with explicit analysis of all relevant principles. Plans surface hidden coupling, surface area expansion, and boundary violations before any code is written.

### 3. Task Generation (`/speckit.tasks`)
Each task is annotated with:
- Context budget (maximum files/scope the agent needs to load)
- All applicable AIOA principle checks
- Integrity gates at every boundary crossing
- Explainability requirements for runtime state

### 4. Code Review (`/speckit.review`)
The AIOA code review template enforces all **9 review gates** (note: `/speckit.review` is AIOA-specific — it is not part of the core Spec Kit):
1. Crystallization Radius — context budget check
2. Semantic Integrity — shared types and boundary contracts
3. Local Reasoning — can code be understood without external context?
4. Boundary Explicitness — are all boundaries declared?
5. Contract Determinism — are interfaces machine-verifiable?
6. Control-Flow Simplicity — is code straight-line and declarative?
7. Decomposition Quality — appropriate granularity?
8. Integration Locality — are integrations local and explicit?
9. Runtime Explainability — can runtime state be explained?

---

## Key Concepts

### Crystallization Radius

> *"The amount of additional context an AI agent must consume before making a safe change to a given component."*

**Measure it:**
- **Low** (👍 ideal): 1–3 files, no cross-module understanding needed
- **Medium** (⚠️ caution): 4–8 files, some module interdependence
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
| `/speckit.constitution` | Create or update project constitution with AIOA principles |
| `/speckit.specify` | Define feature requirements with full AIOA principle analysis |
| `/speckit.clarify` | Interactive Q&A to fix under-specification |
| `/speckit.plan` | Generate an implementation plan with ADRs and principle checks |
| `/speckit.tasks` | Decompose tasks with AIOA annotations and context budgets |
| `/speckit.analyze` | Cross-artifact consistency check |
| `/speckit.implement` | Execute implementation tasks |
| `/speckit.checklist` | Generate quality checklists |
| `/speckit.review` | Review code against all 9 AIOA review gates |
| `/speckit.taskstoissues` | Convert tasks to GitHub issues |

### ⚠️ Important: Mentioning principles in `/speckit.constitution`

When running `/speckit.constitution`, you **must** mention the principles you want in your prompt. The agent needs explicit instruction to include them.

**Correct:**
```
/speckit.constitution
AIOA project. Follow AI-Oriented Architecture principles. Also use OOP, DRY, KISS.
```

**Wrong (principles will be missing):**
```
/speckit.constitution
My project description here...
```

The AIOA preset template hardcodes the 10 AIOA principles, but the agent will only fill them in if you explicitly ask. Include any additional principles (OOP, DRY, KISS, SOLID, TDD, etc.) in the same prompt.

### Create a new specification with AIOA compliance

```
/speckit.specify
Add user authentication with email+password, JWT tokens, works in monolith and microservices.
```

The AIOA preset will prompt for all 10 principles:
- Local Reasoning assessment
- Crystallization Radius of authentication feature
- Semantic Integrity of user identity across modules
- Boundaries Explicit map
- Contracts Deterministic check
- Control-Flow Complexity check
- Reasoning Boundaries vs Deployment check
- Extract Under Reuse Pressure assessment
- Event Boundaries plan
- Runtime State Explainability plan

### Generate a plan with architecture decisions

```
/speckit.plan
```

Each plan step includes:
- ADRs with all applicable AIOA principle analysis
- Component boundary map
- Semantic Integrity checkpoints
- Runtime state explainability requirements

### Review code against AIOA principles

```
/speckit.review
```

The review template checks all 9 review gates:
- Crystallization Radius regression
- Semantic Integrity preservation
- Local Reasoning quality
- Boundary Explicitness
- Contract Determinism
- Control-Flow Simplicity
- Decomposition Quality
- Integration Locality
- Runtime Explainability

---

## Preset Structure

```
spec-kit-aioa-preset/
├── preset.yml                      # Preset manifest
├── README.md                       # This file
├── LICENSE                         # MIT License
├── templates/
│   ├── constitution.md             # AIOA principles as project constitution
│   ├── spec-template.md            # Spec template with AIOA constraints
│   ├── plan-template.md            # Plan template with Crystallization Radius checks
│   ├── task-template.md            # Task template with Semantic Integrity gates
│   └── code-review-template.md     # Code review template with AIOA compliance
├── commands/
│   ├── speckit.specify.md          # Enhanced specify command with AIOA guidance
│   ├── speckit.plan.md             # Plan command with architecture checks
│   └── speckit.tasks.md            # Tasks command with AIOA validation steps
└── docs/
    ├── AIOA-PRINCIPLES.md          # Full AIOA principles reference (all 10)
    ├── CRYSTALLIZATION-RADIUS.md   # Crystallization Radius guide
    └── SEMANTIC-INTEGRITY.md       # Semantic Integrity guide
```

---

## License

MIT — see [LICENSE](./LICENSE).

---

## Author

**undef16**
