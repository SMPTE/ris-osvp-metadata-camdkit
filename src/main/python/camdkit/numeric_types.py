#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Constrained versions of built-in numeric types"""

import numbers
from fractions import Fraction
from typing import Any, Final, Annotated
from pydantic import Field

from camdkit.compatibility import CompatibleBaseModel

__all__ = ['MIN_INT_8', 'MAX_INT_8',
           'MIN_UINT_8', 'MAX_UINT_8',
           'MIN_UINT_32', 'MAX_UINT_32',
           'MIN_INT_32', 'MAX_INT_32',
           'MAX_UINT_48',
           'SingleDigitInt',
           'NonNegative8BitInt', 'StrictlyPositive8BitInt',
           'NonNegativeInt', 'NonNegative48BitInt', 'StrictlyPositiveInt',
           'NonNegativeFloat', 'StrictlyPositiveFloat', 'NormalizedFloat', 'UnityOrGreaterFloat',
           'Rational', 'StrictlyPositiveRational', 'rationalize_strictly_and_positively']

MIN_INT_8: Final[int] = -2**7
MAX_INT_8: Final[int] = 2**7-1
MIN_UINT_8: Final[int] = 0
MAX_UINT_8: Final[int] = 2**8-1
MIN_UINT_32: Final[int] = 0
MAX_UINT_32: Final[int] = 2**32-1
MIN_INT_32: Final[int] = -2**31
MAX_INT_32: Final[int] = 2**31-1
MAX_UINT_48: Final[int] = 2**48-1

type SingleDigitInt = Annotated[int, Field(..., ge=0, le=9, strict=True)]

type NonNegative8BitInt = Annotated[int, Field(..., ge=0, le=MAX_INT_8, strict=True)]

type StrictlyPositive8BitInt = Annotated[int, Field(..., ge=0, le=MAX_UINT_8, strict=True)]

type NonNegativeInt = Annotated[int, Field(..., ge=0, le=MAX_UINT_32, strict=True)]

type NonNegative48BitInt = Annotated[int, Field(..., ge=0, le=MAX_UINT_48, strict=True)]

type StrictlyPositiveInt = Annotated[int, Field(..., ge=1, le=MAX_UINT_32, strict=True)]

type NonNegativeFloat = Annotated[float, Field(..., ge=0, strict=True)]

type StrictlyPositiveFloat = Annotated[float, Field(..., gt=0.0, strict=True)]

type NormalizedFloat = Annotated[float, Field(..., ge=0.0, le=1.0, strict=True)]

type UnityOrGreaterFloat = Annotated[float, Field(..., ge=1.0, strict=True)]

# init methods because by default Pydantic BaseModel doesn't let you use positional arguments,
# and camdkit 0.9 uses that style of object instantiation

class Rational(CompatibleBaseModel):
    num: int = Field(ge=MIN_INT_32, le=MAX_INT_32, strict=True)
    denom: int = Field(ge=1, le=MAX_UINT_32, strict=True)

    def __init__(self, num: int, denom: int) -> None:
        super(Rational, self).__init__(num=num, denom=denom)

    # Not the full set of operations; just enough to pass classic unit tests
    @staticmethod
    def _canonicalize(other: Any):
        if isinstance(other, Rational):
            return other
        elif isinstance(other, StrictlyPositiveRational):
            return Rational(num=other.num, denom=other.denom)
        frac = Fraction(other)  # may well throw TypeError
        return Rational(frac.numerator, frac.denominator)

    def __eq__(self, other: Any) -> bool:
        if other:
            wrapped = Rational._canonicalize(other)
            return self.num == wrapped.num and self.denom == wrapped.denom
        return False

    def __mul__(self, other: Any):
        wrapped = Rational._canonicalize(other)
        return Rational(self.num * wrapped.num, self.denom * wrapped.denom)

    def __rtruediv__(self, other: Any):
        wrapped = Rational._canonicalize(other)
        return Rational(self.num * wrapped.denom, self.denom * wrapped.num)


class StrictlyPositiveRational(CompatibleBaseModel):
    num: int = Field(ge=1, le=MAX_INT_32, strict=True)
    denom: int = Field(ge=1, le=MAX_UINT_32, strict=True)

    def __init__(self, num: int, denom: int, ) -> None:
        super(StrictlyPositiveRational, self).__init__(num=num, denom=denom)

    # Not the full set of operations; just enough to pass classic unit tests
    @staticmethod
    def _canonicalize(other: Any):
        if isinstance(other, StrictlyPositiveRational):
            return other
        elif isinstance(other, Rational):
            return StrictlyPositiveRational(num=other.num, denom=other.denom)
        frac = Fraction(other)  # may well throw TypeError
        return StrictlyPositiveRational(frac.numerator, frac.denominator)

    def __eq__(self, other: Any) -> bool:
        if other:
            wrapped = StrictlyPositiveRational._canonicalize(other)
            return self.num == wrapped.num and self.denom == wrapped.denom
        return False

    def __mul__(self, other: Any):
        wrapped = StrictlyPositiveRational._canonicalize(other)
        return StrictlyPositiveRational(self.num * wrapped.num, self.denom * wrapped.denom)

    def __rtruediv__(self, other: Any):
        wrapped = StrictlyPositiveRational._canonicalize(other)
        return StrictlyPositiveRational(self.num * wrapped.denom, self.denom * wrapped.num)

def rationalize_strictly_and_positively(x: Any) -> StrictlyPositiveRational:
    if x:
        if not isinstance(x, StrictlyPositiveRational):
            if isinstance(x, int) and x <= MAX_INT_32:
                return StrictlyPositiveRational(x, 1)
            elif isinstance(x, numbers.Rational):
                return StrictlyPositiveRational(int(x.numerator), int(x.denominator))
            elif isinstance(x, dict) and len(x) == 2 and "num" in x and "denom" in x:
                return StrictlyPositiveRational(int(x["num"]), int(x["denom"]))
            raise ValueError(f"could not convert input of type {type(x)} to a StrictlyPositiveRational")
    return x
