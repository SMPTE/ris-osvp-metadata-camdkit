#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

'''ARRI CLI tool'''

import json
import argparse
import camdkit.arri.reader

def main():
  parser = argparse.ArgumentParser(description="Converts ARRI camera metadata to JSON according to the OSVP Camera Metadata Model.")
  parser.add_argument('csv_path', type=str, help='Path the CSV file extracted using ARRI Meta Extract (AME)')

  args = parser.parse_args()

  model = camdkit.arri.reader.to_clip(args.csv_path)

  print(json.dumps(model.to_json(), indent=2))

if __name__ == "__main__":
  main()
