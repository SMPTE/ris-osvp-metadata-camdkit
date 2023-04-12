#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Cook data parser'''

import dataclasses

@dataclasses.dataclass
class CookeLensData:
  entrance_pupil_position: int
  aperture_value: int

def lens_data_from_binary_string(cooked_packed_bin_data: bytes) -> CookeLensData:
  sign = -1 if cooked_packed_bin_data[25] & 0b00100000 else 1
  entrance_pupil_position = sign * (((cooked_packed_bin_data[25] & 0b00001111) << 6) + (cooked_packed_bin_data[26] & 0b00111111))
  aperture_value = (((cooked_packed_bin_data[5] & 0b00111111) << 6) + (cooked_packed_bin_data[6] & 0b00111111))
  return CookeLensData(entrance_pupil_position=entrance_pupil_position, aperture_value=aperture_value)

@dataclasses.dataclass
class CookeFixedData:
  firmware_version_number: str

def fixed_data_from_string(cooked_fixed_data: str) -> CookeFixedData:
  return CookeFixedData(firmware_version_number=cooked_fixed_data[61:65])
