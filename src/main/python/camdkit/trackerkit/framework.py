# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project


import typing
import numbers
import dataclasses

from camdkit.framework import Parameter, Sampling

@dataclasses.dataclass
class Vector3:
  "3 doubles x,y,z to encode - for example - a location or a translation."
  x: numbers.Real
  y: numbers.Real
  z: numbers.Real
  
class TrackingParameter(Parameter):
  """All tracking parameters are dynamic."""
  sampling = Sampling.DYNAMIC


class Vector3Parameter(TrackingParameter):

  @staticmethod
  def validate(value) -> bool:
    """The x, y, and z shall be each be a Real number."""

    if not isinstance(value, Vector3):
      return False

    if not isinstance(value.x, numbers.Real) or not isinstance(value.y, numbers.Real) or not isinstance(value.z, numbers.Real):
      return False

    return True

  @staticmethod
  def to_json(value: typing.Any) -> typing.Any:
    return dataclasses.asdict(value)

  @staticmethod
  def from_json(value: typing.Any) -> typing.Any:
    return Vector3(**value)

  @staticmethod
  def make_json_schema() -> dict:
    return {
      "type": "object",
      "additionalProperties": False,
      "required": [
          "x",
          "y",
          "z"
      ],
      "properties": {
        "x": {
            "type": "float",
        },
        "y": {
            "type": "float",
        },
        "z": {
            "type": "float",
        }
      }
    }
  