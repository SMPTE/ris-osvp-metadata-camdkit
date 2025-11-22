#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""ARRI camera reader tests"""

import unittest

from pydantic import BaseModel

import camdkit.arri.reader
import camdkit.model
from camdkit.numeric_types import StrictlyPositiveRational


class JSONTestCaseData(BaseModel):
    input: str
    iso: int
    physical_height: float
    physical_width: float
    camera_make: str
    camera_model: str
    camera_serial_number: str
    camera_firmware: str
    camera_label: str
    capture_frame_rate: StrictlyPositiveRational
    # Lenses without any LDS or /i capabilities and with no mechanism for conveying
    # some basic attributes of lens state may produce values of 'None' for the next
    # several items of metadata
    lens_make: str | None
    lens_model: str | None
    lens_serial_number: str | None
    lens_nominal_focal_length: float | None
    lens_focus_distance: float | None
    lens_t_number: float | None
    lens_entrance_pupil_offset: float | None
    anamorphic_squeeze: StrictlyPositiveRational
    shutter_angle: float


JSON_TEST_CASES_DATA = {
    'alexa_35_xt': {
        'input': 'DW0001C001_251020_111956_c1I7H.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 19.22,
        'physical_width': 27.99,
        'camera_make': 'ARRI',
        'camera_model': 'ALEXA 35',
        'camera_serial_number': '70253',
        'camera_firmware': '5.01.00',
        'camera_label': 'DW',
        'lens_make': 'ARRI',
        'lens_model': 'SZ45-135 T2.8',
        'lens_serial_number': '137384',
        'lens_nominal_focal_length': 67.885,
        'lens_focus_distance': 4.021,
        'lens_t_number': 5.641,
        'lens_entrance_pupil_offset': 0.230804,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_265': {
        'input': 'A_0003C035_250922_110738_a0V3O.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 25.58,
        'physical_width': 54.12,
        'camera_make': 'ARRI',
        'camera_model': 'ALEXA 265',
        'camera_serial_number': '40308',
        'camera_firmware': '3.00.03',
        'camera_label': 'A_',
        'lens_make': None,
        'lens_model': '50-110mm',
        'lens_serial_number': '17025',
        'lens_nominal_focal_length': None,
        'lens_focus_distance': None,
        'lens_t_number': None,
        'lens_entrance_pupil_offset': None,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_35': {
        'input': 'A_0005C002_221019_172236_a12SO.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 19.22,
        'physical_width': 27.99,
        'camera_make': 'ARRI',
        'camera_model': 'ALEXA 35',
        'camera_serial_number': '50280',
        'camera_firmware': '1.00.03',
        'camera_label': 'A_',
        'lens_make': 'ARRI',
        'lens_model': 'SP58 T1.8',
        'lens_serial_number': '63541',
        'lens_nominal_focal_length': 58.0,
        'lens_focus_distance': 2.395,
        'lens_t_number': 3.615,
        'lens_entrance_pupil_offset': 0.14408,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_mini_lf': {
        'input': 'A001C001_190715_RN80.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 25.54,
        'physical_width': 36.7,
        'camera_make': 'ARRI',
        'camera_model': 'ALEXA Mini LF',
        'camera_serial_number': '30120',
        'camera_firmware': '6.00.03',
        'camera_label': 'A',
        'lens_make': 'ARRI',
        'lens_model': 'SP150 T1.8',
        'lens_serial_number': '12222',
        'lens_nominal_focal_length': 150.0,
        'lens_focus_distance': 1.749,
        'lens_t_number': 1.988,
        # n.b. note that this entrance pupil offset appears to be hallucinated by the
        # ARRI command-line metadata export tool; there is likely no actual
        # Entrance Pupil Offset Item in the original MXF file, as that Item is
        # defined to be optional in SMPTE RDD 55
        'lens_entrance_pupil_offset': -1e-6,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_lf': {
        'input': 'B003C003_180327_R1ZA.json',
        'iso': 400,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 0.0, # bug present in ART_CMD 4.0.1 and perhaps other releases
        'physical_width': 0.0,  # bug present in ART_CMD 4.0.1 and perhaps other releases
        'camera_make': 'ARRI',
        'camera_model': 'Alexa LF Plus W',
        'camera_serial_number': '2566',
        'camera_firmware': 'AlexaLF_2.0:41017',
        'camera_label': 'B',
        'lens_make': 'ARRI',
        'lens_model': 'SP40 T1.8',
        'lens_serial_number': '2',
        'lens_nominal_focal_length': 40.0,
        'lens_focus_distance': 4.844,
        'lens_t_number': 1.782,
        # n.b. note that this entrance pupil offset appears to be hallucinated by the
        # ARRI command-line metadata export tool; there is likely no actual
        # Entrance Pupil Offset Item in the original MXF file, as that Item is optional
        'lens_entrance_pupil_offset': None,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_mini': {
        'input': 'M002C003_161207_R00H.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 18.17,
        'physical_width': 28.25,
        'camera_make': 'ARRI',
        'camera_model': 'ALEXA Mini',
        'camera_serial_number': '20017',
        'camera_firmware': '4.02.05',
        'camera_label': 'M',
        'lens_make': None,
        'lens_model': None,
        'lens_serial_number': '0', # check in GUI
        'lens_nominal_focal_length': None,
        'lens_focus_distance': None,
        'lens_t_number': None,
        # EPO was '-1' in file, almost certainly to mean 'unknown'
        'lens_entrance_pupil_offset': None,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 172.8
    },
    'alexa_sxt': {
        'input': 'S002C001_161207_R6ZJ.json',
        'iso': 800,
        'capture_frame_rate': StrictlyPositiveRational(24, 1),
        'physical_height': 0.0, # not recorded and not computed by extraction tool
        'physical_width': 0.0, # same
        'camera_make': 'ARRI',
        'camera_model': 'Alexa Plus 4:3 SXT',
        'camera_serial_number': '9055',
        'camera_firmware': 'AlexaSXT_1.0:36225',
        'camera_label': 'S',
        'lens_make': 'Fujinon',
        'lens_model': 'Alura AZ15.5-45 T2.8',
        'lens_serial_number': '23308',
        'lens_nominal_focal_length': 26.266,
        'lens_focus_distance': 0.78,
        'lens_t_number': 6.216,
        'lens_entrance_pupil_offset': None,
        'anamorphic_squeeze': StrictlyPositiveRational(1, 1),
        'shutter_angle': 22.499
    }
}


class ARRIReaderTest(unittest.TestCase):

  def test_reader_csv(self):
    clip = camdkit.arri.reader.to_clip("src/test/resources/arri/B001C001_180327_R1ZA.mov.csv")

    self.assertEqual(clip.iso, 400)

    self.assertEqual(
      clip.active_sensor_physical_dimensions,
      camdkit.model.Dimensions(width=316.8, height=178.2)
    )

    self.assertEqual(clip.camera_make, "ARRI")

    self.assertEqual(clip.camera_model, "Alexa LF Plus W")

    self.assertEqual(clip.camera_serial_number, "2566")

    self.assertEqual(clip.lens_make, "ARRI")

    self.assertEqual(clip.lens_model, "SP40 T1.8")

    self.assertEqual(clip.lens_serial_number, "2")

    self.assertEqual(clip.capture_frame_rate, 24)

    self.assertEqual(clip.lens_nominal_focal_length, 40)

    self.assertEqual(clip.lens_focus_distance[0], 4.812)

    self.assertEqual(clip.anamorphic_squeeze, 1)

    self.assertEqual(round(clip.lens_t_number[0] * 1000), 1782)

    self.assertEqual(clip.shutter_angle, 172.8)

  def test_reader_json(self):
      for value in JSON_TEST_CASES_DATA.values():
          self.per_model_test_reader_json(JSONTestCaseData(**value))

  def per_model_test_reader_json(self, reference: JSONTestCaseData):
      clip = camdkit.arri.reader.to_clip(f"src/test/resources/arri/{reference.input}")

      self.assertEqual(clip.iso, reference.iso)

      # in some cases, when the physical height is not known, the ARRI JSON
      # exporter inserts a value of 0.0 instead of omitting the height
      if clip.active_sensor_physical_dimensions.height != 0.0:
          self.assertAlmostEqual(clip.active_sensor_physical_dimensions.height,
                                 reference.physical_height, 2)

      # in some cases, when the physical width is not known, the ARRI JSON
      # exporter inserts a value of 0.0 instead of omitting the width
      if clip.active_sensor_physical_dimensions.width != 0.0:
          self.assertAlmostEqual(clip.active_sensor_physical_dimensions.width,
                                 reference.physical_width, 2)

      self.assertEqual(clip.camera_make, reference.camera_make)

      self.assertEqual(clip.camera_model, reference.camera_model)

      self.assertEqual(clip.camera_serial_number, reference.camera_serial_number)

      self.assertEqual(clip.camera_firmware, reference.camera_firmware)

      self.assertEqual(clip.camera_label, reference.camera_label)

      self.assertEqual(clip.lens_make, reference.lens_make)

      self.assertEqual(clip.lens_model, reference.lens_model)

      self.assertEqual(clip.lens_serial_number, reference.lens_serial_number)

      self.assertEqual(clip.capture_frame_rate, reference.capture_frame_rate)

      self.assertAlmostEqual(clip.lens_nominal_focal_length,
                             reference.lens_nominal_focal_length, 1)

      if clip.lens_focus_distance:
          self.assertAlmostEqual(clip.lens_focus_distance[0],
                                 reference.lens_focus_distance, 3)

      if clip.lens_entrance_pupil_offset:
          self.assertAlmostEqual(clip.lens_entrance_pupil_offset[0],
                                 reference.lens_entrance_pupil_offset, 5)

      self.assertEqual(clip.anamorphic_squeeze, reference.anamorphic_squeeze)

      # As an example: ARRI GUI says the clip is 2.8 + 7/10
      # https://scantips.com/lights/tenths.pdf has 2.828 + 7/10 at 3.605
      # Given rounding in the "7/10" part, a calculated 3.615 seems reasonable
      if clip.lens_t_number:
          self.assertAlmostEqual(clip.lens_t_number[0], reference.lens_t_number, 3)

      self.assertAlmostEqual(clip.shutter_angle, reference.shutter_angle, 1)

  def test_linear_iris_value(self):
    self.assertEqual(round(camdkit.arri.reader.t_number_from_linear_iris_value(6000) * 1000), 5657)
