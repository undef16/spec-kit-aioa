# Context Budget Annotations

This document defines context budget annotations for all public interfaces in the spec-kit-aioa preset.

## What is Context Budget?

Context budget is the maximum number of files and tokens an AI agent needs to load to understand or modify a component. Every public interface must declare its context budget.

## Template Context Budgets

### constitution-template-aioa.md
- **Context Budget:** 2 files (this template + AIOA-PRINCIPLES.md)
- **Token Estimate:** ~3000 tokens
- **Modification Risk:** Low — changes affect project constitution only

### spec-template-aioa.md
- **Context Budget:** 3 files (this template + AIOA-PRINCIPLES.md + constitution-template-aioa.md)
- **Token Estimate:** ~4000 tokens
- **Modification Risk:** Medium — changes affect feature specifications

### plan-template-aioa.md
- **Context Budget:** 4 files (this template + AIOA-PRINCIPLES.md + constitution-template-aioa.md + spec-template-aioa.md)
- **Token Estimate:** ~5000 tokens
- **Modification Risk:** Medium — changes affect implementation plans

### tasks-template-aioa.md
- **Context Budget:** 5 files (this template + AIOA-PRINCIPLES.md + constitution-template-aioa.md + spec-template-aioa.md + plan-template-aioa.md)
- **Token Estimate:** ~4000 tokens
- **Modification Risk:** Medium — changes affect task decomposition

### code-review-template-aioa.md
- **Context Budget:** 6 files (this template + AIOA-PRINCIPLES.md + constitution-template-aioa.md + spec-template-aioa.md + plan-template-aioa.md + tasks-template-aioa.md)
- **Token Estimate:** ~5000 tokens
- **Modification Risk:** High — changes affect code quality gates

## Command Context Budgets

### speckit.specify.md
- **Context Budget:** 2 files (this command + spec-template-aioa.md)
- **Token Estimate:** ~2000 tokens
- **Modification Risk:** Low

### speckit.plan.md
- **Context Budget:** 3 files (this command + plan-template-aioa.md + spec-template-aioa.md)
- **Token Estimate:** ~2000 tokens
- **Modification Risk:** Low

### speckit.tasks.md
- **Context Budget:** 4 files (this command + tasks-template-aioa.md + plan-template-aioa.md + spec-template-aioa.md)
- **Token Estimate:** ~2000 tokens
- **Modification Risk:** Low
