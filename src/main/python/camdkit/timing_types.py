#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling of time-related metadata"""

from enum import Enum, verify, UNIQUE, StrEnum, unique
from typing import Annotated, Optional
from fractions import Fraction

from pydantic import Field, field_validator, model_validator

from camdkit.compatibility import (CompatibleBaseModel,
                                   NON_NEGATIVE_INTEGER,
                                   STRICTLY_POSITIVE_RATIONAL)
from camdkit.numeric_types import (rationalize_strictly_and_positively,
                                   StrictlyPositiveRational,
                                   NonNegative8BitInt,
                                   StrictlyPositive8BitInt,
                                   NonNegativeInt,
                                   NonNegative48BitInt, NonNegativeFloat)
from camdkit.string_types import NonBlankUTF8String
from camdkit.units import SECOND

# This was in the classic implementation, but Pydantic doesn't currently
# allow backreferences in regular expressions. Brute force it.
# PTP_LEADER_PATTERN = "[0-9a-opt_param_fn]{2}([-:]?)[0-9a-opt_param_fn]{2}(\\1[0-9a-opt_param_fn]{2}){4}$"
#
# highly recommended: regex101.com in Python mode
PTP_LEADER_PATTERN = r"(?:^[0-9a-f]{2}(?::[0-9a-f]{2}){5}$)|(?:^[0-9a-f]{2}(?:-[0-9a-f]{2}){5}$)"

@unique
class PTPProfile(StrEnum):
    IEEE_1588_2019 = "IEEE Std 1588-2019"
    IEEE_802_1AS_2020 = "IEEE Std 802.1AS-2020"
    SMPTE_2059_2_2021 = "SMPTE ST2059-2:2021"

@unique
class PTPLeaderTimeSource(StrEnum):
    GNSS = "GNSS"
    ATOMIC_CLOCK = "Atomic clock"
    NTP = "NTP"


class SynchronizationPTPPriorities(CompatibleBaseModel):
    """Data structure for PTP synchronization priorities"""
    priority1: Annotated[StrictlyPositive8BitInt, Field()]
    priority2: Annotated[StrictlyPositive8BitInt, Field()]

    def __init__(self, priority1: int, priority2: int):
        super(SynchronizationPTPPriorities, self).__init__(priority1=priority1,
                                                           priority2=priority2)
        self.priority1 = priority1
        self.priority2 = priority2


@unique
class TimingMode(StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class Timecode(CompatibleBaseModel):
    """SMPTE timecode of the sample. Timecode is a standard for labeling
    individual frames of data in media systems and is useful for
    inter-frame synchronization. Frame rate is a rational number, allowing
    drop frame rates such as that colloquially called 29.97 to be
    represented exactly, as 30000/1001. The timecode frame rate may differ
    from the sample frequency. The zero-based sub-frame field allows for finer
    division of the frame, e.g. interlaced frames have two sub-frames,
    one per field.
    """
    hours: int = Field(..., ge=0, le=23, strict=True)
    minutes: int = Field(..., ge=0, le=59, strict=True)
    seconds: int = Field(..., ge=0, le=59, strict=True)
    frames: int = Field(..., ge=0, le=119, strict=True)
    frame_rate: Annotated[StrictlyPositiveRational, Field(alias="frameRate")]
    sub_frame: Annotated[NonNegativeInt, Field(alias="subFrame", strict=True)] = 0

    # noinspection PyNestedDecorators
    @field_validator("frame_rate", mode="before")
    @classmethod
    def coerce_frame_rate_to_strictly_positive_rational(cls, v):
        return rationalize_strictly_and_positively(v)

    @model_validator(mode="after")
    def check_frames_allowed_by_format(self):
        if self.frames >= Fraction(self.frame_rate.num, self.frame_rate.denom).__ceil__():
            raise ValueError("The frame number must be less than the frame rate.")
        return self

class Timestamp(CompatibleBaseModel):
    seconds: NonNegative48BitInt
    nanoseconds: NonNegativeInt

    def __init__(self, seconds: NonNegativeInt, nanoseconds: NonNegativeInt):
        super(Timestamp, self).__init__(seconds=seconds, nanoseconds=nanoseconds)

    class Config:
        json_schema_extra = {"units": SECOND}


@verify(UNIQUE)
class SynchronizationSource(StrEnum):

    GENLOCK = "genlock"
    VIDEO_IN = "videoIn"
    PTP = "ptp"
    NTP = "ntp"


class SynchronizationOffsets(CompatibleBaseModel):

    translation: float | None = None
    rotation: float | None = None
    lensEncoders: Annotated[float | None, Field(alias="lensEncoders")] = None

    def __init__(self, translation: float, rotation: float, lensEncoders: float) -> None:
        super(SynchronizationOffsets, self).__init__(translation=translation,
                                                     rotation=rotation,
                                                     lensEncoders=lensEncoders)


class SynchronizationPTP(CompatibleBaseModel):

    profile: Annotated[PTPProfile, Field()]

    domain: Annotated[NonNegative8BitInt,
      Field(strict=True)]

    leader_identity: Annotated[NonBlankUTF8String,
      Field(pattern=PTP_LEADER_PATTERN, alias="leaderIdentity")]

    leader_priorities: Annotated[SynchronizationPTPPriorities,
      Field(alias="leaderPriorities")]

    leader_accuracy: Annotated[NonNegativeFloat,
      Field(alias="leaderAccuracy")]

    leader_time_source: Annotated[PTPLeaderTimeSource | None,
      Field(alias="leaderTimeSource")] = None

    mean_path_delay: Annotated[NonNegativeFloat,
      Field(alias="meanPathDelay")]

    vlan: Annotated[NonNegativeInt | None, Field(strict=True)] = None


class Synchronization(CompatibleBaseModel):
    locked: bool
    source: SynchronizationSource
    frequency: StrictlyPositiveRational | None = None
    offsets: SynchronizationOffsets | None = None
    present: bool | None = None
    ptp: SynchronizationPTP | None = None

    def __init__(self, locked: bool,
                 source: SynchronizationSource,
                 frequency: StrictlyPositiveRational | None = None,
                 offsets: SynchronizationOffsets | None = None,
                 present: bool | None = None,
                 ptp: SynchronizationPTP | None = None) -> None:
        super(Synchronization, self).__init__(locked=locked,
                                              source=source,
                                              frequency=frequency,
                                              offsets=offsets,
                                              present=present,
                                              ptp=ptp)

    # noinspection PyNestedDecorators
    @field_validator("frequency", mode="before")
    @classmethod
    def coerce_frequency_to_strictly_positive_rational(cls, v):
        return rationalize_strictly_and_positively(v)


class Timing(CompatibleBaseModel):
    mode: Annotated[tuple[TimingMode, ...] | None,
      Field(json_schema_extra={"clip_property": "timing_mode",
                               "constraints": "The parameter shall be one of the allowed values."})] = None
    """Enumerated value indicating whether the sample transport mechanism
    provides inherent ('external') timing, or whether the transport
    mechanism lacks inherent timing and so the sample must contain a PTP
    timestamp itself ('internal') to carry timing information.
    """

    recorded_timestamp: Annotated[tuple[Timestamp, ...] | None,
      Field(alias="recordedTimestamp",
            json_schema_extra={"clip_property": "timing_recorded_timestamp",
                               "constraints": """The parameter shall contain valid number of seconds, nanoseconds
elapsed since the start of the epoch.
"""})] = None
    """PTP timestamp of the data recording instant, provided for convenience
    during playback of e.g. pre-recorded tracking data. The timestamp
    comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
    integer (nanoseconds)
    """

    sample_rate: Annotated[tuple[StrictlyPositiveRational, ...] | None,
      Field(alias="sampleRate",
            json_schema_extra={"clip_property": "timing_sample_rate",
                               "constraints": STRICTLY_POSITIVE_RATIONAL})] = None
    """Sample frame rate as a rational number. Drop frame rates such as
    29.97 should be represented as e.g. 30000/1001. In a variable rate
    system this should is estimated from the last sample delta time.
    """

    sample_timestamp: Annotated[tuple[Timestamp, ...] | None,
      Field(alias="sampleTimestamp",
            json_schema_extra={"clip_property": "timing_sample_timestamp",
                               "constraints": """The parameter shall contain valid number of seconds, nanoseconds
elapsed since the start of the epoch.
"""})] = None
    """PTP timestamp of the data capture instant. Note this may differ
    from the packet's transmission PTP timestamp. The timestamp
    comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
    integer (nanoseconds)
    """

    sequence_number: Annotated[tuple[NonNegativeInt, ...] | None,
      Field(alias="sequenceNumber",
            json_schema_extra={"clip_property": "timing_sequence_number",
                               "constraints": NON_NEGATIVE_INTEGER})] = None
    """Integer incrementing with each sample."""

    synchronization: Annotated[tuple[Synchronization, ...] | None,
      Field(json_schema_extra={"clip_property": "timing_synchronization",
                               "constraints": "The parameter shall contain the required valid fields."})] = None
    """Object describing how the tracking device is synchronized for this
    sample.

    frequency: The frequency of a synchronization signal.This may differ from
    the sample frame rate for example in a genlocked tracking device. This is
    not required if the synchronization source is PTP or NTP.
    locked: Is the tracking device locked to the synchronization source
    offsets: Offsets in seconds between sync and sample. Critical for e.g.
    frame remapping, or when using different data sources for
    position/rotation and lens encoding
    present: Is the synchronization source present (a synchronization
    source can be present but not locked if frame rates differ for
    example)
    ptp: If the synchronization source is a PTP leader, then this object
    contains:
    - "profile": Specifies the PTP profile in use. This defines the operational
    rules and parameters for synchronization. For example "SMPTE ST2059-2:2021"
    for SMPTE 2110 based systems, or "IEEE Std 1588-2019" or
    "IEEE Std 802.1AS-2020" for industrial applications
    - "domain": Identifies the PTP domain the device belongs to. Devices in the
    same domain can synchronize with each other
    - "leaderIdentity": The unique identifier (usually MAC address) of the
    current PTP leader (grandmaster)
    - "leaderPriorities": The priority values of the leader used in the Best
    Master Clock Algorithm (BMCA). Lower values indicate higher priority
    - "priority1": Static priority set by the administrator
    - "priority2": Dynamic priority based on the leader's role or clock quality
    - "leaderAccuracy": The timing offset in seconds from the sample timestamp
    to the PTP timestamp
    - "meanPathDelay": The average round-trip delay between the device and the
    PTP leader, measured in seconds
    source: The source of synchronization must be defined as one of the
    following:
    - "vlan": Integer representing the VLAN ID for PTP traffic (e.g., 100 for
    VLAN 100)
    - "leaderTimeSource": Indicates the leader's source of time, such as GNSS, atomic
    clock, or NTP
    - "genlock": The tracking device has an external black/burst or
    tri-level analog sync signal that is triggering the capture of
    tracking samples
    - "videoIn": The tracking device has an external video signal that is
    triggering the capture of tracking samples
    - "ptp": The tracking device is locked to a PTP leader
    - "ntp": The tracking device is locked to an NTP server
    """

    timecode: Annotated[tuple[Timecode, ...] | None,
      Field(json_schema_extra={"clip_property": "timing_timecode",
                               "constraints": """The parameter shall contain a valid format and hours, minutes,
seconds and frames with appropriate min/max values.
"""})] = None

    # noinspection PyNestedDecorators
    @field_validator("sample_rate", mode="before")
    @classmethod
    def coerce_sample_rates_to_strictly_positive_rationals(cls, vs):
        if isinstance(vs, (tuple, list)):
            return tuple([rationalize_strictly_and_positively(v) for v in vs])
        return rationalize_strictly_and_positively(vs)


@unique
class Sampling(Enum):
    STATIC = 'static'
    REGULAR = 'regular'


class FrameRate(StrictlyPositiveRational):
    canonical_name: str = 'captureRate'
    sampling: Sampling = Sampling.REGULAR
    units: str = "hertz"
    section: str = "camera"
