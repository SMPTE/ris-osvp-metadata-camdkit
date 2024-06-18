#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''CLI tool to generate and validate example JSON'''

import json
from jsonschema import validate
from camdkit.framework import Vector3, Rotator3, Transform
from camdkit.model import Clip

def main():
  clip = Clip()
  translation = Vector3(x=1.0, y=2.0, z=3.0)
  rotation = Rotator3(pan=1.0, tilt=2.0, roll=3.0)
  clip.transforms = ((Transform(translation=translation, rotation=rotation),),)
  clip.f_number = (4000,)
  clip.timing_mode = ("internal",)
  
  # Create the static single frame of JSON
  clip._set_static()
  json_clip = clip[0].to_json()

  # Now validate this against the generated schema
  schema = clip.make_json_schema()
  validate(json_clip, schema)

  print(json.dumps(json_clip, indent=2))
  
if __name__ == "__main__":
  main()
