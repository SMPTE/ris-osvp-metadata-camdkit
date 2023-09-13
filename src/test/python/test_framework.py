#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Framework tests'''

import unittest
from fractions import Fraction
import json

import camdkit.framework as framework

class RetionalTest(unittest.TestCase):

  def test_limits(self):
    self.assertTrue(framework.RationalParameter.validate(Fraction(2147483647, 2147483647)))
    self.assertTrue(framework.RationalParameter.validate(Fraction(-2147483648, 1)))

    self.assertFalse(framework.RationalParameter.validate(Fraction(-2147483649, 1)))
    self.assertFalse(framework.RationalParameter.validate(Fraction(2147483648, 1)))
    self.assertFalse(framework.RationalParameter.validate(Fraction(1, 2147483648)))

  def test_from_dict(self):
    r = framework.RationalParameter.from_json({
      "num": 1,
      "denom": 2
    })

    self.assertEqual(r, Fraction(1,2))

  def test_to_dict(self):
    j = framework.RationalParameter.to_json(Fraction(1,2))

    self.assertDictEqual(j, { "num": 1, "denom": 2 })