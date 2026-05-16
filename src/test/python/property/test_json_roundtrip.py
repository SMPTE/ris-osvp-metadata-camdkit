#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Property tests: JSON roundtrip for all camdkit model types."""

import sys
import unittest

from hypothesis import given, settings, HealthCheck

from camdkit.numeric_types import (
    MAX_INT_8, MAX_INT_32, MAX_UINT_32, MIN_INT_32,
    Rational, StrictlyPositiveRational,
)
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.lens_types import Distortion, FizEncoders, RawFizEncoders, ExposureFalloff
from camdkit.timing_types import (
    Timestamp, Timecode, Synchronization, SynchronizationSource,
    SynchronizationPTP, SynchronizationPTPPriorities, PTPProfile,
)
from camdkit.clip import Clip

from property.generators import (
    rationals, strictly_positive_rationals,
    vector3s, rotator3s, transforms,
    distortions, fiz_encoders, raw_fiz_encoders, exposure_falloffs,
    timestamps, timecodes, synchronization_ptps, synchronizations,
    clips,
    non_negative_8bit_ints, strictly_positive_floats, unity_or_greater_floats,
    ptp_leader_identities, synchronization_ptp_priorities, non_negative_floats,
    non_negative_ints,
)

_SUPPRESS = [HealthCheck.too_slow, HealthCheck.filter_too_much]


class RationalRoundtripTests(unittest.TestCase):

    @given(r=rationals())
    def test_rational_roundtrip(self, r):
        recovered = Rational.from_json(Rational.to_json(r))
        self.assertEqual(r, recovered)

    @given(r=strictly_positive_rationals())
    def test_strictly_positive_rational_roundtrip(self, r):
        recovered = StrictlyPositiveRational.from_json(
            StrictlyPositiveRational.to_json(r)
        )
        self.assertEqual(r, recovered)

    def test_rational_max_values(self):
        r = Rational(MAX_INT_32, MAX_UINT_32)
        self.assertEqual(r, Rational.from_json(Rational.to_json(r)))

    def test_rational_min_numerator(self):
        r = Rational(MIN_INT_32, 1)
        self.assertEqual(r, Rational.from_json(Rational.to_json(r)))

    def test_strictly_positive_rational_max(self):
        r = StrictlyPositiveRational(MAX_INT_32, MAX_UINT_32)
        self.assertEqual(r, StrictlyPositiveRational.from_json(
            StrictlyPositiveRational.to_json(r)
        ))


class GeometricTypeRoundtripTests(unittest.TestCase):

    @given(v=vector3s())
    def test_vector3_roundtrip(self, v):
        recovered = Vector3.from_json(Vector3.to_json(v))
        self.assertEqual(v, recovered)

    @given(r=rotator3s())
    def test_rotator3_roundtrip(self, r):
        recovered = Rotator3.from_json(Rotator3.to_json(r))
        self.assertEqual(r, recovered)

    @given(t=transforms())
    def test_transform_roundtrip(self, t):
        recovered = Transform.from_json(Transform.to_json(t))
        self.assertEqual(t, recovered)


class LensTypeRoundtripTests(unittest.TestCase):

    @given(d=distortions())
    def test_distortion_roundtrip(self, d):
        recovered = Distortion.from_json(Distortion.to_json(d))
        self.assertEqual(d, recovered)

    @given(f=fiz_encoders())
    def test_fiz_encoders_roundtrip(self, f):
        recovered = FizEncoders.from_json(FizEncoders.to_json(f))
        self.assertEqual(f, recovered)

    @given(r=raw_fiz_encoders())
    def test_raw_fiz_encoders_roundtrip(self, r):
        recovered = RawFizEncoders.from_json(RawFizEncoders.to_json(r))
        self.assertEqual(r, recovered)

    @given(e=exposure_falloffs())
    def test_exposure_falloff_roundtrip(self, e):
        recovered = ExposureFalloff.from_json(ExposureFalloff.to_json(e))
        self.assertEqual(e, recovered)


class TimingTypeRoundtripTests(unittest.TestCase):

    @given(ts=timestamps())
    def test_timestamp_roundtrip(self, ts):
        recovered = Timestamp.from_json(Timestamp.to_json(ts))
        self.assertEqual(ts, recovered)

    @given(tc=timecodes())
    @settings(suppress_health_check=_SUPPRESS)
    def test_timecode_roundtrip(self, tc):
        recovered = Timecode.from_json(Timecode.to_json(tc))
        self.assertEqual(tc, recovered)

    @given(s=synchronizations())
    @settings(suppress_health_check=_SUPPRESS)
    def test_synchronization_roundtrip(self, s):
        recovered = Synchronization.from_json(Synchronization.to_json(s))
        self.assertEqual(s, recovered)

    def test_ptp_domain_lower_bound(self):
        ptp = SynchronizationPTP(
            profile=PTPProfile.SMPTE_2059_2_2021,
            domain=0,
            leader_identity="00:11:22:33:44:55",
            leader_priorities=SynchronizationPTPPriorities(1, 2),
            leader_accuracy=0.0,
            mean_path_delay=0.0,
        )
        recovered = SynchronizationPTP.from_json(SynchronizationPTP.to_json(ptp))
        self.assertEqual(ptp, recovered)

    def test_ptp_domain_upper_bound(self):
        ptp = SynchronizationPTP(
            profile=PTPProfile.SMPTE_2059_2_2021,
            domain=MAX_INT_8,  # 127
            leader_identity="ff:ff:ff:ff:ff:ff",
            leader_priorities=SynchronizationPTPPriorities(255, 255),
            leader_accuracy=0.0,
            mean_path_delay=0.0,
        )
        recovered = SynchronizationPTP.from_json(SynchronizationPTP.to_json(ptp))
        self.assertEqual(ptp, recovered)


class ClipRoundtripTests(unittest.TestCase):

    @given(clip=clips())
    @settings(max_examples=75, suppress_health_check=_SUPPRESS)
    def test_clip_roundtrip(self, clip):
        json_data = Clip.to_json(clip)
        recovered = Clip.from_json(json_data)
        self.assertEqual(clip, recovered)

    def test_clip_roundtrip_empty(self):
        clip = Clip()
        self.assertEqual(clip, Clip.from_json(Clip.to_json(clip)))

    def test_focus_distance_large_value(self):
        """Boundary: focus distance at float max (open issue: infinity handling)."""
        clip = Clip()
        clip.lens_focus_distance = (sys.float_info.max,)
        recovered = Clip.from_json(Clip.to_json(clip))
        self.assertEqual(clip, recovered)

    def test_multiple_distortion_objects_per_frame(self):
        """Boundary: multiple Distortion objects in a single frame (open issue)."""
        clip = Clip()
        d1 = Distortion(model="Brown-Conrady D-U", radial=(0.1, 0.2, 0.3))
        d2 = Distortion(model="Brown-Conrady U-D", radial=(-0.1, -0.2))
        clip.lens_distortions = ((d1, d2),)
        recovered = Clip.from_json(Clip.to_json(clip))
        self.assertEqual(clip, recovered)

    def test_zoom_lens_nominal_focal_length_absent(self):
        """Boundary: zoom lens with nominalFocalLength explicitly absent (open issue)."""
        clip = Clip()
        clip.lens_make = "Zeiss"
        clip.lens_model = "CZ.2 70-200"
        json_data = Clip.to_json(clip)
        # Confirm the field is absent from the serialized JSON, not just unset in Python
        self.assertNotIn("nominalFocalLength", json_data.get("static", {}).get("lens", {}))
        recovered = Clip.from_json(json_data)
        self.assertEqual(clip, recovered)

    def test_ptp_domain_boundaries_in_clip(self):
        """Boundary: PTP domain at 0 and 127."""
        for domain in (0, MAX_INT_8):
            clip = Clip()
            sync = Synchronization(
                locked=True,
                source=SynchronizationSource.PTP,
                ptp=SynchronizationPTP(
                    profile=PTPProfile.SMPTE_2059_2_2021,
                    domain=domain,
                    leader_identity="aa:bb:cc:dd:ee:ff",
                    leader_priorities=SynchronizationPTPPriorities(1, 1),
                    leader_accuracy=0.0,
                    mean_path_delay=0.0,
                ),
            )
            clip.timing_synchronization = (sync,)
            recovered = Clip.from_json(Clip.to_json(clip))
            self.assertEqual(clip, recovered)


if __name__ == '__main__':
    unittest.main()
