#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for numeric types"""

import sys
import unittest
from fractions import Fraction

from pydantic import ValidationError

from camdkit.compatibility import CompatibleBaseModel
from camdkit.numeric_types import (MAX_INT_8, MIN_INT_32,
                                   MAX_UINT_32, MAX_UINT_48, MAX_INT_32,
                                   NonNegative8BitInt,
                                   NonNegativeInt,
                                   NonNegative48BitInt,
                                   StrictlyPositiveInt,
                                   NonNegativeFloat, StrictlyPositiveFloat, NormalizedFloat,
                                   UnityOrGreaterFloat,
                                   Rational, StrictlyPositiveRational)


class NumericsTestCases(unittest.TestCase):

    def test_non_negative_8bit_int(self):
        class NonNegative8BitIntTestbed(CompatibleBaseModel):
            value: NonNegative8BitInt
        x = NonNegative8BitIntTestbed(value=0)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1
        with self.assertRaises(ValidationError):
            x.value = 0.0
        x.value = 0
        self.assertEqual(0, x.value)
        x.value = 1
        self.assertEqual(1, x.value)
        x.value = MAX_INT_8
        self.assertEqual(MAX_INT_8, x.value)
        with self.assertRaises(ValidationError):
            x.value = MAX_INT_8 + 1
        expected_schema = {
            "type": "integer",
            "minimum": 0,
            "maximum": MAX_INT_8,
        }
        entire_schema = NonNegative8BitIntTestbed.make_json_schema()
        non_negative_8bit_int_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, non_negative_8bit_int_schema)

    def test_non_negative_int(self):
        class NonNegativeIntTestbed(CompatibleBaseModel):
            value: NonNegativeInt
        x = NonNegativeIntTestbed(value=0)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1
        with self.assertRaises(ValidationError):
            x.value = 0.0
        x.value = 0
        self.assertEqual(0, x.value)
        x.value = 1
        self.assertEqual(1, x.value)
        x.value = MAX_UINT_32
        self.assertEqual(MAX_UINT_32, x.value)
        with self.assertRaises(ValidationError):
            x.value = MAX_UINT_32 + 1
        expected_schema = {
            "type": "integer",
            "minimum": 0,
            "maximum": MAX_UINT_32,
        }
        entire_schema = NonNegativeIntTestbed.make_json_schema()
        non_negative_int_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, non_negative_int_schema)

    def test_non_negative_48bit_int(self):
        class NonNegative48BitIntTestbed(CompatibleBaseModel):
            value: NonNegative48BitInt

        x = NonNegative48BitIntTestbed(value=0)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1
        with self.assertRaises(ValidationError):
            x.value = 0.0
        x.value = 0
        self.assertEqual(0, x.value)
        x.value = 1
        self.assertEqual(1, x.value)
        x.value = MAX_UINT_48
        self.assertEqual(MAX_UINT_48, x.value)
        with self.assertRaises(ValidationError):
            x.value = MAX_UINT_48 + 1
        expected_schema = {
            "type": "integer",
            "minimum": 0,
            "maximum": MAX_UINT_48,
        }
        entire_schema = NonNegative48BitIntTestbed.make_json_schema()
        non_negative_int_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, non_negative_int_schema)

    def test_strictly_positive_int(self):
        class StrictlyPositiveIntTestbed(CompatibleBaseModel):
            value: StrictlyPositiveInt
        x = StrictlyPositiveIntTestbed(value=1)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1
        with self.assertRaises(ValidationError):
            x.value = 0
        with self.assertRaises(ValidationError):
            x.value = 0.0
        x.value = 1
        self.assertEqual(1, x.value)
        x.value = MAX_UINT_32
        self.assertEqual(MAX_UINT_32, x.value)
        with self.assertRaises(ValidationError):
            x.value = MAX_UINT_32 + 1
        expected_schema = {
            "type": "integer",
            "minimum": 1,
            "maximum": MAX_UINT_32
        }
        entire_schema = StrictlyPositiveIntTestbed.make_json_schema()
        strictly_positive_int_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, strictly_positive_int_schema)

    def test_non_negative_float(self):
        class NonNegativeFloatTestbed(CompatibleBaseModel):
            value: NonNegativeFloat
        x = NonNegativeFloatTestbed(value=0)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1.0
        with self.assertRaises(ValidationError):
            x.value = -sys.float_info.epsilon
        x.value = 0.0
        self.assertEqual(0.0, x.value)
        x.value = sys.float_info.epsilon
        self.assertEqual(sys.float_info.epsilon, x.value)
        x.value = 1.0
        self.assertEqual(1, x.value)
        x.value = sys.float_info.max
        self.assertEqual(sys.float_info.max, x.value)
        expected_schema = {
            "type": "number",
            "minimum": 0.0,
        }
        entire_schema = NonNegativeFloatTestbed.make_json_schema()
        non_negative_float_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, non_negative_float_schema)

    def test_strictly_positive_float(self):
        class StrictlyPositiveFloatTestbed(CompatibleBaseModel):
            value: StrictlyPositiveFloat
        x = StrictlyPositiveFloatTestbed(value=sys.float_info.epsilon)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1.0
        with self.assertRaises(ValidationError):
            x.value = -sys.float_info.epsilon
        with self.assertRaises(ValidationError):
            x.value = 0.0
        x.value = sys.float_info.epsilon
        self.assertEqual(sys.float_info.epsilon, x.value)
        x.value = 1.0
        self.assertEqual(1, x.value)
        x.value = sys.float_info.max
        self.assertEqual(sys.float_info.max, x.value)
        expected_schema = {
            "type": "number",
            "exclusiveMinimum": 0.0,
        }
        entire_schema = StrictlyPositiveFloatTestbed.make_json_schema()
        strictly_positive_float_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, strictly_positive_float_schema)

    def test_normalized_float(self):
        class NormalizedFloatTestbed(CompatibleBaseModel):
            value: NormalizedFloat
        valid_value: float = 0.5
        x = NormalizedFloatTestbed(value=sys.float_info.epsilon)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -0.5
        with self.assertRaises(ValidationError):
            x.value = 0.0 - sys.float_info.epsilon
        x.value = 0.0
        self.assertEqual(0.0, x.value)
        x.value = 0.0 + sys.float_info.epsilon
        self.assertEqual(0.0 + sys.float_info.epsilon, x.value)
        x.value = 0.5
        self.assertEqual(0.5, x.value)
        x.value = 1.0 - sys.float_info.epsilon
        self.assertEqual(1.0 - sys.float_info.epsilon, x.value)
        x.value = 1.0
        self.assertEqual(1.0, x.value)
        with self.assertRaises(ValidationError):
            x.value = 1.0 + sys.float_info.epsilon
        with self.assertRaises(ValidationError):
            x.value = 1.5
        expected_schema = {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
        }
        entire_schema = NormalizedFloatTestbed.make_json_schema()
        strictly_positive_float_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, strictly_positive_float_schema)

    def test_unity_or_greater_float(self):
        class UnityOrGreaterFloatTestbed(CompatibleBaseModel):
            value: UnityOrGreaterFloat
        x = UnityOrGreaterFloatTestbed(value=1.0)
        with self.assertRaises(ValidationError):
            x.value = 'foo'
        with self.assertRaises(ValidationError):
            x.value = -1.0
        with self.assertRaises(ValidationError):
            x.value = -sys.float_info.epsilon
        with self.assertRaises(ValidationError):
            x.value = 0.0
        with self.assertRaises(ValidationError):
            x.value = sys.float_info.epsilon
        with self.assertRaises(ValidationError):
            x.value = 1.0 - sys.float_info.epsilon
        x.value = 1.0
        self.assertEqual(1, x.value)
        expected_schema = {
            "type": "number",
            "minimum": 1.0,
        }
        entire_schema = UnityOrGreaterFloatTestbed.make_json_schema()
        unity_or_greater_float_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, unity_or_greater_float_schema)

    def test_rational(self):
        with self.assertRaises(ValidationError):
            Rational(MIN_INT_32 - 1, 1)
        Rational(MIN_INT_32, 1)
        Rational(0, 1)
        Rational(MAX_INT_32, 1)
        with self.assertRaises(ValidationError):
            Rational(MAX_INT_32 + 1, 1)
        with self.assertRaises(ValidationError):
            Rational(0, MAX_UINT_32+1)
        with self.assertRaises(ValidationError):
            Rational(0, -1)
        with self.assertRaises(ValidationError):
            Rational(0, 0)
        Rational(1, 1)
        Rational(0, MAX_UINT_32)
        with self.assertRaises(ValidationError):
            Rational(0, MAX_UINT_32 +1)
        with self.assertRaises(ValidationError):
            Rational(1, MAX_UINT_32 + 1)
        Rational(MAX_INT_32, MAX_UINT_32)
        half_as_json = {"num": 1, "denom": 2}
        half_from_json = Rational.from_json(half_as_json)
        self.assertEqual(half_from_json, Rational(1, 2))
        half_as_rational = Rational(1, 2)
        json_from_half = Rational.to_json(half_as_rational)
        self.assertEqual({"num": 1, "denom": 2}, json_from_half)
        expected_schema = {
            "type": "object",
            "properties": {
                "num" : {
                    "type": "integer",
                    "minimum": MIN_INT_32,
                    "maximum": MAX_INT_32
                },
                "denom" : {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_UINT_32
                }
            },
            "required": ["num", "denom" ],
            "additionalProperties": False
        }
        schema = Rational.make_json_schema()
        self.assertDictEqual(expected_schema, schema)

    def test_strictly_positive_rational(self):
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(MIN_INT_32 - 1, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(MIN_INT_32, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(-1, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(0, 1)
        StrictlyPositiveRational(1, 1)
        StrictlyPositiveRational(MAX_INT_32, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(MAX_INT_32 + 1, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(0, 1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(1, MAX_UINT_32+1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(1, -1)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(1, 0)
        StrictlyPositiveRational(1, 1)
        StrictlyPositiveRational(1, MAX_UINT_32)
        with self.assertRaises(ValidationError):
            StrictlyPositiveRational(1, MAX_UINT_32 +1)
        StrictlyPositiveRational(MAX_INT_32, MAX_UINT_32)
        half_as_json = {"num": 1, "denom": 2}
        half_from_json = StrictlyPositiveRational.from_json(half_as_json)
        self.assertEqual(half_from_json, StrictlyPositiveRational(1, 2))
        half_as_strictly_positive_rational = StrictlyPositiveRational(1, 2)
        json_from_half = Rational.to_json(half_as_strictly_positive_rational)
        self.assertEqual({"num": 1, "denom": 2}, json_from_half)
        # TODO file Issue: existing implementation has StrictlyPositiveRational that allows 0/N
        expected_schema = {
            "type": "object",
            "properties": {
                "num" : {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_INT_32
                },
                "denom" : {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_UINT_32
                }
            },
            "required": ["num", "denom" ],
            "additionalProperties": False
        }
        schema = StrictlyPositiveRational.make_json_schema()
        self.assertDictEqual(expected_schema, schema)


if __name__ == '__main__':
    unittest.main()
