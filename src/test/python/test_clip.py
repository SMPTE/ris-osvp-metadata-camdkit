#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Tests for clips"""

import json
import unittest

from typing import Final
from fractions import Fraction

from camdkit.lens_types import (ExposureFalloff,
                                Distortion, DistortionOffset, ProjectionOffset,
                                FizEncoders, RawFizEncoders)
from camdkit.numeric_types import StrictlyPositiveRational
from camdkit.camera_types import PhysicalDimensions, SenselDimensions
from camdkit.timing_types import Timestamp, Timecode, TimecodeFormat, SynchronizationSource, \
    SynchronizationOffsets, SynchronizationPTP, Synchronization, PTPProfile, SynchronizationPTPPriorities
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.clip import Clip
from camdkit.tracker_types import GlobalPosition

VALID_SAMPLE_ID = "urn:uuid:abcdefab-abcd-abcd-abcd-abcdefabcdef"  # 8-4-4-4-12

class ClipTestCases(unittest.TestCase):
    pass

    # def test_frame_rate_validation(self):
    #     rate = FrameRate(24000, 1001)
    #     self.assertEqual(24000, rate.numerator)
    #     self.assertEqual(1001, rate.denominator)
    #     with self.assertRaises(ValidationError):
    #         FrameRate(-24000, 1001)

    def test_global_static_parameters(self):
        # reference value
        duration = StrictlyPositiveRational(3, 1)

        clip = Clip()
        self.assertIsNone(clip.duration)
        clip.duration = duration
        self.assertEqual(clip.duration, duration)

        clip_as_json = Clip.to_json(clip)
        self.assertEqual(clip_as_json["static"]["duration"], {"num": 3, "denom": 1})

        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_camera_static_parameters(self):
        # reference values
        capture_frame_rate = Fraction(24000, 1001)
        canonical_capture_frame_rate = StrictlyPositiveRational(24000, 1001)
        active_sensor_physical_dimensions = PhysicalDimensions(width=36.0, height=24.0)
        active_sensor_resolution = SenselDimensions(width=3840, height=2160)
        anamorphic_squeeze = Fraction(2, 1)
        canonical_anamorphic_squeeze = StrictlyPositiveRational(2, 1)
        camera_make = "Bob"
        camera_model = "Hello"
        camera_serial_number = "123456"
        camera_firmware = "7.1"
        camera_label = "A"
        iso = 13
        fdl_link = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
        shutter_angle = 180

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.active_sensor_physical_dimensions)
        clip.active_sensor_physical_dimensions = active_sensor_physical_dimensions
        self.assertEqual(active_sensor_physical_dimensions, clip.active_sensor_physical_dimensions)
        self.assertIsNone(clip.active_sensor_resolution)
        clip.active_sensor_resolution = active_sensor_resolution
        self.assertEqual(active_sensor_resolution, clip.active_sensor_resolution)
        self.assertIsNone(clip.anamorphic_squeeze)
        clip.anamorphic_squeeze = anamorphic_squeeze
        self.assertEqual(canonical_anamorphic_squeeze, clip.anamorphic_squeeze)
        self.assertIsNone(clip.capture_frame_rate)
        clip.capture_frame_rate = capture_frame_rate
        self.assertEqual(canonical_capture_frame_rate, clip.capture_frame_rate)
        self.assertIsNone(clip.camera_make)
        clip.camera_make = camera_make
        self.assertEqual(camera_make, clip.camera_make)
        self.assertIsNone(clip.camera_model)
        clip.camera_model = camera_model
        self.assertEqual(camera_model, clip.camera_model)
        self.assertIsNone(clip.camera_serial_number)
        clip.camera_serial_number = camera_serial_number
        self.assertEqual(camera_serial_number, clip.camera_serial_number)
        self.assertIsNone(clip.camera_firmware)
        clip.camera_firmware = camera_firmware
        self.assertEqual(camera_firmware, clip.camera_firmware)
        self.assertIsNone(clip.camera_label)
        clip.camera_label = camera_label
        self.assertEqual(camera_label, clip.camera_label)
        self.assertIsNone(clip.iso)
        clip.iso = iso
        self.assertEqual(iso, clip.iso)
        self.assertIsNone(clip.fdl_link)
        clip.fdl_link = fdl_link
        self.assertEqual(fdl_link, clip.fdl_link)
        self.assertIsNone(clip.shutter_angle)
        clip.shutter_angle = shutter_angle
        self.assertEqual(shutter_angle, clip.shutter_angle)

        clip_as_json = Clip.to_json(clip)
        self.assertEqual(clip_as_json["static"]["camera"]["captureFrameRate"], {"num": 24000, "denom": 1001})
        self.assertDictEqual(clip_as_json["static"]["camera"]["activeSensorPhysicalDimensions"], {"height": 24.0, "width": 36.0})
        self.assertDictEqual(clip_as_json["static"]["camera"]["activeSensorResolution"], {"height": 2160, "width": 3840})
        self.assertEqual(clip_as_json["static"]["camera"]["make"], camera_make)
        self.assertEqual(clip_as_json["static"]["camera"]["model"], camera_model)
        self.assertEqual(clip_as_json["static"]["camera"]["serialNumber"], camera_serial_number)
        self.assertEqual(clip_as_json["static"]["camera"]["firmwareVersion"], "7.1")
        self.assertEqual(clip_as_json["static"]["camera"]["label"], "A")

        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_lens_static_parameters(self):
        # reference values
        lens_distortion_overscan_max = 1.2
        lens_undistortion_overscan_max = 1.2
        lens_distortion_is_projection = True
        lens_make = "ABC"
        lens_model = "FGH"
        lens_firmware = "1-dev.1"
        lens_serial_number = "123456789"
        lens_nominal_focal_length = 24

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.lens_distortion_overscan_max)
        clip.lens_distortion_overscan_max = lens_distortion_overscan_max
        self.assertEqual(lens_distortion_overscan_max, clip.lens_distortion_overscan_max)
        self.assertIsNone(clip.lens_undistortion_overscan_max)
        clip.lens_undistortion_overscan_max = lens_undistortion_overscan_max
        self.assertEqual(lens_undistortion_overscan_max, clip.lens_undistortion_overscan_max)
        self.assertIsNone(clip.lens_distortion_is_projection)
        clip.lens_distortion_is_projection = lens_distortion_is_projection
        self.assertEqual(lens_distortion_is_projection, clip.lens_distortion_is_projection)
        self.assertIsNone(clip.lens_make)
        clip.lens_make = lens_make
        self.assertEqual(lens_make, clip.lens_make)
        self.assertIsNone(clip.lens_model)
        clip.lens_model = lens_model
        self.assertEqual(lens_model, clip.lens_model)
        self.assertIsNone(clip.lens_firmware)
        clip.lens_firmware = lens_firmware
        self.assertEqual(lens_firmware, clip.lens_firmware)
        self.assertIsNone(clip.lens_serial_number)
        clip.lens_serial_number = lens_serial_number
        self.assertEqual(lens_serial_number, clip.lens_serial_number)
        self.assertIsNone(clip.lens_nominal_focal_length)
        clip.lens_nominal_focal_length = lens_nominal_focal_length

        clip_as_json = Clip.to_json(clip)
        self.assertEqual(clip_as_json["static"]["lens"]["distortionOverscanMax"], 1.2)
        self.assertEqual(clip_as_json["static"]["lens"]["undistortionOverscanMax"], 1.2)
        self.assertEqual(clip_as_json["static"]["lens"]["distortionIsProjection"], True)
        self.assertEqual(clip_as_json["static"]["lens"]["make"], "ABC")
        self.assertEqual(clip_as_json["static"]["lens"]["model"], "FGH")
        self.assertEqual(clip_as_json["static"]["lens"]["serialNumber"], "123456789")
        self.assertEqual(clip_as_json["static"]["lens"]["firmwareVersion"], "1-dev.1")
        self.assertEqual(clip_as_json["static"]["lens"]["nominalFocalLength"], 24)

        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_tracker_static_parameters(self):
        # reference values
        tracker_make = "ABC"
        tracker_model = "FGH"
        tracker_serial_number = "1234567890A"
        tracker_firmware = "1.0.1a"

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.tracker_make)
        clip.tracker_make = tracker_make
        self.assertEqual(tracker_make, clip.tracker_make)
        self.assertIsNone(clip.tracker_model)
        clip.tracker_model = tracker_model
        self.assertEqual(tracker_model, clip.tracker_model)
        self.assertIsNone(clip.tracker_serial_number)
        clip.tracker_serial_number = tracker_serial_number
        self.assertEqual(tracker_serial_number, clip.tracker_serial_number)
        self.assertIsNone(clip.tracker_firmware)
        clip.tracker_firmware = tracker_firmware
        self.assertEqual(tracker_firmware, clip.tracker_firmware)

        clip_as_json = Clip.to_json(clip)
        self.assertEqual(clip_as_json["static"]["tracker"]["make"], tracker_make)
        self.assertEqual(clip_as_json["static"]["tracker"]["model"], tracker_model)
        self.assertEqual(clip_as_json["static"]["tracker"]["serialNumber"], tracker_serial_number)
        self.assertEqual(clip_as_json["static"]["tracker"]["firmwareVersion"], tracker_firmware)

        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_lens_regular_parameters(self):
        # reference values
        lens_t_number = (2000, 4000)
        lens_f_number = (1200, 2800)
        lens_pinhole_focal_length = (2.0, 4.0)
        lens_focus_distance = (2, 4)
        lens_entrance_pupil_offset = (1.23, 2.34)
        lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),
                         FizEncoders(focus=0.1, iris=0.2, zoom=0.3))
        lens_raw_encoders = (RawFizEncoders(focus=1, iris=2, zoom=3),
                             RawFizEncoders(focus=1, iris=2, zoom=3))
        lens_distortion_overscan = (1.0, 1.0)
        lens_undistortion_overscan = (1.0, 1.0)
        lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),
                                 ExposureFalloff(1.0, 2.0, 3.0))
        # These (copied from the current main camdkit) fail validation because the typing is for tuples, not lists
        # lens_distortion = (Distortion([1.0, 2.0, 3.0], [1.0, 2.0], "Brown-Conrady D-U"),
        #                    Distortion([1.0, 2.0, 3.0], [1.0, 2.0], "Brown-Conrady D-U"))
        # lens_undistortion = (Distortion([1.0, 2.0, 3.0], [1.0, 2.0], "Brown-Conrady U-D"),
        #                      Distortion([1.0, 2.0, 3.0], [1.0, 2.0], "Brown-Conrady U-D"))
        lens_distortion_d_u = Distortion((1.0, 2.0, 3.0), (1.0, 2.0), "Brown-Conrady D-U")
        lens_distortion_u_d = Distortion((1.0, 2.0, 3.0), (1.0, 2.0), "Brown-Conrady U-D")
        lens_distortion = (lens_distortion_d_u, lens_distortion_u_d)
        lens_distortions = (lens_distortion, lens_distortion)
        lens_undistortions = (lens_distortion, lens_distortion)
        lens_distortion_offset = (DistortionOffset(1.0, 2.0), DistortionOffset(1.0, 2.0))
        lens_projection_offset = (ProjectionOffset(0.1, 0.2), ProjectionOffset(0.1, 0.2))

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.lens_t_number)
        clip.lens_t_number = lens_t_number
        self.assertEqual(lens_t_number, clip.lens_t_number)
        self.assertIsNone(clip.lens_f_number)
        clip.lens_f_number = lens_f_number
        self.assertEqual(lens_f_number, clip.lens_f_number)
        self.assertIsNone(clip.lens_pinhole_focal_length)
        clip.lens_pinhole_focal_length = lens_pinhole_focal_length
        self.assertEqual(lens_pinhole_focal_length, clip.lens_pinhole_focal_length)
        self.assertIsNone(clip.lens_focus_distance)
        clip.lens_focus_distance = lens_focus_distance
        self.assertEqual(lens_focus_distance, clip.lens_focus_distance)
        self.assertIsNone(clip.lens_entrance_pupil_offset)
        clip.lens_entrance_pupil_offset = lens_entrance_pupil_offset
        self.assertEqual(lens_entrance_pupil_offset, clip.lens_entrance_pupil_offset)
        self.assertIsNone(clip.lens_encoders)
        clip.lens_encoders = lens_encoders
        self.assertEqual(lens_encoders, clip.lens_encoders)
        self.assertIsNone(clip.lens_raw_encoders)
        clip.lens_raw_encoders = lens_raw_encoders
        self.assertEqual(lens_raw_encoders, clip.lens_raw_encoders)
        self.assertIsNone(clip.lens_distortion_overscan)
        clip.lens_distortion_overscan = lens_distortion_overscan
        self.assertEqual(lens_distortion_overscan, clip.lens_distortion_overscan)
        self.assertIsNone(clip.lens_undistortion_overscan)
        clip.lens_undistortion_overscan = lens_undistortion_overscan
        self.assertEqual(lens_undistortion_overscan, clip.lens_undistortion_overscan)
        self.assertIsNone(clip.lens_exposure_falloff)
        clip.lens_exposure_falloff = lens_exposure_falloff
        self.assertEqual(lens_exposure_falloff, clip.lens_exposure_falloff)
        self.assertIsNone(clip.lens_distortions)
        clip.lens_distortions = lens_distortions
        self.assertEqual(lens_distortions, clip.lens_distortions)
        # self.assertIsNone(clip.lens_undistortions)
        # clip.lens_undistortions = lens_undistortions
        # self.assertEqual(lens_undistortions, clip.lens_undistortions)
        self.assertIsNone(clip.lens_distortion_offset)
        clip.lens_distortion_offset = lens_distortion_offset
        self.assertEqual(lens_distortion_offset, clip.lens_distortion_offset)
        self.assertIsNone(clip.lens_projection_offset)
        clip.lens_projection_offset = lens_projection_offset
        self.assertEqual(lens_projection_offset, clip.lens_projection_offset)
        
        clip_as_json = Clip.to_json(clip)
        # self.assertTupleEqual(clip_as_json["lens"]["custom"], lens_custom)
        self.assertTupleEqual(clip_as_json["lens"]["tStop"], lens_t_number)
        self.assertTupleEqual(clip_as_json["lens"]["fStop"], lens_f_number)
        self.assertTupleEqual(clip_as_json["lens"]["pinholeFocalLength"], lens_pinhole_focal_length)
        self.assertTupleEqual(clip_as_json["lens"]["focusDistance"], lens_focus_distance)
        self.assertTupleEqual(clip_as_json["lens"]["entrancePupilOffset"], lens_entrance_pupil_offset)
        self.assertTupleEqual(clip_as_json["lens"]["encoders"], ({ "focus":0.1, "iris":0.2, "zoom":0.3 },
                                                                 { "focus":0.1, "iris":0.2, "zoom":0.3 }))
        self.assertTupleEqual(clip_as_json["lens"]["rawEncoders"], ({ "focus":1, "iris":2, "zoom":3 },
                                                                    { "focus":1, "iris":2, "zoom":3 }))
        self.assertTupleEqual(clip_as_json["lens"]["distortionOverscan"], lens_distortion_overscan)
        self.assertTupleEqual(clip_as_json["lens"]["undistortionOverscan"], lens_undistortion_overscan)
        self.assertTupleEqual(clip_as_json["lens"]["exposureFalloff"], ({"a1": 1.0, "a2": 2.0, "a3": 3.0},
                                                             {"a1": 1.0, "a2": 2.0, "a3": 3.0}))
        self.assertTupleEqual(clip_as_json["lens"]["distortion"],(
            (Distortion.to_json(lens_distortion_d_u), Distortion.to_json(lens_distortion_u_d)),
            (Distortion.to_json(lens_distortion_d_u), Distortion.to_json(lens_distortion_u_d))))
        # self.assertTupleEqual(clip_as_json["lens"]["undistortion"],(
        #     (Distortion.to_json(lens_distortion_d_u), Distortion.to_json(lens_distortion_u_d)),
        #     (Distortion.to_json(lens_distortion_d_u), Distortion.to_json(lens_distortion_u_d))))
        self.assertTupleEqual(clip_as_json["lens"]["distortionOffset"], ({"x": 1.0, "y": 2.0}, {"x": 1.0, "y": 2.0}))
        self.assertTupleEqual(clip_as_json["lens"]["projectionOffset"], ({"x": 0.1, "y": 0.2}, {"x": 0.1, "y": 0.2}))

        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_timing_regular_parameters(self):
        # reference values
        timing_mode = ("internal", "internal")
        timing_sample_timestamp = (Timestamp(1718806554, 0),
                                    Timestamp(1718806555, 0))
        timing_recorded_timestamp = (Timestamp(1718806000, 0),
                                      Timestamp(1718806001, 0))
        timing_sequence_number = (0, 1)
        sample_rate = StrictlyPositiveRational(24000, 1001)
        timing_sample_rate = (sample_rate, sample_rate)
        timecode0 = Timecode(1, 2, 3, 4,
                            TimecodeFormat(frame_rate=StrictlyPositiveRational(24, 1),
                                           sub_frame=0))
        timecode1= Timecode(1, 2, 3, 5,
                            TimecodeFormat(frame_rate=StrictlyPositiveRational(24, 1),
                                           sub_frame=1))
        timing_timecode = (timecode0, timecode1)
        ptp = SynchronizationPTP(profile=PTPProfile.SMPTE_2059_2_2021,
                                 domain=1,
                                 leader_identity="00:11:22:33:44:55",
                                 leader_priorities=SynchronizationPTPPriorities(1,2),
                                 leader_accuracy=0.1,
                                 mean_path_delay=0.001)
        sync_offsets = SynchronizationOffsets(translation=1.0, rotation=2.0, lensEncoders=3.0)
        synchronization = Synchronization(present=True,
                                          locked=True,
                                          frequency=sample_rate,
                                          source=SynchronizationSource.PTP,
                                          ptp=ptp,
                                          offsets=sync_offsets)
        timing_synchronization = (synchronization, synchronization)

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.timing_mode)
        clip.timing_mode = timing_mode
        self.assertEqual(timing_mode, clip.timing_mode)
        self.assertIsNone(clip.timing_sample_timestamp)
        clip.timing_sample_timestamp = timing_sample_timestamp
        self.assertEqual(timing_sample_timestamp, clip.timing_sample_timestamp)
        self.assertIsNone(clip.timing_recorded_timestamp)
        clip.timing_recorded_timestamp = timing_recorded_timestamp
        self.assertEqual(timing_recorded_timestamp, clip.timing_recorded_timestamp)
        self.assertIsNone(clip.timing_sequence_number)
        clip.timing_sequence_number = timing_sequence_number
        self.assertEqual(timing_sequence_number, clip.timing_sequence_number)
        self.assertIsNone(clip.timing_sample_rate)
        clip.timing_sample_rate = timing_sample_rate
        self.assertEqual(timing_sample_rate, clip.timing_sample_rate)
        self.assertIsNone(clip.timing_timecode)
        clip.timing_timecode = timing_timecode
        self.assertEqual(timing_timecode, clip.timing_timecode)
        self.assertIsNone(clip.timing_synchronization)
        clip.timing_synchronization = timing_synchronization
        self.assertEqual(timing_synchronization, clip.timing_synchronization)

        clip_as_json = Clip.to_json(clip)
        self.assertTupleEqual(clip_as_json["timing"]["mode"], timing_mode)
        self.assertTupleEqual(clip_as_json["timing"]["sampleTimestamp"], (
            {"seconds": 1718806554, "nanoseconds": 0},
            {"seconds": 1718806555, "nanoseconds": 0}))
        self.assertTupleEqual(clip_as_json["timing"]["recordedTimestamp"], (
            {"seconds": 1718806000, "nanoseconds": 0},
            {"seconds": 1718806001, "nanoseconds": 0}))
        self.assertTupleEqual(clip_as_json["timing"]["sequenceNumber"], timing_sequence_number)
        self.assertTupleEqual(clip_as_json["timing"]["sampleRate"], (
            {"num": 24000, "denom": 1001},
            {"num": 24000, "denom": 1001}))
        self.assertTupleEqual(clip_as_json["timing"]["timecode"], (
            {"hours":1, "minutes":2, "seconds":3, "frames":4,
             "format": {"frameRate": {"num": 24, "denom": 1}}},
            {"hours": 1,"minutes": 2,"seconds": 3,"frames": 5,
             "format": {"frameRate": {"num": 24, "denom": 1},
                        "subFrame": 1}}))
        expected_synchronization_dict = {
            "locked": True,
            "source": "ptp",
            "frequency": {"num": 24000, "denom": 1001},
            "offsets": {"translation": 1.0, "rotation": 2.0, "lensEncoders": 3.0},
            "present": True,
            "ptp": {"profile": PTPProfile.SMPTE_2059_2_2021.value,
                    "domain": 1,
                    "leaderIdentity": "00:11:22:33:44:55",
                    "leaderPriorities": {"priority1": 1, "priority2": 2},
                    "leaderAccuracy": 0.1,
                    "meanPathDelay": 0.001}
        }
        self.assertEqual(clip_as_json["timing"]["synchronization"],
                              (expected_synchronization_dict,
                               expected_synchronization_dict))
        self.assertTupleEqual(clip_as_json["timing"]["synchronization"],
                              (expected_synchronization_dict,
                               expected_synchronization_dict))
        clip_from_json: Clip = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_tracker_regular_parameters(self):
        # reference values
        tracker_status = ("Optical Good", "Optical Good")
        tracker_recording = (False, True)
        tracker_slate = ("A101_A_4", "A101_A_5")
        tracker_notes = ("Test serialize.", "Test serialize.")

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.tracker_status)
        clip.tracker_status = tracker_status
        self.assertEqual(tracker_status, clip.tracker_status)
        self.assertIsNone(clip.tracker_recording)
        clip.tracker_recording = tracker_recording
        self.assertEqual(tracker_recording, clip.tracker_recording)
        self.assertIsNone(clip.tracker_slate)
        clip.tracker_slate = tracker_slate
        self.assertEqual(tracker_slate, clip.tracker_slate)
        self.assertIsNone(clip.tracker_notes)
        clip.tracker_notes = tracker_notes
        self.assertEqual(tracker_notes, clip.tracker_notes)

        clip_as_json = Clip.to_json(clip)
        self.assertTupleEqual(clip_as_json["tracker"]["status"], tracker_status)
        self.assertTupleEqual(clip_as_json["tracker"]["recording"], tracker_recording)
        self.assertTupleEqual(clip_as_json["tracker"]["slate"], tracker_slate)
        self.assertTupleEqual(clip_as_json["tracker"]["notes"], tracker_notes)

        clip_from_json = Clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_global_regular_parameters(self):
        sample_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                     "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7")
        source_id = ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                     "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9")
        source_number = (1, 2)
        related_sample_ids = (("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                                "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"),
                               ("urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf8",
                                "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf9"))
        global_stage = (GlobalPosition(100.0, 200.0, 300.0, 100.0, 200.0, 300.0),
                        GlobalPosition(100.0, 200.0, 300.0, 100.0, 200.0, 300.0))
        translation = Vector3(x=1.0, y=2.0, z=3.0)
        rotation = Rotator3(pan=1.0, tilt=2.0, roll=3.0)
        transforms = ((Transform(translation=translation, rotation=rotation),
                            Transform(translation=translation, rotation=rotation)),
                           (Transform(translation=translation, rotation=rotation),
                            Transform(translation=translation, rotation=rotation)))

        # noinspection DuplicatedCode
        clip = Clip()
        self.assertIsNone(clip.sample_id)
        clip.sample_id = sample_id
        self.assertEqual(sample_id, clip.sample_id)
        self.assertIsNone(clip.source_id)
        clip.source_id = source_id
        self.assertEqual(source_id, clip.source_id)
        self.assertIsNone(clip.source_number)
        clip.source_number = source_number
        self.assertEqual(source_number, clip.source_number)
        self.assertIsNone(clip.related_sample_ids)
        clip.related_sample_ids = related_sample_ids
        self.assertEqual(related_sample_ids, clip.related_sample_ids)
        self.assertIsNone(clip.global_stage)
        clip.global_stage = global_stage
        self.assertEqual(global_stage, clip.global_stage)

        clip_as_json = Clip.to_json(clip)
        self.assertTupleEqual(clip_as_json["sampleId"], sample_id)
        self.assertTupleEqual(clip_as_json["sourceId"], source_id)
        self.assertTupleEqual(clip_as_json["sourceNumber"], source_number)
        self.assertTupleEqual(clip_as_json["relatedSampleIds"], related_sample_ids)
        self.assertTupleEqual(clip_as_json["globalStage"],
                              ({"E": 100.0, "N": 200.0, "U": 300.0,
                                "lat0": 100.0, "lon0": 200.0, "h0": 300.0},
                               {"E": 100.0, "N": 200.0, "U": 300.0,
                                "lat0": 100.0, "lon0": 200.0, "h0": 300.0})
                              )

        clip_from_json = clip.from_json(clip_as_json)
        self.assertEqual(clip, clip_from_json)

    def test_append(self):
        focus_distance_a: Final[tuple[float, ...]] = (1.2, 3.4, 5.6)
        focus_distance_b: Final[tuple[float, ...]] = (7.8, 9.0)
        focus_distance_post_append: Final[tuple[float, ...]] = focus_distance_a + focus_distance_b
        entrance_pupil_offset_a: Final[tuple[float, ...]] = (-0.1, -0.2, -0.3)
        entrance_pupil_offset_post_append: Final[tuple[float, ...]] = entrance_pupil_offset_a
        t_stop_b: Final[tuple[float, ...]] = (11.0, 15.6, 22.0)
        t_stop_post_append: Final[tuple[float, ...]] = t_stop_b
        a = Clip()
        a.lens_focus_distance = focus_distance_a
        a.lens_entrance_pupil_offset = entrance_pupil_offset_a
        b = Clip()
        b.lens_focus_distance = focus_distance_b
        b.lens_t_number = t_stop_b
        a.append(b)
        self.assertEqual(focus_distance_post_append, a.lens_focus_distance)
        self.assertEqual(entrance_pupil_offset_post_append, a.lens_entrance_pupil_offset)
        self.assertEqual(t_stop_post_append, a.lens_t_number)

    def test_make_documentation(self):

        def print_doc_entry(entry, fp) -> None:
            for key in ("python_name",
                        "canonical_name",
                        "description",
                        "constraints",
                        "sampling",
                        "section",
                        "units"):
                print(f"{key}: {entry[key]}", file=fp)

        doc: list[dict[str, str]] = Clip.make_documentation()
        self.assertTrue(len(doc) > 0)
        # if something breaks, uncomment the below, and use diff against a reference
        #
        # sorted_doc = sorted(doc, key=lambda x: x["canonical_name"])
        # print(f"sorted_doc has {len(sorted_doc)} items")
        # with open("/tmp/pydantic-doc.txt", "w") as fp:
        #     for doc_entry in sorted_doc:
        #         print_doc_entry(doc_entry, fp)


if __name__ == '__main__':
    unittest.main()
