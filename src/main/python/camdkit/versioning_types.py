#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for versioning protocols"""

from typing import Annotated

from camdkit.compatibility import CompatibleBaseModel
from camdkit.numeric_types import SingleDigitInt
from camdkit.string_types import NonBlankUTF8String

from pydantic import Field

__all__ = ['OPENTRACKIO_PROTOCOL_NAME', 'OPENTRACKIO_PROTOCOL_VERSION', 'VersionedProtocol']

OPENTRACKIO_PROTOCOL_NAME = "OpenTrackIO"
OPENTRACKIO_PROTOCOL_VERSION = (1, 0, 1)

VersionComponent = Annotated[int, Field(ge=0, le=9)]

class VersionedProtocol(CompatibleBaseModel):
    name: NonBlankUTF8String
    version: Annotated[tuple[VersionComponent, ...], Field(min_length=3, max_length=3)]

    def __init__(self, name: NonBlankUTF8String, version: tuple[SingleDigitInt, SingleDigitInt, SingleDigitInt]):
        super(VersionedProtocol, self).__init__(name=name, version=version)
        if name != OPENTRACKIO_PROTOCOL_NAME:
            raise ValueError("The only currently accepted name for a versioned protocol"
                             " is {OPENTRACKIO_PROTOCOL_NAME}")
