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

'''Sony Venice camera reader tests'''

import unittest

import camdkit.venice.reader
from fractions import Fraction

class VenicReaderTest(unittest.TestCase):

  def test_frac_stop(self):
    self.assertEqual(round(camdkit.venice.reader.t_number_from_frac_stop("T 2 3/10") * 1000), 2219)

    self.assertEqual(round(camdkit.venice.reader.t_number_from_frac_stop("T 6") * 1000), 8000)

  def test_reader(self):
    with open("src/test/resources/venice/D001C005_210716AGM01.xml", "r", encoding="utf-8") as static_file, \
      open("src/test/resources/venice/D001C005_210716AG.csv", "r", encoding="utf-8") as dynamic_file:
      clip = camdkit.venice.reader.to_clip(static_file, dynamic_file)

    self.assertEqual(clip.iso, 500)

    self.assertEqual(clip.get_focal_length()[0], 32)

    self.assertEqual(clip.get_t_number()[0], 2219)

    self.assertEqual(clip.fps, 24)

    self.assertEqual(clip.lens_serial_number, "7032.0100")

    self.assertEqual(clip.white_balance, 4300)

    self.assertEqual(
      clip.active_sensor_pixel_dimensions,
      camdkit.model.IntegerDimensions(width=5674, height=3192)
    )

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.IntegerDimensions(width=round(5674 * 5.9375), height=round(3192 * 5.9375))
    )
