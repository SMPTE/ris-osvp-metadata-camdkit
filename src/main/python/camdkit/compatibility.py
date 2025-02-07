#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

"""Provisions for compatibility with OpenTrackIO 0.9 release"""

import jsonref

from abc import abstractmethod
from typing import Final, Any, Self
from copy import deepcopy

from pydantic import BaseModel, ValidationError, ConfigDict
from pydantic.json_schema import (GenerateJsonSchema,
                                  JsonSchemaValue,
                                  JsonSchemaMode)

from pydantic_core.core_schema import ModelField

__all__ = [
    'CompatibleBaseModel',
    'BOOLEAN',
    'NONBLANK_UTF8_MAX_1023_CHARS', 'UUID_URN',
    'RATIONAL', 'STRICTLY_POSITIVE_RATIONAL',
    'NON_NEGATIVE_INTEGER', 'STRICTLY_POSITIVE_INTEGER',
    'NON_NEGATIVE_REAL', 'STRICTLY_POSITIVE_REAL',
    'REAL', 'REAL_AT_LEAST_UNITY',
    'PROTOCOL', 'ARRAY', 'GLOBAL_POSITION', 'TRANSFORMS',
    'canonicalize_descriptions'
]


BOOLEAN: Final[str] = """The parameter shall be a boolean."""

NONBLANK_UTF8_MAX_1023_CHARS: Final[str] = \
"""The parameter shall be a Unicode string between 0 and 1023
codepoints.
"""

UUID_URN: Final[str] = \
"""The parameter shall be a UUID URN as specified in IETF RFC 4122.
Only lowercase characters shall be used.
Example: `f81d4fae-7dec-11d0-a765-00a0c91e6bf6`
"""

RATIONAL: Final[str] = \
"""The parameter shall be a rational number where (i) the numerator
is in the range [-2,147,483,648..2,147,483,647] and (ii) the
denominator is in the range (0..4,294,967,295].
"""

STRICTLY_POSITIVE_RATIONAL: Final[str] = \
"""The parameter shall be a rational number whose numerator
is in the range [0..2,147,483,647] and denominator in the range
(0..4,294,967,295].
"""

NON_NEGATIVE_INTEGER: Final[str] = \
"""The parameter shall be a integer in the range (0..4,294,967,295]."""

STRICTLY_POSITIVE_INTEGER: Final[str] = \
"""The parameter shall be a integer in the range (1..4,294,967,295]."""

REAL: Final[str] = \
    """The parameter shall be a real number."""

NON_NEGATIVE_REAL: Final[str] = \
    """The parameter shall be a non-negative real number."""

STRICTLY_POSITIVE_REAL: Final[str] = \
    """The parameter shall be a real number greater than 0."""

REAL_AT_LEAST_UNITY: Final[str]= \
    """The parameter shall be a real number >= 1."""

PROTOCOL: Final[str] = \
"""Protocol name is nonblank string; protocol version is basic x.y.z
semantic versioning string
"""

ARRAY: Final[str] = \
"""The parameter shall be a tuple of items of the class itemClass.
The tuple can be empty
"""

GLOBAL_POSITION: Final[str] = \
    """Each field in the GlobalPosition shall be a real number"""

TRANSFORMS: Final[str] = \
    """Each component of each transform shall contain Real numbers."""

# Attributes of parameters that should be culled from any exported property_schema
ALWAYS_EXCLUDED = ("title",)
EXCLUDED_CAMDKIT_INTERNALS = ("clip_property", "constraints")


def scrub_excluded(d: JsonSchemaValue, unwanted: tuple[str, ...]) -> JsonSchemaValue:
    for key, value in d.items():
        if isinstance(value, dict):
            scrub_excluded(value, unwanted)
    for key in unwanted:
        d.pop(key, None)
    return d


def canonicalize_descriptions(d: JsonSchemaValue) -> JsonSchemaValue:
    """Canonicalize docstrings into PEP8- and PEP 257-compliant form"""
    for key, value in d.items():
        if isinstance(value, dict):
            canonicalize_descriptions(value)
        if "description" in d:
            # PEP8 just says "PEP 257 describes good docstring conventions" and
            # PEP 257 has 13 paragraphs and four examples to try and explain what
            # it means (just for multiline docstrings and indentation thereof).
            # This is not the full canonicalization algorithm given in the second
            # example, but it should be enough.
            no_newlines_at_either_end: str = d["description"].strip()
            compliant = (no_newlines_at_either_end + "\n"
                         if '\n' in no_newlines_at_either_end
                         else no_newlines_at_either_end)
            d["description"] = compliant
    return d


class CompatibleSchemaGenerator(GenerateJsonSchema):

    def model_field_schema(self, schema: ModelField) -> JsonSchemaValue:

        def clip_property_from_schema(mf_schema: ModelField) -> str | None:
            if ('metadata' in mf_schema
                    and 'pydantic_js_extra' in mf_schema['metadata']
                    and 'clip_property' in mf_schema['metadata']['pydantic_js_extra']):
                return mf_schema['metadata']['pydantic_js_extra']['clip_property']
            return None

        def trapdoor_for_layer_type(layer_type: str) -> tuple[str | None, bool]:
            # First returned value is name of trapdoor; second is whether we need to index (at 0) into it
            table = {'default': ('schema', False),
                     'nullable': ('schema', False),
                     'tuple': ('items_schema', True),
                     'model': ('schema', False),
                     'function-before': ('schema', False),
                     'function-after': ('schema', False),
                     'model-field': ('schema', False),
                     'model-fields': ('fields', False)}
            try:
                return table[layer_type]
            except KeyError:
                return None, False

        def find_layer(layer_schema: dict[str, Any],
                       sought_layer_type: str) -> dict[str, Any] | None:
            """From the given layer, descend through a series of trapdoors
            (which will have different names, depending on the layer)
            until we reach a layer of the sought type, and return it"""
            current_layer: dict[str, Any] | list = layer_schema
            while True:
                if "type" in current_layer:
                    current_layer_type = current_layer["type"]
                    if current_layer_type == sought_layer_type:
                        return current_layer
                    trapdoor, must_index = trapdoor_for_layer_type(current_layer_type)
                    if trapdoor:
                        if trapdoor in current_layer:
                            current_layer = current_layer[trapdoor]
                            if must_index:
                                current_layer = current_layer[0]
                        else:
                            raise RuntimeError(f"schema layer of type {current_layer_type}"
                                               f" missing expected trapdoor {trapdoor}")
                    else:
                        return None
                else:
                    return None

        def remove_layer(layer_schema: dict[str, Any],
                         layer_to_be_removed) -> None:
            current_layer: dict[str, Any] | list = layer_schema
            while isinstance(current_layer, dict):
                current_layer_type = current_layer["type"]
                trapdoor, must_index = trapdoor_for_layer_type(current_layer_type)
                if trapdoor:
                    if trapdoor in current_layer:
                        if current_layer == layer_to_be_removed:
                            # print(f"removing layer of type {current_layer_type}")
                            layer_below = current_layer[trapdoor]
                            if must_index:
                                layer_below = layer_below[0]
                            current_keys = list(current_layer.keys())
                            # TODO re-evaluate whether this is too fragile to keep. The effect is
                            #   to merge the lower layer keys into what's coming up. If what's
                            #   coming up has the same key but a different value, it wins.
                            #   The hazard is a container with at most two things is wrapped around
                            #   a container with at least four things, so you end up with a merged
                            #   min_length of 4 and max_length of 2.
                            merged_not_popped_keys: set[str] = {"min_length", "max_length"}
                            for k in current_keys:
                                if k not in merged_not_popped_keys:
                                    # print(f"popped key {k} for type {current_layer_type}")
                                    current_layer.pop(k)
                                else:
                                    pass
                                    # print(f"skipped pop of key {k} for type {current_layer_type}")
                            for k, v in layer_below.items():
                                current_layer[k] = v
                            return
                    else:
                        raise RuntimeError(f"schema layer of type {current_layer_type}"
                                           f" missing expected trapdoor {trapdoor}")
                    current_layer = current_layer[trapdoor]
                else:
                    raise RuntimeError(f"can't remove layer of type {current_layer_type}"
                                       f" because we don't know how to hoist up the layer"
                                       f" underneath it")

        removed_tuple_layer: bool = False
        mutable_schema: ModelField = deepcopy(schema)
        while True:
            removed_layer: bool = False
            if default_layer := find_layer(mutable_schema, 'default'):
                remove_layer(mutable_schema, default_layer)
                removed_layer = True
            if nullable_layer := find_layer(mutable_schema, 'nullable'):
                remove_layer(mutable_schema, nullable_layer)
                removed_layer = True
            if tuple_layer := find_layer(mutable_schema, 'tuple'):
                if  clip_property_from_schema(mutable_schema) and not removed_tuple_layer:
                    remove_layer(mutable_schema, tuple_layer)
                    removed_layer = True
                    removed_tuple_layer = True
            if not removed_layer:
                break

        json_schema: JsonSchemaValue = super().model_field_schema(mutable_schema)
        return json_schema

    def sort(
            self, value: JsonSchemaValue, parent_key: str | None = None
    ) -> JsonSchemaValue:
        """No-op, we don't want to sort schema values at all."""
        return value

    @abstractmethod
    def cleanup(self, schema: JsonSchemaValue) -> None:
        raise NotImplementedError()

    def generate(self, schema: JsonSchemaValue, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema = jsonref.replace_refs(json_schema, proxies=False, merge_props=True)
        self.cleanup(json_schema)
        canonicalize_descriptions(json_schema)
        return json_schema

class InternalCompatibleSchemaGenerator(CompatibleSchemaGenerator):
    def cleanup(self, schema: JsonSchemaValue) -> None:
        scrub_excluded(schema, ALWAYS_EXCLUDED)

class ExternalCompatibleSchemaGenerator(CompatibleSchemaGenerator):
    def cleanup(self, schema: JsonSchemaValue) -> None:
        scrub_excluded(schema, ALWAYS_EXCLUDED + EXCLUDED_CAMDKIT_INTERNALS)


# For compatibility with existing code
class CompatibleBaseModel(BaseModel):
    """Base class for all camdkit parameters."""

    # TODO: look into using alias generator
    model_config = ConfigDict(populate_by_name=True,
                              validate_assignment=True,
                              use_enum_values=True,
                              extra="forbid",
                              use_attribute_docstrings=True)

    @classmethod
    def validate(cls, value:Any) -> bool:
        try:
            cls.model_validate(value)
            return True
        except ValidationError:
            return False

    @classmethod
    def to_json(cls, model_or_tuple: Self | tuple):
        def inner(one_or_many: Self | tuple):
            if isinstance(one_or_many, tuple):
                return tuple([inner(e) for e in one_or_many])
            return one_or_many.model_dump(by_alias=True,
                                            exclude_none=True,
                                            exclude_defaults=True,
                                            exclude={"canonical_name",
                                                     "sampling",
                                                     "units",
                                                     "section"})
        return inner(model_or_tuple)

    @classmethod
    def from_json(cls, json_or_tuple: JsonSchemaValue | tuple[Any, ...]) -> Any:
        """Return a validated object from a JSON dict, or tuple of validated objects
        from a tuple of JSON dicts, or a tuple of tuples of validated objects from
        a tuple of tuples of JSON dicts, or ... it's basically JSON all the way down
        """
        def inner(value) -> cls | tuple[cls, ...]:
            if isinstance(value, dict) and all([type(k) == str for k in value.keys()]):
                return cls.model_validate(value)
            elif isinstance(value, tuple):
                return tuple([inner(v) for v in value])
            else:
                raise ValueError(f"unhandled type {type(value)} supplied to"
                                 f" {cls.__name__}.from_json()")
        return inner(json_or_tuple)

    @classmethod
    def make_json_schema(cls, mode: JsonSchemaMode = 'serialization',
                         exclude_camdkit_internals: bool = True) -> JsonSchemaValue:
        schema = cls.model_json_schema(schema_generator=(ExternalCompatibleSchemaGenerator
                                                         if exclude_camdkit_internals
                                                         else InternalCompatibleSchemaGenerator),
                                       mode = mode)
        schema.pop("$defs", None)
        return schema
