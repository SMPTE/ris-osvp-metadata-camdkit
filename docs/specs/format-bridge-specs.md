# Format Bridge Specs

## Shared Interface

- [x] **BRIDGE-IFACE-001**: Each reader shall expose a `to_clip(*file_args) -> Clip` function that returns a `Clip` populated from proprietary camera metadata.
- [x] **BRIDGE-IFACE-002**: Each reader CLI `main()` shall serialize the resulting `Clip` to JSON and write it to stdout.

## ARRI Reader

- [x] **BRIDGE-ARRI-001**: The ARRI reader `to_clip()` shall parse a tab-delimited AME CSV and populate `iso`, `camera_model`, `camera_serial_number`, `lens_model`, `lens_nominal_focal_length`, `capture_frame_rate`, `shutter_angle`, `anamorphic_squeeze`, and per-frame `lens_focus_distance` and `lens_t_number`.
- [x] **BRIDGE-ARRI-002**: `t_number_from_linear_iris_value(lin_value)` shall convert a linear iris integer from the ARRI CSV to an approximate T-stop via threshold comparison against standard T-stop values, returning `None` if no match is found.
- [x] **BRIDGE-ARRI-003**: The ARRI reader shall compute `active_sensor_physical_dimensions` from a hardcoded pixel pitch lookup table keyed on camera model string, for supported ALEXA LF variants.
- [ ] **BRIDGE-ARRI-004**: The ARRI reader shall populate `lens_entrance_pupil_offset` from the entrance pupil field in the AME CSV.
- [ ] **BRIDGE-ARRI-005**: If the ARRI CSV contains a lens distance unit other than `"Meter"`, the system shall raise `ValueError` with a descriptive message (currently uses `assert`, which raises `AssertionError` and is stripped by `-O`).

## BMD Reader

- [x] **BRIDGE-BMD-001**: The BMD reader `to_clip()` shall parse a Blackmagic RAW SDK metadata text file (key: value sections) and populate camera identity, optical, and per-frame lens fields.
- [x] **BRIDGE-BMD-002**: The BMD reader shall compute `active_sensor_physical_dimensions` for the Blackmagic URSA Mini Pro 12K.
- [ ] **BRIDGE-BMD-003**: If the BMD metadata text contains no frame sections, the system shall raise `ValueError` with a descriptive message (currently `raise "string"` which raises `TypeError` — a bug at `bmd/reader.py:45`).
- [ ] **BRIDGE-BMD-004**: The BMD reader shall extract `lens_focus_distance`, `lens_focal_length`, and `lens_t_number` regardless of whether the shutter metadata key is present (currently these are inside the `if shutter_value is not None:` block at `bmd/reader.py:112–123` — a logic bug).

## Canon Reader

- [x] **BRIDGE-CANON-001**: The Canon reader `to_clip()` shall parse a static CSV and per-frame CSV, populating `iso`, `shutter_angle`, `anamorphic_squeeze`, `lens_nominal_focal_length`, per-frame `lens_focus_distance`, and per-frame aperture.
- [x] **BRIDGE-CANON-002**: When `ApertureMode` is `2`, the Canon reader shall populate `lens_t_number`; when `ApertureMode` is `1`, it shall populate `lens_f_number`.
- [x] **BRIDGE-CANON-003**: The Canon reader shall decode `FocusPosition` from a hex-encoded IEEE 754 float32 string using `struct.unpack`.
- [x] **BRIDGE-CANON-004**: The Canon reader shall map the `LensSqueezeFactor` enum (0→1.0, 1→1.33, 2→2.0, 3→1.8) to `anamorphic_squeeze`.

## RED Reader

- [x] **BRIDGE-RED-001**: The RED reader `to_clip()` shall parse meta_3 (static) and meta_5 (per-frame) REDline CSVs, populating full camera identity, sensor dimensions (for supported RED sensors), optical static fields, and per-frame `lens_focus_distance`, `lens_entrance_pupil_offset`, and `lens_t_number` from Cooke metadata.
- [x] **BRIDGE-RED-002**: If the `Total Frames` field in meta_3 does not match the row count in meta_5, the RED reader shall raise `ValueError`.
- [x] **BRIDGE-RED-003**: The RED reader shall compute `active_sensor_physical_dimensions` from a hardcoded pixel pitch lookup table keyed on the `Sensor Name` field, for supported RED sensor variants (RAPTOR, MONSTRO, KOMODO, HELIUM, GEMINI, DRAGON).

## Venice Reader

- [x] **BRIDGE-VENICE-001**: The Venice reader `to_clip()` shall parse a Sony Venice XML static file (namespace `urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10`) and per-frame CSV, populating full camera identity, sensor dimensions, and per-frame `lens_focus_distance`, `lens_t_number`, and `lens_nominal_focal_length`.
- [x] **BRIDGE-VENICE-002**: If the clip duration in the Venice XML does not match the row count in the per-frame CSV, the Venice reader shall raise `ValueError`.
- [x] **BRIDGE-VENICE-003**: `t_number_from_frac_stop()` shall parse T-stop strings in the formats `"T N"`, `"T N.D"`, and `"T N M/D"`, computing the T-stop value as `2^(aperture/2)`.
- [x] **BRIDGE-VENICE-004**: The Venice reader shall convert focus distance from feet (CSV) to meters using the factor `12 × 25.4 / 1000`.
- [x] **BRIDGE-VENICE-005**: The Venice reader shall convert shutter angle from hundredths of a degree (XML) to degrees by dividing by 100.
- [ ] **BRIDGE-VENICE-006**: The Venice reader shall populate `lens_entrance_pupil_offset` from Venice metadata when present.
