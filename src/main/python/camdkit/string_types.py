#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling constrained strings"""

from typing import Final, Annotated

from pydantic import Field

__all__ = [
  'NonBlankUTF8String',
  'UUIDURN'
]

MAX_STR_LENGTH: Final[int] = 1023
type NonBlankUTF8String = Annotated[str, Field(min_length=1, max_length=MAX_STR_LENGTH)]

UUID_URN_PATTERN: Final[str] = r'^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

type UUIDURN = Annotated[str, Field(pattern=UUID_URN_PATTERN)]
