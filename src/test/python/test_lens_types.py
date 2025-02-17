#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Tests for lens types"""

import unittest
import os
import sys
import json

from pathlib import Path

from typing import Any, Final

from pydantic import ValidationError
from pydantic.json_schema import JsonSchemaValue

from camdkit.compatibility import canonicalize_descriptions
from camdkit.lens_types import StaticLens, Distortion, Lens


CLASSIC_LENS_SCHEMA_PATH = Path("src/test/resources/classic/subschemas/lens.json")
CLASSIC_LENS_SCHEMA: JsonSchemaValue | None = None
CLASSIC_STATIC_LENS_SCHEMA_PATH = Path("src/test/resources/classic/subschemas/static_lens.json")
CLASSIC_STATIC_LENS_SCHEMA: JsonSchemaValue | None = None

def setUpModule():
    global CLASSIC_LENS_SCHEMA
    global CLASSIC_STATIC_LENS_SCHEMA
    with open(CLASSIC_LENS_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_LENS_SCHEMA = json.load(fp)
    with open(CLASSIC_STATIC_LENS_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_STATIC_LENS_SCHEMA = json.load(fp)


def tearDownModule():
    pass

class LensTypesTestCases(unittest.TestCase):

    # example of testing a struct:
    #   verify no-arg instantiation fails
    #   verify trying to instantiate with arguments of invalid type raises a validation error
    #   verify correct instantiation returns an object the attributes of which meet expectations
    #   verify one can set the object's attributes to new values
    #   when applicable, verify that trying to instantiate with arguments of the correct type
    #     but out-of-range or otherwise invalid values fail

    def test_nominal_focal_length(self):
        valid_nominal_focal_length: Final[float] = 1.0
        with self.assertRaises(ValidationError):
            StaticLens(nominal_focal_length="foo")
        with self.assertRaises(ValidationError):
            StaticLens(nominal_focal_length=0+1j)
        with self.assertRaises(ValidationError):
            StaticLens(nominal_focal_length=-1)
        with self.assertRaises(ValidationError):
            StaticLens(nominal_focal_length=0)
        static_lens = StaticLens(nominal_focal_length=sys.float_info.epsilon)
        self.assertEqual(sys.float_info.epsilon, static_lens.nominal_focal_length)
        static_lens.nominal_focal_length = valid_nominal_focal_length
        self.assertEqual(valid_nominal_focal_length, static_lens.nominal_focal_length)

    def test_f_number(self):
        valid_f_number: Final[tuple[float, ...]] = (1.0,)
        with self.assertRaises(ValidationError):
            Lens(f_number=("foo",))
        with self.assertRaises(ValidationError):
            Lens(f_number=(0 + 1j,))
        with self.assertRaises(ValidationError):
            Lens(f_number=(-1,))
        with self.assertRaises(ValidationError):
            Lens(f_number=(0,))
        static_lens = Lens(f_number=(sys.float_info.epsilon,))
        self.assertEqual((sys.float_info.epsilon,), static_lens.f_number)
        static_lens.f_number = valid_f_number
        self.assertEqual(valid_f_number, static_lens.f_number)

    def test_t_number(self):
        valid_t_number: Final[tuple[float, ...]] = (1.0,)
        with self.assertRaises(ValidationError):
            Lens(t_number=("foo",))
        with self.assertRaises(ValidationError):
            Lens(t_number=(0 + 1j,),)
        with self.assertRaises(ValidationError):
            Lens(t_number=(-1,))
        with self.assertRaises(ValidationError):
            Lens(t_number=(0,))
        static_lens = Lens(t_number=(sys.float_info.epsilon,))
        self.assertEqual((sys.float_info.epsilon,), static_lens.t_number)
        static_lens.t_number = valid_t_number
        self.assertEqual(valid_t_number, static_lens.t_number)

    def test_distortion(self):
        with self.assertRaises(ValidationError):
            Distortion()  # invalid: neither name nor data
        with self.assertRaises(ValidationError):
            Distortion(model="", radial=(1,))  # blank model
        with self.assertRaises(ValidationError):
            Distortion(radial=1.0)  # scalar radial datum
        with self.assertRaises(ValueError):
            Distortion(radial=tuple())  # empty radial tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=("foo",))  # non-numeric radial tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=(1+1j,))  # non-float radial tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=tuple())  # empty radial tuple
        Distortion(radial=(1.0,))
        Distortion(radial=(1.0, 2.0))
        with self.assertRaises(ValueError):
            Distortion(radial=(1.0,),
                       tangential=tuple())  # empty tangential tuple
        with self.assertRaises(ValueError):
            Distortion(radial=(1.0,),
                       tangential=1.0)  # scalar tangential datum
        with self.assertRaises(ValueError):
            Distortion(radial=(1.0,),
                       tangential=("foo",))  # non-numeric tangential tuple
        with self.assertRaises(ValueError):
            Distortion(radial=(1.0,),
                       tangential=(0+1j, 0+2j))  # non-float tangential tuple
        Distortion(radial=(1.0,), tangential=(1.0,))
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=1.0)  # scalar overscan datum
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=tuple())  # empty overscan tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=tuple("foo"))  # non-numeric overscan tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=(0+1j, 0+2j))  # non-float overscan tuple
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=(-0.1,))  # negative overscan
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=(0.0,))  # zero overscan
        with self.assertRaises(ValidationError):
            Distortion(radial=(1.0,),
                       tangential=(1.0,),
                       overscan=(1.0 - sys.float_info.epsilon,))  # zero overscan
        valid = Distortion(model="Brown-Conrady D-U",
                           radial=(1.0,),
                           tangential=(1.0,),
                           overscan=(1.0,))
        Distortion.validate(valid)
        expected_json: dict[str, Any] = {
            # default model is not serialized
            "radial": (1.0,),
            "tangential": (1.0,),
            "overscan": (1.0,)
        }
        json_from_instance: dict[str, Any] = Distortion.to_json(valid)
        self.assertDictEqual(expected_json, json_from_instance)
        instance_from_json: Distortion = Distortion.from_json(json_from_instance)
        self.assertEqual(valid, instance_from_json)

        full_expected_schema: JsonSchemaValue = CLASSIC_LENS_SCHEMA
        self.assertIn("properties", full_expected_schema)
        self.assertIn("distortion", full_expected_schema["properties"])
        expected_schema = full_expected_schema["properties"]["distortion"]
        full_actual_schema: JsonSchemaValue = Lens.make_json_schema()
        self.assertIn("properties", full_actual_schema)
        self.assertIn("distortion", full_actual_schema["properties"])
        actual_schema = full_actual_schema["properties"]["distortion"]
        self.assertEqual(expected_schema, actual_schema)

    def test_static_lens_schemas_match(self):
        expected: JsonSchemaValue = CLASSIC_STATIC_LENS_SCHEMA
        actual = StaticLens.make_json_schema()
        tmp_path = os.path.join(os.path.abspath(os.sep), "tmp")
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        with open(os.path.join(tmp_path, "sorted_expected_static_lens_schema.json"), "w") as ef:
            json.dump(expected, ef, indent=4, sort_keys=True)
        with open(os.path.join(tmp_path, "sorted_actual_static_lens_schema.json"), "w") as cf:
            json.dump(actual, cf, indent=4, sort_keys=True)
        self.assertDictEqual(expected, actual)

    def test_regular_lens_schemas_match(self):
        expected: JsonSchemaValue = CLASSIC_LENS_SCHEMA
        actual = Lens.make_json_schema()
        tmp_path = os.path.join(os.path.abspath(os.sep), "tmp")
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        with open(os.path.join(tmp_path, "sorted_expected_lens_schema.json"), "w") as ef:
            json.dump(expected, ef, indent=4, sort_keys=True)
        with open(os.path.join(tmp_path, "sorted_actual_lens_schema.json"), "w") as cf:
            json.dump(actual, cf, indent=4, sort_keys=True)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
