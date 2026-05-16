#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Hypothesis strategies for camdkit types, organized bottom-up by layer."""

import math
import sys
from fractions import Fraction

from hypothesis import strategies as st, assume

from camdkit.numeric_types import (
    MAX_INT_8, MAX_UINT_8, MAX_UINT_32, MAX_UINT_48, MIN_INT_32, MAX_INT_32,
    Rational, StrictlyPositiveRational,
)
from camdkit.string_types import UUID_URN_PATTERN
from camdkit.timing_types import (
    PTPProfile, PTPLeaderTimeSource, SynchronizationSource, TimingMode,
    Timestamp, Timecode, SynchronizationPTP, SynchronizationPTPPriorities,
    SynchronizationOffsets, Synchronization,
)
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.lens_types import (
    Distortion, DistortionOffset, ProjectionOffset,
    FizEncoders, RawFizEncoders, ExposureFalloff,
)
from camdkit.camera_types import PhysicalDimensions, SenselDimensions
from camdkit.tracker_types import GlobalPosition
from camdkit.clip import Clip


# ---------------------------------------------------------------------------
# Layer 1: Primitive strategies
# ---------------------------------------------------------------------------

non_negative_8bit_ints = st.integers(min_value=0, max_value=MAX_INT_8)
non_negative_ints = st.integers(min_value=0, max_value=MAX_UINT_32)
non_negative_48bit_ints = st.integers(min_value=0, max_value=MAX_UINT_48)
strictly_positive_ints = st.integers(min_value=1, max_value=MAX_UINT_32)
sensel_ints = st.integers(min_value=0, max_value=MAX_INT_32)
uint8_ints = st.integers(min_value=0, max_value=MAX_UINT_8)

non_negative_floats = st.floats(min_value=0.0, allow_nan=False, allow_infinity=False)
strictly_positive_floats = st.floats(
    min_value=sys.float_info.epsilon, allow_nan=False, allow_infinity=False
)
normalized_floats = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
unity_or_greater_floats = st.floats(min_value=1.0, allow_nan=False, allow_infinity=False)
reals = st.floats(allow_nan=False, allow_infinity=False)
shutter_angle_floats = st.floats(min_value=0.0, max_value=360.0, allow_nan=False, allow_infinity=False)


# ---------------------------------------------------------------------------
# Layer 2: Rational types
# ---------------------------------------------------------------------------

@st.composite
def rationals(draw):
    num = draw(st.integers(min_value=MIN_INT_32, max_value=MAX_INT_32))
    denom = draw(st.integers(min_value=1, max_value=MAX_UINT_32))
    return Rational(num, denom)


@st.composite
def strictly_positive_rationals(draw):
    num = draw(st.integers(min_value=1, max_value=MAX_INT_32))
    denom = draw(st.integers(min_value=1, max_value=MAX_UINT_32))
    return StrictlyPositiveRational(num, denom)


# ---------------------------------------------------------------------------
# Layer 3: String types and geometric types
# ---------------------------------------------------------------------------

@st.composite
def non_blank_utf8_strings(draw):
    return draw(st.text(
        min_size=1, max_size=50,
        alphabet=st.characters(blacklist_categories=('Cs',))
    ))


uuid_urns = st.from_regex(UUID_URN_PATTERN, fullmatch=True)

# MAC address in colon-separated form, always valid per PTP_LEADER_PATTERN
ptp_leader_identities = st.builds(
    lambda octets: ':'.join(octets),
    octets=st.lists(
        st.integers(min_value=0, max_value=255).map(lambda x: f"{x:02x}"),
        min_size=6, max_size=6,
    )
)


@st.composite
def vector3s(draw):
    return Vector3(draw(reals), draw(reals), draw(reals))


@st.composite
def rotator3s(draw):
    return Rotator3(draw(reals), draw(reals), draw(reals))


@st.composite
def transforms(draw):
    t = Transform(translation=draw(vector3s()), rotation=draw(rotator3s()))
    if draw(st.booleans()):
        t.scale = draw(vector3s())
    if draw(st.booleans()):
        t.id = draw(non_blank_utf8_strings())
    return t


# ---------------------------------------------------------------------------
# Layer 4: Camera/sensor and lens types
# ---------------------------------------------------------------------------

@st.composite
def physical_dimensions(draw):
    return PhysicalDimensions(
        width=draw(non_negative_floats),
        height=draw(non_negative_floats),
    )


@st.composite
def sensel_dimensions(draw):
    return SenselDimensions(
        width=draw(sensel_ints),
        height=draw(sensel_ints),
    )


@st.composite
def global_positions(draw):
    return GlobalPosition(
        E=draw(reals), N=draw(reals), U=draw(reals),
        lat0=draw(reals), lon0=draw(reals), h0=draw(reals),
    )


@st.composite
def distortions(draw):
    radial = tuple(draw(st.lists(reals, min_size=1, max_size=6)))
    tangential = draw(st.one_of(
        st.none(),
        st.lists(reals, min_size=1, max_size=4).map(tuple),
    ))
    # model=None is excluded by exclude_none but the default "Brown-Conrady D-U"
    # is restored on deserialization, breaking the roundtrip. Only generate non-None.
    model_name = draw(st.one_of(
        st.just("Brown-Conrady D-U"),
        st.just("Brown-Conrady U-D"),
    ))
    overscan = draw(st.one_of(st.none(), unity_or_greater_floats))
    return Distortion(model=model_name, radial=radial, tangential=tangential, overscan=overscan)


@st.composite
def distortion_offsets(draw):
    return DistortionOffset(draw(reals), draw(reals))


@st.composite
def projection_offsets(draw):
    return ProjectionOffset(draw(reals), draw(reals))


@st.composite
def fiz_encoders(draw):
    focus = draw(st.one_of(st.none(), normalized_floats))
    iris = draw(st.one_of(st.none(), normalized_floats))
    zoom = draw(st.one_of(st.none(), normalized_floats))
    if focus is None and iris is None and zoom is None:
        target = draw(st.sampled_from(['focus', 'iris', 'zoom']))
        val = draw(normalized_floats)
        if target == 'focus':
            focus = val
        elif target == 'iris':
            iris = val
        else:
            zoom = val
    return FizEncoders(focus=focus, iris=iris, zoom=zoom)


@st.composite
def raw_fiz_encoders(draw):
    focus = draw(st.one_of(st.none(), non_negative_ints))
    iris = draw(st.one_of(st.none(), non_negative_ints))
    zoom = draw(st.one_of(st.none(), non_negative_ints))
    if focus is None and iris is None and zoom is None:
        target = draw(st.sampled_from(['focus', 'iris', 'zoom']))
        val = draw(non_negative_ints)
        if target == 'focus':
            focus = val
        elif target == 'iris':
            iris = val
        else:
            zoom = val
    return RawFizEncoders(focus=focus, iris=iris, zoom=zoom)


@st.composite
def exposure_falloffs(draw):
    return ExposureFalloff(
        a1=draw(reals),
        a2=draw(st.one_of(st.none(), reals)),
        a3=draw(st.one_of(st.none(), reals)),
    )


# ---------------------------------------------------------------------------
# Layer 5: Timing types
# ---------------------------------------------------------------------------

@st.composite
def timestamps(draw):
    return Timestamp(draw(non_negative_48bit_ints), draw(non_negative_ints))


@st.composite
def timecodes(draw):
    frame_rate = draw(strictly_positive_rationals())
    ceil_rate = math.ceil(Fraction(frame_rate.num, frame_rate.denom))
    max_frames = min(ceil_rate - 1, 119)
    assume(max_frames >= 0)
    return Timecode(
        hours=draw(st.integers(min_value=0, max_value=23)),
        minutes=draw(st.integers(min_value=0, max_value=59)),
        seconds=draw(st.integers(min_value=0, max_value=59)),
        frames=draw(st.integers(min_value=0, max_value=max_frames)),
        frame_rate=frame_rate,
        sub_frame=draw(non_negative_ints),
        dropFrame=draw(st.booleans()),
    )


@st.composite
def synchronization_ptp_priorities(draw):
    return SynchronizationPTPPriorities(draw(uint8_ints), draw(uint8_ints))


@st.composite
def synchronization_ptps(draw):
    return SynchronizationPTP(
        profile=draw(st.sampled_from(PTPProfile)),
        domain=draw(non_negative_8bit_ints),
        leader_identity=draw(ptp_leader_identities),
        leader_priorities=draw(synchronization_ptp_priorities()),
        leader_accuracy=draw(non_negative_floats),
        leader_time_source=draw(st.one_of(st.none(), st.sampled_from(PTPLeaderTimeSource))),
        mean_path_delay=draw(non_negative_floats),
        vlan=draw(st.one_of(st.none(), non_negative_ints)),
    )


@st.composite
def synchronization_offsets(draw):
    return SynchronizationOffsets(
        translation=draw(reals),
        rotation=draw(reals),
        lensEncoders=draw(reals),
    )


@st.composite
def synchronizations(draw):
    return Synchronization(
        locked=draw(st.booleans()),
        source=draw(st.sampled_from(SynchronizationSource)),
        frequency=draw(st.one_of(st.none(), strictly_positive_rationals())),
        offsets=draw(st.one_of(st.none(), synchronization_offsets())),
        present=draw(st.one_of(st.none(), st.booleans())),
        ptp=draw(st.one_of(st.none(), synchronization_ptps())),
    )


# ---------------------------------------------------------------------------
# Layer 6: Clip
# ---------------------------------------------------------------------------

def _tuple_of(strategy, n):
    """Draw a tuple of n elements from strategy."""
    return st.tuples(*[strategy] * n)


@st.composite
def clips(draw):
    clip = Clip()

    # Static: global
    if draw(st.booleans()):
        clip.duration = draw(strictly_positive_rationals())

    # Static: camera
    if draw(st.booleans()):
        clip.capture_frame_rate = draw(strictly_positive_rationals())
    if draw(st.booleans()):
        clip.anamorphic_squeeze = draw(strictly_positive_rationals())
    if draw(st.booleans()):
        clip.active_sensor_physical_dimensions = draw(physical_dimensions())
    if draw(st.booleans()):
        clip.active_sensor_resolution = draw(sensel_dimensions())
    if draw(st.booleans()):
        clip.camera_make = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.camera_model = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.camera_serial_number = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.camera_firmware = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.camera_label = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.iso = draw(strictly_positive_ints)
    if draw(st.booleans()):
        clip.fdl_link = draw(uuid_urns)
    if draw(st.booleans()):
        clip.shutter_angle = draw(shutter_angle_floats)

    # Static: lens
    if draw(st.booleans()):
        clip.lens_make = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.lens_model = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.lens_serial_number = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.lens_firmware = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.lens_nominal_focal_length = draw(strictly_positive_floats)
    if draw(st.booleans()):
        clip.lens_distortion_overscan_max = draw(unity_or_greater_floats)
    if draw(st.booleans()):
        clip.lens_undistortion_overscan_max = draw(unity_or_greater_floats)

    # Static: tracker
    if draw(st.booleans()):
        clip.tracker_make = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.tracker_model = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.tracker_serial_number = draw(non_blank_utf8_strings())
    if draw(st.booleans()):
        clip.tracker_firmware = draw(non_blank_utf8_strings())

    # Dynamic fields: all tuples share the same length n
    n = draw(st.integers(min_value=1, max_value=3))

    # Dynamic: lens
    if draw(st.booleans()):
        clip.lens_t_number = draw(_tuple_of(strictly_positive_floats, n))
    if draw(st.booleans()):
        clip.lens_f_number = draw(_tuple_of(strictly_positive_floats, n))
    if draw(st.booleans()):
        clip.lens_pinhole_focal_length = draw(_tuple_of(strictly_positive_floats, n))
    if draw(st.booleans()):
        clip.lens_focus_distance = draw(_tuple_of(strictly_positive_floats, n))
    if draw(st.booleans()):
        clip.lens_entrance_pupil_offset = draw(_tuple_of(reals, n))
    if draw(st.booleans()):
        clip.lens_encoders = draw(_tuple_of(fiz_encoders(), n))
    if draw(st.booleans()):
        clip.lens_raw_encoders = draw(_tuple_of(raw_fiz_encoders(), n))
    if draw(st.booleans()):
        clip.lens_exposure_falloff = draw(_tuple_of(exposure_falloffs(), n))
    if draw(st.booleans()):
        one_frame_distortions = st.lists(distortions(), min_size=1).map(tuple)
        clip.lens_distortions = draw(_tuple_of(one_frame_distortions, n))
    if draw(st.booleans()):
        clip.lens_distortion_offset = draw(_tuple_of(distortion_offsets(), n))
    if draw(st.booleans()):
        clip.lens_projection_offset = draw(_tuple_of(projection_offsets(), n))

    # Dynamic: timing
    if draw(st.booleans()):
        clip.timing_mode = draw(_tuple_of(st.sampled_from(TimingMode), n))
    if draw(st.booleans()):
        clip.timing_sample_timestamp = draw(_tuple_of(timestamps(), n))
    if draw(st.booleans()):
        clip.timing_recorded_timestamp = draw(_tuple_of(timestamps(), n))
    if draw(st.booleans()):
        clip.timing_sequence_number = draw(_tuple_of(non_negative_ints, n))
    if draw(st.booleans()):
        clip.timing_sample_rate = draw(_tuple_of(strictly_positive_rationals(), n))
    if draw(st.booleans()):
        clip.timing_timecode = draw(_tuple_of(timecodes(), n))
    if draw(st.booleans()):
        clip.timing_synchronization = draw(_tuple_of(synchronizations(), n))

    # Dynamic: tracker
    if draw(st.booleans()):
        clip.tracker_status = draw(_tuple_of(non_blank_utf8_strings(), n))
    if draw(st.booleans()):
        clip.tracker_recording = draw(_tuple_of(st.booleans(), n))
    if draw(st.booleans()):
        clip.tracker_slate = draw(_tuple_of(non_blank_utf8_strings(), n))
    if draw(st.booleans()):
        clip.tracker_notes = draw(_tuple_of(non_blank_utf8_strings(), n))

    # Dynamic: global
    if draw(st.booleans()):
        clip.sample_id = draw(_tuple_of(uuid_urns, n))
    if draw(st.booleans()):
        clip.source_id = draw(_tuple_of(uuid_urns, n))
    if draw(st.booleans()):
        clip.source_number = draw(_tuple_of(non_negative_ints, n))
    if draw(st.booleans()):
        clip.related_sample_ids = draw(
            _tuple_of(st.lists(uuid_urns, min_size=1).map(tuple), n)
        )
    if draw(st.booleans()):
        clip.global_stage = draw(_tuple_of(global_positions(), n))
    if draw(st.booleans()):
        one_frame_transforms = st.lists(transforms(), min_size=1).map(tuple)
        clip.transforms = draw(_tuple_of(one_frame_transforms, n))

    return clip
