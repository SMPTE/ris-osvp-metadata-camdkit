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
                              RationalParameter, TransformsParameter, TimingModeParameter

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
  section = "lens"

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


class Transforms(TransformsParameter):
  """
  X,Y,Z in metres of camera sensor relative to stage origin.
  The Z axis points upwards and the coordinate system is right-handed.
  Y points in the forward camera direction (when pan, tilt and roll are zero).
  For example in an LED volume Y would point towards the centre of the LED wall and so X would point to camera-right.
  Rotation expressed as euler angles in degrees of the camera sensor relative to stage origin
  Rotations are intrinsic and are measured around the axes ZXY, commonly referred to as [pan, tilt, roll]
  Notes on Euler angles:
  Euler angles are human readable and unlike quarternions, provide the ability for cycles (with angles >360 or <0 degrees).
  Where a tracking system is providing the pose of a virtual camera, gimbal lock does not present the physical challenges of a robotic system.
  Conversion to and from quarternions is trivial with an acceptable loss of precision
  """
  canonical_name = "transforms"
  units = "metres / degrees"

class TimingMode(TimingModeParameter):
  """
  'external' timing mode describes the case where the transport packet has inherent timing, so no explicit timing data is required in the data).
  'internal' mode indicates the transport packet does not have inherent timing, so a PTP timestamp must be provided.
  """
  canonical_name = "mode"
  section = "timing"
  allowedValues = ["internal", "external"]

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
  # TODO JU rest of the tracking model!
  transforms: typing.Optional[typing.Tuple[TransformsParameter]] = Transforms()
  # TODO this to test enumerations
  timing_mode: typing.Optional[typing.Tuple[TimingModeParameter]] = TimingMode()

  def append(self, clip):
    "Helper to add another clip's parameters to this clip's REGULAR data tuples"
    if not isinstance(clip, Clip):
      raise ValueError
    for prop, desc in self._params.items():
      if clip._values[prop] != None and desc.sampling == Sampling.REGULAR:
        self._values[prop] += clip._values[prop]

  def __getitem__(self, i):
    "Helper to convert to a single STATIC data frame for JSON output"
    clip = Clip()
    for f in dir(self):
      desc = getattr(self, f)
      if not isinstance(desc, tuple):
        continue
      setattr(clip, f, desc[i])
    return clip
  
  @classmethod
  def make_static_json_schema(cls) -> dict:
    "Helper to create a static json schema representation of a single frame"
    # Remove all the existing STATIC parameters and make the REGULAR parameters STATIC
    for prop, desc in cls._params.copy().items():
      if desc.sampling == Sampling.STATIC:
        del cls._params[prop]
        continue
      desc.sampling = Sampling.STATIC
    return super().make_json_schema()
  