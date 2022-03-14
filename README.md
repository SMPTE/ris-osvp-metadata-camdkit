# Camera Metadata Toolkit (camdkit)

## Introduction

_THIS IS A WORK IN PROGRESS_

The toolkit implements the [SMPTE RIS OSVP camera metadata
model](https://www.smpte.org/rapid-industry-solutions/on-set-virtual-production).
The objective is to validate the model as well lower barrier to adoption.

```
Camera file from Vendor #1 --
                              \
Camera file from Vendor #2 ------ OSVP metadata model -------- JSON
                              /
Camera file from Vendor #3 --
```

The toolkit works by extracting metadata from various sources, e.g. camera
files, and converting it into a single internal model that follows the metadata
model currently in development by the SMPTE RIS OSVP effort. The internal model
can then be serialized into representations such as JSON.

## How to extend

* source readers, e.g. RED Camera reader at `src/main/python/red`.
* metadata model at `src/main/python/model.py`

## Quick start and demo

* clone this repo

`git clone ...`

* install Python (https://www.python.org/)

* install pipenv

`pip install --user pipenv`

* install dependencies

`pipenv install --dev`

* set the PYTHONPATH environment variable to `src/main/python`, e.g.

`export PYTHONPATH=src/main/python`

* install the REDline camera software (https://www.red.com/downloads)

* convert a sample RED camera files

`pipenv run python src/main/python/camdkit/red/cli.py src/test/resources/red/A001_C066_0303LZ_001.R3D`
