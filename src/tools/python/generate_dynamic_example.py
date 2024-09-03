#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''CLI tool to generate and validate JSON for an example dynamic data frame'''

import json
import uuid

from camdkit.framework import Vector3, Rotator3, Transform
from camdkit.model import *

def main():
  clip = Clip()
  clip.sample_id = (uuid.uuid4().urn,)
  clip.sample_type = ("dynamic",)
  clip.protocol = ("OpenTrackIO_0.1.0",)
  clip.related_samples = ((uuid.uuid4().urn,uuid.uuid4().urn),)
  clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)

  clip.device_status = ("Optical Good",)
  clip.device_recording = (False,)
  clip.device_slate = ("A101_A_4",)
  clip.device_notes = ("Example generated sample.",)

  clip.timing_mode = (TimingModeEnum.INTERNAL,)
  clip.timing_sample_timestamp = (Timestamp(1718806554, 0, 0),)
  clip.timing_recorded_timestamp = (Timestamp(1718806000, 0),)
  clip.timing_sequence_number = (0,)
  clip.timing_frame_rate = (Fraction(24000, 1001),)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat(Fraction(24000, 1001),True)),)
  clip.timing_synchronization = (Synchronization(
    present=True,
    locked=True,
    frequency=Fraction(24000, 1001),
    source=SynchronizationSourceEnum.PTP,
    ptp_offset=0.0,
    ptp_domain=1,
    ptp_master="00:11:22:33:44:55",
    offsets=SynchronizationOffsets(1.0,2.0,3.0)
  ),)
  
  v = Vector3(x=1.0, y=2.0, z=3.0)
  r = Rotator3(pan=1.0, tilt=2.0, roll=3.0)
  clip.transforms = ((Transform(translation=v, rotation=Rotator3(0,0,0), name="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, name="Crane Arm", parent="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, name="Camera", parent="Crane Arm")
                      ),)

  clip.lens_f_number = (4000,)
  clip.lens_t_number = (4100,)
  clip.lens_focal_length = (24.305,)
  clip.lens_focus_position = (1000,)
  clip.lens_entrance_pupil_distance = (Fraction(1000,100),)
  clip.lens_encoders = (Encoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_fov_scale = (Orientations(1.0, 1.0),)
  clip.lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),)
  clip.lens_distortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_undistortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_centre_shift = (CentreShift(1.0, 2.0),)
  clip.lens_perspective_shift = (PerspectiveShift(0.1, 0.2),)
  clip.lens_custom = ((1.0,2.0),)

  clip_json = clip.validate()

	# Add additional custom data
  clip_json["custom"] = {
		"pot1": 2435,
		"button1": False
	}

  print(json.dumps(clip_json, indent=2))
  

if __name__ == "__main__":
  main()
