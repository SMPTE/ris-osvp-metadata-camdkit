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
    self.maxDiff = None # Make sure we log large diffs here
    clip = camdkit.model.Clip()

    # Static parameters
    clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(width=36000, height=24000)
    clip.active_sensor_resolution = camdkit.model.Dimensions(width=3840, height=2160)
    clip.anamorphic_squeeze = 120
    clip.capture_fps = Fraction(24000, 1001)
    clip.duration = 3
    clip.camera_make = "Bob"
    clip.camera_model = "Hello"
    clip.camera_serial_number = "132456"
    clip.camera_firmware = "7.1"
    clip.camera_id = "A"
    clip.device_make = "ABCD"
    clip.device_model = "EFGH"
    clip.device_firmware = "1.0.1a"
    clip.device_serial_number = "1234567890A"
    clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.iso = 13
    clip.lens_make = "ABC"
    clip.lens_model = "FGH"
    clip.lens_firmware = "1-dev.1"
    clip.lens_serial_number = "123456789"
    clip.lens_distortion_model = "OpenLensIO"
    clip.lens_nominal_focal_length = 24
    clip.shutter_angle = 180
    # Regular parameters
    clip.packet_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7")
    clip.protocol = ("OpenTrackIO_0.1.0","OpenTrackIO_0.1.0")

    clip.device_status = ("Optical Good","Optical Good")
    clip.device_recording = (False,True)
    clip.device_slate = ("A101_A_4","A101_A_5")
    clip.device_notes = ("Test serialize.","Test serialize.")
    clip.related_packets = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                             "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"),
                            ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                             "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"))
    clip.global_stage = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),
                         camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0))

    clip.timing_mode = (camdkit.framework.TimingModeEnum.INTERNAL,
                        camdkit.framework.TimingModeEnum.INTERNAL)
    clip.timing_sample_timestamp = (camdkit.framework.Timestamp(1718806554, 0),
                                    camdkit.framework.Timestamp(1718806555, 0))
    clip.timing_recorded_timestamp = (camdkit.framework.Timestamp(1718806000, 0),
                                      camdkit.framework.Timestamp(1718806001, 0))
    clip.timing_sequence_number = (0,1)
    clip.timing_frame_rate = (Fraction(24000, 1001), Fraction(24000, 1001))
    clip.timing_timecode = (camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat(24)),
                            camdkit.framework.Timecode(1,2,3,5,camdkit.framework.TimecodeFormat(24)))
    sync = camdkit.framework.Synchronization(
      present=True,
      locked=True,
      frequency=Fraction(24000, 1001),
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
    clip.lens_entrance_pupil_distance = (Fraction(1, 2), Fraction(13, 7))
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3),
                          camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3))
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(focus=1, iris=2, zoom=3),
                              camdkit.framework.RawEncoders(focus=1, iris=2, zoom=3))
    clip.lens_fov_scale = (camdkit.framework.Orientations(1.0, 1.0),camdkit.framework.Orientations(1.0, 1.0))
    clip.lens_exposure_falloff = (camdkit.framework.ExposureFalloff(1.0, 2.0, 3.0),
                                  camdkit.framework.ExposureFalloff(1.0, 2.0, 3.0))
    clip.lens_distortion = (camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]),
                            camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]))
    clip.lens_undistortion = (camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]),
                              camdkit.framework.Distortion([1.0,2.0,3.0], [1.0,2.0]))
    clip.lens_centre_shift = (camdkit.framework.CentreShift(1.0, 2.0),camdkit.framework.CentreShift(1.0, 2.0))
    clip.lens_perspective_shift = (camdkit.framework.PerspectiveShift(0.1, 0.2),
                                   camdkit.framework.PerspectiveShift(0.1, 0.2))

    d = clip.to_json()

    # Static parameters
    self.assertEqual(d["duration"], {"num": 3, "denom": 1})
    self.assertEqual(d["cameraCaptureRate"], {"num": 24000, "denom": 1001})
    self.assertDictEqual(d["cameraActiveSensorPhysicalDimensions"], {"height": 24000, "width": 36000})
    self.assertDictEqual(d["cameraActiveSensorResolution"], {"height": 2160, "width": 3840})
    self.assertEqual(d["cameraMake"], "Bob")
    self.assertEqual(d["cameraModel"], "Hello")
    self.assertEqual(d["cameraSerialNumber"], "132456")
    self.assertEqual(d["cameraFirmwareVersion"], "7.1")
    self.assertEqual(d["cameraId"], "A")
    self.assertEqual(d["lensMake"], "ABC")
    self.assertEqual(d["lensModel"], "FGH")
    self.assertEqual(d["lensSerialNumber"], "123456789")
    self.assertEqual(d["lensFirmwareVersion"], "1-dev.1")
    self.assertEqual(d["lensDistortionModel"], "OpenLensIO")
    self.assertEqual(d["lensNominalFocalLength"], 24)
    self.assertEqual(d["deviceMake"], "ABCD")
    self.assertEqual(d["deviceModel"], "EFGH")
    self.assertEqual(d["deviceSerialNumber"], "1234567890A")
    self.assertEqual(d["deviceFirmwareVersion"], "1.0.1a")
    self.assertEqual(d["cameraAnamorphicSqueeze"], 120)
    self.assertEqual(d["cameraIsoSpeed"], 13)
    self.assertEqual(d["cameraFdlLink"], "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    self.assertEqual(d["cameraShutterAngle"], 180)

    # Regular parameters

    self.assertTupleEqual(d["packetId"], ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                          "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"))
    self.assertTupleEqual(d["protocol"], ("OpenTrackIO_0.1.0","OpenTrackIO_0.1.0"))
    self.assertTupleEqual(d["relatedPackets"], (["urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                                 "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"],
                                                ["urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                                 "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"]))
    self.assertTupleEqual(d["globalStage"], ({ "E":100.0, "N":200.0, "U":300.0,
                                               "lat0":100.0, "lon0":200.0, "h0":300.0 },
                                             { "E":100.0, "N":200.0, "U":300.0,
                                               "lat0":100.0, "lon0":200.0, "h0":300.0 }))
    self.assertTupleEqual(d["deviceStatus"], ("Optical Good","Optical Good"))
    self.assertTupleEqual(d["deviceRecording"], (False,True))
    self.assertTupleEqual(d["deviceSlate"], ("A101_A_4","A101_A_5"))
    self.assertTupleEqual(d["deviceNotes"], ("Test serialize.","Test serialize."))

    self.assertTupleEqual(d["timingMode"], ("internal", "internal"))
    self.assertTupleEqual(d["timingSampleTimestamp"], ({ "seconds": 1718806554, "nanoseconds": 0 },
                                                       { "seconds": 1718806555, "nanoseconds": 0 } ))
    self.assertTupleEqual(d["timingRecordedTimestamp"], ({ "seconds": 1718806000, "nanoseconds": 0 },
                                                         { "seconds": 1718806001, "nanoseconds": 0 }))
    self.assertTupleEqual(d["timingSequenceNumber"], (0, 1))
    self.assertTupleEqual(d["timingFrameRate"], ({ "num": 24000, "denom": 1001 }, { "num": 24000, "denom": 1001 }))
    self.assertTupleEqual(d["timingTimecode"], ({ "hours":1,"minutes":2,"seconds":3,"frames":4,"format": { "frameRate": { "num": 24, "denom": 1 }, "dropFrame": False } },
                                                { "hours":1,"minutes":2,"seconds":3,"frames":5,"format": { "frameRate": { "num": 24, "denom": 1 }, "dropFrame": False } }))
    sync_dict = { "present":True,"locked":True,"frequency":{ "num": 24000, "denom": 1001 },"source":"ptp","ptp_offset":0.0,"ptp_domain":1,
                  "ptp_master": "00:11:22:33:44:55","offsets": { "translation":1.0,"rotation":2.0,"encoders":3.0 } }
    self.assertTupleEqual(d["timingSynchronization"], (sync_dict, sync_dict))
    transform_dict = { "translation": { "x":1.0,"y":2.0,"z":3.0 }, "rotation": { "pan":1.0,"tilt":2.0,"roll":3.0 } }
    self.assertTupleEqual(d["transforms"], ([transform_dict, transform_dict], [transform_dict, transform_dict]))

    self.assertTupleEqual(d["lensTStop"], (2000, 4000))
    self.assertTupleEqual(d["lensFStop"], (1200, 2800))
    self.assertTupleEqual(d["lensFocalLength"], (2.0, 4.0))
    self.assertTupleEqual(d["lensFocusPosition"], (2, 4))
    self.assertTupleEqual(d["lensEntrancePupilDistance"], ({ "num":1, "denom":2 }, { "num":13, "denom":7 }))
    self.assertTupleEqual(d["lensEncoders"], ({ "focus":0.1, "iris":0.2, "zoom":0.3 },
                                              { "focus":0.1, "iris":0.2, "zoom":0.3 }))
    self.assertTupleEqual(d["lensRawEncoders"], ({ "focus":1, "iris":2, "zoom":3 },
                                                 { "focus":1, "iris":2, "zoom":3 }))
    self.assertTupleEqual(d["lensFovScale"], ({ "horizontal":1.0, "vertical":1.0 },
                                              { "horizontal":1.0, "vertical":1.0 }))
    self.assertTupleEqual(d["lensExposureFalloff"], ({ "a1":1.0,"a2":2.0,"a3":3.0 },
                                                     { "a1":1.0,"a2":2.0,"a3":3.0 }))
    self.assertTupleEqual(d["lensDistortion"], ({ "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] },
                                                { "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] }))
    self.assertTupleEqual(d["lensUndistortion"], ({ "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] },
                                                  { "radial":[1.0,2.0,3.0], "tangential":[1.0,2.0] }))
    self.assertTupleEqual(d["lensCentreShift"], ({ "cx":1.0,"cy":2.0 }, { "cx":1.0,"cy":2.0 }))
    self.assertTupleEqual(d["lensPerspectiveShift"], ({ "Cx":0.1,"Cy":0.2 }, { "Cx":0.1,"Cy":0.2 }))

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

  def test_active_sensor_resolution(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.active_sensor_resolution)

    dims = camdkit.model.Dimensions(4, 5)

    clip.active_sensor_resolution = dims

    self.assertEqual(clip.active_sensor_resolution, dims)

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
      clip.lens_focal_length = 0
    with self.assertRaises(ValueError):
      clip.lens_focal_length = -1.0

    value = (24.1, 24.2)

    clip.lens_focal_length = value

    self.assertTupleEqual(clip.lens_focal_length, value)

  def test_nominal_focal_length(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_nominal_focal_length)

    with self.assertRaises(ValueError):
      clip.lens_nominal_focal_length = [Fraction(5,7)]

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

  def test_entrance_pupil_distance(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.lens_entrance_pupil_distance)

    with self.assertRaises(ValueError):
      clip.lens_entrance_pupil_distance = 0.6

    value = (Fraction(5,7), 7)

    clip.lens_entrance_pupil_distance = value

    self.assertTupleEqual(clip.lens_entrance_pupil_distance, value)

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

  def test_device_data(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.device_status)
    self.assertIsNone(clip.device_recording)
    self.assertIsNone(clip.device_slate)
    self.assertIsNone(clip.device_notes)
    self.assertIsNone(clip.related_packets)
    self.assertIsNone(clip.global_stage)

    with self.assertRaises(ValueError):
      clip.device_status = ""
    with self.assertRaises(ValueError):
      clip.device_recording = 0
    with self.assertRaises(ValueError):
      clip.device_recording = "True"
    with self.assertRaises(ValueError):
      clip.device_slate = ""
    with self.assertRaises(ValueError):
      clip.device_notes = ""
    with self.assertRaises(ValueError):
      clip.related_packets = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                              "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    with self.assertRaises(ValueError):
      clip.global_stage = camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0)
    with self.assertRaises(TypeError):
      clip.global_stage = (camdkit.framework.GlobalPosition(),)
    with self.assertRaises(TypeError):
      clip.global_stage = (camdkit.framework.GlobalPosition(100.0),)
    with self.assertRaises(TypeError):
      clip.global_stage = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0),)

    value = ("Optical Good",)
    clip.device_status = value
    self.assertTupleEqual(clip.device_status, value)
    value = (True,False)
    clip.device_recording = value
    self.assertTupleEqual(clip.device_recording, value)
    value = ("A104_A_4",)
    clip.device_slate = value
    self.assertTupleEqual(clip.device_slate, value)
    value = ("Test notes",)
    clip.device_notes = value
    self.assertTupleEqual(clip.device_notes, value)
    value = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
              "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"),)
    clip.related_packets = value
    self.assertTupleEqual(clip.related_packets, value)
    value = (camdkit.framework.GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)
    clip.global_stage = value
    self.assertTupleEqual(clip.global_stage, value)

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

  def test_timing_frame_rate_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_frame_rate)

    with self.assertRaises(ValueError):
      clip.timing_frame_rate = -1.0

    value = (Fraction(24000, 1001),)
    clip.timing_frame_rate = value
    self.assertEqual(clip.timing_frame_rate, value)

  def test_timing_sample_timestamp_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_sample_timestamp)

    with self.assertRaises(ValueError):
      clip.timing_sample_timestamp = 0
    with self.assertRaises(TypeError):
      clip.timing_sample_timestamp = camdkit.framework.Timestamp(0)

    value = (camdkit.framework.Timestamp(0,0), camdkit.framework.Timestamp(1718806800,0))
    clip.timing_sample_timestamp = value
    self.assertEqual(clip.timing_sample_timestamp, value)

  def test_timing_timecode_model(self):
    clip = camdkit.model.Clip()

    self.assertIsNone(clip.timing_timecode)

    with self.assertRaises(ValueError):
      clip.timing_timecode = {}
    with self.assertRaises(ValueError):
      clip.timing_timecode = {1,2,3,24,"24"}

    value = camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat(24))
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
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat(24)), 24)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat(24, True)), 24)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat(25)), 25)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat(30)), 30)
    self.assertEqual(camdkit.framework.TimecodeFormat.to_int(camdkit.framework.TimecodeFormat(30, True)), 30)
    with self.assertRaises(TypeError):
      camdkit.framework.TimecodeFormat()
    with self.assertRaises(ValueError):
      camdkit.framework.TimecodeFormat(0).to_int()

  def test_timecode_formats(self):
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode()
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode(1,2,3)
    with self.assertRaises(TypeError):
      camdkit.framework.Timecode(0,0,0,0)
    with self.assertRaises(ValueError):
      camdkit.framework.Timecode(0,0,0,0,camdkit.framework.TimecodeFormat(0))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(0,0,0,0,camdkit.framework.TimecodeFormat(24))))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat(24))))
    self.assertTrue(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(23,59,59,23,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(-1,2,3,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(24,2,3,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,-1,3,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,60,3,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,-1,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,60,4,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,-1,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,24,camdkit.framework.TimecodeFormat(24))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,24,camdkit.framework.TimecodeFormat(24, True))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,25,camdkit.framework.TimecodeFormat(25))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,30,camdkit.framework.TimecodeFormat(30))))
    self.assertFalse(camdkit.model.TimingTimecode.validate(camdkit.framework.Timecode(1,2,3,30,camdkit.framework.TimecodeFormat(30, True))))

  def test_timecode_from_dict(self):
    r = camdkit.model.TimingTimecode.from_json({
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "format": {
        "frameRate": {
          "num": 24,
          "denom": 1
        },
        "dropFrame": False
      }
    })
    self.assertEqual(str(r), str(camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat(24))))

  def test_timecode_to_dict(self):
    j = camdkit.model.TimingTimecode.to_json(camdkit.framework.Timecode(1,2,3,4,camdkit.framework.TimecodeFormat(24)))
    self.assertDictEqual(j, {
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "format": {
        "frameRate": {
          "num": 24,
          "denom": 1
        },
        "dropFrame": False
      }
    })

  def test_lens_encoders_limits(self):
    clip = camdkit.model.Clip()
    self.assertIsNone(clip.lens_encoders)
    self.assertIsNone(clip.lens_raw_encoders)

    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.0),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=1.0),)
    clip.lens_encoders = (camdkit.framework.Encoders(zoom=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(iris=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5, iris=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(iris=0.5, zoom=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(zoom=0.5, focus=0.5),)
    clip.lens_encoders = (camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5),)

    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(focus=0),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(focus=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(zoom=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(iris=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(focus=5, iris=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(iris=5, zoom=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(zoom=5, focus=5),)
    clip.lens_raw_encoders = (camdkit.framework.RawEncoders(focus=5, iris=5, zoom=5),)
    

    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(1,2,3),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(-1,0,0),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (camdkit.framework.Encoders(-1,0,0),)

    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (camdkit.framework.RawEncoders(),)
    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (camdkit.framework.RawEncoders(-1,0,0),)
    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (camdkit.framework.RawEncoders(-1,0,0),)

    value = (camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3),)
    clip.lens_encoders = value
    self.assertTupleEqual(clip.lens_encoders, value)
    
    value = (camdkit.framework.RawEncoders(focus=1, iris=2, zoom=3),)
    clip.lens_raw_encoders = value
    self.assertTupleEqual(clip.lens_raw_encoders, value)

  def test_lens_encoders_from_dict(self):
    r = camdkit.model.LensEncoders.from_json({
      "focus": 0.1,
      "iris": 0.2,
      "zoom": 0.3,
    })
    self.assertEqual(r,camdkit.framework.Encoders(focus=0.1, iris=0.2, zoom=0.3))
    r = camdkit.model.LensRawEncoders.from_json({
      "focus": 1,
      "iris": 2,
      "zoom": 3,
    })
    self.assertEqual(r,camdkit.framework.RawEncoders(focus=1, iris=2, zoom=3))
    
  def test_lens_encoders_to_dict(self):
    j = camdkit.model.LensEncoders.to_json(camdkit.framework.Encoders(focus=0.5, iris=0.5, zoom=0.5))
    self.assertDictEqual(j, {
      "focus": 0.5,
      "iris": 0.5,
      "zoom": 0.5,
    })
    j = camdkit.model.LensRawEncoders.to_json(camdkit.framework.RawEncoders(focus=5, iris=5, zoom=5))
    self.assertDictEqual(j, {
      "focus": 5,
      "iris": 5,
      "zoom": 5,
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
      
    value = (camdkit.framework.Synchronization(locked=True, source=camdkit.framework.SynchronizationSourceEnum.GENLOCK, frequency=25),)
    clip.timing_synchronization = value
    self.assertTupleEqual(clip.timing_synchronization, value)

  def test_synchronization_mac(self):
    sync = camdkit.framework.Synchronization(locked=True, source=camdkit.framework.SynchronizationSourceEnum.GENLOCK, frequency=25)
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
