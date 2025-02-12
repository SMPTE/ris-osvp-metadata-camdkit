#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Sony Venice camera reader tests'''

import unittest

import camdkit.venice.reader
from fractions import Fraction

class VeniceReaderTest(unittest.TestCase):

  def test_frac_stop(self):
    self.assertEqual(round(1000*camdkit.venice.reader.t_number_from_frac_stop("T 2 3/10")), 2219)

    self.assertEqual(round(1000*camdkit.venice.reader.t_number_from_frac_stop("T 6")), 8000)

  def test_reader(self):
    with open("src/test/resources/venice/D001C005_210716AGM01.xml", "r", encoding="utf-8") as static_file, \
      open("src/test/resources/venice/D001C005_210716AG.csv", "r", encoding="utf-8") as dynamic_file:
      clip = camdkit.venice.reader.to_clip(static_file, dynamic_file)

    self.assertEqual(clip.camera_make, "Sony")

    self.assertEqual(clip.camera_model, "MPC-3610")

    self.assertEqual(clip.camera_serial_number, "0010201")

    self.assertEqual(clip.camera_firmware, "6.10")

    self.assertIsNone(clip.lens_make)

    self.assertEqual(clip.lens_model, "S7i-32")

    self.assertEqual(clip.lens_serial_number, "7032.0100")

    self.assertEqual(clip.iso, 500)

    self.assertEqual(clip.lens_nominal_focal_length, 32)

    self.assertEqual(round(1000.0*clip.lens_t_number[0]), 2219)

    self.assertEqual(clip.capture_frame_rate, 24)

    self.assertEqual(clip.anamorphic_squeeze, 1)

    self.assertEqual(clip.shutter_angle, 103.8)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(width=5674.0 * 5.9375 / 1000.0, height=3192.0 * 5.9375 / 1000.0)
    )
