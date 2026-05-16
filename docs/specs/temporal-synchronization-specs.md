# Temporal Synchronization Specs

## Timecode

- [x] **TSYNC-TC-001**: `Timecode.frames` shall be validated to be strictly less than the ceiling of the `frame_rate` rational value, preventing frame counts that exceed the format's capacity.
- [x] **TSYNC-TC-002**: `Timecode.hours` shall be constrained to `[0, 23]`, `minutes` to `[0, 59]`, `seconds` to `[0, 59]`, and `frames` to `[0, 119]`.
- [x] **TSYNC-TC-003**: `Timecode.frame_rate` shall be a `StrictlyPositiveRational` (both numerator and denominator strictly positive integers).
- [x] **TSYNC-TC-004**: `Timecode.dropFrame` shall be an optional boolean flag; its absence does not imply non-drop-frame.

## Timestamp

- [x] **TSYNC-TS-001**: `Timestamp` shall store time as a pair of `seconds` (`NonNegative48BitInt`, max ≈ year 10889 from epoch) and `nanoseconds` (`NonNegativeInt`).
- [ ] **TSYNC-TS-002**: `Timestamp.nanoseconds` shall be constrained to `[0, 999_999_999]` (values ≥ 1 second shall be rejected as invalid).

## PTP Synchronization

- [x] **TSYNC-PTP-001**: `SynchronizationPTP.leader_identity` shall match a MAC-address-like hex string with colon or dash separators (six two-hex-digit groups).
- [x] **TSYNC-PTP-002**: `SynchronizationPTP.domain` shall be constrained to `[0, 127]`.
- [x] **TSYNC-PTP-003**: `SynchronizationPTP.leader_accuracy` shall be constrained to `[0, 254]`.
- [x] **TSYNC-PTP-004**: `SynchronizationPTP.mean_path_delay` shall represent one-way network delay in nanoseconds as a non-negative integer.
- [x] **TSYNC-PTP-005**: `SynchronizationPTPPriorities` shall hold `priority1` and `priority2` each constrained to `[0, 255]`.

## Synchronization

- [x] **TSYNC-SYNC-001**: `Synchronization` shall carry `locked` (bool), `source` (`SynchronizationSourceEnum`), and `frequency` (`StrictlyPositiveRational`) as the core sync status fields.
- [x] **TSYNC-SYNC-002**: `Synchronization.ptp` shall be present only when `synchronization.source` is `"ptp"`.
- [x] **TSYNC-SYNC-003**: `SynchronizationOffsets` shall carry optional per-axis temporal calibration offsets for `translation`, `rotation`, and `lensEncoders` as floats.

## Timing Container

- [x] **TSYNC-TIMING-001**: `Timing.sample_rate` shall be a single `StrictlyPositiveRational` value for the whole clip (not a per-frame tuple).
- [x] **TSYNC-TIMING-002**: When setting `Timing.sample_rate` from a tuple input (as produced by `Clip` accessors), the system shall extract element `[0]` and coerce it to `StrictlyPositiveRational`.
- [x] **TSYNC-TIMING-003**: `Timing.mode`, `sample_timestamp`, `sequence_number`, `synchronization`, and `timecode` shall each be per-frame tuple fields on `Clip`.
