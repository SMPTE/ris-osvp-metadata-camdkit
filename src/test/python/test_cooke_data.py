#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Cooke lens reader tests"'''

import unittest

import camdkit.red.cooke

_COOKE_METADATA = bytes(map(lambda i: int(i, 16), "64/40/40/46/68/48/70/B8/80/40/40/40/42/66/6D/40/40/46/5E/40/40/46/73/45/4E/41/7F/40/40/53/47/35/33/35/39/39/37/36/34/0A/0D".split("/")))

class CookeDataTest(unittest.TestCase):

  def test_entrance_pupil_position(self):
    c = camdkit.red.cooke.lens_data_from_binary_string(_COOKE_METADATA)

    self.assertEqual(c.entrance_pupil_position, 127)

  def test__position(self):
    c = camdkit.red.cooke.lens_data_from_binary_string(_COOKE_METADATA)

    self.assertEqual(c.aperture_value, 560)
