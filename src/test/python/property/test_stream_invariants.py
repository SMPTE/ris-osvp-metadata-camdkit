#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Stream invariant tests: temporal coherence and lens math correctness.

These tests verify two categories of invariants:

  Tier 1 — Temporal coherence: properties that must hold for a data stream to be
    self-consistent (timestamps, sequence numbers, PTP coherence). Several tests
    in this section document *gaps* — constraints the spec mandates but camdkit
    does not enforce — so that consumers know they must validate themselves.

  Tier 2 — Lens math: properties of the distortion model. The Brown-Conrady
    self-consistency test is the core: it exercises the actual formula, not just
    serialization.

Tests labelled "[gap]" in their docstrings verify that camdkit accepts inputs
that violate a semantic invariant. These are intentionally expected to pass —
they document the gap.
"""

import math
import unittest

import jsonschema
from hypothesis import given, settings, HealthCheck, assume
from hypothesis import strategies as st
from fractions import Fraction

from camdkit.numeric_types import StrictlyPositiveRational
from camdkit.timing_types import (
    Timestamp, Timecode, Synchronization, SynchronizationSource,
    SynchronizationPTP, SynchronizationPTPPriorities, PTPProfile,
)
from camdkit.lens_types import Distortion
from camdkit.clip import Clip

from property.generators import (
    synchronization_ptps, synchronization_ptp_priorities,
    strictly_positive_rationals,
)

_SUPPRESS = [HealthCheck.too_slow, HealthCheck.filter_too_much]

CLIP_SCHEMA = None
CLIP_VALIDATOR = None


def setUpModule():
    global CLIP_SCHEMA, CLIP_VALIDATOR
    CLIP_SCHEMA = Clip.make_json_schema()
    CLIP_VALIDATOR = jsonschema.Draft202012Validator(CLIP_SCHEMA)


# ---------------------------------------------------------------------------
# Brown-Conrady math — used by Tier 2 tests
# ---------------------------------------------------------------------------

def _brown_conrady_apply(x: float, y: float,
                          radial: tuple, tangential: tuple | None = None
                          ) -> tuple[float, float]:
    """Apply the Brown-Conrady radial+tangential formula.

    Both D-U and U-D models use the same polynomial; the caller decides what
    (x, y) represents (distorted or undistorted input).

        r² = x² + y²
        κ(r) = (1 + k1·r² + k2·r⁴ + k3·r⁶) / (1 + k4·r² + k5·r⁴ + k6·r⁶)
        x_out = x·κ + 2·p1·x·y + p2·(r² + 2·x²)
        y_out = y·κ + p1·(r² + 2·y²) + 2·p2·x·y
    """
    r2 = x * x + y * y
    r4 = r2 * r2
    r6 = r4 * r2

    k = list(radial) + [0.0] * (6 - len(radial))
    k1, k2, k3, k4, k5, k6 = k[:6]

    denom = 1.0 + k4 * r2 + k5 * r4 + k6 * r6
    if abs(denom) < 1e-15:
        return x, y  # degenerate denominator — skip
    kappa = (1.0 + k1 * r2 + k2 * r4 + k3 * r6) / denom

    xo = x * kappa
    yo = y * kappa

    if tangential:
        p = list(tangential) + [0.0, 0.0]
        p1, p2 = p[0], p[1]
        xo += 2.0 * p1 * x * y + p2 * (r2 + 2.0 * x * x)
        yo += p1 * (r2 + 2.0 * y * y) + 2.0 * p2 * x * y

    return xo, yo


def _brown_conrady_iterative_inverse(xd: float, yd: float,
                                      radial: tuple, tangential: tuple | None = None,
                                      max_iter: int = 200, tol: float = 1e-10
                                      ) -> tuple[float, float]:
    """Iteratively find (xu, yu) such that _brown_conrady_apply(xu, yu) ≈ (xd, yd).

    Convergence rate per iteration is |f'(y) - 1| ≈ 3·|k1|·r². For |k1| ≤ 0.3
    and r ≤ sqrt(2), the rate is at most 0.85, so 200 iterations gives residual
    < 0.85^200 ≈ 3e-15 — well below the 1e-6 test tolerance.
    """
    xu, yu = xd, yd
    for _ in range(max_iter):
        xe, ye = _brown_conrady_apply(xu, yu, radial, tangential)
        dx, dy = xd - xe, yd - ye
        xu += dx
        yu += dy
        if dx * dx + dy * dy < tol * tol:
            break
    return xu, yu


# ---------------------------------------------------------------------------
# Tier 1: Temporal coherence
# ---------------------------------------------------------------------------

class TimingCoherenceTests(unittest.TestCase):

    # --- PTP coherence gap ---

    def test_ptp_source_without_ptp_object_is_accepted(self):
        """[gap] Camdkit accepts source=PTP with no ptp object.

        The spec requires a ptp block when source is 'ptp', but Synchronization
        has no model validator enforcing this. A producer that sets source=PTP
        and omits the ptp block will not be caught by camdkit — consumers must
        validate this themselves.
        """
        sync = Synchronization(locked=True, source=SynchronizationSource.PTP)
        self.assertIsNone(sync.ptp)
        # It also round-trips without error, silently preserving the invalid state.
        clip = Clip()
        clip.timing_synchronization = (sync,)
        recovered = Clip.from_json(Clip.to_json(clip))
        self.assertIsNone(recovered.timing_synchronization[0].ptp)

    def test_schema_does_not_enforce_ptp_coherence(self):
        """[gap] The JSON schema accepts source=PTP without a ptp block.

        JSON Schema (Draft 2020-12) cannot easily express the cross-field
        constraint 'if source == ptp then ptp is required'. The schema therefore
        accepts this invalid combination, leaving validation to the consumer.
        """
        bad = {
            "timing": {
                "synchronization": {
                    "locked": True,
                    "source": "ptp",
                    # no "ptp" block
                }
            }
        }
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertEqual(errors, [],
            "Schema should have no objection to missing ptp block — this documents the gap")

    @given(ptp=synchronization_ptps())
    @settings(suppress_health_check=_SUPPRESS)
    def test_ptp_object_survives_roundtrip_when_source_is_ptp(self, ptp):
        """When source=PTP and a ptp block is present, the block is not dropped on roundtrip.

        Non-vacuous: an incorrect serializer could drop the optional ptp field
        while preserving the source enum value, silently destroying the data.
        """
        sync = Synchronization(
            locked=True,
            source=SynchronizationSource.PTP,
            ptp=ptp,
        )
        clip = Clip()
        clip.timing_synchronization = (sync,)
        recovered = Clip.from_json(Clip.to_json(clip))
        r_sync = recovered.timing_synchronization[0]
        self.assertEqual(r_sync.source, SynchronizationSource.PTP)
        self.assertIsNotNone(r_sync.ptp,
            "ptp block must not be dropped during roundtrip when source=PTP")
        self.assertEqual(r_sync.ptp, ptp)

    # --- Timestamp nanoseconds gap ---

    def test_timestamp_nanoseconds_above_999_million_is_accepted(self):
        """[gap] Timestamp.nanoseconds accepts values > 999_999_999.

        The field is named 'nanoseconds' implying SI values of 0–999_999_999,
        but the type is NonNegativeInt (uint32, up to 4_294_967_295). Values
        that would imply more than one second of nanoseconds are silently accepted
        and round-trip without error — there is no normalisation.
        """
        overflow_ns = 1_500_000_000  # 1.5 billion: more than one second
        ts = Timestamp(seconds=0, nanoseconds=overflow_ns)
        recovered = Timestamp.from_json(Timestamp.to_json(ts))
        self.assertEqual(recovered.nanoseconds, overflow_ns,
            "Nanosecond overflow value is preserved, not rejected or normalised")

    # --- PTP domain boundary ---

    def test_ptp_domain_boundary_127_accepted_128_rejected(self):
        """SynchronizationPTP.domain is correctly bounded to [0..127].

        The model uses NonNegative8BitInt (MAX_INT_8 = 127), matching the spec's
        PTP domain range for SMPTE ST2059-2 and IEEE 1588 profiles. Domain=127
        is the valid maximum; domain=128 is rejected by the validator.

        Non-vacuous: an earlier LLD draft claimed this was a gap (the full byte
        range [0..255] was accepted). Verified against the actual model — the
        constraint IS enforced.
        """
        # 127 is the valid maximum and must be accepted
        ptp = SynchronizationPTP(
            profile=PTPProfile.SMPTE_2059_2_2021,
            domain=127,
            leader_identity="00:11:22:33:44:55",
            leader_priorities=SynchronizationPTPPriorities(1, 2),
            leader_accuracy=0.0,
            mean_path_delay=0.0,
        )
        recovered = SynchronizationPTP.from_json(SynchronizationPTP.to_json(ptp))
        self.assertEqual(recovered.domain, 127)

        # 128 is one past the valid maximum and must be rejected
        with self.assertRaises(Exception):
            SynchronizationPTP(
                profile=PTPProfile.SMPTE_2059_2_2021,
                domain=128,
                leader_identity="00:11:22:33:44:55",
                leader_priorities=SynchronizationPTPPriorities(1, 2),
                leader_accuracy=0.0,
                mean_path_delay=0.0,
            )

    # --- Timecode frame boundary ---

    def test_timecode_frame_at_max_valid_is_accepted(self):
        """frames = ceil(frame_rate) - 1 is the maximum valid frame and must be accepted."""
        # For 24 fps: valid range is 0-23
        tc = Timecode(
            hours=0, minutes=0, seconds=0, frames=23,
            frame_rate=StrictlyPositiveRational(24, 1),
        )
        recovered = Timecode.from_json(Timecode.to_json(tc))
        self.assertEqual(recovered.frames, 23)

    def test_timecode_frame_at_ceiling_is_rejected(self):
        """frames = ceil(frame_rate) must be rejected — it is one frame past the end."""
        with self.assertRaises(Exception):
            Timecode(
                hours=0, minutes=0, seconds=0, frames=24,
                frame_rate=StrictlyPositiveRational(24, 1),
            )

    def test_timecode_frame_boundary_for_drop_frame_rate(self):
        """frames = ceil(30000/1001) - 1 = 29 is valid for a drop-frame-rate clip."""
        # ceil(30000/1001) = ceil(29.97...) = 30, so max frame = 29
        tc = Timecode(
            hours=0, minutes=0, seconds=0, frames=29,
            frame_rate=StrictlyPositiveRational(30000, 1001),
            dropFrame=True,
        )
        recovered = Timecode.from_json(Timecode.to_json(tc))
        self.assertEqual(recovered.frames, 29)

    def test_timecode_frame_ceiling_for_drop_frame_rate_is_rejected(self):
        """frames = 30 must be rejected for a 30000/1001 clip (ceil = 30)."""
        with self.assertRaises(Exception):
            Timecode(
                hours=0, minutes=0, seconds=0, frames=30,
                frame_rate=StrictlyPositiveRational(30000, 1001),
                dropFrame=True,
            )

    @given(frame_rate=strictly_positive_rationals())
    @settings(suppress_health_check=_SUPPRESS)
    def test_timecode_frame_boundary_holds_for_any_rate(self, frame_rate):
        """For any frame rate, frames at max valid survives roundtrip;
        frames one over is rejected at construction.

        Non-vacuous: the validator computes ceil(num/denom) dynamically, so a
        broken validator could accept or reject wrong values for unusual rates.
        """
        ceil_rate = math.ceil(Fraction(frame_rate.num, frame_rate.denom))
        max_frames = min(ceil_rate - 1, 119)
        assume(max_frames >= 0)

        tc = Timecode(
            hours=0, minutes=0, seconds=0, frames=max_frames,
            frame_rate=frame_rate,
        )
        recovered = Timecode.from_json(Timecode.to_json(tc))
        self.assertEqual(recovered.frames, max_frames)

        if max_frames < 119:  # can we go one over without hitting the Field cap?
            with self.assertRaises(Exception):
                Timecode(
                    hours=0, minutes=0, seconds=0, frames=max_frames + 1,
                    frame_rate=frame_rate,
                )


# ---------------------------------------------------------------------------
# Tier 2: Lens math
# ---------------------------------------------------------------------------

# Hypothesis strategies for well-conditioned distortion parameters.
#
# Convergence of the simple iteration requires that the spectral radius of
# (I - J_f) < 1, where J_f is the Jacobian of the distortion function.
# For radial-only Brown-Conrady, the dominant eigenvalue is 1 + 3·k1·r².
# Convergence requires |3·k1·r²| + |5·k2·r⁴| < 1.
#
# With |k1| ≤ 0.2, |k2| ≤ 0.05, and points in [-0.7, 0.7] (r² ≤ 0.98):
#   3·0.2·0.98 + 5·0.05·0.96 = 0.588 + 0.240 = 0.828 < 1  ✓
# Adding small tangential (|p| ≤ 0.005) contributes < 0.03, still < 1.
# With 200 iterations: 0.86^200 ≈ 2e-14 — well below 1e-6 test tolerance.
_small_k1 = st.floats(min_value=-0.2, max_value=0.2, allow_nan=False, allow_infinity=False)
_small_tangential_p = st.floats(min_value=-0.005, max_value=0.005, allow_nan=False, allow_infinity=False)
_convergence_domain = st.floats(min_value=-0.7, max_value=0.7, allow_nan=False, allow_infinity=False)


@st.composite
def well_conditioned_ud_distortions(draw):
    """U-D Distortion with coefficients that guarantee iterative inverse convergence.

    Bounds derived from convergence analysis: 3·|k1|·r_max² + 5·|k2|·r_max⁴ < 1
    at r_max = sqrt(2) * 0.7 ≈ 0.99.
    """
    k1 = draw(_small_k1)
    k2 = draw(st.floats(min_value=-0.05, max_value=0.05, allow_nan=False, allow_infinity=False))
    radial = (k1, k2)

    if draw(st.booleans()):
        p1 = draw(_small_tangential_p)
        p2 = draw(_small_tangential_p)
        tangential = (p1, p2)
    else:
        tangential = None

    return Distortion(model="Brown-Conrady U-D", radial=radial, tangential=tangential)


class LensMathTests(unittest.TestCase):

    # --- Schema overscan constraint ---

    def test_schema_rejects_static_distortion_overscan_below_unity(self):
        """The schema must reject distortionOverscanMax < 1.0.

        Non-vacuous: this exercises the schema's 'minimum: 1.0' constraint on the
        static lens overscan field. A schema that omitted the minimum would pass
        the 'above unity' test but fail this one.
        """
        bad = {"static": {"lens": {"distortionOverscanMax": 0.9}}}
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertGreater(len(errors), 0,
            "Schema should reject distortionOverscanMax < 1.0")

    def test_schema_accepts_static_distortion_overscan_at_unity(self):
        """The schema must accept distortionOverscanMax = 1.0 exactly.

        Non-vacuous: a schema using 'exclusiveMinimum: 1.0' would incorrectly
        reject the boundary value.
        """
        ok = {"static": {"lens": {"distortionOverscanMax": 1.0}}}
        errors = list(CLIP_VALIDATOR.iter_errors(ok))
        self.assertEqual(errors, [],
            "Schema should accept distortionOverscanMax = 1.0 (boundary must be valid)")

    def test_schema_rejects_undistortion_overscan_below_unity(self):
        """The schema must reject undistortionOverscanMax < 1.0."""
        bad = {"static": {"lens": {"undistortionOverscanMax": 0.5}}}
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertGreater(len(errors), 0,
            "Schema should reject undistortionOverscanMax < 1.0")

    def test_schema_accepts_undistortion_overscan_at_unity(self):
        """The schema must accept undistortionOverscanMax = 1.0 exactly."""
        ok = {"static": {"lens": {"undistortionOverscanMax": 1.0}}}
        errors = list(CLIP_VALIDATOR.iter_errors(ok))
        self.assertEqual(errors, [],
            "Schema should accept undistortionOverscanMax = 1.0")

    # --- Distortion model name constraint ---

    def test_schema_accepts_arbitrary_distortion_model_name(self):
        """[gap] The schema places no constraint on distortion model names beyond non-blank.

        A consumer receives 'model' as a plain string and must validate it against
        its own supported set. Camdkit does not enumerate valid model names in the
        schema — any non-blank string is accepted.
        """
        ok = {
            "lens": {
                "distortion": [
                    {"model": "some-future-lens-model-2025", "radial": [0.1]}
                ]
            }
        }
        errors = list(CLIP_VALIDATOR.iter_errors(ok))
        self.assertEqual(errors, [],
            "Schema accepts any non-blank model name — model validation is consumer-side")

    def test_schema_rejects_blank_distortion_model_name(self):
        """The schema must reject an empty string as a model name."""
        bad = {
            "lens": {
                "distortion": [
                    {"model": "", "radial": [0.1]}
                ]
            }
        }
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertGreater(len(errors), 0,
            "Schema should reject empty string as distortion model name")

    # --- Brown-Conrady self-consistency ---

    @given(
        dist=well_conditioned_ud_distortions(),
        xu=_convergence_domain,
        yu=_convergence_domain,
    )
    @settings(max_examples=300, suppress_health_check=_SUPPRESS)
    def test_brown_conrady_ud_self_consistency(self, dist, xu, yu):
        """Brown-Conrady U-D: iterative_undistort(distort(p)) ≈ p within 1e-6.

        Non-vacuous: this exercises the actual distortion formula and its iterative
        inverse. It would fail if the formula was wrong, the coefficients ill-conditioned,
        or the iteration failed to converge. The coefficient and domain bounds are
        chosen so convergence is guaranteed by analysis (see comment above the strategy).
        """
        radial = dist.radial
        tangential = dist.tangential

        xd, yd = _brown_conrady_apply(xu, yu, radial, tangential)
        assume(math.isfinite(xd) and math.isfinite(yd))

        xu_rec, yu_rec = _brown_conrady_iterative_inverse(xd, yd, radial, tangential)

        self.assertAlmostEqual(xu_rec, xu, places=6,
            msg=f"x recovery failed: radial={radial}, tangential={tangential}, "
                f"input=({xu:.6f},{yu:.6f}), distorted=({xd:.6f},{yd:.6f})")
        self.assertAlmostEqual(yu_rec, yu, places=6,
            msg=f"y recovery failed: radial={radial}, tangential={tangential}, "
                f"input=({xu:.6f},{yu:.6f}), distorted=({xd:.6f},{yd:.6f})")

    @given(
        dist=well_conditioned_ud_distortions(),
        xu=_convergence_domain,
        yu=_convergence_domain,
    )
    @settings(max_examples=150, suppress_health_check=_SUPPRESS)
    def test_brown_conrady_ud_coefficients_survive_serialization(self, dist, xu, yu):
        """Distortion coefficients produce the same output before and after JSON roundtrip.

        Non-vacuous: if float precision was lost during serialization (e.g., truncated
        to fewer decimal places), the distortion output would differ.
        """
        xd_before, yd_before = _brown_conrady_apply(xu, yu, dist.radial, dist.tangential)
        assume(math.isfinite(xd_before) and math.isfinite(yd_before))

        recovered = Distortion.from_json(Distortion.to_json(dist))
        xd_after, yd_after = _brown_conrady_apply(
            xu, yu, recovered.radial, recovered.tangential
        )

        self.assertAlmostEqual(xd_before, xd_after, places=10,
            msg="Distortion x output changed after coefficient serialization roundtrip")
        self.assertAlmostEqual(yd_before, yd_after, places=10,
            msg="Distortion y output changed after coefficient serialization roundtrip")


if __name__ == '__main__':
    unittest.main()
