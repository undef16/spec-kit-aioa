---
description: "Post-implementation code review — scans generated source files against AIOA TIPs"
---

# speckit.code-review — AIOA Code Review

> **Post-implementation check.** Called automatically by `after_implement` hook with `optional: false`. Validates generated source code, not just markdown specs.

**Purpose:** Scan generated source files against AIOA TIPs after implementation. This catches violations that markdown-only validation cannot detect.

## Process

### Step 1: Scan Source Files

Scan the project directory recursively for source files. Use the project's configured language patterns (e.g., glob patterns for source extensions). Skip build artifacts, dependencies, and generated directories.

### Step 1.5: Load Language-Specific Examples

Detect the project's primary language and load the corresponding examples directory:
- **Python**: `docs/py_examples/` — reference implementations for all TIPs
- **Other languages**: `docs/<language>_examples/` — equivalent TIP demonstrations

Use these as concrete reference during code review. Compare implementation patterns, naming conventions, and structural choices against the examples.

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

### Step 5: Sync Task Signatures with Code

After code review, sync the `.signatures:` declarations in all `tasks.md` files with the actual code:

1. Discover all `tasks.md` files via glob
2. For each file, extract every `.signatures:` entry
3. For each declared signature, check if it exists in the source code:
   - Classes: `class ClassName`, `struct ClassName`, `dataclass ClassName`
   - Types: `TypeName = ...`, `class TypeName`, `enum TypeName`
   - Methods: `ClassName.methodName` — search in the class scope
   - Functions: `def methodName`, `func methodName`
4. For missing signatures (declared but not in code):
   - Remove them from `.signatures:` — mark as removed with `# REMOVED — not in code`
5. For found signatures (in code but not declared):
   - Add them to `.signatures:` — append with `# ADDED — found in code`
6. For drifted signatures (declared signature differs from code):
   - Update `.signatures:` to match actual code signatue — `# SYNCED — signature changed`

Always sync. Even if code review found violations, the `.signatures:` must reflect reality. This ensures tasks.md is always an accurate catalog of what exists.

After sync, append to the code review report:
```
### Signature Sync
- Entries synced: {n}
- Removed (not in code): {n}
- Added (found in code): {n}
- Updated (signature changed): {n}
```

### Important Rules

1. **Scan ALL source files.** Do not hardcode file paths — glob for source files using the project's language patterns.
2. **Skip generated directories.** Build artifacts, dependencies, and generated code.
3. **Be specific.** For each violation, include file path and line number.
4. **Be deterministic.** No "partial" verdicts — only PASS or FAIL per TIP.
5. **Do not skip.** Execute every TIP check completely.
6. **Create report.** Save `code-review-report.md` in the project root with the full report.
