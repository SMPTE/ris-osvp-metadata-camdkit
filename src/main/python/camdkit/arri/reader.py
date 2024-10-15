#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''ARRI camera metadata reader'''

import csv
import math
import typing
from fractions import Fraction

import camdkit.model
import camdkit.utils as utils

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

    clip.iso = int(csv_data[0]["Exposure Index ASA"])

    clip.duration = len(csv_data)/Fraction(csv_data[0]["Project FPS"])

    clip.camera_make = "ARRI"

    clip.camera_model = csv_data[0]["Camera Model"]

    clip.camera_serial_number = csv_data[0]["Camera Serial Number"]

    lens_model = csv_data[0]["Lens Model"]

    if lens_model.startswith("ARRI "):
      clip.lens_make = "ARRI"
      clip.lens_model = lens_model[5:]
    else:
      clip.lens_model = lens_model

    clip.lens_serial_number = csv_data[0]["Lens Serial Number"]

    clip.capture_frame_rate = utils.guess_fps(Fraction(csv_data[0]["Project FPS"]))

    clip.shutter_angle = round(float(csv_data[0]["Shutter Angle"])  * 1000)

    clip.anamorphic_squeeze = round(float(csv_data[0]["Lens Squeeze"]) * 100)

    pix_dims = camdkit.model.Dimensions(
      width=int(csv_data[0]["Image Width"]),
      height=int(csv_data[0]["Image Height"])
    )
    pixel_pitch = _CAMERA_FAMILY_PIXEL_PITCH_MAP[(csv_data[0]["Camera Family"], pix_dims.width)]
    clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(
        width=round(pix_dims.width * pixel_pitch),
        height=round(pix_dims.height * pixel_pitch)
      )

    clip.lens_focal_length = tuple(round(float(m["Lens Focal Length"])) for m in csv_data)

    clip.lens_focus_distance = tuple(int(float(m["Lens Focus Distance"]) * 1000) for m in csv_data)

    clip.lens_t_number = tuple(round(t_number_from_linear_iris_value(int(m["Lens Linear Iris"])) * 1000) for m in csv_data)

    # TODO: Entrance Pupil Position
    # TODO: Sensor physical dimensions

  return clip
