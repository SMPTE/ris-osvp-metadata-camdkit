#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys F4 data reader'''

from camdkit.model import Clip
from camdkit.mosys.f4 import F4PacketParser

def to_frame(data: bytes) -> Clip:
  """Parse a frame of Mo-Sys F4 data into a Clip.
  """
  parser = F4PacketParser()
  success = parser.initialise(data)
  if success:
    frame = parser.get_tracking_frame()
  return success, frame, parser._packet.size

def to_clip(filename: str, frames: int = -1) -> Clip:
  """Read Mo-Sys F4 data into a Clip.
  `filename`: Filename of the f4 file.
  """
  clip = Clip()
  with open(filename, "rb") as f4_file:
    data = f4_file.read()
    offset = 0
    success = True
    count = 0
    while success and (frames == -1 or (count <= frames)):
      success, frame, packet_size = to_frame(data[offset:])
      if success:
        if offset == 0:
          clip = frame
        else:
          clip.append(frame)
        offset += packet_size
        count += 1
  return clip

def to_frames(filename: str, frame_count: int) -> list[dict]:
  """Read Mo-Sys F4 data into a list of `Frame`s.
  `filename`: Filename of the f4 file.
  """
  clip = to_clip(filename, frame_count)
  frames = []
  for i in range(0, frame_count):
    frames.append(clip.to_json(i))
  return frames
