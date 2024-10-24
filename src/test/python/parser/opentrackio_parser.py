#!/usr/bin/env python3
#
# opentrackio_parser.py
#
# Reference code for decoding OpenTrackIO samples
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project
#
# Example run: python3 opentrackio_parser.py --file=opentrackio_sample.json --schema=opentrackio_schema.json
# This is tested against the generated "complete_static_example" and "complete_dynamic_example" json

import os
import argparse
from opentrackio_lib import *

def main():
    parser = argparse.ArgumentParser(description='OpenTrackIO protocol parser')
    parser.add_argument('-f', '--file', help='The JSON input file.', default=None)
    parser.add_argument('-s', '--schema', help='The schema (JSON) input file.', default=None)
    parser.add_argument('-v', '--verbose', help='Make script more verbose',action='store_true')
    args = parser.parse_args()

    sample_text = ''
    schematext = ''
    verbose = False
    schemapath = None
    filepath = None

    if (args.schema):
        if os.path.exists(args.schema):
            schemapath = args.schema
            if (schemapath != None):        
                with open(schemapath, 'r') as fd:
                    print("Reading OpenTrackIO schema file: {0}".format(schemapath))
                    lines = fd.readlines()
                    for line in lines:
                        schematext = schematext + line
    if (args.file):
        if os.path.exists(args.file):
            filepath = args.file
            if (filepath != None):        
                with open(filepath, 'r') as fd:
                    print("Reading OpenTrackIO sample file: {0}".format(filepath))
                    lines = fd.readlines()
                    for line in lines:
                        sample_text = sample_text + line
    if (args.verbose):
        verbose = True

    if not filepath or not schemapath:
        print("Usage: python3 opentrackio_parser.py --file=opentrackio_sample.json --schema=opentrackio_schema.json")
        exit (-1)

    sample = OpenTrackIOProtocol(sample_text,schematext,verbose) # a "Sample" is a de-serialized JSON object containing the protocol
    sample.parse()                # parse the actual JSON of the protocol
    sample.import_schema()        # read the schema which governs the interpretation of the protocol

    sample.set_translation_units("cm")              # end-user preferred units
    sample.set_sample_time_format("sec")
    sample.set_focus_distance_units("cm")
    sample.set_rotation_units("deg")
    print()

    print("Detected protocol: {} version: {}".format(sample.get_protocol_name(), sample.get_protocol_version()))
    slate = sample.get_slate()
    print("On slate: {}".format(slate))
    timecode = sample.get_timecode()
    print("Current camera timecode: {}".format(timecode))
    framerate = sample.get_timecode_framerate()
    print("At a camera frame rate of: {:.5}".format(framerate))
    print()
    print("Sample time PTP time is: {} sec".format(sample.get_sample_time()))
    sample.set_sample_time_format("string")        # end-user preferred units.
    print("Sample time PTP as a string: {}".format(sample.get_sample_time()))
    sample.set_sample_time_format("timecode")        # end-user preferred units.
    print("Sample time PTP as timecode: {}".format(sample.get_sample_time()))
    print("Sample time PTP elements: {} {} {} {} {} {}".format(sample.get_sample_time('yy'),
        sample.get_sample_time('dd'),
        sample.get_sample_time('hh'),
        sample.get_sample_time('mm'),
        sample.get_sample_time('ss'),
        sample.get_sample_time('ns')))
    print()

    snum = sample.get_tracking_device_serial_number()
    if snum:
        print("Tracking device serial number: {}".format(snum))
    else:
        print("Unknown tracking device, wait for static sample to come in...")
    posX = sample.get_camera_translation('x')
    posY = sample.get_camera_translation('y')
    posZ =sample.get_camera_translation('z')
    print("Camera position is: ({},{},{}) cm".format(posX, posY, posZ))
    rotX = sample.get_camera_rotation('p')
    rotY = sample.get_camera_rotation('t')
    rotZ = sample.get_camera_rotation('r')
    print("Camera rotation is: ({},{},{}) deg".format(rotX, rotY, rotZ))
    sample.set_rotation_units("rad")
    rotX = sample.get_camera_rotation('p')
    rotY = sample.get_camera_rotation('t')
    rotZ = sample.get_camera_rotation('r')
    print("Camera rotation is: ({:.5},{:.5},{:.5}) radians".format(rotX, rotY, rotZ))
    print()

    fl = sample.get_focal_length()
    height = sample.get_sensor_dimension_height()
    if height:
        width = sample.get_sensor_dimension_width()
        units = sample.get_sensor_dimension_units()
        print("Active camera sensor height: {}, width: {} {}".format(height,width,units))
    else:
        print("Unknown camera sensor, wait for static sample to come in...")
    fl_units = sample.sd["properties"]["lens"]["properties"]["focalLength"]["units"]
    print("Focal length is: {} {}".format(fl,fl_units))
    fd = sample.get_focus_distance()
    print("Focus distance is: {} cm".format(fd))
    sample.set_focus_distance_units("in")     # end-user preferred units
    fd = sample.get_focus_distance()
    print("Focus distance is: {:.4} in".format(fd))

if __name__ == "__main__":
    main()
