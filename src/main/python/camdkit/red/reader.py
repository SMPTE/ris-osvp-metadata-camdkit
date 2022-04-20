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

'''RED camera reader'''

import csv
import io
from fractions import Fraction
import subprocess

import camdkit.model

def to_clip(camera_file_path: str) -> camdkit.model.Clip:
  """Read RED camera metadata into a `Clip`. Requires the RED camera REDline tool (https://www.red.com/downloads)."""

  # read clip metadata
  clip_metadata = next(
    csv.DictReader(
      io.StringIO(
        subprocess.run(
          f"REDline --silent --i {camera_file_path} --printMeta 3",
          check=False,
          encoding="UTF-8",
          stdout=subprocess.PIPE
        ).stdout
      )
    )
  )
  clip = camdkit.model.Clip()
  clip.set_iso(int(clip_metadata['ISO']))
  clip.set_lens_serial_number(clip_metadata["Lens Serial Number"])
  clip.set_sensor_pixel_dimensions(
    camdkit.model.SensorPixelDimensions(
      width=int(clip_metadata["Frame Width"]),
      height=int(clip_metadata["Frame Height"])
    )
  )

  # TODO: missing sensor physical dimensions

  # read frame metadata
  csv_data = list(csv.DictReader(
    io.StringIO(
      subprocess.run(
        f"REDline --silent --i {camera_file_path} --printMeta 5",
        check=False,
        encoding="UTF-8",
        stdout=subprocess.PIPE
      ).stdout
    )
  ))

  n_frames = int(clip_metadata["Total Frames"])

  if len(csv_data) != n_frames:
    raise ValueError(f"Inconsistent frame count between header {n_frames} and frame {len(csv_data)} files")

  clip.set_duration(len(csv_data)/Fraction(clip_metadata["FPS"]))
  clip.set_fps(Fraction(clip_metadata["FPS"]))

  clip.set_focal_length(tuple(int(m["Focal Length"]) * 1000 for m in csv_data))

  clip.set_focal_position(tuple(int(m["Focus Distance"]) * 1000 for m in csv_data))

  # TODO: missing Entrance Pupil Position
  # TODO: missing Iris position

  return clip
