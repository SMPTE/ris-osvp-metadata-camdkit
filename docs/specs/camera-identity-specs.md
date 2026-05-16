# Camera Identity Specs

## StaticCamera

- [x] **CAMID-CAM-001**: `StaticCamera` shall accept camera hardware metadata fields (`make`, `model`, `serial_number`, `firmware_version`, `label`, `capture_frame_rate`, `active_sensor_physical_dimensions`, `active_sensor_resolution`, `iso`, `fdl_link`, `shutter_angle`, `anamorphic_squeeze`) as individually optional with no required minimum set.
- [x] **CAMID-CAM-002**: `PhysicalDimensions` shall constrain `height` and `width` to non-negative floats representing active sensor area in millimeters.
- [x] **CAMID-CAM-003**: `SenselDimensions` shall constrain `height` and `width` to non-negative integers bounded by `MAX_INT_32`, representing active sensor photosite resolution in pixels.
- [x] **CAMID-CAM-004**: `ShutterAngle` shall constrain values to the closed range `[0.0, 360.0]` degrees.
- [x] **CAMID-CAM-005**: When setting `capture_frame_rate` or `anamorphic_squeeze` on `StaticCamera`, the system shall coerce the input to `StrictlyPositiveRational` before validation, accepting `int`, `Rational`, or `{"num": n, "denom": d}` dict inputs.
- [x] **CAMID-CAM-006**: `fdl_link` shall be validated as a UUID URN matching the pattern `urn:uuid:{8hex}-{4hex}-{4hex}-{4hex}-{12hex}` with lowercase hex digits.

## StaticLens

- [x] **CAMID-LENS-001**: `StaticLens` shall accept lens hardware metadata fields (`make`, `model`, `serial_number`, `firmware_version`, `nominal_focal_length`, `calibration_history`, `overscan_percent`) as individually optional.
- [x] **CAMID-LENS-002**: `StaticLens.nominal_focal_length` shall be a strictly positive integer in millimeters representing the marked prime or zoom label on the lens body.
- [x] **CAMID-LENS-003**: `StaticLens.overscan_percent` shall be constrained to values greater than or equal to 1.0 (representing the minimum overscan factor required by this lens).
- [x] **CAMID-LENS-004**: `StaticLens.calibration_history` shall be an unbounded tuple of non-blank strings each capped at 1023 characters.

## StaticTracker

- [x] **CAMID-TRK-001**: `StaticTracker` shall accept tracker hardware metadata fields (`make`, `model`, `serial_number`, `firmware_version`) as individually optional non-blank strings capped at 1023 characters.

## Reader Coverage

- [x] **CAMID-READ-001**: The ARRI reader shall populate `camera_model`, `camera_serial_number`, `iso`, `capture_frame_rate`, `shutter_angle`, `anamorphic_squeeze`, `lens_nominal_focal_length`, and `active_sensor_physical_dimensions` (for supported ALEXA LF variants) from the AME CSV.
- [x] **CAMID-READ-002**: The BMD reader shall populate `camera_make`, `camera_model`, `camera_serial_number`, `camera_firmware`, `lens_model`, `iso`, `capture_frame_rate`, `shutter_angle`, `anamorphic_squeeze`, and `active_sensor_physical_dimensions` (for URSA Mini Pro 12K only) from the metadata text file.
- [x] **CAMID-READ-003**: The Canon reader shall populate `camera_make` (hardcoded "Canon"), `iso`, `shutter_angle`, `anamorphic_squeeze`, and `lens_nominal_focal_length` from the static CSV.
- [x] **CAMID-READ-004**: The RED reader shall populate `camera_make`, `camera_model`, `camera_serial_number`, `camera_firmware`, `lens_make`, `lens_model`, `lens_serial_number`, `iso`, `capture_frame_rate`, `shutter_angle`, `anamorphic_squeeze`, `lens_nominal_focal_length`, and `active_sensor_physical_dimensions` (for supported RED sensor variants) from the meta_3 CSV.
- [x] **CAMID-READ-005**: The Venice reader shall populate `camera_make`, `camera_model`, `camera_serial_number`, `camera_firmware`, `lens_make`, `lens_model`, `lens_serial_number`, `iso`, `capture_frame_rate`, `shutter_angle`, `anamorphic_squeeze`, `lens_nominal_focal_length`, and `active_sensor_physical_dimensions` from the static XML.
- [ ] **CAMID-READ-006**: The Canon reader shall populate `capture_frame_rate` from the Canon static CSV.
- [ ] **CAMID-READ-007**: The Canon reader shall populate `active_sensor_physical_dimensions` from Canon sensor metadata.
- [ ] **CAMID-READ-008**: The BMD reader shall populate `active_sensor_physical_dimensions` for BMD camera models other than the URSA Mini Pro 12K.
