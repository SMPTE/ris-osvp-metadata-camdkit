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

from camdkit.framework import ParameterContainer, StrictlyPostiveRationalParameter, StrictlyPositiveIntegerParameter, StringParameter, Sampling, IntegerDimensionsParameter, Dimensions

class ActiveSensorPixelDimensions(IntegerDimensionsParameter):
  "Height and width of the active area of the camera sensor"

  canonical_name = "active_sensor_pixel_dimensions"
  sampling = Sampling.STATIC
  units = "pixel"


class ActiveSensorPhysicalDimensions(IntegerDimensionsParameter):
  "Height and width of the active area of the camera sensor"

  canonical_name = "active_sensor_physical_dimensions"
  sampling = Sampling.STATIC
  units = "micron"


class Duration(StrictlyPostiveRationalParameter):
  """Duration of the clip"""

  canonical_name = "duration"
  sampling = Sampling.STATIC
  units = "second"


class FPS(StrictlyPostiveRationalParameter):
  """Capture frame frate of the camera"""

  canonical_name = "fps"
  sampling = Sampling.STATIC
  units = "hertz"


class ISO(StrictlyPositiveIntegerParameter):
  """Arithmetic ISO scale as defined in ISO 12232"""

  canonical_name = "iso"
  sampling = Sampling.STATIC
  units = "unit"


class WhiteBalance(StrictlyPositiveIntegerParameter):
  """White balance of the camera."""

  canonical_name = "white_balance"
  sampling = Sampling.STATIC
  units = "kelvin"


class LensSerialNumber(StringParameter):
  """Unique identifier of the lens"""

  canonical_name = "lens_serial_number"
  sampling = Sampling.STATIC
  units = None

class TNumber(StrictlyPositiveIntegerParameter):
  """The linear t-number of the lens"""

  canonical_name = "t_number"
  sampling = Sampling.REGULAR
  units = "0.001 unit"

class FocalLength(StrictlyPositiveIntegerParameter):
  """Focal length of the lens"""

  canonical_name = "focal_length"
  sampling = Sampling.REGULAR
  units = "millimeter"


class FocalPosition(StrictlyPositiveIntegerParameter):
  """Focus distance/position of the lens"""

  canonical_name = "focal_position"
  sampling = Sampling.REGULAR
  units = "millimeter"


class EntrancePupilPosition(StrictlyPostiveRationalParameter):
  """Entrance pupil diameter of the lens"""

  canonical_name = "entrance_pupil_position"
  sampling = Sampling.REGULAR
  units = "millimeter"


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
