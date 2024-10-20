# opentrackio_lib.py
#
# Reference code for decoding OpenTrackIO samples
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import json
import os
import math

class OpenTrackIOProtocol:
    """Class to decode and interpret the OpenTrackIO protocol
    Arguments:
        msg_text: string containing a single json "sample"
        schema_text: string containing a json schema for the protocol
        verbose: Whether to print extra status during processing"""
    def __init__(self, msg_text=None, schema_text=None, verbose=False):
        self.sample_str = msg_text              # the Sample raw JSON
        self.schema_str = schema_text           # the Sample raw JSON
        self.verbose = verbose
        self.schema_text = None             # the Schema raw JSON
        self.trans_mult = 1.0                               # user-preferred units multiplier
        self.rot_mult = 1.0
        self.pd = None          # the parsed procotol dictionary
        self.sd = None          # the parsed schema dictionary
        self.sample_time_format = "sec"
        self.sample_time_formats = ["sec","timecode","string"]
        self.focus_dist_mult = 1.0

    def import_schema(self):
        """Read the schema which governs the interpretation of the protocol"""
        if self.schema_str:
            try:
                self.sd = json.loads(self.schema_str)
            except json.decoder.JSONDecodeError:
                print("Got JSONDecodeError while decoding the sample!")
                self.sd = None
            if not self.sd:
                print("Import_schema(): Failed to parse OpenTrackIO schema file.")
            else:                                   # we have a valid schema
                print("Parsed the schema JSON successfully.")
                if self.verbose:
                    print("Contents of the parsed JSON schema dict:\n")
                    print(self.sd)
                    print("\n")
        else:
            print("ERROR: no schema provided!")
            return -1

    def parse(self):        
        """Ingest the text and store the JSON items in a dictionary"""
        protocol = None
        if self.sample_str != None:        
            print("Parsing JSON string from sample buffer...")  
            try:
                self.pd = json.loads(self.sample_str)
            except:
                print("Parse(): Error. Failed to parse JSON file! Either path incorrect or JSON invalid.")
                exit(-1)
            if not self.pd:
                print("Parse(): Failed to parse OpenTrackIO sample file.")
            else:                                   # we have a OTP message
                print("Parsed the sample JSON successfully.")
                if self.verbose:
                    print("Contents of the parsed sample JSON dict:\n")
                    print(self.pd)
                    print("\n")
        else:
            print("Parse(): Error. No json text provided!")
            return -1

    def validate_dict_elements(self, mdict, keys):
        """Validate whether the supplied list of keys are found in the dict"""
        subdict = mdict
        for key in keys:
            if key in subdict:
                subdict = subdict[key]
            else:
                return False
        return True

    def conversion_factor_from_meters(self,unit_str):
        """Stores the multiplicative conversion factor from meters to user-specified units
        Valid unit specifier strings: m, cm, mm, in"""
        if unit_str == "m":
            return 1.0
        elif unit_str == "cm":
            return 100.0
        elif unit_str == "mm":
            return 1000.0
        elif unit_str == "in":
            return (1000.0/25.4)

    def get_camera_translation(self, dimension):
        """Return a single axis of camera translation, such as: x,y, or z"""
        if "transforms" in self.pd.keys():
            for tr in self.pd["transforms"]:
                if ("Camera" in tr["transformId"]):
                    if self.verbose:
                        print("found camera, dim = {}, mult factor: {}".format(dimension,self.trans_mult))
                    if (dimension == 'x'):
                        return tr["translation"]["x"] * self.trans_mult
                    elif (dimension == 'y'):
                        return tr["translation"]["y"] * self.trans_mult
                    elif (dimension == 'z'):
                        return tr["translation"]["z"] * self.trans_mult
                    break
        return None

    def get_camera_rotation(self, dimension):
        """Return a single axis of camera rotation like pan, tilt, or roll.
        Valid arguments are: p, t, r"""
        if "transforms" in self.pd.keys():
           for tr in self.pd["transforms"]:
               if ("Camera" in tr["transformId"]):
                   if (dimension == 'p'):
                       return tr["rotation"]["pan"] * self.rot_mult
                   elif (dimension == 't'):
                       return tr["rotation"]["tilt"] * self.rot_mult
                   elif (dimension == 'r'):
                       return tr["rotation"]["roll"] * self.rot_mult
                   break
        return None

    def get_camera_translations(self):
        """Return 3DOF camera coordinate: (x,y,z)"""
        return (self.get_trans('X'), self.get_trans('Y'), self.get_trans('Z'))

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

    def get_sample_time(self,part=None):
        """Get the PTP sample time in user-preferred format"""
        if self.validate_dict_elements(self.pd,["timing","sampleTimestamp","seconds"]):
            ssec = int(self.pd["timing"]["sampleTimestamp"]["seconds"])
            nsec = int(self.pd["timing"]["sampleTimestamp"]["nanoseconds"])
            asec = int(self.pd["timing"]["sampleTimestamp"]["attoseconds"])
            # Constants
            epoch = 1970                        # PTP is since this epoch
            spm = 60                            # seconds per minute. Common knowledge, but consistency is important
            sph = 3600                          # seconds per hour
            spd = 86400                         # sec per day
            spy = 31536000                      # sec per year
            # separate into years, days, hours, min, sec
            ydelta = int(ssec / spy)            # years since epoch
            yr = int(epoch + ydelta)            # current year
            sty = int(ssec - (ydelta * spy))    # seconds elapsed this year
            day = int(sty / spd)                # current day of year
            std = int(sty - (day * spd))        # seconds elapsed today (since midnight)
            hr = int(std / sph)                 # hours elapsed today
            mn = int((std - (hr * sph)) / spm)  # remainder minutes
            st = int(std - (hr * sph) - (mn * spm))  # remainder seconds
        if not part:
            if self.sample_time_format == "sec":
                return ssec + (nsec * 0.000000001) + (asec * 0.000000000000000001)
            elif self.sample_time_format == "timecode":             # since midnight
                frm = int((nsec * 0.000000001) * self.get_timecode_framerate())
                return '{:02}'.format(hr) + ":" + '{:02}'.format(mn) + ":" + '{:02}'.format(st) + ":" + '{:02}'.format(frm)
            elif self.sample_time_format == "string":
                return "year:{} day:{} hour:{} min:{} sec:{} nsec:{}".format(yr,day,hr,mn,st,nsec)
        else:
            if part == 'yy':
                return yr
            elif part == 'dd':
                return day
            elif part == 'hh':
                return hr
            elif part == 'mm':
                return mn
            elif part == 'ss':
                return st
            elif part == 'ns':
                return nsec
        return None

    def get_timecode_framerate(self):
        """Frame rate which the house timecode represents"""
        if self.validate_dict_elements(self.pd,["timing","frameRate","num"]):
            numerator = float(self.pd["timing"]["frameRate"]["num"])  
            denominator = float(self.pd["timing"]["frameRate"]["denom"]) 
            return float(numerator / denominator)
        else:
            return None

    def set_translation_units(self,unit_str):
        """Establish user-preferred units for translations. 
        Valid args: m, cm, mm, in"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","transforms","items","properties","translation","units"]):
            schema_units = self.sd["properties"]["transforms"]["items"]["properties"]["translation"]["units"]
        if self.verbose:
            print("Schema says camera translation units are: {}".format(schema_units))
            print("Setting preferred camera translation units to: {0}".format(unit_str))
        if schema_units == "meter":
            self.trans_mult = self.conversion_factor_from_meters(unit_str)
        elif schema_units == None:
            print("Error: camera translation units not found in schema")

    def set_rotation_units(self,unit_str):
        """Establish user-preferred units for rotations. 
        Valid args: deg, rad"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","transforms","items","properties","rotation","units"]):
            schema_units = self.sd["properties"]["transforms"]["items"]["properties"]["rotation"]["units"]
        if self.verbose:
            print("Schema says camera rotation units are: {}".format(schema_units))
            print("Setting preferred camera rotation units to: {0}".format(unit_str))
        if schema_units == "degree":
            if unit_str == "deg":
                self.rot_mult = 1.0
            if unit_str == "rad":
                self.rot_mult = math.pi/180
        elif schema_units == None:
            print("Error: camera rotation units not found in schema")

    def set_sample_time_format(self,format_str):
        """Establish user preference for sample time format.
        Valid args: sec, timecode, string"""
        if self.verbose:
            schema_units = None
            if self.validate_dict_elements(self.sd,["properties","timing","properties","sampleTimestamp","units"]):
                schema_units = self.sd["properties"]["timing"]["properties"]["sampleTimestamp"]["units"]
            print("Schema says sample time units are: {}".format(schema_units))
            print("Setting preferred sample time format to: {0}".format(format_str))
        if (format_str in self.sample_time_formats):
            self.sample_time_format = format_str

    def set_focus_distance_units(self,unit_str):
        """Establish a user-preference for units of focus distance by storing a conversion factor.
        Valid: m, cm, mm, in"""
        schema_units = None
        if self.validate_dict_elements(self.sd,["properties","lens","properties","focusDistance","units"]):
            schema_units = self.sd["properties"]["lens"]["properties"]["focusDistance"]["units"]
        if self.verbose:
            print("Schema says focus distance units are: {}".format(schema_units))
            print("Setting preferred focus distance units to: {}".format(unit_str))
        if schema_units == "millimeter":
            if unit_str == "m":
                self.focus_dist_mult = .001
            elif unit_str == "cm":
                self.focus_dist_mult = 0.1
            elif unit_str == "mm":
                self.focus_dist_mult = 1.0
            elif unit_str == "in":
                self.focus_dist_mult = 1/25.4
        elif schema_units == None:
            print("Error: focus distance units not found in schema")

    def get_protocol_name(self):
        """Name of protocol to which this sample conforms"""
        if self.validate_dict_elements(self.pd,["protocol","name"]):
            return str(self.pd["protocol"]["name"])
        else:
            return None

    def get_protocol_version(self):
        """Version of the protocol to which this sample conforms"""
        if self.validate_dict_elements(self.pd,["protocol","version"]):
            return str(self.pd["protocol"]["version"])
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
