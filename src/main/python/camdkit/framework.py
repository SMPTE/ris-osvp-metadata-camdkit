import typing

class Parameter:
  """Metadata parameter base class"""
  @classmethod
  def __init_subclass__(cls) -> None:
    if not hasattr(cls, "canonical_name"):
      raise TypeError("Parameters must has a canonical_name parameter")

  @staticmethod
  def validate(value) -> bool:
    raise NotImplementedError

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    raise NotImplementedError

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    raise NotImplementedError
    
    
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
      obj[desc.canonical_name] = desc.to_json(self._values[k])
    return obj

  def from_json(self, json_dict: dict):
    for k, v in json_dict:
      if k in self._params:
        self._values[k] = self._params[k].from_json(v)