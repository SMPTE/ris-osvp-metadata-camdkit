# Arrow: format-bridge

Proprietary camera format adapters — ARRI AME CSV, Blackmagic RAW SDK text, Canon CSV, RED REDline CSV, and Sony Venice XML+CSV.

## Status

**AUDITED** — last audited 2026-05-16 (git SHA `de5c56e9b2bbecff1b7a89ca6ad0c6ea2cd04ebd`). Two critical bugs in BMD reader; three entrance-pupil TODOs across ARRI, Venice, Canon; Canon missing frame rate and sensor dims.

## References

### HLD
- [docs/high-level-design.md](../high-level-design.md) — "Domain Clusters" row for Format Bridge; "No shared error handling" cross-cutting concern

### LLD
- [docs/llds/format-bridge.md](../llds/format-bridge.md)

### EARS
- [docs/specs/format-bridge-specs.md](../specs/format-bridge-specs.md) — 25 specs (20 implemented, 5 gaps)

### Tests
- `src/test/python/test_arri_reader.py`
- `src/test/python/test_bmd_reader.py`
- `src/test/python/test_canon_reader.py`
- `src/test/python/test_red_reader.py`
- `src/test/python/test_venice_reader.py`

### Test Resources
- `src/test/resources/arri/B001C001_180327_R1ZA.mov.csv`
- `src/test/resources/bmd/metadata.txt`
- `src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_{Static,Frames}.csv`
- `src/test/resources/red/A001_C066_0303LZ_001.{static,frames}.csv`
- `src/test/resources/venice/D001C005_210716AG{.csv,.xml}`

### Code
- `src/main/python/camdkit/arri/` (reader.py, cli.py)
- `src/main/python/camdkit/bmd/` (reader.py, cli.py)
- `src/main/python/camdkit/canon/` (reader.py, cli.py)
- `src/main/python/camdkit/red/` (reader.py, cli.py)
- `src/main/python/camdkit/venice/` (reader.py, cli.py)

## Architecture

**Purpose:** Converts proprietary camera metadata file formats into `Clip` objects via the shared `to_clip() -> Clip` interface. Each reader is an isolated adapter with no shared parsing code.

**Key Components:**
1. ARRI reader (`arri/reader.py:30`) — tab-delimited AME CSV; `t_number_from_linear_iris_value()` for T-stop conversion
2. BMD reader (`bmd/reader.py:20`) — key:value text sections via regex; **two critical bugs**
3. Canon reader (`canon/reader.py:19`) — 2 CSVs (static + frames); mode-dependent aperture; hex float focus decoding
4. RED reader (`red/reader.py:26`) — 2 CSVs (meta_3 + meta_5); Cooke /i lens data; frame count validation
5. Venice reader (`venice/reader.py:136`) — XML static + CSV frames; fractional T-stop string parsing; frame count validation

## Spec Coverage

| Category | Spec IDs | Implemented | Gaps |
|---|---|---|---|
| Shared interface | BRIDGE-IFACE-001 to BRIDGE-IFACE-002 | 2 | 0 |
| ARRI | BRIDGE-ARRI-001 to BRIDGE-ARRI-005 | 3 | 2 |
| BMD | BRIDGE-BMD-001 to BRIDGE-BMD-004 | 2 | 2 |
| Canon | BRIDGE-CANON-001 to BRIDGE-CANON-004 | 4 | 0 |
| RED | BRIDGE-RED-001 to BRIDGE-RED-003 | 3 | 0 |
| Venice | BRIDGE-VENICE-001 to BRIDGE-VENICE-006 | 5 | 1 |

**Summary:** 19 of 24 specs; 5 gaps (BRIDGE-ARRI-004,005; BRIDGE-BMD-003,004; BRIDGE-VENICE-006).

## Key Findings

1. **BMD `raise "string"` bug** — `bmd/reader.py:45`: `raise "Camera data does not contain frame information"` raises a string literal. In Python 3, `raise <non-exception>` is a `TypeError`. This reader crashes with the wrong exception type when input has no frame sections (BRIDGE-BMD-003).
2. **BMD indentation bug** — `bmd/reader.py:112–123`: focal length, focus distance, and T-stop extraction are inside `if shutter_value is not None:`. These are silently dropped when shutter is absent (BRIDGE-BMD-004).
3. **ARRI `assert` instead of `ValueError`** — `arri/reader.py:44`: `assert len_distance_unit == "Meter"` is stripped by Python's `-O` flag and produces `AssertionError` rather than a meaningful error (BRIDGE-ARRI-005).
4. **Canon missing frame rate and sensor dims** — Canon reader explicitly comments out these fields (CAMID-READ-006, CAMID-READ-007); investigate whether derivation from existing fields is possible.
5. **Inconsistent input type** — ARRI takes a path string; BMD/Canon/RED/Venice take file handles. Makes ARRI harder to unit test without filesystem.
6. **Venice shutter ÷ 100 undocumented** — `venice/reader.py` divides shutter angle by 100 with no comment; the encoding (hundredths of a degree in XML) is not obvious.

## Work Required

### Must Fix
1. BRIDGE-BMD-003: `raise "string"` → `raise ValueError(...)` at `bmd/reader.py:45`
2. BRIDGE-BMD-004: Move focal length/focus/T-stop extraction out of `if shutter_value` block at `bmd/reader.py:112–123`
3. BRIDGE-ARRI-005: `assert` → `if ... raise ValueError(...)` at `arri/reader.py:44`

### Should Fix
4. BRIDGE-ARRI-004: Wire up ARRI entrance pupil extraction (field exists in CSV, TODO in reader)
5. BRIDGE-VENICE-006: Wire up Venice entrance pupil extraction (TODO at `venice/reader.py:200`)
6. Add comment at Venice shutter angle division explaining the ÷100 encoding

### Nice to Have
7. Normalize reader input to file handles (align ARRI with others) for improved testability
8. Add BMD sensor dimension support for camera models beyond URSA Mini Pro 12K
