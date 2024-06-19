# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import typing
import numbers
from fractions import Fraction
from enum import Enum
import dataclasses
import re

INT_MAX = 2147483647 # 2^31 - 1
INT_MIN = -2147483648 # -2^31
UINT_MAX = 4294967295 # 2^32 - 1
UINT48_MAX = 281474976710655 # 2^48 - 1


class Sampling(Enum):
  STATIC = "Static"   # Data that does not change for a Clip or across many Frames
  REGULAR = "Regular" # Data that appears at regular intervals in a Clip

@dataclasses.dataclass
class Dimensions:
  "Height and width of a rectangular area"
  height: numbers.Real
  width: numbers.Real

@dataclasses.dataclass
class Vector3:
  "3 doubles x,y,z to encode - for example - a location or a translation."
  x: typing.Optional[numbers.Real] = 0.0
  y: typing.Optional[numbers.Real] = 0.0
  z: typing.Optional[numbers.Real] = 0.0

@dataclasses.dataclass
class Rotator3:
  "3 doubles pan, tilt, roll to encode - for example - a camera rotation."
  pan: typing.Optional[numbers.Real] = 0.0
  tilt: typing.Optional[numbers.Real] = 0.0
  roll: typing.Optional[numbers.Real] = 0.0

@dataclasses.dataclass
class Transform:
  "A translation, rotation and scale. 'name' and 'parent' fields enable geometry chains"
  translation: Vector3
  rotation: Rotator3
  scale: typing.Optional[Vector3] = None
  name: typing.Optional[str] = None
  parent: typing.Optional[str] = None

@dataclasses.dataclass
class Timestamp:
  """
  A 48-bit integer representing seconds, and a 32-bit integer representing nanoseconds, and an
  optional 32-bit integer representing attoseconds elapsed since 00:00 January 1st 1970 epoch.
  """
  seconds: int
  nanoseconds: int
  attoseconds: typing.Optional[int] = 0

class TimingMode(Enum):
  INTERNAL = "internal"
  EXTERNAL = "external"
  
  def __str__(self):
    return self.value

class TimecodeFormat(Enum):
  TC_24  = "24"
  TC_24D = "24D"
  TC_25  = "25"
  TC_30  = "30"
  TC_30D = "30D"

  @classmethod
  def to_int(cls, value):
    if value == cls.TC_24 or value == cls.TC_24D: return 24
    if value == cls.TC_25: return 25
    if value == cls.TC_30 or value == cls.TC_30D: return 30
    raise ValueError
  
  @classmethod
  def to_float(cls, value):
    if value == cls.TC_24: return 24.0
    if value == cls.TC_24D: return 23.976
    if value == cls.TC_25: return 25.0
    if value == cls.TC_30: return 30
    if value == cls.TC_30D: return 29.97
    raise ValueError
  
  def __str__(self):
    return self.value
  
  @staticmethod
  def from_string(value):
    return TimecodeFormat(value)

@dataclasses.dataclass
class Timecode:
  "Timecode is a standard for labeling individual frames of data in media systems."
  hours: int
  minutes: int
  seconds: int
  frames: int
  format: TimecodeFormat

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
    """The height and width shall be each be an integer in the range [0..2,147,483,647]."""

    if not isinstance(value, Dimensions):
      return False

    if not isinstance(value.height, numbers.Integral) or not isinstance(value.width, numbers.Integral):
      return False

    if value.height < 0 or value.width < 0 or value.height > INT_MAX or value.width > INT_MAX:
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

class StringParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a Unicode string betwee 0 and 1023 codepoints."""
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

class UUIDURNParameter(Parameter):

  _UUID_RE = re.compile("urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a UUID URN as specified in IETF RFC 4122. Only lowercase characters shall be used.
    Example: `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6`"""
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
      "pattern": '^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    }

class StrictlyPositiveRationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number whose numerator
    is in the range [0..2,147,483,647] and denominator in the range
    (0..4,294,967,295]."""

    if not isinstance(value, numbers.Rational):
      return False

    if value.numerator < 0 or value.denominator <= 0 or value.numerator > INT_MAX or value.denominator > UINT_MAX:
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
          "min": 0,
          "maximum": INT_MAX
        },
        "denom" : {
          "type": "integer",
          "min": 1,
          "maximum": UINT_MAX
        }
      },
      "required": ["num", "denom" ],
      "additionalProperties": False
    }

class RationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number where (i) the numerator is in the
    range [-2,147,483,648..2,147,483,647] and (ii) the denominator is in the
    range (0..4,294,967,295]."""

    if not isinstance(value, numbers.Rational):
      return False

    if value.numerator < INT_MIN or value.denominator <= 0 or value.numerator > INT_MAX or value.denominator > UINT_MAX:
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
    """The parameter shall be a integer in the range (0..2,147,483,647]."""

    return isinstance(value, numbers.Integral) and value >= 0

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 0,
      "maximum": INT_MAX
    }
  
class StrictlyPositiveIntegerParameter(IntegerParameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a integer in the range (1..2,147,483,647]."""

    return isinstance(value, numbers.Integral) and value > 0

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "integer",
      "minimum": 1,
      "maximum": INT_MAX
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
  enum_class = None

  @classmethod
  def __init_subclass__(cls) -> None:
    if cls.enum_class == None:
      # Sub-class must specify the related Enum class
      raise ValueError
    cls.allowedValues = [e.value for e in cls.enum_class]

  def validate(self, value) -> bool:
    """The parameter shall be one of the allowed values."""
    return str(value) in self.allowedValues

  def make_json_schema(self) -> dict:
    return {
      "type": "string",
      "enum": self.allowedValues
    }
  
class TimingModeParameter(EnumParameter):
  sampling = Sampling.REGULAR
  enum_class = TimingMode
  
class TimestampParameter(Parameter):
  sampling = Sampling.REGULAR

  @staticmethod
  def validate(value) -> bool:
    """
    The parameter shall contain valid number of seconds, nanoseconds and optionally
    attoseconds elapsed since the start of the epoch.
    """
    if not isinstance(value, Timestamp):
      return False
    if not (isinstance(value.seconds, int) and value.seconds >= 0 and value.seconds <= UINT48_MAX):
      return False
    if not (isinstance(value.nanoseconds, int) and value.nanoseconds >= 0 and value.nanoseconds <= UINT_MAX):
      return False
    if not (isinstance(value.attoseconds, int) and value.attoseconds >= 0 and value.attoseconds <= UINT_MAX):
      return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

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


class TimecodeParameter(Parameter):
  sampling = Sampling.REGULAR

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
    if not (isinstance(value.frames, int) and value.frames >= 0 and value.frames < TimecodeFormat.to_int(value.format)):
      return False
    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    d = dataclasses.asdict(value)
    d["format"] = str(d["format"])
    return d

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Timecode(value["hours"], value["minutes"], value["seconds"], value["frames"],
                    TimecodeFormat.from_string(value["format"]))

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
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
          "type": "string",
          "enum": ["24", "24D", "25", "30", "30D"]
        }
      }
    }

class TransformsParameter(Parameter):
  sampling = Sampling.REGULAR

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
      transforms += (Transform(**v), )
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
          }
        },
        "required": ["translation", "rotation"]
      }
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

  def to_json(self) -> dict:
    obj = {}
    for k, desc in self._params.items():
      value = self._values[k]
      # Handle sections
      if hasattr(desc, "section"):
        if value != None:
          if desc.section not in obj:
            obj[desc.section] = {}
          obj[desc.section][desc.canonical_name] = desc.to_json(value)
      elif value is None:
        pass
      elif desc.sampling is Sampling.STATIC:
        obj[desc.canonical_name] = desc.to_json(value)
      elif desc.sampling is Sampling.REGULAR:
        obj[desc.canonical_name] = tuple(map(desc.to_json, value))
      else:
        raise ValueError

    return obj

  def from_json(self, json_dict: dict):
    for json_key, json_value in json_dict.items():
      for prop, desc in self._params.items():
        if hasattr(desc, "section") and desc.section == json_key:
          self.from_json(json_dict[json_key])
        if desc.canonical_name != json_key:
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
      # TODO "$id": "https://...",
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "properties": {}
    }
    for _, desc in cls._params.items():
      description = desc.__doc__.replace("\n ", "")
      # Handle sections
      if hasattr(desc, "section"):
        if desc.section not in schema["properties"]:
          schema["properties"][desc.section] = {
            "type": "object",
            "additionalProperties": False,
            "properties": {}
          }
        # Assumes STATIC sampling
        schema["properties"][desc.section]["properties"][desc.canonical_name] = desc.make_json_schema()
        schema["properties"][desc.section]["properties"][desc.canonical_name]["description"] = description
      elif desc.sampling is Sampling.STATIC:
        schema["properties"][desc.canonical_name] = desc.make_json_schema()
        schema["properties"][desc.canonical_name]["description"] = description
      elif desc.sampling is Sampling.REGULAR:
        schema["properties"][desc.canonical_name] = {
          "type": "array",
          "items": desc.make_json_schema(),
          "description": description
        }
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
    if self.transforms == None or self.i >= len(self.transforms):
      self._set_regular()
      raise StopIteration
    return self[self.i]
  
  def _set_static(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.STATIC 

  def _set_regular(self):
    for p in self._params.keys():
      self._params[p].sampling = Sampling.REGULAR
