# Optical Characteristics Specs

## Distortion Model

- [x] **OPT-DIST-001**: `Distortion` shall require at least one radial coefficient in the `radial` tuple field.
- [x] **OPT-DIST-002**: If `Distortion` is constructed with an empty `radial` tuple, the system shall raise a validation error.
- [x] **OPT-DIST-003**: `Distortion.model` shall default to `"Brown-Conrady D-U"` when not specified.
- [x] **OPT-DIST-004**: `Distortion.overscan` shall be constrained to values greater than or equal to 1.0 when present.
- [x] **OPT-DIST-005**: The `Lens.distortions` field shall support multiple simultaneous `Distortion` models per frame as a tuple with at least one entry.

## Encoders

- [x] **OPT-ENC-001**: `FizEncoders` shall require at least one of `focus`, `iris`, or `zoom` to be non-None at construction time.
- [x] **OPT-ENC-002**: `FizEncoders` fields (`focus`, `iris`, `zoom`) shall be constrained to the normalized range `[0.0, 1.0]`.
- [x] **OPT-ENC-003**: `RawFizEncoders` shall require at least one of `focus`, `iris`, or `zoom` to be non-None at construction time.
- [x] **OPT-ENC-004**: `RawFizEncoders` fields (`focus`, `iris`, `zoom`) shall be non-negative integers when present.

## Geometric Offsets

- [x] **OPT-OFFSET-001**: `DistortionOffset` and `ProjectionOffset` shall be distinct named types both representing a 2D planar offset (`x`, `y` floats), semantically distinguishing distortion center offset from projection center offset.

## Exposure Falloff

- [x] **OPT-FALLOFF-001**: `ExposureFalloff` shall hold three vignetting polynomial coefficients `a1`, `a2`, `a3` as floats.

## Dynamic Lens Fields

- [x] **OPT-LENS-001**: `Lens.focal_length` (JSON: `pinholeFocalLength`) shall represent the computed per-frame pinhole equivalent focal length in millimeters, distinct from `StaticLens.nominal_focal_length`.
- [x] **OPT-LENS-002**: `Lens.focus_distance` shall represent per-frame focus distance in meters as a strictly positive float.
- [x] **OPT-LENS-003**: `Lens.entrance_pupil_offset` shall represent the per-frame nodal point offset from the camera origin in meters.
- [ ] **OPT-LENS-004**: The ARRI reader shall populate `lens_entrance_pupil_offset` from the entrance pupil field in the AME CSV.
- [ ] **OPT-LENS-005**: The Venice reader shall populate `lens_entrance_pupil_offset` from Venice metadata when present.

## Cooke /i Parser

- [x] **OPT-COOKE-001**: `lens_data_from_binary_string()` shall extract `entrance_pupil_position` as a signed value from a 14-bit field spanning bytes 25–26 of the Cooke binary payload, with sign encoded in bit 5 of byte 25.
- [x] **OPT-COOKE-002**: `lens_data_from_binary_string()` shall extract `aperture_value` as an unsigned 12-bit value spanning bytes 5–6 of the Cooke binary payload.
- [x] **OPT-COOKE-003**: `fixed_data_from_string()` shall extract the firmware version string from character positions 61–65 of the Cooke fixed data string.
- [ ] **OPT-COOKE-004**: If `lens_data_from_binary_string()` receives a payload shorter than the minimum required length, the system shall raise `ValueError` rather than producing incorrect values silently.
