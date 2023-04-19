#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) Society of Motion Picture and Television Engineers
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

'''Canon CLI tool'''

import json
import argparse
import camdkit.canon.reader

def main():
  parser = argparse.ArgumentParser(description="Convert Canon camera metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'static_csv_path',
    type=str,
    help="Path to CSV file containing static Canon camera metadata"
    )
  parser.add_argument(
    'frame_csv_path',
    type=str,
    help="Path to CSV file containing per-frame Canon camera metadata"
    )

  args = parser.parse_args()

  with open(args.static_csv_path, "r", encoding="utf-8") as static_csv, \
    open(args.frame_csv_path, "r", encoding="utf-8") as frame_csv:
    clip = camdkit.canon.reader.to_clip(static_csv, frame_csv)

  print(json.dumps(clip.to_json(), indent=2))

if __name__ == "__main__":
  main()
