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

'''Blackmagic RAW reader tests'''

import unittest

import camdkit.bmd.reader
import camdkit.model

class BMDReaderTest(unittest.TestCase):

  def test_reader(self):
    with open("src/test/resources/bmd/metadata.txt", "r", encoding="utf-8") as fp:
      clip = camdkit.bmd.reader.to_clip(fp)

    self.assertEqual(clip.camera_make, "Blackmagic Design")

    self.assertEqual(clip.camera_model, "Blackmagic URSA Mini Pro 12K")

    self.assertEqual(clip.camera_serial_number, "7ef33b36-a5ba-4a04-b218-0afc7eb1f8b6")

    self.assertEqual(clip.camera_firmware, "7.2.1")

    self.assertEqual(clip.lens_model, "Cooke Anamorphic /i Prime Lens 50mm")

    self.assertEqual(clip.iso, 800)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(
        width=round(5120 * 270030 / 12288),
        height=round(4272 * 14250 / 6480)
      )
    )

    self.assertEqual(clip.capture_fps, 48)

    self.assertEqual(clip.focal_length[0], 50)

    self.assertEqual(clip.focal_position[0], 991)

    # self.assertEqual(clip.white_balance, 6000)

    self.assertEqual(clip.anamorphic_squeeze, 200)

    self.assertEqual(clip.t_number[0], 2300)

    self.assertEqual(clip.shutter_angle, 180000)
