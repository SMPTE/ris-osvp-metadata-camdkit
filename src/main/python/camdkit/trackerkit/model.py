#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import numbers
import typing

from camdkit.framework import ParameterContainer, StringParameter, Sampling, TransformsParameter
from camdkit.model import FStop

class Transforms(TransformsParameter):
  """List of transforms"""
  canonical_name = "transforms"
  units = "metres / degrees"

class TestString(StringParameter):
  """Test string"""
  canonical_name = "testString"
  sampling = Sampling.REGULAR
  units = None

class TrackingClip(ParameterContainer):
  """
  Dynamic metadata from e.g. a camera tracking system. Each frame of data for each
  parameter is stored in the parameter's tuple
  """
  # TODO JU rest of the model!
  test: typing.Optional[typing.Tuple[StringParameter]] = TestString()
  transforms: typing.Optional[typing.Tuple[TransformsParameter]] = Transforms()
  f_number: typing.Optional[typing.Tuple[numbers.Integral]] = FStop()

  def append(self, clip):
    "Helper to add another clip's parameters to this clip's tuples"
    if not isinstance(clip, TrackingClip):
      raise ValueError
    self.test += clip.test
    self.transforms += clip.transforms
    # Optional parameters:
    if clip.f_number != None:
      self.f_number += clip.f_number

  def __getitem__(self, i):
    "Helper to convert to a static frame for JSON output"
    clip = TrackingClip()
    clip.test = self.test[i]

    clip.transforms = self.transforms[i]
    # Optional parameters:
    if self.f_number != None:
      clip.f_number = self.f_number[i]
    return clip

  def __iter__(self):
    self.i = 0
    self._set_static()
    return self
  
  def __next__(self):
    self.i += 1
    if self.transforms == None or self.i >= len(self.transforms):
      self._set_regular()
      raise StopIteration
    return self[self.i]
  
  def _set_static(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.STATIC 

  def _set_regular(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.REGULAR
