#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

""" F4 helper classes ported from C++ """

# TODO JU uncomment the frame assignment when the model is defined

import struct
from camdkit.trackerkit.model import Vector3, Transform, Frame

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
  ANGLE_FACTOR  = 1000
  LINEAR_FACTOR = 1000

class Timecode:
  hours = 0
  minutes = 0
  seconds = 0
  frames = 0
  frame_rate = 0.0

class F4AxisBlock:
  axis_id: int = 0
  axis_status: int = 0
  data_bits1: int = 0
  data_bits2: int = 0
  data_bits3: int = 0

  def to_timecode(self) -> Timecode:
     timecode = Timecode()
     match ((self._axisStatus >> 5) & 0b11):
       case 0b00:
         timecode.frame_rate = 24.0
       case 0b01:
         timecode.frame_rate = 25.0
       case 0b10:
         timecode.frame_rate = 30.0
       case 0b11:
         timecode.frame_rate = 60.0

     if timecode.frame_rate > 0.0:
       timecode.hours = (self.data_bits1 >> 2) % 24
       timecode.minutes = ((self.data_bits1 << 4) % 64) + ((self.data_bits2 >> 4) % 16)
       timecode.seconds = ((self.data_bits2 << 2) % 64) + ((self.data_bits3 >> 6) % 4)
       timecode.frames = self.data_bits3 % 64
     return timecode

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
  
  def _float_from_integer(integer):
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
       
  def get_tracking_frame(self) -> Frame:
    # TODO JU Complete once the model is defined
    frame = Frame()
    if self._initialised:
      frame.test = "Hello World!"
      frame.transform = Transform()
      frame.transform.translation = Vector3(0, 0, 0)
      frame.transform.rotation = Vector3(0, 0, 0)
      #frame.transform.name = f'Camera {self._packet.camera_id}'
      #frame.timing.packet_sequence_number = self.frame_number
      #frame.metadta.recording = (self._packet.status & (1 << 4)) != 0
      #frame.timing.synchronization.source = SynchronizationSource.genlock
      #frame.timing.synchronization.enabled = true
      #frame.timing.synchronization.locked = (self._packet.status & (1 << 5)) != 0
      for i in range(0, self._packet.axis_count):
        axis_block = self._packet.axis_block_list[i]
        match axis_block.axis_id:
          case F4.FIELD_ID_ROLL:
            frame.transform.rotation.z = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_TILT:
            frame.transform.rotation.y = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_PAN:
            frame.transform.rotation.x = self._axis_block_to_angle_linear_raw(axis_block, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_X:
            frame.transform.translation.x = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_Y:
            frame.transform.translation.y = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_HEIGHT:
            frame.transform.translation.z = self._axis_block_to_angle_linear_raw(axis_block, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_ENTRANCE_PUPIL:
            #frame.lens.entrance_pupil_distance = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_LENS_DISTORTION_K1:
            #frame.lens.distortion.radial[0] = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_LENS_DISTORTION_K2:
            #frame.lens.distortion.radial[1] = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_LENGTH_FX:
            #frame.lens.fov_h = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_LENGTH_FY:
            #frame.lens.fov_v = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_CX:
            #frame.lens.center_shift.cx = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_CY:
            #frame.lens.center_shift.cy = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCAL_DISTANCE:
            #frame.lens.inv_focal_d = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_APERTURE:
            #frame.lens.aperture = self._axis_block_to_lens_param(axis_block)
            pass
          case F4.FIELD_ID_FOCUS:
            #frame.lens.encoders.focus = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_ZOOM:
            #frame.lens.encoders.zoom = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_IRIS:
            #frame.lens.encoders.zoom = self._axis_block_to_lens_type(axis_block) / 65536.0
            pass
          case F4.FIELD_ID_TIMECODE:
            #frame.time.timecode = axis_block.to_timecode()
            pass
    return frame
  