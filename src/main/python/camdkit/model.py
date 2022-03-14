#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2022, Sandflow Consulting LLC
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

"""Data model"""

import numbers

class Frame:
  """Metadata for a camera frame
  """
  def __init__(self):
    self._focal_length = None

  def set_focal_length(self, position: numbers.Real):
    if not isinstance(position, numbers.Real):
      raise TypeError("Focal length must be a real number")
    self._focal_length = position

  def get_focal_length(self) -> float:
    return self._focal_length

  focal_length = property(get_focal_length, set_focal_length)

  def serialize(self) -> dict:    
    return {
      "focal_length": self.get_focal_length()
    }

class Clip(list):
  """Metadata for a camera clip
  """
  def __init__(self, *args):
    self._iso = None
    super().__init__(args)

  def __setitem__(self, i, item):
    if not isinstance(item, Frame):
      raise TypeError("Item must be a Frame")
    super().__setitem__(i, item)

  def get_iso(self) -> int:
    return self._iso

  def set_iso(self, iso : int):
    if not isinstance(iso, int):
      raise TypeError("ISO must be an int")
    self._iso = iso

  def serialize(self) -> dict:
    return {
      "frames": tuple(map(lambda e: e.serialize(), self)),
      "iso": self.get_iso()
    }
