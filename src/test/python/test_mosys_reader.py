#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

import unittest

from camdkit.trackerkit.mosys import reader
from camdkit.trackerkit.model import Vector3

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    frames = reader.to_frames("src/test/resources/trackerkit/mosys/A003_C001_01 15-03-47-01.f4")

    # Test parameters against known values across multple frames
    self.assertEqual(frames[0].transform.translation, Vector3(x=-8.045, y=-185.355, z=119.801))
    self.assertEqual(frames[1].transform.rotation, Vector3(x=-3.001, y=-28.062, z=3.076))
    # TODO JU Test more parameters when supported
