# Spatial Tracking Specs

## Transform Types

- [x] **TRACK-TYPES-001**: `Transform` shall hold `translation` (`Vector3`) and `rotation` (`Rotator3`) as required fields, with `scale` (`Vector3`) and `id` (string) as optional fields.
- [x] **TRACK-TYPES-002**: The `Clip.transforms` field shall support multiple `Transform` objects per frame as a tuple, enabling named transforms (e.g., camera body and lens nodal point) within a single frame.
- [x] **TRACK-TYPES-003**: `Vector3` shall represent a 3D point or displacement with nullable `x`, `y`, `z` float components in meters.
- [x] **TRACK-TYPES-004**: `Rotator3` shall represent orientation with nullable `pan`, `tilt`, `roll` float components in degrees.
- [x] **TRACK-TYPES-005**: `GlobalPosition` shall hold ENU (East-North-Up) local tangent plane coordinates (`E`, `N`, `U` in meters) and a geodetic origin (`lat0` in degrees, `lon0` in degrees, `h0` in meters).

## Tracker Dynamic State

- [x] **TRACK-DYN-001**: `Tracker` shall support per-frame `notes`, `recording`, `slate`, and `status` fields as optional tuples.

## Mo-Sys F4 Protocol

- [x] **TRACK-F4-001**: The F4 packet parser shall validate the packet checksum (XOR of all bytes with 0x40) before processing axis data, and reject packets with invalid checksums.
- [x] **TRACK-F4-002**: The F4 packet parser shall map F4 axis IDs to corresponding OpenTrackIO `Clip` fields (pan/tilt/roll → rotation, x/y/z → translation, focus/iris/zoom → encoders, distortion coefficients, projection offset, f-number, focal length, focus distance, entrance pupil).
- [x] **TRACK-F4-003**: The F4 packet parser shall generate a unique `uuid4()` for `sample_id` and `source_id` on each parsed frame.
- [x] **TRACK-F4-004**: The F4 packet parser shall extract timecode from the packet status byte, with frame rate encoded as a 2-bit field supporting 24, 25, 30, and 30000/1001 fps.
- [x] **TRACK-F4-005**: The MoSys reader `to_clip()` shall accumulate per-frame `Clip` objects using `Clip.append()`, building a multi-frame clip from a sequential F4 binary stream.
- [x] **TRACK-F4-006**: The MoSys reader `to_clip()` shall read frames indefinitely from the F4 file when called with the default `frames=-1` argument, or up to `frames` frames when a positive count is specified.
- [ ] **TRACK-F4-007**: The F4 packet parser focal length computation shall use a configurable sensor size parameter rather than the hardcoded 36×24mm full-frame assumption at `f4.py:287`.
- [ ] **TRACK-F4-008**: `GlobalPosition` shall validate `lat0` to the range `[-90.0, 90.0]` degrees and `lon0` to the range `[-180.0, 180.0]` degrees.
