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

'''RED camera reader tests'''

import unittest

import camdkit.red.reader
from fractions import Fraction

class REDReaderTest(unittest.TestCase):

  def test_reader(self):
    with open("src/test/resources/red/A001_C066_0303LZ_001.static.csv", "r", encoding="utf-8") as type_3_file, \
      open("src/test/resources/red/A001_C066_0303LZ_001.frames.csv", "r", encoding="utf-8") as type_5_file:
      clip = camdkit.red.reader.to_clip(type_3_file, type_5_file)

    self.assertEqual(clip.get_iso(), 250)

    self.assertEqual(clip.get_focal_length()[0], 40000)

    self.assertEqual(clip.get_entrance_pupil_position()[0], 127)

    self.assertEqual(clip.get_t_number()[0], 5600)

    self.assertEqual(clip.get_fps(), 24)

    self.assertEqual(clip.get_lens_serial_number(), "G53599764")

    self.assertEqual(clip.get_white_balance(), 5600)

    self.assertEqual(
      clip.get_sensor_pixel_dimensions(),
      camdkit.model.SensorPixelDimensions(width=4096, height=2160)
    )

    self.assertEqual(
      clip.get_sensor_physical_dimensions(),
      camdkit.model.SensorPhysicalDimensions(width=4096 * 5, height=2160 * 5)
    )
