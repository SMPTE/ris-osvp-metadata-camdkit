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

"""Utility functions"""

from fractions import Fraction
import numbers

_WELL_KNOWN_FRACTIONAL_FPS = set([Fraction(24000, 1001), Fraction(30000, 1001), Fraction(60000, 1001), Fraction(120000, 1001)])
_FPS_THRESHOLD = 0.01

def guess_fps(fps: numbers.Real) -> Fraction:
  """Heuristically determines an exact fps value from an approximate one using
  well-known fps values."""

  if fps is None:
    raise ValueError

  if isinstance(fps,  numbers.Integral):
    return Fraction(fps)

  if not isinstance(fps, numbers.Real):
    raise TypeError

  if isinstance(fps, numbers.Rational) and fps.denominator == 1:
    return fps

  approx_fps = float(fps)

  if abs(int(approx_fps) - approx_fps) / approx_fps < _FPS_THRESHOLD:
    return Fraction(int(approx_fps))

  for wkfps in _WELL_KNOWN_FRACTIONAL_FPS:
    if round(float(wkfps), 2) == round(approx_fps, 2):
      return wkfps

  raise ValueError("Not a valid FPS")
