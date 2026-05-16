# Protocol Envelope Specs

## Clip Model

- [x] **PROTO-CORE-001**: The system shall synthesize `Clip` property accessors from `json_schema_extra` `clip_property` paths at class definition time, without hand-coded per-property accessor code.
- [x] **PROTO-CORE-002**: `Clip.to_json()` shall serialize to a JSON-compatible dict excluding all fields set to their default values (compact wire format).
- [x] **PROTO-CORE-003**: `Clip.append(other)` shall concatenate the dynamic tuple fields of `other` onto `self`, growing each per-frame tuple by one entry.
- [x] **PROTO-CORE-004**: When a `Clip` is indexed with `clip[i]`, the system shall return a new single-frame `Clip` containing the data at frame index `i`.
- [x] **PROTO-CORE-005**: `Clip.make_json_schema()` shall produce a self-contained JSON Schema document with all `$ref` pointers inlined.
- [x] **PROTO-CORE-006**: The external schema generator shall strip Pydantic-internal wrapping layers (default, anyOf-for-None, tuple) from the published OpenTrackIO schema.
- [x] **PROTO-CORE-007**: When `VersionedProtocol` is constructed with a `name` value other than `"OpenTrackIO"`, the system shall raise `ValueError`.
- [x] **PROTO-CORE-008**: `guess_fps(fps)` shall convert approximate float FPS values to exact `Fraction` rationals for known broadcast frame rates (24, 25, 30, 60 and their NTSC drop-frame equivalents) within a 1% tolerance.
- [x] **PROTO-CORE-009**: If `guess_fps(fps)` receives a non-integer, non-rational float that does not match any known frame rate within 1% tolerance, the system shall raise `ValueError`.
- [x] **PROTO-CORE-010**: If `guess_fps(fps)` receives a value that is not a `numbers.Real`, the system shall raise `TypeError`.

## Schema Compatibility

- [x] **PROTO-SCHEMA-001**: The internal schema generator shall retain `clip_property` metadata in the schema (used for property accessor synthesis).
- [x] **PROTO-SCHEMA-002**: The external schema generator shall strip `clip_property` metadata from the published schema.
- [x] **PROTO-SCHEMA-003**: The schema generator shall resolve all JSON Schema `$ref` pointers via `jsonref` before returning the schema document.
- [x] **PROTO-SCHEMA-004**: `CompatibleBaseModel` subclasses shall forbid extra fields during validation.
- [x] **PROTO-SCHEMA-005**: `CompatibleBaseModel` subclasses shall validate field assignments after construction.

## Examples

- [x] **PROTO-EX-001**: The system shall provide a recommended static example `Clip` with minimal required fields populated.
- [x] **PROTO-EX-002**: The system shall provide a complete static example `Clip` with all documented static fields populated.
- [x] **PROTO-EX-003**: The system shall provide a recommended dynamic example `Clip` with minimal per-frame fields populated.
- [x] **PROTO-EX-004**: The system shall provide a complete dynamic example `Clip` with all documented dynamic fields populated, including PTP synchronization.
- [ ] **PROTO-EX-005**: When generating example JSON for schema validation, the system shall use a stable deterministic UUID rather than a random `uuid4()` to enable regression comparison without UUID normalization.
