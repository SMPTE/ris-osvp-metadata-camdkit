#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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

  print(json.dumps(clip.to_json(), indent=2))

if __name__ == "__main__":
  main()
