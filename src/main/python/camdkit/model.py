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

from camdkit.framework import Parameter, ParameterContainer

@dataclasses.dataclass
class IntegerDimensions:
  "Integer height and width of a rectangular area"
  height: numbers.Integral
  width: numbers.Integral

class ActiveSensorPixelDimensions(Parameter):
  "Height and width in pixels of the active area of the camera sensor"
  
  canonical_name = "active_sensor_pixels_dimensions"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True

    if not isinstance(value, IntegerDimensions):
      return False

    if value.height <= 0 or value.width <= 0:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value.asdict()

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return IntegerDimensions(**value)

class ActiveSensorPhysicalDimensions(Parameter):
  "Height and width in whole microns of the active area of the camera sensor"
  
  canonical_name = "active_sensor_physical_dimensions"

  @staticmethod
  def validate(value) -> bool:
    if value is None:
      return True

    if not isinstance(value, IntegerDimensions):
      return False

    if value.height <= 0 or value.width <= 0:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value.asdict()

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return IntegerDimensions(**value)

class Duration(Parameter):
  """Duration in seconds"""
  canonical_name = "duration"

  @staticmethod
  def validate(value) -> bool:
    return value is None or (isinstance(value, numbers.Rational) and value >= 0)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Fraction(value)

class FPS(Parameter):
  """Frame frate in frames per second (fps)"""

  canonical_name = "fps"

  @staticmethod
  def validate(value) -> bool:
    return value is None or (isinstance(value, numbers.Rational) and value > 0)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Fraction(value)


class ISO(Parameter):
  """ISO number as an integer"""

  canonical_name = "iso"

  @staticmethod
  def validate(value) -> bool:
    return value is None or (isinstance(value, numbers.Integral) and value > 0)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)


class WhiteBalance(Parameter):
  """White balance of the camera expressed as an integer in units of degrees kelvin."""

  canonical_name = "white_balance"

  @staticmethod
  def validate(value) -> bool:
    return value is None or (isinstance(value, numbers.Integral) and value > 0)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)


class LensSerialNumber(Parameter):
  """Unique identifier of the lens"""

  canonical_name = "lens_serial_number"

  @staticmethod
  def validate(value) -> bool:
    return value is None or isinstance(value, str)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return str(value)

class Clip(ParameterContainer):
  """Metadata for a camera clip
  """
  duration: typing.Optional[numbers.Rational] = Duration()
  fps: typing.Optional[numbers.Rational] = FPS()
  active_sensor_physical_dimensions: typing.Optional[IntegerDimensions] = ActiveSensorPhysicalDimensions()
  active_sensor_pixel_dimensions: typing.Optional[IntegerDimensions] = ActiveSensorPixelDimensions()
  lens_serial_number: typing.Optional[str] = LensSerialNumber()
  white_balance: typing.Optional[numbers.Integral] = WhiteBalance()
  iso: typing.Optional[numbers.Integral] = ISO()

  #
  # t-number
  #

  def set_t_number(self, samples: typing.Iterable[numbers.Integral]):
    """T-number of the lens (thousandth)
    """
    t_number = tuple(samples)

    if not all(isinstance(s, numbers.Integral) and s > 0 for s in t_number):
      raise TypeError("Each t-number sample must be an integer larger than 0.")

    self._t_number = t_number

  def get_t_number(self) -> typing.Tuple[numbers.Integral]:
    return self._t_number

  #
  # Focal length
  #

  def set_focal_length(self, samples: typing.Iterable[numbers.Integral]):
    focal_length = tuple(samples)

    if not all(isinstance(s, numbers.Integral) and s > 0 for s in focal_length):
      raise TypeError("Each sample must be an integer larger than 0 in units of millimeter.")

    self._focal_length = focal_length

  def get_focal_length(self) -> typing.Tuple[numbers.Integral]:
    return self._focal_length


  #
  # Focal position
  #

  def set_focal_position(self, samples: typing.Iterable[numbers.Integral]):
    focal_position = tuple(samples)

    if not all(isinstance(s, numbers.Integral) and s > 0 for s in focal_position):
      raise TypeError("Each sample must be an integer larger than 0 in units of millimeter.")

    self._focal_position = focal_position

  def get_focal_position(self) -> typing.Tuple[numbers.Integral]:
    return self._focal_position


  #
  # Entrance Pupil Position
  #

  def set_entrance_pupil_position(self, samples: typing.Iterable[numbers.Rational]):
    entrance_pupil_position = tuple(samples)

    if not all(isinstance(s, numbers.Rational) for s in entrance_pupil_position):
      raise TypeError("Each sample must be a rational number in units of millimeter.")

    self._entrance_pupil_position = entrance_pupil_position

  def get_entrance_pupil_position(self) -> typing.Tuple[numbers.Rational]:
    return self._entrance_pupil_position

  #
  # constructor
  #

  def __init__(self) -> None:
    self._focal_length = tuple()
    self._focal_position = tuple()
    self._t_number = tuple()
    self._entrance_pupil_position = tuple()

