#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''CLI tool to generate and validate JSON for an example OpenTrackIO recommended static metadata sample'''

import json
from camdkit.examples import get_recommended_static_example

if __name__ == "__main__":
  print(json.dumps(get_recommended_static_example(), indent=2))
