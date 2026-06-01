# ADTO (Auditable Data Transfer Object) — Universal Pattern

> **Reference:** TIP-009 — Auditable DTOs  
> **Purpose:** Automatic, universal property-change tracking for any DTO via inheritance  
> **Source:** See [TIP-009.md](../AI-Native-Crystallization/TIP-009.md) for canonical definition

## The Problem

An AI agent reads data, transforms it, and writes results. If the agent needs to debug a problem, it must be able to trace **who** changed **what** and **when** — automatically, without manual instrumentation.

Traditional DTOs store state. They do not store provenance.

## The Pattern (Language-Agnostic)

This is the canonical implementation from TIP-009:

```pseudo
structure PropertyChange {
    property_name: String
    new_value: Any
}

structure TraceEntry {
    timestamp: Datetime          // Always UTC, timezone-aware
    caller_class: String         // Who made the change
    caller_method: String        // What method made the change
    changes: List<PropertyChange> // What properties changed (grouped)
    snapshot: Object              // Full object state at this point
}

abstract class ADTO {
    private history: List<TraceEntry> = []
    private trace_enabled: Boolean = Config.get("ADTO_TRACE_ENABLED")

    constructor() {
        if trace_enabled {
            bind_property_triggers(this)
        }
    }

    private on_property_changed(property_name: String, new_value: Any) {
        if !trace_enabled {
            return
        }

        caller = StackTrace.get_external_caller()
        last = history.last_or_null()

        change = PropertyChange(
            property_name = property_name,
            new_value = deep_clone(new_value)
        )

        // Merge consecutive changes from the same caller into one TraceEntry
        if last != null
           and last.caller_class == caller.class
           and last.caller_method == caller.method {

            last.changes.upsert_by_property(property_name, change)
            last.snapshot = deep_clone(this)
            return
        }

        history.add(
            TraceEntry(
                timestamp = Clock.utc_now(),
                caller_class = caller.class,
                caller_method = caller.method,
                changes = [change],
                snapshot = deep_clone(this)
            )
        )
    }

    function mutation_history(): List[TraceEntry] {
        return history
    }
}
```

**Key design point from TIP-009:** *"One caller method should produce one mutation slice. Not one audit record per setter."*

## How It Works

1. **Extend ADTO**: Any DTO class inherits from ADTO
2. **Constructor auto-registers**: `bind_property_triggers(this)` automatically binds ALL property setters — no manual wiring needed
3. **Set properties normally**: `dto.name = "foo"`, `dto.value = 42`
4. **Property triggers fire**: `on_property_changed` detects each change via automatic binding
5. **Caller is identified**: Stack trace determines which class+method made the change
6. **Consecutive calls merge**: If the same method sets multiple properties, they group into one TraceEntry (the "mutation slice")
7. **Snapshot captured**: Full object state is deep-cloned and stored
8. **History queryable**: `dto.mutation_history()` returns all TraceEntries

## Concrete Example (Python)

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, List, get_type_hints
import copy
import inspect


@dataclass(frozen=True)
class PropertyChange:
    """A single property change — immutable."""
    property_name: str
    new_value: Any


@dataclass(frozen=True)
class TraceEntry:
    """A group of changes from a single caller — the 'mutation slice'."""
    timestamp: datetime
    caller_class: str
    caller_method: str
    changes: List[PropertyChange]
    snapshot: Any


class ADTO:
    """
    Base class for auditable DTOs.

    Usage:
        class OrderDTO(ADTO):
            total: float = 0.0
            status: str = "pending"

        order = OrderDTO()
        order.total = 100.0       # Auto-tracked
        order.status = "confirmed" # Merged into same TraceEntry (same caller)
    """

    _adto_tracked: dict = {}

    def __init_subclass__(cls, trace_enabled: bool = True, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._trace_enabled = trace_enabled
        cls._adto_tracked = {
            name: getattr(cls, name)
            for name in vars(cls)
            if not name.startswith("_") and not callable(getattr(cls, name))
        }
        for name in cls._adto_tracked:
            private = f"_adto_{name}"
            setattr(cls, name, property(
                lambda self, p=private: getattr(self, p),
                lambda self, val, n=name, p=private: (
                    object.__setattr__(self, p, val),
                    self._on_property_changed(n, val),
                ),
            ))

    def __init__(self) -> None:
        self._history: List[TraceEntry] = []
        for name, default in self._adto_tracked.items():
            object.__setattr__(self, f"_adto_{name}", copy.deepcopy(default))

    def _on_property_changed(self, property_name: str, new_value: Any) -> None:
        if not getattr(type(self), "_trace_enabled", True):
            return

        caller_class, caller_method = self._get_caller()

        change = PropertyChange(
            property_name=property_name,
            new_value=copy.deepcopy(new_value),
        )

        last = self._history[-1] if self._history else None
        if last and last.caller_class == caller_class and last.caller_method == caller_method:
            merged = [c for c in last.changes if c.property_name != property_name]
            merged.append(change)
            self._history[-1] = TraceEntry(
                timestamp=last.timestamp,
                caller_class=last.caller_class,
                caller_method=last.caller_method,
                changes=merged,
                snapshot=copy.deepcopy(self),
            )
            return

        self._history.append(TraceEntry(
            timestamp=datetime.now(timezone.utc),
            caller_class=caller_class,
            caller_method=caller_method,
            changes=[change],
            snapshot=copy.deepcopy(self),
        ))

    def _get_caller(self):
        for frame in inspect.stack()[2:]:
            obj = frame.frame.f_locals.get("self")
            if obj is not None and type(obj).__name__ != "ADTO":
                return type(obj).__name__, frame.function
        return "unknown", "unknown"

    def mutation_history(self) -> List[TraceEntry]:
        return list(self._history)


# === USAGE ===

class OrderDTO(ADTO):
    total: float = 0.0
    status: str = "pending"
    discount: float = 0.0


order = OrderDTO()
order.total = 100.0       # TraceEntry #1
order.status = "confirmed" # Merged into #1 (same caller)
order.discount = 20.0     # TraceEntry #2 (different caller)

for entry in order.mutation_history():
    print(f"[{entry.timestamp}] {entry.caller_class}.{entry.caller_method}: "
          f"{[c.property_name for c in entry.changes]}")
```

## Concrete Example (TypeScript)

```typescript
interface PropertyChange {
    propertyName: string;
    newValue: unknown;
}

interface TraceEntry {
    timestamp: Date;
    callerClass: string;
    callerMethod: string;
    changes: PropertyChange[];
    snapshot: unknown;
}

abstract class ADTO {
    private history: TraceEntry[] = [];
    private traceEnabled: boolean;

    constructor(traceEnabled: boolean = true) {
        this.traceEnabled = traceEnabled;

        if (this.traceEnabled) {
            this.bindPropertyTriggers();
        }
    }

    private bindPropertyTriggers(): void {
        // Auto-register all own properties via Proxy
        const handler: ProxyHandler<this> = {
            set: (target, prop: string, value) => {
                const oldValue = target[prop];
                target[prop] = value;

                if (typeof prop !== 'string' || prop.startsWith('_')) return true;

                this.onPropertyChanged(prop, value);
                return true;
            }
        };

        // Apply proxy (TypeScript/JavaScript auto-registration)
        return new Proxy(this, handler) as unknown as void;
    }

    private onPropertyChanged(propertyName: string, newValue: unknown): void {
        if (!this.traceEnabled) return;

        const caller = this.getCaller();
        const last = this.history[this.history.length - 1];

        const change: PropertyChange = {
            propertyName,
            newValue: structuredClone(newValue)
        };

        // Merge consecutive changes from same caller
        if (last && last.callerClass === caller.className && last.callerMethod === caller.methodName) {
            const idx = last.changes.findIndex(c => c.propertyName === propertyName);
            if (idx >= 0) {
                last.changes[idx] = change;
            } else {
                last.changes.push(change);
            }
            last.snapshot = structuredClone(this);
            return;
        }

        this.history.push({
            timestamp: new Date(),
            callerClass: caller.className,
            callerMethod: caller.methodName,
            changes: [change],
            snapshot: structuredClone(this)
        });
    }

    private getCaller(): { className: string; methodName: string } {
        const stack = new Error().stack ?? '';
        const frames = stack.split('\n').slice(3);
        for (const frame of frames) {
            const match = frame.match(/at (\w+)\.(\w+)/);
            if (match && match[1] !== 'ADTO') {
                return { className: match[1], methodName: match[2] };
            }
        }
        return { className: 'unknown', methodName: 'unknown' };
    }

    mutationHistory(): TraceEntry[] {
        return [...this.history];
    }
}
```

## Anti-Patterns

### ❌ AP1: Manual @property instead of auto-registration

```python
# WRONG — developer must wire every property manually, violates P1 (Local Reasoning)
class OrderDTO(ADTO):
    @property
    def total(self): return self._total

    @total.setter
    def total(self, val):
        self._total = val
        self._on_property_changed("total", val)

# CORRECT — just declare fields, __init_subclass__ auto-wires everything
class OrderDTO(ADTO):
    total: float = 0.0   # Auto-tracked via __init_subclass__
    status: str = "pending"
```

### ❌ AP2: One audit record per setter (no grouping)

```python
# WRONG — each property change is a separate TraceEntry
# This creates noise: 5 entries for one service method
order.total = 100.0   # TraceEntry #1
order.status = "confirmed"  # TraceEntry #2 (same method!)
order.discount = 20.0  # TraceEntry #3 (same method!)

# CORRECT — consecutive changes from same caller merge into one TraceEntry
# This creates clarity: 1 entry for one service method
order.total = 100.0     # TraceEntry #1
order.status = "confirmed"  # Merged into #1
order.discount = 20.0   # TraceEntry #2 (different caller)
```

### ❌ AP3: Naive datetime

```python
# WRONG — uncomparable, unserializable
self.timestamp = datetime.now()

# CORRECT — UTC, comparable, serializable
self.timestamp = datetime.now(timezone.utc)
```

### ❌ AP4: Mutable mutation history

```python
# WRONG — anyone can corrupt the audit trail
self.history = []

# CORRECT — defensive copy on read
def mutation_history(self):
    return list(self._history)
```

## Checklist for AI Agents

Before marking an ADTO implementation as `[x]`, verify:

- [ ] ADTO is a **base class** — any DTO extends it (no copy-paste per class)
- [ ] `__init_subclass__` auto-creates `@property` from type annotations — **no manual setters**, follows P1 (Local Reasoning)
- [ ] Caller identification uses **stack trace** (`caller_class` + `caller_method`)
- [ ] Consecutive calls from same caller are **merged** into one TraceEntry (one mutation slice per caller method)
- [ ] Each TraceEntry has a **full snapshot** (deep-cloned object state)
- [ ] All `datetime` fields use `timezone.utc` — no naive datetimes
- [ ] History is **append-only** with defensive copy on read
- [ ] Trace is **config-gated** (`ADTO_TRACE_ENABLED`) — zero overhead when disabled
