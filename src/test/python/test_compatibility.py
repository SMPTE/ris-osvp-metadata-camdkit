#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Tests for components providing compatibility with classic camdkit"""

import unittest
import json

from typing import Annotated, Any
from copy import deepcopy

from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue

from camdkit.camera_types import StaticCamera
from camdkit.compatibility import CompatibleBaseModel

class PureOpt(BaseModel):
    a: int
    b: int | None = None
    c: str

EXPECTED_PURE_OPT_SCHEMA = {
    # n.b. dict order changed from BaseModel.model_json_schema() output to be sure that
    #   order of elements isn't important
    "type": "object",
    "properties": {
        "a": { "title": "A", "type": "integer" },
        "b": { "anyOf": [ { "type": "integer" }, { "type": "null" } ],
               "default": None, "title": "B" },
        "c": { "title": "C", "type": "string" }
    },
    "required": [ "a", "c" ],
    "title": "PureOpt"
}


class CompatiblePureOpt(CompatibleBaseModel):
    a: int
    b: int | None = None
    c: str

EXPECTED_COMPATIBLE_PURE_OPT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "a": { "type": "integer" },
        "b": { "type": "integer" },
        "c": { "type": "string" }
    },
    "required": [ "a", "c" ]
}


class AnnotatedOpt(BaseModel):
    class FauxField:
        def __init__(self, *_) -> None:
            pass

    a: int
    b: Annotated[int | None, FauxField("foo")] = None
    c: str

EXPECTED_ANNOTATED_OPT_SCHEMA = {
    "type": "object",
    "properties": {
        "a": { "title": "A", "type": "integer" },
        "b": { "anyOf": [ { "type": "integer" }, { "type": "null" } ],
               "default": None, "title": "B" },
        "c": { "title": "C", "type": "string" }
    },
    "required": [ "a", "c" ],
    "title": "AnnotatedOpt"
}


class PureArray(BaseModel):
    a: int
    b: tuple[int, ...]
    c: str

EXPECTED_PURE_ARRAY_SCHEMA = {
    "properties": {
        "a": { "title": "A", "type": "integer" },
        "b": { "title": "B",
               "type": "array",
               "items": {"type": "integer" } },
        "c": { "title": "C", "type": "string" }
    },
    "required": [ "a", "b", "c" ],
    "title": "PureArray",
    "type": "object"
}


# regular POD parameters, e.g. lens entrance pupil offset
class OptArray(BaseModel):
    a: int
    b: tuple[int, ...] | None
    c: str

EXPECTED_OPT_ARRAY_SCHEMA = {
    "properties": {
        "a": { "title": "A", "type": "integer" },
        "b": { "title": "B",
               "anyOf": [
                   { "items": { "type": "integer" }, "type": "array" },
                   { "type": "null" } ] },
        "c": { "title": "C", "type": "string" }
    },
    "required": [ "a", "b", "c" ],
    "title": "OptArray",
    "type": "object"
}

CLASSIC_STATIC_CAMERA_SCHEMA_W_JUST_ANAMORPHIC_SQUEEZE = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "anamorphicSqueeze": {
            "type": "object",
            "properties": {
                "num": { "type": "integer", "minimum": 1, "maximum": 2147483647 },
                "denom": { "type": "integer", "minimum": 1, "maximum": 4294967295 } },
            "required": [ "num", "denom" ],
            "additionalProperties": False,
            "description": "Nominal ratio of height to width of the image of an axis-aligned\nsquare captured by the camera sensor. It can be used to de-squeeze\nimages but is not however an exact number over the entire captured\narea due to a lens' intrinsic analog nature.\n"
        },
    }
}

STATIC_CAMERA_SCHEMA_W_JUST_ANAMORPHIC_SQUEEZE = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "anamorphicSqueeze": {
            "anyOf": [
                { "type": "object",
                  "properties": {
                      "num": { "type": "integer", "maximum": 2147483647, "minimum": 1 },
                      "denom": { "type": "integer", "maximum": 4294967295, "minimum": 1 }
                  },
                  "required": [ "num", "denom" ],
                  "additionalProperties": False },
                { "type": "null" }
            ],
            "default": None,
            "description": "Nominal ratio of height to width of the image of an axis-aligned\nsquare captured by the camera sensor. It can be used to de-squeeze\nimages but is not however an exact number over the entire captured\narea due to a lens' intrinsic analog nature.\n"
        }
    }
}


def remove_properties_besides(schema: JsonSchemaValue, keeper: str) -> JsonSchemaValue:
    property_names = [k for k in schema["properties"].keys() if k != keeper]
    for property_name in property_names:
        schema["properties"].pop(property_name)
    return schema


class CompatibilityTestCases(unittest.TestCase):
    # make sure Pydantic hasn't changed its schema generator without our noticing
    def test_schema_generation(self):
        self.assertDictEqual(EXPECTED_PURE_OPT_SCHEMA, PureOpt.model_json_schema())
        self.assertDictEqual(EXPECTED_COMPATIBLE_PURE_OPT_SCHEMA, CompatiblePureOpt.make_json_schema())
        self.assertDictEqual(EXPECTED_ANNOTATED_OPT_SCHEMA, AnnotatedOpt.model_json_schema())
        self.assertDictEqual(EXPECTED_PURE_ARRAY_SCHEMA, PureArray.model_json_schema())
        self.assertDictEqual(EXPECTED_OPT_ARRAY_SCHEMA, OptArray.model_json_schema())

    def test_annotated_opt_same_as_pure_opt(self):
        """Convince ourselves Annotated leaves no trace in generated schema"""
        pure_opt_schema = PureOpt.model_json_schema()
        annotated_opt_schema = AnnotatedOpt.model_json_schema()
        pure_opt_schema.pop("title", None)
        annotated_opt_schema.pop("title", None)
        self.assertDictEqual(pure_opt_schema, annotated_opt_schema)


if __name__ == '__main__':
    unittest.main()
