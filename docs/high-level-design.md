# camdkit — High-Level Design

## System Purpose

camdkit is a Python library that defines the canonical **OpenTrackIO metadata model** for broadcast camera tracking. It provides: (1) a schema-driven `Clip` container that holds all camera, lens, tracker, and timing metadata for a recording; (2) adapters that convert proprietary camera file formats into `Clip` objects; (3) the authoritative JSON Schema for the OpenTrackIO wire format; and (4) reference documentation and example data. It is the reference implementation of the SMPTE RIS OSVP camera metadata specification.

## Architecture Overview

The system has two orthogonal structures: a **dependency hierarchy** (what imports what) and a **data flow** (how data moves through the system at runtime).

### Dependency Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  Format Bridge                    Spatial Tracking (MoSys)  │
│  ARRI │ BMD │ Canon │ RED │Venice  F4 binary protocol       │
└──────────────────────┬────────────────────┬─────────────────┘
                       │  to_clip() → Clip  │
                       ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  Protocol Envelope — Clip                                   │
│  Schema-driven property synthesis · Serialization           │
│  Public API (framework.py, model.py)                        │
└──────┬──────────────┬───────────────┬──────────────┬────────┘
       │              │               │              │
       ▼              ▼               ▼              ▼
┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────────┐
│ Camera   │  │ Optical      │  │ Temporal │  │ Spatial      │
│ Identity │  │ Charact.     │  │ Sync     │  │ Tracking     │
│          │  │              │  │          │  │ (types only) │
└──────────┘  └──────────────┘  └──────────┘  └──────────────┘
       │              │               │              │
       └──────────────┴───────────────┴──────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Protocol Envelope — Foundation                             │
│  CompatibleBaseModel · numeric_types · string_types         │
│  units · utils                                              │
└─────────────────────────────────────────────────────────────┘
```

### Runtime Data Flow

```
Proprietary files                    Live binary stream
(ARRI CSV, BMD text,                 (Mo-Sys F4 packets)
 Canon CSV, RED CSV,                        │
 Venice XML+CSV)                            │ F4PacketParser
       │                                    │ .get_tracking_frame()
       │ reader.to_clip()                   │
       ▼                                    ▼
       ┌────────────────────────────────────┐
       │             Clip                   │
       │  static.*   (singleton fields)     │
       │  dynamic.*  (tuple[T, ...] fields) │
       │                                    │
       │  .append(frame_clip) ──────────────┤ ← MoSys accumulation
       │  clip[i] ──────────────────────────┤ ← frame extraction
       └──────────────┬─────────────────────┘
                      │
          ┌───────────┴────────────────┐
          ▼                            ▼
  clip.to_json()              Clip.make_json_schema()
  OpenTrackIO JSON            JSON Schema document
  (wire format)               (published spec)
          │
          └──────────────────────────────┐
                                         ▼
                               examples.py → reference JSON
                               make_opentrackio_documentation.py
                               → HTML documentation site
```

## Domain Clusters

| Cluster | What it answers | Key types |
|---|---|---|
| **Protocol Envelope** | How is metadata structured and transmitted? | `Clip`, `CompatibleBaseModel`, `VersionedProtocol`, schema generators |
| **Camera Identity** | What device captured this? | `StaticCamera`, `StaticLens`, `StaticTracker` |
| **Optical Characteristics** | How does the lens behave per frame? | `Lens`, `Distortion`, `FizEncoders`, `ExposureFalloff` |
| **Spatial Tracking** | Where is the camera in 3D space? | `Transform`, `Vector3`, `Rotator3`, `Tracker`, `GlobalPosition` |
| **Temporal Synchronization** | When exactly did each sample occur? | `Timing`, `Timecode`, `Timestamp`, `Synchronization`, `SynchronizationPTP` |
| **Format Bridge** | How do proprietary formats map to `Clip`? | ARRI, BMD, Canon, RED, Venice readers |

## Cross-Cutting Concerns

### CompatibleBaseModel — universal base

Every domain type in the codebase inherits from `CompatibleBaseModel` rather than Pydantic's `BaseModel` directly. This provides uniform serialization behavior (`to_json`/`from_json`), consistent validation config (`validate_assignment=True`, `extra='forbid'`), and the custom JSON Schema generator that strips Pydantic's internal wrapping layers.

### json_schema_extra — connective tissue

All field definitions carry metadata in `json_schema_extra`:

```python
Field(..., json_schema_extra={
    "clip_property": ("static", "camera", "capture_frame_rate"),
    "units": HERTZ,
    "constraints": STRICTLY_POSITIVE_RATIONAL,
    "sampling": "static",
    "section": "camera",
})
```

This metadata drives three separate mechanisms: property accessor synthesis (via `clip_property` path), JSON Schema export (units, constraints, section), and documentation generation (all fields). It is the connective tissue that makes the schema-driven design work.

### Tuple semantics for dynamic data

Every per-frame field is `tuple[T, ...]`, never a list. This is enforced consistently across all domain type clusters. The tuple is the unit of per-frame data; `Clip.append()` concatenates tuples; `clip[i]` slices them. Lists are never stored; when Pydantic receives a list input for a tuple field, it coerces it.

### Positional `__init__` constructors

All domain type classes override Pydantic v2's keyword-only `__init__` to accept positional arguments. This is a cross-cutting camdkit 0.9 API compatibility constraint. Every `CompatibleBaseModel` subclass follows this pattern.

### guess_fps() for frame rate normalization

Camera metadata sources express frame rate as floating-point approximations (23.976, 29.97). `guess_fps()` converts these to exact rationals (24000/1001, 30000/1001) via fuzzy matching within 1%. Used by the ARRI and RED readers; should be used by any future reader that parses a floating-point frame rate.

### No shared error handling

The six readers use inconsistent error strategies:
- ARRI: `assert` (produces `AssertionError`, stripped by `-O`)
- RED, Venice: `raise ValueError(...)`
- BMD: `raise "string"` (produces `TypeError` — a bug)
- Canon, most: silent omission (unsupported fields simply not set)

There is no cross-cutting error handling pattern. Failures surface inconsistently to callers.

### No logging

No logging infrastructure exists anywhere in the library. Reader errors are either raised as exceptions or silently dropped. There is no way for a caller to distinguish "field not in source format" from "field parsing failed."

## Key Architectural Decisions

| Decision | What was chosen | Why it matters |
|---|---|---|
| **Schema-driven metaprogramming** | `Clip.setup_clip_properties()` synthesizes property accessors from `json_schema_extra` at class definition time | Adding a spec field requires only a Pydantic field declaration; no accessor code. The schema and the API stay in sync by construction |
| **Pydantic v2 rewrite** | Full rewrite in 1.0.0 (7,461 lines added) | Replaced bespoke validation with an industry-standard framework; enabled the two-schema design and `json_schema_extra` metadata pattern |
| **Two-schema design** | `InternalCompatibleSchemaGenerator` (retains `clip_property`) vs `ExternalCompatibleSchemaGenerator` (strips it) | Property synthesis machinery is invisible in the published schema; internal and external representations are cleanly separated |
| **Static + dynamic in one Clip** | `Clip.Static` (singletons) + tuple fields (per-frame) in one class | Consumers always receive one object; no type branching; append semantics are explicit |
| **No abstract reader base class** | Five standalone adapter modules | Zero shared parsing code between readers; an abstraction would be empty; the contract is enforced by tests |
| **Pixel pitch lookup tables** | Hardcoded per-reader maps for sensor dimension computation | Camera protocols do not transmit physical sensor dimensions; lookup tables are the only practical approach without manufacturer APIs |
| **Cooke /i for RED optical data** | `red/cooke.py` parses Cooke binary protocol for entrance pupil + T-stop | Cooke /i is the only file-based source of calibrated entrance pupil position and lens-side T-stop in the codebase |

## Shared Infrastructure

| Infrastructure | Details |
|---|---|
| **Pydantic v2** | Validation, serialization, JSON Schema generation for all domain types |
| **jsonref** | Inlines `$ref` pointers in the generated schema, producing a self-contained document |
| **hypothesis** | Property-based test generation for JSON roundtrip and schema agreement tests |
| **jsonschema** | Validates generated Clip JSON against the published schema in property tests |
| **jinja2** | Renders the OpenTrackIO HTML documentation from a template |
| **Test resources** | Real camera output files in `src/test/resources/` (ARRI, BMD, Canon, MoSys, RED, Venice) — one corpus file per reader |

No databases, message queues, caches, or network services are used at runtime. camdkit is a pure in-process library.

## Known Technical Debt (Cross-Cluster)

| Issue | Location | Severity |
|---|---|---|
| `raise "string"` bug | `bmd/reader.py:45` | High — crashes with wrong exception type |
| Indentation bug | `bmd/reader.py:112–123` | High — T-stop/focus silently dropped when no shutter key |
| `assert` instead of `ValueError` | `arri/reader.py:44` | Medium — stripped by `-O`, wrong error type |
| f-string bug in error message | `versioning_types.py:31` | Low — error message prints literal text instead of value |
| `__ALL__` typo | `units.py` | Low — `import *` won't export unit constants |
| Unused import | `transform_types.py:8` | Low — `DefaultContext` import is dead code |
| Commented-out units in schema | `transform_types.py:22,34` | Low — unclear if intentional omission |
| Hardcoded 36×24mm sensor | `mosys/f4.py:287` | Medium — wrong for non-35mm rigs |
| `nanoseconds` no upper bound | `timing_types.py` | Medium — accepts values > 999,999,999 |
| `domain` allows 128–255 | `timing_types.py` | Low — out-of-spec for most PTP profiles |

## Non-Goals

camdkit explicitly does **not**:
- Transmit data over a network (no UDP, TCP, WebSocket, or NMOS)
- Decode or process video frames
- Perform real-time tracking or IMU sensor fusion
- Calibrate camera or lens systems
- Control camera hardware
- Solve tracking (no bundle adjustment, no SLAM)
- Provide a storage format or database
- Support tracking data from systems other than Mo-Sys F4 (live) and the five supported camera file formats (file-based)

## Correctness Roadmap

`correctness-plan.md` defines a five-step path toward formal verification:

| Step | Status | Description |
|---|---|---|
| 1 | ✅ Complete | Hypothesis property tests: JSON roundtrip + schema agreement |
| 2 | Upcoming | Metamorphic tests (key order, numeric normalization, geometric identity) |
| 3 | Planned | Independent Python spec model + differential testing against camdkit |
| 4 | Planned | OpenCV↔OpenTrackIO projection differential tests |
| 5 | Long-term | Lean proof kernel through Layer D |

## References

- LLDs: `docs/llds/` (6 cluster-level design documents)
- Coordinate system derivation: `src/main/resources/res/OpenCV_to_OpenTrackIO.pdf`
- OpenLensIO lens spec: `src/main/resources/res/OpenLensIO_v1-0-1.pdf`
- Correctness roadmap: `correctness-plan.md`
- Release history: `CHANGELOG.md`
