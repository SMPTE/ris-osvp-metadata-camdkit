#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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
