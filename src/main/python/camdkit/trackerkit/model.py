#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import numbers
import typing

from camdkit.framework import ParameterContainer
from camdkit.trackerkit.framework import Vector3, Vector3Parameter

class Translation(Vector3Parameter):
  """
  X,Y,Z in metres of camera sensor relative to stage origin.
  The Z axis points upwards and the coordinate system is right-handed.
  Y points in the forward camera direction (when pan, tilt and roll are zero).
  For example in an LED volume Y would point towards the centre of the LED wall and so X would point to camera-right.
  """
  canonical_name = "translation"
  units = "metres"


class Frame(ParameterContainer):
  """A frame of dynamic metadata from a camera tracking system.
  """
  translation: typing.Required[Vector3] = Translation()
  # TODO JU rest of the model!
