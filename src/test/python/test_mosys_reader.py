#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

import unittest
import uuid

from camdkit.framework import Vector3, Rotator3, Synchronization, SynchronizationSourceEnum, \
                              Timecode, TimecodeFormat, FizEncoders, Distortion, PerspectiveShift
from camdkit.model import OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION
from camdkit.mosys import reader

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    clip = reader.to_clip("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4", 20)

    # Test parameters against known values across multple frames
    self.assertEqual(clip.protocol[0].name, OPENTRACKIO_PROTOCOL_NAME)
    self.assertEqual(clip.protocol[0].version, OPENTRACKIO_PROTOCOL_VERSION)
    self.assertEqual(len(clip.sample_id[1]), len(uuid.uuid4().urn))
    self.assertEqual(clip.device_recording[2], True)
    self.assertEqual(clip.device_status[3], "Optical Good")
    self.assertEqual(clip.timing_frame_rate[4], 25.0)
    self.assertEqual(clip.timing_mode[5], "internal")
    self.assertEqual(clip.timing_sequence_number[6], 13)
    self.assertEqual(clip.timing_synchronization[7],
                     Synchronization(frequency=25, locked=True, source=SynchronizationSourceEnum.GENLOCK, ptp=None, present=True))
    self.assertEqual(str(clip.timing_timecode[8]), str(Timecode(15,3,47,10,TimecodeFormat(25))))
    self.assertEqual(clip.transforms[9][0].translation, Vector3(x=-8.121, y=-185.368, z=119.806))
    self.assertEqual(clip.transforms[10][0].rotation, Rotator3(pan=-2.969, tilt=-28.03, roll=3.1))
    self.assertEqual(clip.lens_encoders[11], FizEncoders(focus=0.7643280029296875, zoom=0.0014190673828125))
    self.assertEqual(clip.lens_distortion[12], Distortion([0.15680991113185883, -0.0881580114364624]))
    self.assertEqual(clip.lens_perspective_shift[13], PerspectiveShift(-7.783590793609619, 6.896144866943359))
    self.assertAlmostEqual(clip.lens_focal_length[14], 22.35, 2)
    self.assertEqual(clip.lens_focus_distance[15], 2313)
