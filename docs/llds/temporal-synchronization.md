# Temporal Synchronization

## Context and Design Philosophy

Temporal Synchronization covers everything related to *when* a sample was captured: SMPTE timecode, hardware timestamps, sync lock status, IEEE 1588 PTP (Precision Time Protocol) configuration, and the timing mode that governs how the sample clock relates to an external reference.

All timing fields are dynamic — per-frame tuples on `Clip`. There are no static timing fields. This reflects the physical reality: sync lock can be lost mid-clip, sequence numbers always advance, and timestamps are inherently per-sample.

The cluster is contained entirely within `timing_types.py`. Of the six readers, only the Mo-Sys F4 reader populates timing fields; the other five readers work with production files that carry no live synchronization metadata.

## Type Inventory

### Enums

| Enum | Values | Notes |
|---|---|---|
| `TimingMode` | `internal`, `external` | Whether the camera clock is freerunning or locked to an external reference |
| `SynchronizationSourceEnum` | `genlock`, `videoIn`, `ptp`, `ntp` | What signal the sync is locked to |
| `PTPProfile` | `IEEE 1588-2019`, `IEEE 802.1AS-2020`, `SMPTE ST2059-2:2021` | PTP profile variant |
| `PTPLeaderTimeSource` | `GNSS`, `Atomic clock`, `NTP` | What the PTP grandmaster clock is locked to |
| `Sampling` | `static`, `regular` | Whether values are sampled per frame or are static for the clip |

All enums use `StrEnum` + `@unique` enforcement.

### Timecode

SMPTE timecode for a single frame:

```
Timecode:
  hours:      int [0..23]
  minutes:    int [0..59]
  seconds:    int [0..59]
  frames:     int [0..119]       # upper bound is format-dependent
  frame_rate: StrictlyPositiveRational
  sub_frame:  uint32             # sub-frame offset
  dropFrame:  bool | None        # drop-frame flag
```

The `frames` field is validated against `frame_rate` by `check_frames_allowed_by_format()`: it checks `frames < math.ceil(Fraction(frame_rate.num, frame_rate.denom))`. This means a 24fps timecode rejects `frames >= 24`, a 29.97fps timecode rejects `frames >= 30`. The upper bound of 119 in the field annotation covers 120fps as the maximum supported rate.

`sub_frame` is a `uint32` that subdivides one frame into finer increments. Its interpretation depends on the system; the spec does not mandate a specific sub-frame unit.

### Timestamp

A 64-bit hardware timestamp split into seconds and nanoseconds:

```
Timestamp:
  seconds:     uint48   # TAI or PTP epoch seconds
  nanoseconds: uint32   # sub-second nanoseconds [0..999999999]
```

`seconds` uses `NonNegative48BitInt` (max value 2^48 − 1 ≈ year 10889 from epoch). `nanoseconds` is a plain `NonNegativeInt`; no upper bound of 999999999 is enforced in the model.

### SynchronizationPTP

The most complex type in the cluster. Carries the full IEEE 1588 grandmaster clock description:

```
SynchronizationPTP:
  profile:           PTPProfile enum
  domain:            int [0..127]     # PTP domain number
  leader_identity:   str              # MAC-like hex string (colon or dash separated)
  leader_priorities: SynchronizationPTPPriorities  # { priority1, priority2 ∈ [0..255] }
  leader_accuracy:   uint8 [0..254]   # clock accuracy class
  leader_time_source: PTPLeaderTimeSource enum
  mean_path_delay:   uint32           # nanoseconds, one-way network delay
  vlan:              uint16           # VLAN ID [0..65535]
```

`leader_identity` matches `PTP_LEADER_PATTERN` — a regex for MAC-address-like hex strings that supports both colon and dash separators. The pattern uses explicit alternation rather than backreferences because Pydantic v2 does not support regex backreferences.

`SynchronizationPTP` is the only type in the project with an extensive embedded docstring (lines 233–276 in `timing_types.py`) that explains each field's meaning and source. This was noted as a design pattern for "metadata transparency."

### Synchronization

The per-frame sync status container:

```
Synchronization:
  locked:    bool
  source:    SynchronizationSourceEnum
  frequency: StrictlyPositiveRational   # sync signal frequency (Hz)
  offsets:   SynchronizationOffsets | None
  present:   bool | None
  ptp:       SynchronizationPTP | None  # present only when source == ptp
```

`SynchronizationOffsets` carries calibration offsets applied to the sync signal:

```
SynchronizationOffsets:
  translation:   float | None   # temporal offset applied to position data
  rotation:      float | None   # temporal offset applied to rotation data
  lensEncoders:  float | None   # temporal offset applied to lens encoder data
```

All three offset fields are optional in the Pydantic model, but the `__init__` signature lists them as required positional args with no defaults. This is a constructor signature inconsistency (matching the pattern seen in other types for 0.9 compatibility) that conflicts with the optional field types.

### Timing

The top-level per-frame timing container on `Clip`:

```
Timing:
  mode:                tuple[TimingMode, ...]
  recorded_timestamp:  tuple[Timestamp, ...] | None
  sample_rate:         StrictlyPositiveRational       # single value, not per-frame
  sample_timestamp:    tuple[Timestamp, ...]
  sequence_number:     tuple[int, ...]
  synchronization:     tuple[Synchronization, ...]
  timecode:            tuple[Timecode, ...]
```

`sample_rate` is the one non-tuple field: it is a single rational value for the whole clip, not per-frame. A `@field_validator` (mode "before") coerces the input to `StrictlyPositiveRational`, handling both scalar inputs and tuple inputs (it extracts element [0] from a tuple, which is the pattern used when setting from a Clip accessor).

### FrameRate

`FrameRate` is a nominal subclass of `StrictlyPositiveRational` that adds documentation metadata:

```
FrameRate(StrictlyPositiveRational):
  canonical_name: str    # e.g. "24" or "23.976"
  sampling:       str    # "regular" or "static"
  units:          str    # always "1/s" (Hz)
  section:        str    # spec section reference
```

These are class-level metadata fields, not instance data. `FrameRate` is not used as a field type anywhere in the model — it exists to attach documentation metadata to specific well-known frame rates for schema/documentation generation. This is an unusual inheritance pattern that conflates a value type with a documentation carrier.

## Per-Frame Timing Data Flow

Only the Mo-Sys F4 reader populates timing fields. The F4 packet provides:
- **Timecode** — encoded in the packet status byte; frame rate is a 2-bit field (four possible values: 24, 25, 30, 30000/1001 fps)
- **Sequence number** — extracted from F4 axis data
- **Synchronization** — lock status, source, and PTP configuration if applicable
- **Sample timestamp** — not directly from F4; the F4 protocol does not carry wall-clock timestamps; the Mo-Sys reader does not populate `sample_timestamp`

The five non-Mo-Sys readers do not populate any `Timing` fields. Static production files (CSV, XML, text) carry no live synchronization metadata.

## Relationship to OpenTrackIO Wire Format

The complete dynamic example (`examples.py`) demonstrates the full PTP configuration:
- `synchronization.source = "ptp"`
- `synchronization.ptp.profile = PTPProfile.SMPTE_ST_2059_2` (broadcast standard)
- `synchronization.ptp.domain` — network domain number
- `synchronization.ptp.leader_identity` — grandmaster MAC address
- `synchronization.ptp.leader_time_source = PTPLeaderTimeSource.GNSS`
- `synchronization.ptp.mean_path_delay` — one-way network delay in nanoseconds

This is the normative example of how a broadcast-grade PTP-synchronized camera should report its timing state.

## Decisions & Alternatives

| Decision | Chosen | Alternatives Considered | Rationale |
|---|---|---|---|
| All timing fields as per-frame tuples | `tuple[T, ...]` for every Timing field | Static values for mode and sample_rate | [inferred] Sync lock can be lost mid-clip; mode can change; tuple semantics are consistent with rest of dynamic fields |
| `sample_rate` as single value, not tuple | `StrictlyPositiveRational` scalar | `tuple[StrictlyPositiveRational, ...]` | [inferred] Sample rate is a clip-level property, not per-frame; a variable sample rate clip is not a supported use case |
| Timecode frame validation via `math.ceil(Fraction(...))` | Validate `frames < ceil(num/denom)` | Validate against an integer lookup table | [inferred] Handles non-integer frame rates (e.g., 30000/1001) without a hardcoded table; `Fraction` arithmetic is exact |
| PTP_LEADER_PATTERN with explicit alternation | `([0-9a-f]{2}[:-]){5}[0-9a-f]{2}` | Backreference to enforce consistent separator | Explicit: Pydantic v2 does not support regex backreferences; comment documents this |
| `SynchronizationPTP` embedded docstring | Inline field-by-field documentation in the class body | External spec reference only | [inferred] Self-contained field documentation is valuable when the schema is published without the source code |
| `FrameRate` as `StrictlyPositiveRational` subclass | Subclass with metadata fields | Standalone dataclass; annotated constant | [inferred] Allows `FrameRate` instances to be used wherever a `StrictlyPositiveRational` is accepted while carrying documentation metadata |
| `Timestamp` split as seconds + nanoseconds | Two fields (`uint48` + `uint32`) | Single `uint64` nanoseconds since epoch | [inferred] Avoids 64-bit integer precision loss in Python/JSON; matches common PTP wire format conventions |

## Open Questions & Future Decisions

### Resolved
1. ✅ PTP profile enum values match SMPTE ST2059-2:2021 and IEEE 1588-2019 / 802.1AS-2020

### Deferred
1. `SynchronizationOffsets.__init__` lists all three params as required positional args, but all three fields are `float | None` in the model. Decide whether to make the constructor match the field types (accept `None`) or make the fields non-nullable.
2. `Timestamp.nanoseconds` is `NonNegativeInt` with no upper bound of 999,999,999 enforced. A value of 1,500,000,000 nanoseconds is accepted — which is invalid (exceeds one second). Consider adding `lt=1_000_000_000`.
3. `FrameRate` subclass pattern conflates value type and documentation carrier. If `FrameRate` instances are never used as runtime field values, consider replacing with a plain dataclass or constants dict.
4. No reader other than Mo-Sys populates `timing.sample_timestamp`. For production file workflows (ARRI, RED, Venice, Canon, BMD), consumers receive no wall-clock timestamp even when one could be inferred from clip metadata.
5. Mo-Sys F4 reader does not populate `timing.recorded_timestamp`. The F4 protocol carries timecode but not a full UTC/TAI timestamp. This gap may be intentional or a missing feature.
6. ~~`domain` accepts 128–255~~: The model correctly enforces `[0..127]` via `NonNegative8BitInt` (MAX_INT_8). Values ≥ 128 are rejected by the validator. No gap exists here.

## References

- Files owned by this cluster:
  - `src/main/python/camdkit/timing_types.py` (all of it)
- Dependencies on other clusters:
  - Protocol Envelope: `CompatibleBaseModel`, `NonBlankUTF8String`, `StrictlyPositiveRational`, `NonNegative8BitInt`, `StrictlyPositive8BitInt`, `NonNegativeInt`, `NonNegative48BitInt`, `NonNegativeFloat`, `units`
- Populated by: Mo-Sys F4 reader (timecode, synchronization, sequence number, timing mode); no other reader populates timing fields
- External dependencies: `pydantic`, `enum`, `fractions`, `math`
