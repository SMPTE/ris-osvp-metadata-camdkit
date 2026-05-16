# Arrow: protocol-envelope

The structural core of camdkit — the `Clip` container, schema machinery, serialization, and primitive type foundation.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). All active specs implemented except PROTO-EX-005 (deterministic UUID in examples).

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters", "Cross-Cutting Concerns", "Key Architectural Decisions"

### LLD
- [docs/llds/protocol-envelope.md](../llds/protocol-envelope.md)

### EARS
- [docs/specs/protocol-envelope-specs.md](../specs/protocol-envelope-specs.md) — 19 specs (18 implemented, 1 gap)

### Tests
- `src/test/python/test_clip.py`
- `src/test/python/test_compatibility.py`
- `src/test/python/test_model.py`
- `src/test/python/test_numeric_types.py`
- `src/test/python/test_string_types.py`
- `src/test/python/test_utils.py`
- `src/test/python/test_versioning_types.py`
- `src/test/python/test_example_regression.py`
- `src/test/python/property/test_json_roundtrip.py`
- `src/test/python/property/test_schema_agreement.py`

### Code
- `src/main/python/camdkit/clip.py`
- `src/main/python/camdkit/compatibility.py`
- `src/main/python/camdkit/framework.py`
- `src/main/python/camdkit/model.py`
- `src/main/python/camdkit/versioning_types.py`
- `src/main/python/camdkit/numeric_types.py`
- `src/main/python/camdkit/string_types.py`
- `src/main/python/camdkit/units.py`
- `src/main/python/camdkit/utils.py`
- `src/main/python/camdkit/examples.py`
- `src/tools/python/generate_opentrackio_schema.py`
- `src/tools/python/generate_component_schemas.py`

## Architecture

**Purpose:** Defines the `Clip` container for all OpenTrackIO metadata, synthesizes property accessors from JSON Schema metadata, generates and exports the OpenTrackIO JSON Schema, and provides the primitive type infrastructure shared by all domain clusters.

**Key Components:**
1. `Clip` (`clip.py`) — central model; metaprogramming-driven property synthesis via `setup_clip_properties()`; tuple-based multi-frame storage; `append()` / `__getitem__()` / `to_json()` operations
2. `CompatibleBaseModel` (`compatibility.py`) — universal base class for all domain types; custom schema generation that strips Pydantic-internal wrapping layers
3. `InternalCompatibleSchemaGenerator` / `ExternalCompatibleSchemaGenerator` — two-schema design; internal retains `clip_property` metadata, external strips it
4. `VersionedProtocol` (`versioning_types.py`) — protocol name/version envelope; enforces `"OpenTrackIO"` name at construction
5. `guess_fps()` (`utils.py`) — fuzzy float-to-rational FPS conversion for reader use
6. Primitive types (`numeric_types.py`, `string_types.py`, `units.py`) — constrained primitives shared across all clusters
7. `examples.py` — four canonical Clip fixtures for testing and documentation

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| Clip model | PROTO-CORE-001 to PROTO-CORE-010 | 10 | 0 |
| Schema compatibility | PROTO-SCHEMA-001 to PROTO-SCHEMA-005 | 5 | 0 |
| Examples | PROTO-EX-001 to PROTO-EX-005 | 4 | 1 |

**Summary:** 19 of 20 active specs implemented; 1 gap (PROTO-EX-005).

## Key Findings

1. **Schema-driven metaprogramming** — `Clip.setup_clip_properties()` (`clip.py:213`) synthesizes all property accessors at class definition time from `json_schema_extra` `clip_property` paths. Adding a spec field requires only a Pydantic field declaration.
2. **Two-schema design** — `InternalCompatibleSchemaGenerator` and `ExternalCompatibleSchemaGenerator` (`compatibility.py:256,260`) produce different outputs from the same model; the internal schema drives property synthesis, the external schema is the published spec.
3. **Schema layer removal fragility** — `remove_layer()` in `compatibility.py` has a documented TODO at line 192 about `min_length`/`max_length` merging. This is a known fragility.
4. **f-string bug** — `versioning_types.py:31`: `ValueError` message uses `{OPENTRACKIO_PROTOCOL_NAME}` in a plain string (not an f-string); error message prints literal braces rather than the value.
5. **`__ALL__` typo** — `units.py`: `__ALL__` should be `__all__`; `from camdkit.units import *` will not export unit constants.
6. **Non-deterministic examples** — `examples.py` calls `uuid4()` on every run; regression tests must normalize UUIDs for comparison (PROTO-EX-005 gap).

## Work Required

### Must Fix
1. f-string bug in error message (`versioning_types.py:31`) — PROTO-CORE-007 (error message only, not the validation itself)
2. `__ALL__` typo in `units.py` — cosmetic but breaks `import *`

### Should Fix
3. PROTO-EX-005 — deterministic UUID in examples for clean regression comparison

### Nice to Have
4. Document the `remove_layer()` fragility (TODO at `compatibility.py:192`) with a regression test before any schema surgery changes
