#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Data model"""

import numbers
import typing
from jsonschema import validate

from camdkit.framework import *

OPENTRACKIO_PROTOCOL_NAME = "OpenTrackIO"
OPENTRACKIO_PROTOCOL_VERSION = (0,9,1)

class ActiveSensorPhysicalDimensions(DimensionsParameter):
  """Height and width of the active area of the camera sensor in microns
  """

  canonical_name = "activeSensorPhysicalDimensions"
  sampling = Sampling.STATIC
  units = "millimeter"
  section = "camera"
  
class ActiveSensorResolution(IntegerDimensionsParameter):
  """Photosite resolution of the active area of the camera sensor in
  pixels
  """

  canonical_name = "activeSensorResolution"
  sampling = Sampling.STATIC
  units = "pixel"
  section = "camera"

class Duration(StrictlyPositiveRationalParameter):
  """Duration of the clip"""

  canonical_name = "duration"
  sampling = Sampling.STATIC
  units = "second"


class CaptureFrameRate(StrictlyPositiveRationalParameter):
  """Capture frame rate of the camera"""

  canonical_name = "captureFrameRate"
  sampling = Sampling.STATIC
  units = "hertz"
  section = "camera"


class ISO(StrictlyPositiveIntegerParameter):
  """Arithmetic ISO scale as defined in ISO 12232"""

  canonical_name = "isoSpeed"
  sampling = Sampling.STATIC
  units = None
  section = "camera"


class LensSerialNumber(StringParameter):
  """Non-blank string uniquely identifying the lens"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensMake(StringParameter):
  """Non-blank string naming lens manufacturer"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensModel(StringParameter):
  """Non-blank string identifying lens model"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class LensFirmware(StringParameter):
  """Non-blank string identifying lens firmware version"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "lens"

class CameraSerialNumber(StringParameter):
  """Non-blank string uniquely identifying the camera"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraMake(StringParameter):
  """Non-blank string naming camera manufacturer"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraModel(StringParameter):
  """Non-blank string identifying camera model"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class CameraFirmware(StringParameter):
  """Non-blank string identifying camera firmware version"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "camera"
  
class CameraLabel(StringParameter):
  """Non-blank string containing user-determined camera identifier"""
  
  canonical_name = "label"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class TrackerSerialNumber(StringParameter):
  """Non-blank string uniquely identifying the tracking device"""

  canonical_name = "serialNumber"
  sampling = Sampling.STATIC
  units = None
  section = "tracker"

class TrackerMake(StringParameter):
  """Non-blank string naming tracking device manufacturer"""

  canonical_name = "make"
  sampling = Sampling.STATIC
  units = None
  section = "tracker"

class TrackerModel(StringParameter):
  """Non-blank string identifying tracking device model"""

  canonical_name = "model"
  sampling = Sampling.STATIC
  units = None
  section = "tracker"

class TrackerFirmware(StringParameter):
  """Non-blank string identifying tracking device firmware version"""

  canonical_name = "firmwareVersion"
  sampling = Sampling.STATIC
  units = None
  section = "tracker"

class AnamorphicSqueeze(StrictlyPositiveRationalParameter):
  """Nominal ratio of height to width of the image of an axis-aligned
  square captured by the camera sensor. It can be used to de-squeeze
  images but is not however an exact number over the entire captured
  area due to a lens' intrinsic analog nature.
  """

  canonical_name = "anamorphicSqueeze"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class FDLLink(UUIDURNParameter):
  """URN identifying the ASC Framing Decision List used by the camera.
  """

  canonical_name = "fdlLink"
  sampling = Sampling.STATIC
  units = None
  section = "camera"

class ShutterAngle(RealParameter):
  """Shutter speed as a fraction of the capture frame rate. The shutter
  speed (in units of 1/s) is equal to the value of the parameter divided
  by 360 times the capture frame rate.
  """

  canonical_name = "shutterAngle"
  sampling = Sampling.STATIC
  units = "degree"
  section = "camera"

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a real number in the range (0..360]."""

    return isinstance(value, numbers.Real) and 0.0 <= value <= 360.0

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "number",
      "minimum": 0.0,
      "maximum": 360.0
    }

class SampleId(UUIDURNParameter):
  """URN serving as unique identifier of the sample in which data is
  being transported.
  """

  canonical_name = "sampleId"
  sampling = Sampling.REGULAR
  units = None

class SourceId(UUIDURNParameter):
  """URN serving as unique identifier of the source from which data is
  being transported.
  """

  canonical_name = "sourceId"
  sampling = Sampling.REGULAR
  units = None

class SourceNumber(NonNegativeIntegerParameter):
  """Number that identifies the index of the stream from a source from which
  data is being transported. This is most important in the case where a source
  is producing multiple streams of samples.
  """

  canonical_name = "sourceNumber"
  sampling = Sampling.REGULAR
  units = None

class Protocol(Parameter):
  """Name of the protocol in which the sample is being employed, and
  version of that protocol
  """
  canonical_name = "protocol"
  sampling = Sampling.REGULAR
  units = None

  @staticmethod
  def validate(value) -> bool:
    """Protocol name is nonblank string; protocol version is basic x.y.z
     semantic versioning string
     """

    if not isinstance(value, VersionedProtocol):
      return False

    if not isinstance(value.name, str):
      return False
    if not len(value.name):
      return False
    if value.name != OPENTRACKIO_PROTOCOL_NAME:  # Temporary restriction
      return False

    if not isinstance(value.version, tuple):
      return False
    if len(value.version) != 3:
      return False
    return all([
      isinstance(version_number_component, int) \
                and version_number_component >= 0 \
                and version_number_component <= 9 \
                for version_number_component in value.version])

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {k: v for k, v in dataclasses.asdict(value).items() if v is not None}

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return VersionedProtocol(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "name": {
          "type": "string",
            "minLength": 1,
            "maxLength": 1023
        },
        "version": {
          "type": "array",
          "items": {
            "type": "integer",
            "minValue": 0,
            "maxValue": 9
          },
          "minItems": 3,
          "maxItems": 3
        }
      }
    }


class Status(StringParameter):
  """Non-blank string describing status of tracking system"""

  canonical_name = "status"
  sampling = Sampling.REGULAR
  units = None
  section = "tracker"
  
class Recording(BooleanParameter):
  """Boolean indicating whether tracking system is recording data"""
  
  canonical_name = "recording"
  sampling = Sampling.REGULAR
  units = None
  section = "tracker"
  
class Slate(StringParameter):
  """Non-blank string describing the recording slate"""
  
  canonical_name = "slate"
  sampling = Sampling.REGULAR
  units = None
  section = "tracker"
  
class Notes(StringParameter):
  """Non-blank string containing notes about tracking system"""
  
  canonical_name = "notes"
  sampling = Sampling.REGULAR
  units = None
  section = "tracker"

class RelatedSampleIds(ArrayParameter):
  """List of sampleId properties of samples related to this sample. The
  existence of a sample with a given sampleId is not guaranteed.
  """

  canonical_name = "relatedSampleIds"
  sampling = Sampling.REGULAR
  units = None
  item_class = UUIDURNParameter

class GlobalStagePosition(Parameter):
  """Position of stage origin in global ENU and geodetic coordinates
  (E, N, U, lat0, lon0, h0). Note this may be dynamic if the stage is
  inside a moving vehicle.
  """
  sampling = Sampling.REGULAR
  canonical_name = "globalStage"
  units = "meter"
  
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
  """A list of transforms.
  Transforms are composed in order with the last in the list representing
  the X,Y,Z in meters of camera sensor relative to stage origin.
  The Z axis points upwards and the coordinate system is right-handed.
  Y points in the forward camera direction (when pan, tilt and roll are
  zero).
  For example in an LED volume Y would point towards the centre of the
  LED wall and so X would point to camera-right.
  Rotation expressed as euler angles in degrees of the camera sensor
  relative to stage origin
  Rotations are intrinsic and are measured around the axes ZXY, commonly
  referred to as [pan, tilt, roll]
  Notes on Euler angles:
  Euler angles are human readable and unlike quarternions, provide the
  ability for cycles (with angles >360 or <0 degrees).
  Where a tracking system is providing the pose of a virtual camera,
  gimbal lock does not present the physical challenges of a robotic
  system.
  Conversion to and from quarternions is trivial with an acceptable loss
  of precision.
  """
  sampling = Sampling.REGULAR
  canonical_name = "transforms"
  units = "meter / degree"

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
      # id is optional
      if transform.id != None and not isinstance(transform.id, str):
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
            },
            "units": "meter"
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
            },
            "units": "degree"
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
          "id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1023
          }
        },
        "required": ["translation", "rotation"]
      }
    }


class TimingSynchronization(Parameter):
  """Object describing how the tracking device is synchronized for this
  sample.

  frequency: The frequency of a synchronization signal.This may differ from
  the sample frame rate for example in a genlocked tracking device. This is
  not required if the synchronization source is PTP or NTP.
  locked: Is the tracking device locked to the synchronization source
  offsets: Offsets in seconds between sync and sample. Critical for e.g.
  frame remapping, or when using different data sources for
  position/rotation and lens encoding
  present: Is the synchronization source present (a synchronization
  source can be present but not locked if frame rates differ for
  example)
  ptp: If the synchronization source is a PTP master, then this object
  contains:
  - "master": The MAC address of the PTP master
  - "offset": The timing offset in seconds from the sample timestamp to
  the PTP timestamp
  - "domain": The PTP domain number
  source: The source of synchronization must be defined as one of the
  following:
  - "genlock": The tracking device has an external black/burst or
  tri-level analog sync signal that is triggering the capture of
  tracking samples
  - "videoIn": The tracking device has an external video signal that is
  triggering the capture of tracking samples
  - "ptp": The tracking device is locked to a PTP master
  - "ntp": The tracking device is locked to an NTP server
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
    if not isinstance(value.locked, bool):
      return False
    if not isinstance(value.source, SynchronizationSourceEnum):
      return False
    if value.frequency != None:
      if not (isinstance(value.frequency, numbers.Rational) and value.frequency > 0):
        return False
    if value.ptp != None:
      # Validate MAC address
      if value.ptp.master != None and not (isinstance(value.ptp.master,str) and 
                                           re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
                                           value.ptp.master.lower())):
        return False
      if value.ptp.offset != None and not isinstance(value.ptp.offset, float):
        return False
      if value.ptp.domain != None and not (isinstance(value.ptp.domain, int) \
                                           and value.ptp.domain < 128 \
                                           and value.ptp.domain >= 0):
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
    if "frequency" in d:
      d["frequency"] = { "num": d["frequency"].numerator, "denom": d["frequency"].denominator }
    if value.offsets is not None:
        d["offsets"] = SynchronizationOffsets.to_json(value.offsets)
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    sync = Synchronization(**value)
    sync.source = SynchronizationSourceEnum(sync.source)
    sync.offsets = SynchronizationOffsets(translation=value["offsets"]["translation"],
                                          rotation=value["offsets"]["rotation"],
                                          lens_encoders=value["offsets"]["lensEncoders"])
    sync.ptp = SynchronizationPTP(**value["ptp"])
    sync.frequency = Fraction(value["frequency"]["num"], value["frequency"]["denom"])
    return sync

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "description": Synchronization.__doc__,
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
            "lensEncoders": { "type": "number" }
          }
        },
        "present": { "type": "boolean" },
        "ptp": {
          "type": "object",
          "additionalProperties": False,
          "properties": {
            "master": { "type": "string", "pattern": "^([A-F0-9]{2}:){5}[A-F0-9]{2}$" },
            "offset": { "type": "number" },
            "domain": { "type": "integer", "minimum": 0, "maximum": 127 }
          }
        },
        "source": { "type": "string", "enum": [e.value for e in SynchronizationSourceEnum] },
      },
      "required": ["locked", "source"]
    }

class LensEncoders(Parameter):
  """
  Normalised real numbers (0-1) for focus, iris and zoom.
  Encoders are represented in this way (as opposed to raw integer
    values) to ensure values remain independent of encoder resolution,
    minimum and maximum (at an acceptable loss of precision).
  These values are only relevant in lenses with end-stops that
    demarcate the 0 and 1 range.
  Value should be provided in the following directions (if known):
    Focus:   0=infinite     1=closest
    Iris:    0=open         1=closed
    Zoom:    0=wide angle   1=telephoto
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
    if not isinstance(value, FizEncoders):
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
  def from_json(value: typing.Any) -> typing.Any:
    return FizEncoders(**value)

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
  These values are dependent on encoder resolution and before any
    homing / ranging has taken place.
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
    if not isinstance(value, RawFizEncoders):
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
  def from_json(value: typing.Any) -> typing.Any:
    return RawFizEncoders(**value)

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
  """Enumerated value indicating whether the sample transport mechanism
    provides inherent ('external') timing, or whether the transport
    mechanism lacks inherent timing and so the sample must contain a PTP
    timestamp itself ('internal') to carry timing information.
  """
  sampling = Sampling.REGULAR
  canonical_name = "mode"
  section = "timing"
  units = None

class TimingTimestamp(TimestampParameter):
  """PTP timestamp of the data capture instant. Note this may differ
    from the packet's transmission PTP timestamp. The timestamp
    comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
    integer (nanoseconds)
  """
  sampling = Sampling.REGULAR
  canonical_name = "sampleTimestamp"
  section = "timing"
  units = "second"

class RecordedTimestamp(TimestampParameter):
  """
  PTP timestamp of the data recording instant, provided for convenience
    during playback of e.g. pre-recorded tracking data. The timestamp
    comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
    integer (nanoseconds)
  """
  sampling = Sampling.REGULAR
  canonical_name = "recordedTimestamp"
  section = "timing"
  units = "second"

class TimingSequenceNumber(NonNegativeIntegerParameter):
  """Integer incrementing with each sample."""
  sampling = Sampling.REGULAR
  canonical_name = "sequenceNumber"
  section = "timing"
  units = None

class TimingSampleRate(StrictlyPositiveRationalParameter):
  """Sample frame rate as a rational number. Drop frame rates such as
  29.97 should be represented as e.g. 30000/1001. In a variable rate
  system this should is estimated from the last sample delta time.
  """
  sampling = Sampling.REGULAR
  canonical_name = "sampleRate"
  section = "timing"
  units = None

class TimingTimecode(Parameter):
  """SMPTE timecode of the sample. Timecode is a standard for labeling
  individual frames of data in media systems and is useful for
  inter-frame synchronization.
   - format.frameRate: The frame rate as a rational number. Drop frame
  rates such as 29.97 should be represented as e.g. 30000/1001. The
  timecode frame rate may differ from the sample frequency.
  """
  sampling = Sampling.REGULAR
  canonical_name = "timecode"
  section = "timing"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall contain a valid format and hours, minutes,
    seconds and frames with appropriate min/max values.
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
    if not (isinstance(value.frames, int) and value.frames >= 0 and \
            value.frames < value.format.to_int() and value.format.frame_rate <= 120):
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
      "subFrame": d["format"].sub_frame,
    }
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Timecode(value["hours"], value["minutes"], value["seconds"], value["frames"],
                    TimecodeFormat(in_frame_rate=Fraction(value["format"]["frameRate"]["num"],
                                                          value["format"]["frameRate"]["denom"]),
                                   in_sub_frame=value["format"]["subFrame"]))

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
          "maximum": 119
        },
        "format": {
          "type": "object",
          "description": TimecodeFormat.__doc__.replace("\n ", ""),
          "required": [ "frameRate" ],
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
            "subFrame": {
              "type": "integer",
              "minimum": 0,
              "maximum": UINT_MAX
            }
          }
        }
      }
    }

class TStop(NonNegativeRealParameter):
  """Linear t-number of the lens, equal to the F-number of the lens
  divided by the square root of the transmittance of the lens.
  """

  canonical_name = "tStop"
  sampling = Sampling.REGULAR
  units = None
  section = "lens"

class FStop(NonNegativeRealParameter):
  """The linear f-number of the lens, equal to the focal length divided
  by the diameter of the entrance pupil.
  """

  canonical_name = "fStop"
  sampling = Sampling.REGULAR
  units = None
  section = "lens"

class NominalFocalLength(NonNegativeRealParameter):
  """Nominal focal length of the lens. The number printed on the side
  of a prime lens, e.g. 50 mm, and undefined in the case of a zoom lens.
  """

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

class FocusDistance(NonNegativeRealParameter):
  """Focus distance/position of the lens"""

  canonical_name = "focusDistance"
  sampling = Sampling.REGULAR
  units = "meter"
  section = "lens"

class EntrancePupilOffset(RealParameter):
  """Offset of the entrance pupil relative to the nominal imaging plane
  (positive if the entrance pupil is located on the side of the nominal
  imaging plane that is towards the object, and negative otherwise).
  Measured in meters as in a render engine it is often applied in the
  virtual camera's transform chain.
  """

  canonical_name = "entrancePupilOffset"
  sampling = Sampling.REGULAR
  units = "meter"
  section = "lens"

class DistortionOverscan(GreaterEqualOneRealParameter):
  """Overscan factor on lens distortion. This is primarily relevant when
  storing overscan values, not in transmission as the overscan should be
  calculated by the consumer.
  """

  sampling = Sampling.REGULAR
  canonical_name = "distortionOverscan"
  section = "lens"
  units = None

class UndistortionOverscan(GreaterEqualOneRealParameter):
  """Overscan factor on lens undistortion. This is primarily relevant when
  storing overscan values, not in transmission as the overscan should be
  calculated by the consumer.
  """

  sampling = Sampling.REGULAR
  canonical_name = "undistortionOverscan"
  section = "lens"
  units = None

class DistortionOverscanMaximum(GreaterEqualOneRealParameter):
  """Static maximum overscan factor on lens distortion. This is primarily
  relevant when storing overscan values, not in transmission as the
  overscan should be calculated by the consumer.
  """

  sampling = Sampling.STATIC
  canonical_name = "distortionOverscanMax"
  section = "lens"
  units = None
  
class UndistortionOverscanMaximum(GreaterEqualOneRealParameter):
  """Static maximum overscan factor on lens undistortion. This is primarily
  relevant when storing overscan values, not in transmission as the
  overscan should be calculated by the consumer.
  """

  sampling = Sampling.STATIC
  canonical_name = "undistortionOverscanMax"
  section = "lens"
  units = None

class DistortionIsProjection(BooleanParameter):
  """Indicator that the OpenLensIO distortion model is the Projection
  Characterization, not the Field-Of-View Characterization. This is 
  primarily relevant when storing overscan values, not in transmission
  as the overscan should be calculated by the consumer.
  """

  sampling = Sampling.STATIC
  canonical_name = "distortionIsProjection"
  section = "lens"
  units = None

class LensExposureFalloff(Parameter):
  """Coefficients for calculating the exposure fall-off (vignetting) of
  a lens
  """
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
  
class LensDistortions(Parameter):
  """A list of Distortion objects that each define the coefficients for
  calculating the distortion characteristics of a lens comprising radial
  distortion coefficients of the spherical distortion (k1-N) and the
  tangential distortion (p1-N). An optional key 'model' can be used that
  describes the distortion model. The default is Brown-Conrady D-U (that
  maps Distorted to Undistorted coordinates).
  """
  sampling = Sampling.REGULAR
  canonical_name = "distortion"
  section = "lens"
  units = None

  @staticmethod
  def validate(value) -> bool:
    """The list shall contain at least one Distortion object, and in each
    object the radial and tangential coefficients shall each be real numbers.
    """

    if not isinstance(value, tuple):
      return False
    
    if len(value) == 0:
      return False
    
    for v in value:
      if not isinstance(v, Distortion):
        return False
      
      # If model is provided check the length
      if v.model != None and len(v.model) == 0:
        return False
  
      # At least one radial coefficient is required
      if v.radial == None or len(v.radial) == 0:
        return False

      for k in v.radial:
        if k is not None and not isinstance(k, numbers.Real):
          return False
      if v.tangential is not None:
        if len(v.tangential) == 0:
          return False
        for p in v.tangential:
          if p is not None and not isinstance(p, numbers.Real):
            return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    a = []
    for element in value:
      d = dataclasses.asdict(element)
      if d["model"] == None:
        del d["model"]
      if d["tangential"] == None:
        del d["tangential"]
      a.append(d)
    return a

  @staticmethod
  def from_json(value: typing.Any) -> typing.Tuple[Distortion]:
    a = ()
    for element in value:
      a += (Distortion(**element),)
    return a

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["radial"],
        "properties": {
          "model": {
            "type": "string",
          },
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
    }
  
class LensDistortionOffset(Parameter):
  """Offset in x and y of the centre of distortion of the virtual camera
  """

  sampling = Sampling.REGULAR
  canonical_name = "distortionOffset"
  section = "lens"
  units = "millimeter"

  @staticmethod
  def validate(value) -> bool:
    """X and Y centre shift shall each be real numbers."""

    if not isinstance(value, DistortionOffset):
      return False
 
    if value.x is None or not isinstance(value.x, numbers.Real):
      return False
    if value.y is None or not isinstance(value.x, numbers.Real):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return DistortionOffset(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["x", "y"],
      "properties": {
        "x": {
          "type": "number"
        },
        "y": {
          "type": "number"
        }
      }
    }
  
class LensProjectionOffset(Parameter):
  """Offset in x and y of the centre of perspective projection of the
  virtual camera
  """
  sampling = Sampling.REGULAR
  canonical_name = "projectionOffset"
  section = "lens"
  units = "millimeter"

  @staticmethod
  def validate(value) -> bool:
    """X and Y projection offset shall each be real numbers."""

    if not isinstance(value, ProjectionOffset):
      return False
 
    if value.x is None or not isinstance(value.x, numbers.Real):
      return False
    if value.y is None or not isinstance(value.x, numbers.Real):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return ProjectionOffset(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": ["x", "y"],
      "properties": {
        "x": {
          "type": "number"
        },
        "y": {
          "type": "number"
        }
      }
    }

class LensCustom(ArrayParameter):
  """This list provides optional additional custom coefficients that can 
  extend the existing lens model. The meaning of and how these characteristics
  are to be applied to a virtual camera would require negotiation between a
  particular producer and consumer.
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
  camera_label: typing.Optional[str] = CameraLabel()
  capture_frame_rate: typing.Optional[numbers.Rational] = CaptureFrameRate()
  tracker_make: typing.Optional[str] = TrackerMake()
  tracker_model: typing.Optional[str] = TrackerModel()
  tracker_firmware: typing.Optional[str] = TrackerFirmware()
  tracker_serial_number: typing.Optional[str] = TrackerSerialNumber()
  duration: typing.Optional[numbers.Rational] = Duration()
  fdl_link: typing.Optional[str] = FDLLink()
  iso: typing.Optional[numbers.Integral] = ISO()
  lens_distortion_is_projection: typing.Optional[bool] = DistortionIsProjection()
  lens_distortion_overscan_max: typing.Optional[numbers.Real] = DistortionOverscanMaximum()
  lens_undistortion_overscan_max: typing.Optional[numbers.Real] = UndistortionOverscanMaximum()
  lens_firmware: typing.Optional[str] = LensFirmware()
  lens_make: typing.Optional[str] = LensMake()
  lens_model: typing.Optional[str] = LensModel()
  lens_nominal_focal_length: typing.Optional[numbers.Real] = NominalFocalLength()
  lens_serial_number: typing.Optional[str] = LensSerialNumber()
  shutter_angle: typing.Optional[numbers.Real] = ShutterAngle()
  # Regular parameters
  tracker_notes: typing.Optional[typing.Tuple[str]] = Notes()
  tracker_recording: typing.Optional[typing.Tuple[bool]] = Recording()
  tracker_slate: typing.Optional[typing.Tuple[str]] = Slate()
  tracker_status: typing.Optional[typing.Tuple[str]] = Status()
  global_stage: typing.Optional[typing.Tuple[GlobalPosition]] = GlobalStagePosition()
  lens_custom: typing.Optional[typing.Tuple[tuple]] = LensCustom()
  lens_distortions: typing.Optional[typing.Tuple[typing.Tuple[Distortion]]] = LensDistortions()
  lens_distortion_overscan: typing.Optional[typing.Tuple[numbers.Real]] = DistortionOverscan()
  lens_distortion_offset: typing.Optional[typing.Tuple[DistortionOffset]] = LensDistortionOffset()
  lens_encoders: typing.Optional[typing.Tuple[LensEncoders]] = LensEncoders()
  lens_entrance_pupil_offset: typing.Optional[typing.Tuple[numbers.Real]] = EntrancePupilOffset()
  lens_exposure_falloff: typing.Optional[typing.Tuple[ExposureFalloff]] = LensExposureFalloff()
  lens_f_number: typing.Optional[typing.Tuple[numbers.Real]] = FStop()
  lens_focal_length: typing.Optional[typing.Tuple[numbers.Real]] = FocalLength()
  lens_focus_distance: typing.Optional[typing.Tuple[numbers.Real]] = FocusDistance()
  lens_projection_offset: typing.Optional[typing.Tuple[ProjectionOffset]] = LensProjectionOffset()
  lens_raw_encoders: typing.Optional[typing.Tuple[LensRawEncoders]] = LensRawEncoders()
  lens_t_number: typing.Optional[typing.Tuple[numbers.Real]] = TStop()
  lens_undistortion_overscan: typing.Optional[typing.Tuple[numbers.Real]] = UndistortionOverscan()
  protocol: typing.Optional[typing.Tuple[VersionedProtocol]] = Protocol()
  related_sample_ids: typing.Optional[typing.Tuple[tuple]] = RelatedSampleIds()
  sample_id: typing.Optional[typing.Tuple[str]] = SampleId()
  source_id: typing.Optional[typing.Tuple[str]] = SourceId()
  source_number: typing.Optional[typing.Tuple[int]] = SourceNumber()
  timing_mode: typing.Optional[typing.Tuple[TimingMode]] = TimingMode()
  timing_recorded_timestamp: typing.Optional[typing.Tuple[TimestampParameter]] = RecordedTimestamp()
  timing_sample_rate: typing.Optional[typing.Tuple[StrictlyPositiveRationalParameter]] = TimingSampleRate()
  timing_sample_timestamp: typing.Optional[typing.Tuple[TimestampParameter]] = TimingTimestamp()
  timing_sequence_number: typing.Optional[typing.Tuple[NonNegativeIntegerParameter]] = TimingSequenceNumber()
  timing_synchronization: typing.Optional[typing.Tuple[Synchronization]] = TimingSynchronization()
  timing_timecode: typing.Optional[typing.Tuple[TimingTimecode]] = TimingTimecode()
  transforms: typing.Optional[typing.Tuple[Transforms]] = Transforms()

  def validate(self):
    """Validate a single static data set against the schema. Return the
    JSON for convenience
    """
    json = self[0].to_json()
    schema = self.make_json_schema()
    validate(json, schema)
    self._reset_sampling()
    return json

  def append(self, clip):
    """Helper to add another clip's parameters to this clip's REGULAR
    data tuples
    """
    if not isinstance(clip, Clip):
      raise ValueError
    for prop, desc in self._params.items():
      if clip._values[prop] != None and desc.sampling == Sampling.REGULAR:
        self._values[prop] += clip._values[prop]

  _changed_sampling = []

  def __getitem__(self, i):
    """Helper to convert the frame at the given index to a single data
    frame for JSON output
    """
    clip = Clip()
    for f in dir(self):
      desc = getattr(self, f)
      if f in self._values and desc:
        if self._params[f].sampling == Sampling.REGULAR:
          # Temporarily set it static so it passes validation
          self._params[f].sampling = Sampling.STATIC
          setattr(clip, f, desc[i])
          self._changed_sampling.append(f)
        else:
          setattr(clip, f, desc)
    return clip
  
  def _reset_sampling(self):
    """Used in conjunction with __getitem__ to reset the Clip's sampling
    back to default
    """
    for f in self._changed_sampling:
      self._params[f].sampling = Sampling.REGULAR
    self._changed_sampling = []
  