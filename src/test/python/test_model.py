#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Generic camera model tests'''

import unittest
from fractions import Fraction

import camdkit.framework
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
    self.assertTupleEqual(d["lens"]["fStop"], (1200, 2800))
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

  def test_packet_id(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.packet_id)

    with self.assertRaises(ValueError):
      clip.packet_id = ""
    with self.assertRaises(ValueError):
      clip.packet_id = ("",)
    with self.assertRaises(ValueError):
      clip.packet_id = ("a",)
    with self.assertRaises(ValueError):
      clip.packet_id = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    with self.assertRaises(ValueError):
      clip.packet_id = ("f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    with self.assertRaises(ValueError):
      clip.fdl_link = ("urn:uuid:f81d4fae-7dec-11d0-A765-00a0c91e6Bf6",)

    value = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    clip.packet_id = value
    self.assertEqual(clip.packet_id, value)

  def test_protocol(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.protocol)

    with self.assertRaises(ValueError):
      clip.protocol = ""

    value = ("OpenTrackIO_0.1.0",)
    clip.protocol = value
    self.assertTupleEqual(clip.protocol, value)

  def test_metadata(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.metadata_status)
    self.assertIsNone(clip.metadata_recording)
    self.assertIsNone(clip.metadata_slate)
    self.assertIsNone(clip.metadata_notes)
    self.assertIsNone(clip.metadata_related_packets)

    with self.assertRaises(ValueError):
      clip.metadata_status = ""
    with self.assertRaises(ValueError):
      clip.metadata_recording = 0
    with self.assertRaises(ValueError):
      clip.metadata_recording = "True"
    with self.assertRaises(ValueError):
      clip.metadata_slate = ""
    with self.assertRaises(ValueError):
      clip.metadata_notes = ""
    with self.assertRaises(ValueError):
      clip.metadata_related_packets = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                       "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")

    value = ("Optical Good",)
    clip.metadata_status = value
    self.assertTupleEqual(clip.metadata_status, value)
    value = (True,False)
    clip.metadata_recording = value
    self.assertTupleEqual(clip.metadata_recording, value)
    value = ("A104_A_4",)
    clip.metadata_slate = value
    self.assertTupleEqual(clip.metadata_slate, value)
    value = ("Test notes",)
    clip.metadata_notes = value
    self.assertTupleEqual(clip.metadata_notes, value)
    value = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
              "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"),)
    clip.metadata_related_packets = value
    self.assertTupleEqual(clip.metadata_related_packets, value)

  def test_timing_mode_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_mode)

    with self.assertRaises(ValueError):
      clip.timing_mode = ""
    with self.assertRaises(ValueError):
      clip.timing_mode = "a"

    value = (camdkit.framework.TimingModeEnum.INTERNAL, camdkit.framework.TimingModeEnum.EXTERNAL)
    clip.timing_mode = value
    self.assertEqual(clip.timing_mode, value)

  def test_timing_timestamp_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_frame_rate)

    with self.assertRaises(ValueError):
      clip.timing_frame_rate = -1.0

    value = (24.0,)
    clip.timing_frame_rate = value
    self.assertEqual(clip.timing_frame_rate, value)

  def test_timing_frame_rate_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_timestamp)

    with self.assertRaises(ValueError):
      clip.timing_timestamp = 0
    with self.assertRaises(TypeError):
      clip.timing_timestamp = camdkit.framework.Timestamp(0)

    value = (camdkit.framework.Timestamp(0,0), camdkit.framework.Timestamp(1718806800,0))
    clip.timing_timestamp = value
    self.assertEqual(clip.timing_timestamp, value)

  def test_timing_timecode_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_timecode)

    with self.assertRaises(ValueError):
      clip.timing_timecode = {}
    with self.assertRaises(ValueError):
      clip.timing_timecode = {1,2,3,24,"24"}

    value = camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat.TC_24)
    clip.timing_timecode = (value,)
    self.assertEqual(clip.timing_timecode, (value,))

  def test_timing_sequence_number(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_sequence_number)

    with self.assertRaises(ValueError):
      clip.timing_sequence_number = [Fraction(5,7)]
      
    with self.assertRaises(ValueError):
      clip.timing_sequence_number = -1

    with self.assertRaises(ValueError):
      clip.timing_sequence_number = (-1,)

    value = (0, 1)

    clip.timing_sequence_number = value

    self.assertTupleEqual(clip.timing_sequence_number, value)

  def test_transforms_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.transforms)

    with self.assertRaises(TypeError):
      clip.transforms = camdkit.framework.Transform()
    with self.assertRaises(ValueError):
      clip.timing_mode = "a"
    transform = camdkit.framework.Transform(
      translation=camdkit.framework.Vector3(1.0,2.0,3.0),
      rotation=camdkit.framework.Rotator3(1.0,2.0,3.0),
      scale=camdkit.framework.Vector3(1.0,2.0,3.0)
    )
    value = ((transform,),)
    clip.transforms = value
    self.assertEqual(clip.transforms, value)

  def test_transforms_to_dict(self):
    j = camdkit.model.Transforms.to_json((camdkit.framework.Transform(
      translation=camdkit.framework.Vector3(1,2,3), \
      rotation=camdkit.framework.Rotator3(1,2,3)), ))
    self.assertListEqual(j, [{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 } 
    }])
    j = camdkit.model.Transforms.to_json((camdkit.framework.Transform(
      translation=camdkit.framework.Vector3(1,2,3),
      rotation=camdkit.framework.Rotator3(1,2,3),
      scale=camdkit.framework.Vector3(1,2,3)), ))
    self.assertListEqual(j, [{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    }])
  
  def test_transforms_from_dict(self):
    t = camdkit.model.Transforms.from_json([{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 }
    }])
    self.assertDictEqual(t[0].translation, { "x": 1, "y": 2, "z": 3 })
    self.assertDictEqual(t[0].rotation, { "pan": 1, "tilt": 2, "roll": 3 })
    t = camdkit.model.Transforms.from_json([{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    }])
    self.assertDictEqual(t[0].translation, { "x": 1, "y": 2, "z": 3 })
    self.assertDictEqual(t[0].rotation, { "pan": 1, "tilt": 2, "roll": 3 })
    self.assertDictEqual(t[0].scale, { "x": 1, "y": 2, "z": 3 })

  def test_timing_mode_enum(self):
    param = camdkit.model.TimingMode()
    self.assertTrue(param.validate(camdkit.framework.TimingModeEnum.INTERNAL))
    self.assertTrue(param.validate(camdkit.framework.TimingModeEnum.EXTERNAL))
    self.assertFalse(param.validate(""))
    self.assertFalse(param.validate("a"))
    self.assertFalse(param.validate(None))
    self.assertFalse(param.validate(0))

  def test_timestamp_limits(self):
    with self.assertRaises(TypeError):
      camdkit.framework.Timestamp()
    with self.assertRaises(TypeError):
      camdkit.framework.Timestamp(0)
    self.assertTrue(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(0,0)))
    self.assertTrue(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(1,2)))
    self.assertTrue(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(0,0,0)))
    self.assertTrue(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(1,2,3)))
    self.assertTrue(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(281474976710655,4294967295,4294967295)))
    self.assertFalse(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(-1,2,3)))
    self.assertFalse(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(1,-2,3)))
    self.assertFalse(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(1,2,-3)))
    self.assertFalse(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(0,281474976710655,0)))
    self.assertFalse(camdkit.model.TimingTimestamp.validate(camdkit.framework.Timestamp(0,0,281474976710655)))

  def test_timecode_format(self):
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat.TC_24), 24)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat.TC_24D), 24)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat.TC_25), 25)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat.TC_30), 30)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat.TC_30D), 30)
    with self.assertRaises(TypeError):
      camdkit.framework.TimecodeFormat.to_int()
    with self.assertRaises(ValueError):
      camdkit.framework.TimecodeFormat.to_int(0)
    with self.assertRaises(ValueError):
      camdkit.framework.TimecodeFormat.to_int(24)

  def test_timecode_formats(self):
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode()
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode(1,2,3)
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode(0,0,0,0)
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(0,0,0,0,0)))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(0,0,0,0,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(23,59,59,23,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(-1,2,3,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(24,2,3,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,-1,3,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,60,3,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,-1,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,60,4,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,-1,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,24,camdkit.framework.TimecodeFormat.TC_24)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,24,camdkit.framework.TimecodeFormat.TC_24D)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,25,camdkit.framework.TimecodeFormat.TC_25)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,30,camdkit.framework.TimecodeFormat.TC_30)))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,30,camdkit.framework.TimecodeFormat.TC_30D)))

  def test_timecode_from_dict(self):
    r = camdkit.model.TimingTimecode.from_json({
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "format": camdkit.framework.TimecodeFormat.TC_24
    })
    self.assertEqual(r, camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat.TC_24))

  def test_timecode_to_dict(self):
    j = camdkit.model.TimingTimecode.to_json(camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat.TC_24))
    self.assertDictEqual(j, {
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "format": str(camdkit.framework.TimecodeFormat.TC_24)
    })

  def test_lens_encoders_limits(self):
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.lens_encoders)

    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.0),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=1.0),)
    clip.lens_encoders = (camdkit.framework.Encoders(zoom=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(iris=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5, iris=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(iris=0.5, zoom=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(zoom=0.5, focus=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5),)

    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(1,2,3),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(-1,0,0),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(-1,0,0),)

    value = (camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5),)
    clip.lens_encoders = value
    self.assertTupleEqual(clip.lens_encoders, value)

  def test_lens_encoders_from_dict(self):
    r = camdkit.model.LensEncoders.from_json({
      "focus": 0.5,
      "iris": 0.5,
      "zoom": 0.5,
    })
    self.assertEqual(r,camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5))
    
  def test_lens_encoders_to_dict(self):
    j = camdkit.model.LensEncoders.to_json(camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5))
    self.assertDictEqual(j, {
      "focus": 0.5,
      "iris": 0.5,
      "zoom": 0.5,
    })

  def test_lens_fov_scale(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_fov_scale)

    with self.assertRaises(ValueError):
      clip.lens_fov_scale = ""
    with self.assertRaises(TypeError):
      clip.lens_fov_scale = camdkit.framework.Orientations()
    with self.assertRaises(ValueError):
      clip.lens_fov_scale = camdkit.framework.Orientations(1.0,1.0)
    with self.assertRaises(ValueError):
      clip.lens_fov_scale = (camdkit.framework.Orientations(-1.0,-1.0),)

    value = (camdkit.framework.Orientations(1.0,1.0),)
    clip.lens_fov_scale = value
    self.assertTupleEqual(clip.lens_fov_scale, value)
    
  def test_lens_fov_scale_from_dict(self):
    r = camdkit.model.LensFoVScale.from_json({
      "horizontal": 0.5,
      "vertical": 0.5
    })
    self.assertEqual(r,camdkit.framework.Orientations(0.5, 0.5))
    
  def test_lens_fov_scales_to_dict(self):
    j = camdkit.model.LensFoVScale.to_json(camdkit.framework.Orientations(0.5, 0.5))
    self.assertDictEqual(j, {
      "horizontal": 0.5,
      "vertical": 0.5
    })
    
  def test_lens_exposure_falloff(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_exposure_falloff)

    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = ""
    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = camdkit.framework.ExposureFalloff(1.0,2.0,3.0)
    with self.assertRaises(TypeError):
      clip.lens_exposure_falloff = (camdkit.framework.ExposureFalloff(),)

    value = (camdkit.framework.ExposureFalloff(1.0),)
    value = (camdkit.framework.ExposureFalloff(1.0,2.0),)
    value = (camdkit.framework.ExposureFalloff(-1.0,1.0,-1.0),)
    clip.lens_exposure_falloff = value
    self.assertTupleEqual(clip.lens_exposure_falloff, value)
    
  def test_lens_exposure_falloff_from_dict(self):
    r = camdkit.model.LensExposureFalloff.from_json({
      "a1": 0.5,
      "a2": 0.5,
      "a3": 0.5
    })
    self.assertEqual(r,camdkit.framework.ExposureFalloff(0.5, 0.5, 0.5))
    
  def test_lens_exposure_falloff_to_dict(self):
    j = camdkit.model.LensExposureFalloff.to_json(camdkit.framework.ExposureFalloff(0.5, 0.5, 0.5))
    self.assertDictEqual(j, {
      "a1": 0.5,
      "a2": 0.5,
      "a3": 0.5
    })
    
  def test_lens_distortion(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_distortion)

    with self.assertRaises(ValueError):
      clip.lens_distortion = ""
    with self.assertRaises(ValueError):
      clip.lens_distortion = camdkit.framework.Distortion([1.0])
    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = (camdkit.framework.Distortion([]),)
    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = (camdkit.framework.Distortion([],[]),)
    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = (camdkit.framework.Distortion([1.0],[]),)

    value = (camdkit.framework.Distortion([1.0]),)
    value = (camdkit.framework.Distortion([1.0,2.0]),)
    value = (camdkit.framework.Distortion([-1.0,1.0,-1.0]),)
    value = (camdkit.framework.Distortion([1.0],[0.0]),)
    value = (camdkit.framework.Distortion([1.0,2.0],[1.0,2.0]),)
    value = (camdkit.framework.Distortion([-1.0,1.0,-1.0],[1.0,2.0,3.0]),)
    clip.lens_distortion = value
    self.assertTupleEqual(clip.lens_distortion, value)
    
  def test_lens_distortion_from_dict(self):
    r = camdkit.model.LensDistortion.from_json({
      "radial": [0.1,0.2,0.3],
      "tangential": [0.1,0.2,0.3]
    })
    self.assertEqual(r,camdkit.framework.Distortion([0.1,0.2,0.3],[0.1,0.2,0.3]))
    
  def test_lens_distortion_to_dict(self):
    j = camdkit.model.LensDistortion.to_json(camdkit.framework.Distortion([0.1,0.2,0.3],[0.1,0.2,0.3]))
    self.assertDictEqual(j, {
      "radial": [0.1,0.2,0.3],
      "tangential": [0.1,0.2,0.3]
    })

  def test_synchronization(self):
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization()
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization(locked=True)
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization(locked=True, frequency=25.0)
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization(locked=True, frequency=0.0)
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization(locked=True, frequency=-1.0)
    with self.assertRaises(TypeError):
      camdkit.framework.Synchronization(locked=True, source=camdkit.framework.SynchronizationSourceEnum.GENLOCK)
    
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.timing_synchronization)
      
    value = (camdkit.framework.Synchronization(locked=True, source=camdkit.framework.SynchronizationSourceEnum.GENLOCK, frequency=25.0),)
    clip.timing_synchronization = value
    self.assertTupleEqual(clip.timing_synchronization, value)

  def test_synchronization_mac(self):
    sync = camdkit.framework.Synchronization(locked=True, source=camdkit.framework.SynchronizationSourceEnum.GENLOCK, frequency=25.0)
    clip = camdkit.model.Clip()
    with self.assertRaises(ValueError):
      sync.ptp_master = ""
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = "00:"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = "00:00:00:00:00"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = ":00:00:00:00:00:00"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = "12:12:12:12:12:12:12"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = "we:te:as:te:gd:ds"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp_master = "WE:TE:AS:TE:GD:DS"
      clip.timing_synchronization = (sync, )

    sync.ptp_master = "00:00:00:00:00:00"
    clip.timing_synchronization = (sync, )
    sync.ptp_master = "ab:CD:eF:23:45:67"
    clip.timing_synchronization = (sync, )
