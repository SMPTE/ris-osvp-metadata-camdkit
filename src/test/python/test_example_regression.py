#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import json
import unittest

from copy import deepcopy
from pathlib import Path
from typing import Literal

from pydantic.json_schema import JsonSchemaValue

CLASSIC = Path("src/test/resources/classic")
CLASSIC_EXAMPLES_DIR: Path = CLASSIC / "examples"

CURRENT = Path("build/opentrackio")
CURRENT_EXAMPLES_DIR: Path = CURRENT / "examples"

def corrupt_clip_to_pseudo_frame(clip: JsonSchemaValue) -> None:
    paths_to_unwrap: tuple[tuple[str, ...], ...] = (
        ("globalStage",),
        ("lens", "custom"),
        ("lens", "distortion"),
        ("lens", "distortionOffset"),
        ("lens", "distortionOverscan"),
        ("lens", "encoders"),
        ("lens", "entrancePupilOffset"),
        ("lens", "exposureFalloff"),
        ("lens", "fStop"),
        ("lens", "focalLength"),
        ("lens", "focusDistance"),
        ("lens", "projectionOffset"),
        ("lens", "rawEncoders"),
        ("lens", "tStop"),
        ("lens", "undistortionOverscan"),
        ("protocol",),
        ("relatedSampleIds",),
        ("sampleId",),
        ("sourceId",),
        ("sourceNumber",),
        ("timing", "mode"),
        ("timing", "recordedTimestamp"),
        ("timing", "sampleRate"),
        ("timing", "sampleTimestamp"),
        ("timing", "sequenceNumber"),
        ("timing", "synchronization"),
        ("timing", "timecode"),
        ("tracker", "notes"),
        ("tracker", "recording"),
        ("tracker", "slate"),
        ("tracker", "status"),
        ("transforms",)
    )
    for path in paths_to_unwrap:
        # REALLY brute-force
        if len(path) == 1:
            k0 = path[0]
            if k0 in clip:
                clip[k0] = clip[k0][0]
        elif len(path) == 2:
            k0 = path[0]
            if k0 in clip:
                k1 = path[1]
                if k1 in clip[k0]:
                    clip[k0][k1] = clip[k0][k1][0]
        else:
            raise RuntimeError("That's too deep for me I'm afraid")
    return clip

def generify_urn_uuids(clip: JsonSchemaValue) -> None:
    paths_to_generify: tuple[str | tuple[str, ...], ...] = (
        "sampleId",
        "sourceId",
        "relatedSampleIds",
        ("static", "camera", "fdlLink")
    )
    for path in paths_to_generify:
        containing_dict = clip
        if isinstance(path, tuple):
            if not path:
                raise RuntimeError("empty tuple of dict keys in URN generification")
            if len(path) == 1:
                path = path[0]
            else:
                for pathlet in path[:-1]:
                    if pathlet not in containing_dict:
                        return
                    containing_dict = containing_dict[pathlet]
                path = path[-1]
        if path in containing_dict:
            if type(containing_dict[path]) is list:
                containing_dict[path] = ["urn:uuid:random" for _ in containing_dict[path]]
            else:
                containing_dict[path] = "urn:uuid:random"


class ExampleTestCases(unittest.TestCase):

    def test_corruption(self):
        good_clip = {
            "globalStage": ["foo"],
            "lens": { "distortion": [4.1] }
        }
        pseudo_frame = {
            "globalStage": "foo",
            "lens": { "distortion": 4.1}
        }
        corrupted_clip = corrupt_clip_to_pseudo_frame(deepcopy(good_clip))
        self.assertEqual(pseudo_frame, corrupted_clip)

    def compare(self, completeness: Literal['recommended', 'complete'],
                scope: Literal['static', 'dynamic']) -> None:
        classic_path = Path(CLASSIC_EXAMPLES_DIR, f"{completeness}_{scope}_example.json")
        pydantic_path = Path(CURRENT_EXAMPLES_DIR, f"{completeness}_{scope}_example.json")
        with open(classic_path) as classic_file:
            classic_json = json.load(classic_file)
            with open(pydantic_path) as pydantic_file:
                pydantic_json = json.load(pydantic_file)
                corrupt_clip_to_pseudo_frame(pydantic_json)
                generify_urn_uuids(classic_json)
                generify_urn_uuids(pydantic_json)
                self.assertEqual(classic_json, pydantic_json)

    def test_recommended_dynamic(self):
        self.compare('recommended', 'dynamic')

    def test_complete_dynamic(self):
        self.compare('complete', 'dynamic')

    def test_recommended_static(self):
        self.compare('recommended', 'static')

    def test_complete_static(self):
        self.compare('complete', 'static')


if __name__ == '__main__':
    unittest.main()
