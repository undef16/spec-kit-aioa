# Provenance Tracking

This document defines provenance tracking for all generated artifacts.

## What is Provenance?

Provenance is the history of how a piece of data was created and modified. In AIOA, every generated artifact must carry provenance so agents can understand how it reached its current state.

## Provenance Fields

Every generated artifact must include these fields:

```yaml
provenance:
  created_by: "agent-name-or-user"
  created_at: "ISO-8601 timestamp"
  template_version: "1.0.0"
  preset_version: "1.0.0"
  modifications:
    - timestamp: "ISO-8601 timestamp"
      agent: "agent-name"
      change: "description of change"
```

## Artifact Provenance

### Specifications
- Created by: `/speckit.specify` command
- Template: `spec-template-aioa.md`
- Version tracked: template version, preset version

### Plans
- Created by: `/speckit.plan` command
- Template: `plan-template-aioa.md`
- Version tracked: template version, preset version, ADR count

### Tasks
- Created by: `/speckit.tasks` command
- Template: `tasks-template-aioa.md`
- Version tracked: template version, preset version, task count

### Code Reviews
- Created by: `/speckit.review` command
- Template: `code-review-template-aioa.md`
- Version tracked: template version, preset version, gate results

## Why This Matters

When an AI agent investigates a bug or reviews code, it can:
1. Identify which template generated the artifact
2. Understand what version of the preset was used
3. Trace modifications back to specific agents
4. Verify that the artifact is up-to-date with current principles
