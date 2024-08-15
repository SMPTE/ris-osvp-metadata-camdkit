#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import numbers
import typing
from jsonschema import validate

from camdkit.framework import *

PRETTY_FLOAT_DP = 5

class ActiveSensorPhysicalDimensions(IntegerDimensionsParameter):
  "Height and width of the active area of the camera sensor in microns"

  canonical_name = "activeSensorPhysicalDimensions"
  sampling = Sampling.STATIC
  units = "micron"
  section = "camera"

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return {
      "height": round(value.height / 1000.0, 3),
      "width": round(value.width / 1000.0, 3)
    }
  
class ActiveSensorResolution(IntegerDimensionsParameter):
  "Photosite resolution of the active area of the camera sensor in pixels"

  canonical_name = "activeSensorResolution"
  sampling = Sampling.STATIC
  units = "pixels"
  section = "camera"

class Duration(StrictlyPositiveRationalParameter):
  """Duration of the clip"""

  canonical_name = "duration"
  sampling = Sampling.STATIC
  units = "second"


class CaptureFPS(StrictlyPositiveRationalParameter):
  """Capture frame rate of the camera"""

  canonical_name = "captureRate"
  sampling = Sampling.STATIC
  units = "hertz"
  section = "camera"


class ISO(StrictlyPositiveIntegerParameter):
  """Arithmetic ISO scale as defined in ISO 12232"""

  canonical_name = "isoSpeed"
  sampling = Sampling.STATIC
  units = "unit"
  section = "camera"


class LensSerialNumber(StringParameter):
  """Unique identifier of the lens"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensMake(StringParameter):
  """Make of the lens"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensModel(StringParameter):
  """Model of the lens"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensFirmware(StringParameter):
  """Version identifier for the firmware of the lens"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "lens"
  
class LensDistortionModel(StringParameter):
  """Free string for notes about the specific lens distortion model"""  
  canonical_name = "distortionModel"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class CameraSerialNumber(StringParameter):
  """Unique identifier of the camera"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraMake(StringParameter):
  """Make of the camera"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraModel(StringParameter):
  """Model of the camera"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraFirmware(StringParameter):
  """Version identifier for the firmware of the camera"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "camera"
  
class CameraId(StringParameter):
  """Free string that identifies the camera - e.g. 'A'"""
  
  canonical_name = "id"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class DeviceSerialNumber(StringParameter):
  """Unique identifier of the device producing data"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "device"

class DeviceMake(StringParameter):
  """Make of the device producing data"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "device"

class DeviceModel(StringParameter):
  """Model of the device producing data"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "device"

class DeviceFirmware(StringParameter):
  """Version identifier for the firmware of the device producing data"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "device"

class AnamorphicSqueeze(StrictlyPositiveIntegerParameter):
  """Nominal ratio of height to width of the image of an axis-aligned square
  captured by the camera sensor. It can be used to de-squeeze images but is not
  however an exact number over the entire captured area due to a lens' intrinsic
  analog nature."""

  canonical_name = "anamorphicSqueeze"
  sampling = Sampling.STATIC
  units = "0.01 unit"
  section = "camera"

class FDLLink(UUIDURNParameter):
  """Unique identifier of the FDL used by the camera."""

  canonical_name = "fdlLink"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class ShutterAngle(Parameter):
  """Shutter speed as a fraction of the capture frame rate. The shutter speed
  (in units of 1/s) is equal to the value of the parameter divided by 360 times
  the capture frame rate."""

  canonical_name = "shutterAngle"
  sampling = Sampling.STATIC
  units = "degrees (angular)"
  section = "camera"

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be an integer in the range (0..360000]."""

    return isinstance(value, numbers.Integral) and 0 < value <= 360000

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 1,
      "maximum": 360000
    }

class PacketId(UUIDURNParameter):
  """Unique identifier of the packet in which data is being transported."""

  canonical_name = "packetId"
  sampling = Sampling.REGULAR
  units = None
  
class Protocol(StringParameter):
  """Unique identifier of the packet in which data is being traansported."""

  canonical_name = "protocol"
  sampling = Sampling.REGULAR
  units = None

class Status(StringParameter):
  """Free string that describes the status of the system - e.g. 'Optical Good' in a tracking system"""

  canonical_name = "status"
  sampling = Sampling.REGULAR
  units = None
  section = "device"
  
class Recording(BooleanParameter):
  """True if the system is recording data - e.g. tracking data"""
  
  canonical_name = "recording"
  sampling = Sampling.REGULAR
  units = None
  section = "device"
  
class Slate(StringParameter):
  """Free string that describes the recording slate - e.g. 'A101_A_4'"""
  
  canonical_name = "slate"
  sampling = Sampling.REGULAR
  units = None
  section = "device"
  
class Notes(StringParameter):
  """Free string for notes about tracking"""
  
  canonical_name = "notes"
  sampling = Sampling.REGULAR
  units = None
  section = "device"

class RelatedPackets(ArrayParameter):
  """
  List of packet unique IDs that are related to this packet. E.g. a related performance capture packet
  or a packet of static data from the same device.
  """

  canonical_name = "relatedPackets"
  sampling = Sampling.REGULAR
  units = None
  item_class = UUIDURNParameter

class GlobalStagePosition(Parameter):
  """
  Position of stage origin in global ENU and geodetic coordinates (E, N, U, lat0, lon0, h0). Note this may be dynamic
  e.g. if the stage is inside a moving vehicle.
  """
  sampling = Sampling.REGULAR
  canonical_name = "globalStage"
  units = "metres"
  
  @staticmethod
  def validate(value) -> bool:
    """
    Each field in the GlobalPosition shall be a real number
    """
    if not isinstance(value, GlobalPosition):
      return False
    
    for v in [value.E, value.N, value.U, value.lat0, value.lon0, value.h0]:
      if v is None or not isinstance(v, float):
        return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return GlobalPosition(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["E", "N", "U", "lat0", "lon0", "h0"],
      "properties": {
        "E": { "type": "number" },
        "N": { "type": "number" },
        "U": { "type": "number" },
        "lat0": { "type": "number" },
        "lon0": { "type": "number" },
        "h0": { "type": "number" }
      }
    }

class Transforms(Parameter):
  """
  X,Y,Z in metres of camera sensor relative to stage origin.
  The Z axis points upwards and the coordinate system is right-handed.
  Y points in the forward camera direction (when pan, tilt and roll are zero).
  For example in an LED volume Y would point towards the centre of the LED wall and so X would point to camera-right.
  Rotation expressed as euler angles in degrees of the camera sensor relative to stage origin
  Rotations are intrinsic and are measured around the axes ZXY, commonly referred to as [pan, tilt, roll]
  Notes on Euler angles:
  Euler angles are human readable and unlike quarternions, provide the ability for cycles (with angles >360 or <0 degrees).
  Where a tracking system is providing the pose of a virtual camera, gimbal lock does not present the physical challenges of a robotic system.
  Conversion to and from quarternions is trivial with an acceptable loss of precision
  """
  sampling = Sampling.REGULAR
  canonical_name = "transforms"
  units = "metres / degrees"

  @staticmethod
  def validate(value) -> bool:
    """Each component of each transform shall contain Real numbers."""

    if not isinstance(value, typing.Tuple):
      return False
    
    if len(value) == 0:
      return False

    for transform in value:
      if not isinstance(transform, Transform):
        return False
      if not isinstance(transform.translation, Vector3):
        return False
      if not isinstance(transform.rotation, Rotator3):
        return False
      # Scale is optional
      if transform.scale != None and not isinstance(transform.scale, Vector3):
        return False
      if not isinstance(transform.translation.x, numbers.Real) \
         or not isinstance(transform.translation.y, numbers.Real) \
         or not isinstance(transform.translation.z, numbers.Real):
        return False
      if not isinstance(transform.rotation.pan, numbers.Real) \
         or not isinstance(transform.rotation.tilt, numbers.Real) \
         or not isinstance(transform.rotation.roll, numbers.Real):
        return False
      if transform.scale != None:
        if not isinstance(transform.scale.x, numbers.Real) \
           or not isinstance(transform.scale.y, numbers.Real) \
           or not isinstance(transform.scale.z, numbers.Real):
          return False
      # Name and parent are optional
      if transform.name != None and not isinstance(transform.name, str):
        return False
      if transform.parent != None and not isinstance(transform.parent, str):
        return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    transforms = []
    for transform in value:
      # Factory ignores the optional fields
      transforms.append(dataclasses.asdict(transform, \
                                           dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
    return transforms  

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    transforms = ()
    for v in value:
      transform = Transform(**v)
      transform.translation = Vector3(transform.translation["x"], transform.translation["y"], transform.translation["z"])
      transform.rotation = Rotator3(transform.rotation["pan"], transform.rotation["tilt"], transform.rotation["roll"])
      if transform.scale is not None:
        transform.scale = Vector3(transform.scale["x"], transform.scale["y"], transform.scale["z"])
      transforms += (transform, )
    return transforms
  
  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "array",
      "minItems": 1,
      "uniqueItems": False,
      "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
          "translation": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
              "x": {
                  "type": "number",
              },
              "y": {
                  "type": "number",
              },
              "z": {
                  "type": "number"
              }
            }
          },
          "rotation": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
              "pan": {
                  "type": "number",
              },
              "tilt": {
                  "type": "number",
              },
              "roll": {
                  "type": "number"
              }
            }
          },
          "scale": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
              "x": {
                  "type": "number",
              },
              "y": {
                  "type": "number",
              },
              "z": {
                  "type": "number"
              }
            }
          },
          "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1023
          },
          "parent": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1023
          }
        },
        "required": ["translation", "rotation"]
      }
    }
  
class TimingMode(EnumParameter):
  """
  'external' timing mode describes the case where the transport packet has inherent timing, so no explicit timing data
  is required in the data).
  'internal' mode indicates the transport packet does not have inherent timing, so a PTP timestamp must be provided.
  """
  sampling = Sampling.REGULAR
  canonical_name = "mode"
  section = "timing"
  units = None

class TimingSynchronization(Parameter):
  """
  TODO doc
  """
  
  sampling = Sampling.REGULAR
  canonical_name = "synchronization"
  section = "timing"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """
    The parameter shall contain the required valid fields.
    """
    if not isinstance(value, Synchronization):
      return False
    if not (isinstance(value.frequency, numbers.Rational) and value.frequency > 0):
      return False
    if not isinstance(value.locked, bool):
      return False
    if not isinstance(value.source, SynchronizationSourceEnum):
      return False
    # Validate MAC address
    if value.ptp_master != None and not (isinstance(value.ptp_master,str) and 
                                         re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
                                                  value.ptp_master.lower())):
      return False
    if value.ptp_offset != None and not isinstance(value.ptp_offset, float):
      return False
    if value.ptp_domain != None and not (isinstance(value.ptp_domain, int) and value.ptp_domain >= 0):
      return False
    if value.offsets != None and not value.offsets.validate():
      return False
    if value.present != None and not isinstance(value.present, bool):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    d = {k: v for k, v in dataclasses.asdict(value).items() if v is not None}
    d["source"] = str(d["source"])
    d["frequency"] = { "num": d["frequency"].numerator, "denom": d["frequency"].denominator }
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    sync = Synchronization(**value)
    sync.source = SynchronizationSourceEnum(sync.source)
    sync.offsets = SynchronizationOffsets(**value["offsets"])
    sync.frequency = Fraction(value["frequency"]["num"], value["frequency"]["denom"])
    return sync

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "frequency": {
          "type": "object",
          "additionalProperties": False,
          "required": [ "num", "denom" ],
          "properties": {
            "num": {
              "type": "integer",
              "minimum": 1,
              "maximum": UINT_MAX
            },
            "denom": {
              "type": "integer",
              "minimum": 1,
              "maximum": UINT_MAX
            }
          }
        },
        "locked": { "type": "boolean" },
        "offsets": {
          "type": "object",
          "additionalProperties": False,
          "properties": {
            "translation": { "type": "number" },
            "rotation": { "type": "number" },
            "encoders": { "type": "number" }
          }
        },
        "present": { "type": "boolean" },
        "ptp_master": { "type": "string", "pattern": "^([A-F0-9]{2}:){5}[A-F0-9]{2}$" },
        "ptp_offset": { "type": "number" },
        "ptp_domain": { "type": "integer", "minimum": 0 },
        "source": { "type": "string", "enum": [e.value for e in SynchronizationSourceEnum] },
      },
      "required": ["frequency", "locked", "source"]
    }

class LensEncoders(Parameter):
  """
  Normalised real numbers (0-1) for focus, iris and zoom.
  Encoders are represented in this way (as opposed to raw integer values) to ensure values remain independent
  of encoder resolution, mininum and maximum (at an acceptable loss of precision).
  These values are only relevant in lenses with end-stops that demark the 0 and 1 range."
  """
  sampling = Sampling.REGULAR
  canonical_name = "encoders"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """
    The parameter shall contain at least one normalised values (0..1) for the FIZ encoders.
    """
    if not isinstance(value, Encoders):
      return False
    if value.focus == None and value.iris == None and value.zoom == None:
      return False
    for test in [value.focus, value.iris, value.zoom]:
      if test != None and not (isinstance(test, float) and test >= 0.0 and test <= 1.0):
        return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {k: v for k, v in dataclasses.asdict(value).items() if v is not None}

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensEncoders.to_json(value)
    for k,v in d.items():
      d[k] = round(v, PRETTY_FLOAT_DP)
    return d
  
  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Encoders(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "focus": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "iris": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "zoom": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        }
      },
      "anyOf": [ {"required": ["focus"]}, {"required": ["iris"]}, {"required": ["zoom"]}
      ]
    }
  
class LensRawEncoders(Parameter):
  """
  Raw encoder values for focus, iris and zoom.
  These values are dependent on encoder resolution and before any homing / ranging has taken place.
  """
  sampling = Sampling.REGULAR
  canonical_name = "rawEncoders"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """
    The parameter shall contain at least one integer value for the FIZ encoders.
    """
    if not isinstance(value, RawEncoders):
      return False
    if value.focus == None and value.iris == None and value.zoom == None:
      return False
    for test in [value.focus, value.iris, value.zoom]:
      if test != None and not (isinstance(test, int) and test >= 0):
        return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {k: v for k, v in dataclasses.asdict(value).items() if v is not None}

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensRawEncoders.to_json(value)
    for k,v in d.items():
      d[k] = round(v, PRETTY_FLOAT_DP)
    return d
  
  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return RawEncoders(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "focus": {
          "type": "integer",
          "minimum": 0
        },
        "iris": {
          "type": "integer",
          "minimum": 0
        },
        "zoom": {
          "type": "integer",
          "minimum": 0
        }
      },
      "anyOf": [ {"required": ["focus"]}, {"required": ["iris"]}, {"required": ["zoom"]}
      ]
    }
  
  
class TimingMode(EnumParameter):
  """
  'external' timing mode describes the case where the transport packet has inherent timing, so no explicit timing data is required in the data).
  'internal' mode indicates the transport packet does not have inherent timing, so a PTP timestamp must be provided.
  """
  sampling = Sampling.REGULAR
  canonical_name = "mode"
  section = "timing"
  units = None

class TimingTimestamp(TimestampParameter):
  """
  PTP timestamp of the data capture instant. Note this may differ from the packet's transmission PTP timestamp
  48-bit unsigned integer (seconds), 32-bit unsigned integer (nanoseconds), optional 32-bit unsigned integer (attoseconds)
  """
  sampling = Sampling.REGULAR
  canonical_name = "sampleTimestamp"
  section = "timing"
  units = None

class RecordedTimestamp(TimestampParameter):
  """
  PTP timestamp at which the data was recorded. Provided for convenience during playback of e.g. pre-recorded tracking data.
  48-bit unsigned integer (seconds), 32-bit unsigned integer (nanoseconds), optional 32-bit unsigned integer (attoseconds)
  """
  sampling = Sampling.REGULAR
  canonical_name = "recordedTimestamp"
  section = "timing"
  units = None

class TimingSequenceNumber(NonNegativeIntegerParameter):
  """
  TODO doc
  """
  sampling = Sampling.REGULAR
  canonical_name = "sequenceNumber"
  section = "timing"
  units = None

class TimingFrameRate(StrictlyPositiveRationalParameter):
  """
  TODO doc
  """
  sampling = Sampling.REGULAR
  canonical_name = "frameRate"
  section = "timing"
  units = None

class TimingTimecode(Parameter):
  """
  TODO doc
  """
  sampling = Sampling.REGULAR
  canonical_name = "timecode"
  section = "timing"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """
    The parameter shall contain a valid format and hours, minutes, seconds and frames with
    appropriate min/max values.
    """

    if not isinstance(value, Timecode):
      return False
    if not isinstance(value.format, TimecodeFormat):
      return False
    if not (isinstance(value.hours, int) and value.hours >= 0 and value.hours < 24):
      return False
    if not (isinstance(value.minutes, int) and value.minutes >= 0 and value.minutes < 60):
      return False
    if not (isinstance(value.seconds, int) and value.seconds >= 0 and value.seconds < 60):
      return False
    if not (isinstance(value.frames, int) and value.frames >= 0 and value.frames < value.format.to_int()):
      return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    d = dataclasses.asdict(value)
    d["format"] = {
      "frameRate": {
        "num": d["format"].frame_rate.numerator,
        "denom": d["format"].frame_rate.denominator
      },
      "dropFrame": d["format"].drop_frame
    }
    return d

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Timecode(value["hours"], value["minutes"], value["seconds"], value["frames"],
                    TimecodeFormat(in_frame_rate=Fraction(value["format"]["frameRate"]["num"],
                                                          value["format"]["frameRate"]["denom"]),
                                   in_drop_frame=value["format"]["dropFrame"]))

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": [ "hours", "minutes", "seconds", "frames", "format" ],
      "properties": {
        "hours": {
          "type": "integer",
          "minimum": 0,
          "maximum": 23
        },
        "minutes": {
          "type": "integer",
          "minimum": 0,
          "maximum": 59
        },
        "seconds": {
          "type": "integer",
          "minimum": 0,
          "maximum": 59
        },
        "frames": {
          "type": "integer",
          "minimum": 0,
          "maximum": 29
        },
        "format": {
          "type": "object",
          "required": [ "frameRate", "dropFrame" ],
          "additionalProperties": False,
          "properties": {
            "frameRate": {
              "type": "object",
              "additionalProperties": False,
              "required": [ "num", "denom" ],
              "properties": {
                "num": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": UINT_MAX
                },
                "denom": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": UINT_MAX
                }
              }
            },
            "dropFrame": {
              "type": "boolean"
            }
          }
        }
      }
    }

class TStop(StrictlyPositiveIntegerParameter):
  """The linear t-number of the lens, equal to the F-number of the lens divided
  by the square root of the transmittance of the lens."""

  canonical_name = "tStop"
  sampling = Sampling.REGULAR
  units = "0.001 unit"
  section = "lens"
  
  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return f"T{round(value/1000.0, 1)}"

class FStop(StrictlyPositiveIntegerParameter):
  """The linear f-number of the lens, equal to the focal length divided by the
  diameter of the entrance pupil."""

  canonical_name = "fStop"
  sampling = Sampling.REGULAR
  units = "0.001 unit"
  section = "lens"

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return f"F{round(value/1000.0, 1)}"

class NominalFocalLength(StrictlyPositiveIntegerParameter):
  """Nominal focal length of the lens. The number printed on the side of a prime
  lens, e.g. 50 mm, and undefined in the case of a zoom lens."""

  canonical_name = "nominalFocalLength"
  sampling = Sampling.STATIC
  units = "millimeter"
  section = "lens"

class FocalLength(NonNegativeRealParameter):
  """Focal length of the lens."""

  canonical_name = "focalLength"
  sampling = Sampling.REGULAR
  units = "millimeter"
  section = "lens"

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return round(value, 3)

class FocusPosition(StrictlyPositiveIntegerParameter):
  """Focus distance/position of the lens"""

  canonical_name = "focusPosition"
  sampling = Sampling.REGULAR
  units = "millimeter"
  section = "lens"

class EntrancePupilDistance(RationalParameter):
  """Position of the entrance pupil relative to the nominal imaging plane
  (positive if the entrance pupil is located on the side of the nominal imaging
  plane that is towards the object, and negative otherwise)"""

  canonical_name = "entrancePupilDistance"
  sampling = Sampling.REGULAR
  units = "millimeter"
  section = "lens"

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    return round(float(value), 3)

class FoVScale(Parameter):
  """Scaling factor on horizontal and vertical field-of-view for tweaking lens calibrations"""

  sampling = Sampling.REGULAR
  canonical_name = "fovScale"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """The horizontal and vertical measurements shall be each be a real non-negative number."""

    if not isinstance(value, Orientations):
      return False

    if not isinstance(value.horizontal, numbers.Real) or not isinstance(value.vertical, numbers.Real):
      return False

    if value.horizontal < 0.0 or value.vertical < 0.0:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Orientations(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": [
          "horizontal",
          "vertical"
      ],
      "properties": {
        "horizontal": {
            "type": "number",
            "minimum": 0.0
        },
        "vertical": {
            "type": "number",
            "minimum": 0.0
        }
      }
    }
  
class LensExposureFalloff(Parameter):
  """Coefficients for calculating the exposure fall-off (vignetting) of a lens"""
  sampling = Sampling.REGULAR
  canonical_name = "exposureFalloff"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """The coefficients shall each be real numbers."""

    if not isinstance(value, ExposureFalloff):
      return False
 
    # a1 is required
    if value.a1 == None:
      return False

    for v in [value.a1, value.a2, value.a3]:
      if v is not None and not isinstance(v, numbers.Real):
        return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensExposureFalloff.to_json(value)
    for k,v in d.items():
      d[k] = round(d[k], PRETTY_FLOAT_DP)
    return d
  
  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return ExposureFalloff(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["a1"],
      "properties": {
        "a1": {
            "type": "number"
        },
        "a2": {
            "type": "number"
        },
        "a3": {
            "type": "number"
        }
      }
    }
  
class LensDistortion(Parameter):
  """
  Coefficients for calculating the distortion characteristics of a lens comprising radial distortion
  coefficients of the spherical distortion (k1-N) and the tangential distortion (p1-N).
  """
  sampling = Sampling.REGULAR
  canonical_name = "distortion"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """The radial and tangential coefficients shall each be real numbers."""

    if not isinstance(value, Distortion):
      return False
 
    # At least one radial coefficient is required
    if value.radial == None or len(value.radial) == 0:
      return False

    for k in value.radial:
      if k is not None and not isinstance(k, numbers.Real):
        return False
    if value.tangential is not None:
      for p in value.tangential:
        if p is not None and not isinstance(p, numbers.Real):
          return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    d = dataclasses.asdict(value)
    if d["tangential"] == None:
      del d["tangential"]
    return d
  
  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensDistortion.to_json(value)
    d["radial"] = [round(x, PRETTY_FLOAT_DP) for x in d["radial"]]
    if "tangential" in d:
      d["tangential"] = [round(x, PRETTY_FLOAT_DP) for x in d["tangential"]]
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Distortion(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["radial"],
      "properties": {
        "radial": {
            "type": "array",
            "items": {
              "type": "number"
            },
            "minLength": 1
        },
        "tangential": {
            "type": "array",
            "items": {
              "type": "number"
            },
            "minLength": 1
        },
      }
    }
  
class LensUndistortion(LensDistortion):
  """
  Coefficients for calculating the undistortion characteristics of a lens comprising radial distortion
  coefficients of the spherical distortion (k1-N) and the tangential distortion (p1-N).
  """
  sampling = Sampling.REGULAR
  canonical_name = "undistortion"
  section = "lens"
  units = None
  
class LensCentreShift(Parameter):
  "Shift in x and y of the centre of distortion of the virtual camera"

  sampling = Sampling.REGULAR
  canonical_name = "centreShift"
  section = "lens"
  units = "Determined by distortion model"

  @staticmethod
  def validate(value) -> bool:
    """X and Y centre shift shall each be real numbers."""

    if not isinstance(value, CentreShift):
      return False
 
    if value.cx is None or not isinstance(value.cx, numbers.Real):
      return False
    if value.cy is None or not isinstance(value.cx, numbers.Real):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensCentreShift.to_json(value)
    d["cx"] = round(d["cx"], PRETTY_FLOAT_DP)
    d["cy"] = round(d["cy"], PRETTY_FLOAT_DP)
    return d
  
  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return CentreShift(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["cx", "cy"],
      "properties": {
        "cx": {
          "type": "number"
        },
        "cy": {
          "type": "number"
        }
      }
    }
  
class LensPerspectiveShift(Parameter):
  "Shift in x and y of the centre of projection of the virtual camera"
  sampling = Sampling.REGULAR
  canonical_name = "perspectiveShift"
  section = "lens"
  units = "millimetres"

  @staticmethod
  def validate(value) -> bool:
    """X and Y perspective shift shall each be real numbers."""

    if not isinstance(value, PerspectiveShift):
      return False
 
    if value.Cx is None or not isinstance(value.Cx, numbers.Real):
      return False
    if value.Cy is None or not isinstance(value.Cx, numbers.Real):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def to_pretty_json(value: typing.Any) -> typing.Any:
    d = LensCentreShift.to_json(value)
    d["Cx"] = round(d["Cx"], PRETTY_FLOAT_DP)
    d["Cy"] = round(d["Cy"], PRETTY_FLOAT_DP)
    return d
  
  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return PerspectiveShift(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["Cx", "Cy"],
      "properties": {
        "Cx": {
          "type": "number"
        },
        "Cy": {
          "type": "number"
        }
      }
    }

class LensCustom(ArrayParameter):
  """
  Until the OpenLensIO model is finalised, this list provides custom coefficients for a particular lens model
  e.g. undistortion, anamorphic etc
  """
  sampling = Sampling.REGULAR
  canonical_name = "custom"
  section = "lens"
  item_class = float
  units = None

class Clip(ParameterContainer):
  """
  Metadata for a camera clip.
  """
  # Static parameters
  active_sensor_physical_dimensions: typing.Optional[Dimensions] = ActiveSensorPhysicalDimensions()
  active_sensor_resolution: typing.Optional[Dimensions] = ActiveSensorResolution()
  anamorphic_squeeze: typing.Optional[numbers.Rational] = AnamorphicSqueeze()
  camera_make: typing.Optional[str] = CameraMake()
  camera_model: typing.Optional[str] = CameraModel()
  camera_firmware: typing.Optional[str] = CameraFirmware()
  camera_serial_number: typing.Optional[str] = CameraSerialNumber()
  camera_id: typing.Optional[str] = CameraId()
  capture_fps: typing.Optional[numbers.Rational] = CaptureFPS()
  device_make: typing.Optional[str] = DeviceMake()
  device_model: typing.Optional[str] = DeviceModel()
  device_firmware: typing.Optional[str] = DeviceFirmware()
  device_serial_number: typing.Optional[str] = DeviceSerialNumber()
  duration: typing.Optional[numbers.Rational] = Duration()
  fdl_link: typing.Optional[str] = FDLLink()
  iso: typing.Optional[numbers.Integral] = ISO()
  lens_distortion_model: typing.Optional[str] = LensDistortionModel()
  lens_firmware: typing.Optional[str] = LensFirmware()
  lens_make: typing.Optional[str] = LensMake()
  lens_model: typing.Optional[str] = LensModel()
  lens_nominal_focal_length: typing.Optional[numbers.Integral] = NominalFocalLength()
  lens_serial_number: typing.Optional[str] = LensSerialNumber()
  shutter_angle: typing.Optional[numbers.Integral] = ShutterAngle()
  # Regular parameters
  device_notes: typing.Optional[typing.Tuple[str]] = Notes()
  device_recording: typing.Optional[typing.Tuple[bool]] = Recording()
  device_slate: typing.Optional[typing.Tuple[str]] = Slate()
  device_status: typing.Optional[typing.Tuple[str]] = Status()
  global_stage: typing.Optional[typing.Tuple[GlobalPosition]] = GlobalStagePosition()
  lens_centre_shift: typing.Optional[typing.Tuple[CentreShift]] = LensCentreShift()
  lens_custom: typing.Optional[typing.Tuple[tuple]] = LensCustom()
  lens_distortion: typing.Optional[typing.Tuple[Distortion]] = LensDistortion()
  lens_encoders: typing.Optional[typing.Tuple[LensEncoders]] = LensEncoders()
  lens_raw_encoders: typing.Optional[typing.Tuple[LensRawEncoders]] = LensRawEncoders()
  lens_entrance_pupil_distance: typing.Optional[typing.Tuple[numbers.Rational]] = EntrancePupilDistance()
  lens_exposure_falloff: typing.Optional[typing.Tuple[Orientations]] = LensExposureFalloff()
  lens_f_number: typing.Optional[typing.Tuple[numbers.Integral]] = FStop()
  lens_focal_length: typing.Optional[typing.Tuple[numbers.Real]] = FocalLength()
  lens_focus_position: typing.Optional[typing.Tuple[numbers.Integral]] = FocusPosition()
  lens_fov_scale: typing.Optional[typing.Tuple[Orientations]] = FoVScale()
  lens_perspective_shift: typing.Optional[typing.Tuple[PerspectiveShift]] = LensPerspectiveShift()
  lens_t_number: typing.Optional[typing.Tuple[numbers.Integral]] = TStop()
  lens_undistortion: typing.Optional[typing.Tuple[Distortion]] = LensUndistortion()
  packet_id: typing.Optional[typing.Tuple[str]] = PacketId()
  protocol: typing.Optional[typing.Tuple[str]] = Protocol()
  related_packets: typing.Optional[typing.Tuple[tuple]] = RelatedPackets()
  timing_frame_rate: typing.Optional[typing.Tuple[NonNegativeRealParameter]] = TimingFrameRate()
  timing_mode: typing.Optional[typing.Tuple[TimingMode]] = TimingMode()
  timing_recorded_timestamp: typing.Optional[typing.Tuple[TimestampParameter]] = RecordedTimestamp()
  timing_sample_timestamp: typing.Optional[typing.Tuple[TimestampParameter]] = TimingTimestamp()
  timing_sequence_number: typing.Optional[typing.Tuple[NonNegativeIntegerParameter]] = TimingSequenceNumber()
  timing_synchronization: typing.Optional[typing.Tuple[Synchronization]] = TimingSynchronization()
  timing_timecode: typing.Optional[typing.Tuple[TimingTimecode]] = TimingTimecode()
  transforms: typing.Optional[typing.Tuple[Transforms]] = Transforms()

  def validate(self):
    "Validate a single static data set against the schema. Return the JSON for convenience"
    self._set_static()
    json = self[0].to_json()
    schema = self.make_json_schema()
    validate(json, schema)
    return json

  def prettify(self):
    "Return a pretty version of the json with units and sections"
    self._set_static()
    return self[0].to_pretty_json()

  def append(self, clip):
    "Helper to add another clip's parameters to this clip's REGULAR data tuples"
    if not isinstance(clip, Clip):
      raise ValueError
    for prop, desc in self._params.items():
      if clip._values[prop] != None and desc.sampling == Sampling.REGULAR:
        self._values[prop] += clip._values[prop]

  def __getitem__(self, i):
    "Helper to convert to a single STATIC data frame for JSON output"
    clip = Clip()
    for f in dir(self):
      desc = getattr(self, f)
      if not isinstance(desc, tuple):
        if not f in self._values.keys() or self._values[f] is None:
          continue
        setattr(clip, f, desc)
      else:
        setattr(clip, f, desc[i])
    return clip
  
  @classmethod
  def make_opentrackio_dynamic_schema(cls) -> dict:
    "Helper to create a schema for a single dynamic frame of OpenTrackIO"
    # Remove all the existing STATIC parameters and make the REGULAR parameters STATIC
    for prop, desc in cls._params.copy().items():
      if desc.sampling == Sampling.STATIC:
        del cls._params[prop]
        continue
      desc.sampling = Sampling.STATIC
    return super().make_json_schema()
  
  @classmethod
  def make_opentrackio_static_schema(cls) -> dict:
    "Helper to create a schema for a single static frame of OpenTrackIO"
    # Remove all the existing REGULAR parameters
    for prop, desc in cls._params.copy().items():
      if desc.sampling == Sampling.REGULAR:
        del cls._params[prop]
        continue
    return super().make_json_schema()