#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import numbers
import typing

from camdkit.framework import ParameterContainer, StrictlyPositiveRationalParameter, \
                              StrictlyPositiveIntegerParameter, StringParameter, Sampling, \
                              IntegerDimensionsParameter, Dimensions, UUIDURNParameter, Parameter, \
                              RationalParameter

class ActiveSensorPhysicalDimensions(IntegerDimensionsParameter):
  "Height and width of the active area of the camera sensor"

  canonical_name = "activeSensorPhysicalDimensions"
  sampling = Sampling.STATIC
  units = "micron"


class Duration(StrictlyPositiveRationalParameter):
  """Duration of the clip"""

  canonical_name = "duration"
  sampling = Sampling.STATIC
  units = "second"


class CaptureFPS(StrictlyPositiveRationalParameter):
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
  """Nominal focal length of the lens. The number printed on the side of a prime
  lens, e.g. 50 mm, and undefined in the case of a zoom lens."""

  canonical_name = "focalLength"
  sampling = Sampling.REGULAR
  units = "millimeter"


class FocusPosition(StrictlyPositiveIntegerParameter):
  """Focus distance/position of the lens"""

  canonical_name = "focusPosition"
  sampling = Sampling.REGULAR
  units = "millimeter"


class EntrancePupilPosition(RationalParameter):
  """Position of the entrance pupil relative to the nominal imaging plane
  (positive if the entrance pupil is located on the side of the nominal imaging
  plane that is towards the object, and negative otherwise)"""

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
  focus_position: typing.Optional[typing.Tuple[numbers.Integral]] = FocusPosition()
  entrance_pupil_position: typing.Optional[typing.Tuple[numbers.Rational]] = EntrancePupilPosition()
  anamorphic_squeeze: typing.Optional[numbers.Rational] = AnamorphicSqueeze()
  fdl_link: typing.Optional[str] = FDLLink()
  shutter_angle: typing.Optional[numbers.Integral] = ShutterAngle()
