#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types to classic time, timing and synchronization"""

import json
import unittest
from pathlib import Path
from typing import Final

from pydantic import ValidationError
from pydantic.json_schema import JsonSchemaValue

from camdkit.numeric_types import (MAX_INT_8, MAX_UINT_32, MAX_UINT_48,
                                   Rational, StrictlyPositiveRational)
from camdkit.timing_types import (Timecode,
                                  Timestamp,
                                  SynchronizationSource,
                                  SynchronizationOffsets,
                                  PTPProfile,
                                  SynchronizationPTP,
                                  Synchronization,
                                  Timing, SynchronizationPTPPriorities)


MAX_FRAME_RATE_FPS: Final[int] = 120

CLASSIC_TIMING_SCHEMA_PATH = Path("src/test/resources/classic/subschemas/timing.json")
CLASSIC_TIMING_SCHEMA: JsonSchemaValue | None = None


def setUpModule():
    global CLASSIC_TIMING_SCHEMA
    with open(CLASSIC_TIMING_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_TIMING_SCHEMA = json.load(fp)


def tearDownModule():
    pass


class TimingTestCases(unittest.TestCase):


    def test_timecode(self):
        valid_frame_rate_num: Final[int] = 30
        valid_frame_rate_denom: Final[int] = 1
        valid_frame_rate: Final[StrictlyPositiveRational] = (
            StrictlyPositiveRational(valid_frame_rate_num,
                                     valid_frame_rate_denom))
        max_valid_frame_rate: Final[StrictlyPositiveRational] = (
            StrictlyPositiveRational(MAX_FRAME_RATE_FPS, 1))
        valid_sub_frame: Final[int] = 0
        valid_drop_frame: Final[bool] = False

        # test hours during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours="foo", minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0.0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=-1, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=24, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=0, seconds=0, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(0, tc.hours)

        # test minutes during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes="foo", seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0.0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=-1, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=60, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=59, seconds=0, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(59, tc.minutes)

        # test seconds during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds="foo", frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0.0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=-1, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=60, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame= valid_sub_frame, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=0, seconds=59, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(59, tc.seconds)

        # test frames during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames="foo",
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0.0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=-1,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=MAX_FRAME_RATE_FPS,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=0, seconds=0, frames=MAX_FRAME_RATE_FPS - 1,
                      frame_rate=max_valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(MAX_FRAME_RATE_FPS - 1, tc.frames)

        # test frame rates during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate="foo",
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=0.0,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=-1,
                     sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=0, seconds=0, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(valid_frame_rate, tc.frame_rate)

        # test sub-frames during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame="foo", dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=0.0, dropFrame=valid_drop_frame)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=-1, dropFrame=valid_drop_frame)
        tc = Timecode(hours=0, minutes=0, seconds=0, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(valid_sub_frame, tc.sub_frame)
        
        # test drop-frames during TC creation
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame="foo")
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=2)
        with self.assertRaises(ValidationError):
            Timecode(hours=0, minutes=0, seconds=0, frames=0,
                     frame_rate=valid_frame_rate,
                     sub_frame=valid_sub_frame, dropFrame=-1)
        tc = Timecode(hours=0, minutes=0, seconds=0, frames=0,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        self.assertEqual(valid_drop_frame, tc.dropFrame)

        valid_hours: int = 1
        valid_minutes: int = 2
        valid_seconds: int =  3
        valid_frames: int = 4
        tc = Timecode(hours=valid_hours, minutes=valid_minutes, seconds=valid_seconds, frames=valid_frames,
                      frame_rate=valid_frame_rate,
                      sub_frame=valid_sub_frame, dropFrame=valid_drop_frame)
        # test assigning value of hours field
        with self.assertRaises(ValidationError):
            tc.hours = "foo"
        with self.assertRaises(ValidationError):
            tc.hours = 0.0
        with self.assertRaises(ValidationError):
            tc.hours = -1
        with self.assertRaises(ValidationError):
            tc.hours = 24
        # test assigning value of minutes field
        with self.assertRaises(ValidationError):
            tc.minutes = "foo"
        with self.assertRaises(ValidationError):
            tc.minutes = 0.0
        with self.assertRaises(ValidationError):
            tc.minutes = -1
        with self.assertRaises(ValidationError):
            tc.minutes = 60
        # test assigning value of seconds field
        with self.assertRaises(ValidationError):
            tc.seconds = "foo"
        with self.assertRaises(ValidationError):
            tc.seconds = 0.0
        with self.assertRaises(ValidationError):
            tc.seconds = -1
        with self.assertRaises(ValidationError):
            tc.seconds = 60
        # test assigning value of frames field
        with self.assertRaises(ValidationError):
            tc.frames = "foo"
        with self.assertRaises(ValidationError):
            tc.frames = 0.0
        with self.assertRaises(ValidationError):
            tc.frames = -1
        with self.assertRaises(ValidationError):
            tc.frames = MAX_FRAME_RATE_FPS

        # test assigning value of frame rate
        with self.assertRaises(ValidationError):
            tc.frame_rate = "foo"
        with self.assertRaises(ValidationError):
            tc.frame_rate = 0.0
        with self.assertRaises(ValidationError):
            tc.frame_rate = -1
        with self.assertRaises(ValidationError):
            tc.frame_rate = Rational(-4,1)

        # test assigning value of sub_frame
        with self.assertRaises(ValidationError):
            tc.sub_frame = "foo"
        with self.assertRaises(ValidationError):
            tc.sub_frame = 0.0
        with self.assertRaises(ValidationError):
            tc.sub_frame = -1
        with self.assertRaises(ValidationError):
            tc.sub_frame = Rational(-4, 1)

        # test assigning value of dropFrame
        with self.assertRaises(ValidationError):
            tc.dropFrame = "foo"
        with self.assertRaises(ValidationError):
            tc.dropFrame = 2
        with self.assertRaises(ValidationError):
            tc.dropFrame = -1
        with self.assertRaises(ValidationError):
            tc.dropFrame = Rational(-4, 1)

        doubled_hours: Final[int] = valid_hours * 2
        doubled_minutes: Final[int] = valid_minutes * 2
        doubled_seconds: Final[int] = valid_seconds * 2
        doubled_frames: Final[int] = valid_frames * 2
        doubled_frame_rate: Final[StrictlyPositiveRational] = StrictlyPositiveRational(
            2 * valid_frame_rate_num, valid_frame_rate_denom)
        doubled_sub_frame: Final[int] = 2
        doubled_drop_frame: Final[bool] = True
        tc.hours = doubled_hours
        self.assertEqual(tc.hours, doubled_hours)
        tc.minutes = doubled_minutes
        self.assertEqual(tc.minutes, doubled_minutes)
        tc.seconds = doubled_seconds
        self.assertEqual(tc.seconds, doubled_seconds)
        tc.frames = doubled_frames
        self.assertEqual(tc.frames, doubled_frames)
        tc.frame_rate = doubled_frame_rate
        self.assertEqual(tc.frame_rate, doubled_frame_rate)
        tc.sub_frame = doubled_sub_frame
        self.assertEqual(tc.sub_frame, doubled_sub_frame)
        tc.dropFrame = doubled_drop_frame
        self.assertEqual(tc.dropFrame, doubled_drop_frame)

        timecode_as_json = Timecode.to_json(tc)
        self.assertEqual(timecode_as_json["hours"], doubled_hours)
        self.assertEqual(timecode_as_json["minutes"], doubled_minutes)
        self.assertEqual(timecode_as_json["seconds"], doubled_seconds)
        self.assertEqual(timecode_as_json["frames"], doubled_frames)
        self.assertEqual(timecode_as_json["frameRate"],
                         StrictlyPositiveRational.to_json(doubled_frame_rate))
        self.assertEqual(timecode_as_json["subFrame"], doubled_sub_frame)
        self.assertEqual(timecode_as_json["dropFrame"], doubled_drop_frame)

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
        valid_profile = PTPProfile.SMPTE_2059_2_2021
        valid_domain: int = 1
        valid_leader_identity: str = "00:11:22:33:44:55"
        valid_leader_priorities = SynchronizationPTPPriorities(1, 2)
        valid_leader_accuracy = 0.1
        valid_mean_path_delay = 0.001
        valid_vlan = 50
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile="foo",
                               domain=valid_domain,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain="foo",
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=min_valid_domain - 1,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=max_valid_domain + 1,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=valid_domain,
                               leader_identity=0.0,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=valid_domain,
                               leader_identity=valid_leader_identity,
                               leader_priorities="foo",
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=valid_domain,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy="foo",
                               mean_path_delay=valid_mean_path_delay,
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=valid_domain,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay="foo",
                               vlan=valid_vlan)
        with self.assertRaises(ValidationError):
            SynchronizationPTP(profile=valid_profile,
                               domain=valid_domain,
                               leader_identity=valid_leader_identity,
                               leader_priorities=valid_leader_priorities,
                               leader_accuracy=valid_leader_accuracy,
                               mean_path_delay=valid_mean_path_delay,
                               vlan="foo")
        valid_ptp = SynchronizationPTP(profile=valid_profile,
                                       domain=valid_domain,
                                       leader_identity=valid_leader_identity,
                                       leader_priorities=valid_leader_priorities,
                                       leader_accuracy=valid_leader_accuracy,
                                       mean_path_delay=valid_mean_path_delay,
                                       vlan=valid_vlan)

        updated_domain: int = valid_domain * 2
        updated_leader: str = "00:11:22:33:44:56"
        valid_ptp.domain = updated_domain
        self.assertEqual(updated_domain, valid_ptp.domain)
        valid_ptp.leader_identity = updated_leader
        self.assertEqual(updated_leader, valid_ptp.leader_identity)
        with self.assertRaises(ValidationError):
            valid_ptp.domain = "foo"
        with self.assertRaises(ValidationError):
            valid_ptp.leader_identity = 0.0
        with self.assertRaises(ValidationError):
            valid_ptp.offset = "foo"

        ptp_as_json = SynchronizationPTP.to_json(valid_ptp)
        self.assertEqual(ptp_as_json["domain"], updated_domain)
        self.assertEqual(ptp_as_json["leaderIdentity"], updated_leader)

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
        valid_profile=PTPProfile.SMPTE_2059_2_2021
        valid_ptp_domain: int = 1
        valid_ptp_leader_identity: str = "00:11:22:33:44:55"
        valid_ptp_leader_priorities = SynchronizationPTPPriorities(1, 2)
        valid_leader_accuracy: float = 0.1
        valid_mean_path_delay: float = 0.001
        valid_ptp = SynchronizationPTP(profile=valid_profile,
                                       domain=valid_ptp_domain,
                                       leader_identity=valid_ptp_leader_identity,
                                       leader_priorities=valid_ptp_leader_priorities,
                                       leader_accuracy=valid_leader_accuracy,
                                       mean_path_delay=valid_mean_path_delay)
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
        updated_ptp = SynchronizationPTP(profile=PTPProfile.SMPTE_2059_2_2021,
                                         domain=1,
                                         leader_identity="00:11:22:33:44:55",
                                         leader_priorities=SynchronizationPTPPriorities(128, 128),
                                         leader_accuracy=0.1,
                                         mean_path_delay=0.01)
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
