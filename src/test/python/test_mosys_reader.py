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
    frame = reader.to_frame("src/test/resources/mosys/A003_C001_01 15-03-47-01.f4")

    # TODO for now
    self.assertEqual(frame.transform.translation, Vector3(x=0, y=0, z=0))
    self.assertEqual(frame.transform.rotation, Vector3(x=0, y=0, z=0))
