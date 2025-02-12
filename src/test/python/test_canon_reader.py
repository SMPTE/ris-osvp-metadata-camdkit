#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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

    self.assertEqual(clip.lens_nominal_focal_length, 18)      # focal_length: 18 mm

    self.assertEqual(clip.lens_focus_distance[0], 0.5)   # focus_position: 0.5 mm

    self.assertEqual(clip.shutter_angle, 180)    # shutter_angle: 180 deg

    self.assertIsNone(clip.lens_entrance_pupil_offset)

    self.assertEqual(clip.lens_t_number[0], 4.5)        # t_number: 4.5

    self.assertIsNone(clip.capture_frame_rate)

    self.assertIsNone(clip.lens_serial_number)

    self.assertEqual(clip.anamorphic_squeeze, 1)  # anamorphic_squeeze: 1

    self.assertIsNone(clip.active_sensor_physical_dimensions)
