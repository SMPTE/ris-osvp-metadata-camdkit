#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import uuid

from camdkit.framework import *
from camdkit.model import Clip, OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION

def get_recommended_static_example():
  clip = _get_recommended_dynamic_clip()
  clip.camera_label = "A"
  clip.lens_make = "LensMaker"
  clip.lens_model = "Model15"
  clip.active_sensor_physical_dimensions = Dimensions(width=36.0,height=24.0)
  return clip.to_json(0)

def get_complete_static_example():
  clip = _get_complete_dynamic_clip()
  clip.active_sensor_physical_dimensions = Dimensions(width=36.0,height=24.0)
  clip.active_sensor_resolution = Dimensions(width=3840,height=2160)
  clip.anamorphic_squeeze = 1
  clip.camera_label = "A"
  clip.camera_make = "CameraMaker"
  clip.camera_model = "Model20"
  clip.camera_firmware = "1.2.3"
  clip.camera_serial_number = "1234567890A"
  clip.capture_frame_rate = Fraction(24000, 1001)
  clip.duration = Fraction(1,25)
  clip.fdl_link = uuid.uuid4().urn
  clip.iso = 4000
  clip.lens_distortion_overscan_max = 1.2
  clip.lens_make = "LensMaker"
  clip.lens_model = "Model15"
  clip.lens_nominal_focal_length = 14
  clip.lens_serial_number = "1234567890A"
  clip.shutter_angle = 45.0
  clip.tracker_model = "Tracker"
  clip.tracker_firmware = "1.2.3"
  clip.tracker_make = "TrackerMaker"
  clip.tracker_serial_number = "1234567890A"
  
  clip_json = clip.to_json(0)
  # Add additional custom data
  clip_json["custom"] = {
    "pot1": 2435,
    "button1": False
  }
  return clip_json

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
  clip.source_id = (uuid.uuid4().urn,)
  clip.source_number = (1,)
  clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME,OPENTRACKIO_PROTOCOL_VERSION,),)

  clip.tracker_status = ("Optical Good",)
  clip.tracker_recording = (False,)
  clip.tracker_slate = ("A101_A_4",)
  clip.tracker_notes = ("Example generated sample.",)

  clip.timing_mode = (TimingModeEnum.EXTERNAL,)
  clip.timing_frame_rate = (Fraction(24000, 1001),)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat(Fraction(24000, 1001),True)),)
  
  v = Vector3(x=1.0, y=2.0, z=3.0)
  r = Rotator3(pan=180.0, tilt=90.0, roll=45.0)
  clip.transforms = ((Transform(translation=v, rotation=r, transformId="Camera"),),)
  clip.lens_f_number = (4.0,)
  clip.lens_focal_length = (24.305,)
  clip.lens_focus_distance = (1000,)
  clip.lens_entrance_pupil_offset = (0.123,)
  clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_distortion = (Distortion([1.0,2.0,3.0], [1.0,2.0]),)
  clip.lens_perspective_shift = (PerspectiveShift(0.1, 0.2),)
  return clip

def _get_complete_dynamic_clip():
  clip = Clip()
  clip.sample_id = (uuid.uuid4().urn,)
  clip.source_id = (uuid.uuid4().urn,)
  clip.source_number = (1,)
  clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION),)
  clip.related_sample_ids = ((uuid.uuid4().urn,uuid.uuid4().urn),)
  clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)

  clip.tracker_status = ("Optical Good",)
  clip.tracker_recording = (False,)
  clip.tracker_slate = ("A101_A_4",)
  clip.tracker_notes = ("Example generated sample.",)

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
      leader="00:11:22:33:44:55"
    ),
    offsets=SynchronizationOffsets(1.0,2.0,3.0)
  ),)
  
  v = Vector3(x=1.0, y=2.0, z=3.0)
  r = Rotator3(pan=180.0, tilt=90.0, roll=45.0)
  clip.transforms = ((Transform(translation=v, rotation=r, transformId="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, transformId="Crane Arm", parentTransformId="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, transformId="Camera", parentTransformId="Crane Arm")
                      ),)

  clip.lens_f_number = (4.0,)
  clip.lens_t_number = (4.1,)
  clip.lens_focal_length = (24.305,)
  clip.lens_focus_distance = (10.0,)
  clip.lens_entrance_pupil_offset = (0.123,)
  clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_raw_encoders = (RawFizEncoders(focus=1000, iris=2000, zoom=3000),)
  clip.lens_distortion_overscan = (1.0,)
  clip.lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),)
  clip.lens_distortion = (Distortion([1.0,2.0,3.0,4.0,5.0,6.0], [1.0,2.0]),)
  clip.lens_undistortion = (Distortion([1.0,2.0,3.0,4.0,5.0,6.0], [1.0,2.0]),)
  clip.lens_distortion_shift = (DistortionShift(1.0, 2.0),)
  clip.lens_perspective_shift = (PerspectiveShift(0.1, 0.2),)
  clip.lens_custom = ((1.0,2.0),)
  return clip
