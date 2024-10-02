#!/usr/bin/env python3
#
# opentrackIO_parser.py
#
# Reference code for parsing/decoding opentrackIO samples
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project
#
# Example run: python3 opentrackIO_parser.py --file=opentrackio_complete_static_example-20241001.json --schema=opentrackio_schema_20241001.json
# This is tested against the generated "complete_static_example" and "complete_dynamic_example" json

import os
import argparse
from opentrackIOlib import *

parser = argparse.ArgumentParser(description='OpenTrackingProtocol parser')
parser.add_argument('-f', '--file', help='The JSON input file.', default=None)
parser.add_argument('-s', '--schema', help='The schema (JSON) input file.', default=None)
parser.add_argument('-v', '--verbose', help='Make script more verbose',action='store_true')
args = parser.parse_args()

sample_text = ''
schematext = ''
verbose = False

if (args.schema):
    if os.path.exists(args.schema):
        schemapath = args.schema
        if (schemapath != None):        
            with open(schemapath, 'r') as fd:
                print("Reading OTIO schema file: {0}".format(schemapath))
                lines = fd.readlines()
                for line in lines:
                    schematext = schematext + line
if (args.file):
    if os.path.exists(args.file):
        filepath = args.file
        if (filepath != None):        
            with open(filepath, 'r') as fd:
                print("Reading OTIO sample file: {0}".format(filepath))
                lines = fd.readlines()
                for line in lines:
                    sample_text = sample_text + line
if (args.verbose):
    verbose = True

sample = OpenTrackIOProtocol(sample_text,schematext,verbose) # a "Sample" is a de-serialized JSON object containing the protocol
sample.Parse()                # parse the actual JSON of the protocol
sample.Import_schema()        # read the schema which governs the interpretation of the protocol

sample.Set_translation_units("cm")              # end-user preferred units
sample.Set_sample_time_format("sec")
sample.Set_focus_distance_units("cm")
sample.Set_rotation_units("deg")
print()

protocol= sample.Get_protocol()
slate = sample.Get_slate()
print("Detected protocol version: {}".format(protocol))
print("On slate: {}".format(slate))
timecode = sample.Get_timecode()
print("Current camera timecode: {}".format(timecode))
framerate = sample.Get_timecode_framerate()
print("At a camera frame rate of: {:.5}".format(framerate))
print()
print("Sample time PTP time is: {} sec".format(sample.Get_sample_time()))
sample.Set_sample_time_format("string")        # end-user preferred units.
print("Sample time PTP as a string: {}".format(sample.Get_sample_time()))
sample.Set_sample_time_format("timecode")        # end-user preferred units.
print("Sample time PTP as timecode: {}".format(sample.Get_sample_time()))
print("Sample time PTP elements: {} {} {} {} {} {}".format(sample.Get_sample_time('yy'),
    sample.Get_sample_time('dd'),
    sample.Get_sample_time('hh'),
    sample.Get_sample_time('mm'),
    sample.Get_sample_time('ss'),
    sample.Get_sample_time('ns')))
print()

snum = sample.Get_tracking_device_serial_number()
if snum:
    print("Tracking device serial number: {}".format(snum))
else:
    print("Unknown tracking device, wait for static sample to come in...")
posX = sample.Get_camera_translation('x')
posY = sample.Get_camera_translation('y')
posZ =sample.Get_camera_translation('z')
print("Camera position is: ({},{},{}) cm".format(posX, posY, posZ))
rotX = sample.Get_camera_rotation('p')
rotY = sample.Get_camera_rotation('t')
rotZ = sample.Get_camera_rotation('r')
print("Camera rotation is: ({},{},{}) deg".format(rotX, rotY, rotZ))
sample.Set_rotation_units("rad")
rotX = sample.Get_camera_rotation('p')
rotY = sample.Get_camera_rotation('t')
rotZ = sample.Get_camera_rotation('r')
print("Camera rotation is: ({:.5},{:.5},{:.5}) radians".format(rotX, rotY, rotZ))
print()

fl = sample.Get_focal_length()
height = sample.Get_sensor_dimension_height()
if height:
    width = sample.Get_sensor_dimension_width()
    units = sample.Get_sensor_dimension_units()
    print("Active camera sensor height: {}, width: {} {}".format(height,width,units))
else:
    print("Unknown camera sensor, wait for static sample to come in...")
fl_units = sample.sd["properties"]["lens"]["properties"]["focalLength"]["units"]
print("Focal length is: {} {}".format(fl,fl_units))
fd = sample.Get_focus_distance()
print("Focus distance is: {} cm".format(fd))
sample.Set_focus_distance_units("in")     # end-user preferred units
fd = sample.Get_focus_distance()
print("Focus distance is: {:.4} in".format(fd))


