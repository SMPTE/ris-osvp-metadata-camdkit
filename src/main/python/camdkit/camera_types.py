#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for camera modeling"""

from typing import Annotated

from pydantic import Field, field_validator

from camdkit.compatibility import (CompatibleBaseModel,
                                   NONBLANK_UTF8_MAX_1023_CHARS,
                                   UUID_URN,
                                   STRICTLY_POSITIVE_RATIONAL,
                                   STRICTLY_POSITIVE_INTEGER,)
from camdkit.numeric_types import (MAX_INT_32,
                                   StrictlyPositiveInt,
                                   StrictlyPositiveRational,
                                   rationalize_strictly_and_positively)
from camdkit.units import MILLIMETER, PIXEL, HERTZ, DEGREE
from camdkit.string_types import NonBlankUTF8String, UUIDURN

# Tempting as it might seem to make PhysicalDimensions and SenselDimensions subclasses
# of a single generic Dimension[T] class, that doesn't work play well with the Field
# annotations, unfortunately. Maybe someone smart will figure out how to make this idea
# work, but for now it's a wish, not something for a to-do list.


class PhysicalDimensions(CompatibleBaseModel):
    """Height and width of the active area of the camera sensor in millimeters
    """
    height: Annotated[float, Field(ge=0.0, strict=True)]
    width: Annotated[float, Field(ge=0.0, strict=True)]

    class Config:
        json_schema_extra = {"units": MILLIMETER}

    def __init__(self, width: float, height: float) -> None:
        super(PhysicalDimensions, self).__init__(width=width, height=height)


class SenselDimensions(CompatibleBaseModel):
    """Photosite resolution of the active area of the camera sensor in pixels"""
    height: Annotated[int, Field(ge=0, le=MAX_INT_32)]
    width: Annotated[int, Field(ge=0, le=MAX_INT_32)]

    class Config:
        json_schema_extra = {"units": PIXEL}

    def __init__(self, width: int, height: int) -> None:
        super(SenselDimensions, self).__init__(width=width, height=height)


ShutterAngle = Annotated[float, Field(ge=0.0, le=360.0, strict=True)]


class StaticCamera(CompatibleBaseModel):
    capture_frame_rate: Annotated[StrictlyPositiveRational | None,
      Field(alias="captureFrameRate",
          json_schema_extra={"units": HERTZ,
                             "clip_property": "capture_frame_rate",
                             "constraints": STRICTLY_POSITIVE_RATIONAL})] = None
    """Capture frame rate of the camera"""

    active_sensor_physical_dimensions: Annotated[PhysicalDimensions | None,
      Field(alias="activeSensorPhysicalDimensions",
            json_schema_extra={"clip_property": 'active_sensor_physical_dimensions',
                               "constraints": "The height and width shall be each be real non-negative numbers."})] = None

    active_sensor_resolution: Annotated[SenselDimensions | None,
      Field(alias="activeSensorResolution",
            json_schema_extra={"clip_property": 'active_sensor_resolution',
                               "constraints": """The height and width shall be each be an integer in the range
[0..2,147,483,647].
"""})] = None

    make: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "camera_make",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """
    Non-blank string naming camera manufacturer
    """

    model: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "camera_model",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying camera model"""

    serial_number: Annotated[NonBlankUTF8String | None,
      Field(alias="serialNumber",
            json_schema_extra={"clip_property": "camera_serial_number",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string uniquely identifying the camera"""

    firmware_version: Annotated[NonBlankUTF8String | None,
      Field(alias="firmwareVersion",
            json_schema_extra={"clip_property": "camera_firmware",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying camera firmware version"""

    label: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "camera_label",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string containing user-determined camera identifier"""

    anamorphic_squeeze: Annotated[StrictlyPositiveRational | None,
      Field(alias="anamorphicSqueeze",
            json_schema_extra={"clip_property": "anamorphic_squeeze",
                               "constraints": STRICTLY_POSITIVE_RATIONAL})] = None
    """Nominal ratio of height to width of the image of an axis-aligned
    square captured by the camera sensor. It can be used to de-squeeze
    images but is not however an exact number over the entire captured
    area due to a lens' intrinsic analog nature.
    """

    iso: Annotated[StrictlyPositiveInt | None,
      Field(alias="isoSpeed",
            json_schema_extra={"clip_property": "iso",
                               "constraints": STRICTLY_POSITIVE_INTEGER})] = None
    """Arithmetic ISO scale as defined in ISO 12232"""

    fdl_link: Annotated[UUIDURN | None,
    Field(alias="fdlLink",
          json_schema_extra={"clip_property": "fdl_link",
                             "constraints": UUID_URN})] = None
    """URN identifying the ASC Framing Decision List used by the camera."""

    shutter_angle: Annotated[ShutterAngle | None,
    Field(alias="shutterAngle",
          json_schema_extra={"units": DEGREE,
                             "clip_property": "shutter_angle",
                             "constraints": "The parameter shall be a real number in the range (0..360]."})] = None
    """Shutter speed as a fraction of the capture frame rate. The shutter
    speed (in units of 1/s) is equal to the value of the parameter divided
    by 360 times the capture frame rate.
    """

    # noinspection PyNestedDecorators
    @field_validator("capture_frame_rate", "anamorphic_squeeze", mode="before")
    @classmethod
    def coerce_camera_type_to_strictly_positive_rational(cls, v):
        return rationalize_strictly_and_positively(v)
