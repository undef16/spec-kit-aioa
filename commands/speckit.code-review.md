---
description: "Post-implementation code review — scans generated source files against AIOA TIPs"
---

# speckit.code-review — AIOA Code Review

> **Post-implementation check.** Called automatically by `after_implement` hook with `optional: false`. Validates generated source code, not just markdown specs.

**Purpose:** Scan generated source files against AIOA TIPs after implementation. This catches violations that markdown-only validation cannot detect.

## Process

### Step 1: Scan Source Files

Scan the project directory recursively for source files. Use the project's configured language patterns (e.g., glob patterns for source extensions). Skip build artifacts, dependencies, and generated directories.

### Step 2: Run TIP Checks Against Source Code

1. Read `docs/AIOA.md` to extract all TIP definitions, patterns, anti-patterns, and detection categories
2. For each TIP, check source code against its detection categories using AST/pattern analysis
3. Report violations with file:line references

### Step 3: Generate Code Review Report

Format the report:

```markdown
## AIOA Code Review Report
{date}, Project: {project_name}

### TIP Results
| TIP | Verdict | Violations |
|-----|---------|------------|
| {TIP-ID}: {TIP Name} | PASS/FAIL | {n} |
... (one row per TIP found in AIOA.md)

### Violation Details

**TIP-{N}: {TIP Name} — FAIL**
- {file}:{line} — {description of violation}

### Summary
- Files scanned: {n}
- Total TIPs: {n}
- Passed: {n}
- Failed: {n}
- Blocking: {YES/NO}
```

### Step 4: Determine Verdict

- **ALL TIPs PASS** → Output:
  ```
  ## AIOA Code Review: PASS ✅
  Implementation passes all AIOA TIP checks.
  ```
- **ANY TIP FAIL** → Output:
  ```
  ## AIOA Code Review: FAIL ❌
  **Implementation BLOCKED.**
  Fix all violations listed above before proceeding.
  ```

### Important Rules

1. **Scan ALL source files.** Do not hardcode file paths — glob for source files using the project's language patterns.
2. **Skip generated directories.** Build artifacts, dependencies, and generated code.
3. **Be specific.** For each violation, include file path and line number.
4. **Be deterministic.** No "partial" verdicts — only PASS or FAIL per TIP.
5. **Do not skip.** Execute every TIP check completely.
6. **Create report.** Save `code-review-report.md` in the project root with the full report.
