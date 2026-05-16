# Optical Characteristics

## Context and Design Philosophy

Optical Characteristics covers the per-frame state of the lens: its distortion profile, focus and iris positions (both normalized and raw), exposure falloff, focal length, and the geometric offsets that relate the lens's optical axis to the camera's coordinate frame.

These are dynamic fields — one value per sample — stored as tuples in `Clip`. They are the primary data consumed by VFX compositing and virtual production pipelines to project CGI into the real camera's optical model.

The cluster is anchored in `lens_types.py`, which owns all dynamic lens Pydantic models. `StaticLens` (hardware identity) also lives in this file but is logically owned by the Camera Identity cluster.

## Dynamic Lens Fields on Clip

The `Lens` class (`lens_types.py`) is the per-frame container. All fields are optional; a `Clip` may populate any subset.

| Field | Type | Units | Notes |
|---|---|---|---|
| `distortions` | `tuple[Distortion, ...]` (≥ 1) | — | One or more distortion models for this frame |
| `distortion_offset` | `DistortionOffset` | — | 2D offset of distortion center from image center |
| `projection_offset` | `ProjectionOffset` | — | 2D offset of projection center from image center |
| `encoders` | `FizEncoders` | normalized [0,1] | Focus / iris / zoom encoder readings |
| `raw_encoders` | `RawFizEncoders` | integer | Raw (uncalibrated) FIZ encoder readings |
| `f_number` | `StrictlyPositiveFloat` | — | Aperture as f-stop |
| `t_number` | `StrictlyPositiveFloat` | — | Aperture as T-stop (calibrated) |
| `focal_length` | `StrictlyPositiveFloat` | mm | Pinhole focal length (computed, not the marked label) |
| `focus_distance` | `StrictlyPositiveFloat` | m | Focus distance |
| `entrance_pupil_offset` | `StrictlyPositiveFloat` | m | Nodal point offset from origin |
| `exposure_falloff` | `ExposureFalloff` | — | Vignetting coefficients {a1, a2, a3} |
| `custom` | `NonBlankUTF8String` | — | Vendor-specific extension payload |

### Focal length naming

`focal_length` on `Lens` is the **computed pinhole equivalent focal length** — it changes per-frame as zoom/focus breathe. It was renamed from `focal_length` to `pinhole_focal_length` in the 1.0.0 release (CHANGELOG). The current field name in the Pydantic model is `focal_length` with JSON alias `pinholeFocalLength`. This is distinct from `StaticLens.nominal_focal_length`, which is the marked prime/zoom label.

## Distortion Model

`Distortion` represents a single lens distortion model.

```
Distortion:
  model: str                        # default "Brown-Conrady D-U"
  radial: tuple[float, ...]         # min_length=1; Brown-Conrady k1..kN coefficients
  tangential: tuple[float, ...] | None   # p1, p2 tangential coefficients
  overscan: float (≥ 1.0) | None    # minimum overscan required by this distortion
```

`distortions` on `Lens` is `tuple[Distortion, ...]` — a frame can carry more than one distortion model simultaneously (e.g., when both a Brown-Conrady and a custom model are valid for the same frame). The tuple must have at least one entry.

`Distortion.check_tuples_not_empty()` is a model validator that explicitly rejects empty `radial` tuples. This is redundant with `min_length=1` on the `Field`, but is explicit belt-and-suspenders.

## Encoder Types

### FizEncoders (normalized)

Normalized focus/iris/zoom in `[0.0, 1.0]`. All three fields are optional; at least one must be present at construction time. The "at least one" constraint is enforced in a custom `__init__` override because Pydantic v2 has no built-in constraint for "at least one of these optional fields must be non-None."

### RawFizEncoders (integer)

Uncalibrated raw encoder counts as integers. Same "at least one" constraint, same custom `__init__` enforcement pattern.

Both encoder types use camelCase JSON aliases (`focusPosition`, `irisPosition`, `zoomPosition`).

## Geometric Offsets

Two planar offset types exist, both inheriting from `PlanarOffset` (`{x: float, y: float}`):

- `DistortionOffset` — offset of the distortion center from the image center
- `ProjectionOffset` — offset of the projection (principal point) from the image center

The two subclasses are structurally identical — no additional fields or validators. The distinction is purely semantic: they describe different optical phenomena that happen to both be 2D offsets.

## Exposure Falloff

`ExposureFalloff` holds three vignetting polynomial coefficients: `a1`, `a2`, `a3`. These model the radial light falloff from the lens center. No model equation is documented in the code; the field names and interpretation are defined by the OpenTrackIO spec.

## Cooke Lens Protocol (RED reader)

`red/cooke.py` parses Cooke `/i` lens metadata embedded in RED camera files. This is the only reader that provides entrance pupil position and uses a calibrated aperture value from the lens itself rather than the camera body.

Two dataclasses:
- `CookeLensData` — `entrance_pupil_position` (signed, 14-bit), `aperture_value` (12-bit, unsigned)
- `CookeFixedData` — `firmware_version_number` (string at bytes 61–65)

Extraction is pure bitwise arithmetic against hardcoded byte and bit offsets from the Cooke `/i` format specification. No validation or error handling — malformed data produces wrong values silently.

`entrance_pupil_position` sign is encoded as bit 5 of byte 25; magnitude spans bits 0–9 across bytes 25–26. `aperture_value` is 12 bits across bytes 5–6.

## Reader Coverage for Optical Data

| Field | ARRI | BMD | Canon | MoSys | RED | Venice |
|---|---|---|---|---|---|---|
| `t_number` | ✓ (from linear iris) | ✓ | ✓ (aperture mode 2) | — | ✓ (Cooke) | ✓ (fractional stop string) |
| `f_number` | — | — | ✓ (aperture mode 1) | ✓ | — | — |
| `focus_distance` | ✓ (m) | ✓ | ✓ (hex float) | ✓ | ✓ | ✓ (ft→mm→m) |
| `encoders` (normalized FIZ) | — | — | — | ✓ | — | — |
| `distortions` | — | — | — | ✓ | — | — |
| `projection_offset` | — | — | — | ✓ | — | — |
| `entrance_pupil_offset` | ⚠ TODO | — | ⚠ unsupported | ✓ (F4 field 0x3E) | ✓ (Cooke) | ⚠ TODO |
| `focal_length` (pinhole) | — | — | — | ✓ | — | — |

### T-stop / f-stop sourcing strategies per reader

- **ARRI** — `t_number_from_linear_iris_value()`: converts a linear iris integer from the CSV using a lookup against standard T-stop values. The function is exported and independently tested.
- **BMD** — T-stop read directly from "T-Stop" key in the metadata text; focus and focal length extraction has an indentation bug (lines 112–123 are inside the `if shutter_value is not None:` block, meaning they're only extracted when shutter data is present).
- **Canon** — Mode-dependent: `ApertureMode == 2` → `t_number`, `ApertureMode == 1` → `f_number`. Focus distance decoded from a float32 hex string using `struct.unpack`.
- **MoSys** — F4 binary field IDs: `0x2E` (f-number), `0x2F` (focus distance), `0x3E` (entrance pupil), `0x3C` (focal length), plus FIZ encoder axes by axis ID.
- **RED** — T-stop from Cooke `aperture_value` (12-bit), scaled. Focus distance from "Focus Distance" CSV column.
- **Venice** — T-stop parsed from strings like `"T 2"`, `"T 2.8"`, `"T 2 3/10"` via regex; computed as `2^(aperture/2)`. Focus distance converted from feet to mm.

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| `distortions` as tuple (multiple models per frame) | `tuple[Distortion, ...]` with min_length=1 | Single `Distortion` field | [inferred] Some workflows need to carry multiple calibrated distortion models simultaneously (e.g., for different downstream pipelines) |
| Separate `DistortionOffset` and `ProjectionOffset` subclasses | Two semantically distinct classes, both subclass `PlanarOffset` | Single `PlanarOffset` type used for both | [inferred] Future-proofing — the two offsets may diverge (add metadata fields); semantic distinction aids documentation generation |
| Normalized vs raw encoders as separate fields | `FizEncoders` (normalized) and `RawFizEncoders` (raw integer) | Single encoder type with a flag | [inferred] Both are useful: normalized for interop, raw for round-tripping to the original device |
| "At least one" FIZ field enforced in `__init__` | Custom `__init__` override | Pydantic `model_validator` | [inferred] Pydantic v2 has no native "at least one optional field must be present" constraint; `__init__` override is the clearest expression |
| Cooke data parsed in `red/cooke.py` separately | Standalone module `CookeLensData` + `CookeFixedData` dataclasses | Inline in `red/reader.py` | [inferred] Cooke `/i` is a published third-party protocol; separating it allows independent testing and potential reuse by other readers |
| `focal_length` → `pinholeFocalLength` JSON alias | Renamed in 1.0.0 | Keep `focalLength` | Explicit: CHANGELOG notes semantic clarification — "pinhole" distinguishes computed from marked focal length |
| `ExposureFalloff` as {a1, a2, a3} | Three named coefficients | Array of N coefficients | [inferred] Fixed-degree polynomial is sufficient for typical vignetting; named fields are clearer in schema documentation |

## Open Questions & Future Decisions

### Resolved
1. ✅ `focal_length` renamed to `pinholeFocalLength` in 1.0.0 to distinguish from `nominal_focal_length`

### Deferred
1. ARRI reader: entrance pupil position not implemented (TODO comment in `arri/reader.py`). ARRI CSV contains the field; parsing is just not wired up.
2. Venice reader: entrance pupil offset not implemented (TODO at `venice/reader.py:200`).
3. Canon reader: entrance pupil offset explicitly marked unsupported (comment at `canon/reader.py:72`).
4. BMD reader: indentation error at lines 112–123 causes focal length, focus position, and T-number extraction to only occur when shutter data is present. This is a logic bug, not a missing feature.
5. Cooke parser (`red/cooke.py`): no validation or error handling — malformed input produces wrong values silently. Binary offsets are hardcoded with no reference to which version of the Cooke `/i` spec they target.
6. `ExposureFalloff` coefficients `{a1, a2, a3}` — the polynomial model and normalization conventions are not documented in code; defer to spec document for interpretation.
7. `PlanarOffset` base class with two identical subclasses: if `DistortionOffset` and `ProjectionOffset` never diverge structurally, the inheritance hierarchy adds complexity for no gain. Evaluate at next major schema revision.

## References

- Files owned by this cluster:
  - `src/main/python/camdkit/lens_types.py` (dynamic classes: `Distortion`, `Distortions`, `PlanarOffset`, `DistortionOffset`, `ProjectionOffset`, `FizEncoders`, `RawFizEncoders`, `ExposureFalloff`, `Lens`)
  - `src/main/python/camdkit/red/cooke.py`
- Files cross-referenced (static sub-class only):
  - `src/main/python/camdkit/lens_types.py` → `StaticLens` (owned by Camera Identity)
- Dependencies on other clusters:
  - Protocol Envelope: `CompatibleBaseModel`, `NonBlankUTF8String`, `StrictlyPositiveFloat`, `NormalizedFloat`, `NonNegativeInt`, `UnityOrGreaterFloat`, `NonNegativeFloat`, `units`
- Populated by: ARRI reader (T-stop, focus), BMD reader (T-stop, focus), Canon reader (T/f-stop, focus), MoSys reader (FIZ encoders, distortion, projection offset, focal length, f-number), RED reader (T-stop + Cooke entrance pupil), Venice reader (T-stop, focus)
- External dependencies: `pydantic`, `dataclasses`, `struct` (Canon reader)
