#!/usr/bin/env python3
#
# opentrack_parser.py
# Reference code for decoding opentrack messages
# Steve Rosenbluth, RiS OSVP committee
# test run: python3 opentrack_parser.py --schema=dynamic_schema.pretty.json --file=open_tracking_example-1.json
# test run: python3 opentrack_parser.py --file=mosys_dynamic-output-example-2.json

import json
import argparse
import os

# Class to decode and interpret the protocol
# Pass in either a JSON message or a test filename
class OTProtocol:
    def __init__(self, msg_str=None, filepath=None):
        # msg_str = string containing a single json message
        # filepath: file containing a message, for testing
        self.filepath = filepath
        self.schemapath = None
        self.trans_scale = 1.0
        self.time_units = "timecode"
        self.curtime = 0
        self.cam_trans = {"X":0,"Y":0,"Z":0}
        self.pd = None          # the parsed procotol dictionary
        self.sd = None          # the parsed schema dictionary
        self.valid_formats = ["timecode","seconds","milliseconds"]
        self.verbose = False

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
        if (self.schemapath != None):        
            with open(self.schemapath, 'r') as fd:
                print("Reading OTP schema file: {0}".format(self.schemapath))
                lines = fd.readlines()
                for line in lines:
                    text = text + line
        self.sd = json.loads(text)
        # FIXME: except: json.decoder.JSONDecodeError
        if not self.sd:
            print("Parse(): Failed to parse OTP schema file.")
        else:                                   # we have a OTP message
            print("Parsed the schema JSON successfully.")
            if self.verbose:
                print("Contents of the parsed JSON schema dict:\n")
                print(self.sd)
            print("\n")
        

    def Parse(self):        # walk through the text and create task objects based on items listed 
        protocol = None
        text = ''
        if (self.filepath != None):        
            with open(self.filepath, 'r') as fd:
                print("Reading OTP protocol file: {0}".format(self.filepath))
                lines = fd.readlines()
                for line in lines:
                    text = text + line
        elif msg_str != None:
            print("Parsing JSON string from buffer...")
            text = msg_str
        #print(text)
        #print('\n')    
        self.pd = json.loads(text)
        if not self.pd:
            print("Parse(): Failed to parse OTP message file.")
        else:                                   # we have a OTP message
            print("Parsed the sample JSON successfully.")
            if self.verbose:
                print("Contents of the parsed JSON dict:\n")
                print(self.pd)
                print("\n")

    def Get_trans(self, dimension,object_name=None):
        for tr in self.pd["transforms"]:
            #if (tr["name"]) == "Camera":
            if ("Camera" in tr["name"]):
                #print(tr)
                if (dimension == 'X'):
                    return tr["translation"]["x"] * self.trans_scale
                elif (dimension == 'Y'):
                    return tr["translation"]["y"] * self.trans_scale
                elif (dimension == 'Z'):
                    return tr["translation"]["z"] * self.trans_scale
                break

    def Get_cam_translations(self,object_name=None):
        return (self.Get_trans('X'), self.Get_trans('Y'), self.Get_trans('Z'))

    def Get_time(self):
        if self.time_units == "timecode":
            if ("timing" in self.pd) and (self.pd["timing"]["timecode"]):
                hh = '{:02}'.format(int(self.pd["timing"]["timecode"]["hours"]))
                mm = '{:02}'.format(int(self.pd["timing"]["timecode"]["minutes"]))                
                ss = '{:02}'.format(int(self.pd["timing"]["timecode"]["seconds"]))
                ff = '{:02}'.format(int(self.pd["timing"]["timecode"]["frames"]))
                #return str(self.pd["timing"]["timecode"]["hours"])+':'+str(self.pd["timing"]["timecode"]["minutes"])+':'+str(self.pd["timing"]["timecode"]["seconds"])+':'+str(self.pd["timing"]["timecode"]["frames"])
                return hh + ':' + mm + ':' + ss + ':' + ff
            else:
                return None
        elif self.time_units == "seconds":
            return self.curtime
        elif self.time_units == "milliseconds":
            return self.curtime * 1000.0

    def Set_trans_units(self,unit_str):
        #TODO: read the schema first, to get native protocol units
        print("Setting preferred translation units to: {0}.".format(unit_str))
        if unit_str == "cm":
            self.trans_scale = 100.0          # convert schemas meters to cm

    def Set_time_units(self,units_str):
        print("Setting preferred time format to: {0}.".format(units_str))
        if (units_str in self.valid_formats):
            self.time_units = units_str

    def Get_protocol(self):
        if (self.pd["protocol"]):               # getattr ?
            return str(self.pd["protocol"])
        else:
            return None

    def Get_slate(self):
        if "metadata" in self.pd.keys():
            if self.pd["metadata"]["slate"]:            # getattr ?
                return str(self.pd["metadata"]["slate"])
            else:
                return None
        else:
            return None

    def Get_packet_type(self):
        if "sampleType" in self.pd.keys():
            if (self.pd["sampleType"] == "dynamic") or (self.pd["sampleType"] == "static"):
                return str(self.pd["sampleType"])
            else:
                return None


################
#Sample app below:

tmsg = OTProtocol(None,"open_tracking_sample.json")
tmsg.Set_trans_units("cm")              # end-user preferred units
tmsg.Set_time_units("timecode")          # float seconds

if (tmsg.Get_packet_type() == "dynamic"):
    msgtype = tmsg.Get_packet_type()
    protocol= tmsg.Get_protocol()
    slate = tmsg.Get_slate()
    print("Detected protocol: {0}.\nOn slate {1}".format(protocol,slate))
    timecode = tmsg.Get_time()
    posX = tmsg.Get_trans('X')
    posY = tmsg.Get_trans('Y')
    posZ =tmsg.Get_trans('Z')
    print("At {0} the camera position is ({1},{2},{3})".format(timecode, posX, posY, posZ))
else:
    print("Expected dynamic packet type, quitting...")
