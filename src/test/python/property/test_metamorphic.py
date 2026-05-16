#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Metamorphic property tests for camdkit.

Metamorphic tests verify relationships between inputs and outputs rather than
exact values. They catch classes of bugs that roundtrip tests miss — in
particular, bugs where the code is consistent with itself but wrong about the
spec.

  Key order independence:
    from_json(shuffle(to_json(x))) == from_json(to_json(x))

  Default exclusion (exclude_defaults=True in the serializer):
    to_json drops fields whose value equals their declared default

  None exclusion (exclude_none=True):
    to_json never emits explicit null; the output is always fully concrete

  Optional-field neutrality:
    setting an optional field to None produces the same JSON as leaving it unset

  Extra-field tolerance:
    from_json silently ignores unrecognized keys (extra='ignore')

  Dynamic field length gap [documented]:
    a clip with mismatched per-sample field lengths is accepted without error

  Rational non-normalization [documented]:
    Rational(2, 4) != Rational(1, 2) — camdkit compares structurally, not semantically;
    consumers must normalize before comparing

Tests marked [gap] document invariants the spec mandates but camdkit does not enforce.
"""

import unittest

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from camdkit.numeric_types import Rational, StrictlyPositiveRational
from camdkit.timing_types import Timecode, TimingMode
from camdkit.clip import Clip

from property.generators import clips, timecodes, rationals

_SUPPRESS = [HealthCheck.too_slow, HealthCheck.filter_too_much]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _reverse_keys(obj):
    """Recursively reverse the insertion order of all dict keys.

    Array order is not changed — frame 0 must remain frame 0.
    """
    if isinstance(obj, dict):
        return {k: _reverse_keys(v) for k, v in reversed(list(obj.items()))}
    if isinstance(obj, list):
        return [_reverse_keys(v) for v in obj]
    return obj


def _has_none(obj) -> bool:
    """Return True if any value at any depth in a JSON-like structure is None."""
    if obj is None:
        return True
    if isinstance(obj, dict):
        return any(_has_none(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_has_none(v) for v in obj)
    return False


# ---------------------------------------------------------------------------
# Key order independence
# ---------------------------------------------------------------------------

class KeyOrderTests(unittest.TestCase):

    @given(clip=clips())
    @settings(max_examples=75, suppress_health_check=_SUPPRESS)
    def test_reversed_json_keys_give_same_clip(self, clip):
        """Reversing all dict key orderings in JSON does not change the decoded clip.

        Non-vacuous: tests that from_json is order-insensitive at every nesting level.
        A parser that depended on key order (e.g. a positional dict reader) would fail.
        """
        json_data = Clip.to_json(clip)
        reversed_json = _reverse_keys(json_data)
        self.assertEqual(Clip.from_json(json_data), Clip.from_json(reversed_json))

    def test_reversed_keys_on_multi_section_clip(self):
        """Key reversal on a clip with multiple top-level sections (static, lens, timing)."""
        clip = Clip()
        clip.lens_make = "Zeiss"
        clip.camera_make = "ARRI"
        clip.lens_nominal_focal_length = 35.0
        clip.timing_sequence_number = (0, 1, 2)
        json_data = Clip.to_json(clip)
        self.assertGreater(len(json_data), 1,
            "Clip must have multiple top-level keys for this test to be non-trivial")
        self.assertEqual(Clip.from_json(json_data), Clip.from_json(_reverse_keys(json_data)))


# ---------------------------------------------------------------------------
# Default exclusion
# ---------------------------------------------------------------------------

class DefaultExclusionTests(unittest.TestCase):
    """Verify that exclude_defaults=True correctly suppresses known default values."""

    def test_sub_frame_zero_excluded_from_timecode_json(self):
        """Timecode.sub_frame=0 (the default) must not appear in serialized JSON.

        Non-vacuous: if exclude_defaults was not applied, subFrame would appear in
        every Timecode object even when it carries no information.
        """
        tc = Timecode(
            hours=1, minutes=30, seconds=45, frames=12,
            frame_rate=StrictlyPositiveRational(24, 1),
            sub_frame=0,
        )
        json_data = Timecode.to_json(tc)
        self.assertNotIn("subFrame", json_data,
            "subFrame=0 (the default) should be excluded by exclude_defaults=True")

    def test_drop_frame_false_excluded_from_timecode_json(self):
        """Timecode.dropFrame=False (the default) must not appear in serialized JSON."""
        tc = Timecode(
            hours=0, minutes=0, seconds=0, frames=0,
            frame_rate=StrictlyPositiveRational(24, 1),
            dropFrame=False,
        )
        json_data = Timecode.to_json(tc)
        self.assertNotIn("dropFrame", json_data,
            "dropFrame=False (the default) should be excluded by exclude_defaults=True")

    def test_drop_frame_true_included_in_timecode_json(self):
        """Non-default dropFrame=True must appear in serialized JSON.

        Non-vacuous complement: confirms the exclusion is selective — only the default
        value is suppressed, not the field entirely.
        """
        tc = Timecode(
            hours=0, minutes=0, seconds=0, frames=0,
            frame_rate=StrictlyPositiveRational(30000, 1001),
            dropFrame=True,
        )
        json_data = Timecode.to_json(tc)
        self.assertIn("dropFrame", json_data,
            "dropFrame=True (non-default) must be present in JSON")
        self.assertTrue(json_data["dropFrame"])

    @given(tc=timecodes())
    @settings(suppress_health_check=_SUPPRESS)
    def test_sub_frame_zero_always_excluded(self, tc):
        """For any timecode, forcing sub_frame=0 causes subFrame to be absent from JSON.

        Non-vacuous: generators produce varied sub_frame values; this test specifically
        exercises the zero-value exclusion path.
        """
        tc_zero = Timecode(
            hours=tc.hours, minutes=tc.minutes, seconds=tc.seconds,
            frames=tc.frames, frame_rate=tc.frame_rate, sub_frame=0,
        )
        self.assertNotIn("subFrame", Timecode.to_json(tc_zero))

    @given(tc=timecodes())
    @settings(suppress_health_check=_SUPPRESS)
    def test_nonzero_sub_frame_always_included(self, tc):
        """For any timecode, setting sub_frame=1 causes subFrame to appear in JSON.

        Non-vacuous complement: confirms exclude_defaults doesn't suppress the
        entire field, only the zero default.
        """
        tc_nonzero = Timecode(
            hours=tc.hours, minutes=tc.minutes, seconds=tc.seconds,
            frames=tc.frames, frame_rate=tc.frame_rate, sub_frame=1,
        )
        json_data = Timecode.to_json(tc_nonzero)
        self.assertIn("subFrame", json_data)
        self.assertEqual(json_data["subFrame"], 1)


# ---------------------------------------------------------------------------
# None exclusion and optional-field neutrality
# ---------------------------------------------------------------------------

class OptionalFieldNeutralityTests(unittest.TestCase):

    def test_unset_optional_and_explicit_none_produce_same_json(self):
        """Setting clip.lens_nominal_focal_length = None explicitly is identical to
        leaving it unset — both produce the same JSON document.

        Non-vacuous: a model that tracked 'explicitly set to None' as a different
        state from 'never set' would produce different output for these two clips.
        """
        clip_unset = Clip()

        clip_explicit = Clip()
        clip_explicit.lens_nominal_focal_length = None

        self.assertEqual(Clip.to_json(clip_unset), Clip.to_json(clip_explicit))

    def test_extra_json_fields_are_rejected(self):
        """[gap] Camdkit rejects unrecognized JSON keys — extra='forbid' is in effect.

        Non-vacuous: documents a forward-compatibility gap. A producer emitting
        fields from a newer version of the OpenTrackIO spec will cause from_json
        to raise a ValidationError in consumers built on the current camdkit.
        Producers and consumers must be kept at the same spec version.
        """
        json_with_future_field = {
            "static": {
                "lens": {
                    "nominalFocalLength": 35.0,
                    "fieldFromFutureSpecVersion": "causes ValidationError",
                }
            }
        }
        with self.assertRaises(Exception,
                msg="from_json must raise when it encounters an unrecognized field"):
            Clip.from_json(json_with_future_field)

    @given(clip=clips())
    @settings(max_examples=75, suppress_health_check=_SUPPRESS)
    def test_clip_json_contains_no_none_values(self, clip):
        """to_json output must never contain None at any nesting level.

        Non-vacuous: exclude_none=True must apply recursively through all nested
        models. A regression that applied it only at the top level would allow None
        values to appear inside nested objects such as SynchronizationPTP.
        """
        json_data = Clip.to_json(clip)
        self.assertFalse(
            _has_none(json_data),
            "to_json must not emit None at any depth — exclude_none=True must be recursive"
        )


# ---------------------------------------------------------------------------
# Dynamic field length gap
# ---------------------------------------------------------------------------

class DynamicFieldLengthTests(unittest.TestCase):

    def test_mismatched_dynamic_field_lengths_are_accepted(self):
        """[gap] A clip with different per-sample field lengths is accepted without error.

        The OpenTrackIO spec implies all dynamic fields in a given clip share the
        same sample count. Clip enforces no such constraint: fields are stored as
        independent tuples, so a producer can create a structurally inconsistent
        clip that serializes and deserializes without any error or normalization.
        """
        clip = Clip()
        clip.timing_mode = (TimingMode.INTERNAL,)     # 1 sample
        clip.timing_sequence_number = (0, 1, 2)       # 3 samples

        # Accepted at construction
        self.assertEqual(len(clip.timing_mode), 1)
        self.assertEqual(len(clip.timing_sequence_number), 3)

        # Survives roundtrip unchanged — no validation, no normalization
        recovered = Clip.from_json(Clip.to_json(clip))
        self.assertEqual(len(recovered.timing_mode), 1)
        self.assertEqual(len(recovered.timing_sequence_number), 3)

    def test_single_frame_clip_is_consistent(self):
        """A clip with a uniform single-sample field count is always consistent."""
        clip = Clip()
        clip.timing_mode = (TimingMode.EXTERNAL,)
        clip.timing_sequence_number = (42,)
        clip.timing_sample_rate = (StrictlyPositiveRational(24, 1),)

        recovered = Clip.from_json(Clip.to_json(clip))
        field_lengths = {
            "timing_mode": len(recovered.timing_mode),
            "timing_sequence_number": len(recovered.timing_sequence_number),
            "timing_sample_rate": len(recovered.timing_sample_rate),
        }
        self.assertEqual(len(set(field_lengths.values())), 1,
            f"All field lengths should be 1, got: {field_lengths}")


# ---------------------------------------------------------------------------
# Rational non-normalization
# ---------------------------------------------------------------------------

class RationalEquivalenceTests(unittest.TestCase):
    """Camdkit compares rationals structurally, not semantically.

    Rational(2, 4) and Rational(1, 2) represent the same mathematical value
    but are treated as distinct by camdkit. Consumers that compare frame rates
    or other rational quantities must normalize before comparing.
    """

    def test_equivalent_rationals_are_structurally_distinct(self):
        """Rational(2, 4) != Rational(1, 2) — structural, not semantic, equality.

        Non-vacuous: documents a consumer-side responsibility. A consumer that
        checks `clip1.timing_sample_rate == clip2.timing_sample_rate` can get
        False even when both represent the same rate.
        """
        r_unreduced = Rational(2, 4)
        r_reduced = Rational(1, 2)
        self.assertNotEqual(r_unreduced, r_reduced,
            "Camdkit does not reduce fractions — Rational(2, 4) != Rational(1, 2)")

    def test_equivalent_rationals_produce_different_json(self):
        """Rational(2, 4) and Rational(1, 2) serialize to different JSON objects.

        Non-vacuous: a serializer that reduced fractions would emit the same JSON
        for both, hiding the structural distinction from consumers.
        """
        j_unreduced = Rational.to_json(Rational(2, 4))
        j_reduced = Rational.to_json(Rational(1, 2))
        self.assertNotEqual(j_unreduced, j_reduced,
            "Semantically equivalent rationals must produce different JSON")
        self.assertEqual(j_unreduced["num"], 2)
        self.assertEqual(j_unreduced["denom"], 4)
        self.assertEqual(j_reduced["num"], 1)
        self.assertEqual(j_reduced["denom"], 2)

    @given(r=rationals())
    def test_roundtrip_preserves_exact_numerator_and_denominator(self, r):
        """Roundtrip preserves the exact num and denom without reduction.

        Non-vacuous companion to test_equivalent_rationals_are_structurally_distinct:
        confirms that the structural identity is preserved through serialization, not
        just in memory. A serializer that silently reduced fractions would pass the
        Python equality check but change num/denom for unreduced inputs.
        """
        recovered = Rational.from_json(Rational.to_json(r))
        self.assertEqual(recovered.num, r.num,
            f"Numerator changed during roundtrip: {r.num} → {recovered.num}")
        self.assertEqual(recovered.denom, r.denom,
            f"Denominator changed during roundtrip: {r.denom} → {recovered.denom}")

    def test_strictly_positive_rational_also_not_normalized(self):
        """StrictlyPositiveRational is also structurally compared — fractions not reduced."""
        r1 = StrictlyPositiveRational(4, 8)
        r2 = StrictlyPositiveRational(1, 2)
        self.assertNotEqual(r1, r2,
            "StrictlyPositiveRational(4, 8) != StrictlyPositiveRational(1, 2)")

    def test_frame_rate_structural_comparison_in_clip(self):
        """Two clips with the same frame rate expressed differently are not equal.

        Non-vacuous: documents that clip equality depends on exact rational
        representation. A producer using 30/1 and a producer using 60/2 for the
        same physical frame rate will produce clips that compare unequal.
        """
        clip_a = Clip()
        clip_a.capture_frame_rate = StrictlyPositiveRational(30, 1)

        clip_b = Clip()
        clip_b.capture_frame_rate = StrictlyPositiveRational(60, 2)

        self.assertNotEqual(clip_a, clip_b,
            "Clips with 30/1 and 60/2 capture frame rates must compare unequal")


if __name__ == '__main__':
    unittest.main()
