#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import uuid

from camdkit.framework import *
from camdkit.model import Clip, VERSION_STRING

def get_recommended_static_example():
  clip = _get_recommended_dynamic_clip()
  clip.camera_id = "A"
  clip.lens_make = "LensMaker"
  clip.lens_model = "Model15"
  clip.active_sensor_physical_dimensions = Dimensions(width=36000,height=24000)
  return clip.to_json(0)

def get_complete_static_example():
  clip = _get_complete_dynamic_clip()
  clip.camera_id = "A"
  clip.lens_make = "LensMaker"
  clip.lens_model = "Model15"
  clip.lens_nominal_focal_length = 14
  clip.lens_serial_number = "1234567890A"
  clip.device_model = "Tracker"
  clip.device_firmware = "1.2.3"
  clip.device_make = "TrackerMaker"
  clip.device_serial_number = "1234567890A"
  clip.active_sensor_physical_dimensions = Dimensions(width=36000,height=24000)
  clip.active_sensor_resolution = Dimensions(width=3840,height=2160)
  clip.anamorphic_squeeze = 1
  return clip.to_json(0)

def get_recommended_dynamic_example():
  clip = _get_recommended_dynamic_clip()
  return clip.to_json(0)

def get_complete_dynamic_example():
  clip = _get_complete_dynamic_clip()
  clip_json = clip.to_json(0)

	# Add additional custom data
  clip_json["custom"] = {
		"pot1": 2435,
		"button1": False
	}
  return clip_json

def _get_recommended_dynamic_clip():
  clip = Clip()
  clip.sample_id = (uuid.uuid4().urn,)
  clip.protocol_version = (VERSION_STRING,)
  clip.related_samples = ((uuid.uuid4().urn,uuid.uuid4().urn),)

  clip.device_status = ("Optical Good",)
  clip.device_recording = (False,)
  clip.device_slate = ("A101_A_4",)
  clip.device_notes = ("Example generated sample.",)

  clip.timing_mode = (TimingModeEnum.EXTERNAL,)
  clip.timing_frame_rate = (Fraction(24000, 1001),)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat(Fraction(24000, 1001),True)),)
  
  v = Vector3(x=1.0, y=2.0, z=3.0)
  r = Rotator3(pan=180.0, tilt=90.0, roll=45.0)
  clip.transforms = ((Transform(translation=v, rotation=Rotator3(0,0,0), name="Camera"),),)
  clip.lens_f_number = (4000,)
  clip.lens_focal_length = (24.305,)
  clip.lens_focus_distance = (1000,)
  clip.lens_entrance_pupil_distance = (Fraction(1000,100),)
  clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_distortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_perspective_shift = (PerspectiveShift(0.1, 0.2),)
  return clip

def _get_complete_dynamic_clip():
  clip = Clip()
  clip.sample_id = (uuid.uuid4().urn,)
  clip.protocol_version = (VERSION_STRING,)
  clip.related_samples = ((uuid.uuid4().urn,uuid.uuid4().urn),)
  clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)

  clip.device_status = ("Optical Good",)
  clip.device_recording = (False,)
  clip.device_slate = ("A101_A_4",)
  clip.device_notes = ("Example generated sample.",)

  clip.timing_mode = (TimingModeEnum.INTERNAL,)
  clip.timing_sample_timestamp = (Timestamp(1718806554, 500000000, 0),)
  clip.timing_recorded_timestamp = (Timestamp(1718806000, 500000000),)
  clip.timing_sequence_number = (0,)
  clip.timing_frame_rate = (Fraction(24000, 1001),)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat(Fraction(24000, 1001),True)),)
  clip.timing_synchronization = (Synchronization(
    present=True,
    locked=True,
    frequency=Fraction(24000, 1001),
    source=SynchronizationSourceEnum.PTP,
    ptp=SynchronizationPTP(
      offset=0.0,
      domain=1,
      master="00:11:22:33:44:55"
    ),
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
  clip.lens_focus_distance = (1000,)
  clip.lens_entrance_pupil_distance = (Fraction(1000,100),)
  clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_distortion_overscan = (1.0,)
  clip.lens_distortion_scale = (1.0,)
  clip.lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),)
  clip.lens_distortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_undistortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_distortion_shift = (DistortionShift(1.0, 2.0),)
  clip.lens_perspective_shift = (PerspectiveShift(0.1, 0.2),)
  clip.lens_custom = ((1.0,2.0),)
  return clip
