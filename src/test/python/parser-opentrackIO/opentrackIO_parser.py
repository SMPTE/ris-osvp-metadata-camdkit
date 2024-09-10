#!/usr/bin/env python3
#
# opentrackIO_parser.py
#
# Reference code for decoding opentrack messages
# Copyright (c) 2024 Steve Rosenbluth, RiS OSVP camera tracking committee
#
# License: this code is open-source under the FreeBSD License
#
# example: python3 src/test/python/parser-opentrackIO/opentrackIO_parser.py --file=complete_dynamic_example_20240907.json --schema=opentrackio_schema_modified_20240907.json
# exemple: python3 src/test/python/parser-opentrackIO/opentrackIO_parser.py --file=complete_static_example_20240907.json --schema=opentrackio_schema_modified_20240907.json

import json
import argparse
import os

# Class to decode and interpret the protocol
# Pass in either a JSON message or a test filename
class OTProtocol:
    def __init__(self, msg_str=None, filepath=None):
        # msg_str = string containing a single json "sample"
        # filepath: file containing a JSON "sample", for testing
        self.sample_str = msg_str
        self.filepath = filepath
        self.schemapath = None
        self.trans_mult = 1.0                               # user-preferred units multiplier
        self.curtime = 0
        self.cam_trans = {"X":0,"Y":0,"Z":0}
        self.pd = None          # the parsed procotol dictionary
        self.sd = None          # the parsed schema dictionary
        self.sample_time_format = "seconds"
        self.sample_time_formats = ["seconds","milliseconds","microseconds","nanoseconds"]
        self.verbose = False
        self.focus_dist_mult = 1.0

        parser = argparse.ArgumentParser(description='OpenTrackingProtocol parser')
        parser.add_argument('-f', '--file', help='The JSON input file.', default=None)
        parser.add_argument('-s', '--schema', help='The schema (JSON) input file.', default=None)
        parser.add_argument('-t', '--test', help='If present, will only verify json',action='store_true')
        parser.add_argument('-v', '--verbose', help='Make script more verbose',action='store_true')
        args = parser.parse_args()
        if (args.schema):
            if os.path.exists(args.schema):
                self.schemapath = args.schema
        if self.schemapath:
            self.Import_schema()
        if (args.file):
            if os.path.exists(args.file):
                self.filepath = args.file
        if (args.verbose):
            self.verbose = True

        self.Parse()                # parse the actual JSON of the protocol

    def Import_schema(self):
        text = ''
        try:
            if (self.schemapath != None):        
                with open(self.schemapath, 'r') as fd:
                    print("Reading OTIO schema file: {0}".format(self.schemapath))
                    lines = fd.readlines()
                    for line in lines:
                        text = text + line
            self.sd = json.loads(text)
        except json.decoder.JSONDecodeError:
            print("Got JSONDecodeError decoding the sample!")
            self.sd = None
        if not self.sd:
            print("Parse(): Failed to parse OTIO schema file.")
        else:                                   # we have a OTP message
            print("Parsed the schema JSON successfully.")
            if self.verbose:
                print("Contents of the parsed JSON schema dict:\n")
                print(self.sd)
                print("\n")
            #print("camera is: {}".format(self.sd["properties"]["camera"]))
            #print("finding: {}".format(self.sd["properties"]["lens"]["properties"]["focalLength"]["units"]))

    # ingest the text and store the JSON items in a dictionary
    def Parse(self):        
        protocol = None
        text = ''
        if (self.filepath != None):        
            with open(self.filepath, 'r') as fd:
                print("Reading OTIO sample file: {0}".format(self.filepath))
                lines = fd.readlines()
                for line in lines:
                    text = text + line
        elif self.sample_str != None:        
            print("Parsing JSON string from sample buffer...")
            text = self.sample_str
        #print(text)
        #print('\n')    
        try:
            self.pd = json.loads(text)
        except:
            print("Error: failed to parse JSON file! Either path incorrect or JSON invalid.")
            exit(-1)
        if not self.pd:
            print("Parse(): Failed to parse OTIO message file.")
        else:                                   # we have a OTP message
            print("Parsed the sample OTIO JSON successfully.")
            if self.verbose:
                print("Contents of the parsed JSON dict:\n")
                print(self.pd)
                print("\n")

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

    def Get_camera_trans(self, dimension,object_name=None):
        for tr in self.pd["transforms"]:
            if ("Camera" in tr["name"]):
                if (dimension == 'X'):
                    return tr["translation"]["x"] * self.trans_mult
                elif (dimension == 'Y'):
                    return tr["translation"]["y"] * self.trans_mult
                elif (dimension == 'Z'):
                    return tr["translation"]["z"] * self.trans_mult
                break

    def Get_camera_translations(self,object_name=None):
        return (self.Get_trans('X'), self.Get_trans('Y'), self.Get_trans('Z'))

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
    def Get_sample_time(self):
        if ("timing" in self.pd) and (self.pd["timing"]["sampleTimestamp"]):
            sec = float(self.pd["timing"]["sampleTimestamp"]["seconds"])
            nsec = float(self.pd["timing"]["sampleTimestamp"]["nanoseconds"])
            asec = float(self.pd["timing"]["sampleTimestamp"]["attoseconds"])
            ctime = sec + (nsec * 0.000000001) + (asec * 0.000000000000000001)
        if self.sample_time_format == "seconds":
            return ctime
        elif self.sample_time_format == "milliseconds":
            return ctime * 1000.0
        elif self.sample_time_format == "microseconds":
            return ctime * 10000.0
        elif self.sample_time_format == "nanoseconds":
            return ctime * 100000.0
        # can't convert to timecode becuase it is PTP and has no epoch?

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
            print("Schema says camera translation units are {}".format(schema_units))
        print("Setting preferred translation units to: {0}".format(unit_str))
        if schema_units == "meters":
            self.trans_mult = self.Conversion_factor_from_meters(unit_str)

    # User preference for time format
    # Valid args: "timecode"
    def Set_sample_time_format(self,format_str):
        print("Setting preferred sample time format to: {0}".format(format_str))
        if (format_str in self.sample_time_formats):
            self.sample_time_format = format_str

    # Esablish a user-preference for units of focus distance.
    # Valid: "m","cm","mm","in"
    def Set_focus_distance_units(self,unit_str):
        schema_units = self.sd["properties"]["lens"]["properties"]["focusDistance"]["units"]
        if self.verbose:
            print("Schema says focus distance units are {}".format(schema_units))
        print("Setting preferred focus distance units to: {}".format(unit_str))
        if unit_str == "m":
            if schema_units == "millimeter":
                self.focus_dist_mult = .001
        elif unit_str == "cm":
            if schema_units == "millimeter":
                self.focus_dist_mult = 0.1
        elif unit_str == "mm":
            if schema_units == "millimeter":        
                self.focus_dist_mult = 1.0
        elif unit_str == "in":
            if schema_units == "millimeter":        
                self.focus_dist_mult = 1/25.4

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
            if self.pd["static"]["device"]["serialNumber"]:
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
         return float(self.pd["lens"]["focusDistance"]) * self.focus_dist_mult


################
# Sample parsing below:

tsample = OTProtocol(None,None)
tsample.Set_trans_units("cm")              # end-user preferred units
tsample.Set_sample_time_format("sec")        # end-user preferred units.
tsample.Set_focus_distance_units("cm")     # end-user preferred units
print()

protocol= tsample.Get_protocol()
slate = tsample.Get_slate()
print("Detected protocol: {}".format(protocol))
print("On slate: {}".format(slate))
timecode = tsample.Get_timecode()
print("Current sample timecode: {}".format(timecode))
framerate = tsample.Get_timecode_framerate()
print("At a frame rate of: {:.5}".format(framerate))
sample_time =  tsample.Get_sample_time()
print("Sample PTP time is: {} sec".format(sample_time))
snum = tsample.Get_tracking_device_serial_number()
if snum:
    print("Tracking device serial number: {}".format(snum))
else:
    print("Unknown tracking device, wait for static sample to come in...")
posX = tsample.Get_camera_trans('X')
posY = tsample.Get_camera_trans('Y')
posZ =tsample.Get_camera_trans('Z')
print("Camera position is: ({1},{2},{3}) cm".format(timecode, posX, posY, posZ))
fl = tsample.Get_focal_length()
height = tsample.Get_sensor_dim_height()
if height:
    width = tsample.Get_sensor_dim_width()
    units = tsample.Get_sensor_dim_units()
    print("Active camera sensor height: {}, width: {} {}".format(height,width,units))
else:
    print("Unknown camera sensor, wait for static sample to come in...")
fl_units = tsample.sd["properties"]["lens"]["properties"]["focalLength"]["units"]
print("Focal length is: {} {}".format(fl,fl_units))
fd = tsample.Get_focus_distance()
print("Focus distance is: {} cm".format(fd))
