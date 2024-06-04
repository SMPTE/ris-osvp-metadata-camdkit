#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import typing

from camdkit.framework import ParameterContainer, StringParameter, Sampling
from camdkit.trackerkit.framework import Vector3, TranslationParameter, RotationParameter, ParameterSection

class Translation(TranslationParameter):
  """
  X,Y,Z in metres of camera sensor relative to stage origin.
  The Z axis points upwards and the coordinate system is right-handed.
  Y points in the forward camera direction (when pan, tilt and roll are zero).
  For example in an LED volume Y would point towards the centre of the LED wall and so X would point to camera-right.
  """
  canonical_name = "translation"
  units = "metres"

class Rotation(RotationParameter):
  """
  Rotation expressed as euler angles in degrees of the camera sensor relative to stage origin
  Rotations are intrinsic and are measured around the axes ZXY, commonly referred to as [pan, tilt, roll]
  Notes on Euler angles:
  Euler angles are human readable and unlike quarternions, provide the ability for cycles (with angles >360 or <0 degrees).
  Where a tracking system is providing the pose of a virtual camera, gimbal lock does not present the physical challenges of a robotic system.
  Conversion to and from quarternions is trivial with an acceptable loss of precision
  """
  canonical_name = "rotation"
  units = "degrees"

class Transform(ParameterSection):
  """Transform section"""
  canonical_name = "transform"

  translation: typing.Optional[Vector3] = Translation()
  rotation: typing.Optional[Vector3] = Rotation()


class TestString(StringParameter):
  """Test string"""
  canonical_name = "test_string"
  sampling = Sampling.STATIC
  units = None

class Frame(ParameterContainer):
  """
  A frame of dynamic metadata from e.g. a camera tracking system.
  """
  # TODO JU rest of the model!
  test: typing.Optional[StringParameter] = TestString()
  transform: typing.Optional[ParameterSection] = Transform()
