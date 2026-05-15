# Correctness Plan

The camdkit repo positions code and unit tests as the executable reference for the OpenTrackIO metadata model. Currently the tests are example- and unit-test-oriented. This plan adds property tests, metamorphic tests, a differential harness against an independent spec model, and a formal proof layer — building toward a credible verified conformance harness.

**Architecture:**
- Lean proofs define truth for the math
- Python spec model defines executable truth for protocol semantics
- camdkit is tested against both
- Hypothesis searches the edge cases

---

## Step 1 — Property tests: generators and roundtrips

Add Hypothesis to dev dependencies. Build generators for all model entities and establish the core JSON/schema invariants.

### Core invariants

```
decode(encode(x)) ≡ canonicalize(x)
encode(decode(json)) ≡ canonicalize(json)
valid(x) → schema_accepts(to_json(x))
schema_rejects(bad_json) → camdkit_rejects(bad_json)
```

The canonical form:

```
generated valid model
  → to_json
  → validate JSON schema
  → from_json
  → to_json
  = canonical JSON
```

### Generators to build

- Camera body (make, model, serial, firmware, label, ISO, shutter angle)
- Lens (make, model, serial, firmware, nominal focal length, distortion objects, FIZ encoders)
- Frame / timecode / PTP fields
- Distortion objects (including multiple-object payloads)
- Focus distance
- Focal length / zoom
- Sensor and image dimensions
- Transforms and poses
- Rational and StrictlyPositiveRational (all boundary conditions)
- All constrained numeric types (int ranges, float constraints, normalized, unity-or-greater)

### Boundary cases to encode as named Hypothesis examples from day one

These come from open repo issues and changelog — they should be explicit boundary targets, not discovered later:

- `focusDistance` = infinity, very large value, zero, missing
- zoom lens `nominalFocalLength` undefined
- vignetting payloads
- multiple distortion objects in a single frame
- PTP domain: 0, 127, 128, -1 (valid range is 0–127)

### File layout

```
src/test/python/
  property/
    generators.py
    test_json_roundtrip.py
    test_schema_agreement.py
```

---

## Step 2 — Metamorphic tests

Metamorphic tests catch spec ambiguities that roundtrip tests miss. They assert relationships between inputs and outputs rather than exact values.

### Properties

**Structural neutrality:**
- Adding irrelevant optional fields then canonicalizing does not change semantics
- JSON key order does not affect decoded value
- Missing optional field and explicit default agree where the spec says they should

**Numeric normalization:**
- Equivalent rational spellings normalize consistently (e.g. 2/4 vs 1/2 — spec says whether these are equal or distinct)
- Unit conversion there-and-back is identity within tolerance

**Geometric identity:**
- Coordinate transform composed with identity is identity
- Composing inverse transforms yields identity within floating-point tolerance

**Lens/camera math:**
```
OpenCV params
  → convert to OpenTrackIO / OpenLensIO
  → project point
  ≈ OpenCV project point
```

### Tolerance discipline

Separate exact and floating properties from the start:

- **Exact:** JSON structure, schema validity, discrete enum values, integer fields
- **Floating:** projection and distortion transform results — use explicit tolerances, document the tolerance and why

### File layout

```
src/test/python/
  property/
    test_metamorphic.py
```

---

## Step 3 — Differential harness: independent spec model vs camdkit

The differential oracle is an *independent* Python spec model written in plain dataclasses with no camdkit internals. This is the key design decision: `opentrackio_lib.py` (the existing reference parser in the repo) is camdkit-adjacent and may share the same misunderstandings. It can serve as a third comparator later, but not as the oracle.

### Structure

```
src/test/python/
  differential/
    spec_model.py        # independent dataclasses + semantics, no camdkit imports
    adapters.py          # spec ↔ camdkit conversion only
    test_spec_vs_camdkit.py
```

### Differential flows

**Forward:**
```
Hypothesis generated SpecValue
  → spec_to_json
  → camdkit.from_json
  → camdkit.to_json
  → spec_from_json
  → compare semantic equality
```

**Reverse:**
```
Hypothesis generated camdkit-compatible JSON
  → camdkit.from_json
  → spec_from_json
  → both accept and normalize same
    OR both reject
```

### Most valuable differential properties

| Property | Description |
|---|---|
| Acceptance agreement | `spec_accepts(x) ↔ camdkit_accepts(x)` |
| Canonicalization agreement | `spec_canonical_json(x) = camdkit_canonical_json(x)` |
| Lens math agreement | `spec_project(params, point) ≈ reference_project(params, point)` |
| Conversion agreement | `spec_convert_opencv_to_opentrackio(params) ≈ camdkit/reference result` |

Every disagreement is one of: implementation bug, spec ambiguity, missing precondition, or wrong test assumption. Treat all four as bugs worth filing.

---

## Step 4 — Projection and distortion differential tests

Add OpenCV ↔ OpenTrackIO projection differential tests as a focused extension of Step 3. These require camera parameter generators that produce valid projection-testable configurations.

```
OpenCV params
  → spec_convert_opencv_to_opentrackio
  → spec_project(point)

OpenCV params
  → cv2.projectPoints(point)

assert spec_result ≈ opencv_result within tolerance
```

Document tolerances and the exact pixel-coordinate convention assumptions (principal point origin, image plane orientation) as inline preconditions on each test — these are where subtle spec ambiguities will surface.

---

## Step 5 — Lean proof kernel

Prove the semantic kernel; do not start by proving the full protocol.

### Layers

**Layer A — numeric and vector foundations**
- Vec2, Vec3, matrices, affine transforms
- Normalized coordinates
- Pixel coordinates

**Layer B — camera model semantics**
- Pinhole projection
- Principal point convention
- Focal length convention
- Sensor/image dimension assumptions

**Layer C — distortion semantics**
- Radial rational distortion
- Tangential distortion
- Denominator nonzero preconditions

**Layer D — conversion theorems**
- OpenCV params → OpenTrackIO params
- Projection equivalence
- Radial distortion equivalence
- Full pixel equivalence under stated assumptions

**Layer E — executable extraction**
- Lean spec generates JSON test vectors
- Python differential harness checks camdkit against them

### Named theorems to prove

- `principal_point_conversion_iff`
- `focal_length_conversion_iff`
- `linear_projection_pixel_equivalence`
- `radial_distortion_value_equivalence`
- `opencv_to_opentrackio_projection_equivalence`
- `json_roundtrip_semantic_preservation`
- `canonicalization_idempotent`

### Design constraint

Make theorem statements mirror the Hypothesis test properties. Every bug found by Hypothesis is then one of: implementation bug, spec ambiguity, missing precondition, or wrong theorem statement — a clear four-way triage instead of "the test failed."

---

## Sequence summary

| Step | Deliverable |
|---|---|
| 1 | Hypothesis generators, roundtrip and schema agreement tests, boundary cases from open issues |
| 2 | Metamorphic tests (key order, optional fields, numeric normalization, geometric identity) |
| 3 | Independent Python spec model, adapters, differential acceptance and canonicalization tests |
| 4 | OpenCV ↔ OpenTrackIO projection and distortion differential tests |
| 5 | Lean proof kernel through Layer D, conformance vector export |
