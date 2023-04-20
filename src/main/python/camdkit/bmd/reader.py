#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Blackmagic camera reader'''

import typing
import re
from fractions import Fraction

import camdkit.model

_CLIP_HEADING_RE = re.compile(r"^Clip Metadata$")
_FRAME_HEADING_RE = re.compile(r"^Frame (\d+) Metadata$")
_METADATA_LINE_RE = re.compile(r"^([^:]+): (.+)$")


def to_clip(metadata_file: typing.IO) -> camdkit.model.Clip:
  """Read Blackmagic camera metadata into a `Clip`.
  `metadata_raw_sdk`: Output of the ExtractMetadata sample tool from the Blackmagic RAW SDK
  """

  clip_data = {}
  frame_data = []
  cur_metadata = {}

  for line in metadata_file:

    m = _METADATA_LINE_RE.match(line)

    if m:
      cur_metadata[m.group(1)] = m.group(2)

    elif _CLIP_HEADING_RE.match(line):
      cur_metadata = clip_data

    elif _FRAME_HEADING_RE.match(line):
      frame_data.append({})
      cur_metadata = frame_data[-1]


  if len(frame_data) == 0:
    raise "Camera data does not contain frame information"

  # read clip metadata
  clip = camdkit.model.Clip()

  # read frame metadata
  first_frame_data = frame_data[0]

  # clip metadata

  # active_sensor_physical_dimensions
  if clip_data.get("camera_type") == "Blackmagic URSA Mini Pro 12K":
    crop_size = clip_data.get("crop_size")
    if crop_size is not None:
      width, height, _ = clip_data.get("crop_size").split(",")
      clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(
        width=round(int(width) * 270030 / 12288),
        height=round(int(height) * 14250 / 6480)
      )

  # fps
  sensor_rate = first_frame_data.get("sensor_rate")
  if sensor_rate is not None:
    num, denom, _ = sensor_rate.split(",")
    clip.capture_fps = Fraction(int(num), int(denom))

  # duration
  if clip.capture_fps is not None:
    clip.duration = clip.capture_fps * len(frame_data)

  # anamorphic_squeeze
  anamorphic_enable = int(clip_data.get("anamorphic_enable", 0))
  anamorphic = clip_data.get("anamorphic")
  if anamorphic_enable != 0 and anamorphic is not None:
    clip.anamorphic_squeeze = 100 * int(anamorphic[:-1])

  # ISO
  iso = first_frame_data.get("iso", None)
  if iso is not None:
    clip.iso = int(iso)

  clip.camera_make = clip_data.get("manufacturer")

  clip.camera_model = clip_data.get("camera_type")

  clip.camera_serial_number = clip_data.get("camera_id")

  clip.camera_firmware = clip_data.get("firmware_version")

  clip.lens_model = clip_data.get("lens_type")

  # clip.lens_serial_number is not supported
  # clip.active_sensor_physical_dimensions is not supported

  # white_balance
  # white_balance_kelvin = first_frame_data.get("white_balance_kelvin")
  # if white_balance_kelvin is not None:
  #   clip.white_balance = int(white_balance_kelvin)

  # shutter angle
  shutter_value = first_frame_data.get("shutter_value")
  if shutter_value is not None:
    clip.shutter_angle = int(shutter_value[:-1]) * 1000

  # sampled metadata

  # focal_length
  clip.focal_length = tuple(int(m["focal_length"][:-2]) for m in frame_data)

  # focus_position
  clip.focus_position = tuple(int(m["distance"][:-2]) for m in frame_data)

  # entrance_pupil_position not supported

  # t_number
  clip.t_number = tuple(round(float(m["aperture"][1:]) * 1000) for m in frame_data)

  return clip
