#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) Society of Motion Picture and Television Engineers
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

'''RED camera reader tests'''

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