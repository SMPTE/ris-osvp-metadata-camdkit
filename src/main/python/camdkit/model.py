#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) Society of Motion Picture and Television Engineers
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Data model"""

import numbers
import typing

from camdkit.framework import ParameterContainer, StrictlyPostiveRationalParameter, \
                              StrictlyPositiveIntegerParameter, StringParameter, Sampling, \
                              IntegerDimensionsParameter, Dimensions, UUIDURNParameter, Parameter

class ActiveSensorPhysicalDimensions(IntegerDimensionsParameter):
  "Height and width of the active area of the camera sensor"

  canonical_name = "activeSensorPhysicalDimensions"
  sampling = Sampling.STATIC
  units = "micron"


class Duration(StrictlyPostiveRationalParameter):
  """Duration of the clip"""

  canonical_name = "duration"
  sampling = Sampling.STATIC
  units = "second"


class CaptureFPS(StrictlyPostiveRationalParameter):
  """Capture frame frate of the camera"""

  canonical_name = "captureRate"
  sampling = Sampling.STATIC
  units = "hertz"


class ISO(StrictlyPositiveIntegerParameter):
  """Arithmetic ISO scale as defined in ISO 12232"""

  canonical_name = "isoSpeed"
  sampling = Sampling.STATIC
  units = "unit"


class LensSerialNumber(StringParameter):
  """Unique identifier of the lens"""

  canonical_name = "lensSerialNumber"
  sampling = Sampling.STATIC
  units = None

class LensMake(StringParameter):
  """Make of the lens"""

  canonical_name = "lensMake"
  sampling = Sampling.STATIC
  units = None

class LensModel(StringParameter):
  """Model of the lens"""

  canonical_name = "lensModel"
  sampling = Sampling.STATIC
  units = None

class LensFirmware(StringParameter):
  """Version identifier for the firmware of the lens"""

  canonical_name = "lensFirmwareVersion"
  sampling = Sampling.STATIC
  units = None

class CameraSerialNumber(StringParameter):
  """Unique identifier of the camera"""

  canonical_name = "cameraSerialNumber"
  sampling = Sampling.STATIC
  units = None

class CameraMake(StringParameter):
  """Make of the camera"""

  canonical_name = "cameraMake"
  sampling = Sampling.STATIC
  units = None

class CameraModel(StringParameter):
  """Model of the camera"""

  canonical_name = "cameraModel"
  sampling = Sampling.STATIC
  units = None

class CameraFirmware(StringParameter):
  """Version identifier for the firmware of the camera"""

  canonical_name = "cameraFirmwareVersion"
  sampling = Sampling.STATIC
  units = None

class TStop(StrictlyPositiveIntegerParameter):
  """The linear t-number of the lens, equal to the F-number of the lens divided
  by the square root of the transmittance of the lens."""

  canonical_name = "tStop"
  sampling = Sampling.REGULAR
  units = "0.001 unit"

class FStop(StrictlyPositiveIntegerParameter):
  """The linear f-number of the lens, equal to the focal length divided by the
  diameter of the entrance pupil."""

  canonical_name = "fStop"
  sampling = Sampling.REGULAR
  units = "0.001 unit"

class FocalLength(StrictlyPositiveIntegerParameter):
  """Focal length of the lens"""

  canonical_name = "focalLength"
  sampling = Sampling.REGULAR
  units = "millimeter"


class FocalPosition(StrictlyPositiveIntegerParameter):
  """Focus distance/position of the lens"""

  canonical_name = "focalPosition"
  sampling = Sampling.REGULAR
  units = "millimeter"


class EntrancePupilPosition(StrictlyPostiveRationalParameter):
  """Position of the entrance pupil of the lens"""

  canonical_name = "entrancePupilPosition"
  sampling = Sampling.REGULAR
  units = "millimeter"

class AnamorphicSqueeze(StrictlyPositiveIntegerParameter):
  """Nominal ratio of height to width of the image of an axis-aligned square
  captured by the camera sensor. It can be used to de-squeeze images but is not
  however an exact number over the entire captured area due to a lens' intrinsic
  analog nature."""

  canonical_name = "anamorphicSqueeze"
  sampling = Sampling.STATIC
  units = "0.01 unit"

class FDLLink(UUIDURNParameter):
  """Unique identifier of the FDL used by the camera."""

  canonical_name = "fdlLink"
  sampling = Sampling.STATIC
  units = None


class ShutterAngle(Parameter):
  """Shutter speed as a fraction of the capture frame rate. The shutter speed
  (in units of 1/s) is equal to the value of the parameter divided by 360 times
  the capture frame rate."""

  canonical_name = "shutterAngle"
  sampling = Sampling.STATIC
  units = "degrees (angular)"

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be an integer in the range (0..360000]."""

    return isinstance(value, numbers.Integral) and 0 < value <= 360000

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 1,
      "maximum": 360000
    }


class Clip(ParameterContainer):
  """Metadata for a camera clip.
  """
  duration: typing.Optional[numbers.Rational] = Duration()
  capture_fps: typing.Optional[numbers.Rational] = CaptureFPS()
  active_sensor_physical_dimensions: typing.Optional[Dimensions] = ActiveSensorPhysicalDimensions()
  lens_make: typing.Optional[str] = LensMake()
  lens_model: typing.Optional[str] = LensModel()
  lens_serial_number: typing.Optional[str] = LensSerialNumber()
  lens_firmware: typing.Optional[str] = LensFirmware()
  camera_make: typing.Optional[str] = CameraMake()
  camera_model: typing.Optional[str] = CameraModel()
  camera_firmware: typing.Optional[str] = CameraFirmware()
  camera_serial_number: typing.Optional[str] = CameraSerialNumber()
  iso: typing.Optional[numbers.Integral] = ISO()
  t_number: typing.Optional[typing.Tuple[numbers.Integral]] = TStop()
  f_number: typing.Optional[typing.Tuple[numbers.Integral]] = FStop()
  focal_length: typing.Optional[typing.Tuple[numbers.Integral]] = FocalLength()
  focal_position: typing.Optional[typing.Tuple[numbers.Integral]] = FocalPosition()
  entrance_pupil_position: typing.Optional[typing.Tuple[numbers.Rational]] = EntrancePupilPosition()
  anamorphic_squeeze: typing.Optional[numbers.Rational] = AnamorphicSqueeze()
  fdl_link: typing.Optional[str] = FDLLink()
  shutter_angle: typing.Optional[numbers.Integral] = ShutterAngle()
