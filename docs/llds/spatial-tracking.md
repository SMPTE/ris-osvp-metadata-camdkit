# Spatial Tracking

## Context and Design Philosophy

Spatial Tracking covers everything related to where the camera is in 3D space: its position and orientation as `Transform` data, the tracker device's dynamic state (`Tracker`), its global geodetic position (`GlobalPosition`), and the Mo-Sys F4 binary protocol that is the primary live tracking data source.

This cluster is the most protocol-specific in the codebase. While ARRI, RED, Venice, and Canon readers extract static device metadata from production files, the Mo-Sys F4 reader decodes a live-streaming binary wire protocol carrying per-frame spatial and optical data. The F4 packet parser (`f4.py`) is the most complex single file in the project — it was ported from C++ and drives the richest `Clip` population of any reader.

## Transform Types

`transform_types.py` defines the 3D spatial primitives.

### Vector3

Three nullable floats representing a point or displacement in meters:

```
Vector3: { x: float | None, y: float | None, z: float | None }
```

All three fields are `float | None` in the Pydantic model, but the positional `__init__` constructor requires all three to be provided. This is a type-annotation/constructor mismatch — the field type allows `None` but the constructor signature does not. The practical effect is that `None` can only be assigned post-construction via attribute assignment.

Units annotation (METER) is present in the LLD but is **commented out** in `json_schema_extra` on `Vector3` and `Rotator3`. The comments indicate this was stripped intentionally, but no explanation is recorded.

### Rotator3

Three nullable floats representing orientation in degrees:

```
Rotator3: { pan: float | None, tilt: float | None, roll: float | None }
```

Same nullable/constructor mismatch as `Vector3`.

### Transform

The primary per-frame spatial record:

```
Transform:
  translation: Vector3      # required, position in meters
  rotation:    Rotator3     # required, orientation in degrees
  scale:       Vector3      # optional, scale factors per axis
  id:          str | None   # optional, named reference (e.g. "Camera", "Lens")
```

`id` allows a single frame to carry multiple named transforms (e.g., camera body + lens nodal point). The `transforms` field on `Clip` is `tuple[tuple[Transform, ...], ...]` — an outer tuple per frame, inner tuple of one or more `Transform` objects per frame.

`transform_types.py` also contains an unused import: `from multiprocessing.context import DefaultContext` (line 8). This is dead code.

## Tracker Dynamic State

`tracker_types.py` defines `Tracker` — the per-frame dynamic state of the tracking device — and `GlobalPosition`.

### Tracker

```
Tracker:
  notes:     tuple[str, ...]   # optional, free-text per frame
  recording: tuple[bool, ...]  # optional, recording flag per frame
  slate:     tuple[str, ...]   # optional, slate identifier per frame
  status:    tuple[str, ...]   # optional, status string per frame
```

All four fields are unconstrained tuples — no `min_length` requirement. Empty tuples are valid. This may be unintentional given that `FizEncoders` and similar types enforce "at least one" constraints.

`status` in practice carries strings like `"Optical Good"` from the Mo-Sys F4 protocol.

### GlobalPosition

Represents the camera's position in the real world using an ENU (East-North-Up) local tangent plane with a geodetic anchor:

```
GlobalPosition:
  E, N, U:        float   # local tangent plane coordinates (meters)
  lat0, lon0, h0: float   # geodetic origin (degrees, degrees, meters)
```

All six fields are required at construction. No range validation exists on any field — latitude, longitude, and height are accepted as arbitrary floats. The ENU coordinate system is documented via a Wikipedia link in the source (`tracker_types.py:67`).

## Mo-Sys F4 Protocol

The Mo-Sys F4 binary protocol is a streaming wire format for tracking data. The parser in `mosys/f4.py` was ported from C++ and is the most complex file in the project.

### Packet structure

```
[0xf4]  command byte (identifies F4 packet)
[u8]    camera_id
[u8]    axis_count
[u8]    status
[5 × axis_count bytes]  axis blocks
[u8]    checksum  (XOR of all preceding bytes with 0x40)
```

Each axis block:
```
[u8]  axis_id
[u8]  axis_status  (encodes frame rate as 2-bit field in bits 6-7)
[u8]  data_bits1
[u8]  data_bits2
[u8]  data_bits3
```

Checksum is validated by `_compute_f4_checksum()`. Signed 24-bit and 32-bit integers use two's complement arithmetic implemented in helper methods.

### Axis ID → OpenTrackIO field mapping

Selected mappings (full table in `f4.py` constants class `F4`):

| Axis ID | Field | Notes |
|---|---|---|
| `0x01` | pan (rotation) | Degrees |
| `0x02` | tilt (rotation) | Degrees |
| `0x03` | roll (rotation) | Degrees |
| `0x04` | x (translation) | Millimeters → meters |
| `0x05` | y (translation) | Millimeters → meters |
| `0x06` | z (translation) | Millimeters → meters |
| `0x10` | focus encoder | Normalized [0,1] |
| `0x11` | iris encoder | Normalized [0,1] |
| `0x12` | zoom encoder | Normalized [0,1] |
| `0x2E` | f-number | — |
| `0x2F` | focus distance | Meters |
| `0x3C` | pinhole focal length | mm; computed from 35mm sensor assumption |
| `0x3E` | entrance pupil offset | Meters |
| `0x50` | projection offset x | — |
| `0x51` | projection offset y | — |
| `0x40`–`0x47` | distortion radial coefficients | Up to 8 coefficients |

### get_tracking_frame()

`F4PacketParser.get_tracking_frame()` uses Python 3.10+ `match`/`case` to dispatch on axis IDs and build a `Clip` object with one frame of data. It:
1. Generates fresh `uuid4()` for `sample_id` and `source_id` on every frame
2. Sets `protocol` to `OPENTRACKIO_PROTOCOL_NAME` / `OPENTRACKIO_PROTOCOL_VERSION`
3. Extracts timecode from the packet status byte (frame rate encoded as 2-bit field)
4. Populates `timing.synchronization` with sequence number and lock status
5. Assembles `Transform(translation=Vector3(...), rotation=Rotator3(...))` from pan/tilt/roll/x/y/z axes
6. Populates `Lens` fields: encoders, distortions, projection offset, f-number, focal length, focus distance, entrance pupil

**Sensor assumption:** Focal length conversion uses a hardcoded 35mm full-frame sensor (36×24mm) at `f4.py:287`. This is correct for some Mo-Sys rigs but wrong for others; there is no mechanism to configure the sensor size.

### Reader accumulation pattern

`mosys/reader.py` reads frames sequentially:

```python
# to_clip() accumulation pattern
clip = None
for frame in f4_frames:
    frame_clip = to_frame(data)
    if clip is None:
        clip = frame_clip
    else:
        clip.append(frame_clip)
```

This uses `Clip.append()` to grow tuple fields. The first frame's `Clip` becomes the base; subsequent frames' tuples are concatenated onto it.

`to_frames()` does the reverse: reads a full clip, then extracts individual frames via `clip[i].to_json()`.

### CLI limitation

`mosys/cli.py` hardcodes reading the first 10 frames and outputs only frame 0 to stdout. This makes it unsuitable as a general-purpose conversion tool; it is effectively a diagnostic/demo utility.

## Coordinate System

The OpenTrackIO coordinate system is documented in:
- `src/main/resources/lyx/OpenCV_to_OpenTrackIO.lyx` / `.tex` — derivation of the transform from OpenCV camera coordinates to OpenTrackIO
- `src/main/resources/res/OpenCV_to_OpenTrackIO.pdf` — compiled reference

Rotation is expressed as pan/tilt/roll (extrinsic Euler angles), not a quaternion or rotation matrix. Translation is in meters; rotation in degrees.

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| F4 parser as Python port from C++ | Direct port of field-ID dispatch logic | Clean-room Python reimplementation | [inferred] F4 spec is stable; porting preserves verified behavior; original C++ had been tested against real hardware |
| `match`/`case` for axis dispatch | Python 3.10+ structural pattern matching | `if`/`elif` chain, dict dispatch | [inferred] Clean expression of the field-ID dispatch pattern; requires Python 3.10+ (project requires 3.11 per Pipfile) |
| UUID per frame for sample_id / source_id | `uuid4()` generated fresh each frame | Deterministic UUID from frame content | [inferred] Live streaming context — no stable frame content to hash; random UUID is the safe default |
| `Transform.id` as optional string | Free-form label | Enum of known transform types | [inferred] Future-proofing — new named transforms (e.g., "Nodal", "Entrance Pupil") don't require schema changes |
| `transforms` as tuple of tuples | `tuple[tuple[Transform, ...], ...]` | `tuple[Transform, ...]` (one per frame) | [inferred] Supports multi-transform frames (camera body + lens nodal point as separate named transforms) |
| Vector3/Rotator3 fields nullable | `float | None` on all component fields | Non-nullable floats | [inferred] Allows partial transform data — a tracker might report rotation but not position |
| GlobalPosition no range validation | All floats unconstrained | Validate lat ∈ [-90,90], lon ∈ [-180,180] | [inferred] Simplicity; validation burden deferred to consumer |
| Hardcoded 36×24mm sensor in F4 parser | Constant in `f4.py:287` | Configurable sensor parameter | [inferred] Mo-Sys rigs in the test corpus are 35mm; no mechanism existed to pass sensor metadata through the F4 protocol |

## Open Questions & Future Decisions

### Resolved
1. ✅ Coordinate system derivation documented (OpenCV_to_OpenTrackIO.pdf)

### Deferred
1. `f4.py:287` — hardcoded 36×24mm sensor assumption. No mechanism to configure sensor size per rig. Blocks correct focal length computation for non-35mm cameras.
2. `transform_types.py:8` — unused import `from multiprocessing.context import DefaultContext`. Should be removed.
3. `Vector3` and `Rotator3` — `json_schema_extra` units annotations are commented out. Reason is not recorded. If units are intentionally absent from the schema, this should be documented; if it was an accidental omission, they should be restored.
4. `Vector3`/`Rotator3` constructor/field type mismatch: fields are `float | None` but positional `__init__` requires non-None values. Decide whether to make fields non-nullable (simpler) or make the constructor accept None (consistent).
5. `Tracker` tuple fields have no `min_length` constraint — empty tuples are valid. Evaluate whether this is intentional (empty status is meaningful) or an oversight.
6. `mosys/cli.py` hardcodes first 10 frames / frame 0 output. Not useful as a general converter. Evaluate aligning with other reader CLIs (full clip → stdout JSON).
7. `GlobalPosition` has no range validation. Consider validating lat ∈ [-90, 90], lon ∈ [-180, 180] at a minimum.

## References

- Files owned by this cluster:
  - `src/main/python/camdkit/transform_types.py`
  - `src/main/python/camdkit/tracker_types.py` (dynamic classes: `Tracker`, `GlobalPosition`)
  - `src/main/python/camdkit/mosys/f4.py`
  - `src/main/python/camdkit/mosys/reader.py`
  - `src/main/python/camdkit/mosys/cli.py`
  - `src/main/python/camdkit/mosys/__init__.py`
- Files cross-referenced (static sub-class only):
  - `src/main/python/camdkit/tracker_types.py` → `StaticTracker` (owned by Camera Identity)
- Coordinate system reference:
  - `src/main/resources/lyx/OpenCV_to_OpenTrackIO.lyx`
  - `src/main/resources/res/OpenCV_to_OpenTrackIO.pdf`
- Dependencies on other clusters:
  - Protocol Envelope: `CompatibleBaseModel`, `NonBlankUTF8String`, `BOOLEAN`, `units`, `Clip`, `OPENTRACKIO_PROTOCOL_NAME`, `OPENTRACKIO_PROTOCOL_VERSION`
  - Optical Characteristics: `FizEncoders`, `Distortion`, `ProjectionOffset` (populated by F4 parser)
  - Temporal Synchronization: `Timecode`, `Synchronization` (populated by F4 parser)
- External dependencies: `math`, `struct`, `uuid`, `pydantic`
