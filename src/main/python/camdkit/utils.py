#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Utility functions"""

import copy
import numbers
from fractions import Fraction

from pydantic.json_schema import JsonSchemaValue

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

def unwrap_clip_to_pseudo_frame(wrapped_clip: JsonSchemaValue) -> JsonSchemaValue:
  paths_to_unwrap: tuple[tuple[str, ...], ...] = (
    ("globalStage",),
    ("lens", "custom"),
    ("lens", "distortion"),
    ("lens", "distortionOffset"),
    ("lens", "distortionOverscan"),
    ("lens", "encoders"),
    ("lens", "entrancePupilOffset"),
    ("lens", "exposureFalloff"),
    ("lens", "fStop"),
    ("lens", "pinholeFocalLength"),
    ("lens", "focusDistance"),
    ("lens", "projectionOffset"),
    ("lens", "rawEncoders"),
    ("lens", "tStop"),
    ("lens", "undistortionOverscan"),
    ("protocol",),
    ("relatedSampleIds",),
    ("sampleId",),
    ("sourceId",),
    ("sourceNumber",),
    ("timing", "mode"),
    ("timing", "recordedTimestamp"),
    ("timing", "sampleRate"),
    ("timing", "sampleTimestamp"),
    ("timing", "sequenceNumber"),
    ("timing", "synchronization"),
    ("timing", "timecode"),
    ("tracker", "notes"),
    ("tracker", "recording"),
    ("tracker", "slate"),
    ("tracker", "status"),
    ("transforms",)
  )
  clip = copy.deepcopy(wrapped_clip)
  for path in paths_to_unwrap:
    # REALLY brute-force
    if len(path) == 1:
      k0 = path[0]
      if k0 in clip:
        clip[k0] = clip[k0][0]
    elif len(path) == 2:
      k0 = path[0]
      if k0 in clip:
        k1 = path[1]
        if k1 in clip[k0]:
          clip[k0][k1] = clip[k0][k1][0]
    else:
      raise RuntimeError("That's too deep for me I'm afraid")
  return clip
