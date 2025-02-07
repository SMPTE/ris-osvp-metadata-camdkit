#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling of tracker-related metadata"""

import json
import unittest

from pathlib import Path

from pydantic import ValidationError
from pydantic.json_schema import JsonSchemaValue

from camdkit.clip import Clip
from camdkit.compatibility import canonicalize_descriptions
from camdkit.string_types import UUIDURN
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.units import DEGREE, METER


CLASSIC_TRANSFORM_SCHEMA_PATH = Path("src/test/resources/classic/subschemas/transforms.json")
CLASSIC_TRANSFORM_SCHEMA: JsonSchemaValue | None = None


def setUpModule():
    global CLASSIC_TRANSFORM_SCHEMA
    with open(CLASSIC_TRANSFORM_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_TRANSFORM_SCHEMA = json.load(fp)


def tearDownModule():
    pass


class TestTransformCases(unittest.TestCase):

    def test_vector3(self):
        orig_x: float = 2.0
        orig_y: float = 3.0
        orig_z: float = 4.0
        # verify validation when constructed
        with self.assertRaises(ValidationError):
            Vector3("foo", orig_y, orig_z)
        with self.assertRaises(ValidationError):
            Vector3(orig_x, "foo", orig_z)
        with self.assertRaises(ValidationError):
            Vector3(orig_x, orig_y, "foo")
        valid_v3 = Vector3(orig_x, orig_y, orig_z)
        # verify constructed values and accessors
        self.assertEqual(valid_v3.x, orig_x)
        self.assertEqual(valid_v3.y, orig_y)
        self.assertEqual(valid_v3.z, orig_z)
        # verify names of fields are as expected
        also_valid_v3 = Vector3(x=orig_x, y=orig_y, z=orig_z)
        self.assertEqual(also_valid_v3, valid_v3)
        # verify integers promote to floats as needed
        updated_x = 5
        updated_y = 6
        updated_z = 7
        valid_v3.x = updated_x
        valid_v3.y = updated_y
        valid_v3.z = updated_z
        self.assertEqual(valid_v3.x, float(updated_x))
        self.assertEqual(valid_v3.y, float(updated_y))
        self.assertEqual(valid_v3.z, float(updated_z))
        # verify that sort of thing doesn't go too far though
        with self.assertRaises(ValidationError):
            valid_v3.x = 8+0j
        # verify that JSON is constructed as expected
        valid_v3_as_json = Vector3.to_json(valid_v3)
        self.assertEqual(valid_v3_as_json["x"], float(updated_x))
        self.assertEqual(valid_v3_as_json["y"], float(updated_y))
        self.assertEqual(valid_v3_as_json["z"], float(updated_z))
        # verify that we can make a dupe of the original from the JSON
        valid_v3_from_json = Vector3.from_json(valid_v3_as_json)
        self.assertEqual(valid_v3, valid_v3_from_json)
        # verify that the JSON schema from Pydantic is what we think it is
        full_expected_schema: JsonSchemaValue = CLASSIC_TRANSFORM_SCHEMA
        self.assertIn("items", full_expected_schema)
        self.assertIn("properties", full_expected_schema["items"])
        self.assertIn("rotation", full_expected_schema["items"]["properties"])
        expected_schema = full_expected_schema["items"]["properties"]["translation"]
        actual_schema = Vector3.make_json_schema()
        # This is only required because we are testing outside the context in which
        # the Vector3 object will actually be used.
        actual_schema["units"] = METER
        self.assertEqual(expected_schema, actual_schema)

    def test_rotator3(self):
        orig_pan: float = 2.0
        orig_tilt: float = 3.0
        orig_roll: float = 4.0
        # verify validation when constructed
        with self.assertRaises(ValidationError):
            Rotator3("foo", orig_tilt, orig_roll)
        with self.assertRaises(ValidationError):
            Rotator3(orig_pan, "foo", orig_roll)
        with self.assertRaises(ValidationError):
            Rotator3(orig_pan, orig_tilt, "foo")
        valid_v3 = Rotator3(orig_pan, orig_tilt, orig_roll)
        # verify constructed values and accessors
        self.assertEqual(valid_v3.pan, orig_pan)
        self.assertEqual(valid_v3.tilt, orig_tilt)
        self.assertEqual(valid_v3.roll, orig_roll)
        # verify names of fields are as expected
        also_valid_v3 = Rotator3(pan=orig_pan, tilt=orig_tilt, roll=orig_roll)
        self.assertEqual(also_valid_v3, valid_v3)
        # verify integers promote to floats as needed
        updated_pan = 5
        updated_tilt = 6
        updated_roll = 7
        valid_v3.pan = updated_pan
        valid_v3.tilt = updated_tilt
        valid_v3.roll = updated_roll
        self.assertEqual(valid_v3.pan, float(updated_pan))
        self.assertEqual(valid_v3.tilt, float(updated_tilt))
        self.assertEqual(valid_v3.roll, float(updated_roll))
        # verify that sort of thing doesn't go too far though
        with self.assertRaises(ValidationError):
            valid_v3.pan = 8+0j
        # verify that JSON is constructed as expected
        valid_v3_as_json = Vector3.to_json(valid_v3)
        self.assertEqual(valid_v3_as_json["pan"], float(updated_pan))
        self.assertEqual(valid_v3_as_json["tilt"], float(updated_tilt))
        self.assertEqual(valid_v3_as_json["roll"], float(updated_roll))
        # verify that we can make a dupe of the original from the JSON
        valid_v3_from_json = Rotator3.from_json(valid_v3_as_json)
        self.assertEqual(valid_v3, valid_v3_from_json)
        # verify that the JSON schema from Pydantic is what we think it is
        full_expected_schema: JsonSchemaValue = CLASSIC_TRANSFORM_SCHEMA
        self.assertIn("items", full_expected_schema)
        self.assertIn("properties", full_expected_schema["items"])
        self.assertIn("rotation", full_expected_schema["items"]["properties"])
        expected_schema = full_expected_schema["items"]["properties"]["rotation"]
        actual_schema = Rotator3.make_json_schema()
        # The units are attached to the parameter, not to the underlying Model
        # (or dataclass, in classic camdkit), so as we are testing the underlying
        # model here against a piece of the overall schema, we need to add DEGREE
        # as a unit, as we did for Vector3 with METER
        actual_schema["units"] = DEGREE
        self.assertEqual(expected_schema, actual_schema)
    
    def test_transform(self):
        valid_translation = Vector3(1.0, 2.0, 3.0)
        valid_rotator = Rotator3(10.0, 20.0, 30.0)
        valid_scale = Vector3(0.5, 1.0, 2.0)
        valid_id: UUIDURN = "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf7"
        with self.assertRaises(ValidationError):
            Transform(translation="foo", rotation=valid_rotator)
        with self.assertRaises(ValidationError):
            Transform(translation=valid_translation, rotation="foo")
        with self.assertRaises(ValidationError):
            Transform(translation=valid_translation, rotation=valid_rotator,
                      scale="foo")
        with self.assertRaises(ValidationError):
            Transform(translation=valid_translation, rotation=valid_rotator,
                      id=0+1j)
        valid_transform = Transform(translation=valid_translation, rotation=valid_rotator)
        self.assertEqual(valid_transform.translation, valid_translation)
        self.assertEqual(valid_transform.rotation, valid_rotator)
        self.assertIsNone(valid_transform.scale)
        self.assertIsNone(valid_transform.id)
        updated_translation = Vector3(8 * valid_translation.x,
                                      8 * valid_translation.y,
                                      8 * valid_translation.z)
        valid_transform.translation = updated_translation
        self.assertEqual(valid_transform.translation, updated_translation)
        updated_rotation = Rotator3(8 * valid_rotator.pan,
                                    8 * valid_rotator.tilt,
                                    8 * valid_rotator.roll)
        valid_transform.rotation = updated_rotation
        self.assertEqual(valid_transform.rotation, updated_rotation)
        valid_transform.scale = valid_scale
        self.assertEqual(valid_transform.scale, valid_scale)
        valid_transform.scale = None
        self.assertIsNone(valid_transform.scale)
        valid_transform.id = valid_id
        self.assertEqual(valid_transform.id, valid_id)
        valid_transform.id = None
        self.assertIsNone(valid_transform.id)
        valid_transform = Transform(translation=valid_translation,
                                    rotation=valid_rotator,
                                    scale=valid_scale,
                                    id=valid_id)
        self.assertEqual(valid_transform.translation, valid_translation)
        self.assertEqual(valid_transform.rotation, valid_rotator)
        self.assertEqual(valid_transform.scale, valid_scale)
        self.assertEqual(valid_transform.id, valid_id)

        valid_transform_as_json = Transform.to_json(valid_transform)
        self.assertEqual(valid_transform_as_json["translation"], Vector3.to_json(valid_translation))
        self.assertEqual(valid_transform_as_json["rotation"], Rotator3.to_json(valid_rotator))
        self.assertEqual(valid_transform_as_json["scale"], Vector3.to_json(valid_scale))
        self.assertEqual(valid_transform_as_json["id"], valid_id)

        valid_transform_from_json = Transform.from_json(valid_transform_as_json)
        self.assertEqual(valid_transform, valid_transform_from_json)

        expected_schema: JsonSchemaValue = CLASSIC_TRANSFORM_SCHEMA
        full_actual_schema: JsonSchemaValue = Clip.make_json_schema()
        self.assertIn("properties", full_actual_schema)
        self.assertIn("transforms", full_actual_schema["properties"])
        actual_schema: JsonSchemaValue = full_actual_schema["properties"]["transforms"]
        self.assertEqual(expected_schema, actual_schema)


if __name__ == '__main__':
    unittest.main()
