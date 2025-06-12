# Camera Metadata Toolkit (camdkit)

## Introduction

### Initial project scope: simple camera and lens metadata

`camdkit` is the code embodiment of  the [SMPTE RIS for OSVP camera metadata
model](https://www.smpte.org/rapid-industry-solutions/on-set-virtual-production). `camdkit` exists because code, especially code that passes unit tests, is as unambiguous a reference as we know how to provide. Documentation _should_ describe the metadata the SMPTE RIS for OSVP describes; but if there is any uncertainty in interpreting the documentation, the code exists to precisely state what a metadatum describes and how it is conveyed.

Today `camdkit` supports mapping (or importing, if you will) of metadata from five popular digital cinema cameras into a canonical form; it also supports a mapping of the metadata defined in the *F4* protocol used by tracking system components from Mo-Sys.

There is no current provision in `camdkit` for an inverse mapping, _e.g._ there is nothing in `camdkit` that would take canonical camera and lens data that was imported from the output of a RED camera and produce an equivalent file of ARRI camera and lens data in ARRI's CSV format.

Initially `camdkit` was comprised solely of these forward mappings to a canonical form, the canonical form being a SMPTE-defined Python class, yclept `Clip`, with each accessible metadatum being a Python `property`, the metadata being called 'parameters' in the vocabulary of `camdkit`. This allows one to speak of a `Clip` having a `camera_model` the value of which was the string `"V-Raptor XL 8K"`.

Parameters that are considered to be unchanging throughout the course of a clip are termed 'static parameters'; parameters that can change from one frame to the next are called 'regular' parameters, the implication being that they represent some metadata that are sampled at a regular interval.

### Enlarged scope: OpenLensIO and OpenTrackIO

Early on `camdkit` showed itself to be successful and useful for basic camera and lens metadata, but in developing a common model for lens optics, the group members realized that the larger community of OSVP vendors was not well represented and reached out, in particular, to makers of camera tracking systems. Both Mo-Sys Engineering Ltd and TrackMen GmbH invested considerable effort in clarifying an optical model, which now exists as **OpenLensIO** and can be found (here)[res/OpenLensIO_v0_9_0.pdf]. Further work (with contributions by RIS members from Concept Overdrive, Inc. and Original Syndicate) produced recommendations for OSVP static and regular parameter transport leveraging standards such as the IETF's RTP and associated protocols, and SMPTE's ST 2110 suite. This combination of `camdkit`, OpenLensIO and transport recommendations is termed **OpenTrackingIO**.
  
## `camdkit`'s continued utility as payload generator

If **OpenTrackingIO** is about how to move payload around, and **OpenLensIO** is about the details of a subset of payload semantics for a few key lens metadata (_e.g._ distortion), then where does `camdkit` fit into this enlarged world?

`camdkit` is still the method by which parametric data (static and regular) is canonically represented in applications. It provides for payload validation, serialization and deserialization and for payload self-description and documentation.

The remainder of this document will discuss how to install camdkit, and how to use it at the application (_e.g._ Python object) level. For information on how to transport JSON-serialized `camdkit` data, see the OpenTrackingIO documentation referenced above; for details of the semantics of the lens-related static and regular metadata, including lens distortion models, see the **OpenLensIO** documentation.

### Installation

This is not to say that the tool use below is the only correct way to install `camdkit`, but it is perhaps the simplest.

* clone this repo

`git clone ...`

* install Python (https://www.python.org/)

* install pipenv

`pip install --user pipenv`

* install dependencies

`pipenv install --dev`

* set the PYTHONPATH environment variable to `src/main/python`, e.g.

`export PYTHONPATH=src/main/python`

* convert RED camera files

`pipenv run python src/main/python/camdkit/red/cli.py src/test/resources/red/A001_C066_0303LZ_001.static.csv src/test/resources/red/A001_C066_0303LZ_001.frames.csv`

## `Clip`, the foundational `camdkit` object
The fundamental organizing tool for `camdkit` parameters is the `Clip` object. It holds parameter values, validates any new parameter values to be added or to replace existing values, and handles JSON serialization and deserialization.

Parameter values are accessed or set with simple access as attributes of a clip object.

`camdkit` takes care of translating proper 'snake case' attribute names such as `lens_entrance_pupil_offset` to canonical JSON 'capitalCase' form when the `Clip` object is serialized:

```python
from camdkit.model import Clip
c = Clip()
...
# something here that loads lens data into the Clip object
...
epo_values = clip.lens_entrance_pupil_offset
```
When `epo_values` is serialized, the resulting JSON values look like:
```python
...
  { "entrancePupilOffset":
    [
        4,
        5,
        6,
        7
    ]
  }
...
```

To add more values to regular metadata, which are stored as tuples, simply add new tuples of values:

```python
from camdkit.model import Clip

c = Clip()
c.lens_entrance_pupil_offset = (14.2, 12.4)
print(f"Initial lens EPO values are {c0.lens_entrance_pupil_offset}")
c.lens_entrance_pupil_offset += (31.4, 26.2)
print(f"augmented lens EPO values are {c.lens_entrance_pupil_offset}")
```

### Advanced topics

- Serialization notes

If one is trying to debug an interoperability issue with some tool that examines "bits on the wire", the following note on optimizing serialization to reduce byte count on scarce-bandwidth sets may be useful.

Though initially the group had discussed using various compression schemes to minimize the size of grouped transmitted parameters, eventually it settled on just transmitting the JSON. Keeping the transmitted data 'slim' is aided by two rules for transmission:
- there is no need (and indeed no mechanism) to explicitly represent that a metadata field is undefined; neither for undefined static metadata nor for undefiend regular metadata. As an example, if you don't know the version of firmware installed on a camera's lens (or if it isn't a lens that even _has_ firmware) there is no need to transmit that fact with every sent group of metadata.
- metadata that are defined to have a default value need not be transmitted. As part of sending timecode data, there is a metadatum termed a "sub-frame" useful for indicating which portion of a multipart frame is associated with the accompanying metadata. For interlaced video, this might be the field number, with values 0 and 1. This sub-frame field has a default value of 0. If the metadata pertain to a frame's field 0, there is no need to transmit the sub-frame metadatum; only if the metadata pertain to field 1 does the sub-frame need to be sent. (It bears noting that applications of sub-frame beyond denoting interlaced fields are possible, _cf._ the sub-frame concept in Megapixel's HELIOS LED Processing Platform.)

## Extension and maintenance

The model documentation is [auto-generated](https://ris-pub.smpte.org/ris-osvp-metadata-camdkit/).

For source readers (those modules that convert proprietary metadata into `camdkit` metadata), simply following the model of existing systems, and placing importer source and importer unit test source files alongside existing systems should suffice.

The core implementation model for camdkit is Pydantic; if one is going to add new parameters to the model, the [Pydantic website](https://docs.pydantic.dev/latest/) is a very useful resource, as is the [Python documentation on type hinting](https://docs.python.org/3/library/typing.html#module-typing).
