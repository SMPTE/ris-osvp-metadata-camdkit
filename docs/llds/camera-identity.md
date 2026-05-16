# Camera Identity

## Context and Design Philosophy

Camera Identity captures the static, hardware-level description of the capture device: who made it, what model it is, what sensor it has, what lens is attached, and what tracker is recording its position. These fields describe facts that do not change frame-to-frame — they are set once for a recording and stay constant.

The cluster spans three Pydantic models — `StaticCamera`, `StaticLens`, and `StaticTracker` — which map to the `clip.static.camera`, `clip.static.lens`, and `clip.static.tracker` sub-objects in the serialized `Clip`. All fields are optional in the schema; there is no required minimum set of device metadata.

**File boundary note:** `StaticCamera` lives in `camera_types.py` (owned entirely by this cluster). `StaticLens` lives in `lens_types.py` and `StaticTracker` lives in `tracker_types.py` — both files are owned by the Optical Characteristics and Spatial Tracking clusters respectively, because those files contain predominantly dynamic types. Camera Identity references the static sub-classes across that boundary.

## StaticCamera

`StaticCamera` (`camera_types.py`) is the primary hardware descriptor for the camera body.

### Fields

| Field | Type | Units | Notes |
|---|---|---|---|
| `make` | `NonBlankUTF8String` | — | Manufacturer name |
| `model` | `NonBlankUTF8String` | — | Camera model name |
| `serial_number` | `NonBlankUTF8String` | — | Body serial number |
| `firmware_version` | `NonBlankUTF8String` | — | Firmware version string |
| `label` | `NonBlankUTF8String` | — | User-assigned label (e.g. "A-cam") |
| `capture_frame_rate` | `StrictlyPositiveRational` | Hz | Frames per second as exact rational |
| `active_sensor_physical_dimensions` | `PhysicalDimensions` | mm | Active sensor area height × width |
| `active_sensor_resolution` | `SenselDimensions` | pixel | Active sensor photosites height × width |
| `iso` | `StrictlyPositiveInt` | — | ISO sensitivity |
| `fdl_link` | `UUIDURN` | — | UUID URN referencing an ASC FDL file |
| `shutter_angle` | `ShutterAngle` | degree | Shutter angle [0.0, 360.0] |
| `anamorphic_squeeze` | `StrictlyPositiveRational` | — | Horizontal squeeze factor (1.0 = spherical) |

All fields are optional. The `@field_validator` on `capture_frame_rate` and `anamorphic_squeeze` auto-coerces inputs to `StrictlyPositiveRational` before validation, accepting ints, `Rational` objects, or `{"num": n, "denom": d}` dicts.

### Dimension types

Two separate dimension types exist rather than a generic `Dimension[T]`:

- `PhysicalDimensions` — `height: float`, `width: float`, both ≥ 0, in millimeters. Represents the physical size of the active sensor area.
- `SenselDimensions` — `height: int`, `width: int`, both in `[0, MAX_INT_32]`, in pixels. Represents the photosite resolution.

Both override Pydantic's `__init__` to accept positional arguments (camdkit 0.9 legacy, consistent with all other domain types).

### ShutterAngle

`ShutterAngle` is a type alias (`Annotated[float, Field(ge=0.0, le=360.0)]`) rather than a class. It appears as a field on `StaticCamera` — stored as a static value in the `Clip`. Some camera readers (ARRI, RED, BMD, Canon, Venice) populate `shutter_angle` from per-clip metadata even though individual frames could in principle have different shutter angles. There is no per-frame shutter angle field in the current model.

## StaticLens

`StaticLens` (in `lens_types.py`) captures the optical hardware identity of the attached lens.

### Fields

| Field | Type | Units | Notes |
|---|---|---|---|
| `make` | `NonBlankUTF8String` | — | Lens manufacturer |
| `model` | `NonBlankUTF8String` | — | Lens model name |
| `serial_number` | `NonBlankUTF8String` | — | Lens serial number |
| `firmware_version` | `NonBlankUTF8String` | — | Lens firmware |
| `nominal_focal_length` | `StrictlyPositiveInt` | mm | Marked focal length of lens |
| `calibration_history` | `tuple[NonBlankUTF8String, ...]` | — | Ordered list of calibration event descriptions |
| `overscan_percent` | `UnityOrGreaterFloat` | — | Minimum overscan factor required by this lens (≥ 1.0) |

`nominal_focal_length` is the prime or zoom label on the lens body (e.g. 50mm), distinct from the computed `pinhole_focal_length` in per-frame optical data. `calibration_history` is unbounded in length; individual strings are capped at 1023 chars.

## StaticTracker

`StaticTracker` (in `tracker_types.py`) captures the hardware identity of the tracking device.

### Fields

| Field | Type | Notes |
|---|---|---|
| `make` | `NonBlankUTF8String` | Tracker manufacturer |
| `model` | `NonBlankUTF8String` | Tracker model |
| `serial_number` | `NonBlankUTF8String` | Tracker serial number |
| `firmware_version` | `NonBlankUTF8String` | Tracker firmware |

All fields are optional strings with 1–1023 char constraint.

## How Readers Populate Camera Identity

All six readers set camera identity fields from their proprietary source format:

| Field | ARRI | BMD | Canon | MoSys | RED | Venice |
|---|---|---|---|---|---|---|
| `camera_make` | CSV | "Blackmagic" | "Canon" | — | CSV | XML |
| `camera_model` | CSV | CSV | — | — | CSV | XML |
| `camera_serial_number` | CSV | CSV | — | — | CSV ("PIN") | XML |
| `camera_firmware` | — | CSV | — | — | CSV | XML |
| `lens_make` | — | — | — | — | CSV | XML |
| `lens_model` | — | CSV | — | — | CSV | XML |
| `lens_serial_number` | — | — | — | — | CSV | XML (✓) |
| `lens_nominal_focal_length` | CSV | CSV | CSV | — | CSV | CSV |
| `capture_frame_rate` | CSV | CSV | ⚠ unsupported | F4 packet | CSV | XML |
| `active_sensor_physical_dimensions` | computed (pixel pitch map) | computed (hardcoded) | ⚠ unsupported | assumed 36×24mm | computed (pixel pitch map) | computed (pixel pitch × resolution) |

**Sensor dimension strategy:** No reader receives physical dimensions directly from the camera. Instead, readers compute sensor dimensions from a combination of pixel pitch (a hardware constant per sensor model) and resolution:
- ARRI and RED: `_CAMERA_FAMILY_PIXEL_PITCH_MAP` / `_LENS_NAME_PIXEL_PITCH_MAP` — lookup tables keyed on camera/sensor model string.
- BMD: hardcoded only for "Blackmagic URSA Mini Pro 12K".
- Venice: hardcoded pixel pitch (22800/3840 µm per pixel), scaled by resolution.
- MoSys: hardcoded assumption of 35mm full-frame (36×24mm) in `f4.py`.
- Canon: not implemented (comment at reader line 53).

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| Static device metadata as nested sub-objects | `Clip.Static.camera`, `Clip.Static.lens`, `Clip.Static.tracker` | Flat fields on `Clip` | [inferred] Groups related fields; mirrors the spec document structure; reduces top-level Clip field count |
| Generic `Dimension[T]` | Rejected — two separate classes (`PhysicalDimensions`, `SenselDimensions`) | `Dimension[float]` / `Dimension[int]` | Explicit: Pydantic v2 `Field` annotation incompatibility with generic type parameters (documented comment at `camera_types.py:25`) |
| `shutter_angle` as static, not per-frame | Field on `StaticCamera` | Per-frame tuple field | [inferred] Most camera sources provide a single shutter angle per clip; per-frame shutter is not in the spec |
| Pixel pitch lookup tables per reader | Hardcoded maps keyed on camera model string | Receive physical dims from camera, or user-supplied | [inferred] Camera manufacturer protocols do not expose physical sensor dimensions directly; lookup tables are the only practical approach |
| All static fields optional | No required fields on `StaticCamera`, `StaticLens`, `StaticTracker` | Require make+model minimum | [inferred] Different readers support different subsets; a required minimum would make many real clips invalid |
| Positional `__init__` constructors | Override Pydantic's keyword-only default | Keyword-only | Explicit: camdkit 0.9 API compatibility |

## Open Questions & Future Decisions

### Resolved
1. ✅ Whether to keep static device metadata separate from dynamic per-frame data — yes, `Clip.Static` nesting established in 1.0.0 rewrite

### Deferred
1. ARRI, RED, and Venice sensor dimension lookup tables are hardcoded per camera/sensor model. When new camera bodies are released, these tables require manual updates. No mechanism exists to extend them without a code change.
2. BMD reader only supports "Blackmagic URSA Mini Pro 12K" for sensor dimension computation. All other BMD bodies will produce a `Clip` with no `active_sensor_physical_dimensions`.
3. MoSys F4 reader assumes 35mm full-frame (36×24mm) regardless of actual camera body. This is hardcoded in `f4.py:287`.
4. Canon reader does not populate `capture_frame_rate` or `active_sensor_physical_dimensions` (comments at `canon/reader.py:53`).
5. No tracker identity fields (make, model, serial) are populated by any reader other than implicitly through MoSys F4 protocol data.
6. `StaticLens` and `StaticTracker` live in `lens_types.py` and `tracker_types.py` respectively — files primarily owned by Optical Characteristics and Spatial Tracking. This is a file-boundary awkwardness only; no runtime coupling issue.

## References

- Files owned by this cluster:
  - `src/main/python/camdkit/camera_types.py` (all of it)
- Files cross-referenced (static sub-classes only):
  - `src/main/python/camdkit/lens_types.py` → `StaticLens`
  - `src/main/python/camdkit/tracker_types.py` → `StaticTracker`
- Dependencies on other clusters:
  - Protocol Envelope: `CompatibleBaseModel`, `NonBlankUTF8String`, `UUIDURN`, `StrictlyPositiveRational`, `StrictlyPositiveInt`, `UnityOrGreaterFloat`, `units`
- Populated by: all six Format Bridge readers (ARRI, BMD, Canon, MoSys, RED, Venice)
- External dependencies: `pydantic`, `fractions`
