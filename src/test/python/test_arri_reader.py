#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''ARRI camera reader tests'''

from fractions import Fraction
import os
import tempfile
import unittest

import camdkit.arri.reader
import camdkit.model

class ARRIReaderTest(unittest.TestCase):

  def test_reader(self):
    clip = camdkit.arri.reader.to_clip("src/test/resources/arri/B001C001_180327_R1ZA.mov.csv")

    self.assertEqual(clip.iso, 400)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(width=316.8, height=178.2)
    )

    self.assertEqual(clip.camera_make, "ARRI")

    self.assertEqual(clip.camera_model, "Alexa LF Plus W")

    self.assertEqual(clip.camera_serial_number, "2566")

    self.assertEqual(clip.lens_make, "ARRI")

    self.assertEqual(clip.lens_model, "SP40 T1.8")

    self.assertEqual(clip.lens_serial_number, "2")

    self.assertEqual(clip.capture_frame_rate, 24)

    self.assertEqual(clip.lens_nominal_focal_length, 40)

    self.assertEqual(clip.lens_focus_distance[0], 4.812)

    self.assertEqual(clip.anamorphic_squeeze, 1)

    self.assertEqual(round(clip.lens_t_number[0] * 1000), 1782)

    self.assertEqual(clip.shutter_angle, 172.8)

  def test_non_meter_distance_unit_raises_value_error(self):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
      f.write("Lens Distance Unit\tExposure Index ASA\tProject FPS\n")
      f.write("Foot\t400\t24.000\n")
      path = f.name
    try:
      with self.assertRaises(ValueError):
        camdkit.arri.reader.to_clip(path)
    finally:
      os.unlink(path)

  def test_linear_iris_value(self):
    self.assertEqual(round(camdkit.arri.reader.t_number_from_linear_iris_value(6000) * 1000), 5657)
