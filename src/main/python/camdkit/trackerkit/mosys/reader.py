#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys F4 data reader'''

from camdkit.trackerkit.model import Frame
from camdkit.trackerkit.mosys.f4 import F4PacketParser

Frames = list[Frame]

def to_frame(data: bytes, offset: int = 0) -> Frame:
  parser = F4PacketParser()
  success = parser.initialise(data[offset:])
  frame = Frame()
  if success:
    frame = parser.get_tracking_frame()
  return success, frame, parser._packet.size

def to_frames(filename: str) -> Frames:
  """Read Mo-Sys F4 data into a list of `Frame`s.
  `filename`: Filename of the f4 file.
  """
  frames = []
  with open(filename, "rb") as f4_file:
    data = f4_file.read()
    offset = 0
    success = True
    while success:
      success, frame, packet_size = to_frame(data, offset)
      if success:
        offset += packet_size
        frames.append(frame)
  return frames
