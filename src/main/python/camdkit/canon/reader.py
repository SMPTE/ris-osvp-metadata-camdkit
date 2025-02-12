#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Canon camera reader'''

import csv
import typing
import struct
from fractions import Fraction

import camdkit.model

def _read_float32_as_hex(float32_hex: str) -> float:
  return struct.unpack('>f', bytes.fromhex(float32_hex))[0]

def to_clip(static_csv: typing.IO, frames_csv: typing.IO) -> camdkit.model.Clip:
  """Read Canon camera metadata into a `Clip`.
  `static_csv`: Static camera metadata.
  `frames_csv`: Per-frame camera metadata.
  """

  # read clip metadata
  clip_metadata = next(csv.DictReader(static_csv))
  clip = camdkit.model.Clip()

  # read frame metadata
  frame_data = list(csv.DictReader(frames_csv))
  first_frame_data = frame_data[0]

  # clip metadata

  # duration
  clip.duration = Fraction(int(clip_metadata["Duration"]), int(clip_metadata["Timescale"]))

  # anamorphic_squeeze
  lens_squeeze_factor = int(clip_metadata["LensSqueezeFactor"])
  if lens_squeeze_factor == 0:
    clip.anamorphic_squeeze = 1
  elif lens_squeeze_factor == 1:
    clip.anamorphic_squeeze = 1.33
  elif lens_squeeze_factor == 2:
    clip.anamorphic_squeeze = 2
  elif lens_squeeze_factor == 3:
    clip.anamorphic_squeeze = 1.8

  # ISO
  if int(first_frame_data['PhotographicSensitivityMode']) == 1:
    clip.iso = Fraction(first_frame_data['PhotographicSensitivity']).numerator - 0x80000000

  # clip.active_sensor_physical_dimensions is not supported
  # clip.capture_frame_rate is no supported

  clip.camera_make = "Canon"

  # shutter angle
  clip.shutter_angle = float(Fraction(first_frame_data['ExposureTime']))

  # sampled metadata

  # focal_length
  focal_lengths = set(Fraction(m["FocalLength"]) for m in frame_data)
  if len(focal_lengths) == 1:
    focal_length = float(focal_lengths.pop())
    clip.lens_nominal_focal_length = focal_length

  # focus_position
  clip.lens_focus_distance = tuple(_read_float32_as_hex(m["FocusPosition"]) for m in frame_data)

  # entrance_pupil_offset not supported

  # t_number
  if int(first_frame_data['ApertureMode']) == 2:
    clip.lens_t_number = tuple(Fraction(m["ApertureNumber"]) for m in frame_data)
  elif int(first_frame_data['ApertureMode']) == 1:
    clip.lens_f_number = tuple(Fraction(m["ApertureNumber"]) for m in frame_data)

  return clip
