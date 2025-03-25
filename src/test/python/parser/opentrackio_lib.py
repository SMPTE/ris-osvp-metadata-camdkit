# opentrackio_lib.py
#
# Reference code for decoding OpenTrackIO samples
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import json
import math
import struct
from datetime import datetime, timedelta
from enum import Enum
from cbor2 import loads
from jsonschema import validate, ValidationError, SchemaError
from typing import Optional

OTRK_VERSION = {1, 0, 0}
OTRK_IDENTIFIER = b'OTrk' 
OTRK_IDENTIFIER_LENGTH = 4
OTRK_HEADER_LENGTH = 16
OTRK_SOURCE_NUMBER = 1
OTRK_MULTICAST_PREFIX =  f"235.135.1."
OTRK_MULTICAST_PORT = 55555
OTRK_MTU = 1500  # Maximum Transmission Unit (bytes)
OTRK_MAX_PAYLOAD_SIZE = OTRK_MTU - OTRK_HEADER_LENGTH

NTPSERVER = "pool.ntp.org"

class Translation(Enum):
    X = "x"
    Y = "y"
    Z = "z"
    
class Rotation(Enum):
    PAN = "pan"
    TILT = "tilt"
    ROLL = "roll"
    
class TranslationUnit(Enum):
    METER = "m"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    INCH = "in"
    
    def conversion_factor_from_meters(self) -> float:
        conversion_factors = {
            "m": 1.0,
            "cm": 100.0,
            "mm": 1000.0,
            "in": 1000.0 / 25.4,
        }
        return conversion_factors[self.value]
        
class RotationUnit(Enum):
    DEGREE = "deg"
    RADIAN = "rad"
    
    def conversion_factor_from_degrees(self) -> float:
        conversion_factors = {
            "deg": 1.0,
            "rad": math.pi/180
        }
        return conversion_factors[self.value]

class TimeFormat(Enum):
    SECONDS = "sec"
    TIMECODE = "tc"
    STRING = "string"
    ISO8601 = "iso8601"
    
class FocusDistanceUnit(Enum):
    METER = "m"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    INCH = "in"
    
    def conversion_factor_from_mm(self) -> float:
        conversion_factors = {
            "m": 0.001,
            "cm": 0.1,
            "mm": 1.0,
            "in": 1 / 25.4
        }    
        return conversion_factors[self.value]
        
class TimeSource(Enum):
    GENLOCK = "genlock"
    VIDEO_IN = "videoIn"
    PTP = "ptp"
    NTP = "ntp"
    
class PayloadFormat(Enum):
    JSON = 0x01
    CBOR = 0x02

def fletcher16(data: bytes) -> bytes:
    """
    Compute the Fletcher-16 checksum for the given data.
    
    Args:
        data (bytes): Input data for which the checksum is calculated.
    
    Returns:
        bytes: A 2-byte Fletcher-16 checksum.
    """
    sum1 = 0
    sum2 = 0
    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    checksum = (sum2 << 8) | sum1
    return struct.pack('!H', checksum)


class OpenTrackIOProtocol:
    """Class to decode and interpret the OpenTrackIO protocol
    Arguments:
        schema_text: string containing a json schema for the protocol
        verbose: Whether to print extra status during processing"""
    def __init__(self, schema_text=None, verbose=False):
        self.sample_str = None              # the Sample raw JSON
        self.schema_str = schema_text           # the Sample raw JSON
        self.verbose = verbose
        self.schema_text = None             # the Schema raw JSON
        self.trans_mult = TranslationUnit.METER
        self.rot_mult = RotationUnit.DEGREE
        self.pd = None          # the parsed procotol dictionary
        self.sd = None          # the parsed schema dictionary
        self.sample_time_format = TimeFormat.ISO8601
        self.focus_dist_mult = 1.0
        
        if schema_text:
            self.import_schema()

    def import_schema(self):
        """Read the schema which governs the interpretation of the protocol"""
        if self.schema_str:
            try:
                self.sd = json.loads(self.schema_str)
            except json.decoder.JSONDecodeError as e:
                raise OpenTrackIOException(e.msg)
            if not self.sd:
                raise OpenTrackIOException("Error: Failed to parse OpenTrackIO schema file.")
            else:                                   # we have a valid schema
                if self.verbose:
                    print("Parsed the schema JSON successfully.")
                    print("Contents of the parsed JSON schema dict:\n")
                    print(self.sd)
                    print("\n")
        else:
            raise OpenTrackIOException("Error: no schema provided.")

    
    def parse_cbor(self, data):
        if data != None:
            try:
                self.pd = loads(data)
            except Exception as e:
                raise OpenTrackIOException(e.message)
        else:
            raise OpenTrackIOException("Error: CBOR data cannot be empty.")
            
    def parse_json(self, data):
        if data != None:
            try:
                self.pd = json.loads(data)
            except Exception as e:
                raise OpenTrackIOException(e.message)
        else:
            raise OpenTrackIOException("Error: JSON data cannot be empty.")
    
    def validate_json(data, schema):
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise OpenTrackIOException(e.message)
        except SchemaError as e:
            raise OpenTrackIOException(e.message)

    def validate_dict_elements(self, mdict, keys):
        """Validate whether the supplied list of keys are found in the dict"""
        subdict = mdict
        for key in keys:
            if key in subdict:
                subdict = subdict[key]
            else:
                return False
        return True
        
    def get_camera_translation(self, dimension: Translation, cameraname="Camera"):
        if "transforms" in self.pd.keys():
            for tr in self.pd["transforms"]:
                if (cameraname in tr["id"]):
                    if self.verbose:
                        print("found camera, dim = {}, mult factor: {}".format(dimension.value, self.trans_mult))
                    if (dimension == Translation.X):
                        return tr["translation"][Translation.X.value] * self.trans_mult.conversion_factor_from_meters()
                    elif (dimension == Translation.Y):
                        return tr["translation"][Translation.Y.value] * self.trans_mult.conversion_factor_from_meters()
                    elif (dimension == Translation.Z):
                        return tr["translation"][Translation.Z.value] * self.trans_mult.conversion_factor_from_meters()
                    break
        return None

    def get_camera_rotation(self, dimension: Rotation, cameraname="Camera"):
        if "transforms" in self.pd.keys():
           for tr in self.pd["transforms"]:
               if (cameraname in tr["id"]):
                   if (dimension == Rotation.PAN):
                       return tr["rotation"][Rotation.PAN.value] * self.rot_mult.conversion_factor_from_degrees()
                   elif (dimension == Rotation.TILT):
                       return tr["rotation"][Rotation.TILT.value] * self.rot_mult.conversion_factor_from_degrees()
                   elif (dimension == Rotation.ROLL):
                       return tr["rotation"][Rotation.ROLL.value] * self.rot_mult.conversion_factor_from_degrees()
                   break
        return None

    def get_camera_translations(self, cameraname="Camera"):
        """Return 3DOF camera coordinate: (x,y,z)"""
        return (self.get_camera_translation(Translation.X), self.get_camera_translation(Translation.Y), self.get_camera_translation(Translation.Z))
    
    def get_camera_rotations(self, cameraname="Camera"):
        """Return 3DOF camera coordinate: (x,y,z)"""
        return (self.get_camera_rotation(Rotation.PAN), self.get_camera_rotation(Rotation.TILT), self.get_camera_rotation(Rotation.ROLL))

    def get_timecode(self):
        """Return house timecode as a string in LTC format HH:MM:SS:FF"""
        if self.validate_dict_elements(self.pd,["timing","timecode","hours"]):
            hh = '{:02}'.format(int(self.pd["timing"]["timecode"]["hours"]))
            mm = '{:02}'.format(int(self.pd["timing"]["timecode"]["minutes"]))                
            ss = '{:02}'.format(int(self.pd["timing"]["timecode"]["seconds"]))
            ff = '{:02}'.format(int(self.pd["timing"]["timecode"]["frames"]))
            return hh + ':' + mm + ':' + ss + ':' + ff
        else:
            return None
    
    def get_time_source(self):
        if self.validate_dict_elements(self.pd,["timing","synchronization","source"]):
            return TimeSource(self.pd["timing"]["synchronization"]["source"])
        else:
            return TimeSource.NONE
            
    def get_time_server(self):
        if self.validate_dict_elements(self.pd,["timing","synchronization","source"]):
            return self.pd["timing"]["synchronization"]["source"]
        else:
            return None

    def get_sample_time(self, format: Optional[TimeFormat] = None, part=None):
        """Get the PTP/NTP sample time in user-preferred format."""
        if self.validate_dict_elements(self.pd, ["timing", "sampleTimestamp", "seconds"]):
            ssec = int(self.pd["timing"]["sampleTimestamp"]["seconds"])
            nsec = int(self.pd["timing"]["sampleTimestamp"]["nanoseconds"])
        
            # Calculate the total time as seconds plus fractional seconds from nanoseconds and attoseconds
            total_time = ssec + (nsec * 1e-9)
            base_time = datetime(1970, 1, 1) + timedelta(seconds=ssec, microseconds=nsec / 1_000)
        
            if not part:
                t_format = self.sample_time_format
                if format and format != self.sample_time_format:
                    t_format = format
                if t_format == TimeFormat.SECONDS:
                    return total_time
                elif t_format == TimeFormat.TIMECODE:
                    frames = int((nsec * 1e-9) * self.get_timecode_framerate())
                    return f"{base_time.hour:02}:{base_time.minute:02}:{base_time.second:02}:{frames:02}"
                elif t_format == TimeFormat.STRING:
                    return f"year:{base_time.year} day:{base_time.timetuple().tm_yday} hour:{base_time.hour} min:{base_time.minute} sec:{base_time.second} nsec:{nsec}"
                elif t_format == TimeFormat.ISO8601:
                    return base_time.strftime(f"%Y-%jT%H:%M:%S.{nsec}")
            else:
                # Return individual components based on 'part' argument
                parts_map = {
                    'yy': base_time.year,
                    'dd': base_time.timetuple().tm_yday,
                    'hh': base_time.hour,
                    'mm': base_time.minute,
                    'ss': base_time.second,
                    'ns': nsec
                }
                return parts_map.get(part)
        
        return None

    def get_timecode_framerate(self):
        """Frame rate which the house timecode represents"""
        if self.validate_dict_elements(self.pd,["timing","sampleRate","num"]):
            numerator = float(self.pd["timing"]["sampleRate"]["num"])  
            denominator = float(self.pd["timing"]["sampleRate"]["denom"]) 
            return float(numerator / denominator)
        else:
            return None

    def set_translation_units(self, unit: TranslationUnit):
        """Establish user-preferred units for translations. 
        Valid args: m, cm, mm, in"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","transforms","items","properties","translation","units"]):
            schema_units = self.sd["properties"]["transforms"]["items"]["properties"]["translation"]["units"]
        if self.verbose:
            print("Schema says camera translation units are: {}".format(schema_units))
            print("Setting preferred camera translation units to: {0}".format(unit.value))
        if schema_units == "meter":
            self.trans_mult = unit
        elif schema_units == None:
            raise OpenTrackIOException("Error: camera translation units not found in schema.")

    def set_rotation_units(self, unit: RotationUnit):
        """Establish user-preferred units for rotations. 
        Valid args: deg, rad"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","transforms","items","properties","rotation","units"]):
            schema_units = self.sd["properties"]["transforms"]["items"]["properties"]["rotation"]["units"]
        if self.verbose:
            print("Schema says camera rotation units are: {}".format(schema_units))
            print("Setting preferred camera rotation units to: {0}".format(unit.value))
        if schema_units == "degree":
            self.rot_mult = unit
        elif schema_units == None:
            raise OpenTrackIOException("Error: camera rotation units not found in schema.")

    def set_sample_time_format(self, format: TimeFormat):
        """Establish user preference for sample time format.
        Valid args: sec, timecode, string"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","timing","properties","sampleTimestamp","units"]):
            schema_units = self.sd["properties"]["timing"]["properties"]["sampleTimestamp"]["units"]
        if self.verbose:
            print("Schema says sample time units are: {}".format(schema_units))
            print("Setting preferred sample time format to: {0}".format(format.value))
        
        self.sample_time_format = format

    def set_focus_distance_units(self, unit: FocusDistanceUnit):
        """Establish a user-preference for units of focus distance by storing a conversion factor.
        Valid: m, cm, mm, in"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","lens","properties","focusDistance","units"]):
            schema_units = self.sd["properties"]["lens"]["properties"]["focusDistance"]["units"]
        if self.verbose:
            print("Schema says focus distance units are: {}".format(schema_units))
            print("Setting preferred focus distance units to: {}".format(unit.value))
        if schema_units == "millimeter":
            self.focus_dist_mult = unit.conversion_factor_from_mm()
        elif schema_units == None:
            raise OpenTrackIOException("Error: focus distance units not found in schema")

    def get_protocol_name(self):
        """Name of protocol to which this sample conforms"""
        if self.validate_dict_elements(self.pd,["protocol","name"]):
            return str(self.pd["protocol"]["name"])
        else:
            return None

    def get_protocol_version(self):
        """Version of the protocol to which this sample conforms"""
        if self.validate_dict_elements(self.pd,["protocol","version"]):
            return ".".join(str(v) for v in self.pd["protocol"]["version"])
        else:
            return None

    def get_slate(self):
        """The current slate denoting scene,setup,take etc."""
        if self.validate_dict_elements(self.pd,["tracker","slate"]):
            return str(self.pd["tracker"]["slate"])
        else:
            return None

    def get_sensor_dimension_height(self):
        """Return the height of the camera sensor.
        If present in this sample, the 'static' block would have this info"""
        if self.validate_dict_elements(self.pd,["static","camera","activeSensorResolution","height"]):
                height = int(self.pd["static"]["camera"]["activeSensorResolution"]["height"])
                return height
        return None

    def get_sensor_dimension_width(self):
        """Return the width of the camera sensor.
        If present in this sample, the 'static' block would have this info"""
        if self.validate_dict_elements(self.pd,["static","camera","activeSensorResolution","width"]):
            width = int(self.pd["static"]["camera"]["activeSensorResolution"]["width"])
            return width
        else:
            return None
        return None

    def get_sensor_dimension_units(self):
        """Returns the units found in the schema for active sensor dimensions"""
        if self.validate_dict_elements(self.sd,["properties","camera","properties","activeSensorPhysicalDimensions","units"]):
            return str(self.sd["properties"]["camera"]["properties"]["activeSensorPhysicalDimensions"]["units"])
        else:
            return None

    def get_tracking_device_serial_number(self):
        """Return the tracking device serial number.
        If present in this sample, the 'static' block would have this info"""
        if self.validate_dict_elements(self.pd,["static","tracker","serialNumber"]):
            return str(self.pd["static"]["tracker"]["serialNumber"])
        else:
            return None
        return None

    def get_focal_length(self):
        """Return the current lens focal length"""
        if self.validate_dict_elements(self.pd,["lens","focalLength"]):
            return self.pd["lens"]["focalLength"]
        else:
            return None

    def get_focus_distance(self):
        """Return the current lens focus distance"""
        if self.validate_dict_elements(self.pd,["lens","focusDistance"]):
            return float(self.pd["lens"]["focusDistance"]) * self.focus_dist_mult
        else:
            return None

    def get_lens_encoders(self):
        """Returns the lens encoder values"""
        if not self.validate_dict_elements(self.pd,["lens"]):
            raise OpenTrackIOException('Lens data not available.')

        lens_data = self.pd['lens']

        if 'encoders' in lens_data:
            e = lens_data['encoders']
            result = []
            if 'focus' in e:
                result.append(f'Focus: {e["focus"]:.3f}')
            if 'iris' in e:
                result.append(f'Iris: {e["iris"]:.3f}')
            if 'zoom' in e:
                result.append(f'Zoom: {e["zoom"]:.3f}')
            return ', '.join(result)
        elif 'rawEncoders' in lens_data:
            e = lens_data['rawEncoders']
            result = []
            if 'focus' in e:
                result.append(f'Focus: {e["focus"]}')
            if 'iris' in e:
                result.append(f'Iris: {e["iris"]}')
            if 'zoom' in e:
                result.append(f'Zoom: {e["zoom"]}')
            return ', '.join(result)
        else:
            raise OpenTrackIOException('Lens encoder data not available.')
            

class OpenTrackIOException(Exception):
            
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"OpenTrackIOException: {self.message}"
