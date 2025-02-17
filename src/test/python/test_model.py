#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Generic camera classic tests'''

import unittest

from camdkit.framework import *
from camdkit.model import *

from camdkit.camera_types import PhysicalDimensions, SenselDimensions
from camdkit.numeric_types import StrictlyPositiveRational
from camdkit.timing_types import PTPLeaderTimeSource


class ModelTest(unittest.TestCase):

  def test_duration(self):
    clip = Clip()

    self.assertIsNone(clip.duration)

    clip.duration = 3

    self.assertEqual(clip.duration, StrictlyPositiveRational(3, 1))

  def test_serialize(self):
    self.maxDiff = None # Make sure we log large diffs here
    clip = Clip()

    # Static parameters
    clip.active_sensor_physical_dimensions = PhysicalDimensions(width=36.0, height=24.0)
    clip.active_sensor_resolution = SenselDimensions(width=3840, height=2160)
    clip.anamorphic_squeeze = 1
    clip.capture_frame_rate = Fraction(24000, 1001)
    clip.duration = 3
    clip.camera_make = "Bob"
    clip.camera_model = "Hello"
    clip.camera_serial_number = "132456"
    clip.camera_firmware = "7.1"
    clip.camera_label = "A"
    clip.tracker_make = "ABCD"
    clip.tracker_model = "EFGH"
    clip.tracker_firmware = "1.0.1a"
    clip.tracker_serial_number = "1234567890A"
    clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.iso = 13
    clip.lens_distortion_overscan_max = 1.2
    clip.lens_undistortion_overscan_max = 1.2
    clip.lens_make = "ABC"
    clip.lens_model = "FGH"
    clip.lens_firmware = "1-dev.1"
    clip.lens_serial_number = "123456789"
    clip.lens_nominal_focal_length = 24
    clip.lens_calibration_history = ("LensMaker 123", "TrackerMaker 123")
    clip.shutter_angle = 180
    # Regular parameters
    clip.sample_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7")
    clip.source_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                      "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9")
    clip.source_number = (1,2)
    clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION),
                     VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION))
    clip.tracker_status = ("Optical Good","Optical Good")
    clip.tracker_recording = (False,True)
    clip.tracker_slate = ("A101_A_4","A101_A_5")
    clip.tracker_notes = ("Test serialize.","Test serialize.")
    clip.related_sample_ids = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"),
                               ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"))
    clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),
                         GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0))

    clip.timing_mode = (TimingModeEnum.INTERNAL,
                        TimingModeEnum.INTERNAL)
    clip.timing_sample_timestamp = (Timestamp(1718806554, 0),
                                    Timestamp(1718806555, 0))
    clip.timing_recorded_timestamp = (Timestamp(1718806000, 0),
                                      Timestamp(1718806001, 0))
    clip.timing_sequence_number = (0,1)
    clip.timing_sample_rate = (Fraction(24000, 1001), Fraction(24000, 1001))
    clip.timing_timecode = (Timecode(hours=1, minutes=2, seconds=3, frames=4,
                                     frame_rate=StrictlyPositiveRational(24, 1),
                                     sub_frame=0),
                            Timecode(hours=1, minutes=2, seconds=3, frames=5,
                                     frame_rate=StrictlyPositiveRational(24, 1),
                                     sub_frame=0))
    sync = Synchronization(
      frequency=Fraction(24000, 1001),
      locked=True,
      offsets=SynchronizationOffsets(1.0,2.0,3.0),
      present=True,
      ptp=SynchronizationPTP(profile=PTPProfile.SMPTE_2059_2_2021,
                             domain=1,
                             leader_identity="00:11:22:33:44:55",
                             leader_priorities=SynchronizationPTPPriorities(128, 128),
                             leader_accuracy=0.1,
                             leader_time_source=PTPLeaderTimeSource.GNSS,
                             mean_path_delay=0.2,
                             vlan=100),
      source=SynchronizationSourceEnum.PTP)
    clip.timing_synchronization = (sync,sync)
    
    translation = Vector3(x=1.0, y=2.0, z=3.0)
    rotation = Rotator3(pan=1.0, tilt=2.0, roll=3.0)
    clip.transforms = ((Transform(translation=translation, rotation=rotation),
                        Transform(translation=translation, rotation=rotation)),
                       (Transform(translation=translation, rotation=rotation),
                        Transform(translation=translation, rotation=rotation)))

    clip.lens_t_number = (2000, 4000)
    clip.lens_f_number = (1200, 2800)
    clip.lens_pinhole_focal_length = (2.0, 4.0)
    clip.lens_focus_distance = (2, 4)
    clip.lens_entrance_pupil_offset = (1.23, 2.34)
    clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),
                          FizEncoders(focus=0.1, iris=0.2, zoom=0.3))
    clip.lens_raw_encoders = (RawFizEncoders(focus=1, iris=2, zoom=3),
                              RawFizEncoders(focus=1, iris=2, zoom=3))
    clip.lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),
                                  ExposureFalloff(1.0, 2.0, 3.0))
    clip.lens_distortions = ((Distortion(radial=(1.0, 2.0, 3.0),
                                         tangential=(1.0, 2.0),
                                         overscan=3.0),
                              Distortion(model="Brown-Conrady U-D",
                                         radial=(1.0, 2.0, 3.0),
                                         tangential=(1.0, 2.0),
                                         overscan=4.0)),
                             (Distortion(radial=(1.0, 2.0, 3.0),
                                         tangential=(1.0, 2.0),
                                         overscan=3.0),
                              Distortion(model="Brown-Conrady U-D",
                                         radial=(1.0, 2.0, 3.0),
                                         tangential=(1.0, 2.0),
                                         overscan=4.0)))
    clip.lens_distortion_offset = (DistortionOffset(1.0, 2.0),DistortionOffset(1.0, 2.0))
    clip.lens_projection_offset = (ProjectionOffset(0.1, 0.2),ProjectionOffset(0.1, 0.2))

    d = Clip.to_json(clip)

    # Static parameters
    self.assertEqual(d["static"]["duration"], {"num": 3, "denom": 1})
    self.assertEqual(d["static"]["camera"]["captureFrameRate"], {"num": 24000, "denom": 1001})
    self.assertDictEqual(d["static"]["camera"]["activeSensorPhysicalDimensions"], {"height": 24.0, "width": 36.0})
    self.assertDictEqual(d["static"]["camera"]["activeSensorResolution"], {"height": 2160, "width": 3840})
    self.assertEqual(d["static"]["camera"]["make"], "Bob")
    self.assertEqual(d["static"]["camera"]["model"], "Hello")
    self.assertEqual(d["static"]["camera"]["serialNumber"], "132456")
    self.assertEqual(d["static"]["camera"]["firmwareVersion"], "7.1")
    self.assertEqual(d["static"]["camera"]["label"], "A")
    self.assertEqual(d["static"]["lens"]["distortionOverscanMax"], 1.2)
    self.assertEqual(d["static"]["lens"]["undistortionOverscanMax"], 1.2)
    self.assertEqual(d["static"]["lens"]["make"], "ABC")
    self.assertEqual(d["static"]["lens"]["model"], "FGH")
    self.assertEqual(d["static"]["lens"]["serialNumber"], "123456789")
    self.assertEqual(d["static"]["lens"]["firmwareVersion"], "1-dev.1")
    self.assertEqual(d["static"]["lens"]["nominalFocalLength"], 24)
    self.assertEqual(d["static"]["lens"]["calibrationHistory"], ("LensMaker 123", "TrackerMaker 123"))
    self.assertEqual(d["static"]["tracker"]["make"], "ABCD")
    self.assertEqual(d["static"]["tracker"]["model"], "EFGH")
    self.assertEqual(d["static"]["tracker"]["serialNumber"], "1234567890A")
    self.assertEqual(d["static"]["tracker"]["firmwareVersion"], "1.0.1a")
    self.assertEqual(d["static"]["camera"]["anamorphicSqueeze"], {"num": 1, "denom": 1})
    self.assertEqual(d["static"]["camera"]["isoSpeed"], 13)
    self.assertEqual(d["static"]["camera"]["fdlLink"], "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    self.assertEqual(d["static"]["camera"]["shutterAngle"], 180)

    # Regular parameters

    self.assertTupleEqual(d["sampleId"], ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                          "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"))
    self.assertTupleEqual(d["sourceId"], ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                          "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"))
    self.assertTupleEqual(d["sourceNumber"], (1, 2))
    self.assertTupleEqual(d["protocol"], ({"name": OPENTRACKIO_PROTOCOL_NAME, "version": OPENTRACKIO_PROTOCOL_VERSION},
                                          {"name": OPENTRACKIO_PROTOCOL_NAME, "version": OPENTRACKIO_PROTOCOL_VERSION}))
    self.assertTupleEqual(d["relatedSampleIds"], (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                                   "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"),
                                                  ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                                   "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9")))
    self.assertTupleEqual(d["globalStage"], ({ "E":100.0, "N":200.0, "U":300.0,
                                               "lat0":100.0, "lon0":200.0, "h0":300.0 },
                                             { "E":100.0, "N":200.0, "U":300.0,
                                               "lat0":100.0, "lon0":200.0, "h0":300.0 }))
    self.assertTupleEqual(d["tracker"]["status"], ("Optical Good","Optical Good"))
    self.assertTupleEqual(d["tracker"]["recording"], (False,True))
    self.assertTupleEqual(d["tracker"]["slate"], ("A101_A_4","A101_A_5"))
    self.assertTupleEqual(d["tracker"]["notes"], ("Test serialize.","Test serialize."))

    self.assertTupleEqual(d["timing"]["mode"], ("internal", "internal"))
    self.assertTupleEqual(d["timing"]["sampleTimestamp"], ({ "seconds": 1718806554, "nanoseconds": 0 },
                                                           { "seconds": 1718806555, "nanoseconds": 0 } ))
    self.assertTupleEqual(d["timing"]["recordedTimestamp"], ({ "seconds": 1718806000, "nanoseconds": 0 },
                                                             { "seconds": 1718806001, "nanoseconds": 0 }))
    self.assertTupleEqual(d["timing"]["sequenceNumber"], (0, 1))
    self.assertTupleEqual(d["timing"]["sampleRate"], ({ "num": 24000, "denom": 1001 }, { "num": 24000, "denom": 1001 }))
    self.assertTupleEqual(d["timing"]["timecode"],
                          ({ "hours":1,"minutes":2,"seconds":3,"frames":4,
                             "frameRate": { "num": 24, "denom": 1 }},
                           { "hours":1,"minutes":2,"seconds":3,"frames":5,
                             "frameRate": { "num": 24, "denom": 1 }}))
    sync_dict = { "present":True,"locked":True,"frequency":{ "num": 24000, "denom": 1001 },"source":"ptp",
                  "ptp": {"profile": PTPProfile.SMPTE_2059_2_2021.value,
                          "domain":1,
                          "leaderIdentity": "00:11:22:33:44:55",
                          "leaderPriorities": {"priority1": 128, "priority2": 128},
                          "leaderAccuracy": 0.1,
                          "leaderTimeSource": PTPLeaderTimeSource.GNSS.value,
                          "meanPathDelay": 0.2,
                          "vlan": 100},
                  "offsets": {"translation":1.0, "rotation":2.0, "lensEncoders":3.0 } }
    self.assertTupleEqual(d["timing"]["synchronization"], (sync_dict, sync_dict))
    transform_dict = { "translation": { "x":1.0,"y":2.0,"z":3.0 }, "rotation": { "pan":1.0,"tilt":2.0,"roll":3.0 } }
    self.assertTupleEqual(d["transforms"], ((transform_dict, transform_dict), (transform_dict, transform_dict)))

    self.assertTupleEqual(d["lens"]["tStop"], (2000, 4000))
    self.assertTupleEqual(d["lens"]["fStop"], (1200, 2800))
    self.assertTupleEqual(d["lens"]["pinholeFocalLength"], (2.0, 4.0))
    self.assertTupleEqual(d["lens"]["focusDistance"], (2, 4))
    self.assertTupleEqual(d["lens"]["entrancePupilOffset"], (1.23, 2.34))
    self.assertTupleEqual(d["lens"]["encoders"], ({ "focus":0.1, "iris":0.2, "zoom":0.3 },
                                                  { "focus":0.1, "iris":0.2, "zoom":0.3 }))
    self.assertTupleEqual(d["lens"]["rawEncoders"], ({ "focus":1, "iris":2, "zoom":3 },
                                                     { "focus":1, "iris":2, "zoom":3 }))
    self.assertTupleEqual(d["lens"]["exposureFalloff"], ({ "a1":1.0,"a2":2.0,"a3":3.0 },
                                                         { "a1":1.0,"a2":2.0,"a3":3.0 }))
    self.assertTupleEqual(d["lens"]["distortion"], (({  # default model is not serialized
                                                      "radial":(1.0,2.0,3.0),
                                                      "tangential":(1.0,2.0),
                                                      "overscan": 3.0},
                                                     {"model": "Brown-Conrady U-D",
                                                      "radial":(1.0, 2.0, 3.0),
                                                      "tangential":(1.0,2.0),
                                                      "overscan": 4.0}),
                                                    ({  # default model is not serialized
                                                      "radial": (1.0, 2.0, 3.0),
                                                      "tangential": (1.0, 2.0),
                                                      "overscan": 3.0},
                                                     {"model": "Brown-Conrady U-D",
                                                      "radial": (1.0, 2.0, 3.0),
                                                      "tangential": (1.0, 2.0),
                                                      "overscan": 4.0})))
    self.assertTupleEqual(d["lens"]["distortionOffset"], ({ "x":1.0,"y":2.0 }, { "x":1.0,"y":2.0 }))
    self.assertTupleEqual(d["lens"]["projectionOffset"], ({ "x":0.1,"y":0.2 }, { "x":0.1,"y":0.2 }))

    d_clip = Clip.from_json(d)
    self.assertEqual(d_clip, clip)


  def test_documentation(self):
    doc = Clip.make_documentation()

    self.assertIn("activeSensorPhysicalDimensions", [e["canonical_name"] for e in doc])

  def test_duration_fraction(self):
    clip = Clip()

    self.assertIsNone(clip.duration)

    clip.duration = Fraction(6, 7)

    with self.assertRaises(ValueError):
      clip.duration = 0.7

    self.assertEqual(clip.duration, StrictlyPositiveRational(6, 7))

  def test_active_sensor_physical_dimensions(self):
    clip = Clip()

    self.assertIsNone(clip.active_sensor_physical_dimensions)

    dims = PhysicalDimensions(4, 5)

    clip.active_sensor_physical_dimensions = dims

    self.assertEqual(clip.active_sensor_physical_dimensions, dims)

  def test_active_sensor_resolution(self):
    clip = Clip()

    self.assertIsNone(clip.active_sensor_resolution)

    dims = SenselDimensions(4, 5)

    clip.active_sensor_resolution = dims

    self.assertEqual(clip.active_sensor_resolution, dims)

  def test_lens_serial_number(self):
    clip = Clip()

    self.assertIsNone(clip.lens_serial_number)

    with self.assertRaises(ValueError):
      clip.lens_serial_number = 0.7

    value = "1231231321"

    clip.lens_serial_number = value

    self.assertEqual(clip.lens_serial_number, value)

  def test_iso(self):
    clip = Clip()

    self.assertIsNone(clip.iso)

    with self.assertRaises(ValueError):
      clip.iso = 0.7

    value = 200

    clip.iso = value

    self.assertEqual(clip.iso, value)

  def test_frame_rate(self):
    clip = Clip()

    self.assertIsNone(clip.capture_frame_rate)

    with self.assertRaises(ValueError):
      clip.capture_frame_rate = 0.7

    with self.assertRaises(ValueError):
      clip.capture_frame_rate = -24

    value = Fraction(24000, 1001)

    clip.capture_frame_rate = value

    self.assertEqual(clip.capture_frame_rate,
                     StrictlyPositiveRational(value.numerator, value.denominator))

  def test_shutter_angle(self):
    clip = Clip()

    self.assertIsNone(clip.shutter_angle)

    with self.assertRaises(ValueError):
      clip.shutter_angle = -0.1

    with self.assertRaises(ValueError):
      clip.shutter_angle = 360.1

    value = 180.0

    clip.shutter_angle = value

    self.assertEqual(clip.shutter_angle, value)

  def test_f_number(self):
    clip = Clip()

    self.assertEqual(clip.lens_f_number, None)

    # TODO identify the error here: is a clip not supposed to accept a list instead of a tuple?
    # pydantic seems to promote automatically (https://docs.pydantic.dev/2.0/usage/types/list_types/)_
    # with self.assertRaises(ValueError):
    #   clip.lens_f_number = [0.7]

    value = (4000, 8000)

    clip.lens_f_number = value

    self.assertTupleEqual(clip.lens_f_number, value)

  def test_t_number(self):
    clip = Clip()

    self.assertEqual(clip.lens_t_number, None)

    # See comment in test_f_number() immediately above
    # with self.assertRaises(ValueError):
    #   clip.lens_t_number = [0.7]

    value = (4000, 8000)

    clip.lens_t_number = value

    self.assertTupleEqual(clip.lens_t_number, value)

  def test_pinhole_focal_length(self):
    clip = Clip()

    self.assertIsNone(clip.lens_pinhole_focal_length)

    with self.assertRaises(ValueError):
      clip.lens_pinhole_focal_length = 0
    with self.assertRaises(ValueError):
      clip.lens_pinhole_focal_length = -1.0

    value = (24.1, 24.2)

    clip.lens_pinhole_focal_length = value

    self.assertTupleEqual(clip.lens_pinhole_focal_length, value)

  def test_nominal_focal_length(self):
    clip = Clip()

    self.assertIsNone(clip.lens_nominal_focal_length)

    with self.assertRaises(ValueError):
      clip.lens_nominal_focal_length = [Fraction(5,7)]

    value = 100.0

    clip.lens_nominal_focal_length = value

    self.assertEqual(clip.lens_nominal_focal_length, value)

  def test_calibration_history(self):
    clip = Clip()

    self.assertIsNone(clip.lens_calibration_history)

    with self.assertRaises(ValueError):
      clip.lens_calibration_history = "Test"

    value = ("Test", "Test")

    clip.lens_calibration_history = value

    self.assertEqual(clip.lens_calibration_history, value)

  def test_focus_position(self):
    clip = Clip()

    self.assertIsNone(clip.lens_focus_distance)

    with self.assertRaises(ValueError):
      clip.lens_focus_distance = [0+1j]
      # This should fail, but does not. Have started a discussion on GitHub for Pydantic:
      #   https://github.com/pydantic/pydantic/discussions/11131
      # clip.lens_focus_distance = [Fraction(5,7)]

    value = (100, 7)

    clip.lens_focus_distance = value

    self.assertTupleEqual(clip.lens_focus_distance, value)

  def test_entrance_pupil_offset(self):
    clip = Clip()

    self.assertIsNone(clip.lens_entrance_pupil_offset)

    with self.assertRaises(ValueError):
      clip.lens_entrance_pupil_offset = Fraction(5,7)

    value = (0.5, 0.7)

    clip.lens_entrance_pupil_offset = value

    self.assertTupleEqual(clip.lens_entrance_pupil_offset, value)

  def test_fdl_link(self):
    clip = Clip()

    self.assertIsNone(clip.fdl_link)

    with self.assertRaises(ValueError):
      clip.fdl_link = "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"

    value = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    clip.fdl_link = value
    self.assertEqual(clip.fdl_link, value)

    # test mixed case

    with self.assertRaises(ValueError):
      clip.fdl_link = "urn:uuid:f81d4fae-7dec-11d0-A765-00a0c91e6Bf6"

  def test_sample_id(self):
    clip = Clip()

    self.assertIsNone(clip.sample_id)

    with self.assertRaises(ValueError):
      clip.sample_id = ""
    with self.assertRaises(ValueError):
      clip.sample_id = ("",)
    with self.assertRaises(ValueError):
      clip.sample_id = ("a",)
    with self.assertRaises(ValueError):
      clip.sample_id = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    with self.assertRaises(ValueError):
      clip.sample_id = ("f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    with self.assertRaises(ValueError):
      clip.sample_id = ("urn:uuid:f81d4fae-7dec-11d0-A765-00a0c91e6Bf6",)

    value = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    clip.sample_id = value
    self.assertEqual(clip.sample_id, value)

  def test_source_id(self):
    clip = Clip()

    self.assertIsNone(clip.source_id)

    with self.assertRaises(ValueError):
      clip.source_id = ""
    with self.assertRaises(ValueError):
      clip.source_id = ("",)
    with self.assertRaises(ValueError):
      clip.source_id = ("a",)
    with self.assertRaises(ValueError):
      clip.source_id = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    with self.assertRaises(ValueError):
      clip.source_id = ("f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    with self.assertRaises(ValueError):
      clip.source_id = ("urn:uuid:f81d4fae-7dec-11d0-A765-00a0c91e6Bf6",)

    value = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",)
    clip.source_id = value
    self.assertEqual(clip.source_id, value)

  def test_source_number(self):
    clip = Clip()

    self.assertIsNone(clip.source_number)

    with self.assertRaises(ValueError):
      clip.source_number = ""
    with self.assertRaises(ValueError):
      clip.source_number = (-1,)

    value = (1,)
    clip.source_number = value
    self.assertEqual(clip.source_number, value)

  def test_protocol(self):
    clip = Clip()

    self.assertIsNone(clip.protocol)

    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol("", (1,2,3)),)
    with self.assertRaises(ValueError):
      # For now, we require the protocol name to be OPENTRACKIO_PROTOCOL_NAME
      clip.protocol = (VersionedProtocol("AnyString", (1,2,3)),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(123, (1,2,3)),)

    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, ()),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, (1,)),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, (1,2)),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, (1,2,3,4)),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, 123),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, 1.23),)
    with self.assertRaises(ValueError):
      clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, "AnyString"),)

    clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION),)

    value = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION),)
    clip.protocol = value
    self.assertTupleEqual(clip.protocol, value)


  def test_tracker_data(self):
    clip = Clip()

    self.assertIsNone(clip.tracker_status)
    self.assertIsNone(clip.tracker_recording)
    self.assertIsNone(clip.tracker_slate)
    self.assertIsNone(clip.tracker_notes)
    self.assertIsNone(clip.related_sample_ids)
    self.assertIsNone(clip.global_stage)

    with self.assertRaises(ValueError):
      clip.tracker_status = ""
    with self.assertRaises(ValueError):
      clip.tracker_recording = 0
    with self.assertRaises(ValueError):
      clip.tracker_recording = "True"
    with self.assertRaises(ValueError):
      clip.tracker_slate = ""
    with self.assertRaises(ValueError):
      clip.tracker_notes = ""
    with self.assertRaises(ValueError):
      clip.related_sample_ids = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                 "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6")
    with self.assertRaises(ValueError):
      clip.global_stage = GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0)
    with self.assertRaises(TypeError):
      clip.global_stage = (GlobalPosition(),)
    with self.assertRaises(TypeError):
      clip.global_stage = (GlobalPosition(100.0),)
    with self.assertRaises(TypeError):
      clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0),)

    value = ("Optical Good",)
    clip.tracker_status = value
    self.assertTupleEqual(clip.tracker_status, value)
    value = (True,False)
    clip.tracker_recording = value
    self.assertTupleEqual(clip.tracker_recording, value)
    value = ("A104_A_4",)
    clip.tracker_slate = value
    self.assertTupleEqual(clip.tracker_slate, value)
    value = ("Test notes",)
    clip.tracker_notes = value
    self.assertTupleEqual(clip.tracker_notes, value)
    value = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
              "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"),)
    clip.related_sample_ids = value
    self.assertTupleEqual(clip.related_sample_ids, value)
    value = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)
    clip.global_stage = value
    self.assertTupleEqual(clip.global_stage, value)

  def test_timing_mode_model(self):
    clip = Clip()

    self.assertIsNone(clip.timing_mode)

    with self.assertRaises(ValueError):
      clip.timing_mode = ""
    with self.assertRaises(ValueError):
      clip.timing_mode = "a"

    value = (TimingModeEnum.INTERNAL, TimingModeEnum.EXTERNAL)
    clip.timing_mode = value
    self.assertEqual(clip.timing_mode, value)

  def test_timing_sample_rate_model(self):
    clip = Clip()

    self.assertIsNone(clip.timing_sample_rate)

    with self.assertRaises(ValueError):
      clip.timing_sample_rate = -1.0

    value = (StrictlyPositiveRational(24000, 1001),)
    clip.timing_sample_rate = value
    self.assertEqual(clip.timing_sample_rate, value)

  def test_timing_sample_timestamp_model(self):
    clip = Clip()

    self.assertIsNone(clip.timing_sample_timestamp)

    with self.assertRaises(ValueError):
      clip.timing_sample_timestamp = 0
    with self.assertRaises(TypeError):
      clip.timing_sample_timestamp = Timestamp(0)

    value = (Timestamp(0,0), Timestamp(1718806800,0))
    clip.timing_sample_timestamp = value
    self.assertEqual(clip.timing_sample_timestamp, value)

  def test_timing_timecode_model(self):
    clip = Clip()

    self.assertIsNone(clip.timing_timecode)

    with self.assertRaises(ValueError):
      clip.timing_timecode = {}
    with self.assertRaises(ValueError):
      clip.timing_timecode = {1,2,3,24,"24"}

    value = Timecode(hours=1, minutes=2, seconds=3, frames=4,
                     frame_rate=StrictlyPositiveRational(24, 1))
    clip.timing_timecode = (value,)
    self.assertEqual(clip.timing_timecode, (value,))

  def test_timing_sequence_number(self):
    clip = Clip()

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
    clip = Clip()

    self.assertIsNone(clip.transforms)
    with self.assertRaises(ValueError):
      clip.timing_mode = "a"
    transform = Transform(
      translation=Vector3(1.0,2.0,3.0),
      rotation=Rotator3(1.0,2.0,3.0),
      scale=Vector3(1.0,2.0,3.0)
    )
    value = ((transform,),)
    clip.transforms = value
    self.assertEqual(clip.transforms, value)

  def test_transforms_to_dict(self):
    j = Transforms.to_json((Transform(
      translation=Vector3(1,2,3),
      rotation=Rotator3(1,2,3)), ))
    self.assertEqual(j, ({
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 }
    },))
    j = Transforms.to_json((Transform(
      translation=Vector3(1,2,3),
      rotation=Rotator3(1,2,3),
      scale=Vector3(1,2,3)), ))
    self.assertEqual(j, ({
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    },))

  def test_transforms_from_dict(self):
    t = Transforms.from_json(({
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 }
    },))
    self.assertEqual(t[0].translation, Vector3(1,2,3))
    self.assertEqual(t[0].rotation, Rotator3(1,2,3))
    t = Transforms.from_json(({
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    },))
    self.assertEqual(t[0].translation, Vector3(1,2,3))
    self.assertEqual(t[0].rotation, Rotator3(1,2,3))
    self.assertEqual(t[0].scale, Vector3(1,2,3))

  def test_timing_mode_enum(self):
    self.assertEqual(TimingMode.INTERNAL, TimingMode(TimingMode.INTERNAL))
    self.assertEqual(TimingMode.EXTERNAL, TimingMode(TimingMode.EXTERNAL))
    with self.assertRaises(ValueError):
      TimingMode("")
    with self.assertRaises(ValueError):
      TimingMode("a")
    with self.assertRaises(ValueError):
      TimingMode(None)
    with self.assertRaises(ValueError):
      TimingMode(0)

  def test_timestamp_limits(self):
    with self.assertRaises(TypeError):
      Timestamp()
    with self.assertRaises(TypeError):
      Timestamp(0)
    self.assertTrue(TimingTimestamp.validate(Timestamp(0,0)))
    self.assertTrue(TimingTimestamp.validate(Timestamp(1,2)))
    self.assertTrue(TimingTimestamp.validate(Timestamp(281474976710655,4294967295)))
    with self.assertRaises(ValueError):
        Timestamp(-1,2)
    with self.assertRaises(ValueError):
        Timestamp(1,-2)
    with self.assertRaises(ValueError):
        Timestamp(0,281474976710655)


  def test_timecode(self):
    with self.assertRaises(ValueError):
      Timecode(hours=0, minutes=0, seconds=0, frames=0,
               frame_rate=StrictlyPositiveRational(0,1),
               sub_frame=0)
    self.assertTrue(TimingTimecode.validate(Timecode(hours=0, minutes=0, seconds=0, frames=0,
                                                     frame_rate=StrictlyPositiveRational(24, 1))))
    self.assertTrue(TimingTimecode.validate(Timecode(hours=1, minutes=2, seconds=3, frames=4,
                                                     frame_rate=StrictlyPositiveRational(24, 1))))
    self.assertTrue(TimingTimecode.validate(Timecode(hours=23, minutes=59, seconds=59, frames=23,
                                                     frame_rate=StrictlyPositiveRational(24, 1))))
    with self.assertRaises(ValueError):
        Timecode(hours=-1, seconds=2, minutes=3, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=24, seconds=2, minutes=3, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=-1, minutes=3, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=60, minutes=3, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=-1, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=60, frames=4,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=-1,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=24,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=24,
        frame_rate=StrictlyPositiveRational(24, 1), sub_frame=1)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=25,
        frame_rate=StrictlyPositiveRational(25, 1), sub_frame=1)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=30,
        frame_rate=StrictlyPositiveRational(30, 1), sub_frame=1)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=30,
        frame_rate=StrictlyPositiveRational(30, 1), sub_frame=1)
    self.assertTrue(TimingTimecode.validate(Timecode(hours=1, minutes=2, seconds=3, frames=119,
                                                     frame_rate=StrictlyPositiveRational(120, 1), sub_frame=0)))
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=120,
        frame_rate=StrictlyPositiveRational(120, 1), sub_frame=0)
    with self.assertRaises(ValueError):
        Timecode(hours=1, seconds=2, minutes=3, frames=120,
        frame_rate=StrictlyPositiveRational(121, 1), sub_frame=0)

  def test_timecode_from_dict(self):
    r = TimingTimecode.from_json({
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "frameRate": {
          "num": 24,
          "denom": 1
        },
      "subFrame": 0,
    })
    self.assertEqual(str(r), str(Timecode(hours=1, minutes=2, seconds=3, frames=4,
                                          frame_rate=StrictlyPositiveRational(24, 1),
                                          sub_frame=0)))

  def test_timecode_to_dict(self):
    j0 = TimingTimecode.to_json(Timecode(hours=1, minutes=2, seconds=3, frames=4,
                                        frame_rate=StrictlyPositiveRational(24, 1),
                                        sub_frame=0))
    # since the explicit sub_frame of zero matches the default, it isn't serialized
    self.assertDictEqual(j0, {
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "frameRate": {
          "num": 24,
          "denom": 1
        }})
    j1 = TimingTimecode.to_json(Timecode(hours=1, minutes=2, seconds=3, frames=4,
                                         frame_rate=StrictlyPositiveRational(24, 1),
                                         sub_frame=1))
    self.assertDictEqual(j1, {
      "hours": 1,
      "minutes": 2,
      "seconds": 3,
      "frames": 4,
      "frameRate": {
        "num": 24,
        "denom": 1
      },
      "subFrame": 1})

  def test_lens_encoders_limits(self):
    clip = Clip()
    self.assertIsNone(clip.lens_encoders)
    self.assertIsNone(clip.lens_raw_encoders)

    clip.lens_encoders = (FizEncoders(focus=0.0),)
    clip.lens_encoders = (FizEncoders(focus=0.5),)
    clip.lens_encoders = (FizEncoders(focus=1.0),)
    clip.lens_encoders = (FizEncoders(zoom=0.5),)
    clip.lens_encoders = (FizEncoders(iris=0.5),)
    clip.lens_encoders = (FizEncoders(focus=0.5, iris=0.5),)
    clip.lens_encoders = (FizEncoders(iris=0.5, zoom=0.5),)
    clip.lens_encoders = (FizEncoders(zoom=0.5, focus=0.5),)
    clip.lens_encoders = (FizEncoders(focus=0.5, iris=0.5, zoom=0.5),)

    clip.lens_raw_encoders = (RawFizEncoders(focus=0),)
    clip.lens_raw_encoders = (RawFizEncoders(focus=5),)
    clip.lens_raw_encoders = (RawFizEncoders(zoom=5),)
    clip.lens_raw_encoders = (RawFizEncoders(iris=5),)
    clip.lens_raw_encoders = (RawFizEncoders(focus=5, iris=5),)
    clip.lens_raw_encoders = (RawFizEncoders(iris=5, zoom=5),)
    clip.lens_raw_encoders = (RawFizEncoders(zoom=5, focus=5),)
    clip.lens_raw_encoders = (RawFizEncoders(focus=5, iris=5, zoom=5),)
    

    with self.assertRaises(ValueError):
      clip.lens_encoders = (FizEncoders(),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (FizEncoders(1, 2, 3),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (FizEncoders(-1, 0, 0),)
    with self.assertRaises(ValueError):
      clip.lens_encoders = (FizEncoders(-1, 0, 0),)

    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (RawFizEncoders(),)
    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (RawFizEncoders(-1, 0, 0),)
    with self.assertRaises(ValueError):
      clip.lens_raw_encoders = (RawFizEncoders(-1, 0, 0),)

    value = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
    clip.lens_encoders = value
    self.assertTupleEqual(clip.lens_encoders, value)
    
    value = (RawFizEncoders(focus=1, iris=2, zoom=3),)
    clip.lens_raw_encoders = value
    self.assertTupleEqual(clip.lens_raw_encoders, value)

  def test_lens_encoders_from_dict(self):
    r = LensEncoders.from_json({
      "focus": 0.1,
      "iris": 0.2,
      "zoom": 0.3,
    })
    self.assertEqual(r, FizEncoders(focus=0.1, iris=0.2, zoom=0.3))
    r = LensRawEncoders.from_json({
      "focus": 1,
      "iris": 2,
      "zoom": 3,
    })
    self.assertEqual(r, RawFizEncoders(focus=1, iris=2, zoom=3))
    
  def test_lens_encoders_to_dict(self):
    j = LensEncoders.to_json(FizEncoders(focus=0.5, iris=0.5, zoom=0.5))
    self.assertDictEqual(j, {
      "focus": 0.5,
      "iris": 0.5,
      "zoom": 0.5,
    })
    j = LensRawEncoders.to_json(RawFizEncoders(focus=5, iris=5, zoom=5))
    self.assertDictEqual(j, {
      "focus": 5,
      "iris": 5,
      "zoom": 5,
    })
    
  def test_lens_distortion_overscan_max(self):
    clip = Clip()

    self.assertIsNone(clip.lens_distortion_overscan_max)

    with self.assertRaises(ValueError):
      clip.lens_distortion_overscan_max = ""
    with self.assertRaises(ValueError):
      clip.lens_distortion_overscan_max = -1.0

    value = 1.2
    clip.lens_distortion_overscan_max = value
    self.assertEqual(clip.lens_distortion_overscan_max, value)
    
  def test_lens_undistortion_overscan_max(self):
    clip = Clip()

    self.assertIsNone(clip.lens_undistortion_overscan_max)

    with self.assertRaises(ValueError):
      clip.lens_undistortion_overscan_max = ""
    with self.assertRaises(ValueError):
      clip.lens_undistortion_overscan_max = -1.0

    value = 1.2
    clip.lens_undistortion_overscan_max = value
    self.assertEqual(clip.lens_undistortion_overscan_max, value)

  def test_lens_exposure_falloff(self):
    clip = Clip()

    self.assertIsNone(clip.lens_exposure_falloff)

    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = ""
    with self.assertRaises(ValueError):
      clip.lens_exposure_falloff = ExposureFalloff(1.0,2.0,3.0)
    with self.assertRaises(TypeError):
      clip.lens_exposure_falloff = (ExposureFalloff(),)

    (ExposureFalloff(1.0),)
    (ExposureFalloff(1.0,2.0),)
    value = (ExposureFalloff(-1.0,1.0,-1.0),)
    clip.lens_exposure_falloff = value
    self.assertTupleEqual(clip.lens_exposure_falloff, value)
    
  def test_lens_exposure_falloff_from_dict(self):
    r = LensExposureFalloff.from_json({
      "a1": 0.5,
      "a2": 0.5,
      "a3": 0.5
    })
    self.assertEqual(r,ExposureFalloff(0.5, 0.5, 0.5))
    
  def test_lens_exposure_falloff_to_dict(self):
    j = LensExposureFalloff.to_json(ExposureFalloff(0.5, 0.5, 0.5))
    self.assertDictEqual(j, {
      "a1": 0.5,
      "a2": 0.5,
      "a3": 0.5
    })
    
  def test_lens_distortions(self):
    clip = Clip()

    self.assertIsNone(clip.lens_distortions)

    with self.assertRaises(ValueError):
      clip.lens_distortions = ""
    with self.assertRaises(ValueError):
      clip.lens_distortions = tuple([])
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((),)
    with self.assertRaises(TypeError):
      clip.lens_distortions = (Distortion((1.0,)),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = (Distortion(radial=(1.0, 2.0), tangential=tuple()),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((Distortion(radial=tuple()),),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((Distortion(radial=tuple(),tangential=tuple()),),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((Distortion(radial=(1.0,), tangential=tuple()),),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((Distortion(model="", radial=(1.0, 2.0), tangential=None),),)
    with self.assertRaises(ValueError):
      clip.lens_distortions = ((Distortion(model="", tangential=(1.0, 2.0), radial=(1.0, 2.0)),),)

    ((Distortion(radial=(1.0,)),),)
    ((Distortion(radial=(1.0, 2.0)),),)
    ((Distortion(radial=(-1.0, 1.0, -1.0)),),)
    ((Distortion(radial=(1.0,),
                 tangential=(0.0,)),),)
    ((Distortion(radial=(1.0, 2.0),
                 tangential=(1.0, 2.0)),),)
    value = ((Distortion(radial=(-1.0, 1.0, -1.0),
                         tangential=(1.0, 2.0, 3.0)),),)
    clip.lens_distortions = value
    self.assertTupleEqual(clip.lens_distortions, value)

  def test_lens_distortions_from_dict(self):
    r = Distortion.from_json(({"model": "TestModel",
                               "radial": (0.1, 0.2, 0.3)}, ))
    self.assertEqual(r, (Distortion(model="TestModel",
                                    radial=(0.1, 0.2, 0.3)), ))
    r = Distortion.from_json(({ "radial": [0.1,0.2,0.3],
                                "tangential": [0.1,0.2,0.3],
                                "model": "TestModel", }, ))
    self.assertEqual(r,(Distortion(model="TestModel",
                                   radial=(0.1, 0.2, 0.3),
                                   tangential=(0.1, 0.2, 0.3)),))

  def test_lens_distortion_to_dict(self):
    j = Distortion.to_json((Distortion(model="TestModel",
                                       radial=(0.1,0.2,0.3)),))
    self.assertEqual(j, ({  "model": "TestModel",
                            "radial": (0.1, 0.2, 0.3),}, ))
    j = Distortion.to_json((Distortion(model="TestModel",
                                       radial=(0.1, 0.2, 0.3),
                                       tangential=(0.1,0.2,0.3),
                                       ),
                            Distortion(model="TestModel2",
                                       radial=(0.1, 0.2, 0.3),
                                       tangential=(0.1, 0.2, 0.3),
                                       )))
    self.assertEqual(j, ({
                           "radial": (0.1,0.2,0.3),
                           "tangential": (0.1,0.2,0.3),
                           "model": "TestModel",
                         }, {
                           "radial": (0.1,0.2,0.3),
                           "tangential": (0.1,0.2,0.3),
                           "model": "TestModel2",
                         }))
    
  def test_lens_distortion_offset(self):
    clip = Clip()
    self.assertIsNone(clip.lens_distortion_offset)

    with self.assertRaises(ValueError):
      clip.lens_distortion_offset = ""
    with self.assertRaises(TypeError):
      clip.lens_distortion_offset = (DistortionOffset(),)
    with self.assertRaises(TypeError):
      clip.lens_distortion_offset = (DistortionOffset(1.0),)
    with self.assertRaises(TypeError):
      clip.lens_distortion_offset = DistortionOffset(1.0)

    value = (DistortionOffset(-1.0,1.0),)
    clip.lens_distortion_offset = value
    self.assertTupleEqual(clip.lens_distortion_offset, value)
    
  def test_lens_distortion_shift_from_dict(self):
    r = LensDistortionOffset.from_json({
      "x": -1.0,
      "y": 1.0
    })
    self.assertEqual(r,DistortionOffset(-1.0,1.0))
    
  def test_lens_distortion_shift_to_dict(self):
    j = LensDistortionOffset.to_json(DistortionOffset(-1.0,1.0))
    self.assertDictEqual(j, {
      "x": -1.0,
      "y": 1.0
    })
    
  def test_lens_projection_offset(self):
    clip = Clip()
    self.assertIsNone(clip.lens_projection_offset)

    with self.assertRaises(ValueError):
      clip.lens_projection_offset = ""
    with self.assertRaises(TypeError):
      clip.lens_projection_offset = (ProjectionOffset(),)
    with self.assertRaises(TypeError):
      clip.lens_projection_offset = (ProjectionOffset(1.0),)
    with self.assertRaises(TypeError):
      clip.lens_projection_offset = ProjectionOffset(1.0)

    value = (ProjectionOffset(-1.0,1.0),)
    clip.lens_projection_offset = value
    self.assertTupleEqual(clip.lens_projection_offset, value)
    
  def test_lens_projection_offset_from_dict(self):
    r = LensProjectionOffset.from_json({
      "x": -1.0,
      "y": 1.0
    })
    self.assertEqual(r,ProjectionOffset(-1.0,1.0))
    
  def test_lens_projection_offset_to_dict(self):
    j = LensProjectionOffset.to_json(ProjectionOffset(-1.0,1.0))
    self.assertDictEqual(j, {
      "x": -1.0,
      "y": 1.0
    })
  
  def test_lens_custom(self):
    clip = Clip()
    self.assertIsNone(clip.lens_custom)

    with self.assertRaises(ValueError):
      clip.lens_custom = ("",)

    value = ((-1.0,1.0),)
    clip.lens_custom = value
    self.assertTupleEqual(clip.lens_custom, value)

  def test_synchronization(self):
    with self.assertRaises(TypeError):
      Synchronization()
    with self.assertRaises(TypeError):
      Synchronization(locked=True)
    with self.assertRaises(TypeError):
      Synchronization(locked=True, frequency=25.0)
    with self.assertRaises(TypeError):
      Synchronization(locked=True, frequency=0.0)
    with self.assertRaises(TypeError):
      Synchronization(locked=True, frequency=-1.0)
    
    clip = Clip()
    self.assertIsNone(clip.timing_synchronization)
      
    value = (Synchronization(locked=True, source=SynchronizationSourceEnum.GENLOCK, frequency=25),)
    clip.timing_synchronization = value
    self.assertTupleEqual(clip.timing_synchronization, value)

  def test_synchronization_ptp(self):
    sync = Synchronization(locked=True, source=SynchronizationSourceEnum.PTP, frequency=25)
    clip = Clip()
    sync.ptp = SynchronizationPTP(profile=PTPProfile.SMPTE_2059_2_2021,
                                  domain=1,
                                  leader_identity="00:11:22:33:44:55",
                                  leader_priorities=SynchronizationPTPPriorities(128, 128),
                                  leader_accuracy=0.1,
                                  mean_path_delay=0.01)
    with self.assertRaises(ValueError):
      sync.ptp.leader = ""
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "00:"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "00:00:00:00:00"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = ":00:00:00:00:00:00"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "12:12:12:12:12:12:12"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "we:te:as:te:gd:ds"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "WE:TE:AS:TE:GD:DS"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.offset = "1"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.domain = "1"
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.domain = -1
      clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.domain = 128
      clip.timing_synchronization = (sync, )

    sync.ptp.domain = 0
    sync.ptp.leader_identity = "00:00:00:00:00:00"
    clip.timing_synchronization = (sync, )
    with self.assertRaises(ValueError):
      sync.ptp.leader = "ab:CD:eF:23:45:67"
