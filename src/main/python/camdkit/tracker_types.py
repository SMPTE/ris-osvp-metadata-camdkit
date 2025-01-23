#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling of tracker-related metadata"""

from typing import Annotated

from pydantic import Field

from camdkit.string_types import NonBlankUTF8String
from camdkit.compatibility import (CompatibleBaseModel,
                                   BOOLEAN,
                                   NONBLANK_UTF8_MAX_1023_CHARS)


class StaticTracker(CompatibleBaseModel):
    make: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "tracker_make",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string naming tracking device manufacturer"""

    model: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "tracker_model",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying tracking device model"""

    serial_number: Annotated[NonBlankUTF8String | None,
      Field(alias="serialNumber",
            json_schema_extra={"clip_property": "tracker_serial_number",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string uniquely identifying the tracking device"""

    firmware: Annotated[NonBlankUTF8String | None,
      Field(alias="firmwareVersion",
            json_schema_extra={"clip_property": "tracker_firmware",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying tracking device firmware version"""

    # def __init__(self, make: NonBlankUTF8String | None,
    #              modelName: NonBlankUTF8String | None,
    #              serialNumber: NonBlankUTF8String | None,
    #              firmwareVersion: NonBlankUTF8String | None):
    #     super(StaticTracker, self).__init__(make=make,
    #                                         modelName=modelName,
    #                                         serialNumber=serialNumber,
    #                                         firmwareVersion=firmwareVersion)


class Tracker(CompatibleBaseModel):
    notes: Annotated[tuple[NonBlankUTF8String, ...] | None,
      Field(json_schema_extra={"clip_property": "tracker_notes",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string containing notes about tracking system"""

    recording: Annotated[tuple[bool, ...] | None,
      Field(json_schema_extra={"clip_property": "tracker_recording",
                               "constraints": BOOLEAN})] = None
    """Boolean indicating whether tracking system is recording data"""

    slate: Annotated[tuple[NonBlankUTF8String, ...] | None,
      Field(json_schema_extra={"clip_property": "tracker_slate",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string describing the recording slate"""

    status: Annotated[tuple[NonBlankUTF8String, ...] | None,
      Field(json_schema_extra={"clip_property": "tracker_status",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string describing status of tracking system"""


class GlobalPosition(CompatibleBaseModel):
    """Global ENU and geodetic coördinates
    Reference:. https://en.wikipedia.org/wiki/Local_tangent_plane_coordinates
    """
    E: float  # East (meters)
    N: float  # North (meters)
    U: float  # Up (meters)
    lat0: float  # latitude (degrees)
    lon0: float  # longitude (degrees)
    h0: float  # height (meters)

    def __init__(self, E: float, N: float, U: float, lat0: float, lon0: float, h0: float):
        super(GlobalPosition, self).__init__(E=E, N=N, U=U, lat0=lat0, lon0=lon0, h0=h0)
