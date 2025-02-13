#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Types for modeling clips"""
from typing import Annotated, Any, get_type_hints, Callable, Self, Optional

from pydantic import Field, field_validator, BaseModel, ConfigDict
from pydantic.json_schema import JsonSchemaMode, JsonSchemaValue

from camdkit.compatibility import (CompatibleBaseModel,
                                   UUID_URN,
                                   NON_NEGATIVE_INTEGER,
                                   STRICTLY_POSITIVE_RATIONAL,
                                   PROTOCOL,
                                   ARRAY,
                                   GLOBAL_POSITION,
                                   TRANSFORMS)
from camdkit.units import METER, METERS_AND_DEGREES, SECOND
from camdkit.numeric_types import (NonNegativeInt,
                                   StrictlyPositiveRational,
                                   rationalize_strictly_and_positively)
from camdkit.lens_types import StaticLens, Lens
from camdkit.camera_types import StaticCamera
from camdkit.string_types import UUIDURN
from camdkit.tracker_types import StaticTracker, Tracker, GlobalPosition
from camdkit.timing_types import Timing, Sampling
from camdkit.versioning_types import VersionedProtocol
from camdkit.transform_types import Transform

__all__ = ['Clip']

CLIP_SCHEMA_PRELUDE = {
    "$id": "https://opentrackio.org/schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema"
}


class Static(CompatibleBaseModel):
    duration: Annotated[StrictlyPositiveRational | None,
      Field(json_schema_extra={"clip_property": "duration",
                               "constraints": STRICTLY_POSITIVE_RATIONAL,
                               "units": SECOND})] = None
    """Duration of the clip"""

    # noinspection PyNestedDecorators
    @field_validator("duration", mode="before")
    @classmethod
    def coerce_duration_to_strictly_positive_rational(cls, v):
        return rationalize_strictly_and_positively(v)

    camera: StaticCamera = StaticCamera()
    lens: StaticLens = StaticLens()
    tracker: StaticTracker = StaticTracker()

ModelPath = tuple[str, ...]
TraversingFunction = Callable[[str, JsonSchemaValue, ModelPath, str], None]

class Clip(CompatibleBaseModel):

    model_config = ConfigDict(extra="ignore")
    static: Static = Static()

    tracker: Tracker = Tracker()
    timing: Timing = Timing()
    lens: Lens = Lens()

    # The "global_" prefix is here because, without it, we would have BaseModel attributes
    # with the same name, from the user's POV, as the property
    global_protocol: Annotated[tuple[VersionedProtocol, ...] | None,
      Field(alias="protocol",
            json_schema_extra={"clip_property": "protocol",
                               "constraints": PROTOCOL})] = None
    """Name of the protocol in which the sample is being employed, and
    version of that protocol
    """

    global_sample_id: Annotated[tuple[UUIDURN, ...] | None,
      Field(alias="sampleId",
            json_schema_extra={"clip_property": "sample_id",
                               "constraints": UUID_URN})] = None
    """URN serving as unique identifier of the sample in which data is
    being transported.
    """

    global_source_id: Annotated[tuple[UUIDURN, ...] | None,
      Field(alias="sourceId",
            json_schema_extra={"clip_property": "source_id",
                               "constraints": UUID_URN})] = None
    """URN serving as unique identifier of the source from which data is
    being transported.
    """

    global_source_number: Annotated[tuple[NonNegativeInt, ...] | None,
      Field(alias="sourceNumber",
            json_schema_extra={"clip_property": "source_number",
                               "constraints": NON_NEGATIVE_INTEGER})] = None
    """Number that identifies the index of the stream from a source from which
    data is being transported. This is most important in the case where a source
    is producing multiple streams of samples.
    """

    global_related_sample_ids: Annotated[tuple[tuple[UUIDURN, ...], ...] | None,
      Field(alias="relatedSampleIds",
            json_schema_extra={"clip_property": "related_sample_ids",
                               "constraints": ARRAY})] = None
    """List of sampleId properties of samples related to this sample. The
    existence of a sample with a given sampleId is not guaranteed.
    """

    global_global_stage: Annotated[tuple[GlobalPosition, ...] | None,
      Field(alias="globalStage",
            json_schema_extra={"units": METER,
                               "clip_property": "global_stage",
                               "constraints": GLOBAL_POSITION})] = None
    """Position of stage origin in global ENU and geodetic coordinates
    (E, N, U, lat0, lon0, h0). Note this may be dynamic if the stage is
    inside a moving vehicle.
    """

    global_transforms: Annotated[tuple[tuple[Transform, ...], ...] | None,
      Field(alias="transforms",
            min_length=1,
            json_schema_extra={"units": METERS_AND_DEGREES,
                               "clip_property": "transforms",
                               "constraints": TRANSFORMS,
                               "uniqueItems": False})] = None
    """A list of transforms.
    Transforms are composed in order with the last in the list representing
    the X,Y,Z in meters of camera sensor relative to stage origin.
    The Z axis points upwards and the coordinate system is right-handed.
    Y points in the forward camera direction (when pan, tilt and roll are
    zero).
    For example in an LED volume Y would point towards the centre of the
    LED wall and so X would point to camera-right.
    Rotation expressed as euler angles in degrees of the camera sensor
    relative to stage origin
    Rotations are intrinsic and are measured around the axes ZXY, commonly
    referred to as [pan, tilt, roll]
    Notes on Euler angles:
    Euler angles are human readable and unlike quarternions, provide the
    ability for cycles (with angles >360 or <0 degrees).
    Where a tracking system is providing the pose of a virtual camera,
    gimbal lock does not present the physical challenges of a robotic
    system.
    Conversion to and from quarternions is trivial with an acceptable loss
    of precision.
    """

    @classmethod
    def traverse_json_schema(cls,
                             last_model: BaseModel,
                             level: JsonSchemaValue,
                             model_path: ModelPath,
                             function: TraversingFunction) -> None:
        def field_name_for_clip_property(model: BaseModel, clip_property_name: str) -> str:
            for k, v in model.model_fields.items():
                if (v.json_schema_extra
                        and "clip_property" in v.json_schema_extra
                        and v.json_schema_extra["clip_property"] == clip_property_name):
                    return k
            raise RuntimeError(f"Field for clip property {clip_property_name} not found in model {model}")
        if level.get("properties", None):
            for property_name, property_schema in level["properties"].items():
                if "clip_property" in property_schema:
                    field_name = field_name_for_clip_property(last_model, property_schema["clip_property"])
                    function(property_name, property_schema, model_path, field_name,)
                elif "properties" in property_schema:
                    hints = get_type_hints(last_model)
                    next_model = hints[property_name]
                    cls.traverse_json_schema(next_model, property_schema, model_path + (property_name,), function)

    @classmethod
    # def add_property(cls, name: str, model_path: tuple[tuple[str, type], ...]):
    def add_property(cls, clip_property_name: str, model_path: ModelPath, field_name: str):

        def get_through_path(instance):
            obj = instance
            model_fields: list[str] = [f for f in model_path] + [field_name]
            # print(f"in getter, model_fields: {model_fields}")
            for model_field in model_fields:
                try:
                    obj = getattr(obj, model_field)
                except AttributeError:
                    return None
            return obj

        def set_through_path(instance, value: Any) -> None:
            model_class = instance.__class__
            obj = instance
            # print(f"in setter, model_path: {model_path}, field_name: {field_name}")
            if model_path:
                for model_field in model_path:
                    model_class = get_type_hints(model_class)[model_field]
                    # print(f"in setter, model_field: {model_field} model_class: {model_class}")
                    if not hasattr(obj, model_field) or getattr(obj, model_field) is None:
                        defaulted_instance = model_class()
                        # print("in setter, defaulted instance: {defaulted_instance}")
                        setattr(obj, model_field, defaulted_instance)
                    obj = getattr(obj, model_field)
            setattr(obj, field_name, value)

        # print(f"called setattr({cls}, {clip_property_name}, {property(get_through_path, set_through_path)}")
        setattr(cls, clip_property_name, property(get_through_path, set_through_path))
        # print(f"called setattr({cls}, {name}, {property(lambda s: 'foo', lambda s, v: None)}")
        # setattr(cls, name, property(lambda s: 'foo', lambda s, v: None))

    @classmethod
    def setup_clip_properties(cls) -> type:
        def property_adder(property_name: str,
                           property_schema: JsonSchemaValue,
                           model_path: ModelPath,
                           field_name) -> None:
            clip_property_name = property_schema["clip_property"]
            # print(f"calling cls.add_property({clip_property_name}, {property_name}, {model_path})")
            cls.add_property(clip_property_name, model_path, field_name)

        full_schema = cls.make_json_schema(mode='validation', exclude_camdkit_internals=False)
        cls.traverse_json_schema(Clip, full_schema, (), property_adder)
        return cls

    @classmethod
    def make_documentation(cls) -> list[dict[str, str]]:
        documentation: list[dict[str, str]] = []

        def document_clip_property(property_name: str,
                                   property_schema: JsonSchemaValue,
                                   model_path: ModelPath,
                                   field_name: str) -> None:
            # last_step = model_path[-1]
            section: str = model_path[-1]
            # print(f"documenting clip property: {property_schema["clip_property"]}; parents {parents}")
            documentation.append({
                "python_name": property_schema["clip_property"],
                "canonical_name": property_name,
                "description": property_schema["description"],
                "constraints": property_schema["constraints"] if "constraints" in property_schema else None,
                "sampling": (Sampling.STATIC.value.capitalize()
                             if "static" in model_path or property_schema["clip_property"] == "duration"
                             else Sampling.REGULAR.value.capitalize()),
                "section": (section if section and property_schema["clip_property"] != "duration" else "None"),
                "units": property_schema["units"] if "units" in property_schema else "None"
            })

        full_schema = Clip.make_json_schema(mode='validation', exclude_camdkit_internals=False)
        Clip.traverse_json_schema(Clip, full_schema, ('',), document_clip_property)
        return documentation

    @classmethod
    def make_json_schema(cls, mode: JsonSchemaMode = 'serialization',
                         exclude_camdkit_internals: bool = True) -> JsonSchemaValue:
        result = CLIP_SCHEMA_PRELUDE | super(Clip, cls).make_json_schema(mode, exclude_camdkit_internals)
        return result

    def append(self, other: Self) -> None:
        full_schema = Clip.make_json_schema(mode='validation', exclude_camdkit_internals=False)

        def appender(property_name: str,
                     property_schema: JsonSchemaValue,
                     model_path: ModelPath,
                     field_name: str) -> None:
            if "clip_property" in property_schema and 'static' not in model_path:
                clip_property_name = property_schema["clip_property"]
                if getattr(other, clip_property_name):  # anything to copy?
                    if ours := getattr(self, clip_property_name):
                        setattr(self, clip_property_name,
                                getattr(self, clip_property_name) + getattr(other, clip_property_name))
                    else:
                        setattr(self, clip_property_name, getattr(other, clip_property_name))

        Clip.traverse_json_schema(Clip, full_schema, ('',), appender)

    def __getitem__(self, i) -> Self:
        full_schema = Clip.make_json_schema(mode='validation', exclude_camdkit_internals=False)
        result = Clip()

        def extractor(property_name: str,
                      property_schema: JsonSchemaValue,
                      model_path: ModelPath,
                      field_name: str) -> None:
            if "clip_property" in property_schema:
                clip_property_name = property_schema["clip_property"]
                if ours := getattr(self, clip_property_name):
                    setattr(result, clip_property_name,
                            ours if "static" in model_path else (ours[i],))

        Clip.traverse_json_schema(Clip, full_schema, ('',), extractor)
        return result

    def to_json(self, i: Optional[int] = None) -> Self:
        if i != None:
            single_frame_clip: Self =  self[i]
            return CompatibleBaseModel.to_json(single_frame_clip)
        return CompatibleBaseModel.to_json(self)

    def _print_non_none(self):
        full_schema = Clip.make_json_schema(mode='validation', exclude_camdkit_internals=False)

        def non_none_printer(property_name: str,
                             property_schema: JsonSchemaValue,
                             model_path: ModelPath,
                             field_name: str) -> None:
            if "clip_property" in property_schema:
                clip_property_name = property_schema["clip_property"]
                if ours := getattr(self, clip_property_name):
                    print(f"{property_name} : {ours}")

        Clip.traverse_json_schema(Clip, full_schema, ('',), non_none_printer)


Clip.setup_clip_properties()
