# Arrow: optical-characteristics

Per-frame lens behavior — distortion, focus/iris/zoom encoders, exposure falloff, geometric offsets, and the Cooke /i binary lens protocol.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). All type specs implemented; 3 reader entrance-pupil gaps and 1 Cooke safety gap.

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters" row for Optical Characteristics

### LLD
- [docs/llds/optical-characteristics.md](../llds/optical-characteristics.md)

### EARS
- [docs/specs/optical-characteristics-specs.md](../specs/optical-characteristics-specs.md) — 17 specs (13 implemented, 4 gaps)

### Tests
- `src/test/python/test_lens_types.py`
- `src/test/python/test_cooke_data.py`
- `src/test/python/test_arri_reader.py` (t_number coverage)
- `src/test/python/test_red_reader.py` (Cooke/entrance pupil coverage)
- `src/test/python/property/test_json_roundtrip.py` (LensTypeRoundtripTests)

### Code
- `src/main/python/camdkit/lens_types.py` (dynamic classes owned here)
- `src/main/python/camdkit/red/cooke.py`

## Architecture

**Purpose:** Models the per-frame optical state of the lens: its distortion profile, calibrated focus/iris/zoom positions, aperture, focal length, and the geometric offsets that relate the lens optical axis to the camera coordinate frame.

**Key Components:**
1. `Distortion` (`lens_types.py:88`) — Brown-Conrady distortion model with radial (≥1) and optional tangential coefficients; default model name `"Brown-Conrady D-U"`
2. `FizEncoders` (`lens_types.py:133`) — normalized [0,1] focus/iris/zoom; at least one must be non-None
3. `RawFizEncoders` (`lens_types.py:146`) — raw integer FIZ; at least one must be non-None
4. `DistortionOffset` / `ProjectionOffset` (`lens_types.py:122,127`) — semantically distinct 2D planar offsets (both inherit `PlanarOffset`)
5. `ExposureFalloff` (`lens_types.py:158`) — vignetting polynomial coefficients {a1, a2, a3}
6. `lens_data_from_binary_string()` (`red/cooke.py:16`) — Cooke /i binary parser for entrance pupil and aperture

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| Distortion | OPT-DIST-001 to OPT-DIST-005 | 5 | 0 |
| Encoders | OPT-ENC-001 to OPT-ENC-004 | 4 | 0 |
| Offsets | OPT-OFFSET-001 | 1 | 0 |
| Falloff | OPT-FALLOFF-001 | 1 | 0 |
| Dynamic lens fields | OPT-LENS-001 to OPT-LENS-005 | 3 | 2 |
| Cooke parser | OPT-COOKE-001 to OPT-COOKE-004 | 3 | 1 |

**Summary:** 17 of 17 type specs implemented; 4 gaps (OPT-LENS-004, OPT-LENS-005 reader entrance-pupil TODOs; OPT-COOKE-004 safety validation).

## Key Findings

1. **BMD indentation bug** — `bmd/reader.py:112–123`: focal length, focus distance, and T-stop extraction are inside `if shutter_value is not None:` block. These values are silently dropped when the shutter metadata key is absent. This is a logic error, not a missing feature.
2. **"At least one" constraint via `__init__` override** — both `FizEncoders` and `RawFizEncoders` enforce "at least one non-None field" in their `__init__` because Pydantic v2 has no native constraint for this pattern.
3. **Cooke parser: no error handling** — `lens_data_from_binary_string()` (`red/cooke.py:16`) silently produces wrong values on short or malformed input (OPT-COOKE-004 gap).
4. **T-stop sourcing varies by reader** — ARRI uses linear-to-T-stop lookup, BMD reads directly, Canon is mode-dependent (ApertureMode), RED uses Cooke aperture_value, Venice parses fractional stop strings.
5. **`pinholeFocalLength` rename** — `Lens.focal_length` has JSON alias `pinholeFocalLength` (renamed in 1.0.0 to distinguish from `StaticLens.nominal_focal_length`).

## Work Required

### Must Fix
1. BMD indentation bug at `bmd/reader.py:112–123` — focal length, focus, T-number silently dropped without shutter key

### Should Fix
2. OPT-LENS-004: ARRI entrance pupil — CSV field exists, parsing not wired up (`arri/reader.py` TODO)
3. OPT-LENS-005: Venice entrance pupil — TODO at `venice/reader.py:200`
4. OPT-COOKE-004: Add length validation to `lens_data_from_binary_string()` before bit extraction

### Nice to Have
5. Document `ExposureFalloff` {a1, a2, a3} polynomial model equation in LLD or spec file
