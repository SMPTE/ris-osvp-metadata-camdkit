#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Individual component schema for various sections"""
import json

from typing import Any
from pathlib import Path

from camdkit.model import Clip

__all__ = 'SECTIONS_AND_FILENAMES'

SECTIONS_AND_FILENAMES = {
    ('static', 'camera'): 'static_camera',
    ('static', 'duration'): 'static_duration',
    ('static', 'lens'): 'static_lens',
    ('static', 'tracker'): 'static_tracker',
    ('lens',): 'lens',
    ('timing',): 'timing',
    ('tracker',): 'tracker',
    ('transforms',): 'transforms'
}

def schema_for_section(schema: dict[str, Any],
                       prop_names: tuple[str, ...]) -> dict[str, Any]:
    remaining_schema = schema
    for prop_name in prop_names:
        remaining_schema = remaining_schema["properties"][prop_name]
    return remaining_schema

def write_schema(schema: dict[str, Any],
                 output_filename,
                 output_dir=Path('/tmp')) -> None:
    with open(output_dir / f"{output_filename}.json", 'w') as f:
        json.dump(schema, f, indent=2, sort_keys=True)

def write_schemas() -> None:
    full_schema = Clip.make_json_schema()
    for section, filename in SECTIONS_AND_FILENAMES.items():
        schema = schema_for_section(full_schema, section)
        write_schema(schema, filename)


if __name__ == '__main__':
    write_schemas()
