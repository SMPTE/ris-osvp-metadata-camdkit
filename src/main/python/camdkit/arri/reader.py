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

'''ARRI camera metadata reader'''

import csv
import math
import typing
from fractions import Fraction

import camdkit.model

# https://www.arri.com/resource/blob/31908/14147b455c90a9a35018c0d091350ff3/2021-10-arri-formatsandresolutionsoverview-3-4-data.pdf
_CAMERA_FAMILY_PIXEL_PITCH_MAP = {
  ("ALEXALF", 1920) : Fraction(316800, 1920),
  ("ALEXALF", 2048) : Fraction(316800, 2048),
  ("ALEXALF", 3840) : Fraction(316800, 3840),
  ("ALEXALF", 4448) : Fraction(367000, 4448),
}

def t_number_from_linear_iris_value(lin_value: int) -> typing.Optional[Fraction]:
  """Calculate t-number (regular iris values) from linear iris values
  """
  return math.pow(2, (lin_value - 1000)/1000/2)

def to_clip(csv_path: str) -> camdkit.model.Clip:
  """Read ARRI camera metadata into a `Clip`. `csv_path` is the path to a CSV
  file extracted using ARRI Meta Extract (AME)."""

  with open(csv_path, encoding="utf-8") as csvfile:
    csv_data = list(csv.DictReader(csvfile, dialect="excel-tab"))

    n_frames = len(csv_data)

    if n_frames <= 0:
      raise ValueError("No data")

    clip = camdkit.model.Clip()

    assert csv_data[0]["Lens Distance Unit"] == "Meter"

    clip.set_iso(int(csv_data[0]["Exposure Index ASA"]))

    clip.set_duration(len(csv_data)/Fraction(csv_data[0]["Project FPS"]))

    clip.set_lens_serial_number(csv_data[0]["Lens Serial Number"])

    clip.set_fps(Fraction(csv_data[0]["Project FPS"]))

    clip.set_white_balance(int(csv_data[0]["White Balance"]))

    clip.set_sensor_pixel_dimensions(
      camdkit.model.SensorPixelDimensions(
        width=int(csv_data[0]["Image Width"]),
        height=int(csv_data[0]["Image Height"])
      )
    )

    pix_dims = clip.get_sensor_pixel_dimensions()
    pixel_pitch = _CAMERA_FAMILY_PIXEL_PITCH_MAP[(csv_data[0]["Camera Family"], pix_dims.width)]
    clip.set_sensor_physical_dimensions(
      camdkit.model.SensorPhysicalDimensions(
        width=round(pix_dims.width * pixel_pitch),
        height=round(pix_dims.height * pixel_pitch)
      )
    )

    clip.set_focal_length(tuple(int(float(m["Lens Focal Length"]) * 1000) for m in csv_data))

    clip.set_focal_position(tuple(int(float(m["Lens Focus Distance"]) * 1000) for m in csv_data))

    clip.set_t_number(tuple(round(t_number_from_linear_iris_value(int(m["Lens Linear Iris"])) * 1000) for m in csv_data))

    # TODO: Entrance Pupil Position
    # TODO: Sensor physical dimensions
    
  return clip
