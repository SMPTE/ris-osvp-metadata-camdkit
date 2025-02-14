#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''Mo-Sys CLI tool'''

import json
import argparse
import camdkit.framework
import camdkit.mosys.reader

def main():
  parser = argparse.ArgumentParser(description="Convert Mo-Sys F4 tracking metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'frame_f4_path',
    type=str,
    help="Path to F4 file containing Mo-Sys camera tracking data"
    )

  args = parser.parse_args()

  # First 10 frames
  clip = camdkit.mosys.reader.to_clip(args.frame_f4_path, 10)
  # Print frame 0 of the clip
  print(json.dumps(clip.to_json(0), indent=2))
  
  
if __name__ == "__main__":
  main()
