#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''RED CLI tool'''

import json
import argparse
import camdkit.red.reader

def main():
  parser = argparse.ArgumentParser(description="Convert RED camera metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'meta_3_file_path',
    type=str,
    help="Path to CSV file generated using REDline (`REDline --silent --i <camera_file_path> --printMeta 3`)"
    )
  parser.add_argument(
    'meta_5_file_path',
    type=str,
    help="Path to CSV file generated using REDline (`REDline --silent --i <camera_file_path> --printMeta 5`)"
    )

  args = parser.parse_args()

  with open(args.meta_3_file_path, "r", encoding="utf-8") as type_3_file, \
    open(args.meta_5_file_path, "r", encoding="utf-8") as type_5_file:
    clip = camdkit.red.reader.to_clip(type_3_file, type_5_file)

  print(json.dumps(clip.to_json(), indent=2))

if __name__ == "__main__":
  main()
