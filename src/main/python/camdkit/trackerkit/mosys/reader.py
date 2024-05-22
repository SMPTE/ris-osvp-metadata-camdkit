#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Canon camera reader'''

import typing

from camdkit.trackerkit.model import Vector3, Transform, Frame

def to_frame(frames_f4: typing.IO) -> Frame:
  """Read Mo-Sys F4 data into a `Frame`.
  `frames_f4`: Per-frame camera tracking metadata.
  """

  frame = Frame()

  # TODO JU Parse the file!
  # For now to test:
  frame.test = "Hello World!"
  frame.transform = Transform()
  frame.transform.translation = Vector3(0.0, 0.0, 0.0)
  frame.transform.rotation = Vector3(0.0, 0.0, 0.0)

  return frame
