#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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
