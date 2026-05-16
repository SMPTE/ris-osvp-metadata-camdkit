# Format Bridge

## Context and Design Philosophy

Format Bridge covers the five camera-manufacturer readers that convert proprietary metadata formats into `Clip` objects: ARRI, Blackmagic Design (BMD), Canon, RED, and Sony Venice. The Mo-Sys reader is in the Spatial Tracking cluster because it decodes a live-streaming binary wire protocol rather than a production file format.

Each reader is an isolated adapter — they share no code with each other, only the `Clip` contract they produce. The design philosophy is one adapter per format: no abstraction layer, no base class, no shared parsing infrastructure. Each reader knows exactly what its source format looks like and maps it directly to `Clip` fields.

The shared interface contract is:

```python
to_clip(*file_args) -> Clip
```

And the shared CLI pattern is:

```python
def main():
    # argparse to collect file paths
    clip = reader.to_clip(path_or_handle)
    print(json.dumps(clip.to_json(), indent=2))
```

## Reader Format Overview

| Reader | Input | Parser | Static source | Per-frame source |
|---|---|---|---|---|
| **ARRI** | 1 tab-delimited CSV (AME export) | `csv` module | First CSV row | All rows |
| **BMD** | 1 text file (key: value sections) | `re` regex | "Clip Metadata" section | "Frame N Metadata" sections |
| **Canon** | 2 CSVs (static + frames) | `csv` module | `static_csv` (1 row) | `frames_csv` (N rows) |
| **RED** | 2 CSVs (meta_3 + meta_5, REDline output) | `csv` module | `meta_3_file` (1 row) | `meta_5_file` (N rows) |
| **Venice** | XML (static) + CSV (per-frame) | `xml.etree` + `csv` | XML document | CSV rows |

## ARRI Reader

**Input:** Tab-delimited CSV exported by ARRI Meta Extract (AME) from an Alexa clip.

**Key CSV fields used:**

| CSV field | Clip field |
|---|---|
| `Exposure Index ASA` | `iso` |
| `Project FPS` | `capture_frame_rate` (via `guess_fps()`) |
| `Camera Model` | `camera_model` |
| `Camera Serial Number` | `camera_serial_number` |
| `Lens Model` | `lens_model` |
| `Lens Focal Length` | `lens_nominal_focal_length` |
| `Lens Focus Distance` | `lens_focus_distance` (per-frame tuple) |
| `Lens Linear Iris` | `lens_t_number` (per-frame, via `t_number_from_linear_iris_value()`) |
| `Shutter Angle` | `shutter_angle` |

Sensor dimensions are computed from `_CAMERA_FAMILY_PIXEL_PITCH_MAP`, a hardcoded lookup table for three ALEXA LF variants. Camera models not in the map produce no sensor dimension data.

`t_number_from_linear_iris_value(lin_value)` converts a raw linear iris integer from the CSV to an approximate T-stop using a threshold-based comparison against standard T-stop values. It is exported and independently tested.

**Known issues:**
- Line 44: `assert len_distance_unit == "Meter"` — crashes with `AssertionError` on non-meter CSV files instead of raising a meaningful `ValueError`.
- Entrance pupil position is not extracted (TODO comment in reader).
- No `camera_make` field — ARRI cameras always have make "ARRI" but the reader does not set it explicitly.

## BMD Reader

**Input:** Text file produced by the Blackmagic RAW SDK `ExtractMetadata` tool. Structure:

```
Clip Metadata
  key: value
  ...
Frame 0 Metadata
  key: value
  ...
Frame 1 Metadata
  ...
```

Three compiled regex patterns parse the sections: `_CLIP_HEADING_RE`, `_FRAME_HEADING_RE`, `_METADATA_LINE_RE`.

**Key metadata keys used:**

| Text key | Clip field |
|---|---|
| `Camera Make` | `camera_make` |
| `Camera Model` | `camera_model` |
| `Camera Serial Number` | `camera_serial_number` |
| `Camera Firmware` | `camera_firmware` |
| `Lens Model` | `lens_model` |
| `ISO` | `iso` |
| `Frame Rate` | `capture_frame_rate` |
| `Shutter Angle` | `shutter_angle` |
| `Anamorphic Squeezed` | `anamorphic_squeeze` |
| `Focal Length` | `lens_nominal_focal_length` (if constant) |
| `Focus Distance` | `lens_focus_distance` (per-frame) |
| `T-Stop` | `lens_t_number` (per-frame) |

Sensor dimensions are hardcoded for `"Blackmagic URSA Mini Pro 12K"` only. All other BMD bodies produce no sensor dimension data.

**Critical bugs:**
1. **Line 45:** `raise "Camera data does not contain frame information"` — raises a string literal rather than an exception. In Python 3, `raise <non-exception>` is a `TypeError` at runtime. This reader cannot handle clips with no frame sections without crashing with the wrong error type.
2. **Lines 112–123:** Focal length, focus distance, and T-stop extraction are indented inside the `if shutter_value is not None:` block. These values are only extracted when the shutter metadata key is present. A clip with focus/T-stop data but no shutter key silently drops those values.
3. White balance extraction is fully commented out (lines 102+). No replacement.

## Canon Reader

**Input:** Two CSVs exported by the Canon camera:
- `static_csv` — one row of clip-level metadata
- `frames_csv` — one row per frame

**Key fields:**

| CSV key | Clip field | Notes |
|---|---|---|
| `Duration` / `Timescale` | `duration` | Rational duration |
| `LensSqueezeFactor` | `anamorphic_squeeze` | Enum: 0→1.0, 1→1.33, 2→2.0, 3→1.8 |
| `PhotographicSensitivity` | `iso` | Adjusted by offset 0x80000000 when mode==1 |
| `ExposureTime` | `shutter_angle` | — |
| `FocalLength` | `lens_nominal_focal_length` | From frames CSV |
| `FocusPosition` | `lens_focus_distance` | Hex-encoded float32, decoded via `struct.unpack` |
| `ApertureNumber` | `lens_t_number` or `lens_f_number` | Mode-dependent: ApertureMode==2→t, ==1→f |

`_read_float32_as_hex()` decodes Canon's hex-encoded float32 focus position values.

The anamorphic squeeze enum mapping (0→1.0, 1→1.33, 2→2.0, 3→1.8) is hardcoded; 1.8x is Canon's proprietary anamorphic format.

**Unsupported fields:** `capture_frame_rate`, `active_sensor_physical_dimensions`, `entrance_pupil_offset` (all noted with comments in reader).

**`camera_make` is hardcoded to `"Canon"`.**

## RED Reader

**Input:** Two CSVs produced by the REDline CLI tool:
- `meta_3_file` — static metadata (1 row, `--useMeta 3` flag)
- `meta_5_file` — per-frame metadata (N rows, `--useMeta 5` flag)

**Key fields:**

| CSV key | Clip field | Notes |
|---|---|---|
| `ISO` | `iso` | — |
| `Camera Model` | `camera_model` | — |
| `Camera PIN` | `camera_serial_number` | PIN = Product Identification Number |
| `Firmware Version` | `camera_firmware` | — |
| `Lens Brand` | `lens_make` | — |
| `Lens Name` | `lens_model` | — |
| `Lens Serial Number` | `lens_serial_number` | — |
| `FPS` | `capture_frame_rate` | Via `guess_fps()` |
| `Pixel Aspect Ratio` | `anamorphic_squeeze` | — |
| `Shutter (deg)` | `shutter_angle` | — |
| `Focal Length` | `lens_nominal_focal_length` | From frames CSV |
| `Focus Distance` | `lens_focus_distance` | Per-frame |
| `Cooke Metadata` | `lens_entrance_pupil_offset`, `lens_t_number` | Hex-encoded binary, parsed via `red/cooke.py` |

Sensor dimensions are computed from `_LENS_NAME_PIXEL_PITCH_MAP` keyed on the `Sensor Name` field. Six variants are supported: RAPTOR, MONSTRO, KOMODO, HELIUM, GEMINI, DRAGON.

**Frame count validation:** raises `ValueError` if `meta_3["Total Frames"]` != `len(meta_5_rows)`. This is the only reader that validates data consistency between its two input files.

Cooke `/i` metadata is the richest optical source of any file-based reader: it provides both entrance pupil position and calibrated T-stop directly from the lens.

## Venice Reader

**Input:** XML static file + CSV per-frame file from a Sony Venice camera.

The XML uses the namespace `urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10`. Helper functions extract specific elements:

| Helper | Extracts |
|---|---|
| `find_camera_info()` | manufacturer, modelName, serialNo, firmware (from Element[@hardware='Main-Board']) |
| `find_lens_info()` | lens modelName, serialNo |
| `find_fps()` | captureFps attribute from VideoFrame element |
| `find_duration()` | Duration element |
| `find_px_dims()` | numOfVerticalLine, pixel from VideoLayout |
| `find_value(name)` | Named Item[@name] elements for ISO, ShutterSpeedAngle, PixelAspectRatio |

**Per-frame CSV fields:** `Focal Length (mm)`, `Focus Distance (ft)`, `Aperture`.

**Notable transformations:**
- `shutter_angle`: XML stores in 100ths of a degree; divided by 100 in reader. No comment explains this.
- `focus_distance`: CSV is in feet; converted to meters via `12 * 25.4 / 1000` (12 inches/foot × 25.4mm/inch ÷ 1000 mm/m).
- `lens_t_number`: parsed from strings like `"T 2"`, `"T 2.8"`, `"T 2 3/10"` via `t_number_from_frac_stop()`, computed as `2^(aperture/2)`.
- Sensor dimensions: hardcoded pixel pitch `22800/3840` µm per pixel, scaled by resolution.
- `anamorphic_squeeze`: parsed from a ratio string (e.g., `"2:1"` → 2.0).

**Frame count validation:** raises `ValueError` if XML duration != CSV row count.

## Feature Coverage Matrix

| Field | ARRI | BMD | Canon | RED | Venice |
|---|---|---|---|---|---|
| `camera_make` | — | ✓ | "Canon" (hardcoded) | ✓ | ✓ |
| `camera_model` | ✓ | ✓ | — | ✓ | ✓ |
| `camera_serial_number` | ✓ | ✓ | — | ✓ | ✓ |
| `camera_firmware` | — | ✓ | — | ✓ | ✓ |
| `capture_frame_rate` | ✓ | ✓ | ⚠ unsupported | ✓ | ✓ |
| `active_sensor_physical_dimensions` | ✓ (3 models) | ✓ (1 model) | ⚠ unsupported | ✓ (6 sensors) | ✓ |
| `iso` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `shutter_angle` | ✓ | ✓ | ✓ | ✓ | ✓ (÷100) |
| `anamorphic_squeeze` | ✓ | ✓ | ✓ (enum) | ✓ | ✓ |
| `lens_make` | — | — | — | ✓ | ✓ |
| `lens_model` | ✓ | ✓ | — | ✓ | ✓ |
| `lens_serial_number` | — | — | — | ✓ | ✓ |
| `lens_firmware` | — | — | — | ✓ | — |
| `lens_nominal_focal_length` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `lens_focus_distance` | ✓ | ✓ ⚠ bug | ✓ (hex float) | ✓ | ✓ (ft→m) |
| `lens_t_number` | ✓ (linear→T) | ✓ ⚠ bug | ✓ (mode 2) | ✓ (Cooke) | ✓ (frac stop) |
| `lens_f_number` | — | — | ✓ (mode 1) | — | — |
| `lens_entrance_pupil_offset` | ⚠ TODO | — | ⚠ unsupported | ✓ (Cooke) | ⚠ TODO |

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| No shared reader base class | Each reader is a standalone module | Abstract base class with `to_clip()` protocol | [inferred] Five readers, zero shared parsing code — an abstraction would be empty; the contract is enforced by tests, not inheritance |
| File handle vs path string as input | Mixed: ARRI/MoSys take path strings; BMD/Canon/RED/Venice take file handles | Uniform path strings or uniform file handles | [inferred] Inconsistency reflects independent authorship; file handles are more testable (no filesystem dependency in tests) |
| Pixel pitch lookup tables per reader | Hardcoded maps in each reader module | Central shared lookup table | [inferred] Lookup tables are camera-make-specific; no cross-reader sharing is needed; keeping them local avoids coupling |
| Frame count validation (RED, Venice) | Raise `ValueError` if frame counts disagree | Silently truncate to shorter | [inferred] Mismatched frame counts indicate corrupted or mismatched input files; fail-fast is correct |
| `guess_fps()` for frame rate parsing | Fuzzy match to known frame rates via 1% threshold | Parse exact rational from string | [inferred] Camera CSV exports often contain floating-point FPS approximations (e.g., 23.976) that need to map to exact rationals (24000/1001) |
| Canon anamorphic squeeze as enum | Map {0→1.0, 1→1.33, 2→2.0, 3→1.8} | Read raw value | Explicit: Canon encodes squeeze as a 4-value enum; 1.8x is Canon's proprietary format |
| Venice shutter angle ÷ 100 | Divide raw XML value by 100 | Store raw value | [inferred] Venice XML encodes shutter angle in hundredths of a degree; no comment in code explains this |

## Open Questions & Future Decisions

### Resolved
1. ✅ Mo-Sys assigned to Spatial Tracking cluster rather than Format Bridge (it decodes a live wire protocol, not a production file)

### Deferred
1. **BMD `raise "string"` bug** (`bmd/reader.py:45`): must be changed to `raise ValueError("...")`. Currently crashes with `TypeError` at runtime when no frame sections are found.
2. **BMD indentation bug** (`bmd/reader.py:112–123`): focal length, focus distance, and T-stop only extracted inside `if shutter_value is not None:` block. Fix requires un-indenting these lines.
3. **ARRI `assert` at line 44**: `assert len_distance_unit == "Meter"` should be `if len_distance_unit != "Meter": raise ValueError(...)`. `assert` is removed by Python's `-O` optimization flag and produces `AssertionError` instead of a meaningful message.
4. **ARRI entrance pupil position**: CSV contains the field; reader has a TODO but does not extract it.
5. **Venice entrance pupil offset**: TODO comment at `venice/reader.py:200`. Field is present in some Venice metadata.
6. **Canon `capture_frame_rate` and `active_sensor_physical_dimensions`**: marked unsupported in comments. The Canon CSV format may not contain frame rate; investigate whether it can be derived from `Duration` / `Timescale` fields already being parsed.
7. **BMD sensor dimensions**: only "Blackmagic URSA Mini Pro 12K" is supported. URSA Mini Pro G2, URSA Mini 4.6K, Pocket Cinema Camera 6K, etc. would produce clips with no sensor dimensions.
8. **Input interface inconsistency**: ARRI takes a path string; BMD/Canon/RED/Venice take file handles. Normalizing to file handles would improve testability of ARRI; normalizing to paths would simplify CLI code. Either direction is acceptable but should be consistent.
9. **Venice shutter angle ÷ 100**: a comment explaining the encoding (XML stores as 100ths of a degree) should be added at `venice/reader.py` near the division.
10. **White balance (BMD)**: the extraction is fully commented out. Determine if white balance is in the OpenTrackIO spec; if so, restore; if not, remove the dead comment.

## References

- Files owned by this cluster:
  - `src/main/python/camdkit/arri/reader.py`, `arri/cli.py`, `arri/__init__.py`
  - `src/main/python/camdkit/bmd/reader.py`, `bmd/cli.py`, `bmd/__init__.py`
  - `src/main/python/camdkit/canon/reader.py`, `canon/cli.py`, `canon/__init__.py`
  - `src/main/python/camdkit/red/reader.py`, `red/cli.py`, `red/__init__.py`
  - `src/main/python/camdkit/venice/reader.py`, `venice/cli.py`, `venice/__init__.py`
- Dependencies on other clusters:
  - Protocol Envelope: `Clip`, `guess_fps()`, `utils`
  - Camera Identity: `StaticCamera`, `StaticLens`, `StaticTracker` (all populated here)
  - Optical Characteristics: `Lens`, `Distortion`, `FizEncoders`, `DistortionOffset` (populated by readers); `red/cooke.py` (owned by Optical Characteristics, consumed here)
- Test resources:
  - `src/test/resources/arri/B001C001_180327_R1ZA.mov.csv`
  - `src/test/resources/bmd/metadata.txt`
  - `src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_{Static,Frames}.csv`
  - `src/test/resources/red/A001_C066_0303LZ_001.{static,frames}.csv`
  - `src/test/resources/venice/D001C005_210716AG{,.csv,.xml}`
- External dependencies: `csv`, `re`, `xml.etree.ElementTree`, `struct`, `fractions`, `math`
