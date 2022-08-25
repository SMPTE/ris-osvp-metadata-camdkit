import typing
import numbers
from fractions import Fraction

INT_MAX = 2147483647 # 2^31 - 1

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

  @classmethod
  def get_description(cls) -> str:
    return cls.__doc__

  @classmethod
  def get_constraints(cls) -> str:
    return cls.validate.__doc__

class StringParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    return value is None or isinstance(value, str) and len(value) < 1024

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return str(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return str(value)

class StrictlyPostiveRationalParameter(Parameter):

  @staticmethod
  def validate(value) -> bool:
    """The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647]."""

    if value is None:
      return True

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

class StrictlyPositiveIntegerParameter(Parameter):
  
  @staticmethod
  def validate(value) -> bool:
    return value is None or (isinstance(value, numbers.Integral) and value > 0)

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return value

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return int(value)

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

      if not hasattr(desc, "canonical_name"):
        raise TypeError("A Parameter must have a canonical_name parameter")

      cls._params[f] = desc

      def _gen_getter(f):
        def getter(self):
          return self._values[f]
        return getter
      def _gen_setter(f):
        def setter(self, value):
          if not self._params[f].validate(value):
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
      obj[desc.canonical_name] = desc.to_json(self._values[k]) if value is not None else None
    return obj

  def from_json(self, json_dict: dict):
    for k, v in json_dict.items():
      if k in self._params:
        self._values[k] = self._params[k].from_json(v)

  @classmethod
  def get_documentation(cls) -> dict:
    doc = {}
    for _, desc in cls._params.items():
      doc[desc.canonical_name] = {
        "description" : desc.get_description(),
        "constraints" : desc.get_constraints(),
      }
    return doc
