#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""ARRI camera metadata reader"""

import csv
import math
from fractions import Fraction

import json

import camdkit.model
import camdkit.utils as utils
from camdkit.camera_types import PhysicalDimensions, SenselDimensions
from camdkit.numeric_types import StrictlyPositiveFloat, StrictlyPositiveRational

# https://www.arri.com/resource/blob/31908/14147b455c90a9a35018c0d091350ff3/2021-10-arri-formatsandresolutionsoverview-3-4-data.pdf
_CAMERA_FAMILY_PIXEL_PITCH_MAP = {
  ("ALEXALF", 1920) : Fraction(316800, 1920),
  ("ALEXALF", 2048) : Fraction(316800, 2048),
  ("ALEXALF", 3840) : Fraction(316800, 3840),
  ("ALEXALF", 4448) : Fraction(367000, 4448),
}

def t_number_from_linear_iris_value(lin_value: int) -> StrictlyPositiveFloat:
  """Calculate t-number (regular iris values) from linear iris values
  """
  return math.pow(2, (lin_value - 1000)/1000/2)

def to_clip(path: str) -> camdkit.model.Clip:
    if path.lower().endswith(".csv"):
        return to_clip_from_csv(path)
    elif path.lower().endswith(".json"):
        return to_clip_from_json(path)
    else:
        raise ValueError(f"ARRI exported metadata must be in either CSV or JSON format")

def to_clip_from_csv(csv_path: str) -> camdkit.model.Clip:
  """Read ARRI camera metadata into a `Clip`. `path` is the path to a CSV
  file extracted using ARRI Meta Extract (AME)."""

  with open(csv_path, encoding="utf-8") as csvfile:
    csv_data = list(csv.DictReader(csvfile, dialect="excel-tab"))

    n_frames = len(csv_data)

    if n_frames <= 0:
      raise ValueError("No data")

    clip = camdkit.model.Clip()

    assert csv_data[0]["Lens Distance Unit"] == "Meter"

    clip.iso = int(csv_data[0]["Exposure Index ASA"])

    clip.duration = len(csv_data)/Fraction(csv_data[0]["Project FPS"])

    clip.camera_make = "ARRI"

    clip.camera_model = csv_data[0]["Camera Model"]

    clip.camera_serial_number = csv_data[0]["Camera Serial Number"]

    lens_model = csv_data[0]["Lens Model"]

    if lens_model.startswith("ARRI "):
      clip.lens_make = "ARRI"
      clip.lens_model = lens_model[5:]
    elif lens_model.startswith("Fujinon "):
        clip.lens_make = "Fujinon"
        clip.lens_model = lens_model[8:]
    else:
      clip.lens_model = lens_model

    clip.lens_serial_number = csv_data[0]["Lens Serial Number"]

    clip.capture_frame_rate = utils.guess_fps(Fraction(csv_data[0]["Project FPS"]))

    clip.shutter_angle = float(csv_data[0]["Shutter Angle"])

    clip.anamorphic_squeeze = Fraction(csv_data[0]["Lens Squeeze"])

    pix_dims = camdkit.model.Dimensions(
      width=int(csv_data[0]["Image Width"]),
      height=int(csv_data[0]["Image Height"])
    )
    pixel_pitch = _CAMERA_FAMILY_PIXEL_PITCH_MAP[(csv_data[0]["Camera Family"], int(pix_dims.width))]
    clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(
        width=pix_dims.width * pixel_pitch / 1000.0,
        height=pix_dims.height * pixel_pitch / 1000.0
      )

    focal_lengths = set([m["Lens Focal Length"] for m in csv_data])
    if len(focal_lengths) == 1:
      focal_length = float(focal_lengths.pop())
      clip.lens_nominal_focal_length = focal_length

    clip.lens_focus_distance = tuple(float(m["Lens Focus Distance"]) for m in csv_data)

    clip.lens_t_number = tuple(t_number_from_linear_iris_value(int(m["Lens Linear Iris"])) for m in csv_data)

  return clip


def to_clip_from_json(path: str) -> camdkit.model.Clip:
    """Read ARRI camera metadata into a `Clip`. `path` is the path to a CSV
    file extracted using the command-line ARRI Reference Tool (ART_CMD)."""
    with open(path, encoding="utf-8") as fp:
        obj:dict = json.load(fp)
        clip = camdkit.model.Clip()

        # camdkit does not yet handle nominal focal length for zoom lenses
        # clip.lens_nominal_focal_length = tuple()

        # camdkit does not currently track effective focal length
        # clip.lens_effective_focal_length = tuple()

        clip.lens_entrance_pupil_offset = tuple()
        clip.lens_focus_distance = tuple()
        clip.lens_t_number = tuple()

        def parse_rational_string(frac: str) -> StrictlyPositiveRational:
            temp = Fraction(frac)
            return StrictlyPositiveRational(temp.numerator, temp.denominator)

        def extract_clip_based_metadata():
            cbm_sets = obj.get('clipBasedMetadataSets', list())
            for cbm_set in cbm_sets:
                set_name = cbm_set.get('metadataSetName')
                set_payload = cbm_set.get('metadataSetPayload')
                match set_name:
                    case 'Sensor Device':
                        width = set_payload['sensorDimensions'].get('width')
                        height = set_payload['sensorDimensions'].get('height')
                        clip.active_sensor_physical_dimensions = PhysicalDimensions(width, height)
                    case 'Sensor State':
                        width = set_payload['acquisitionRect'].get('width')
                        height = set_payload['acquisitionRect'].get('height')
                        clip.active_sensor_resolution = SenselDimensions(width, height)

        def extract_descriptive_metadata():
            dm_sets = obj.get('descriptiveMetadataSets')
            for dm_set in dm_sets:
                set_name = dm_set.get('metadataSetName')
                set_payload = dm_set.get('metadataSetPayload')
                match set_name:
                    case 'Camera Device':
                        clip.camera_make = 'ARRI'
                        if 'cameraModel' in set_payload:
                            # It is possible that if ART_CMD was used on some incredibly old content,
                            # (pre-2011?) such content might not be carrying the camera mode.
                            if set_payload['cameraModel'].startswith('ARRI '):
                                clip.camera_model = set_payload['cameraModel'][5:]
                            else:
                                clip.camera_model = set_payload['cameraModel']
                        if 'cameraSerialNumber' in set_payload:
                            clip.camera_serial_number = set_payload['cameraSerialNumber']
                        if 'cameraSoftwarePackageName' in set_payload:
                            clip.camera_firmware = set_payload['cameraSoftwarePackageName']
                    case 'Lens Device':
                        if 'lensModel' in set_payload:
                            if set_payload['lensModel'].startswith('ARRI '):
                                clip.lens_make = 'ARRI'
                                clip.lens_model = set_payload['lensModel'][5:]
                            elif set_payload['lensModel'].startswith('Fujinon '):
                                clip.lens_make = 'Fujinon'
                                clip.lens_model = set_payload['lensModel'][8:]
                            else:
                                clip.lens_model = set_payload['lensModel']
                        if 'lensSerialNumber' in set_payload:
                            clip.lens_serial_number = set_payload['lensSerialNumber']
                        # n.b. lenses can have firmware versions but if this information is being
                        # presented to the camera, it is not currently (Nov 2025) being recorded
                        if 'lensSqueezeFactor' in set_payload:
                            factor: str = set_payload['lensSqueezeFactor']
                            if '/' not in factor:
                                # A bug in early releases of ART_CMD generated squeeze factors that
                                # were reduced to integers if the denominator divided evenly into
                                # the numerator; handle that special case.
                                clip.anamorphic_squeeze = StrictlyPositiveRational(int(factor), 1)
                            else:
                                clip.anamorphic_squeeze = parse_rational_string(factor)
                    case 'Slate Info':
                        if 'cameraIndex' in set_payload:
                            clip.camera_label = set_payload['cameraIndex']

        def extract_frame_based_metadata():
            first_frame: bool = True
            fbm = obj.get('frameBasedMetadata')
            for frame in fbm.get('frames'):
                for fbm_set_name, fbm_set_value in frame.get('frameBasedMetadataSets').items():
                    match fbm_set_name:
                        case 'Lens State':
                            lens_state = fbm_set_value
                            # n.b. at the moment ARRI does not provide pinhole focal length metadata
                            if 'lensFocalLength' in lens_state:
                                if first_frame:
                                    # camdkit does not record changing nominal focal length for zoom lenses,
                                    # arbitrarily this reader chooses the first frame's nominal focal length.
                                    # microns to millimeters
                                    nominal_focal_length: float = int(lens_state['lensFocalLength']) / 1000
                                    clip.lens_nominal_focal_length = nominal_focal_length
                                    first_frame = False
                            if 'lensEffectiveFocalLength' in lens_state:
                                # microns to ...millimeters, except camdkit doesn't carry effective focal length
                                pass
                                # effective_focal_length: float = int(lens_state['lensEffectiveFocalLength']) / 1000
                                # clip.lens_effective_focal_length += (effective_focal_length,)
                            if 'lensEntrancePupilOffset' in lens_state:
                                # sometimes when the EPO is not known, the camera (incorrectly) records a -1 value
                                if lens_state['lensEntrancePupilOffset'] != -1:
                                    # microns to meters
                                    entrance_pupil_offset: float = int(lens_state['lensEntrancePupilOffset']) / 1000000
                                    clip.lens_entrance_pupil_offset += (entrance_pupil_offset,)
                            if 'lensFocusDistanceMetric' in lens_state:
                                # microns to millimeters
                                focus_distance: float = int(lens_state['lensFocusDistanceMetric']) / 1000
                                clip.lens_focus_distance += (focus_distance,)
                            if 'lensIris' in lens_state:
                                linear_iris_value = int(lens_state['lensIris'])
                                clip.lens_t_number += (t_number_from_linear_iris_value(linear_iris_value),)
                        case 'Sensor State':
                            sensor_state = fbm_set_value
                            if 'sensorSampleRate' in sensor_state:
                                clip.capture_frame_rate = parse_rational_string(sensor_state['sensorSampleRate'])
                            if 'exposureIndex' in sensor_state:
                                clip.iso = sensor_state['exposureIndex']
                            if 'exposureTime' in sensor_state:
                                exp_time = parse_rational_string(sensor_state['exposureTime'])
                                samp_rate = parse_rational_string(sensor_state['sensorSampleRate'])
                                shutter_angle: float = 360.0 * (exp_time.num / exp_time.denom) / (samp_rate.denom / samp_rate.num)
                                clip.shutter_angle = shutter_angle
            num_frames = StrictlyPositiveRational(len(fbm.get('frames')), 1)
            clip.duration = num_frames * clip.capture_frame_rate

        extract_clip_based_metadata()
        extract_descriptive_metadata()
        extract_frame_based_metadata()
    return clip
