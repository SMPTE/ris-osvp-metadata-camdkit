#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Canon camera reader'''

import typing

import camdkit.trackerkit.model

def to_frame(frames_f4: typing.IO) -> camdkit.trackerkit.model.Frame:
  """Read Mo-Sys F4 data into a `Frame`.
  `frames_f4`: Per-frame camera tracking metadata.
  """

  frame = camdkit.trackerkit.model.Frame()

  # TODO JU Parse the file!
  # For now to test:
  frame.translation = camdkit.trackerkit.model.Vector3(0.0, 0.0, 0.0)

  return frame
