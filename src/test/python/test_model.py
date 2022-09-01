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
from fractions import Fraction 

import camdkit.model

class ModelTest(unittest.TestCase):

  def test_duration(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.duration)

    clip.duration = 3

    self.assertEqual(clip.duration, 3)

  def test_serialize(self):
    clip = camdkit.model.Clip()

    clip.duration = 3
    clip.capture_fps = Fraction(24000, 1001)
    clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(width=640, height=480)
    clip.active_sensor_pixel_dimensions = camdkit.model.Dimensions(width=640, height=480)
    clip.lens_serial_number = "123456789"
    clip.white_balance = 7200
    clip.anamorphic_squeeze = 120
    clip.iso = 13
    clip.t_number = (2, 4)
    clip.focal_length = (2, 4)
    clip.focal_position = (2, 4)
    clip.entrance_pupil_position = (Fraction(1, 2), Fraction(13, 7))

    d = clip.to_json()

    self.assertEqual(d["duration"], "3")
    self.assertEqual(d["capture_fps"], "24000/1001")
    self.assertDictEqual(d["active_sensor_physical_dimensions"], {"height": 480, "width": 640})
    self.assertDictEqual(d["active_sensor_pixel_dimensions"], {"height": 480, "width": 640})
    self.assertEqual(d["lens_serial_number"], "123456789")
    self.assertEqual(d["white_balance"], 7200)
    self.assertEqual(d["anamorphic_squeeze"], 120)
    self.assertEqual(d["iso"], 13)
    self.assertTupleEqual(d["t_number"], (2, 4))
    self.assertTupleEqual(d["focal_length"], (2, 4))
    self.assertTupleEqual(d["focal_position"], (2, 4))
    self.assertTupleEqual(d["entrance_pupil_position"], ("1/2", "13/7"))

    d_clip = camdkit.model.Clip()
    d_clip.from_json(d)

    self.assertDictEqual(d_clip._values, clip._values)

  def test_documentation(self):
    doc = camdkit.model.Clip.make_documentation()

    self.assertIn(camdkit.model.ActiveSensorPhysicalDimensions.canonical_name, doc)

  def test_duration_fraction(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.duration)

    clip.duration = Fraction(6, 7)

    with self.assertRaises(ValueError):
      clip.duration = 0.7

    self.assertEqual(clip.duration, Fraction(6, 7))

  def test_active_sensor_physical_dimensions(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.active_sensor_physical_dimensions)

    dims = camdkit.model.Dimensions(4, 5)

    clip.active_sensor_physical_dimensions = dims

    self.assertEqual(clip.active_sensor_physical_dimensions, dims)


  def test_active_sensor_pixel_dimensions(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.active_sensor_pixel_dimensions)

    dims = camdkit.model.Dimensions(4, 5)

    clip.active_sensor_pixel_dimensions = dims

    self.assertEqual(clip.active_sensor_pixel_dimensions, dims)

  def test_lens_serial_number(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_serial_number)

    with self.assertRaises(ValueError):
      clip.lens_serial_number = 0.7

    value = "1231231321"

    clip.lens_serial_number = value

    self.assertEqual(clip.lens_serial_number, value)

  def test_iso(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.iso)

    with self.assertRaises(ValueError):
      clip.iso = 0.7

    value = 200

    clip.iso = value

    self.assertEqual(clip.iso, value)

  def test_fps(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.capture_fps)

    with self.assertRaises(ValueError):
      clip.capture_fps = 0.7

    with self.assertRaises(ValueError):
      clip.capture_fps = -24

    value = Fraction(24000, 1001)

    clip.capture_fps = value

    self.assertEqual(clip.capture_fps, value)


  def test_t_number(self):
    clip = camdkit.model.Clip()

    self.assertEqual(clip.t_number, None)

    with self.assertRaises(ValueError):
      clip.t_number = [0.7]

    value = (4000, 8000)

    clip.t_number = value

    self.assertTupleEqual(clip.t_number, value)

  def test_focal_length(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.focal_length)

    with self.assertRaises(ValueError):
      clip.focal_length = [Fraction(5,7)]

    value = (100, 7)

    clip.focal_length = value

    self.assertTupleEqual(clip.focal_length, value)

  def test_focal_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.focal_position)

    with self.assertRaises(ValueError):
      clip.focal_position = [Fraction(5,7)]

    value = (100, 7)

    clip.focal_position = value

    self.assertTupleEqual(clip.focal_position, value)

  def test_entrance_pupil_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.entrance_pupil_position)

    with self.assertRaises(ValueError):
      clip.focal_position = [0.6]

    value = (Fraction(5,7), 7)

    clip.set_entrance_pupil_position = value

    self.assertIsNone(clip.entrance_pupil_position, value)

  def test_white_balance(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.white_balance)

    with self.assertRaises(ValueError):
      clip.white_balance = 0.5

    value = 6500

    clip.white_balance = value

    self.assertEqual(clip.white_balance, value)
