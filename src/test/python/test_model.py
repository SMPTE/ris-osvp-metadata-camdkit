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

    self.assertIsNone(clip.get_duration())

    clip.set_duration(3)

    self.assertEqual(clip.get_duration(), 3)

  def test_serialize(self):
    clip = camdkit.model.Clip()
    clip.set_duration(3)
    clip.set_iso(13)
    clip.set_focal_length([2, 4])

    d = clip.serialize()

    self.assertEqual(d["focal_length"], (2, 4))
    self.assertEqual(d["duration"], "3")
    self.assertEqual(d["iso"], 13)

  def test_duration(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_duration())

    clip.set_duration(Fraction(6, 7))

    with self.assertRaises(TypeError):
      clip.set_duration(0.7)

    self.assertEqual(clip.get_duration(), Fraction(6, 7))
  
  def test_sensor_physical_dimensions(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_sensor_physical_dimensions())

    dims = camdkit.model.SensorPhysicalDimensions(4, 5)

    clip.set_sensor_physical_dimensions(dims)

    self.assertEqual(clip.get_sensor_physical_dimensions(), dims)


  def test_sensor_pixel_dimensions(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_sensor_pixel_dimensions())

    dims = camdkit.model.SensorPixelDimensions(4, 5)

    clip.set_sensor_pixel_dimensions(dims)

    self.assertEqual(clip.get_sensor_pixel_dimensions(), dims)

  def test_lens_serial_number(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_lens_serial_number())

    with self.assertRaises(TypeError):
      clip.set_lens_serial_number(0.7)

    value = "1231231321"

    clip.set_lens_serial_number(value)

    self.assertEqual(clip.get_lens_serial_number(), value)

  def test_iso(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_iso())

    with self.assertRaises(TypeError):
      clip.set_iso(0.7)

    value = 200

    clip.set_iso(value)

    self.assertEqual(clip.get_iso(), value)

  def test_fps(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.get_fps())

    with self.assertRaises(TypeError):
      clip.set_fps(0.7)

    with self.assertRaises(ValueError):
      clip.set_fps(-24)

    value = Fraction(24000, 1001)

    clip.set_fps(value)

    self.assertEqual(clip.get_fps(), value)


  def test_iris_position(self):
    clip = camdkit.model.Clip()

    self.assertTupleEqual(clip.get_iris_position(), tuple())

    with self.assertRaises(TypeError):
      clip.set_iris_position([0.7])

    value = (Fraction(5,7), 7)

    clip.set_iris_position(value)

    self.assertTupleEqual(clip.get_iris_position(), value)

  def test_focal_length(self):
    clip = camdkit.model.Clip()

    self.assertTupleEqual(clip.get_focal_length(), tuple())

    with self.assertRaises(TypeError):
      clip.set_focal_length([Fraction(5,7)])

    value = (100, 7)

    clip.set_focal_length(value)

    self.assertTupleEqual(clip.get_focal_length(), value)

  def test_focal_position(self):
    clip = camdkit.model.Clip()

    self.assertTupleEqual(clip.get_focal_position(), tuple())

    with self.assertRaises(TypeError):
      clip.set_focal_position([Fraction(5,7)])

    value = (100, 7)

    clip.set_focal_position(value)

    self.assertTupleEqual(clip.get_focal_position(), value)

  def test_entrance_pupil_position(self):
    clip = camdkit.model.Clip()

    self.assertTupleEqual(clip.get_entrance_pupil_position(), tuple())

    with self.assertRaises(TypeError):
      clip.set_focal_position([0.6])

    value = (Fraction(5,7), 7)

    clip.set_entrance_pupil_position(value)

    self.assertTupleEqual(clip.get_entrance_pupil_position(), value)