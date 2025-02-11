import sys
import unittest
import json
from pathlib import Path

from src.test.python.test_example_regression import CLASSIC, CURRENT

CLASSIC_SCHEMA_DIR: Path = CLASSIC
CLASSIC_SCHEMA = CLASSIC_SCHEMA_DIR / "schema.json"

CURRENT_SCHEMA_DIR: Path = CURRENT
CURRENT_SCHEMA = CURRENT_SCHEMA_DIR / "schema.json"


class schemaTestCases(unittest.TestCase):

    def test_current_schema_against_classic_schema(self):
        with open(CLASSIC_SCHEMA) as classic_schema_file:
            classic_schema = json.load(classic_schema_file)
            with open(CURRENT_SCHEMA) as current_schema_file:
                current_schema = json.load(current_schema_file)
                with open("/tmp/sorted_classic_schema_file.json", "w") as sclsf:
                    json.dump(classic_schema, sclsf, indent=4, sort_keys=True)
                with open("/tmp/sorted_current_schema_file.json", "w") as scusf:
                    json.dump(current_schema, scusf, indent=4, sort_keys=True)
                self.assertEqual(classic_schema, current_schema)


if __name__ == '__main__':
    unittest.main()
