#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

import unittest

from camdkit.framework import Vector3, Rotator3
from camdkit.mosys import reader

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    clip = reader.to_clip("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4", 100)

    # Test parameters against known values across multple frames
    self.assertEqual(clip.transforms[0][0].translation, Vector3(x=-8.045, y=-185.355, z=119.801))
    self.assertEqual(clip.transforms[1][0].rotation, Rotator3(pan=-3.001, tilt=-28.062, roll=3.076))
    # TODO JU Test more parameters when supported
