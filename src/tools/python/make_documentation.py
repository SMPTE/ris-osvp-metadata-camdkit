import typing
import sys
import json
import camdkit.model
import camdkit.red.reader
import camdkit.arri.reader
import camdkit.venice.reader
import camdkit.canon.reader

_INTRODUCTION = """# OSVP Clip documentation

## Introduction

The OSVP Clip (clip) is a collection of metadata parameters sampled over a
specified duration. Each parameter is either:

* static: the parameter has at constant value over the duration of the clip
* dynamic: the parameter is sampled at regular intervals over the duration of the clip

Each parameter is identified by a unique name. It also has a general description
as well as a specific set of constraints.

## Parameters

"""

_COVERAGE = {
  "RED" : [],
  "ARRI" : [],
  "Sony" : []
}

def generate_documentation(fp: typing.TextIO):
  doc = camdkit.model.Clip.make_documentation()

  fp.write(_INTRODUCTION)

  for p in doc:
    fp.write(f"### `{p['canonical_name']}`\n")
    fp.write("\n")
    fp.write("#### Description\n")
    fp.write("\n")
    fp.write(p["description"])
    fp.write("\n")
    fp.write("\n")

    fp.write("#### Units\n")
    fp.write("\n")
    fp.write(p["units"] if p["units"] is not None else "n/a")
    fp.write("\n")
    fp.write("\n")

    fp.write("#### Sampling\n")
    fp.write("\n")
    fp.write(p["sampling"])
    fp.write("\n")
    fp.write("\n")

    fp.write("#### Constraints\n")
    fp.write("\n")
    fp.write(p["constraints"])
    fp.write("\n")
    fp.write("\n")

  fp.write("## JSON Schema\n")
  fp.write("\n")
  fp.write("```")
  json.dump(camdkit.model.Clip.make_json_schema(), fp, indent=2)
  fp.write("\n")
  fp.write("```")
  fp.write("\n")

  # Reader coverage

  fp.write("## Reader coverage\n")
  fp.write("\n")
  fp.write("The following table indicates the camera parameters supported by each of the readers.\n")
  fp.write("\n")

  # Parameter names

  parameter_names = tuple(e["canonical_name"] for e in doc)
  fp.write(f"| Reader      | {' | '.join(parameter_names)} |\n")
  fp.write(f"| ----------- | {'----------- |' * len(parameter_names)}\n")

  def _print_reader_coverage(fp, reader_name, doc, clip):
    fp.write(f"| {reader_name} |")
    for p in doc:
      if getattr(clip, p["python_name"], None) is not None:
        fp.write(" + |") 
      else:
        fp.write(" |")
    fp.write("\n")

  # RED reader

  with open("src/test/resources/red/A001_C066_0303LZ_001.static.csv", "r", encoding="utf-8") as type_3_file, \
    open("src/test/resources/red/A001_C066_0303LZ_001.frames.csv", "r", encoding="utf-8") as type_5_file:
    clip = camdkit.red.reader.to_clip(type_3_file, type_5_file)

  _print_reader_coverage(fp, "RED", doc, clip)

  # ARRI reader

  clip = camdkit.arri.reader.to_clip("src/test/resources/arri/B001C001_180327_R1ZA.mov.csv")
  _print_reader_coverage(fp, "ARRI", doc, clip)

  # Venice reader

  with open("src/test/resources/venice/D001C005_210716AGM01.xml", "r", encoding="utf-8") as static_file, \
    open("src/test/resources/venice/D001C005_210716AG.csv", "r", encoding="utf-8") as dynamic_file:
    clip = camdkit.venice.reader.to_clip(static_file, dynamic_file)

  _print_reader_coverage(fp, "Venice", doc, clip)

  # Canon reader

  with open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Static.csv", "r", encoding="utf-8") as static_csv, \
    open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Frames.csv", "r", encoding="utf-8") as frame_csv:
    clip = camdkit.canon.reader.to_clip(static_csv, frame_csv)

  _print_reader_coverage(fp, "Canon", doc, clip)

if __name__ == "__main__":
  generate_documentation(sys.stdout)
