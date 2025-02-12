#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''RED camera reader tests'''

import unittest

import camdkit.red.reader
from fractions import Fraction

class REDReaderTest(unittest.TestCase):

  def test_reader(self):
    with open("src/test/resources/red/A001_C066_0303LZ_001.static.csv", "r", encoding="utf-8") as type_3_file, \
      open("src/test/resources/red/A001_C066_0303LZ_001.frames.csv", "r", encoding="utf-8") as type_5_file:
      clip = camdkit.red.reader.to_clip(type_3_file, type_5_file)

    self.assertEqual(clip.camera_make, "RED")

    self.assertEqual(clip.camera_model, "RANGER MONSTRO 8K VV")

    self.assertEqual(clip.camera_serial_number, "130-27E-4B5")

    self.assertEqual(clip.camera_firmware, "7.4.1")

    self.assertEqual(clip.lens_make, "SIGMA")

    self.assertEqual(clip.lens_model, "40mm T1.5 FF | 018")

    self.assertEqual(clip.lens_serial_number, "G53599764")

    self.assertEqual(clip.lens_firmware, "1.00")

    self.assertEqual(clip.iso, 250)

    self.assertEqual(clip.lens_nominal_focal_length, 40)

    self.assertEqual(clip.lens_focus_distance[0], 410)

    self.assertEqual(clip.lens_entrance_pupil_offset[0], 0.127)

    self.assertEqual(clip.lens_t_number[0], 5.6)

    self.assertEqual(clip.capture_frame_rate, 24)

    self.assertEqual(clip.anamorphic_squeeze, 1)

    self.assertEqual(clip.shutter_angle, 180)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(width=(4096 * 5 / 1000.0), height=(2160 * 5 / 1000.0))
    )
