#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Property tests: generated Clip JSON validates against the published schema."""

import json
import unittest

import jsonschema
from hypothesis import given, settings, HealthCheck

from camdkit.clip import Clip
from camdkit.examples import _unwrap_clip_to_pseudo_frame

from property.generators import clips

_SUPPRESS = [HealthCheck.too_slow, HealthCheck.filter_too_much]

CLIP_SCHEMA = None
CLIP_VALIDATOR = None


def setUpModule():
    global CLIP_SCHEMA, CLIP_VALIDATOR
    CLIP_SCHEMA = Clip.make_json_schema()
    CLIP_VALIDATOR = jsonschema.Draft202012Validator(CLIP_SCHEMA)


def _to_single_frame_json(clip):
    """Return a schema-valid single-frame JSON dict for the clip.

    Clip.to_json() produces multi-frame arrays for dynamic fields; the schema
    expects single values. _unwrap_clip_to_pseudo_frame mirrors what the example
    generators do before writing the example JSON files.
    """
    return json.loads(json.dumps(_unwrap_clip_to_pseudo_frame(clip.to_json(0))))


class SchemaAgreementTests(unittest.TestCase):

    @given(clip=clips())
    @settings(max_examples=75, suppress_health_check=_SUPPRESS)
    def test_valid_clip_validates_against_schema(self, clip):
        """Every generated Clip's first frame passes schema validation."""
        json_data = _to_single_frame_json(clip)
        errors = list(CLIP_VALIDATOR.iter_errors(json_data))
        if errors:
            self.fail(
                f"Schema validation failed for generated clip.\n"
                f"First error: {errors[0].message}\n"
                f"Path: {list(errors[0].path)}\n"
                f"JSON: {json.dumps(json_data, indent=2)}"
            )

    def test_empty_clip_validates_against_schema(self):
        """An empty Clip serializes to {} and the schema must accept it (all fields optional)."""
        json_data = _to_single_frame_json(Clip())
        self.assertEqual(json_data, {}, "Empty Clip should serialize to an empty document")
        CLIP_VALIDATOR.validate(json_data)

    def test_schema_is_stable(self):
        """make_json_schema() is idempotent — calling it twice returns equal results."""
        schema1 = Clip.make_json_schema()
        schema2 = Clip.make_json_schema()
        self.assertEqual(schema1, schema2)

    def test_schema_rejects_wrong_rational_type(self):
        """A rational with a string numerator must fail schema validation."""
        bad = {"static": {"duration": {"num": "not-a-number", "denom": 1}}}
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertTrue(len(errors) > 0, "Schema should reject a non-integer rational numerator")

    def test_schema_rejects_negative_denom(self):
        """A rational with negative denominator must fail schema validation."""
        bad = {"static": {"duration": {"num": 1, "denom": -1}}}
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertTrue(len(errors) > 0, "Schema should reject a negative denominator")

    def test_schema_rejects_unknown_sync_source(self):
        """An unrecognized synchronization source must fail schema validation."""
        # Single-frame format: synchronization is a scalar object, not an array.
        # Using an array would fail for the wrong reason (type mismatch, not enum).
        bad = {
            "timing": {
                "synchronization": {
                    "locked": True,
                    "source": "bluetooth",
                }
            }
        }
        errors = list(CLIP_VALIDATOR.iter_errors(bad))
        self.assertTrue(len(errors) > 0, "Schema should reject unknown synchronization source")


if __name__ == '__main__':
    unittest.main()
