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
    self.assertTrue(param.validate(framework.TimingMode.INTERNAL))
    self.assertTrue(param.validate(framework.TimingMode.EXTERNAL))
    self.assertFalse(param.validate(""))
    self.assertFalse(param.validate("a"))
    self.assertFalse(param.validate(None))
    self.assertFalse(param.validate(0))
    
class TimecodeTest(unittest.TestCase):

  def test_timecode_format(self):
    self.assertEqual(framework.TimecodeFormat.to_int(framework.TimecodeFormat.TC_24), 24)
    self.assertEqual(framework.TimecodeFormat.to_int(framework.TimecodeFormat.TC_24D), 24)
    self.assertEqual(framework.TimecodeFormat.to_int(framework.TimecodeFormat.TC_25), 25)
    self.assertEqual(framework.TimecodeFormat.to_int(framework.TimecodeFormat.TC_30), 30)
    self.assertEqual(framework.TimecodeFormat.to_int(framework.TimecodeFormat.TC_30D), 30)
    with self.assertRaises(TypeError):
      framework.TimecodeFormat.to_int()
    with self.assertRaises(ValueError):
      framework.TimecodeFormat.to_int(0)
      framework.TimecodeFormat.to_int(24)

  def test_timecode_formats(self):
    with self.assertRaises(TypeError):
      framework.TimecodeParameter.validate(framework.Timecode())
      framework.TimecodeParameter.validate(framework.Timecode(1,2,3))
      framework.TimecodeParameter.validate(framework.Timecode(0,0,0,0))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(0,0,0,0,0)))
    self.assertTrue(framework.TimecodeParameter.validate(framework.Timecode(0,0,0,0,framework.TimecodeFormat.TC_24)))
    self.assertTrue(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,4,framework.TimecodeFormat.TC_24)))
    self.assertTrue(framework.TimecodeParameter.validate(framework.Timecode(23,59,59,23,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(-1,2,3,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(24,2,3,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,-1,3,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,60,3,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,-1,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,60,4,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,-1,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,24,framework.TimecodeFormat.TC_24)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,24,framework.TimecodeFormat.TC_24D)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,25,framework.TimecodeFormat.TC_25)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,30,framework.TimecodeFormat.TC_30)))
    self.assertFalse(framework.TimecodeParameter.validate(framework.Timecode(1,2,3,30,framework.TimecodeFormat.TC_30D)))

  def test_from_dict(self):
    r = framework.TimecodeParameter.from_json({
      "hour": 1,
      "minute": 2,
      "second": 3,
      "frame": 4,
      "format": framework.TimecodeFormat.TC_24
    })
    self.assertEqual(r, framework.Timecode(1,2,3,4,framework.TimecodeFormat.TC_24))

  def test_to_dict(self):
    j = framework.TimecodeParameter.to_json(framework.Timecode(1,2,3,4,framework.TimecodeFormat.TC_24))
    self.assertDictEqual(j, {
      "hour": 1,
      "minute": 2,
      "second": 3,
      "frame": 4,
      "format": str(framework.TimecodeFormat.TC_24)
    })


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
