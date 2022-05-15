#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2022, Sandflow Consulting LLC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Venice CLI tool'''

import json
import argparse
import camdkit.venice.reader

def main():
  parser = argparse.ArgumentParser(description="Convert Sony Venice camera metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'static_xml_path',
    type=str,
    help="Path to the static XML metadata file"
    )
  parser.add_argument(
    'dyn_csv_path',
    type=str,
    help="Path to the per-frame CSV file"
    )

  args = parser.parse_args()

  with open(args.static_xml_path, "r", encoding="utf-8") as static_file, \
    open(args.dyn_csv_path, "r", encoding="utf-8") as dynamic_file:
    clip = camdkit.venice.reader.to_clip(static_file, dynamic_file)

  print(json.dumps(clip.serialize(), indent=2))

if __name__ == "__main__":
  main()
