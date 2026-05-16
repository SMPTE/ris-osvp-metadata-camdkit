# Arrow: camera-identity

Static hardware metadata describing the capture device — camera body, lens, and tracker make/model/serial.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). Core type specs implemented; three reader gaps (Canon frame rate, Canon sensor dims, BMD multi-model sensor dims).

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters" row for Camera Identity

### LLD
- [docs/llds/camera-identity.md](../llds/camera-identity.md)

### EARS
- [docs/specs/camera-identity-specs.md](../specs/camera-identity-specs.md) — 16 specs (13 implemented, 3 gaps)

### Tests
- `src/test/python/test_camera_types.py`
- `src/test/python/test_arri_reader.py`
- `src/test/python/test_bmd_reader.py`
- `src/test/python/test_canon_reader.py`
- `src/test/python/test_red_reader.py`
- `src/test/python/test_venice_reader.py`

### Code
- `src/main/python/camdkit/camera_types.py` (owned fully)
- `src/main/python/camdkit/lens_types.py` → `StaticLens` only
- `src/main/python/camdkit/tracker_types.py` → `StaticTracker` only

## Architecture

**Purpose:** Captures the static, hardware-level description of the capture device. Fields do not change frame-to-frame; they are set once per recording.

**Key Components:**
1. `StaticCamera` (`camera_types.py:59`) — camera body metadata; all fields optional; coerces rational fields before validation
2. `PhysicalDimensions` (`camera_types.py:31`) — sensor area in mm (float h×w)
3. `SenselDimensions` (`camera_types.py:44`) — photosite resolution in pixels (int h×w)
4. `ShutterAngle` (`camera_types.py:56`) — constrained float [0.0, 360.0] degrees
5. `StaticLens` (`lens_types.py:27`) — lens hardware identity; owned by Optical Characteristics file, referenced here
6. `StaticTracker` (`tracker_types.py:19`) — tracker hardware identity; owned by Spatial Tracking file, referenced here

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| StaticCamera | CAMID-CAM-001 to CAMID-CAM-006 | 6 | 0 |
| StaticLens | CAMID-LENS-001 to CAMID-LENS-004 | 4 | 0 |
| StaticTracker | CAMID-TRK-001 | 1 | 0 |
| Reader coverage | CAMID-READ-001 to CAMID-READ-008 | 5 | 3 |

**Summary:** 16 of 16 type specs implemented; 3 reader gaps (CAMID-READ-006, CAMID-READ-007, CAMID-READ-008).

## Key Findings

1. **Generic Dimension[T] rejected** — two separate concrete classes (`PhysicalDimensions`, `SenselDimensions`) exist because a generic `Dimension[T]` pattern was incompatible with Pydantic v2 `Field` annotations. Documented comment at `camera_types.py:25`.
2. **Sensor dimensions via pixel pitch lookup** — no camera protocol transmits physical sensor dimensions; all readers compute them from hardcoded lookup tables keyed on camera model string. ARRI supports 3 models, RED supports 6, BMD supports 1, Venice uses a hardcoded pitch, Canon is unsupported.
3. **File boundary** — `StaticLens` and `StaticTracker` live in files owned by other clusters. This is a file-boundary issue only; no runtime coupling.
4. **No tracker identity from readers** — no reader populates `StaticTracker` fields; tracker identity comes only from the Mo-Sys F4 protocol (Spatial Tracking cluster).

## Work Required

### Must Fix
1. CAMID-READ-006: Canon `capture_frame_rate` not populated — investigate whether Duration/Timescale fields already parsed can yield frame rate
2. CAMID-READ-007: Canon `active_sensor_physical_dimensions` not implemented
3. CAMID-READ-008: BMD sensor dimensions limited to URSA Mini Pro 12K; all other BMD bodies produce no sensor dimension data

### Nice to Have
4. Extend ARRI and RED pixel pitch lookup tables as new camera models are released (no mechanism for extension without code change)
