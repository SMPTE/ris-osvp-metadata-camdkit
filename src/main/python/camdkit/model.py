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

class Clip:
  """Metadata for a camera clip
  """
  def __init__(self):
    self._iso = None
    self._duration = None
    self._focal_length = []
    
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
  # ISO
  #

  def set_iso(self, iso : typing.Optional[numbers.Integral]):
    if iso is not None and not (isinstance(iso, numbers.Integral) and iso > 0):
      raise TypeError("ISO must be an integral number larger than 0")
    self._iso = iso

  def get_iso(self) -> typing.Optional[numbers.Integral]:
    return self._iso


  #
  # Focal length
  #

  def set_focal_length(self, samples: typing.Iterable[numbers.Real]):
    if not all(isinstance(s, numbers.Real) for s in samples):
      raise TypeError("Focal length sample must be a real number")

    self._focal_length = samples

  def get_focal_length(self) -> typing.List[numbers.Real]:
    return self._focal_length


  #
  # Serialization length
  #

  def serialize(self) -> dict:
    return {
      "duration": str(self.get_duration()),
      "focal_length": tuple(self.get_focal_length()),
      "iso": self.get_iso()
    }
