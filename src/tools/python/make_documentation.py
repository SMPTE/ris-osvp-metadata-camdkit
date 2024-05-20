import typing
import sys
import json
import camdkit.model
import camdkit.red.reader
import camdkit.arri.reader
import camdkit.trackerkit
import camdkit.trackerkit.model
import camdkit.venice.reader
import camdkit.canon.reader
import camdkit.trackerkit.mosys.reader

_CLIP_INTRODUCTION = """# OSVP documentation

## Introduction

The OSVP Clip (clip) is a collection of metadata parameters sampled over a
specified duration. Each parameter is either:

* static: the parameter has at constant value over the duration of the clip
* dynamic: the parameter is sampled at regular intervals over the duration of the clip

Each parameter is identified by a unique name. It also has a general description
as well as a specific set of constraints.

The OSVP Frame (frame) is a collection of metadata parameters that is dynamic and has a
synchronous relationship with a video frame. In an OSVP environment this describes live
camera position ('tracking') and lens data.

## Clip Parameters

"""
_FRAME_INTRODUCTION = """

## Frame Parameters 

"""

_COVERAGE = {
  "RED" : [],
  "ARRI" : [],
  "Sony" : []
}

def generate_documentation(fp: typing.TextIO, doc, prefix):

  fp.write(prefix)

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

def generate_schema(fp: typing.TextIO, schema, title):
  fp.write(f"## {title} JSON Schema\n")
  fp.write("\n")
  fp.write("```")
  json.dump(schema, fp, indent=2)
  fp.write("\n")
  fp.write("```")
  fp.write("\n")

def generate_clip_reader_coverage(fp: typing.TextIO, doc):
  fp.write("## Reader coverage\n")
  fp.write("\n")
  fp.write("The following table indicates the camera parameters supported by each of the readers.\n")
  fp.write("\n")

  # Parameter names

  parameter_names = tuple(e["canonical_name"] for e in doc)
  fp.write(f"| Reader      | {' | '.join(parameter_names)} |\n")
  fp.write(f"| ----------- | {'----------- |' * len(parameter_names)}\n")

  def _generate_reader_coverage(fp, reader_name, doc, clip):
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

  _generate_reader_coverage(fp, "RED", doc, clip)

  # ARRI reader

  clip = camdkit.arri.reader.to_clip("src/test/resources/arri/B001C001_180327_R1ZA.mov.csv")
  _generate_reader_coverage(fp, "ARRI", doc, clip)

  # Venice reader

  with open("src/test/resources/venice/D001C005_210716AGM01.xml", "r", encoding="utf-8") as static_file, \
    open("src/test/resources/venice/D001C005_210716AG.csv", "r", encoding="utf-8") as dynamic_file:
    clip = camdkit.venice.reader.to_clip(static_file, dynamic_file)

  _generate_reader_coverage(fp, "Venice", doc, clip)

  # Canon reader

  with open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Static.csv", "r", encoding="utf-8") as static_csv, \
    open("src/test/resources/canon/20221007_TNumber_CanonCameraMetadata_Frames.csv", "r", encoding="utf-8") as frame_csv:
    clip = camdkit.canon.reader.to_clip(static_csv, frame_csv)

  _generate_reader_coverage(fp, "Canon", doc, clip)

if __name__ == "__main__":
  clip_doc = camdkit.model.Clip.make_documentation()
  generate_documentation(sys.stdout, clip_doc, _CLIP_INTRODUCTION)
  generate_clip_reader_coverage(sys.stdout, clip_doc)
  generate_schema(sys.stdout, camdkit.model.Clip.make_json_schema(), "Clip")

  frame_doc = camdkit.trackerkit.model.Frame.make_documentation()
  generate_documentation(sys.stdout, frame_doc, _FRAME_INTRODUCTION)
  generate_schema(sys.stdout, camdkit.trackerkit.model.Frame.make_json_schema(), "Frame")
