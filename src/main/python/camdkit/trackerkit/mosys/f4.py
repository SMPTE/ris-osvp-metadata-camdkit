#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

""" F4 helper classes ported from C++ """

# TODO JU complete this port from C++, currently only transform is supported

from camdkit.trackerkit.model import Vector3, Transform, Frame

class F4:
  
#define MSG_MOD_EX_POS4            0xF4
#define CAM_ID_OFFSET            1      // Pos Camera Id
#define NAX_ID_OFFSET            2
#define CNTST_OFFSET            3
#define HEADER_LENGTH            4

#ifndef MOSYS_ROTATIONAL_CNV
#define MOSYS_ROTATIONAL_CNV     0.36  // 1000000 ticks/rev -> 1/1000 degree resolution
#endif
#define MOSYS_LINEAR_CNV        1      // 1/100 of mm resolution

  FIELD_ID_PAN = 0x01
  FIELD_ID_TILT = 0x02
#define F4_FIELD_ID_FOCUS                  0x03
#define F4_FIELD_ID_ZOOM                   0x04
  FIELD_ID_X = 0x05
  FIELD_ID_Y = 0x06
  FIELD_ID_HEIGHT = 0x07
#define F4_FIELD_ID_CPAN                   0x08
#define F4_FIELD_ID_CTILT                  0x09
#define F4_FIELD_ID_TURNT                  0x0A
#define F4_FIELD_ID_CRANEX                 0x0B
#define F4_FIELD_ID_ORIENT                 0x0C
#define F4_FIELD_ID_IRIS                   0x0D
#define F4_FIELD_ID_DIGIFOCUS              0x0E
#define F4_FIELD_ID_DIGIZOOM               0x0F
#define F4_FIELD_ID_DIGIIRIS               0x10
#define F4_FIELD_ID_STRINGX                0x11
#define F4_FIELD_ID_STRINGY                0x12
  FIELD_ID_ROLL = 0x13
#define F4_FIELD_ID_HEAD_Y                 0x14
#define F4_FIELD_ID_HEAD_Z                 0x15


#define F4_FIELD_ID_RAWPAN                 0x32
#define F4_FIELD_ID_RAWTILT                0x33
#define F4_FIELD_ID_RAWROLL                0x34
#define F4_FIELD_ID_RAWJIB                 0x35
#define F4_FIELD_ID_RAWTURN                0x36
#define F4_FIELD_ID_RAWTRACK               0x37
#define F4_FIELD_ID_RAWTELE                0x38
#define F4_FIELD_ID_RAWELEV                0x39

#define F4_FIELD_ID_ENTRANCE_PUPIL         0x50
#define F4_FIELD_ID_LENS_DISTORTION_K1     0x51
#define F4_FIELD_ID_LENS_DISTORTION_K2     0x52
#define F4_FIELD_ID_FOCAL_LENGTH_FX        0x53
#define F4_FIELD_ID_CX                     0x54
#define F4_FIELD_ID_CY                     0x55
#define F4_FIELD_ID_VIRTUAL_FX             0X56
#define F4_FIELD_ID_FOCAL_DISTANCE         0X57
#define F4_FIELD_ID_FOCAL_LENGTH_FY        0x58
#define F4_FIELD_ID_VIRTUAL_FY             0X59
#define F4_FIELD_ID_APERTURE               0x60

#define F4_FIELD_ID_TIMECODE               0xF8

#define F4_FIELD_ID_GATEWAY_BUILD_VERSION  0xFA
#define F4_FIELD_ID_GATEWAY_BUILD_DATE     0xFB
#define F4_FIELD_ID_AXIS_DATA_INFO         0xFC
#define F4_FIELD_ID_NETWORK_STATUS_INFO    0xFD
#define F4_FIELD_ID_PACKET_TIMING_INFO     0xFE
#define F4_FIELD_ID_GENLOCK_INFO           0xFF

#define F4_OUTPUT_ENABLE_OFF            false
#define F4_OUTPUT_ENABLE_ON             true
#define F4_OUTPUT_ENABLE_ONCE           2

  COMMAND_BYTE = 0xf4

#define F4_PACKET_SIZE_MAX   2048


#define F4_STARTRACKER_ID    0xF7
#define F4_TRACKING_STATUS   0xF9

#define F4_TRACKING_STATUS_UNDEFINED            0
#define F4_TRACKING_STATUS_TRACKING             1 
#define F4_TRACKING_STATUS_OPTICAL_GOOD         2
#define F4_TRACKING_STATUS_OPTICAL_ACCEPTABLE   3
#define F4_TRACKING_STATUS_OPTICAL_UNRELIABLE   4
#define F4_TRACKING_STATUS_OPTICAL_UNSTABLE     5
#define F4_TRACKING_STATUS_OPTICAL_LOST         6
#define F4_TRACKING_STATUS_LOST_TOO_FEW_STARS   7
#define F4_TRACKING_STATUS_LOC_SEARCHING        8
#define F4_TRACKING_STATUS_BUSY_OR_WAITING      9
#define F4_TRACKING_STATUS_BUSY_LOADING_MAP     10
#define F4_TRACKING_STATUS_NO_MAP_LOADED        11
#define F4_TRACKING_STATUS_TEST_SIGNAL          12
#define F4_TRACKING_STATUS_MECH_ENC_ONLY        13
#define F4_TRACKING_STATUS_IO_ERROR             14
#define F4_TRACKING_STATUS_INTERNAL_ERROR       15

  ANGLE_FACTOR = 1000
  LINEAR_FACTOR = 1000

# class Timecode:
#   _hours = 0
#   _minutes = 0
#   _seconds = 0
#   _frames = 0
#   _frame_rate = 0.0

class F4AxisBlock:
  _axisID: int = 0
  _axisStatus: int = 0
  _DataBits1: int = 0
  _DataBits2: int = 0
  _DataBits3: int = 0

#   def toTimecode(self) -> Timecode:
#     timecode = Timecode()
#     match ((self._axisStatus >> 5) & 0b11):
#       case 0b00:
#         timecode.m_frameRate = 24.0
#       case 0b01:
#         timecode.m_frameRate = 25.0
#       case 0b10:
#         timecode.m_frameRate = 30.0
#       case 0b11:
#         timecode.m_frameRate = 60.0

#     if timecode.m_frameRate > 0.0:
#       timecode.hours = (self._DataBits1 >> 2) % 24
#       timecode.minutes = ((self._DataBits1 << 4) % 64) + ((self._DataBits2 >> 4) % 16)
#       timecode.seconds = ((self._DataBits2 << 2) % 64) + ((self._DataBits3 >> 6) % 4)
#       timecode.frames = self._DataBits3 % 64
#     return timecode

class F4Packet:
  _commandByte: int = 0
  _cameraID: int = 0
  _axisCount: int = 0
  _status: int = 0
  _checkSum: int = 0
  _size: int = 0
  _axisBlockList: list[F4AxisBlock] = []

  def initialise(self, buffer: bytes) -> bool:
    if len(buffer) == 0:
      return False
    self._commandByte = buffer[0]
    if self._commandByte != F4.COMMAND_BYTE:
        return False
    self._cameraID = buffer[1]
    self._axisCount = buffer[2]
    if self._axisCount == 0:
        return False
    self._size = self._axisCount * 5 + 5;    
    if self._size > len(buffer):
        return False
    self._status = buffer[3]
    self._checkSum = buffer[self._size - 1]
    return True

  def allocateAxisBlocks(self, buffer: bytes):
    if len(self._axisBlockList) != 0:
      self._axisBlockList.clear()

    for i in range(0, self._axisCount):
      axisBlock = F4AxisBlock()
      offset = i * 5
      axisBlock._axisID = buffer[offset]
      axisBlock._axisStatus = buffer[offset + 1]
      axisBlock._DataBits1 = buffer[offset + 2]
      axisBlock._DataBits2 = buffer[offset + 3]
      axisBlock._DataBits3 = buffer[offset + 4]
      self._axisBlockList.append(axisBlock)
    

class F4PacketParser:
  _packet: F4Packet = F4Packet()
  _frameNumber: int = 0
  _initialised: bool = False

  def _twos_comp(self, val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val   
  
  def _threeBytesToInt(self, firstByte: int, secondByte: int, thirdByte: int) -> int:
    paddedFirstByte = firstByte << 16
    paddedSecondByte = secondByte << 8
    paddedThirdByte = thirdByte
    return paddedFirstByte | paddedSecondByte | paddedThirdByte

  def _threeBytesToSignedInt(self, firstByte: int, secondByte: int, thirdByte: int) -> int:
    return self._twos_comp(self._threeBytesToInt(firstByte, secondByte, thirdByte), 24)
  
  def _axisBlockToAngleLinearRaw(self, axisBlock: F4AxisBlock,  factor: int) -> int:
    return self._threeBytesToSignedInt(axisBlock._DataBits1, axisBlock._DataBits2, axisBlock._DataBits3) * (1.0 / factor)
  
  # TODO JU Complete the port from C++
  #void axisBlockToLensType(const F4AxisBlock& axisBlock, uint16_t& value);
  #void axisBlockToLensParam(const F4AxisBlock& axisBlock, float& value);

  def _computeF4CheckSum(self, buffer: bytes) -> int:
      Total: int = 0x40
      for i in range(0, self._packet._size - 1):
        Total -= buffer[i]
      return Total % 256

  def initialise(self, buffer: bytes) -> bool:
    if not self._packet.initialise(buffer):
        return False
    self._frameNumber = self._packet._status % 16

    checkSum = self._computeF4CheckSum(buffer)
    if checkSum != self._packet._checkSum:
        return False

    self._packet.allocateAxisBlocks(buffer[4:])

    self._initialised = True
    return True
       
  def getTrackingFrame(self) -> Frame:

    # TODO JU: For now just parse transform
    frame = Frame()
    if self._initialised:
      frame.test = "Hello World!"
      frame.transform = Transform()
      frame.transform.translation = Vector3(0, 0, 0)
      frame.transform.rotation = Vector3(0, 0, 0)
      # TODO JU Complete the port from C++
      #frame.cameraID = self._packet.cameraID;
      #frame.frameProgressiveCounter = self._frameNumber;
      #frame.recording = (self._packet.status & (1 << 4)) != 0;
      #frame.genlocked = (self._packet.status & (1 << 5)) != 0;
      #frame.oddField = (self._packet.status & (1 << 6)) != 0;
      for i in range(0, self._packet._axisCount):
        axisBlock = self._packet._axisBlockList[i]
        match axisBlock._axisID:
          case F4.FIELD_ID_ROLL:
            frame.transform.rotation.z = self._axisBlockToAngleLinearRaw(axisBlock, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_TILT:
            frame.transform.rotation.y = self._axisBlockToAngleLinearRaw(axisBlock, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_PAN:
            frame.transform.rotation.x = self._axisBlockToAngleLinearRaw(axisBlock, F4.ANGLE_FACTOR)
          case F4.FIELD_ID_X:
            frame.transform.translation.x = self._axisBlockToAngleLinearRaw(axisBlock, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_Y:
            frame.transform.translation.y = self._axisBlockToAngleLinearRaw(axisBlock, F4.LINEAR_FACTOR)
          case F4.FIELD_ID_HEIGHT:
            frame.transform.translation.z = self._axisBlockToAngleLinearRaw(axisBlock, F4.LINEAR_FACTOR)
    return frame

# TODO JU Complete the port from C++

# frame.settings.addAxis(axisBlock.m_axisID)
# switch (axisBlock.m_axisID)
# {

#     case F4_FIELD_ID_ROLL:
#         // Roll
#         axisBlockToAngleLinearRaw(axisBlock, frame.rotation.roll, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_TILT:
#         // Pitch
#         axisBlockToAngleLinearRaw(axisBlock, frame.rotation.pitch, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_PAN:
#         // Yaw
#         axisBlockToAngleLinearRaw(axisBlock, frame.rotation.yaw, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_X:
#         axisBlockToAngleLinearRaw(axisBlock, frame.translation.x, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_Y:
#         axisBlockToAngleLinearRaw(axisBlock, frame.translation.y, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_HEIGHT:
#         axisBlockToAngleLinearRaw(axisBlock, frame.translation.z, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_ENTRANCE_PUPIL:
#         axisBlockToLensParam(axisBlock, frame.lens.entrancePupil);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_LENS_DISTORTION_K1:
#         axisBlockToLensParam(axisBlock, frame.lens.K1);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_LENS_DISTORTION_K2:
#         axisBlockToLensParam(axisBlock, frame.lens.K2);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_FOCAL_LENGTH_FX:
#         axisBlockToLensParam(axisBlock, frame.lens.distortedFx);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_FOCAL_LENGTH_FY:
#         axisBlockToLensParam(axisBlock, frame.lens.distortedFy);
#         frame.lens.hasData = true;
#         frame.lens.P1P2Valid = true; // P1P2Valid temporarily used as an indicator whether ST sends fy
#         break;
#     case F4_FIELD_ID_CX:
#         axisBlockToLensParam(axisBlock, frame.lens.cx);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_CY:
#         axisBlockToLensParam(axisBlock, frame.lens.cy);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_VIRTUAL_FX:
#         axisBlockToLensParam(axisBlock, frame.lens.undistortedFx);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_VIRTUAL_FY:
#         axisBlockToLensParam(axisBlock, frame.lens.virtualCameraFy);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_FOCAL_DISTANCE:
#         axisBlockToLensParam(axisBlock, frame.lens.recipFocalDistance);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_APERTURE:
#         axisBlockToLensParam(axisBlock, frame.lens.aperture);
#         frame.lens.hasData = true;
#         break;
#     case F4_FIELD_ID_FOCUS:
#         axisBlockToLensType(axisBlock, frame.focusVal);
#         break;
#     case F4_FIELD_ID_ZOOM:
#         axisBlockToLensType(axisBlock, (uint16_t&)frame.zoomVal);
#         //actual extender setting is in defined in bits [2:4] of Lensinfo byte
#         frame.lensExtender = static_cast<mosys::extenderSettings::e>(axisBlock.m_DataBits1 >> 3 & 0x07);
#         break;
#     case F4_FIELD_ID_CPAN:
#         axisBlockToAngleLinearRaw(axisBlock, frame.cranePan, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_CTILT:
#         axisBlockToAngleLinearRaw(axisBlock, frame.craneTilt, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_TURNT:
#         axisBlockToAngleLinearRaw(axisBlock, frame.turnTableRotation, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_CRANEX:
#         axisBlockToAngleLinearRaw(axisBlock, frame.dollyCranePosition, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_ORIENT:
#         axisBlockToAngleLinearRaw(axisBlock, frame.generalOrientationCoord, ANGLE_FACTOR);
#         break;
#     case F4_FIELD_ID_IRIS:
#         axisBlockToLensType(axisBlock, frame.irisVal);
#         break;
#     case F4_FIELD_ID_DIGIFOCUS:
#         axisBlockToLensType(axisBlock, frame.digiLensFocus);
#         break;
#     case F4_FIELD_ID_DIGIZOOM:
#         axisBlockToLensType(axisBlock, frame.digiLensZoom);
#         break;
#     case F4_FIELD_ID_DIGIIRIS:
#         axisBlockToLensType(axisBlock, frame.digiLensIris);
#         break;
#     case F4_FIELD_ID_STRINGX:
#         axisBlockToAngleLinearRaw(axisBlock, frame.xString, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_STRINGY:
#         axisBlockToAngleLinearRaw(axisBlock, frame.yString, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_HEAD_Y:
#         axisBlockToAngleLinearRaw(axisBlock, frame.headY, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_HEAD_Z:
#         axisBlockToAngleLinearRaw(axisBlock, frame.headZ, LINEAR_FACTOR);
#         break;
#     case F4_FIELD_ID_RAWPAN:
#         axisBlockToInt24(axisBlock, frame.rawEncoder); // this used to be a float angle but got overriden by the latest enconder.
#         break;
#     case F4_FIELD_ID_RAWTILT:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawTilt);
#         break;
#     case F4_FIELD_ID_RAWROLL:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawRoll);
#         break;
#     case F4_FIELD_ID_RAWJIB:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawJib);
#         break;
#     case F4_FIELD_ID_RAWTURN:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawTurn);
#         break;
#     case F4_FIELD_ID_RAWTRACK:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawTrack);
#         break;
#     case F4_FIELD_ID_RAWTELE:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawTele);
#         break;
#     case F4_FIELD_ID_RAWELEV:
#         axisBlockToAngleLinearRaw(axisBlock, frame.rawElev);
#         break;
#     case F4_FIELD_ID_GATEWAY_BUILD_VERSION:
#         lowerAxisBlockToValue(axisBlock, frame.buildInfo.major);
#         lowerAxisBlockToValue(axisBlock, frame.buildInfo.minor);
#         break;
#     case F4_FIELD_ID_GATEWAY_BUILD_DATE:
#         axisBlockToUint32(axisBlock, frame.buildInfo.buildDate);
#         break;
#     case F4_FIELD_ID_AXIS_DATA_INFO:
#         frame.axisDataInfo.fieldDelay = axisBlock.m_axisStatus;
#         frame.axisDataInfo.dataCollisionCounter = axisBlock.m_DataBits1;
#         frame.axisDataInfo.dataCollisionID = axisBlock.m_DataBits2;
#         frame.axisDataInfo.networkFaultCounter = axisBlock.m_DataBits3;
#         break;
#     case F4_FIELD_ID_NETWORK_STATUS_INFO:
#         frame.networkInfo.networkFlags = axisBlock.m_axisStatus;
#         frame.networkInfo.busOffCounterBits = axisBlock.m_DataBits1 << 8 | axisBlock.m_DataBits2;
#         frame.networkInfo.lastMissedNetworkID = axisBlock.m_DataBits3;
#         break;
#     case F4_FIELD_ID_PACKET_TIMING_INFO:
#         lowerAxisBlockToValue(axisBlock, frame.packetTimingInfo.lastSensorPacketTimestamp);
#         lowerAxisBlockToValue(axisBlock, frame.packetTimingInfo.f4PacketTransmissionTimestamp);
#         break;
#     case F4_FIELD_ID_GENLOCK_INFO:
#         lowerAxisBlockToValue(axisBlock, frame.genlockInfo.timestamp);
#         lowerAxisBlockToValue(axisBlock, frame.genlockInfo.counter);
#         break;
#     case F4_STARTRACKER_ID:
#     {
#         axisBlockToUint32(axisBlock, frame.startrackerID);
#         break;
#     }
#     case F4_FIELD_ID_TIMECODE:
#         F4AxisBlock::toTimecode(axisBlock, frame.timecode);
#         break;
#     case F4_TRACKING_STATUS:
#         frame.status = mosys::tracking::TrackingStatus(axisBlock.m_DataBits2);
#         break;
#     default:
#         break;
