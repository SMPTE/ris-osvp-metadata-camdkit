#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Framework tests'''

import unittest
from fractions import Fraction

import camdkit.framework as framework

class RationalTest(unittest.TestCase):

  def test_limits(self):
    self.assertTrue(framework.RationalParameter.validate(Fraction(2147483647, 4294967295)))
    self.assertTrue(framework.RationalParameter.validate(Fraction(-2147483648, 1)))

    self.assertFalse(framework.RationalParameter.validate(Fraction(-2147483649, 1)))
    self.assertFalse(framework.RationalParameter.validate(Fraction(2147483648, 1)))
    self.assertFalse(framework.RationalParameter.validate(Fraction(1, 4294967296)))

  def test_from_dict(self):
    r = framework.RationalParameter.from_json({
      "num": 1,
      "denom": 2
    })

    self.assertEqual(r, Fraction(1,2))

  def test_to_dict(self):
    j = framework.RationalParameter.to_json(Fraction(1,2))

    self.assertDictEqual(j, { "num": 1, "denom": 2 })

class StrictlyPositiveRationalTest(unittest.TestCase):

  def test_limits(self):
    self.assertTrue(framework.StrictlyPositiveRationalParameter.validate(Fraction(2147483647, 4294967295)))
    self.assertTrue(framework.StrictlyPositiveRationalParameter.validate(Fraction(0, 1)))

    self.assertFalse(framework.StrictlyPositiveRationalParameter.validate(Fraction(-1, 1)))
    self.assertFalse(framework.StrictlyPositiveRationalParameter.validate(Fraction(2147483648, 1)))
    self.assertFalse(framework.StrictlyPositiveRationalParameter.validate(Fraction(1, 4294967296)))

  def test_from_dict(self):
    r = framework.StrictlyPositiveRationalParameter.from_json({
      "num": 1,
      "denom": 2
    })

    self.assertEqual(r, Fraction(1,2))

  def test_to_dict(self):
    j = framework.StrictlyPositiveRationalParameter.to_json(Fraction(1,2))

    self.assertDictEqual(j, { "num": 1, "denom": 2 })
    
class EnumParameterTest(unittest.TestCase):

  def test_allowed_values(self):
    param = framework.TimingModeParameter()
    self.assertTrue(param.validate("internal"))
    self.assertTrue(param.validate("external"))
    self.assertFalse(param.validate(""))
    self.assertFalse(param.validate("a"))
    self.assertFalse(param.validate(None))
    self.assertFalse(param.validate(0))
    

class TransformsTest(unittest.TestCase):

  def test_to_dict(self):
    j = framework.TransformsParameter.to_json((framework.Transform(
      translation=framework.Vector3(1,2,3), \
      rotation=framework.Rotator3(1,2,3)), ))
    self.assertListEqual(j, [{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 } 
    }])
    j = framework.TransformsParameter.to_json((framework.Transform(
      translation=framework.Vector3(1,2,3),
      rotation=framework.Rotator3(1,2,3),
      scale=framework.Vector3(1,2,3)), ))
    self.assertListEqual(j, [{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    }])
  
  def test_from_dict(self):
    t = framework.TransformsParameter.from_json([{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 }
    }])
    self.assertDictEqual(t[0].translation, { "x": 1, "y": 2, "z": 3 })
    self.assertDictEqual(t[0].rotation, { "pan": 1, "tilt": 2, "roll": 3 })
    t = framework.TransformsParameter.from_json([{
      "translation": { "x": 1, "y": 2, "z": 3 },
      "rotation": { "pan": 1, "tilt": 2, "roll": 3 },
      "scale": { "x": 1, "y": 2, "z": 3 }
    }])
    self.assertDictEqual(t[0].translation, { "x": 1, "y": 2, "z": 3 })
    self.assertDictEqual(t[0].rotation, { "pan": 1, "tilt": 2, "roll": 3 })
    self.assertDictEqual(t[0].scale, { "x": 1, "y": 2, "z": 3 })
