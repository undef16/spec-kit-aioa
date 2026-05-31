# Boundary Declarations

This document declares the context cost for every architectural boundary in the spec-kit-aioa preset.

## What is Context Cost?

Context cost is the number of files and components an AI agent must read to understand or safely modify something across a boundary. Higher context cost means higher risk of errors.

## Preset Boundaries

### commands/ → templates/

| Property | Value |
|----------|-------|
| Direction | Commands invoke templates |
| Context Cost | 1 file (the command references the template by name) |
| Contract | Template must accept mustache placeholders |
| Risk | Low — commands only reference templates, they don't modify them |

### templates/ → docs/

| Property | Value |
|----------|-------|
| Direction | Templates reference principles from docs |
| Context Cost | 3 files (AIOA-PRINCIPLES.md, CRYSTALLIZATION-RADIUS.md, SEMANTIC-INTEGRITY.md) |
| Contract | Principles are stable, versioned, immutable |
| Risk | Medium — changing a principle requires updating all templates that reference it |

### docs/ → README.md

| Property | Value |
|----------|-------|
| Direction | README summarizes docs/ |
| Context Cost | 1 file (README.md) |
| Contract | README must stay in sync with docs/ |
| Risk | Low — README is a summary, not a source of truth |

### commands/ → preset.yml

| Property | Value |
|----------|-------|
| Direction | Preset manifest declares commands |
| Context Cost | 1 file (preset.yml) |
| Contract | Command names and file paths must match |
| Risk | Low — preset.yml is a registry, not logic |

## Cross-Boundary Rules

1. No circular dependencies between directories
2. Each boundary must be traversable in ≤ 3 files
3. Changes to docs/ must propagate to templates/ within the same version
4. Commands must not directly reference other commands
