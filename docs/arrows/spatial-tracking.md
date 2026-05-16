# Arrow: spatial-tracking

3D camera position and orientation — Transform types, Tracker dynamic state, GlobalPosition, and the Mo-Sys F4 binary tracking protocol.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). Core F4 protocol implemented; 2 gaps (configurable sensor size, GlobalPosition range validation). Dead code in transform_types.py.

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters" row for Spatial Tracking; "Runtime Data Flow" diagram (MoSys path)

### LLD
- [docs/llds/spatial-tracking.md](../llds/spatial-tracking.md)

### EARS
- [docs/specs/spatial-tracking-specs.md](../specs/spatial-tracking-specs.md) — 13 specs (11 implemented, 2 gaps)

### Tests
- `src/test/python/test_transform_types.py`
- `src/test/python/test_tracker_types.py`
- `src/test/python/test_mosys_reader.py`
- `src/test/python/property/test_json_roundtrip.py` (GeometricTypeRoundtripTests)

### Code
- `src/main/python/camdkit/transform_types.py`
- `src/main/python/camdkit/tracker_types.py` (dynamic classes: `Tracker`, `GlobalPosition`)
- `src/main/python/camdkit/mosys/f4.py`
- `src/main/python/camdkit/mosys/reader.py`
- `src/main/python/camdkit/mosys/cli.py`
- Coordinate system reference: `src/main/resources/res/OpenCV_to_OpenTrackIO.pdf`

## Architecture

**Purpose:** Models where the camera is in 3D space per frame, and provides the Mo-Sys F4 binary protocol parser that is the primary live tracking data source in the codebase.

**Key Components:**
1. `Transform` (`transform_types.py:41`) — required translation (Vector3/meters) + rotation (Rotator3/degrees); optional scale and id; supports multiple named transforms per frame
2. `Vector3` / `Rotator3` (`transform_types.py:17,29`) — nullable float components; units in meters/degrees
3. `Tracker` (`tracker_types.py:43`) — per-frame notes, recording, slate, status tuples
4. `GlobalPosition` (`tracker_types.py:65`) — ENU coordinates with geodetic anchor; no range validation
5. `F4PacketParser.get_tracking_frame()` (`mosys/f4.py:194`) — decodes F4 binary packet into a single-frame Clip; dispatches on axis IDs via `match`/`case`
6. `to_clip()` (`mosys/reader.py:21`) — accumulates frames via `Clip.append()`

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| Transform types | TRACK-TYPES-001 to TRACK-TYPES-005 | 5 | 0 |
| Tracker dynamic state | TRACK-DYN-001 | 1 | 0 |
| F4 protocol | TRACK-F4-001 to TRACK-F4-008 | 6 | 2 |

**Summary:** 12 of 13 active specs implemented; 2 gaps (TRACK-F4-007 configurable sensor size, TRACK-F4-008 GlobalPosition range validation).

## Key Findings

1. **Hardcoded 36×24mm sensor** — `f4.py:287` assumes 35mm full-frame for focal length computation. Correct for many Mo-Sys rigs but wrong for others; no mechanism to configure per-rig (TRACK-F4-007 gap).
2. **Dead import** — `transform_types.py:8`: `from multiprocessing.context import DefaultContext` is unused dead code.
3. **Commented-out units in schema** — `Vector3` and `Rotator3` have units (`METER`, `DEGREE`) commented out of `json_schema_extra`. Reason not recorded; `Transform` fields do have units via field-level annotation.
4. **Constructor/field type mismatch** — `Vector3`/`Rotator3` fields are `float | None` but constructors require non-None. `None` can only be set post-construction.
5. **MoSys CLI outputs frame 0 only** — `mosys/cli.py` hardcodes reading 10 frames and printing only frame 0; not suitable as a general converter.
6. **F4 parser requires Python 3.10+** — `get_tracking_frame()` uses `match`/`case`; Pipfile specifies Python 3.11 so this is not a constraint.

## Work Required

### Must Fix
1. Remove unused import `from multiprocessing.context import DefaultContext` (`transform_types.py:8`)

### Should Fix
2. TRACK-F4-007: Make sensor size configurable in F4 parser rather than hardcoded 36×24mm
3. TRACK-F4-008: Add range validation for `GlobalPosition.lat0` [−90, 90] and `lon0` [−180, 180]

### Nice to Have
4. Restore or explicitly delete commented-out units in `Vector3`/`Rotator3` `json_schema_extra`
5. Align `mosys/cli.py` with other reader CLIs (full clip → stdout JSON)
