---
description: "Mandatory AIOA validation — checks all .md files against AIOA TIPs"
---

# speckit.aioa-enforcement.validate — AIOA TIP Validation

> **Mandatory pre-implementation check.** Called automatically by `before_implement` hook with `optional: false`. Cannot be skipped.

**Purpose:** Verify that ALL `.md` files in the project comply with AIOA TIPs before any code is written.

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


### Step 2: Run Rule Checks

1. Read `docs/AIOA.md` and dynamically extract Rules → TIP mapping by parsing the pattern `### Rule {N} — {Rule Name} (TIP-{M})` from sections 4+. Use the full title text as the Rule Name (e.g. `### Rule 2 — Protect Domain Concepts with Semantic Types (TIP-002)` → Rule-2, TIP-002).
2. Also include the **ADTO Continuity Rule** as a separate Rule entry, mapping to TIP-007 (same TIP as Rule-8). It is documented in AIOA.md as `#### ADTO Continuity Rule` under the Rule 8 section.
3. For each extracted Rule, check all `.md` files against its detection categories defined in AIOA.md
4. Record **Evidence** — what was found
5. Record **Violations** (if any) — specific files/lines
6. Assign **Verdict**: PASS or FAIL per Rule

### Step 3: Generate Validation Report

Format the report:

```
## AIOA Validation Report
{date}, Project: {project_name}

### Rule Results
| Rule | TIP | Verdict | Violations |
|------|-----|---------|------------|
| {Rule-N}: {Rule Name} | {TIP-N}: {TIP Name} | PASS/FAIL | {n} |
... (one row per Rule found in AIOA.md)

### Violation Details

**Rule-{N}: {Rule Name} — FAIL** (TIP-{M}: {TIP Name})
- {file}:{line} — {description of violation}

### Summary
- Total Rules: {n}
- Passed: {n}
- Failed: {n}
- Blocking: {YES/NO}
```

### Step 4: Determine Verdict

- **ALL Rules PASS** → Output:
  ```
  ## AIOA Compliance: PASS ✅
  Proceeding to implementation.
  ```
- **ANY Rule FAIL** → Output:
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
