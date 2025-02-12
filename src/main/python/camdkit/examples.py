#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import uuid
import copy

from pydantic import JsonValue
from pydantic.json_schema import JsonSchemaValue

from camdkit.framework import *
from camdkit.model import Clip, OPENTRACKIO_PROTOCOL_NAME, OPENTRACKIO_PROTOCOL_VERSION
from camdkit.timing_types import TimingMode, SynchronizationPTPPriorities, PTPLeaderTimeSource


def _unwrap_clip_to_pseudo_frame(wrapped_clip: JsonSchemaValue) -> JsonSchemaValue:
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
    ("lens", "pinholeFocalLength"),
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
  clip = copy.deepcopy(wrapped_clip)
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


def get_recommended_static_example():
  clip = _get_recommended_static_clip()
  return  _unwrap_clip_to_pseudo_frame(clip.to_json(0))

def get_complete_static_example():
  clip = _get_complete_static_clip()
  clip_json = clip.to_json(0)
  # Add additional custom data
  clip_json["custom"] = {
    "pot1": 2435,
    "button1": False
  }
  return _unwrap_clip_to_pseudo_frame(clip_json)

def _add_recommended_static_clip_parameters(clip: Clip) -> Clip:
  clip.camera_label = "A"
  clip.lens_make = "LensMaker"
  clip.lens_model = "Model15"
  clip.active_sensor_physical_dimensions = ActiveSensorPhysicalDimensions(width=36.0,height=24.0)
  return clip

def _get_recommended_static_clip() -> Clip:
  clip: Clip = _get_recommended_dynamic_clip()
  _add_recommended_static_clip_parameters(clip)
  return clip

def _get_complete_static_clip() -> Clip:
  clip: Clip = _get_complete_dynamic_clip()
  _add_recommended_static_clip_parameters(clip)
  # no augmentations, just additions
  clip.active_sensor_resolution = Dimensions(width=3840,height=2160)
  clip.anamorphic_squeeze = 1
  clip.camera_make = "CameraMaker"
  clip.camera_model = "Model20"
  clip.camera_firmware = "1.2.3"
  clip.camera_serial_number = "1234567890A"
  clip.capture_frame_rate = Fraction(24000, 1001)
  clip.duration = Fraction(1,25)
  clip.fdl_link = uuid.uuid4().urn
  clip.iso = 4000
  clip.lens_distortion_is_projection = True
  clip.lens_distortion_overscan_max = 1.2
  clip.lens_undistortion_overscan_max = 1.3
  clip.lens_nominal_focal_length = 14
  clip.lens_serial_number = "1234567890A"
  clip.shutter_angle = 45.0
  clip.tracker_model = "Tracker"
  clip.tracker_firmware = "1.2.3"
  clip.tracker_make = "TrackerMaker"
  clip.tracker_serial_number = "1234567890A"
  return clip


def get_recommended_dynamic_example():
  clip = _get_recommended_dynamic_clip()
  return _unwrap_clip_to_pseudo_frame(clip.to_json(0))

def get_complete_dynamic_example():
  clip = _get_complete_dynamic_clip()
  clip_json = clip.to_json(0)

  # Add additional custom data
  clip_json["custom"] = {
    "pot1": 2435,
    "button1": False
  }
  return _unwrap_clip_to_pseudo_frame(clip_json)

def _example_transform_components() -> tuple[Vector3, Rotator3]:
  return Vector3(x=1.0, y=2.0, z=3.0), Rotator3(pan=180.0, tilt=90.0, roll=45.0)

def _get_recommended_dynamic_clip():
  clip = Clip()
  # identity
  clip.sample_id = (uuid.uuid4().urn,)
  clip.source_id = (uuid.uuid4().urn,)
  clip.source_number = (1,)
  clip.protocol = (VersionedProtocol(OPENTRACKIO_PROTOCOL_NAME,OPENTRACKIO_PROTOCOL_VERSION),)
  # tracking
  clip.tracker_status = ("Optical Good",)
  clip.tracker_recording = (False,)
  clip.tracker_slate = ("A101_A_4",)
  clip.tracker_notes = ("Example generated sample.",)
  # timing
  clip.timing_mode = (TimingMode.EXTERNAL,)
  clip.timing_sample_rate = (Fraction(24000, 1001),)
  clip.timing_timecode = (Timecode(1,2,3,4,TimecodeFormat(frame_rate=Fraction(24000, 1001))),)
  # transforms
  v, r = _example_transform_components()
  clip.transforms = ((Transform(translation=v, rotation=r, id="Camera"),),)
  # lens
  clip.lens_f_number = (4.0,)
  clip.lens_pinhole_focal_length = (24.305,)
  clip.lens_focus_distance = (10.0,)
  clip.lens_entrance_pupil_offset = (0.123,)
  clip.lens_encoders = (FizEncoders(focus=0.1, iris=0.2, zoom=0.3),)
  clip.lens_distortions = ((Distortion([1.0,2.0,3.0], [1.0,2.0]),),)
  clip.lens_projection_offset = (ProjectionOffset(0.1, 0.2),)
  return clip

def _get_complete_dynamic_clip():
  clip = _get_recommended_dynamic_clip()
  # augmenting recommended values
  #   timing
  clip.timing_mode = (TimingMode.INTERNAL,)
  #   transforms
  v, r = _example_transform_components()
  clip.transforms = ((Transform(translation=v, rotation=r, id="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, id="Crane Arm"),
                      Transform(translation=v, rotation=r, scale=v, id="Camera")
                      ),)
  #   lens
  clip.lens_distortions = ((Distortion([1.0,2.0,3.0,4.0,5.0,6.0], [1.0,2.0], "Brown-Conrady D-U"), Distortion([1.0,2.0,3.0,4.0,5.0,6.0], [1.0,2.0], "Brown-Conrady U-D"),),)

  # additions
  #   identity
  clip.related_sample_ids = ((uuid.uuid4().urn,uuid.uuid4().urn),)
  #   timing
  clip.timing_sample_timestamp = (Timestamp(1718806554, 500000000),)
  clip.timing_recorded_timestamp = (Timestamp(1718806000, 500000000),)
  clip.timing_sequence_number = (0,)
  clip.timing_synchronization = (Synchronization(
    frequency=Fraction(24000,1001),
    present=True,
    locked=True,
    source=SynchronizationSourceEnum.PTP,
    ptp=SynchronizationPTP(
      profile=PTPProfile.SMPTE_2059_2_2021,
      domain=1,
      leader_identity="00:11:22:33:44:55",
      leader_priorities=SynchronizationPTPPriorities(128, 128),
      leader_accuracy=0.00000005,
      time_source=PTPLeaderTimeSource.GNSS,
      mean_path_delay=0.000123,
      vlan=100)
  ),)
  #   transforms
  clip.global_stage = (GlobalPosition(100.0,200.0,300.0,100.0,200.0,300.0),)
  v = Vector3(x=1.0, y=2.0, z=3.0)
  r = Rotator3(pan=180.0, tilt=90.0, roll=45.0)
  clip.transforms = ((Transform(translation=v, rotation=r, id="Dolly"),
                      Transform(translation=v, rotation=r, scale=v, id="Crane Arm"),
                      Transform(translation=v, rotation=r, scale=v, id="Camera")
                      ),)
  #   lens
  clip.lens_f_number = (4.0,)
  clip.lens_t_number = (4.1,)
  clip.lens_raw_encoders = (RawFizEncoders(focus=1000, iris=2000, zoom=3000),)
  clip.lens_distortion_overscan = (1.1,)
  clip.lens_undistortion_overscan = (1.2,)
  clip.lens_exposure_falloff = (ExposureFalloff(1.0, 2.0, 3.0),)
  clip.lens_distortion_offset = (DistortionOffset(1.0, 2.0),)
  clip.lens_custom = ((1.0,2.0),)
  return clip
