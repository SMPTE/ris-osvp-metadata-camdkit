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

    # Static parameters
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
    clip.device_make = "ABCD"
    clip.device_model = "EFGH"
    clip.device_firmware = "1.0.1a"
    clip.device_serial_number = "1234567890A"
    clip.anamorphic_squeeze = 120
    clip.iso = 13
    clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.shutter_angle = 180
    # Regular parameters
    clip.packet_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7")
    clip.protocol = ("OpenTrackIO_0.1.0","OpenTrackIO_0.1.0")

    clip.metadata_status = ("Optical Good","Optical Good")
    clip.metadata_recording = (False,True)
    clip.metadata_slate = ("A101_A_4","A101_A_5")
    clip.metadata_notes = ("Test serialize.","Test serialize.")
    clip.metadata_related_packets = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"),
                                     ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"))
    clip.metadata_global_stage = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),
                                  camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0))

    clip.timing_mode = (camdkit.framework.TimingModeEnum.INTERNAL,
                        camdkit.framework.TimingModeEnum.INTERNAL)
    clip.timing_timestamp = (camdkit.framework.Timestamp(1718806554, 0),
                             camdkit.framework.Timestamp(1718806555, 0))
    clip.timing_recorded_timestamp = (camdkit.framework.Timestamp(1718806000, 0),
                                      camdkit.framework.Timestamp(1718806001, 0))
    clip.timing_sequence_number = (0,1)
    clip.timing_frame_rate = (23.976,23.976)
    clip.timing_timecode = (camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat.TC_24D),
                            camdkit.framework.Timecode(1,2,3,5,camdkit.framework.TimecodeFormat.TC_24D))
    sync = camdkit.framework.Synchronization(
      enabled=True,
      locked=True,
      frequency=23.976,
      source=camdkit.framework.SynchronizationSourceEnum.PTP,
      ptp_offset=0.0,
      ptp_domain=1,
      ptp_master="00:11:22:33:44:55",
      offsets=camdkit.framework.SynchronizationOffsets(1.0,2.0,3.0)
    )
    clip.timing_synchronization = (sync,sync)
    
    translation = camdkit.framework.Vector3(x=1.0, y=2.0, z=3.0)
    rotation = camdkit.framework.Rotator3(pan=1.0, tilt=2.0, roll=3.0)
    clip.transforms = ((camdkit.framework.Transform(translation=translation, rotation=rotation),
                        camdkit.framework.Transform(translation=translation, rotation=rotation)),
                       (camdkit.framework.Transform(translation=translation, rotation=rotation),
                        camdkit.framework.Transform(translation=translation, rotation=rotation)))

    clip.lens_t_number = (2000, 4000)
    clip.lens_f_number = (1200, 2800)
    clip.lens_focal_length = (2.0, 4.0)
    clip.lens_focus_position = (2, 4)
    clip.lens_entrance_pupil_position = (Fraction(1, 2), Fraction(13, 7))
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3),
                          camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3))
    clip.lens_fov_scale = (camdkit.framework.Orientations(1.0, 1.0),camdkit.framework.Orientations(1.0, 1.0))
    clip.lens_exposure_falloff = (camdkit.framework.ExposureFalloff(1.0, 2.0, 3.0),
                                  camdkit.framework.ExposureFalloff(1.0, 2.0, 3.0))
    clip.lens_distortion = (camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]),
                            camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]))
    clip.lens_centre_shift = (camdkit.framework.CentreShift(1.0, 2.0),camdkit.framework.CentreShift(1.0, 2.0))
    clip.lens_perspective_shift = (camdkit.framework.PerspectiveShift(0.1, 0.2),
                                   camdkit.framework.PerspectiveShift(0.1, 0.2))

    d = clip.to_json()

    # Static parameters
    self.assertEqual(d["duration"], {"num": 3, "denom": 1})
    self.assertEqual(d["camera"]["captureRate"], {"num": 24000, "denom": 1001})
    self.assertDictEqual(d["camera"]["activeSensorPhysicalDimensions"], {"height": 480, "width": 640})
    self.assertEqual(d["camera"]["cameraMake"], "Bob")
    self.assertEqual(d["camera"]["cameraModel"], "Hello")
    self.assertEqual(d["camera"]["cameraSerialNumber"], "132456")
    self.assertEqual(d["camera"]["cameraFirmwareVersion"], "7.1")
    self.assertEqual(d["lens"]["lensMake"], "ABC")
    self.assertEqual(d["lens"]["lensModel"], "FGH")
    self.assertEqual(d["lens"]["lensSerialNumber"], "123456789")
    self.assertEqual(d["lens"]["lensFirmwareVersion"], "1-dev.1")
    self.assertEqual(d["device"]["deviceMake"], "ABCD")
    self.assertEqual(d["device"]["deviceModel"], "EFGH")
    self.assertEqual(d["device"]["deviceSerialNumber"], "1234567890A")
    self.assertEqual(d["device"]["deviceFirmwareVersion"], "1.0.1a")
    self.assertEqual(d["camera"]["anamorphicSqueeze"], 120)
    self.assertEqual(d["camera"]["isoSpeed"], 13)
    self.assertEqual(d["camera"]["fdlLink"], "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    self.assertEqual(d["camera"]["shutterAngle"], 180)

    # Regular parameters

    self.assertTupleEqual(d["packetId"], ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                          "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"))
    self.assertTupleEqual(d["protocol"], ("OpenTrackIO_0.1.0","OpenTrackIO_0.1.0"))
    self.assertTupleEqual(d["metadata"]["status"], ("Optical Good","Optical Good"))
    self.assertTupleEqual(d["metadata"]["recording"], (False,True))
    self.assertTupleEqual(d["metadata"]["slate"], ("A101_A_4","A101_A_5"))
    self.assertTupleEqual(d["metadata"]["notes"], ("Test serialize.","Test serialize."))
    self.assertTupleEqual(d["metadata"]["relatedPackets"], (["urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                                             "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"],
                                                            ["urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                                             "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"]))
    self.assertTupleEqual(d["metadata"]["globalStage"], ({ "E":100.0, "N":200.0, "U":300.0,
                                                           "lat0":100.0, "lon0":200.0, "h0":300.0 },
                                                         { "E":100.0, "N":200.0, "U":300.0,
                                                           "lat0":100.0, "lon0":200.0, "h0":300.0 }))

    self.assertTupleEqual(d["timing"]["mode"], ("internal", "internal"))
    self.assertTupleEqual(d["timing"]["timestamp"], ({ "seconds": 1718806554, "nanoseconds": 0 },
                                                     { "seconds": 1718806555, "nanoseconds": 0 } ))
    self.assertTupleEqual(d["timing"]["recordedTimestamp"], ({ "seconds": 1718806000, "nanoseconds": 0 },
                                                             { "seconds": 1718806001, "nanoseconds": 0 }))
    self.assertTupleEqual(d["timing"]["sequenceNumber"], (0, 1))
    self.assertTupleEqual(d["timing"]["frameRate"], (23.976, 23.976))
    self.assertTupleEqual(d["timing"]["timecode"], ({ "hours":1,"minutes":2,"seconds":3,"frames":4,"format": "24D" },
                                                    { "hours":1,"minutes":2,"seconds":3,"frames":5,"format": "24D" }))
    sync_dict = { "enabled":True,"locked":True,"frequency":23.976,"source":"ptp","ptp_offset":0.0,"ptp_domain":1,
                  "ptp_master": "00:11:22:33:44:55","offsets": { "translation":1.0,"rotation":2.0,"encoders":3.0 } }
    self.assertTupleEqual(d["timing"]["synchronization"], (sync_dict, sync_dict))
    transform_dict = { "translation": { "x":1.0,"y":2.0,"z":3.0 }, "rotation": { "pan":1.0,"tilt":2.0,"roll":3.0 } }
    self.assertTupleEqual(d["transforms"], ([transform_dict, transform_dict], [transform_dict, transform_dict]))

    self.assertTupleEqual(d["lens"]["tStop"], (2000, 4000))
    self.assertTupleEqual(d["lens"]["fStop"], (1200, 2800))
    self.assertTupleEqual(d["lens"]["focalLength"], (2.0, 4.0))
    self.assertTupleEqual(d["lens"]["focusPosition"], (2, 4))
    self.assertTupleEqual(d["lens"]["entrancePupilPosition"], ({ "num":1, "denom":2 }, { "num":13, "denom":7 }))
    self.assertTupleEqual(d["lens"]["encoders"], ({ "focus":0.1, "iris":0.2, "zoom":0.3 },
                                                  { "focus":0.1, "iris":0.2, "zoom":0.3 }))
    self.assertTupleEqual(d["lens"]["fovScale"], ({ "horizontal":1.0, "vertical":1.0 },
                                                  { "horizontal":1.0, "vertical":1.0 }))
    self.assertTupleEqual(d["lens"]["exposureFalloff"], ({ "a1":1.0,"a2":2.0,"a3":3.0 },
                                                         { "a1":1.0,"a2":2.0,"a3":3.0 }))
    self.assertTupleEqual(d["lens"]["distortion"], ({ "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] },
                                                    { "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] }))
    self.assertTupleEqual(d["lens"]["centreShift"], ({ "cx":1.0,"cy":2.0 }, { "cx":1.0,"cy":2.0 }))
    self.assertTupleEqual(d["lens"]["perspectiveShift"], ({ "Cx":0.1,"Cy":0.2 }, { "Cx":0.1,"Cy":0.2 }))

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

    self.assertEqual(clip.lens_f_number, None)

    with self.assertRaises(ValueError):
      clip.lens_f_number = [0.7]

    value = (4000, 8000)

    clip.lens_f_number = value

    self.assertTupleEqual(clip.lens_f_number, value)

  def test_t_number(self):
    clip = camdkit.model.Clip()

    self.assertEqual(clip.lens_t_number, None)

    with self.assertRaises(ValueError):
      clip.lens_t_number = [0.7]

    value = (4000, 8000)

    clip.lens_t_number = value

    self.assertTupleEqual(clip.lens_t_number, value)

  def test_focal_length(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_focal_length)

    with self.assertRaises(ValueError):
      clip.lens_focal_length = [Fraction(5,7)]

    value = (100, 7)

    clip.lens_focal_length = value

    self.assertTupleEqual(clip.lens_focal_length, value)

  def test_focus_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_focus_position)

    with self.assertRaises(ValueError):
      clip.lens_focus_position = [Fraction(5,7)]

    value = (100, 7)

    clip.lens_focus_position = value

    self.assertTupleEqual(clip.lens_focus_position, value)

  def test_entrance_pupil_position(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_entrance_pupil_position)

    with self.assertRaises(ValueError):
      clip.lens_focus_position = [0.6]

    value = (Fraction(5,7), 7)

    clip.set_lens_entrance_pupil_position = value

    self.assertIsNone(clip.lens_entrance_pupil_position, value)

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
    self.assertIsNone(clip.metadata_global_stage)

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
    with self.assertRaises(ValueError):
      clip.metadata_global_stage = camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0)
    with self.assertRaises(TypeError):
      clip.metadata_global_stage = (camdkit.framework.GlobalPosition(),)
    with self.assertRaises(TypeError):
      clip.metadata_global_stage = (camdkit.framework.GlobalPosition(100.0),)
    with self.assertRaises(TypeError):
      clip.metadata_global_stage = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0),)

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
    value = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)
    clip.metadata_global_stage = value
    self.assertTupleEqual(clip.metadata_global_stage, value)

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
    self.assertEqual(t[0].translation, camdkit.framework.Vector3(1,2,3))
    self.assertEqual(t[0].rotation, camdkit.framework.Rotator3(1,2,3))
    t = camdkit.model.Transforms.from_json([{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    }])
    self.assertEqual(t[0].translation, camdkit.framework.Vector3(1,2,3))
    self.assertEqual(t[0].rotation, camdkit.framework.Rotator3(1,2,3))
    self.assertEqual(t[0].scale, camdkit.framework.Vector3(1,2,3))

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
    r = camdkit.model.FoVScale.from_json({
      "horizontal": 0.5,
      "vertical": 0.5
    })
    self.assertEqual(r,camdkit.framework.Orientations(0.5, 0.5))
    
  def test_lens_fov_scales_to_dict(self):
    j = camdkit.model.FoVScale.to_json(camdkit.framework.Orientations(0.5, 0.5))
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
    
  def test_lens_centre_shift(self):
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.lens_centre_shift)

    with self.assertRaises(ValueError):
      clip.lens_centre_shift = ""
    with self.assertRaises(TypeError):
      clip.lens_centre_shift = (camdkit.framework.CentreShift(),)
    with self.assertRaises(TypeError):
      clip.lens_centre_shift = (camdkit.framework.CentreShift(1.0),)
    with self.assertRaises(TypeError):
      clip.lens_centre_shift = camdkit.framework.CentreShift(1.0)

    value = (camdkit.framework.CentreShift(-1.0,1.0),)
    clip.lens_centre_shift = value
    self.assertTupleEqual(clip.lens_centre_shift, value)
    
  def test_lens_centre_shift_from_dict(self):
    r = camdkit.model.LensCentreShift.from_json({
      "cx": -1.0,
      "cy": 1.0
    })
    self.assertEqual(r,camdkit.framework.CentreShift(-1.0,1.0))
    
  def test_lens_centre_shift_to_dict(self):
    j = camdkit.model.LensCentreShift.to_json(camdkit.framework.CentreShift(-1.0,1.0))
    self.assertDictEqual(j, {
      "cx": -1.0,
      "cy": 1.0
    })
    
  def test_lens_perspective_shift(self):
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.lens_perspective_shift)

    with self.assertRaises(ValueError):
      clip.lens_perspective_shift = ""
    with self.assertRaises(TypeError):
      clip.lens_perspective_shift = (camdkit.framework.PerspectiveShift(),)
    with self.assertRaises(TypeError):
      clip.lens_perspective_shift = (camdkit.framework.PerspectiveShift(1.0),)
    with self.assertRaises(TypeError):
      clip.lens_perspective_shift = camdkit.framework.PerspectiveShift(1.0)

    value = (camdkit.framework.PerspectiveShift(-1.0,1.0),)
    clip.lens_perspective_shift = value
    self.assertTupleEqual(clip.lens_perspective_shift, value)
    
  def test_lens_perspective_shift_from_dict(self):
    r = camdkit.model.LensPerspectiveShift.from_json({
      "Cx": -1.0,
      "Cy": 1.0
    })
    self.assertEqual(r,camdkit.framework.PerspectiveShift(-1.0,1.0))
    
  def test_lens_perspective_shift_to_dict(self):
    j = camdkit.model.LensPerspectiveShift.to_json(camdkit.framework.PerspectiveShift(-1.0,1.0))
    self.assertDictEqual(j, {
      "Cx": -1.0,
      "Cy": 1.0
    })
  
  def test_lens_custom(self):
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.lens_custom)

    with self.assertRaises(ValueError):
      clip.lens_custom = ("",)

    value = ((-1.0,1.0),)
    clip.lens_custom = value
    self.assertTupleEqual(clip.lens_custom, value)

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
