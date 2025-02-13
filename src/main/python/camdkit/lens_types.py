#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for lens modeling"""

from typing import Annotated, Self, Optional

from pydantic import Field, model_validator

from camdkit.compatibility import (CompatibleBaseModel,
                                   BOOLEAN,
                                   NONBLANK_UTF8_MAX_1023_CHARS,
                                   NON_NEGATIVE_REAL,
                                   STRICTLY_POSITIVE_REAL,
                                   REAL,
                                   REAL_AT_LEAST_UNITY,
                                   ARRAY)
from camdkit.numeric_types import (StrictlyPositiveFloat, NormalizedFloat,
                                   NonNegativeInt, UnityOrGreaterFloat, NonNegativeFloat)
from camdkit.string_types import NonBlankUTF8String
from camdkit.units import MILLIMETER, METER


class StaticLens(CompatibleBaseModel):
    distortion_overscan_max: Annotated[UnityOrGreaterFloat | None,
      Field(alias="distortionOverscanMax",
            json_schema_extra={"clip_property": "lens_distortion_overscan_max",
                               "constraints": REAL_AT_LEAST_UNITY})] = None
    """Static maximum overscan factor on lens distortion. This is primarily
    relevant when storing overscan values, not in transmission as the
    overscan should be calculated by the consumer.
    """

    undistortion_overscan_max: Annotated[UnityOrGreaterFloat | None,
      Field(alias="undistortionOverscanMax",
            json_schema_extra={"clip_property": "lens_undistortion_overscan_max",
                               "constraints": REAL_AT_LEAST_UNITY})] = None
    """Static maximum overscan factor on lens undistortion. This is primarily
    relevant when storing overscan values, not in transmission as the
    overscan should be calculated by the consumer.
    """

    distortion_is_projection: Annotated[bool | None,
      Field(alias="distortionIsProjection",
            json_schema_extra={"clip_property": "lens_distortion_is_projection",
                               "constraints": BOOLEAN})] = None
    """Indicator that the OpenLensIO distortion model is the Projection
    Characterization, not the Field-Of-View Characterization. This is 
    primarily relevant when storing overscan values, not in transmission
    as the overscan should be calculated by the consumer.
    """

    make: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "lens_make",
    "constraints": NONBLANK_UTF8_MAX_1023_CHARS})]= None
    """Non-blank string naming lens manufacturer"""

    model: Annotated[NonBlankUTF8String | None,
      Field(json_schema_extra={"clip_property": "lens_model",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying lens model"""

    serial_number: Annotated[NonBlankUTF8String | None,
      Field(alias="serialNumber",
            json_schema_extra={"clip_property": "lens_serial_number",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string uniquely identifying the lens"""

    firmware_version: Annotated[NonBlankUTF8String | None,
      Field(alias="firmwareVersion",
            json_schema_extra={"clip_property": "lens_firmware",
                               "constraints": NONBLANK_UTF8_MAX_1023_CHARS})] = None
    """Non-blank string identifying lens firmware version"""

    nominal_focal_length: Annotated[StrictlyPositiveFloat | None,
      Field(alias="nominalFocalLength",
            json_schema_extra={"units": MILLIMETER,
                               "clip_property": "lens_nominal_focal_length",
                               "constraints": STRICTLY_POSITIVE_REAL})] = None
    """Nominal focal length of the lens. The number printed on the side
    of a prime lens, e.g. 50 mm, and undefined in the case of a zoom lens.
    """
    calibration_history: Annotated[tuple[str, ...] | None,
      Field(alias="calibrationHistory",
            json_schema_extra={"clip_property": "lens_calibration_history",
                               "type": "array",
                               "items":
                               { "type": "string", "minLength": 1, "maxLength": 1023 }
                               })] = None
    """List of free strings that describe the history of calibrations of the lens."""


class Distortion(CompatibleBaseModel):
    # TODO ask the group about strictness of type checking.
    #    Let Pydantic convert silently?
    #    Restore strict=True?
    #    Change type to typing.Sequence? collections.abc.Sequence or collections.abc.MutableSequence?
    # radial: Annotated[tuple[float, ...], Field(strict=True)]
    # tangential: Annotated[tuple[float, ...] | None, Field(strict=True)] = None
    radial: Annotated[tuple[float, ...], Field(min_length=1)]
    tangential: Annotated[tuple[float, ...] | None, Field(min_length=1)] = None
    model: NonBlankUTF8String | None = None

    @model_validator(mode="after")
    def check_tuples_not_empty(self) -> Self:
        if self.radial is not None and len(self.radial) == 0:
            raise ValueError("radial distortion coefficient sequence must not be empty")
        if self.tangential is not None and len(self.tangential) == 0:
            raise ValueError("tangential distortion coefficient sequence, if provided, must not be empty")
        return self

    def __init__(self, radial: tuple[float, ...],  # positional __init__() for compatibility
                 tangential: tuple[float, ...] | None = None,
                 model: str | None = None):
        super(Distortion, self).__init__(radial=radial, tangential=tangential, model=model)


Distortions = Annotated[tuple[Distortion, ...], Field(min_length=1)]

class PlanarOffset(CompatibleBaseModel):
    x: float
    y: float

    def __init__(self, x: float, y: float):
        super(PlanarOffset, self).__init__(x=x, y=y)

class DistortionOffset(PlanarOffset):

    def __init__(self, x: float, y: float):
        super(DistortionOffset, self).__init__(x=x, y=y)

class ProjectionOffset(PlanarOffset):

    def __init__(self, x: float, y: float):
        super(ProjectionOffset, self).__init__(x=x, y=y)


class FizEncoders(CompatibleBaseModel):
    focus: NormalizedFloat | None = None
    iris: NormalizedFloat | None = None
    zoom: NormalizedFloat | None = None

    def __init__(self, focus: Optional[float] = None,
                 iris: Optional[float] = None,
                 zoom: Optional[float] = None):
        super(FizEncoders, self).__init__(focus=focus, iris=iris, zoom=zoom)
        if self.focus is None and self.iris is None and self.zoom is None:
            raise ValueError("FizEncoders requires at least one of focus or iris or zoom")


class RawFizEncoders(CompatibleBaseModel):
    focus: NonNegativeInt | None = None
    iris: NonNegativeInt | None = None
    zoom: NonNegativeInt | None = None

    def __init__(self, focus: Optional[NonNegativeInt] = None,
                 iris: Optional[NonNegativeInt] = None,
                 zoom: Optional[NonNegativeInt] = None):
        super(RawFizEncoders, self).__init__(focus=focus, iris=iris, zoom=zoom)
        if self.focus is None and self.iris is None and self.zoom is None:
            raise ValueError("RawFizEncoders requires at least one of focus or iris or zoom")

class ExposureFalloff(CompatibleBaseModel):
    a1: float
    a2: float | None = None
    a3: float | None = None

    def __init__(self, a1: float, a2: float | None = None, a3: float | None = None):
        super(ExposureFalloff, self).__init__(a1=a1, a2=a2, a3=a3)


class Lens(CompatibleBaseModel):
    custom: Annotated[tuple[tuple[float, ...], ...] | None,
      Field(json_schema_extra={"clip_property": "lens_custom",
                               "constraints": ARRAY})] = None
    """This list provides optional additional custom coefficients that can 
    extend the existing lens model. The meaning of and how these characteristics
    are to be applied to a virtual camera would require negotiation between a
    particular producer and consumer.
    """

    distortion: Annotated[tuple[Distortions, ...] | None,
      Field(min_length=1,
            json_schema_extra={"clip_property": "lens_distortions",
                               "constraints": """The list shall contain at least one Distortion object, and in each
object the radial and tangential coefficients shall each be real numbers.
"""})] = None
    """A list of Distortion objects that each define the coefficients for
    calculating the distortion characteristics of a lens comprising radial
    distortion coefficients of the spherical distortion (k1-N) and the
    tangential distortion (p1-N). An optional key 'model' can be used that
    describes the distortion model. The default is Brown-Conrady D-U (that
    maps Distorted to Undistorted coordinates).
    """

    distortion_overscan: Annotated[tuple[UnityOrGreaterFloat, ...] | None,
      Field(alias="distortionOverscan",
            json_schema_extra={"clip_property": "lens_distortion_overscan",
                               "constraints": REAL_AT_LEAST_UNITY})] = None
    """Overscan factor on lens distortion. This is primarily relevant when
    storing overscan values, not in transmission as the overscan should be
    calculated by the consumer.
    """

    undistortion_overscan: Annotated[tuple[UnityOrGreaterFloat, ...] | None,
      Field(alias="undistortionOverscan",
            json_schema_extra={"clip_property": "lens_undistortion_overscan",
                               "constraints": REAL_AT_LEAST_UNITY})] = None
    """Overscan factor on lens undistortion. This is primarily relevant when
    storing overscan values, not in transmission as the overscan should be
    calculated by the consumer.
    """

    distortion_offset: Annotated[tuple[DistortionOffset, ...] | None,
      Field(alias="distortionOffset",
            json_schema_extra={"units": MILLIMETER,
                               "clip_property": "lens_distortion_offset",
                               "constraints": "X and Y centre shift shall each be real numbers."})] = None
    """Offset in x and y of the centre of distortion of the virtual camera
    """

    encoders: Annotated[tuple[FizEncoders, ...] | None,
      Field(json_schema_extra={"clip_property": "lens_encoders",
                               "anyOf": [{"required": ["focus"]},
                                         {"required": ["iris"]},
                                         {"required": ["zoom"]}],
                               "constraints": """
The parameter shall contain at least one normalised values (0..1) for the FIZ encoders.
"""})] = None
    """Normalised real numbers (0-1) for focus, iris and zoom.
    Encoders are represented in this way (as opposed to raw integer
    values) to ensure values remain independent of encoder resolution,
    minimum and maximum (at an acceptable loss of precision).
    These values are only relevant in lenses with end-stops that
    demarcate the 0 and 1 range.
    Value should be provided in the following directions (if known):
    Focus:   0=infinite     1=closest
    Iris:    0=open         1=closed
    Zoom:    0=wide angle   1=telephoto
    """

    entrance_pupil_offset: Annotated[tuple[float, ...] | None,
      Field(alias="entrancePupilOffset",
            json_schema_extra={"units": METER,
                               "clip_property": "lens_entrance_pupil_offset",
                               "constraints": REAL})] = None
    """Offset of the entrance pupil relative to the nominal imaging plane
    (positive if the entrance pupil is located on the side of the nominal
    imaging plane that is towards the object, and negative otherwise).
    Measured in meters as in a render engine it is often applied in the
    virtual camera's transform chain.
    """

    exposure_falloff: Annotated[tuple[ExposureFalloff, ...] | None,
      Field(alias="exposureFalloff",
            json_schema_extra={"clip_property": "lens_exposure_falloff",
                               "constraints": "The coefficients shall each be real numbers."})] = None
    """Coefficients for calculating the exposure fall-off (vignetting) of
    a lens
    """

    f_number: Annotated[tuple[NonNegativeFloat, ...] | None,
      Field(alias="fStop",
            json_schema_extra={"clip_property": "lens_f_number",
                               "constraints": NON_NEGATIVE_REAL})] = None
    """The linear f-number of the lens, equal to the focal length divided
    by the diameter of the entrance pupil.
    """

    pinhole_focal_length: Annotated[tuple[NonNegativeFloat, ...] | None,
      Field(alias="pinholeFocalLength",
            json_schema_extra={"units": MILLIMETER,
                               "clip_property": "lens_pinhole_focal_length",
                               "constraints": NON_NEGATIVE_REAL})] = None
    """Distance between the pinhole and the image plane in the simple CGI pinhole camera model."""

    focus_distance: Annotated[tuple[StrictlyPositiveFloat, ...] | None,
      Field(alias="focusDistance",
            json_schema_extra={"units": METER,
                               "clip_property": "lens_focus_distance",
                               "constraints": STRICTLY_POSITIVE_REAL})] = None
    """Focus distance/position of the lens"""

    projection_offset: Annotated[tuple[ProjectionOffset, ...],
      Field(alias="projectionOffset",
            json_schema_extra={"units": MILLIMETER,
                               "clip_property": "lens_projection_offset",
                               "constraints": "X and Y projection offset shall each be real numbers."})] = None
    """Offset in x and y of the centre of perspective projection of the
    virtual camera
    """

    raw_encoders: Annotated[tuple[RawFizEncoders, ...] | None,
      Field(alias="rawEncoders",
            json_schema_extra={"clip_property": "lens_raw_encoders",
                               "anyOf": [{"required": ["focus"]},
                                         {"required": ["iris"]},
                                         {"required": ["zoom"]}],
                               "constraints": """
The parameter shall contain at least one integer value for the FIZ encoders.
"""})] = None
    """Raw encoder values for focus, iris and zoom.
    These values are dependent on encoder resolution and before any
    homing / ranging has taken place.
    """

    t_number: Annotated[tuple[NonNegativeFloat, ...] | None,
      Field(alias="tStop",
            json_schema_extra={"clip_property": "lens_t_number",
                               "constraints": NON_NEGATIVE_REAL})] = None
    """Linear t-number of the lens, equal to the F-number of the lens
    divided by the square root of the transmittance of the lens.
    """
