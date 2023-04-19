# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import typing
import numbers
from fractions import Fraction
from enum import Enum
import dataclasses
import re

INT_MAX = 2147483647 # 2^31 - 1

class Sampling(Enum):
  STATIC = "Static"
  REGULAR = "Regular"

@dataclasses.dataclass
class Dimensions:
  "Height and width of a rectangular area"
  height: numbers.Real
  width: numbers.Real


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
    """The parameter shall be a UUID URN as specified in IETF RFC 4122. Onlyu lowercase characters shall be used.
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

class StrictlyPostiveRationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647]."""

    if not isinstance(value, numbers.Rational):
      return False

    if value.numerator < 0 or value.denominator < 0 or value.numerator > INT_MAX or value.denominator > INT_MAX:
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Fraction(value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "string",
      "regex": "[0-9]{1,10}/[0-9]{1,10}"
    }

class StrictlyPositiveIntegerParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a integer in the range (0..2,147,483,647]."""

    return isinstance(value, numbers.Integral) and value > 0

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
      "maximum": 2147483647
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
      if value is None:
        obj[desc.canonical_name] = None
      elif desc.sampling is Sampling.STATIC:
        obj[desc.canonical_name] = desc.to_json(self._values[k])
      elif desc.sampling is Sampling.REGULAR:
        obj[desc.canonical_name] = tuple(map(desc.to_json, value))
      else:
        raise ValueError

    return obj

  def from_json(self, json_dict: dict):
    for json_key, json_value in json_dict.items():
      for prop, desc in self._params.items():
        if desc.canonical_name != json_key:
          continue
        if desc.sampling is Sampling.STATIC:
          self._values[prop] = desc.from_json(json_value)
        elif desc.sampling is Sampling.REGULAR:
          self._values[prop] = tuple(map(desc.from_json, json_value))
        else:
          raise ValueError

  @classmethod
  def make_json_schema(cls) -> dict:
    schema = {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "properties": {}
    }

    for _, desc in cls._params.items():
      if desc.sampling is Sampling.STATIC:
        schema[desc.canonical_name] = desc.make_json_schema()
      elif desc.sampling is Sampling.REGULAR:
        schema[desc.canonical_name] = {
          "type": "array",
          "items": desc.make_json_schema()
        }
      else:
        raise ValueError

    return schema

  @classmethod
  def make_documentation(cls) -> dict:
    doc = {}
    for _, desc in cls._params.items():
      doc[desc.canonical_name] = {
        "description" : desc.__doc__,
        "constraints" : desc.validate.__doc__,
        "sampling" : str(desc.sampling.value),
        "units": desc.units
      }
    return doc
