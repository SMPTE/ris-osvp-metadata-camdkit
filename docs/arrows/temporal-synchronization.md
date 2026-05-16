# Arrow: temporal-synchronization

Temporal metadata — SMPTE timecode, hardware timestamps, sync lock status, and IEEE 1588 PTP grandmaster clock configuration.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). All active specs implemented except TSYNC-TS-002 (nanoseconds upper bound missing).

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters" row for Temporal Synchronization

### LLD
- [docs/llds/temporal-synchronization.md](../llds/temporal-synchronization.md)

### EARS
- [docs/specs/temporal-synchronization-specs.md](../specs/temporal-synchronization-specs.md) — 16 specs (15 implemented, 1 gap)

### Tests
- `src/test/python/test_timing_types.py`
- `src/test/python/test_mosys_reader.py` (timing data from F4)
- `src/test/python/property/test_json_roundtrip.py` (TimingTypeRoundtripTests)

### Code
- `src/main/python/camdkit/timing_types.py` (all of it)

## Architecture

**Purpose:** Models when each sample was captured, including SMPTE timecode, hardware timestamps, and the full IEEE 1588 PTP grandmaster clock description required for broadcast-grade synchronization.

**Key Components:**
1. `Timecode` (`timing_types.py:65`) — SMPTE timecode with frame count validated against `frame_rate` ceiling
2. `Timestamp` (`timing_types.py:95`) — 64-bit time as `seconds (uint48)` + `nanoseconds (uint32)`
3. `SynchronizationPTP` (`timing_types.py:127`) — IEEE 1588 grandmaster clock: profile, domain, leader identity (MAC-pattern), priorities, accuracy, time source, mean path delay, VLAN
4. `Synchronization` (`timing_types.py`) — per-frame sync status: locked, source, frequency, offsets, PTP config
5. `Timing` (`timing_types.py:180`) — top-level per-frame timing container on `Clip`; `sample_rate` is the one non-tuple field

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| Timecode | TSYNC-TC-001 to TSYNC-TC-004 | 4 | 0 |
| Timestamp | TSYNC-TS-001 to TSYNC-TS-002 | 1 | 1 |
| PTP synchronization | TSYNC-PTP-001 to TSYNC-PTP-005 | 5 | 0 |
| Synchronization | TSYNC-SYNC-001 to TSYNC-SYNC-003 | 3 | 0 |
| Timing container | TSYNC-TIMING-001 to TSYNC-TIMING-003 | 3 | 0 |

**Summary:** 16 of 16 specs; 1 gap (TSYNC-TS-002).

## Key Findings

1. **Only MoSys populates timing** — the five file-based readers (ARRI, BMD, Canon, RED, Venice) do not set any `Timing` fields. Static production files carry no live synchronization metadata.
2. **`nanoseconds` missing upper bound** — `Timestamp.nanoseconds` is `NonNegativeInt` with no `lt=1_000_000_000` constraint; values ≥ 1 second are accepted as valid (TSYNC-TS-002 gap).
3. **`domain` accepts 128–255** — `SynchronizationPTP.domain` is `NonNegative8BitInt` [0..255], but the spec and tests use [0..127]. Values 128–255 are accepted without error.
4. **PTP_LEADER_PATTERN uses alternation** — Pydantic v2 does not support regex backreferences; the MAC-address pattern manually alternates `:` and `-` separators (`timing_types.py:32`).
5. **`SynchronizationOffsets.__init__` signature mismatch** — all three params listed as required positional args but fields are `float | None`; inconsistency with the pattern used by other types.
6. **`FrameRate` as subclass** — `FrameRate(StrictlyPositiveRational)` adds documentation metadata fields; it is not used as a field type anywhere in the model. Unusual pattern that conflates value type with documentation carrier.

## Work Required

### Must Fix
1. TSYNC-TS-002: Add `lt=1_000_000_000` constraint to `Timestamp.nanoseconds`

### Should Fix
2. Tighten `SynchronizationPTP.domain` to `[0, 127]` to match spec intent (currently [0, 255])

### Nice to Have
3. Evaluate `FrameRate` subclass pattern — if it is never used as a runtime field type, consider replacing with a plain constants dict
