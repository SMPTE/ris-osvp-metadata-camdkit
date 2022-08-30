#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2022, Sandflow Consulting LLC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
