#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types to model time, timing and synchronization"""

import json
import unittest
from pathlib import Path

from pydantic import BaseModel, ValidationError
from pydantic.json_schema import JsonSchemaValue

from camdkit.numeric_types import (MAX_INT_8, MAX_UINT_32, MAX_UINT_48,
                                   Rational, StrictlyPositiveRational)
from camdkit.timing_types import (TimingMode,
                                  TimecodeFormat,
                                  Timecode,
                                  Timestamp,
                                  SynchronizationSource,
                                  SynchronizationOffsets,
                                  SynchronizationPTP,
                                  Synchronization,
                                  Timing)



CLASSIC_TIMING_SCHEMA_PATH = Path("src/test/resources/model/timing.json")
CLASSIC_TIMING_SCHEMA: JsonSchemaValue | None = None


def setUpModule():
    global CLASSIC_TIMING_SCHEMA
    with open(CLASSIC_TIMING_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_TIMING_SCHEMA = json.load(fp)


def tearDownModule():
    pass


class TimingTestCases(unittest.TestCase):

    def test_timecode_format(self):
        with self.assertRaises(ValidationError):
            TimecodeFormat(0, 0)
        with self.assertRaises(ValidationError):
            TimecodeFormat(Rational(-1, 1), 0)
        with self.assertRaises(ValidationError):
            TimecodeFormat(Rational(0, 1), 0)
        frame_rate_30fps_num = 30
        frame_rate_30fps_denom = 1
        frame_rate_30fps = StrictlyPositiveRational(frame_rate_30fps_num,
                                                    frame_rate_30fps_denom)
        frame_rate_ntsc_broadcast_num = 30000
        frame_rate_ntsc_broadcast_denom = 1001
        frame_rate_ntsc_broadcast = StrictlyPositiveRational(frame_rate_ntsc_broadcast_num,
                                                             frame_rate_ntsc_broadcast_denom)
        sub_frame_0: int = 0
        sub_frame_1: int = 1
        tf = TimecodeFormat(frame_rate_30fps, sub_frame_0)
        self.assertEqual(tf.frame_rate, frame_rate_30fps)
        self.assertEqual(tf.sub_frame, sub_frame_0)

        with self.assertRaises(ValidationError):
            tf.frame_rate = "foo"
        with self.assertRaises(ValidationError):
            tf.frame_rate = 29.976
        with self.assertRaises(ValidationError):
            tf.frame_rate = Rational(-1, 1)
        with self.assertRaises(ValidationError):
            TimecodeFormat(frame_rate_30fps, "foo")
        with self.assertRaises(ValidationError):
            TimecodeFormat(frame_rate_30fps, 1.0)
        frame_rate_ntsc_broadcast = StrictlyPositiveRational(30000, 1001)
        tf.frame_rate = frame_rate_ntsc_broadcast
        self.assertEqual(tf.frame_rate, frame_rate_ntsc_broadcast)

        with self.assertRaises(ValidationError):
            tf.sub_frame = "foo"
        tf.sub_frame = sub_frame_1
        self.assertEqual(tf.sub_frame, sub_frame_1)

        timecode_format_as_json = TimecodeFormat.to_json(tf)
        self.assertEqual(timecode_format_as_json["frameRate"]["num"],
                         frame_rate_ntsc_broadcast_num)
        self.assertEqual(timecode_format_as_json["frameRate"]["denom"],
                         frame_rate_ntsc_broadcast_denom)
        self.assertEqual(timecode_format_as_json["subFrame"], sub_frame_1)

        timecode_format_from_json = TimecodeFormat.from_json(timecode_format_as_json)
        self.assertEqual(tf, timecode_format_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("timecode", full_expected_schema["properties"])
        self.assertIn("properties", full_expected_schema["properties"]["timecode"])
        self.assertIn("format", full_expected_schema["properties"]["timecode"]["properties"])
        expected_schema = full_expected_schema["properties"]["timecode"]["properties"]["format"]
        actual_schema = TimecodeFormat.make_json_schema()
        self.assertEqual(expected_schema, actual_schema)

    def test_timecode(self):
        thirty_fps_num = 30
        thirty_fps_denom = 1
        sub_frame = 0
        valid_timecode_format = TimecodeFormat(StrictlyPositiveRational(thirty_fps_num, thirty_fps_denom), sub_frame)
        with self.assertRaises(ValidationError):
            Timecode("foo", 0, 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0.0, 0, 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(-1, 0, 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(24, 0, 0, 0, valid_timecode_format)
        tc = Timecode(0, 0, 0, 0, valid_timecode_format)
        self.assertEqual(0, tc.hours)
        tc = Timecode(23, 0, 0, 0, valid_timecode_format)
        self.assertEqual(23, tc.hours)
        with self.assertRaises(ValidationError):
            Timecode(0, "foo", 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0.0, 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, -1, 0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 60, 0, 0, valid_timecode_format)
        tc = Timecode(0, 59, 0, 0, valid_timecode_format)
        self.assertEqual(59, tc.minutes)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, "foo", 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0.0, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, -1, 0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 60, 0, valid_timecode_format)
        tc = Timecode(0, 0, 59, 0, valid_timecode_format)
        self.assertEqual(59, tc.seconds)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0, "foo", valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0, 0.0, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0, -1, valid_timecode_format)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0, thirty_fps_num, valid_timecode_format)
        tc = Timecode(0, 0, 0, thirty_fps_num - 1, valid_timecode_format)
        self.assertEqual(thirty_fps_num - 1, tc.frames)
        with self.assertRaises(ValidationError):
            Timecode(0, 0, 0, 0, "foo")

        valid_hours: int = 1
        valid_minutes: int = 2
        valid_seconds: int =  3
        valid_frames: int = 4
        tc = Timecode(valid_hours, valid_minutes, valid_seconds, valid_frames, valid_timecode_format)
        with self.assertRaises(ValidationError):
            tc.hours = "foo"
        with self.assertRaises(ValidationError):
            tc.hours = 0.0
        with self.assertRaises(ValidationError):
            tc.hours = -1
        with self.assertRaises(ValidationError):
            tc.hours = 24
        with self.assertRaises(ValidationError):
            tc.minutes = "foo"
        with self.assertRaises(ValidationError):
            tc.minutes = 0.0
        with self.assertRaises(ValidationError):
            tc.minutes = -1
        with self.assertRaises(ValidationError):
            tc.minutes = 60
        with self.assertRaises(ValidationError):
            tc.seconds = "foo"
        with self.assertRaises(ValidationError):
            tc.seconds = 0.0
        with self.assertRaises(ValidationError):
            tc.seconds = -1
        with self.assertRaises(ValidationError):
            tc.seconds = 60
        with self.assertRaises(ValidationError):
            tc.frames = "foo"
        with self.assertRaises(ValidationError):
            tc.frames = 0.0
        with self.assertRaises(ValidationError):
            tc.frames = -1
        with self.assertRaises(ValidationError):
            tc.frames = 120
        with self.assertRaises(ValidationError):
            tc.format = "foo"
        with self.assertRaises(ValidationError):
            tc.format = 0.0
        with self.assertRaises(ValidationError):
            tc.format = 0
        doubled_hours: int = valid_hours * 2
        doubled_minutes: int = valid_minutes * 2
        doubled_seconds: int = valid_seconds * 2
        doubled_frames: int = valid_frames * 2
        thirty_fps_drop_frame_format = TimecodeFormat(StrictlyPositiveRational(30000, 1001), 0)
        tc.hours = doubled_hours
        self.assertEqual(tc.hours, doubled_hours)
        tc.minutes = doubled_minutes
        self.assertEqual(tc.minutes, doubled_minutes)
        tc.seconds = doubled_seconds
        self.assertEqual(tc.seconds, doubled_seconds)
        tc.frames = doubled_frames
        self.assertEqual(tc.frames, doubled_frames)
        tc.format = thirty_fps_drop_frame_format
        self.assertEqual(tc.format, thirty_fps_drop_frame_format)

        timecode_as_json = Timecode.to_json(tc)
        self.assertEqual(timecode_as_json["hours"], doubled_hours)
        self.assertEqual(timecode_as_json["minutes"], doubled_minutes)
        self.assertEqual(timecode_as_json["seconds"], doubled_seconds)
        self.assertEqual(timecode_as_json["frames"], doubled_frames)
        self.assertEqual(timecode_as_json["format"], TimecodeFormat.to_json(thirty_fps_drop_frame_format))

        timecode_from_json = Timecode.from_json(timecode_as_json)
        self.assertEqual(tc, timecode_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("timecode", full_expected_schema["properties"])
        expected_schema = full_expected_schema["properties"]["timecode"]
        actual_schema = Timecode.make_json_schema()
        self.assertEqual(expected_schema, actual_schema)

    def test_timestamp(self):
        with self.assertRaises(ValidationError):
            Timestamp('foo', 0)
        with self.assertRaises(ValidationError):
            Timestamp(0, 'bar')
        with self.assertRaises(ValidationError):
            Timestamp(0, 0.0)
        with self.assertRaises(ValidationError):
            Timestamp(0.0, 0)
        with self.assertRaises(ValidationError):
            Timestamp(-1, 0)
        with self.assertRaises(ValidationError):
            Timestamp(0, -1)
        valid_timestamp = Timestamp(3, 4)
        self.assertEqual(3, valid_timestamp.seconds)
        self.assertEqual(4, valid_timestamp.nanoseconds)
        with self.assertRaises(ValidationError):
            valid_timestamp.seconds = 'foo'
        with self.assertRaises(ValidationError):
            valid_timestamp.nanoseconds = 'bar'
        with self.assertRaises(ValidationError):
            valid_timestamp.seconds = 0.0
        with self.assertRaises(ValidationError):
            valid_timestamp.nanoseconds = 0.0
        with self.assertRaises(ValidationError):
            valid_timestamp.seconds = -1
        with self.assertRaises(ValidationError):
            valid_timestamp.nanoseconds = -1
        with self.assertRaises(ValidationError):
            Timestamp(0, -1)

        timestamp_as_json = Timestamp.to_json(valid_timestamp)
        self.assertEqual(timestamp_as_json["seconds"], 3)
        self.assertEqual(timestamp_as_json["nanoseconds"], 4)

        timestamp_from_json = Timestamp.from_json(timestamp_as_json)
        self.assertEqual(valid_timestamp, timestamp_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("sampleTimestamp", full_expected_schema["properties"])
        expected_schema = full_expected_schema["properties"]["sampleTimestamp"]
        # actual_schema = Timing.make_json_schema()["properties"]["sampleTimestamp"]
        # self.assertEqual(expected_schema, actual_schema)

    def test_synchronization_source_validation(self) -> None:
        # not perfect but better than nothing
        # TODO use changes in snake case to insert underscores
        self.assertListEqual([m.name.lower().replace('_','')
                              for m in SynchronizationSource],
                             [m.value.lower().replace('_','')
                              for m in SynchronizationSource])

    def test_synchronization_offsets_validation(self) -> None:
        valid_translation: float = 1.0
        valid_rotation: float = 2.0
        valid_lens_encoders: float = 3.0
        with self.assertRaises(ValidationError):
            SynchronizationOffsets(translation="foo",
                                   rotation=valid_rotation,
                                   lensEncoders=valid_lens_encoders)
        with self.assertRaises(ValidationError):
            SynchronizationOffsets(translation=valid_translation,
                                   rotation="foo",
                                   lensEncoders=valid_lens_encoders)
        with self.assertRaises(ValidationError):
            SynchronizationOffsets(translation=valid_translation,
                                   rotation=valid_rotation,
                                   lensEncoders="foo")
        valid_offsets = SynchronizationOffsets(translation=valid_translation,
                                               rotation=valid_rotation,
                                               lensEncoders=valid_lens_encoders)

        doubled_translation: float = valid_translation * 2
        doubled_rotation: float = valid_rotation * 2
        doubled_lens_encoders: float = valid_lens_encoders * 2
        valid_offsets.translation = doubled_translation
        self.assertEqual(doubled_translation, valid_offsets.translation)
        valid_offsets.rotation = doubled_rotation
        self.assertEqual(doubled_rotation, valid_offsets.rotation)
        valid_offsets.lensEncoders = doubled_lens_encoders
        self.assertEqual(doubled_lens_encoders, valid_offsets.lensEncoders)
        with self.assertRaises(ValidationError):
            valid_offsets.translation = "foo"
        with self.assertRaises(ValidationError):
            valid_offsets.rotation = "foo"
        with self.assertRaises(ValidationError):
            valid_offsets.lens_encoders = "foo"

        offsets_as_json = SynchronizationOffsets.to_json(valid_offsets)
        self.assertEqual(offsets_as_json["translation"], doubled_translation)
        self.assertEqual(offsets_as_json["rotation"], doubled_rotation)
        self.assertEqual(offsets_as_json["lensEncoders"], doubled_lens_encoders)

        offsets_from_json = SynchronizationOffsets.from_json(offsets_as_json)
        self.assertEqual(valid_offsets, offsets_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("synchronization", full_expected_schema["properties"])
        self.assertIn("properties", full_expected_schema["properties"]["synchronization"])
        self.assertIn("offsets", full_expected_schema["properties"]["synchronization"]["properties"])
        expected_schema = full_expected_schema["properties"]["synchronization"]["properties"]["offsets"]
        actual_schema = SynchronizationOffsets.make_json_schema()
        self.assertDictEqual(expected_schema, actual_schema)

    def test_synchronization_ptp(self):
        min_valid_domain: int = 0
        max_valid_domain: int = MAX_INT_8
        valid_domain: int = 1
        valid_leader: str = "00:11:22:33:44:55"
        valid_offset: float = 1.0
        with self.assertRaises(ValidationError):
            SynchronizationPTP(domain="foo", leader=valid_leader, offset=valid_offset)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(domain=min_valid_domain - 1, leader=valid_leader, offset=valid_offset)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(domain=max_valid_domain + 1, leader=valid_leader, offset=valid_offset)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(domain=valid_domain, leader=0.0, offset=valid_offset)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(domain=valid_domain, leader=valid_leader, offset="foo")
        valid_ptp = SynchronizationPTP(domain=valid_domain, leader=valid_leader, offset=valid_offset)

        updated_domain: int = valid_domain * 2
        updated_leader: str = "00:11:22:33:44:56"
        updated_offset: float = valid_offset * 2
        valid_ptp.domain = updated_domain
        self.assertEqual(updated_domain, valid_ptp.domain)
        valid_ptp.leader = updated_leader
        self.assertEqual(updated_leader, valid_ptp.leader)
        valid_ptp.offset = updated_offset
        self.assertEqual(updated_offset, valid_ptp.offset)
        with self.assertRaises(ValidationError):
            valid_ptp.domain = "foo"
        with self.assertRaises(ValidationError):
            valid_ptp.leader = 0.0
        with self.assertRaises(ValidationError):
            valid_ptp.offset = "foo"

        ptp_as_json = SynchronizationPTP.to_json(valid_ptp)
        self.assertEqual(ptp_as_json["domain"], updated_domain)
        self.assertEqual(ptp_as_json["leader"], updated_leader)
        self.assertEqual(ptp_as_json["offset"], updated_offset)

        ptp_from_json = SynchronizationPTP.from_json(ptp_as_json)
        self.assertEqual(valid_ptp, ptp_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("synchronization", full_expected_schema["properties"])
        self.assertIn("properties", full_expected_schema["properties"]["synchronization"])
        self.assertIn("ptp", full_expected_schema["properties"]["synchronization"]["properties"])
        expected_schema = full_expected_schema["properties"]["synchronization"]["properties"]["ptp"]
        actual_schema = SynchronizationPTP.make_json_schema()
        self.assertEqual(expected_schema, actual_schema)

    def test_synchronization(self):
        valid_locked: bool = True
        valid_synchronization_source: SynchronizationSource = SynchronizationSource.GENLOCK
        valid_frequency_num = 30000
        valid_frequency_denom = 1001
        valid_frequency = StrictlyPositiveRational(valid_frequency_num, valid_frequency_denom)
        valid_translation_offset: float = 1.0
        valid_rotation_offset: float = 1.0
        valid_lens_encoders_offset: float = 1.0
        valid_offsets = SynchronizationOffsets(translation=valid_translation_offset,
                                               rotation=valid_rotation_offset,
                                               lensEncoders=valid_lens_encoders_offset)
        valid_present: bool = True
        valid_ptp_domain: int = 1
        valid_ptp_leader: str = "00:11:22:33:44:55"
        valid_ptp_offset: float = 3.0
        valid_ptp = SynchronizationPTP(domain=valid_ptp_domain,
                                       leader=valid_ptp_leader,
                                       offset=valid_ptp_offset)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            "foo",
                            valid_frequency,
                            valid_offsets,
                            valid_present,
                            valid_ptp)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            "foo",
                            valid_frequency,
                            valid_offsets,
                            valid_present,
                            valid_ptp)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            valid_synchronization_source,
                            "foo",
                            valid_offsets,
                            valid_present,
                            valid_ptp)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            valid_synchronization_source,
                            valid_frequency,
                            "foo",
                            valid_present,
                            valid_ptp)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            valid_synchronization_source,
                            valid_frequency,
                            valid_offsets,
                            "foo",
                            valid_ptp)
        with self.assertRaises(ValidationError):
            Synchronization(valid_locked,
                            valid_synchronization_source,
                            valid_frequency,
                            valid_offsets,
                            valid_present,
                            "foo")
        valid_sync = Synchronization(valid_locked,
                                     valid_synchronization_source,
                                     valid_frequency,
                                     valid_offsets,
                                     valid_present,
                                     valid_ptp)

        updated_locked = not valid_locked
        updated_synchronization_source = SynchronizationSource.PTP
        updated_frequency = StrictlyPositiveRational(valid_frequency_num * 2, valid_frequency_denom)
        updated_translation_offset: float = valid_translation_offset * 2
        updated_rotation_offset: float = valid_rotation_offset * 2
        updated_lens_encoders_offset: float = valid_lens_encoders_offset * 2
        updated_offsets = SynchronizationOffsets(translation=updated_translation_offset,
                                                 rotation=updated_rotation_offset,
                                                 lensEncoders=updated_lens_encoders_offset)
        updated_present: bool = not valid_present
        updated_ptp_domain: int = valid_ptp_domain * 2
        updated_ptp_leader: str = "00:11:22:33:44:56"
        updated_ptp_offset: float = valid_ptp_offset * 2
        updated_ptp = SynchronizationPTP(domain=updated_ptp_domain,
                                         leader=updated_ptp_leader,
                                         offset=updated_ptp_offset)
        valid_sync.locked = updated_locked
        self.assertEqual(updated_locked, valid_sync.locked)
        valid_sync.source = updated_synchronization_source
        valid_sync.frequency = updated_frequency
        self.assertEqual(updated_frequency, valid_sync.frequency)
        valid_sync.offsets = updated_offsets
        self.assertEqual(updated_offsets, valid_sync.offsets)
        valid_sync.present = updated_present
        self.assertEqual(updated_present, valid_sync.present)
        valid_sync.ptp = updated_ptp
        self.assertEqual(updated_ptp, valid_sync.ptp)
        with self.assertRaises(ValidationError):
            valid_sync.locked = "foo"
        with self.assertRaises(ValidationError):
            valid_sync.source = "foo"
        with self.assertRaises(ValidationError):
            valid_sync.frequency = "foo"
        with self.assertRaises(ValidationError):
            valid_sync.offsets = "foo"
        with self.assertRaises(ValidationError):
            valid_sync.present = "foo"
        with self.assertRaises(ValidationError):
            valid_sync.ptp = "foo"

        sync_as_json = Synchronization.to_json(valid_sync)
        self.assertEqual(sync_as_json["locked"], updated_locked)
        self.assertEqual(sync_as_json["source"], updated_synchronization_source)
        self.assertEqual(sync_as_json["frequency"], StrictlyPositiveRational.to_json(updated_frequency))
        self.assertEqual(sync_as_json["offsets"], SynchronizationOffsets.to_json(updated_offsets))
        self.assertEqual(sync_as_json["present"], updated_present)
        self.assertEqual(sync_as_json["ptp"], SynchronizationPTP.to_json(updated_ptp))

        sync_from_json = Synchronization.from_json(sync_as_json)
        self.assertEqual(valid_sync, sync_from_json)

    def test_timing_schemas_match(self):
        expected_schema: JsonSchemaValue = CLASSIC_TIMING_SCHEMA
        actual_schema: JsonSchemaValue = Timing.make_json_schema()
        self.assertEqual(expected_schema, actual_schema)


if __name__ == '__main__':
    unittest.main()
