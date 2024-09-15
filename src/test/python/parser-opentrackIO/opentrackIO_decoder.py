#!/usr/bin/env python3
#
# opentrackIO_decoder.py
#
# Reference code for decoding opentrackIO messages
# Copyright (c) 2024 Steve Rosenbluth, RiS OSVP camera tracking committee
#
# License: this code is open-source under the FreeBSD License
#
# example: python3 src/test/python/parser-opentrackIO/opentrackIO_decoder.py --file=example_json/complete_dynamic_example_20240907.json --schema=example_json/opentrackio_schema_modified_20240907.json
# example: python3 src/test/python/parser-opentrackIO/opentrackIO_decoder.py --file=example_json/complete_static_example_20240907.json --schema=example_json/opentrackio_schema_modified_20240907.json

from opentrackIOlib import *

tsample = OTProtocol(None,None)
tsample.Set_trans_units("cm")              # end-user preferred units
tsample.Set_sample_time_format("seconds")        # end-user preferred units.
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
print("Sample PTP time is: {} sec".format(tsample.Get_sample_time()))
tsample.Set_sample_time_format("string")        # end-user preferred units.
print("Sample PTP as a string: {}".format(tsample.Get_sample_time()))
tsample.Set_sample_time_format("timecode")        # end-user preferred units.
print("Sample PTP as timecode: {}".format(tsample.Get_sample_time()))
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
