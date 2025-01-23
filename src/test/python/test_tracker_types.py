import unittest
import json

from pathlib import Path

from pydantic import ValidationError
from pydantic.json_schema import JsonSchemaValue

from camdkit.compatibility import canonicalize_descriptions
from camdkit.string_types import NonBlankUTF8String
from camdkit.tracker_types import StaticTracker, Tracker


def load_classic_camdkit_schema(path: Path) -> JsonSchemaValue:
    with open(path, "r", encoding="utf-8") as file:
        schema = json.load(file)
        canonicalize_descriptions(schema)
        return schema


CLASSIC_TRACKER_SCHEMA_PATH = Path("src/test/resources/model/static_tracker.json")
CLASSIC_TRACKER_SCHEMA: JsonSchemaValue | None = None


def setUpModule():
    global CLASSIC_TRACKER_SCHEMA
    with open(CLASSIC_TRACKER_SCHEMA_PATH, "r", encoding="utf-8") as fp:
        CLASSIC_TRACKER_SCHEMA = json.load(fp)


def tearDownModule():
    pass

class TrackerTestCases(unittest.TestCase):

    def test_tracker_make(self):
        st = StaticTracker()
        self.assertIsNone(st.make)
        with self.assertRaises(ValidationError):
            st.make = 0+0.1j
        with self.assertRaises(ValidationError):
            st.make = ""
        smallest_valid_make: str = "x"
        st.make = "x"
        self.assertEqual(smallest_valid_make, st.make)
        largest_valid_make: str = "x" * 1023
        st.make = largest_valid_make
        self.assertEqual(largest_valid_make, st.make)
        with self.assertRaises(ValidationError):
            st.make = "x" * 1024

    def test_tracker_model_name(self):
        st = StaticTracker()
        self.assertIsNone(st.model)
        with self.assertRaises(ValidationError):
            st.model = 0 + 0.1j
        with self.assertRaises(ValidationError):
            st.model = ""
        smallest_valid_model_name: str = "x"
        st.model = "x"
        self.assertEqual(smallest_valid_model_name, st.model)
        largest_valid_model_name: str = "x" * 1023
        st.model = largest_valid_model_name
        self.assertEqual(largest_valid_model_name, st.model)
        with self.assertRaises(ValidationError):
            st.model = "x" * 1024

    def test_tracker_serial_number(self):
        st = StaticTracker()
        self.assertIsNone(st.serial_number)
        with self.assertRaises(ValidationError):
            st.serial_number = 0+0.1j
        with self.assertRaises(ValidationError):
            st.serial_number = ""
        smallest_valid_serial_number: str = "x"
        st.serial_number = "x"
        self.assertEqual(smallest_valid_serial_number, st.serial_number)
        largest_valid_serial_number: str = "x" * 1023
        st.serial_number = largest_valid_serial_number
        self.assertEqual(largest_valid_serial_number, st.serial_number)
        with self.assertRaises(ValidationError):
            st.serial_number = "x" * 1024

    def test_tracker_firmware_version(self):
        st = StaticTracker()
        self.assertIsNone(st.firmware)
        with self.assertRaises(ValidationError):
            st.firmware = 0+0.1j
        with self.assertRaises(ValidationError):
            st.firmware = ""
        smallest_valid_firmware_version: str = "x"
        st.firmware = "x"
        self.assertEqual(smallest_valid_firmware_version, st.firmware)
        largest_valid_firmware_version: str = "x" * 1023
        st.firmware = largest_valid_firmware_version
        self.assertEqual(largest_valid_firmware_version, st.firmware)
        with self.assertRaises(ValidationError):
            st.firmware = "x" * 1024

    def test_tracker_notes(self):
        t = Tracker()
        self.assertIsNone(t.notes)
        with self.assertRaises(ValidationError):
            t.notes = 0 + 0.1j
        empty_tuple: tuple[NonBlankUTF8String, ...] = ()
        t.notes = empty_tuple
        self.assertEqual(empty_tuple, t.notes)
        with self.assertRaises(ValidationError):
            t.notes = (1,)
        valid_single_note: tuple[NonBlankUTF8String, ...] = ('foo',)
        t.notes = valid_single_note
        self.assertEqual(valid_single_note, t.notes)
        invalid_heterogenous_notes: tuple[NonBlankUTF8String, ...] = ('foo', 0 + 1j)
        with self.assertRaises(ValidationError):
            t.notes = invalid_heterogenous_notes
        valid_two_notes: tuple[NonBlankUTF8String, ...] = ('foo', 'bar')
        t.notes = valid_two_notes
        self.assertEqual(valid_two_notes, t.notes)
        overlong_note: str = "x" * 1024
        invalid_overlong_notes: tuple[NonBlankUTF8String, ...] = (overlong_note,
                                                                  overlong_note)
        with self.assertRaises(ValidationError):
            t.notes = invalid_overlong_notes

    def test_tracker_recording(self):
        t = Tracker()
        self.assertIsNone(t.recording)
        with self.assertRaises(ValidationError):
            t.recording = 0 + 0.1j
        empty_tuple: tuple[bool, ...] = tuple()
        t.recording = empty_tuple
        self.assertEqual(empty_tuple, t.recording)
        with self.assertRaises(ValidationError):
            t.recording = ('foo',)
        valid_single_recording: tuple[bool, ...] = (True,)
        t.recording = valid_single_recording
        self.assertEqual(valid_single_recording, t.recording)
        invalid_heterogenous_recording: tuple[bool, ...] = (True, 0 + 1j)
        with self.assertRaises(ValidationError):
            t.recording = invalid_heterogenous_recording
        valid_two_recording: tuple[bool, ...] = (True, False)
        t.recording = valid_two_recording
        self.assertEqual(valid_two_recording, t.recording)

    def test_tracker_slate(self):
        t = Tracker()
        self.assertIsNone(t.slate)
        with self.assertRaises(ValidationError):
            t.slate = 0 + 0.1j
        empty_tuple: tuple[NonBlankUTF8String, ...] = ()
        t.slate = empty_tuple
        self.assertEqual(empty_tuple, t.slate)
        with self.assertRaises(ValidationError):
            t.slate = (1,)
        valid_single_note: tuple[NonBlankUTF8String, ...] = ('foo',)
        t.slate = valid_single_note
        self.assertEqual(valid_single_note, t.slate)
        invalid_heterogenous_slate: tuple[NonBlankUTF8String, ...] = ('foo', 0 + 1j)
        with self.assertRaises(ValidationError):
            t.slate = invalid_heterogenous_slate
        valid_two_slate: tuple[NonBlankUTF8String, ...] = ('foo', 'bar')
        t.slate = valid_two_slate
        self.assertEqual(valid_two_slate, t.slate)
        overlong_slate: str = "x" * 1024
        invalid_overlong_slates: tuple[NonBlankUTF8String, ...] = (overlong_slate,
                                                                  overlong_slate)
        with self.assertRaises(ValidationError):
            t.slates = invalid_overlong_slates

    def test_tracker_status(self):
        t = Tracker()
        self.assertIsNone(t.status)
        with self.assertRaises(ValidationError):
            t.status = 0 + 0.1j
        empty_tuple: tuple[NonBlankUTF8String, ...] = ()
        t.status = empty_tuple
        self.assertEqual(empty_tuple, t.status)
        with self.assertRaises(ValidationError):
            t.status = (1,)
        valid_single_note: tuple[NonBlankUTF8String, ...] = ('foo',)
        t.status = valid_single_note
        self.assertEqual(valid_single_note, t.status)
        invalid_heterogenous_status: tuple[NonBlankUTF8String, ...] = ('foo', 0 + 1j)
        with self.assertRaises(ValidationError):
            t.status = invalid_heterogenous_status
        valid_two_status: tuple[NonBlankUTF8String, ...] = ('foo', 'bar')
        t.status = valid_two_status
        self.assertEqual(valid_two_status, t.status)
        overlong_status: str = "x" * 1024
        invalid_overlong_statuses: tuple[NonBlankUTF8String, ...] = (overlong_status,
                                                                     overlong_status)
        with self.assertRaises(ValidationError):
            t.status = invalid_overlong_statuses

    def test_static_tracker_schemas_match(self):
        expected_schema: JsonSchemaValue = load_classic_camdkit_schema(Path("src/test/resources/model/static_tracker.json"))
        actual_schema: JsonSchemaValue = StaticTracker.make_json_schema()
        self.assertDictEqual(expected_schema, actual_schema)


if __name__ == '__main__':
    unittest.main()
