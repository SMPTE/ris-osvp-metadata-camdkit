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

'''ARRI camera reader tests'''

from fractions import Fraction
import unittest

import camdkit.arri.reader
import camdkit.model

class ARRIReaderTest(unittest.TestCase):

  def test_reader(self):
    clip = camdkit.arri.reader.to_clip("src/test/resources/arri/B001C001_180327_R1ZA.mov.csv")

    self.assertEqual(clip.iso, 400)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(width=316800, height=178200)
    )

    self.assertEqual(clip.lens_serial_number, "2")

    self.assertEqual(clip.capture_fps, 24)

    self.assertEqual(clip.focal_length[0], 40)

    self.assertEqual(clip.focal_position[0], 4812)

    self.assertEqual(clip.anamorphic_squeeze, 100)

    self.assertEqual(clip.t_number[0], 1782)

    self.assertEqual(clip.shutter_angle, 172800)

  def test_linear_iris_value(self):
    self.assertEqual(round(camdkit.arri.reader.t_number_from_linear_iris_value(6000) * 1000), 5657)
