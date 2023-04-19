#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''RED camera reader'''

import csv
import typing
from fractions import Fraction

import camdkit.model
import camdkit.utils as utils
import camdkit.red.cooke as cooke

_LENS_NAME_PIXEL_PITCH_MAP = {
  "RAPTOR 8K VV": 5,
  "MONSTRO 8K VV": 5,
  "KOMODO 6K S35": 4.4,
  "HELIUM 8K S35": 3.65,
  "GEMINI 5K S35": 6,
  "DRAGON": 5
}

def to_clip(meta_3_file: typing.IO, meta_5_file: typing.IO) -> camdkit.model.Clip:
  """Read RED camera metadata into a `Clip`.
  `meta_3_file`: Static camera metadata. CSV file generated using REDline (`REDline --silent --i {camera_file_path} --printMeta 3`)
  `meta_5_file`: Per-frame camera metadata. CSV file generated using REDline (`REDline --silent --i {camera_file_path} --printMeta 5`)
  """

  # read clip metadata
  clip_metadata = next(csv.DictReader(meta_3_file))
  clip = camdkit.model.Clip()

  clip.iso = int(clip_metadata['ISO'])

  clip.camera_make = "RED"

  clip.camera_model = clip_metadata["Camera Model"].strip()

  clip.camera_serial_number = clip_metadata["Camera PIN"].strip()

  clip.camera_firmware = clip_metadata["Firmware Version"].strip()

  clip.lens_make = clip_metadata["Lens Brand"].strip()

  clip.lens_model = clip_metadata["Lens Name"].strip()

  clip.lens_serial_number = clip_metadata["Lens Serial Number"].strip()

  clip.lens_firmware = cooke.fixed_data_from_string(clip_metadata["Lens Cooke /i Static"]).firmware_version_number

  pix_dims = camdkit.model.Dimensions(
    width=int(clip_metadata["Frame Width"]),
    height=int(clip_metadata["Frame Height"])
  )
  pixel_pitch = _LENS_NAME_PIXEL_PITCH_MAP[clip_metadata["Sensor Name"]]
  clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(
    width=round(pix_dims.width * pixel_pitch),
    height=round(pix_dims.height * pixel_pitch)
  )

  # read frame metadata
  csv_data = list(csv.DictReader(meta_5_file))

  n_frames = int(clip_metadata["Total Frames"])

  if len(csv_data) != n_frames:
    raise ValueError(f"Inconsistent frame count between header {n_frames} and frame {len(csv_data)} files")

  clip.capture_fps = utils.guess_fps(Fraction(clip_metadata["FPS"]))

  clip.duration = len(csv_data)/clip.capture_fps

  clip.anamorphic_squeeze = int(float(clip_metadata["Pixel Aspect Ratio"]) * 100)

  clip.shutter_angle = round(float(clip_metadata["Shutter (deg)"]) * 1000)

  clip.focal_length = tuple(int(m["Focal Length"]) for m in csv_data)

  clip.focal_position = tuple(int(m["Focus Distance"]) for m in csv_data)

  cooke_metadata = tuple(cooke.lens_data_from_binary_string(bytes(int(i, 16) for i in m["Cooke Metadata"].split("/"))) for m in csv_data)

  clip.entrance_pupil_position = tuple(m.entrance_pupil_position for m in cooke_metadata)

  clip.t_number = tuple(m.aperture_value * 10 for m in cooke_metadata)

  return clip
