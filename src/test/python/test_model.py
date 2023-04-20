#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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
    clip.camera_make = "Bob"
    clip.camera_model = "Hello"
    clip.camera_serial_number = "132456"
    clip.camera_firmware = "7.1"
    clip.lens_make = "ABC"
    clip.lens_model = "FGH"
    clip.lens_firmware = "1-dev.1"
    clip.lens_serial_number = "123456789"
    clip.anamorphic_squeeze = 120
    clip.iso = 13
    clip.t_number = (2000, 4000)
    clip.f_number = (1200, 2800)
    clip.focal_length = (2, 4)
    clip.focus_position = (2, 4)
    clip.entrance_pupil_position = (Fraction(1, 2), Fraction(13, 7))
    clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.shutter_angle = 180

    d = clip.to_json()

    self.assertEqual(d["duration"], {"num": 3, "denom": 1})
    self.assertEqual(d["captureRate"], {"num": 24000, "denom": 1001})
    self.assertDictEqual(d["activeSensorPhysicalDimensions"], {"height": 480, "width": 640})
    self.assertEqual(d["cameraMake"], "Bob")
    self.assertEqual(d["cameraModel"], "Hello")
    self.assertEqual(d["cameraSerialNumber"], "132456")
    self.assertEqual(d["cameraFirmwareVersion"], "7.1")
    self.assertEqual(d["lensMake"], "ABC")
    self.assertEqual(d["lensModel"], "FGH")
    self.assertEqual(d["lensSerialNumber"], "123456789")
    self.assertEqual(d["lensFirmwareVersion"], "1-dev.1")
    self.assertEqual(d["anamorphicSqueeze"], 120)
    self.assertEqual(d["isoSpeed"], 13)
    self.assertEqual(d["fdlLink"], "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    self.assertEqual(d["shutterAngle"], 180)
    self.assertTupleEqual(d["tStop"], (2000, 4000))
    self.assertTupleEqual(d["fStop"], (1200, 2800))
    self.assertTupleEqual(d["focalLength"], (2, 4))
    self.assertTupleEqual(d["focusPosition"], (2, 4))
    self.assertTupleEqual(d["entrancePupilPosition"], ({"num": 1, "denom": 2}, {"num": 13, "denom": 7}))

    d_clip = camdkit.model.Clip()
    d_clip.from_json(d)

    self.assertDictEqual(d_clip._values, clip._values)

  def test_documentation(self):
    doc = camdkit.model.Clip.make_documentation()

    self.assertIn(camdkit.model.ActiveSensorPhysicalDimensions.canonical_name, [e["canonical_name"] for e in doc])

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

  def test_shutter_angle(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.shutter_angle)

    with self.assertRaises(ValueError):
      clip.shutter_angle = 0

    with self.assertRaises(ValueError):
      clip.shutter_angle = 360001

    value = 180

    clip.shutter_angle = value

    self.assertEqual(clip.shutter_angle, value)

  def test_f_number(self):
    clip = camdkit.model.Clip()

    self.assertEqual(clip.f_number, None)

    with self.assertRaises(ValueError):
      clip.f_number = [0.7]

    value = (4000, 8000)

    clip.f_number = value

    self.assertTupleEqual(clip.f_number, value)

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

  def test_focus_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.focus_position)

    with self.assertRaises(ValueError):
      clip.focus_position = [Fraction(5,7)]

    value = (100, 7)

    clip.focus_position = value

    self.assertTupleEqual(clip.focus_position, value)

  def test_entrance_pupil_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.entrance_pupil_position)

    with self.assertRaises(ValueError):
      clip.focus_position = [0.6]

    value = (Fraction(5,7), 7)

    clip.set_entrance_pupil_position = value

    self.assertIsNone(clip.entrance_pupil_position, value)

  def test_fdl_link(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.fdl_link)

    with self.assertRaises(ValueError):
      clip.fdl_link = "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"

    value = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.fdl_link = value
    self.assertEqual(clip.fdl_link, value)

    # test mixed case

    with self.assertRaises(ValueError):
      clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-A765-00a0c91e6Bf6"
