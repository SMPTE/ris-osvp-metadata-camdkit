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

import numbers
import typing
import dataclasses

@dataclasses.dataclass
class SensorPhysicalDimensions:
  "Height and width of the camera sensor in microns"
  height: numbers.Integral
  width: numbers.Integral

  def __post_init__(self):
    if not isinstance(self.height, numbers.Integral) \
      or not isinstance(self.height, numbers.Integral) \
      or self.height <= 0 \
      or self.width <= 0:
      raise TypeError("Height and width must must be positive integers in microns")

  def serialize(self):
    return dataclasses.asdict(self)

@dataclasses.dataclass
class SensorPixelDimensions:
  "Height and width of the camera sensor in pixels (debayered)"
  height: numbers.Integral
  width: numbers.Integral

  def __post_init__(self):
    if not isinstance(self.height, numbers.Integral) \
      or not isinstance(self.height, numbers.Integral) \
      or self.height <= 0 \
      or self.width <= 0:
      raise TypeError("Height and width must must be positive integers in pixels")

  def serialize(self):
    return dataclasses.asdict(self)

class Clip:
  """Metadata for a camera clip
  """
  def __init__(self):
    self._iso = None
    self._duration = None
    self._sensor_physical_dimensions = None
    self._sensor_pixel_dimensions = None
    self._lens_serial_number = None
    self._fps = None
    self._white_balance = None
    self._focal_length = tuple()
    self._focal_position = tuple()
    self._t_number = tuple()
    self._entrance_pupil_position = tuple()
    
  #
  # duration
  #

  def get_duration(self) -> typing.Optional[numbers.Rational]:
    return self._duration

  def set_duration(self, duration: typing.Optional[numbers.Rational]):
    if duration is not None and not (isinstance(duration, numbers.Rational) and duration >= 0):
      raise TypeError("duration must be a positive rational number")
    self._duration = duration

  #
  # fps
  #

  def get_fps(self) -> typing.Optional[numbers.Rational]:
    return self._fps

  def set_fps(self, fps: typing.Optional[numbers.Rational]):
    if fps is not None:
      if not isinstance(fps, numbers.Rational):
        raise TypeError("Must be a rational")

      if fps <= 0:
        raise ValueError("Must be a positive number")

    self._fps = fps

  #
  # Sensor physical dimensions
  #

  def set_sensor_physical_dimensions(self, dims : typing.Optional[SensorPhysicalDimensions]):
    if dims is not None and not isinstance(dims, SensorPhysicalDimensions):
      raise TypeError("Sensor dimensions must be an instance of SensorDimensions")
    self._sensor_physical_dimensions = dims

  def get_sensor_physical_dimensions(self) -> typing.Optional[SensorPhysicalDimensions]:
    return self._sensor_physical_dimensions


  #
  # Sensor pixel dimensions
  #

  def set_sensor_pixel_dimensions(self, dims : typing.Optional[SensorPixelDimensions]):
    if dims is not None and not isinstance(dims, SensorPixelDimensions):
      raise TypeError("Sensor dimensions must be an instance of SensorPixelDimensions")
    self._sensor_pixel_dimensions = dims

  def get_sensor_pixel_dimensions(self) -> typing.Optional[SensorPixelDimensions]:
    return self._sensor_pixel_dimensions

  #
  # Lens serial number
  #

  def set_lens_serial_number(self, serial_number : typing.Optional[str]):
    if serial_number is not None and not isinstance(serial_number, str):
      raise TypeError("The lens serial number must be a string")
    self._lens_serial_number = serial_number

  def get_lens_serial_number(self) -> typing.Optional[str]:
    return self._lens_serial_number

  #
  # ISO
  #

  def set_iso(self, iso : typing.Optional[numbers.Integral]):
    if iso is not None and not (isinstance(iso, numbers.Integral) and iso > 0):
      raise TypeError("ISO must be an integral number larger than 0")
    self._iso = iso

  def get_iso(self) -> typing.Optional[numbers.Integral]:
    return self._iso

  #
  # White balance
  #

  def set_white_balance(self, white_balance : typing.Optional[numbers.Integral]):
    """White balance of the camera expressed as an integer in units of degrees kelvin.
    """
    if white_balance is not None and not (isinstance(white_balance, numbers.Integral) and white_balance > 0):
      raise TypeError("White balance must be an integral number larger than 0")
    self._white_balance = white_balance

  def get_white_balance(self) -> typing.Optional[numbers.Integral]:
    return self._white_balance

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
  # Serialization length
  #

  def serialize(self) -> dict:

    return {
      "duration": str(self.get_duration()),
      "iso": self.get_iso(),
      "focal_length": self.get_focal_length(),
      "lens_serial_number": self.get_lens_serial_number(),
      "sensor_pixel_dimensions": None if self.get_sensor_pixel_dimensions() is None else self.get_sensor_pixel_dimensions().serialize(),
      "sensor_physical_dimensions": None if self.get_sensor_physical_dimensions() is None else self.get_sensor_physical_dimensions().serialize(),
      "entrance_pupil_position": tuple(map(str, self.get_entrance_pupil_position())),
      "focal_position": self.get_focal_position(),
      "t_number": tuple(map(str, self.get_t_number())),
    }
