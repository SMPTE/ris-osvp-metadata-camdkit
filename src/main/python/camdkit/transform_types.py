#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling of spatial transforms"""
from multiprocessing.context import DefaultContext
from typing import Optional, Annotated

from pydantic import Field

from camdkit.compatibility import CompatibleBaseModel
from camdkit.string_types import NonBlankUTF8String
from camdkit.units import DEGREE, METER

class Vector3(CompatibleBaseModel):
    x: Annotated[float | None, Field()] = None
    y: Annotated[float | None, Field()] = None
    z: Annotated[float | None, Field()] = None

    # class Config:
    #     json_schema_extra = {"units": METER}

    def __init__(self, x: float, y: float, z: float):
        super(Vector3, self).__init__(x=x, y=y, z=z)


class Rotator3(CompatibleBaseModel):
    pan: Annotated[float | None, Field()] = None
    tilt: Annotated[float | None, Field()] = None
    roll: Annotated[float | None, Field()] = None

    # class Config:
    #     json_schema_extra = {"units": DEGREE}

    def __init__(self, pan: float, tilt: float, roll: float):
        super(Rotator3, self).__init__(pan=pan, tilt=tilt, roll=roll)


class Transform(CompatibleBaseModel):
    translation: Annotated[Vector3, Field(json_schema_extra={"units": METER})]
    rotation: Annotated[Rotator3, Field(json_schema_extra={"units": DEGREE})]
    scale: Annotated[Vector3 | None, Field()] = None
    id: Annotated[NonBlankUTF8String | None, Field()] = None

    # Nothing in the original code base initializes Transform objects with
    # positional arguments, thus, no need for one
