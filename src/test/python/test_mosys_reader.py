#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys tracking data reader tests'''

from fractions import Fraction
import unittest

import camdkit.trackerkit.mosys.reader
import camdkit.trackerkit.model

class MoSysReaderTest(unittest.TestCase):
  
  def test_reader(self):
    frame = camdkit.trackerkit.mosys.reader.to_frame("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4")

    # TODO for now
    self.assertEqual(frame.translation, camdkit.trackerkit.model.Vector3(x=0, y=0, z=0))
