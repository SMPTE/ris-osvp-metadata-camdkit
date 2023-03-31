#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) Society of Motion Picture and Television Engineers
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Sony Venice camera reader'''

import csv
import typing
import re
import xml.etree.ElementTree as ET
from fractions import Fraction

import camdkit.model
import camdkit.utils as utils

NS_PREFIXES = {
  "nrt" : "urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.10"
}

def find_value(doc: ET.ElementTree, item_name: str) -> typing.Optional[str]:
  elem = doc.find(f".//nrt:Item[@name='{item_name}']" , namespaces=NS_PREFIXES)

  if elem is None:
    return None

  attr = elem.get("value")

  if attr is None:
    return None

  return attr

def get_attribute_value(element: ET.Element, attr_name: str) -> typing.Optional[str]:
  if element is None or attr_name is None:
    return None
  v = element.get(attr_name)
  return None if v is None or v == "" else v.strip()

def find_camera_info(doc: ET.ElementTree) -> typing.Tuple[str]:
  elem = doc.find(".//nrt:Camera" , namespaces=NS_PREFIXES)

  if elem is None:
    return (None, None, None, None)

  camera_make = get_attribute_value(elem, "manufacturer")
  camera_model = get_attribute_value(elem, "modelName")
  camera_sn = get_attribute_value(elem, "serialNo")

  elem = elem.find(".//nrt:Element[@hardware='Main-Board']" , namespaces=NS_PREFIXES)

  camera_firmware = get_attribute_value(elem, "software")

  return (camera_make, camera_model, camera_sn, camera_firmware)

def find_lens_info(doc: ET.ElementTree) -> typing.Tuple[str]:
  elem = doc.find(".//nrt:Lens" , namespaces=NS_PREFIXES)

  lens_make = get_attribute_value(elem, "software")
  lens_model = get_attribute_value(elem, "modelName")

  lens_sn = find_value(doc, "LensAttributes")

  return (lens_make, lens_model, lens_sn)


def find_fps(doc: ET.ElementTree)  -> typing.Optional[Fraction]:
  elem = doc.find(".//nrt:VideoFrame" , namespaces=NS_PREFIXES)

  if elem is None:
    return None

  attr = elem.get("captureFps")

  if attr is None:
    return None

  fps_match = re.fullmatch("([0-9.]+)[a-zA-Z]", attr)

  if fps_match is None:
    return None

  return Fraction(fps_match.group(1))

def find_duration(doc: ET.ElementTree) -> typing.Optional[int]:
  try:
    elem = doc.find(".//nrt:Duration" , namespaces=NS_PREFIXES)

    if elem is None:
      return None

    attr = elem.get("value")

    if attr is None:
      return None

    return int(attr)

  except TypeError:
    return None

def find_px_dims(doc: ET.ElementTree) -> typing.Optional[camdkit.model.Dimensions]:
  try:
    elem = doc.find(".//nrt:VideoLayout" , namespaces=NS_PREFIXES)

    if elem is None:
      return None

    h_pixels = int(elem.get("numOfVerticalLine"))

    v_pixels = int(elem.get("pixel"))

    return camdkit.model.Dimensions(height=h_pixels, width=v_pixels)

  except TypeError:
    return None

def t_number_from_frac_stop(frac_stop_str: str) -> typing.Optional[float]:

  m = re.fullmatch("T ([0-9]+)(?: ([0-9]/10))?", frac_stop_str)

  if m is None:
    return None

  aperture_value = int(m.group(1))

  if m.group(2) is not None:
    aperture_value += Fraction(m.group(2))

  return 2**(float(aperture_value) / 2)

def int_or_none(value: typing.Optional[str]) -> typing.Optional[int]:
  return int(value) if value is not None else None

def to_clip(static_file: typing.IO, dynamic_file: typing.IO) -> camdkit.model.Clip:
  """Read Sony Venice camera metadata into a `Clip`.
  `static_file`: Static camera metadata. XML file.
  `dynamic_file`: Per-frame camera metadata. CSV file
  """

  # read clip metadata
  clip = camdkit.model.Clip()

  clip_metadata = ET.parse(static_file)

  clip.iso = int_or_none(find_value(clip_metadata, "ISOSensitivity"))

  clip.lens_serial_number = find_value(clip_metadata, "LensAttributes")

  clip.camera_make, clip.camera_model, clip.camera_serial_number, clip.camera_firmware = find_camera_info(clip_metadata)

  clip.lens_make, clip.lens_model, clip.lens_serial_number = find_lens_info(clip_metadata)

  # lens_firmware not supported

  shutter_angle = find_value(clip_metadata, "ShutterSpeedAngle")
  clip.shutter_angle = int(shutter_angle) * 10 if shutter_angle is not None else None

  pixel_aspect_ratio = find_value(clip_metadata, "PixelAspectRatio")
  if pixel_aspect_ratio is not None:
    m = re.fullmatch("([0-9]+):([0-9]+)", pixel_aspect_ratio)
    if m is not None:
      clip.anamorphic_squeeze = round(float(m.group(1)) / float(m.group(2)) * 100.0)

  clip_fps = find_fps(clip_metadata)

  if clip_fps is None:
    raise ValueError("No valid capture fps found")

  clip.capture_fps = utils.guess_fps(clip_fps)

  n_frames = find_duration(clip_metadata)

  if n_frames is None:
    raise ValueError("No valid duration found")

  pixel_pitch = 22800 / 3840 # page 5 of "VENICE v6 Ops.pdf"
  pix_dims = find_px_dims(clip_metadata)
  clip.active_sensor_physical_dimensions = camdkit.model.Dimensions(
        width=round(pix_dims.width * pixel_pitch),
        height=round(pix_dims.height * pixel_pitch)
      )

  # read frame metadata
  csv_data = list(csv.DictReader(dynamic_file))

  if len(csv_data) != n_frames:
    raise ValueError(f"Inconsistent frame count between header {n_frames} and frame {len(csv_data)} files")

  clip.duration = len(csv_data)/clip_fps

  clip.focal_length = tuple(int(m["Focal Length (mm)"]) for m in csv_data)

  clip.focal_position = tuple(round(float(m["Focus Distance (ft)"]) * 12 * 25.4) for m in csv_data)

  # TODO: clip.entrance_pupil_position

  clip.t_number = tuple(round(t_number_from_frac_stop(m["Aperture"]) * 1000) for m in csv_data)

  return clip
