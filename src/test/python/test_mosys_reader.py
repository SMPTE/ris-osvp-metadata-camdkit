#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

import unittest
import uuid

from camdkit.framework import (Vector3, Rotator3,
                               Synchronization, SynchronizationSourceEnum,
                               Timecode, StrictlyPositiveRational,
                               FizEncoders, Distortion, ProjectionOffset)
from camdkit.model import OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION
from camdkit.mosys import reader
from camdkit.mosys.f4 import F4PacketParser

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    clip = reader.to_clip("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4", 20)

    # Frame count contract: to_clip(f, n) must return exactly n frames (not n+1)
    self.assertEqual(len(clip.sample_id), 20)

    # Test parameters against known values across multiple frames
    self.assertEqual(clip.protocol[0].name, OPENTRACKIO_PROTOCOL_NAME)
    self.assertEqual(clip.protocol[0].version, OPENTRACKIO_PROTOCOL_VERSION)
    self.assertEqual(len(clip.sample_id[1]), len(uuid.uuid4().urn))
    self.assertEqual(clip.tracker_recording[2], True)
    self.assertEqual(clip.tracker_status[3], "Optical Good")
    self.assertEqual(clip.timing_sample_rate[4], 25.0)
    self.assertEqual(clip.timing_mode[5], "internal")
    self.assertEqual(clip.timing_sequence_number[6], 13)
    self.assertEqual(clip.timing_synchronization[7],
                     Synchronization(frequency=25, locked=True, source=SynchronizationSourceEnum.GENLOCK, ptp=None, present=True))
    self.assertEqual(str(clip.timing_timecode[8]),
                     str(Timecode(hours=15, minutes=3, seconds=47, frames=10,
                                  frame_rate=StrictlyPositiveRational(25,1),
                                  sub_frame=0, dropFrame=False)))
    self.assertEqual(clip.transforms[9][0].translation, Vector3(x=-8.121, y=-185.368, z=119.806))
    self.assertEqual(clip.transforms[10][0].rotation, Rotator3(pan=-2.969, tilt=-28.03, roll=3.1))
    self.assertEqual(clip.lens_encoders[11], FizEncoders(focus=0.7643280029296875, zoom=0.0014190673828125))
    self.assertEqual(clip.lens_distortions[12], (Distortion(radial=(0.15680991113185883, -0.0881580114364624)),))
    self.assertEqual(clip.lens_projection_offset[13], ProjectionOffset(-7.783590793609619, 6.896144866943359))
    self.assertAlmostEqual(clip.lens_pinhole_focal_length[14], 22.35, 2)
    self.assertEqual(int(clip.lens_focus_distance[15]*1000), 2313)


class MoSysF4ParserUnitTest(unittest.TestCase):

  # Minimal valid F4 packet: timecode (25fps) + focus encoder — no focal length axis.
  # Without the focal length axis, fov_h=0.0 and tan(0)=0 causes ZeroDivisionError.
  # Checksum = (0x40 - sum(header+body)) % 256 = 0xae.
  _PACKET_NO_FOCAL_LENGTH = bytes([
    0xf4, 0x01, 0x02, 0x00,         # command, camera_id=1, axis_count=2, status=0
    0xf8, 0x20, 0x00, 0x00, 0x00,   # timecode axis: 25fps, 00:00:00:00
    0x03, 0x00, 0x00, 0x80, 0x00,   # focus encoder axis: 50%
    0xae,                             # checksum
  ])

  def test_no_focal_length_axis_does_not_crash(self):
    """get_tracking_frame() must not raise when no focal length axis is present.

    fov_h defaults to 0.0. Without a guard, 36.0 / (2 * tan(0)) raises
    ZeroDivisionError. The parser must skip pinhole focal length computation
    and leave lens_pinhole_focal_length unset.
    """
    parser = F4PacketParser()
    self.assertTrue(parser.initialise(self._PACKET_NO_FOCAL_LENGTH))
    frame = parser.get_tracking_frame()
    self.assertIsNone(frame.lens_pinhole_focal_length)
