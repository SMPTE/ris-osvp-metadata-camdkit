# opentrackIOlib.py
#
# Reference code for decoding opentrackIO messages
# Copyright (c) 2024 Steve Rosenbluth, RiS OSVP camera tracking committee
#
# License: this code is open-source under the FreeBSD License

import json
import os
import math

# Class to decode and interpret the OTIO protocol
# msg_text: string containing a single json "sample"
# schema_text: string containing a json schema for the protocol
# verbose: Whether to print extra status during processing
class OTProtocol:
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

    # Read the schema which governs the interpretation of the protocol
    def Import_schema(self):
        if self.schema_str:
            try:
                self.sd = json.loads(self.schema_str)
            except json.decoder.JSONDecodeError:
                print("Got JSONDecodeError while decoding the sample!")
                self.sd = None
            if not self.sd:
                print("Import_schema(): Failed to parse OTIO schema file.")
            else:                                   # we have a valid schema
                print("Parsed the schema JSON successfully.")
                if self.verbose:
                    print("Contents of the parsed JSON schema dict:\n")
                    print(self.sd)
                    print("\n")
        else:
            print("ERROR: no schema provided!")
            return -1

    # Ingest the text and store the JSON items in a dictionary
    def Parse(self):        
        protocol = None
        if self.sample_str != None:        
            print("Parsing JSON string from sample buffer...")
            #text = self.sample_str
            #print(text)
            #print('\n')    
            try:
                self.pd = json.loads(self.sample_str)
            except:
                print("Parse(): Error. Failed to parse JSON file! Either path incorrect or JSON invalid.")
                exit(-1)
            if not self.pd:
                print("Parse(): Failed to parse OTIO sample file.")
            else:                                   # we have a OTP message
                print("Parsed the sample JSON successfully.")
                if self.verbose:
                    print("Contents of the parsed JSON dict:\n")
                    print(self.pd)
                    print("\n")
        else:
            print("Parse(): Error. No json text provided!")
            return -1

    # Returns the multiplicative conversion factor from meters to user-specified units
    # Valid unit specifier strings: "m", "cm", "mm", "in"
    def Conversion_factor_from_meters(self,unit_str):
        if unit_str == "m":
            return 1.0
        elif unit_str == "cm":
            return 100.0
        elif unit_str == "mm":
            return 1000.0
        elif unit_str == "in":
            return (1000/25.4)

    def Get_camera_trans(self, dimension):
        for tr in self.pd["transforms"]:
            if ("Camera" in tr["name"]):
                if self.verbose:
                    print("found camera, dim = {}, mult factor: {}".format(dimension,self.trans_mult))
                if (dimension == 'x'):
                    return tr["translation"]["x"] * self.trans_mult
                elif (dimension == 'y'):
                    return tr["translation"]["y"] * self.trans_mult
                elif (dimension == 'z'):
                    return tr["translation"]["z"] * self.trans_mult
                break

    def Get_camera_rot(self, dimension):
        for tr in self.pd["transforms"]:
            if ("Camera" in tr["name"]):
                if (dimension == 'p'):
                    return tr["rotation"]["pan"] * self.rot_mult
                elif (dimension == 't'):
                    return tr["rotation"]["tilt"] * self.rot_mult
                elif (dimension == 'r'):
                    return tr["rotation"]["roll"] * self.rot_mult
                break

    # Return order: x,y,z
    def Get_camera_translations(self):
        return (self.Get_trans('X'), self.Get_trans('Y'), self.Get_trans('Z'))

    # Return house timecode
    def Get_timecode(self):
        if ("timing" in self.pd) and (self.pd["timing"]["timecode"]):
            hh = '{:02}'.format(int(self.pd["timing"]["timecode"]["hours"]))
            mm = '{:02}'.format(int(self.pd["timing"]["timecode"]["minutes"]))                
            ss = '{:02}'.format(int(self.pd["timing"]["timecode"]["seconds"]))
            ff = '{:02}'.format(int(self.pd["timing"]["timecode"]["frames"]))
            return hh + ':' + mm + ':' + ss + ':' + ff
        else:
            return None

    # Get the PTP sample time
    def Get_sample_time(self,part=None):
        if ("timing" in self.pd) and (self.pd["timing"]["sampleTimestamp"]):
            ssec = int(self.pd["timing"]["sampleTimestamp"]["seconds"])
            nsec = int(self.pd["timing"]["sampleTimestamp"]["nanoseconds"])
            asec = int(self.pd["timing"]["sampleTimestamp"]["attoseconds"])
            #ctime = ssec + (nsec * 0.000000001) + (asec * 0.000000000000000001)
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
                # FIXME: is this using the sample framerate?
                frm = int((nsec * 0.000000001) * self.Get_timecode_framerate())
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

    # Frame rate which this timecode represents
    def Get_timecode_framerate(self):
        if ("timing" in self.pd) and (self.pd["timing"]["timecode"]["format"]["frameRate"]):
            numerator = float(self.pd["timing"]["timecode"]["format"]["frameRate"]["num"])  
            denominator = float(self.pd["timing"]["timecode"]["format"]["frameRate"]["denom"]) 
            return float(numerator / denominator)
        else:
            return None

    # Set user-preferred units for translations. 
    # Valid args: "m", "cm", "mm", "in"
    def Set_trans_units(self,unit_str):
        schema_units = self.sd["properties"]["transforms"]["items"]["items"]["properties"]["translation"]["units"]
        if self.verbose:
            print("Schema says camera translation units are: {}".format(schema_units))
            print("Setting preferred translation units to: {0}".format(unit_str))
        if schema_units == "meter":
            self.trans_mult = self.Conversion_factor_from_meters(unit_str)
    
    # Set user-preferred units for rotations. 
    # Valid args: "deg", "rad" 
    def Set_rotation_units(self,unit_str):
        schema_units = self.sd["properties"]["transforms"]["items"]["items"]["properties"]["rotation"]["units"]
        if self.verbose:
            print("Schema says camera rotation units are: {}".format(schema_units))
            print("Setting preferred camera rotation units to: {0}".format(unit_str))
        if schema_units == "degree":
            if unit_str == "deg":
                self.rot_mult = 1.0
            if unit_str == "rad":
                self.rot_mult = math.pi/180

    # User preference for time format
    # Valid args: "sec", "timecode", "string"
    def Set_sample_time_format(self,format_str):
        if self.verbose:
            schema_units = self.sd["properties"]["timing"]["properties"]["sampleTimestamp"]["units"]
            print("Schema says sample time units are: {}".format(schema_units))
            print("Setting preferred sample time format to: {0}".format(format_str))
        if (format_str in self.sample_time_formats):
            self.sample_time_format = format_str

    # Establish a user-preference for units of focus distance by storing a conversion factor.
    # Valid: "m","cm","mm","in"
    def Set_focus_distance_units(self,unit_str):
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

    # The protocol to which this sample conforms
    def Get_protocol(self):
        if (self.pd["protocol"]):
            return str(self.pd["protocol"])
        else:
            return None

    def Get_slate(self):
        if "device" in self.pd.keys():
            if self.pd["device"]["slate"]:
                return str(self.pd["device"]["slate"])
            else:
                return None
        else:
            return None

    # If present in this sample, the 'static' block has the active sensor dimensions
    def Get_sensor_dim_height(self):
        if "static" in self.pd: 
            if self.pd["static"]["camera"]["activeSensorResolution"]:
                height = int(self.pd["static"]["camera"]["activeSensorResolution"]["height"])
                return height
        return None

    # If present in this sample, the 'static' block has the active sensor dimensions
    def Get_sensor_dim_width(self):
        if "static" in self.pd: 
            if self.pd["static"]["camera"]["activeSensorResolution"]:
                width = int(self.pd["static"]["camera"]["activeSensorResolution"]["width"])
                return width
            else:
                return None
        return None

    # Find units in the schema for active sensor dimensions
    def Get_sensor_dim_units(self):
        if "static" in self.pd: 
            if self.sd["properties"]["camera"]["properties"]["activeSensorPhysicalDimensions"]:
                return str(self.sd["properties"]["camera"]["properties"]["activeSensorPhysicalDimensions"]["units"])
            else:
                return None
        else:
            return None

    # If present in this sample, the 'static' block would have the active sensor dimensions
    def Get_tracking_device_serial_number(self):
        if "static" in self.pd: 
            if self.pd["static"]["device"]["serialNumber"]:  # FIXME: helper function to do every level, Joseph write it?
                return str(self.pd["static"]["device"]["serialNumber"])
            else:
                return None
        return None

    def Get_focal_length(self):
        if "lens" in self.pd.keys():
            return self.pd["lens"]["focalLength"]
        else:
            return None

    def Get_focus_distance(self):
        if "lens" in self.pd.keys():
            return float(self.pd["lens"]["focusDistance"]) * self.focus_dist_mult
        else:
            return None
