# Protocol Envelope

## Context and Design Philosophy

The Protocol Envelope is the structural center of camdkit. It defines the `Clip` — the canonical container for all OpenTrackIO metadata — and the infrastructure that governs how that container is validated, serialized, and published as a JSON Schema.

The guiding principle is **schema-driven design**: the shape of `Clip`, its properties, their units, sampling modes, and documentation are all declared once in Pydantic field metadata (`json_schema_extra`), and everything downstream — property accessors, JSON serialization, schema export, documentation generation — is derived from that declaration. No hand-coding of accessors; no parallel data structures.

A second principle is **compatibility-first schema export**: the JSON Schema emitted to consumers strips Pydantic's internal layers (defaults, anyOf-for-None, title fields) to produce a clean, spec-aligned document that matches the OpenTrackIO 0.9 / 1.x specification format.

## The Clip Model

`Clip` (`src/main/python/camdkit/clip.py`) is the central data model. It holds all metadata for a recorded clip or a stream of tracking frames.

### Static vs. dynamic fields

Fields are divided into two kinds:

- **Static** — singleton values that describe the recording as a whole (camera make, sensor size, protocol version). Stored directly on `Clip` or on `Clip.Static` sub-objects.
- **Dynamic** — per-frame tuples (one entry per sample). Examples: `lens_t_number`, `timing_timecode`, `transforms`. Stored as `tuple[T, ...]` fields.

This tuple-based design allows a single `Clip` object to represent either a single frame (tuple of length 1) or a complete multi-frame recording (tuple of length N), without a separate container class.

### Metaprogramming-driven accessors

`Clip` does not hand-code its property accessors. Instead, `Clip.setup_clip_properties()` (called at class definition time, line 315) traverses the Pydantic JSON schema via `Clip.traverse_json_schema()` and synthesizes `@property` accessors on the fly using `setattr()`.

Each synthesized property is backed by a `clip_property` entry in a field's `json_schema_extra` — a `tuple[str, ...]` path that describes where the property lives in the nested model (e.g., `("static", "camera", "capture_frame_rate")`). The traversal finds all such entries and creates accessors that route reads and writes through the nested path.

This means adding a new field to the spec requires only:
1. Adding a Pydantic field with correct `json_schema_extra` (including `clip_property` path)
2. No accessor code; the framework synthesizes it

### Frame operations

- `clip.append(other_clip)` — concatenates dynamic tuple fields from `other_clip` onto `self`. Used to build multi-frame clips from per-frame reads (see MoSys reader).
- `clip[i]` (`__getitem__`) — extracts frame `i` as a new single-frame `Clip`.
- `clip.to_json()` — serializes to a JSON-compatible dict, excluding fields set to their defaults (compact wire format).

## Schema Generation and Compatibility Layer

`compatibility.py` provides two coupled responsibilities:

### CompatibleBaseModel

All camdkit domain types inherit from `CompatibleBaseModel` rather than Pydantic's `BaseModel`. This configures:
- `populate_by_name=True` — allow both alias and Python name for construction
- `validate_assignment=True` — validate on every field write
- `use_enum_values=True` — store enum values not members
- `extra='forbid'` — reject unknown fields
- `use_attribute_docstrings=True` — use field docstrings for schema descriptions

It also adds class-level `validate()`, `to_json()`, `from_json()`, and `make_json_schema()` methods.

### Schema surgery

Pydantic v2's generated JSON Schema is verbose and internal. `CompatibleSchemaGenerator` post-processes it:

1. **Ref resolution** — calls `jsonref.replace_refs()` to inline all `$ref` pointers, producing a self-contained schema document.
2. **Layer removal** — `model_field_schema()` strips Pydantic-internal wrapping layers:
   - `default` layer (the outermost wrapper when a field has a default) → unwrapped to the inner schema
   - `nullable` / `anyOf` layer (Pydantic's `Optional[T]` encoding) → unwrapped to `T`
   - `tuple` layer (Pydantic's encoding of `tuple[T, ...]`) → unwrapped to array schema for the element type
   
   This produces a schema that says `{"type": "array", "items": {...}}` rather than Pydantic's layered internal representation.

3. **Two schema modes** — `InternalCompatibleSchemaGenerator` retains `clip_property` metadata (used by `setup_clip_properties()`). `ExternalCompatibleSchemaGenerator` strips it (used for the published OpenTrackIO schema).

### Description canonicalization

`canonicalize_descriptions()` ensures field descriptions comply with PEP 257 single-newline rules before schema export.

## Public API Facades

`framework.py` and `model.py` are thin re-export modules. They exist to:
- Flatten the import surface (`from camdkit.model import Clip, Dimensions` rather than importing from four sub-modules)
- Apply public-facing name aliases (e.g., `SenselDimensions` is exported as `Dimensions`)
- Provide a stable public API even if internal module structure changes

`framework.py` focuses on type re-exports. `model.py` adds `Clip` and a second set of namespace-prefixed aliases (e.g., `LensEncoders`, `TimingTimecode`).

## Versioning

`versioning_types.py` defines `VersionedProtocol` with `name` ("OpenTrackIO") and `version` (3-tuple of single-digit ints). The current version is `(1, 0, 1)`. The constructor enforces that `name == "OpenTrackIO"` — only one protocol is supported.

`OPENTRACKIO_PROTOCOL_NAME` and `OPENTRACKIO_PROTOCOL_VERSION` constants are re-exported through `framework.py` and `model.py`.

## Primitive Foundation

The following modules underpin all domain types in the codebase:

| Module | Role |
|---|---|
| `numeric_types.py` | Constrained int/float types (`NonNegativeInt`, `StrictlyPositiveRational`, etc.) and `Rational`/`StrictlyPositiveRational` model classes |
| `string_types.py` | `NonBlankUTF8String` (1–1023 chars) and `UUIDURN` (RFC 4122 pattern) |
| `units.py` | String constants for unit annotations used in `json_schema_extra` |
| `utils.py` | `guess_fps(fps)` — converts approximate float FPS to exact `Fraction` (handles 23.98→24000/1001, etc.) |

These are owned by Protocol Envelope because they have no domain-specific knowledge — they are pure infrastructure used by every cluster.

## Examples

`examples.py` provides four canonical `Clip` instances:

| Function | Description |
|---|---|
| `get_recommended_static_example()` | Minimal static metadata (required fields only) |
| `get_complete_static_example()` | All static fields populated |
| `get_recommended_dynamic_example()` | Minimal per-frame data |
| `get_complete_dynamic_example()` | All dynamic fields populated, including PTP sync |

These serve two purposes: regression testing (compared against committed JSON files) and documentation (rendered in the HTML output). They are also the primary consumers of `_unwrap_clip_to_pseudo_frame()`, which extracts a single-frame view for use in schema validation tests.

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| Schema-driven property synthesis | `setup_clip_properties()` + `traverse_json_schema()` at class definition time | Hand-coded properties per field | [inferred] Reduces maintenance burden when spec adds new fields; properties stay in sync with schema automatically |
| Tuple-based multi-frame storage | `tuple[T, ...]` per dynamic field | List, separate `Frame` container class, separate `Clip` + `ClipStream` | [inferred] Tuples are immutable (safe default for value semantics); avoids a second container class; append semantics are explicit |
| Single `Clip` for both static and multi-frame | `Clip.Static` nested inside `Clip` | Separate `StaticClip` and `DynamicClip` | [inferred] Consumers always get one object; no type branching at call sites |
| Schema layer removal in `CompatibleSchemaGenerator` | Strip Pydantic-internal wrapping (default, anyOf, tuple layers) | Accept Pydantic output as-is; use a custom Pydantic plugin | [inferred] Classic camdkit 0.9 schema format predates Pydantic rewrite; consumers depend on that format |
| Inline all `$ref` via `jsonref` | Fully self-contained schema document | Keep `$ref` pointers | [inferred] OpenTrackIO schema is distributed as a single file; external $ref resolution is not guaranteed for all consumers |
| Two schema generators (internal vs external) | `InternalCompatibleSchemaGenerator` (retains `clip_property`) / `ExternalCompatibleSchemaGenerator` (strips it) | Single generator with a mode flag | [inferred] Keeps the property synthesis machinery separate from the published spec schema |
| `CompatibleBaseModel` for all domain types | Shared base with custom config | Per-class Pydantic `model_config` | [inferred] Ensures uniform serialization and validation behavior across all 10+ domain type modules |
| Positional `__init__` constructors | Override Pydantic's keyword-only constructors | Keyword-only (Pydantic default) | Explicit: camdkit 0.9 compatibility — existing call sites use positional args |

## Open Questions & Future Decisions

### Resolved
1. ✅ Whether to use Pydantic v2 — yes, full rewrite in 1.0.0 (49 files, 2953 del, 7461 add per CHANGELOG)

### Deferred
1. Schema layer merge hazard: `remove_layer()` has a known fragility when merging `min_length`/`max_length` constraints across layers (TODO comment at `compatibility.py:192`). Needs a regression test before any schema surgery changes.
2. `examples.py` uses hardcoded index-[0] unwrapping paths to convert multi-frame clips to single-frame pseudo-frames. This is noted as brittle to schema changes — evaluate replacing with a generic frame-index approach.
3. `versioning_types.py:31` — f-string bug: error message in constructor uses `{OPENTRACKIO_PROTOCOL_NAME}` inside a plain string, not an f-string. Message would print literally rather than interpolating the constant.
4. `units.py` — `__ALL__` typo (should be `__all__`); `METERS_AND_DEGREES` flagged as a "confusing non-unit" with a TODO to remove in favor of separate unit strings.

## References

- Files in this cluster:
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
- Dependencies on other clusters: all domain type clusters depend on this cluster's `CompatibleBaseModel`, `numeric_types`, `string_types`, `units`; Format Bridge readers produce `Clip` instances defined here
- External dependencies: `pydantic`, `pydantic_core`, `jsonref`, `fractions`, `uuid`, `copy`
