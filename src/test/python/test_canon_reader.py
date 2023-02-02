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

'''Canon camera reader tests'''

import unittest

import camdkit.canon.reader

class CanonReaderTest(unittest.TestCase):

  def test_reader(self):
    with open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Static.csv", "r", encoding="utf-8") as static_csv, \
      open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Frames.csv", "r", encoding="utf-8") as frame_csv:
      clip = camdkit.canon.reader.to_clip(static_csv, frame_csv)

    self.assertEqual(clip.camera_make, "Canon")

    self.assertEqual(clip.iso, 1600)                # ISO: 1600

    self.assertEqual(clip.focal_length[0], 18)      # focal_length: 18 mm

    self.assertEqual(clip.focal_position[0], 500)   # focal_position: 500 mm

    self.assertEqual(clip.shutter_angle, 180000)    # shutter_angle: 180 deg

    self.assertIsNone(clip.entrance_pupil_position)

    self.assertEqual(clip.t_number[0], 4500)        # t_number: 4.5

    self.assertIsNone(clip.capture_fps)

    self.assertIsNone(clip.lens_serial_number)

    self.assertEqual(clip.anamorphic_squeeze, 100)  # anamorphic_squeeze: 1

    self.assertIsNone(clip.active_sensor_physical_dimensions)
