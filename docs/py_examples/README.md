# AIOA Python Examples

> **AIOA Spec-Kit Python Reference** — This directory contains Python implementations of all AIOA TIPs, used as concrete examples when generating tasks with `/speckit.tasks`.

Concrete implementations of AIOA TIPs in Python 3.10+.

## Files

| File | TIP | Concept |
|------|-----|---------|
| `adto.py` | TIP-007 | ADTO: Auditable Data Transfer Object (with deep-copy history and field validation) |
| `events.py` | TIP-007 + TIP-008 | Event types as ADTO subclasses (trace_id, timestamp, audit trail) |
| `event_bus.py` | TIP-008 | In-process event bus with typed dispatch and error isolation |
| `pipeline_builder.py` | TIP-008 | PipelineBuilder: declarative handler binding with auto-publish and wiring |
| `trading_events.py` | TIP-007 | Re-export of event types for backward compatibility |
| `identifiers.py` | TIP-002 | Typed wrappers for domain identifiers (UserId, OrderId, TrialId) |
| `fee_policy.py` | TIP-006 | Strategy pattern + ADTO-typed boundary data (FeeQuote) |

## Requirements

- Python 3.10+
- `pytest` (optional, for running tests)

## Running Tests

```bash
python -m pytest
```

## Reference

See [docs/AIOA.md](../AIOA.md) for complete TIP definitions.

See [fix.md](fix.md) for the audit report and rationale behind each design choice.
