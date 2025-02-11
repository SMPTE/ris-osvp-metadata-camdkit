#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Tests for string types"""

import json
import unittest

from typing import Optional

from pydantic import ValidationError

from camdkit.compatibility import CompatibleBaseModel
from camdkit.string_types import NonBlankUTF8String, UUID_URN_PATTERN, UUIDURN

VALID_SAMPLE_ID_URN_0 = "urn:uuid:5ca5f233-11b5-4f43-8815-948d73e48a33"
VALID_SAMPLE_ID_URN_1 = "urn:uuid:5ca5f233-11b5-dead-beef-948d73e48a33"


class StringsTestCases(unittest.TestCase):

    def test_non_blank_utf8_string(self):
        class NonBlankUTF8StringTestbed(CompatibleBaseModel):
            value: Optional[NonBlankUTF8String] = None

        x = NonBlankUTF8StringTestbed()
        self.assertIsNone(x.value)
        with self.assertRaises(ValidationError):
            x.value = 1
        with self.assertRaises(ValidationError):
            x.value = ""
        smallest_valid_non_blank_utf8_string: NonBlankUTF8String = "x"
        x.value = smallest_valid_non_blank_utf8_string
        self.assertEqual(smallest_valid_non_blank_utf8_string, x.value)
        largest_valid_non_blank_utf8_string: NonBlankUTF8String = "x" * 1023
        x.value = largest_valid_non_blank_utf8_string
        self.assertEqual(largest_valid_non_blank_utf8_string, x.value)
        smallest_too_long_non_blank_utf8_string: NonBlankUTF8String = "x" * 1024
        with self.assertRaises(ValidationError):
            x.value = smallest_too_long_non_blank_utf8_string
        expected_schema = {'type': 'string', 'minLength': 1, 'maxLength': 1023}
        entire_schema = NonBlankUTF8StringTestbed.make_json_schema()
        value_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, value_schema)

    def test_uuid_urn(self):
        class UUIDTestbed(CompatibleBaseModel):
            value: UUIDURN

        x = UUIDTestbed(value=VALID_SAMPLE_ID_URN_0)
        with self.assertRaises(ValidationError):
            x.value = 1
        with self.assertRaises(ValidationError):
            x.value = ""
        with self.assertRaises(ValidationError):
            x.value = "fail"
        x.value = VALID_SAMPLE_ID_URN_0
        self.assertEqual(VALID_SAMPLE_ID_URN_0, x.value)
        x.value = VALID_SAMPLE_ID_URN_1
        self.assertEqual(VALID_SAMPLE_ID_URN_1, x.value)
        original_re = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        expected_schema = {
            "type": "string",
            "pattern": f"^urn:uuid:{original_re}$"
        }
        entire_schema = UUIDTestbed.make_json_schema()
        uuid_schema = entire_schema["properties"]["value"]
        self.assertDictEqual(expected_schema, uuid_schema)


if __name__ == '__main__':
    unittest.main()
