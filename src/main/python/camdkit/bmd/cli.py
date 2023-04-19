#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''BMD CLI tool'''

import json
import argparse
import camdkit.bmd.reader

def main():
  parser = argparse.ArgumentParser(description="Convert the output of the ExtractMetadata sample \
  tool from the Blackmagic RAW SDK to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument(
    'metadata_path',
    type=str,
    help="Path to the metadata file"
    )
  args = parser.parse_args()

  with open(args.metadata_path, "r", encoding="utf-8") as fp:
    clip = camdkit.bmd.reader.to_clip(fp)

  print(json.dumps(clip.to_json(), indent=2))

if __name__ == "__main__":
  main()
