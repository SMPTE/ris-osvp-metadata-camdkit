import sys
from pathlib import Path
import json
from jsonschema import validate

from .test_example_regression import CLASSIC_REPO, PYDANTIC_REPO

CLASSIC_SCHEMA_DIR: Path = CLASSIC_REPO / "build" / "opentrackio"
CLASSIC_SCHEMA = CLASSIC_SCHEMA_DIR / "schema.json"

PYDANTIC_SCHEMA_DIR: Path = PYDANTIC_REPO / "build" / "opentrackio"
PYDSNTIC_SCHEMA = PYDANTIC_SCHEMA_DIR / "schema.json"

def test_pydantic_schema_against_classic_schema(self):
    with open(CLASSIC_SCHEMA) as classic_schema_file:
        classic_schema = json.load(classic_schema_file)
        with open(PYDSNTIC_SCHEMA) as pydantic_schema_file:
            pydantic_schema = json.load(pydantic_schema_file)
            self.assertEqual(classic_schema, pydantic_schema)
