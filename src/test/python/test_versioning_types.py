#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Tests for types for versioning protocols"""

import unittest

from pydantic import ValidationError

from camdkit.versioning_types import VersionedProtocol

class VersioningTypesTestCases(unittest.TestCase):
    def test_versioning_type(self):
        valid_name: str = "OpenTrackIO"
        valid_major_version = 0
        valid_minor_version = 9
        valid_patch_version = 2
        valid_version = (valid_major_version, valid_minor_version, valid_patch_version)
        with self.assertRaises(TypeError):
            VersionedProtocol()
        with self.assertRaises(ValidationError):
            VersionedProtocol("", valid_version)
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, "foo")
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, "0.9.2")
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, "10.9.2")
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, "0.10.2")
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, "0.9.10")
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, 0.92)
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, 0.9+2j)  # creative thinking
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, ())
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, (valid_major_version,))
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, (valid_major_version,
                                           valid_minor_version))
        with self.assertRaises(ValidationError):
            VersionedProtocol(valid_name, (valid_major_version,
                                           valid_minor_version,
                                           valid_patch_version,
                                           valid_patch_version))
        with self.assertRaises(ValueError):
            VersionedProtocol(reversed(valid_name), valid_version)


if __name__ == '__main__':
    unittest.main()
