#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Blackmagic camera RAW reader tests'''

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

    self.assertEqual(clip.capture_frame_rate, 48)

    self.assertEqual(clip.lens_focal_length[0], 50)

    self.assertEqual(clip.lens_focus_distance[0], 991)

    # self.assertEqual(clip.white_balance, 6000)

    self.assertEqual(clip.anamorphic_squeeze, 200)

    self.assertEqual(clip.lens_t_number[0], 2300)

    self.assertEqual(clip.shutter_angle, 180000)
