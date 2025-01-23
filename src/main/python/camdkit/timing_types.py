#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling of time-related metadata"""

from enum import Enum, verify, UNIQUE, StrEnum
from typing import Annotated, Optional
from fractions import Fraction

from pydantic import Field, field_validator, model_validator

from camdkit.compatibility import (CompatibleBaseModel,
                                   NON_NEGATIVE_INTEGER,
                                   STRICTLY_POSITIVE_RATIONAL)
from camdkit.numeric_types import (rationalize_strictly_and_positively,
                                   StrictlyPositiveRational,
                                   NonNegative8BitInt,
                                   NonNegativeInt,
                                   NonNegative48BitInt)
from camdkit.units import SECOND

# This was in the classic implementation, but Pydantic doesn't currently
# allow backreferences in regular expressions. Brute force it.
# PTP_LEADER_PATTERN = "[0-9a-opt_param_fn]{2}([-:]?)[0-9a-opt_param_fn]{2}(\\1[0-9a-opt_param_fn]{2}){4}$"
#
# highly recommended: regex101.com in Python mode
PTP_LEADER_PATTERN = r"(?:^[0-9a-f]{2}(?::[0-9a-f]{2}){5}$)|(?:^[0-9a-f]{2}(?:-[0-9a-f]{2}){5}$)"

class TimingMode(StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class TimecodeFormat(CompatibleBaseModel):
    """The timecode format is defined as a rational frame rate and - where a
    signal with sub-frames is described, such as an interlaced signal - an
    index of which sub-frame is referred to by the timecode.
    """
    frame_rate: Annotated[StrictlyPositiveRational, Field(alias="frameRate")]
    sub_frame: Annotated[NonNegativeInt, Field(alias="subFrame", strict=True)] = 0

    # noinspection PyNestedDecorators
    @field_validator("frame_rate", mode="before")
    @classmethod
    def coerce_frame_rate_to_strictly_positive_rational(cls, v):
        return rationalize_strictly_and_positively(v)

    # TODO investigate the mismatch between the keyword arg and the field name;
    #   isn't this one of those ugly cases wher ethe field name needs to be capitalCase?
    def __init__(self, frameRate: StrictlyPositiveRational, subFrame: int = 0):
        super(TimecodeFormat, self).__init__(frameRate=frameRate, subFrame=subFrame)

    def to_int(self) -> int:
        return Fraction(self.frame_rate.num, self.frame_rate.denom).__ceil__()


class Timecode(CompatibleBaseModel):
    """SMPTE timecode of the sample. Timecode is a standard for labeling
    individual frames of data in media systems and is useful for
    inter-frame synchronization.
    - format.frameRate: The frame rate as a rational number. Drop frame
    rates such as 29.97 should be represented as e.g. 30000/1001. The
    timecode frame rate may differ from the sample frequency.
    """
    hours: int = Field(..., ge=0, le=23, strict=True)
    minutes: int = Field(..., ge=0, le=59, strict=True)
    seconds: int = Field(..., ge=0, le=59, strict=True)
    frames: int = Field(..., ge=0, le=119, strict=True)
    format: TimecodeFormat

    def __init__(self, hours: int, minutes: int, seconds: int, frames: int, format: TimecodeFormat):
        super(Timecode, self).__init__(hours=hours, minutes=minutes, seconds=seconds, frames=frames,
                                       format=format)

    @model_validator(mode="after")
    def check_frames_allowed_by_format(self):
        if self.frames >= self.format.to_int():
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

    domain: NonNegative8BitInt | None = None
    leader: Annotated[str | None, Field(pattern=PTP_LEADER_PATTERN)] = None
    offset: Annotated[float | None, Field(strict=True)] = None

    def __init__(self, domain: Optional[int] = None,
                 leader: Optional[str] = None,
                 offset: Optional[float] = None) -> None:
        super(SynchronizationPTP, self).__init__(domain=domain, leader=leader, offset=offset)


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
    - "leader": The MAC address of the PTP leader
    - "offset": The timing offset in seconds from the sample timestamp to
    the PTP timestamp
    - "domain": The PTP domain number
    source: The source of synchronization must be defined as one of the
    following:
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


class Sampling(Enum):
    STATIC = 'static'
    REGULAR = 'regular'


class FrameRate(StrictlyPositiveRational):
    canonical_name: str = 'captureRate'
    sampling: Sampling = Sampling.REGULAR
    units: str = "hertz"
    section: str = "camera"
