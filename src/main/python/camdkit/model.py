#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2022, Sandflow Consulting LLC
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

from fractions import Fraction
import numbers
import typing
import dataclasses

from camdkit.framework import Parameter, ParameterContainer, StrictlyPostiveRationalParameter, StrictlyPositiveIntegerParameter, StringParameter

INT_MAX = 2147483647 # 2^31 - 1

@dataclasses.dataclass
class Dimensions:
  "Height and width of a rectangular area"
  height: numbers.Real
  width: numbers.Real

class ActiveSensorPixelDimensions(Parameter):
  "Height and width, in pixels, of the active area of the camera sensor"

  canonical_name = "active_sensor_pixel_dimensions"

  @staticmethod
  def validate(value) -> bool:
    """The height and width shall be each be an integer in the range (0..2,147,483,647]."""
    if value is None:
      return True

    if not isinstance(value, Dimensions):
      return False

    if not isinstance(value.height, numbers.Integral) or not isinstance(value.width, numbers.Integral):
      return False

    if value.height <= 0 or value.width <= 0 or value.height > INT_MAX or value.width > INT_MAX:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Dimensions(**value)

class ActiveSensorPhysicalDimensions(Parameter):
  "Height and width, in microns, of the active area of the camera sensor"
  
  canonical_name = "active_sensor_physical_dimensions"

  @staticmethod
  def validate(value) -> bool:
    """The height and width shall be each be an integer in the range (0..2,147,483,647]."""
    if value is None:
      return True

    if not isinstance(value, Dimensions):
      return False

    if not isinstance(value.height, numbers.Integral) or not isinstance(value.width, numbers.Integral):
      return False

    if value.height <= 0 or value.width <= 0 or value.height > INT_MAX or value.width > INT_MAX:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Dimensions(**value)

class Duration(StrictlyPostiveRationalParameter):
  """Duration of the clip in seconds"""

  canonical_name = "duration"

class FPS(StrictlyPostiveRationalParameter):
  """Capture frame frate of the camera in frames per second (fps)"""

  canonical_name = "fps"

class ISO(StrictlyPositiveIntegerParameter):
  """Arithmetic ISO scale as defined in ISO 12232"""

  canonical_name = "iso"

class WhiteBalance(StrictlyPositiveIntegerParameter):
  """White balance of the camera expressed in degrees kelvin."""

  canonical_name = "white_balance"

class LensSerialNumber(StringParameter):
  """Unique identifier of the lens"""

  canonical_name = "lens_serial_number"


class TNumber(Parameter):
  """Thousandths of the t-number of the lens as positive integer"""

  canonical_name = "t_number"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True

    return isinstance(value, tuple) and all(isinstance(s, numbers.Integral) and s > 0 for s in value)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return tuple(value)


class FocalLength(Parameter):
  """Focal length of the lens in whole millimeters"""

  canonical_name = "focal_length"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True
      
    return isinstance(value, tuple) and all(isinstance(s, numbers.Integral) and s > 0 for s in value)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return tuple(value)


class FocalPosition(Parameter):
  """Focus distance/position of the lens in whole millimeters"""

  canonical_name = "focal_position"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True
      
    return isinstance(value, tuple) and all(isinstance(s, numbers.Integral) and s > 0 for s in value)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return tuple(value)


class EntrancePupilPosition(Parameter):
  """Entrance pupil of the lens in fractional millimeters"""

  canonical_name = "entrance_pupil_position"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True
      
    return isinstance(value, tuple) and all(isinstance(s, numbers.Rational) and s > 0 for s in value)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return tuple(map(str, value))

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return tuple(map(Fraction, value))


class Clip(ParameterContainer):
  """Metadata for a camera clip.
  """
  duration: typing.Optional[numbers.Rational] = Duration()
  fps: typing.Optional[numbers.Rational] = FPS()
  active_sensor_physical_dimensions: typing.Optional[Dimensions] = ActiveSensorPhysicalDimensions()
  active_sensor_pixel_dimensions: typing.Optional[Dimensions] = ActiveSensorPixelDimensions()
  lens_serial_number: typing.Optional[str] = LensSerialNumber()
  white_balance: typing.Optional[numbers.Integral] = WhiteBalance()
  iso: typing.Optional[numbers.Integral] = ISO()
  t_number: typing.Optional[typing.Tuple[numbers.Integral]] = TNumber()
  focal_length: typing.Optional[typing.Tuple[numbers.Integral]] = FocalLength()
  focal_position: typing.Optional[typing.Tuple[numbers.Integral]] = FocalPosition()
  entrance_pupil_position: typing.Optional[typing.Tuple[numbers.Rational]] = EntrancePupilPosition()
