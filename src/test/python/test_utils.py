#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Utilities test'''

import unittest
from fractions import Fraction 

import camdkit.utils as utils

class UtilitiesTest(unittest.TestCase):

  def test_guess_fps(self):

    self.assertEqual(24, utils.guess_fps(24))

    self.assertEqual(Fraction(24, 1), utils.guess_fps(Fraction(24, 1)))

    self.assertEqual(Fraction(24000, 1001), utils.guess_fps(Fraction(24000, 1001)))

    self.assertEqual(Fraction(24000, 1001), utils.guess_fps(float(Fraction(24000, 1001))))

    self.assertEqual(Fraction(30000, 1001), utils.guess_fps(float(Fraction(30000, 1001))))

    self.assertEqual(Fraction(60000, 1001), utils.guess_fps(float(Fraction(60000, 1001))))

    self.assertEqual(Fraction(24000, 1001), utils.guess_fps(23.98))

    self.assertEqual(Fraction(30000, 1001), utils.guess_fps(29.97))

    self.assertEqual(Fraction(60000, 1001), utils.guess_fps(59.94))
