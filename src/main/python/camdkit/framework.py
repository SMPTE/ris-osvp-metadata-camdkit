# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import typing
import numbers
from fractions import Fraction
from enum import Enum
import dataclasses
import re
import importlib

INT_MAX = 2147483647 # 2^31 - 1
INT_MIN = -2147483648 # -2^31
UINT_MAX = 4294967295 # 2^32 - 1
UINT48_MAX = 281474976710655 # 2^48 - 1


class Sampling(Enum):
  STATIC = "Static"   # Data that does not change for a Clip or across many Frames
  REGULAR = "Regular" # Data that appears at regular intervals in a Clip

@dataclasses.dataclass
class Dimensions:
  """Height and width of a rectangular area"""
  height: numbers.Real
  width: numbers.Real

@dataclasses.dataclass
class Orientations:
  """Horizontal and vertical measurements"""
  horizontal: numbers.Real
  vertical: numbers.Real

@dataclasses.dataclass
class Vector3:
  """3 doubles x,y,z to encode - for example - a location or a
  translation.
  """
  x: typing.Optional[numbers.Real]
  y: typing.Optional[numbers.Real]
  z: typing.Optional[numbers.Real]

@dataclasses.dataclass
class Rotator3:
  """3 doubles pan, tilt, roll to encode - for example - a camera
  rotation.
  """
  pan: typing.Optional[numbers.Real]
  tilt: typing.Optional[numbers.Real]
  roll: typing.Optional[numbers.Real]

@dataclasses.dataclass
class Transform:
  """A translation, rotation and scale. 'transformId' and
  'parentTransformId' fields enable geometry chains
  """
  translation: Vector3
  rotation: Rotator3
  scale: typing.Optional[Vector3] = None
  transformId: typing.Optional[str] = None
  parentTransformId: typing.Optional[str] = None

@dataclasses.dataclass
class FizEncoders:
  """Normalised FIZ encoder values"""
  focus: typing.Optional[numbers.Real] = None
  iris: typing.Optional[numbers.Real] = None
  zoom: typing.Optional[numbers.Real] = None

@dataclasses.dataclass
class RawFizEncoders:
  """Unnormalised FIZ encoder values"""
  focus: typing.Optional[int] = None
  iris: typing.Optional[int] = None
  zoom: typing.Optional[int] = None

@dataclasses.dataclass
class ExposureFalloff:
  """Coefficients for the calculation of exposure fall-off"""
  a1: float
  a2: typing.Optional[float] = None
  a3: typing.Optional[float] = None

@dataclasses.dataclass
class Distortion:
  """Coefficients for the calculation of radial and (optionally)
  tangential lens distortion
  """
  radial: typing.Tuple[float]
  tangential: typing.Optional[typing.Tuple[float]] = None

@dataclasses.dataclass
class PerspectiveShift:
  """Shift in x and y of the centre of perspective projection of the
  virtual camera
  """
  x: float
  y: float
  
@dataclasses.dataclass
class DistortionShift:
  """Shift in x and y of the centre of distortion of the virtual camera
  """
  x: float
  y: float

@dataclasses.dataclass
class GlobalPosition:
  """Global ENU and geodetic coordinates"""
  E: float
  N: float
  U: float
  lat0: float
  lon0: float
  h0: float

@dataclasses.dataclass
class Timestamp:
  """48-bit integer representing seconds, 32-bit integer representing
  nanoseconds, and (optionally) an optional 32-bit integer representing
  attoseconds elapsed since 00:00 January 1st 1970 epoch.
  Reference: https://datatracker.ietf.org/doc/html/rfc8877
  """

  seconds: int
  nanoseconds: int
  attoseconds: typing.Optional[int] = None

@dataclasses.dataclass
class VersionedProtocol:
  """A pair of protocol name and protocol version number (though
  'number' should not be seen as a restriction to a numeric character
  set. Both must be specified as strings with strictly positive length.
  The version must be specified as three integers separated by '.'
  characters, and embody the major, minor and patch meanings of
  semantic versioning.
  """
  name: str
  version: str

class BaseEnum(Enum):
  """Base class for enumerations"""

  def __str__(self):
    return self.value

class SampleTypeEnum(BaseEnum):
  """Enumeration for sample types"""

  STATIC = "static"
  DYNAMIC = "dynamic"

class SynchronizationSourceEnum(BaseEnum):
  """Enumeration for synchronization sources"""

  GENLOCK = "genlock"
  VIDEO_IN = "videoIn"
  PTP = "ptp"
  NTP = "ntp"

@dataclasses.dataclass
class SynchronizationOffsets:
  """Data structure for synchronization offsets"""

  translation: typing.Optional[float] = None		
  rotation: typing.Optional[float] = None		
  lens_encoders: typing.Optional[float] = None

  def validate(self):
    return all([isinstance(self.translation, float), 
                isinstance(self.rotation, float),
                isinstance(self.lens_encoders, float)])
  
  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {
      "translation": value.translation,
      "rotation": value.rotation,
      "lensEncoders": value.lens_encoders
    }

@dataclasses.dataclass
class SynchronizationPTP:
  """Data structure for PTP synchronization"""

  domain: typing.Optional[int] = None
  master: typing.Optional[str] = None
  offset: typing.Optional[float] = None
  
  def validate(self):
    return all([isinstance(self.master, str), 
                isinstance(self.offset, float),
                isinstance(self.domain, int)])
  
  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

class TimingModeEnum(BaseEnum):
  """Enumeration for sample timing modes"""

  INTERNAL = "internal"
  EXTERNAL = "external"

class TimecodeFormat:
  """The timecode format is defined as a rational frame rate and drop
  frame flag. Where an interlaced signal is described, the oddField flag
  indicates which field (odd or even) is referred to by the timecode.
  """

  frame_rate: numbers.Rational
  drop_frame: bool = False
  odd_field: bool = True

  def __init__(self, in_frame_rate: numbers.Rational,
               in_drop_frame: bool = False,
               in_odd_field: bool = True):
    # Constructor for convenience
    if in_frame_rate <= 0:
      raise ValueError
    self.frame_rate = in_frame_rate
    self.drop_frame = in_drop_frame
    self.odd_field = in_odd_field

  def to_int(self):
    return self.frame_rate.__ceil__()
  
  def __str__(self):
    return f"{str(self.frame_rate)}{'D' if self.drop_frame else ''}"
  
  def __eq__(self, other):
      if isinstance(other, self.__class__):
          return self.__dict__ == other.__dict__
      else:
          return False

  def __ne__(self, other):
      return not self.__eq__(other)

@dataclasses.dataclass
class Timecode:
  """Timecode is a standard for labeling individual frames of data in
  media systems.
  """
  
  hours: int
  minutes: int
  seconds: int
  frames: int
  format: TimecodeFormat

  def __str__(self):
    return (f"{self.hours:>02}:{self.minutes:>02}"
            f":{self.seconds:>02}:{self.frames:>02}")

@dataclasses.dataclass
class Synchronization:
  """Data structure for synchronization data"""

  frequency: numbers.Rational
  locked: bool
  source: SynchronizationSourceEnum
  offsets: typing.Optional[SynchronizationOffsets] = None
  present: typing.Optional[bool] = None
  ptp: typing.Optional[SynchronizationPTP] = None

class Parameter:
  """Metadata parameter base class"""

  @staticmethod
  def validate(value) -> bool:
    raise NotImplementedError

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    raise NotImplementedError

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    raise NotImplementedError

  @staticmethod
  def make_json_schema() -> dict:
    raise NotImplementedError

class IntegerDimensionsParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The height and width shall be each be an integer in the range
    [0..2,147,483,647].
    """

    if not isinstance(value, Dimensions):
      return False

    if (not isinstance(value.height, numbers.Integral)
            or not isinstance(value.width, numbers.Integral)):
      return False

    if (value.height < 0
            or value.width < 0
            or value.height > INT_MAX
            or value.width > INT_MAX):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Dimensions(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": [
          "height",
          "width"
      ],
      "properties": {
        "height": {
            "type": "integer",
            "minimum": 0,
            "maximum": 2147483647
        },
        "width": {
            "type": "integer",
            "minimum": 0,
            "maximum": 2147483647
        }
      }
    }

class BooleanParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a boolean."""
    return isinstance(value, bool)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return bool(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "boolean"
    }

class StringParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a Unicode string betwee 0 and 1023
    codepoints.
    """
    return isinstance(value, str) and len(value) < 1024

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "string",
      "minLength": 1,
      "maxLength": 1023
    }
  
class ArrayParameter(Parameter):

  item_class = None

  def validate(self, value) -> bool:
    """The parameter shall be a tuple of items of the class itemClass.
    The tuple can be empty
    """

    if self.item_class is None:
      return False
    if not isinstance(value, tuple):
      return False
    for item in value:
      if (not isinstance(item, self.item_class)
              and not self.item_class.validate(item)):
        return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return list(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return tuple(value)

  def make_json_schema(self) -> dict:
    if hasattr(self.item_class, "make_json_schema"):
      return { "type": "array", "items": self.item_class.make_json_schema() }
    name = self.item_class.__name__
    if name == "float": name = "number"
    return { "type": "array", "items": { "type": name } }

_UUID_RE_STRING = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

class UUIDURNParameter(Parameter):
  _UUID_RE = re.compile(f"urn:uuid:{_UUID_RE_STRING}")

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a UUID URN as specified in IETF RFC 4122.
    Only lowercase characters shall be used.
    Example: `f81d4fae-7dec-11d0-a765-00a0c91e6bf6`
    """
    return isinstance(value, str) and UUIDURNParameter._UUID_RE.match(value)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "string",
      "pattern": f"^urn:uuid:{_UUID_RE_STRING}$"
    }

class StrictlyPositiveRationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number whose numerator
    is in the range [0..2,147,483,647] and denominator in the range
    (0..4,294,967,295].
    """

    if not isinstance(value, numbers.Rational):
      return False

    if (value.numerator <= 0
            or value.denominator <= 0
            or value.numerator > INT_MAX
            or value.denominator > UINT_MAX):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {
      "num": value.numerator,
      "denom": value.denominator
    }

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Fraction(value["num"], value["denom"])

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "properties": {
        "num" : {
          "type": "integer",
          "minimum": 0,
          "maximum": INT_MAX
        },
        "denom" : {
          "type": "integer",
          "minimum": 1,
          "maximum": UINT_MAX
        }
      },
      "required": ["num", "denom" ],
      "additionalProperties": False
    }

class RationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number where (i) the numerator
    is in the range [-2,147,483,648..2,147,483,647] and (ii) the
    denominator is in the range (0..4,294,967,295].
    """

    if not isinstance(value, numbers.Rational):
      return False

    if (value.numerator < INT_MIN
            or value.denominator <= 0
            or value.numerator > INT_MAX
            or value.denominator > UINT_MAX):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return {
      "num": value.numerator,
      "denom": value.denominator
    }

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Fraction(value["num"], value["denom"])

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "properties": {
        "num" : {
          "type": "integer",
          "minimum": INT_MIN,
          "maximum": INT_MAX
        },
        "denom" : {
          "type": "integer",
          "minimum": 1,
          "maximum": UINT_MAX
        }
      },
      "required": ["num", "denom" ],
      "additionalProperties": False
    }

class IntegerParameter(Parameter):
  """Base class for integer parameters"""

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)
  
class NonNegativeIntegerParameter(IntegerParameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a integer in the range (0..4,294,967,295].
    """

    return isinstance(value, numbers.Integral) and value >= 0

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 0,
      "maximum": UINT_MAX
    }
  
class StrictlyPositiveIntegerParameter(IntegerParameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a integer in the range (1..4,294,967,295].
    """

    return isinstance(value, numbers.Integral) and value > 0

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 1,
      "maximum": UINT_MAX
    }
  
class NonNegativeRealParameter(Parameter):
  
  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a non-negative real number."""

    return isinstance(value, numbers.Real) and value >= 0.0

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return float(value)
  
  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "number",
      "minimum": 0.0,
    }

class EnumParameter(StringParameter):
  allowedValues = []

  @classmethod
  def __init_subclass__(cls) -> None:
    # Determine the Enum class from the class name
    module = importlib.import_module("camdkit.framework")
    cls.enum_class = getattr(module, cls.__name__ + "Enum")
    if not issubclass(cls.enum_class, Enum):
      # No related Enum class found
      raise TypeError
    cls.allowedValues = [e.value for e in cls.enum_class]

  def validate(self, value) -> bool:
    """The parameter shall be one of the allowed values."""
    return str(value) in self.allowedValues

  @classmethod
  def from_json(cls, value: typing.Any) -> typing.Any:
    v = cls.enum_class(value)
    return v
  
  def make_json_schema(self) -> dict:
    return {
      "type": "string",
      "enum": self.allowedValues
    }

class TimestampParameter(Parameter):
  """PTP timestamp: 48-bit unsigned integer (seconds), 32-bit unsigned
  integer (nanoseconds), optional 32-bit unsigned integer (attoseconds)
  """

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall contain valid number of seconds, nanoseconds
    and optionally attoseconds elapsed since the start of the epoch.
    """
    if not isinstance(value, Timestamp):
      return False
    if (not (isinstance(value.seconds, int)
             and 0 <= value.seconds <= UINT48_MAX)):
      return False
    if (not (isinstance(value.nanoseconds, int)
             and 0 <= value.nanoseconds <= UINT_MAX)):
      return False
    if value.attoseconds != None:
      if (not (isinstance(value.attoseconds, int)
               and 0 <= value.attoseconds <= UINT_MAX)):
        return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    d = dataclasses.asdict(value)
    if d["attoseconds"] == None:
      del d["attoseconds"]
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Timestamp(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "seconds": {
          "type": "integer",
          "minimum": 0,
          "maximum": UINT48_MAX
        },
        "nanoseconds": {
          "type": "integer",
          "minimum": 0,
          "maximum": UINT_MAX
        },
        "attoseconds": {
          "type": "integer",
          "minimum": 0,
          "maximum": UINT_MAX
        }
      },
      "required": ["seconds", "nanoseconds"]
    }
  
class ParameterContainer:
  def __init__(self) -> None:
    self._values = {k: None for k in self._params}

  @classmethod
  def __init_subclass__(cls) -> None:
    cls._params = {}
    for f in dir(cls):
      desc = getattr(cls, f)

      if not isinstance(desc, Parameter):
        continue

      if not hasattr(desc, "canonical_name") or not isinstance(desc.canonical_name, str):
        raise TypeError("A Parameter must have a canonical_name parameter")

      if not hasattr(desc, "sampling") or not isinstance(desc.sampling, Sampling):
        raise TypeError("A Parameter must have a sampling parameter")

      if not hasattr(desc, "units") or not (desc.units is None or isinstance(desc.units, str)):
        raise TypeError("A Parameter must have a units parameter")
      
      cls._params[f] = desc

      def _gen_getter(f):
        def getter(self):
          return self._values[f]
        return getter
      def _gen_setter(f):
        def setter(self, value):
          if value is not None:
            if self._params[f].sampling is Sampling.STATIC:
              if not self._params[f].validate(value):
                raise ValueError
            elif self._params[f].sampling is Sampling.REGULAR:
              if not (isinstance(value, tuple) and all(self._params[f].validate(s) for s in value)):
                raise ValueError
            else:
              raise ValueError
          self._values[f] = value
        return setter

      setattr(cls, f, property(_gen_getter(f), _gen_setter(f)))

    def _auto__call__init__(self, *a, **kwargs):
      for base in cls.__bases__:
        base.__init__(self, *a, **kwargs)
      ParameterContainer.__init__(self)
      cls._saved_init(self, *a, **kwargs)
    cls._saved_init = cls.__init__
    cls.__init__ = _auto__call__init__

  def to_json(self, index=None) -> dict:
    obj = {}
    for k, desc in self._params.items():
      value = self._values[k]
      # Handle sections
      if hasattr(desc, "section"):
        if value != None:
          if desc.sampling is Sampling.STATIC:
            if "static" not in obj:
              obj["static"] = {}
            if desc.section not in obj["static"]:
              obj["static"][desc.section] = {}
            obj["static"][desc.section][desc.canonical_name] = desc.to_json(value)
          elif desc.sampling is Sampling.REGULAR:
            if desc.section not in obj:
              obj[desc.section] = {}
            if index != None:
              obj[desc.section][desc.canonical_name] = desc.to_json(value[index])
            else:
              obj[desc.section][desc.canonical_name] = tuple(map(desc.to_json, value))
      elif value is None:
        pass
      elif desc.sampling is Sampling.STATIC:
        if "static" not in obj:
          obj["static"] = {}
        obj["static"][desc.canonical_name] = desc.to_json(value)
      elif desc.sampling is Sampling.REGULAR:
        if index != None:
          obj[desc.canonical_name] = desc.to_json(value[index])
        else:
          obj[desc.canonical_name] = tuple(map(desc.to_json, value))
      else:
        raise ValueError

    return obj

  def from_json(self, json_dict: dict, section: str=""):
    for json_key, json_value in json_dict.items():
      if json_key == "static":
        self.from_json(json_dict["static"], section)
      for prop, desc in self._params.items():
        if hasattr(desc, "section") and desc.section == json_key:
          self.from_json(json_dict[json_key], desc.section)
        if desc.canonical_name != json_key:
          continue
        if hasattr(desc, "section") and desc.section != section:
          continue
        if desc.sampling is Sampling.STATIC:
          self._values[prop] = desc.from_json(json_value)
        elif desc.sampling is Sampling.REGULAR:
          self._values[prop] = tuple(map(desc.from_json, json_value))
        else:
          raise ValueError
    return self

  @classmethod
  def make_json_schema(cls) -> dict:
    schema = {
      "$id": "https://opentrackio.org/schema.json",
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "properties": {}
    }
    for _, desc in cls._params.items():
      description = desc.__doc__.replace("\n ", "")
      # Handle sections
      if hasattr(desc, "section"):
        if desc.sampling is Sampling.STATIC:
          if "static" not in schema["properties"]:
            schema["properties"]["static"] = {
              "type": "object",
              "additionalProperties": False,
              "properties": {}
            }
          if desc.section not in schema["properties"]["static"]["properties"]:
            schema["properties"]["static"]["properties"][desc.section] = {
              "type": "object",
              "additionalProperties": False,
              "properties": {}
            }
          schema["properties"]["static"]["properties"][desc.section]["properties"][desc.canonical_name] = desc.make_json_schema()
          schema["properties"]["static"]["properties"][desc.section]["properties"][desc.canonical_name]["description"] = description
          if desc.units:
            schema["properties"]["static"]["properties"][desc.section]["properties"][desc.canonical_name]["units"] = desc.units
        elif desc.sampling is Sampling.REGULAR:
          if desc.section not in schema["properties"]:
            schema["properties"][desc.section] = {
              "type": "object",
              "additionalProperties": False,
              "properties": {}
            }
          schema["properties"][desc.section]["properties"][desc.canonical_name] = desc.make_json_schema()
          schema["properties"][desc.section]["properties"][desc.canonical_name]["description"] = description
          if desc.units:
            schema["properties"][desc.section]["properties"][desc.canonical_name]["units"] = desc.units
      elif desc.sampling is Sampling.STATIC:
        schema["properties"]["static"]["properties"][desc.canonical_name] = desc.make_json_schema()
        schema["properties"]["static"]["properties"][desc.canonical_name]["description"] = description
        if desc.units:
          schema["properties"]["static"]["properties"][desc.canonical_name]["units"] = desc.units
      elif desc.sampling is Sampling.REGULAR:
        schema["properties"][desc.canonical_name] = desc.make_json_schema()
        schema["properties"][desc.canonical_name]["description"] = description
        if desc.units:
          schema["properties"][desc.canonical_name]["units"] = desc.units
      else:
        raise ValueError
    return schema

  @classmethod
  def make_documentation(cls) -> dict:
    doc = []
    for k, desc in cls._params.items():
      doc.append({
        "python_name": k,
        "canonical_name": desc.canonical_name,
        "description" : desc.__doc__,
        "constraints" : desc.validate.__doc__,
        "sampling" : str(desc.sampling.value),
        "section": desc.section if hasattr(desc, "section") else "None",
        "units": desc.units if hasattr(desc, "units") else "None"
      })
    return doc
  
  """
  Iteration is useful for representing a clip as a list of frames of data,
  extracting each REGULAR field's tuples into a separate single Clip of
  STATIC data.
  """
  
  def __iter__(self):
    self.i = 0
    self._set_static()
    return self
  
  def __next__(self):
    self.i += 1
    if self.sample_id == None or self.i >= len(self.sample_id):
      self._set_regular()
      raise StopIteration
    return self[self.i]
  
  def _set_static(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.STATIC 

  def _set_regular(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.REGULAR
