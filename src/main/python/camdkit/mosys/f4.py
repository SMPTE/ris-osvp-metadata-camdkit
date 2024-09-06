#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

""" F4 helper classes ported from C++ """

import math
import struct
import uuid

from camdkit.framework import *
from camdkit.model import Clip, Synchronization

class F4:
  
  FIELD_ID_PAN                = 0x01
  FIELD_ID_TILT               = 0x02
  FIELD_ID_FOCUS              = 0x03
  FIELD_ID_ZOOM               = 0x04
  FIELD_ID_X                  = 0x05
  FIELD_ID_Y                  = 0x06
  FIELD_ID_HEIGHT             = 0x07
  FIELD_ID_IRIS               = 0x0D
  FIELD_ID_ROLL               = 0x13
  FIELD_ID_ENTRANCE_PUPIL     = 0x50
  FIELD_ID_LENS_DISTORTION_K1 = 0x51
  FIELD_ID_LENS_DISTORTION_K2 = 0x52
  FIELD_ID_FOCAL_LENGTH_FX    = 0x53
  FIELD_ID_CX                 = 0x54
  FIELD_ID_CY                 = 0x55
  FIELD_ID_FOCAL_DISTANCE     = 0X57
  FIELD_ID_FOCAL_LENGTH_FY    = 0x58
  FIELD_ID_APERTURE           = 0x60
  COMMAND_BYTE                = 0xf4
  FIELD_ID_TIMECODE           = 0xF8
  TRACKING_STATUS             = 0xF9

  ANGLE_FACTOR  = 1000
  LINEAR_FACTOR = 1000

  TRACKING_STATUS_STRINGS = [
    "Undefined",
    "Tracking",
    "Optical Good",
    "Optical Acceptable",
    "Optical Unreliable",
    "Optical Unstable",
    "Optical Lost",
    "Lost Too Few Stars",
    "Location Searching",
    "Busy or Waiting",
    "Busy Loading Map",
    "No Map Loaded",
    "Test Signal",
    "Mechanical Encoders Only",
    "I/O Error",
    "Internal Error"
  ]

class F4AxisBlock:
  axis_id: int = 0
  axis_status: int = 0
  data_bits1: int = 0
  data_bits2: int = 0
  data_bits3: int = 0

  def to_timecode(self) -> Timecode:
     match ((self.axis_status >> 5) & 0b11):
       case 0b00:
         format = TimecodeFormat(24)
       case 0b01:
         format = TimecodeFormat(25)
       case 0b10:
         format = TimecodeFormat(30)

     hours = (self.data_bits1 >> 2) % 24
     minutes = ((self.data_bits1 << 4) % 64) + ((self.data_bits2 >> 4) % 16)
     seconds = ((self.data_bits2 << 2) % 64) + ((self.data_bits3 >> 6) % 4)
     frames = self.data_bits3 % 64
     return Timecode(hours,minutes,seconds,frames,format)

class F4Packet:
  command_byte: int = 0
  camera_id: int = 0
  axis_count: int = 0
  status: int = 0
  checksum: int = 0
  size: int = 0
  axis_block_list: list[F4AxisBlock] = []

  def initialise(self, buffer: bytes) -> bool:
    if len(buffer) == 0:
      return False
    self.command_byte = buffer[0]
    if self.command_byte != F4.COMMAND_BYTE:
        return False
    self.camera_id = buffer[1]
    self.axis_count = buffer[2]
    if self.axis_count == 0:
        return False
    self.size = self.axis_count * 5 + 5;    
    if self.size > len(buffer):
        return False
    self.status = buffer[3]
    self.checksum = buffer[self.size - 1]
    return True

  def allocate_axis_blocks(self, buffer: bytes):
    if len(self.axis_block_list) != 0:
      self.axis_block_list.clear()

    for i in range(0, self.axis_count):
      axis_block = F4AxisBlock()
      offset = i * 5
      axis_block.axis_id = buffer[offset]
      axis_block.axis_status = buffer[offset + 1]
      axis_block.data_bits1 = buffer[offset + 2]
      axis_block.data_bits2 = buffer[offset + 3]
      axis_block.data_bits3 = buffer[offset + 4]
      self.axis_block_list.append(axis_block)
    

class F4PacketParser:
  _packet: F4Packet = F4Packet()
  _frame_number: int = 0
  _initialised: bool = False

  def _twos_comp(self, val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val
  
  def _float_from_integer(self, integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]
  
  def _three_bytes_to_int(self, first_byte: int, second_byte: int, third_byte: int) -> int:
    padded_first_byte = first_byte << 16
    padded_second_byte = second_byte << 8
    padded_third_byte = third_byte
    return padded_first_byte | padded_second_byte | padded_third_byte

  def _three_bytes_to_signed_int(self, first_byte: int, second_byte: int, third_byte: int) -> int:
    return self._twos_comp(self._three_bytes_to_int(first_byte, second_byte, third_byte), 24)
  
  def _four_bytes_to_float(self, first_byte: int, second_byte: int, third_byte: int, fourth_byte: int) -> float:
    padded_first_byte = first_byte << 24
    padded_second_byte = second_byte << 16
    padded_third_byte = third_byte << 8
    padded_fourth_byte = fourth_byte
    padded_int = padded_first_byte | padded_second_byte | padded_third_byte | padded_fourth_byte
    return self._float_from_integer(padded_int)

  def _axis_block_to_angle_linear_raw(self, axis_block: F4AxisBlock,  factor: int) -> int:
    return self._three_bytes_to_signed_int(axis_block.data_bits1, axis_block.data_bits2, axis_block.data_bits3) * (1.0 / factor)
  
  def _axis_block_to_lens_type(self, axis_block: F4AxisBlock) -> int:
    return (axis_block.data_bits2 << 8) | axis_block.data_bits3

  def _axis_block_to_lens_param(self, axis_block: F4AxisBlock) -> float:
    return self._four_bytes_to_float(axis_block.axis_status, axis_block.data_bits1, axis_block.data_bits2, axis_block.data_bits3)

  def _axis_block_to_status_string(self, axis_block: F4AxisBlock) -> str:
    detail = ((axis_block.data_bits2 >> 4) & 0xF)
    return F4.TRACKING_STATUS_STRINGS[detail]

  def _compute_f4_checksum(self, buffer: bytes) -> int:
      total: int = 0x40
      for i in range(0, self._packet.size - 1):
        total -= buffer[i]
      return total % 256

  def initialise(self, buffer: bytes) -> bool:
    if not self._packet.initialise(buffer):
        return False
    self._frame_number = self._packet.status % 16

    checksum = self._compute_f4_checksum(buffer)
    if checksum != self._packet.checksum:
        return False

    self._packet.allocate_axis_blocks(buffer[4:])

    self._initialised = True
    return True
       
  def get_tracking_frame(self) -> Clip:
    # Populates a Clip with a single frame of data of each parameter
    frame = Clip()
    if self._initialised:
      translation = Vector3(0,0,0)
      rotation = Rotator3(0,0,0)
      focus = iris = zoom = frequency = None
      k1 = k2 = cx = cy = fov_h = fov_v = 0.0
      frame.protocol = ("OpenTrackIO_0.1.0",)
      frame.sample_id = (uuid.uuid4().urn,)
      frame.device_recording = ((self._packet.status & (1 << 4)) != 0,)
      for i in range(0, self._packet.axis_count):
        axis_block = self._packet.axis_block_list[i]
        match axis_block.axis_id:
          case F4.FIELD_ID_ROLL:
            rotation.roll = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_TILT:
            rotation.tilt = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_PAN:
            rotation.pan = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_X:
            translation.x = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_Y:
            translation.y = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_HEIGHT:
            translation.z = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_ENTRANCE_PUPIL:
            frame.lens_entrance_pupil_distance = (Fraction(self._axis_block_to_lens_param(axis_block) * 1000),)
            pass
          case F4.FIELD_ID_LENS_DISTORTION_K1:
            k1 = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_LENS_DISTORTION_K2:
            k2 = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_LENGTH_FX:
            fov_h = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_LENGTH_FY:
            fov_v = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_CX:
            cx = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_CY:
            cy = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_DISTANCE:
            inv_focal_d = self._axis_block_to_lens_param(axis_block)
            # In mm
            frame.lens_focus_distance = (int(1000.0 / inv_focal_d),)
            pass
          case F4.FIELD_ID_APERTURE:
            f: float = self._axis_block_to_lens_param(axis_block)
            # Units are 0.001 e.g. F4.0 => 4000
            frame.lens_f_number = (round(f*1000.0),)
            pass
          case F4.FIELD_ID_FOCUS:
            focus = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_ZOOM:
            zoom = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_IRIS:
            iris = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_TIMECODE:
            frame.timing_timecode = (axis_block.to_timecode(),)
            frame_rate = frame.timing_timecode[0].format.frame_rate
            frame.timing_frame_rate = (frame_rate,)
            frequency = frame_rate
            pass
          case F4.TRACKING_STATUS:
            frame.device_status = (self._axis_block_to_status_string(axis_block),)
            pass
      
      frame.timing_mode = ("internal",)
      frame.timing_sequence_number = (self._frame_number,)
      syncEnabled = (self._packet.status & (1 << 5)) != 0
      sync = Synchronization(
        locked=syncEnabled,
        present=syncEnabled,
        source=SynchronizationSourceEnum.GENLOCK,
        frequency=frequency
      )
      frame.timing_synchronization = (sync,)
      # In this case there is only one transform
      transform = Transform(translation=translation, rotation=rotation)
      transform.name = f'Camera {self._packet.camera_id}'
      frame.transforms = ((transform,),)
      # Assuming a full frame 35mm active sensor 36x24mm
      # f = 36/[2*tand(FoV/2)]
      fov_radians = fov_h * math.pi / 180.0
      frame.lens_focal_length = (36.0 / (2.0 * math.tan(fov_radians/2.0)),)
      frame.lens_encoders = (Encoders(focus, iris, zoom),)
      frame.lens_distortion = (Distortion([k1, k2]),)
      frame.lens_perspective_shift = (PerspectiveShift(cx, cy),)
    return frame
  