import typing
import sys
import camdkit.model

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

def generate_documentation(fp: typing.TextIO):
  doc = camdkit.model.Clip.get_documentation()

  fp.write(_INTRODUCTION)

  for name, info in doc.items():
    fp.write(f"### {name}\n")
    fp.write("\n")
    fp.write("#### Description\n")
    fp.write("\n")
    fp.write(info["description"])
    fp.write("\n")
    fp.write("\n")
    fp.write("#### Sampling\n")
    fp.write("\n")
    fp.write(info["sampling"])
    fp.write("\n")
    fp.write("\n")
    fp.write("#### Constraints\n")
    fp.write("\n")
    fp.write(info["constraints"])
    fp.write("\n")
    fp.write("\n")

if __name__ == "__main__":
  generate_documentation(sys.stdout)
