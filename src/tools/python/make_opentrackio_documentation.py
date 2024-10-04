#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import json, os, shutil
from inspect import getmembers, isfunction

import camdkit.examples
from camdkit.model import Clip
from jinja2 import Environment, FileSystemLoader, select_autoescape

current_path = os.path.dirname(__file__)
templates_path = os.path.join(current_path, "templates")
resources_path = os.path.join(current_path,"..","..","main","resources")
docs_path = os.path.join(current_path,"..","..","..","build","opentrackio")
examples_path = os.path.join(docs_path,"examples")
if not os.path.exists(examples_path):
  os.makedirs(examples_path)

def main():
  template_data = {
    "examples": {},
    "fields": Clip.make_documentation(),
    "schema": json.dumps(Clip.make_json_schema(), indent=2)
  }
  # Generate all the examples
  for function_name, function in getmembers(camdkit.examples, isfunction):
    # Ignore the 'private' functions
    if function_name[0] != "_":
      example_name = function_name[4:]
      file_name = f"{example_name}.json"
      print(f"Generating {file_name}")
      example_json = json.dumps(function(), indent=2)
      template_data["examples"][example_name] = example_json
      f = open(os.path.join(examples_path, file_name), "w")
      f.write(example_json)
      f.close()

  # Generate schema
  schema_file_name = "schema.json"
  print(f"Generating {schema_file_name}")
  schema = camdkit.model.Clip.make_json_schema()
  f = open(os.path.join(docs_path, schema_file_name), "w")
  schema_json = json.dumps(schema, indent=2)
  f.write(schema_json)
  f.close()

  # Generate web docs
  env = Environment(
    loader=FileSystemLoader(templates_path),
    autoescape=select_autoescape()
  )
  template = env.get_template("OpenTrackIO.html")
  html = template.render(template_data)

  print("Generating index.html")
  f = open(os.path.join(docs_path, "index.html"), "w")
  f.write(html)
  f.close()
  print("Publishing static web resources")
  for folder in ["css", "img", "res"]:
    shutil.copytree(os.path.join(resources_path, folder), os.path.join(docs_path, folder), dirs_exist_ok=True)

if __name__ == "__main__":
  main()
