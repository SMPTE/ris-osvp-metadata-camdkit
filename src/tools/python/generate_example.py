#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''CLI tool to generate and validate example JSON'''

import json
import uuid

from jsonschema import validate
from camdkit.framework import Vector3, Rotator3, Transform
from camdkit.model import *

def main():
  clip = Clip()
  clip.packet_id = (uuid.uuid1().urn,)
  clip.protocol = ("OpenTrackIO_0.1.0",)
  clip.timing_mode = (TimingModeEnum.INTERNAL,)
  clip.timing_timestamp = (Timestamp(1718806554, 0),)
  clip.timing_sequence_number = (0,)
  clip.timing_frame_rate = (23.976,)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat.TC_24D),)
  clip.timing_synchronization = (Synchronization(
    enabled=True,
    locked=True,
    frequency=23.976,
    source=SynchronizationSourceEnum.PTP,
    ptp_offset=0.0,
    ptp_domain=1,
    ptp_master="00:11:22:33:44:55",
    offsets=SynchronizationOffsets(1.0,2.0,3.0)
  ),)
  
  translation = Vector3(x=1.0, y=2.0, z=3.0)
  rotation = Rotator3(pan=1.0, tilt=2.0, roll=3.0)
  clip.transforms = ((Transform(translation=translation, rotation=rotation),),)

  clip.f_number = (4000,)
  clip.lens_encoders = (Encoders(focus=0.1, iris=0.2, zoom=0.3),)

  # Create the static single frame of JSON
  clip._set_static()
  json_clip = clip[0].to_json()

  # Now validate this against the generated schema
  schema = clip.make_json_schema()
  validate(json_clip, schema)

  print(json.dumps(json_clip, indent=2))
  
if __name__ == "__main__":
  main()
