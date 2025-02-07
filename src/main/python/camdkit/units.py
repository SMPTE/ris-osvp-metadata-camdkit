#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Units for unambiguous annotation of parameters that require them"""

from typing import Final

__ALL__ = [
    'SENSEL', 'PIXEL',
    'MICRON', 'MILLIMETER', 'METER',
    'DEGREE', 'RADIAN',
    'SECOND',
    'HERTZ'
]

SENSEL: Final[str] = "sensel"
PIXEL: Final[str] = "pixel"

MICRON: Final[str] = "micron"
MILLIMETER: Final[str] = "millimeter"
METER: Final[str] = "meter"

DEGREE: Final[str] = "degree"
RADIAN: Final[str] = "radian"

SECOND: Final[str] = "second"

HERTZ: Final[str] = "hertz"

# TODO raise an issue replacing this confusing non-unit with "meters and degrees"
METERS_AND_DEGREES: Final[str] = "meter / degree"
