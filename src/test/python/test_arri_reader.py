#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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

    self.assertEqual(clip.camera_make, "ARRI")

    self.assertEqual(clip.camera_model, "Alexa LF Plus W")

    self.assertEqual(clip.camera_serial_number, "2566")

    self.assertEqual(clip.lens_make, "ARRI")

    self.assertEqual(clip.lens_model, "SP40 T1.8")

    self.assertEqual(clip.lens_serial_number, "2")

    self.assertEqual(clip.capture_fps, 24)

    self.assertEqual(clip.focal_length[0], 40)

    self.assertEqual(clip.focus_position[0], 4812)

    self.assertEqual(clip.anamorphic_squeeze, 100)

    self.assertEqual(clip.t_number[0], 1782)

    self.assertEqual(clip.shutter_angle, 172800)

  def test_linear_iris_value(self):
    self.assertEqual(round(camdkit.arri.reader.t_number_from_linear_iris_value(6000) * 1000), 5657)
