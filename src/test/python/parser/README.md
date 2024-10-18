#Documentation for opentrackIO_parser.py

This python reference code is for parsing "sample" JSON in OpenTrackIO format. User API is in the methods of the class "OpenTrackIOProtocol" and includes methods for getting and scaling values to user-preferred units.

This code works with Python 3.11 and above

Example:
```
export PYTHONPATH=src/main/python
python3 src/tools/python/generate_opentrackio_schema.py > opentrackio_schema.json
python3 src/tools/python/generate_complete_static_example.py > opentrackio_complete_static_sample.json

python3 opentrackio_parser.py --file=opentrackio_complete_static_sample.json --schema=opentrackio_schema.json 

Reading OTIO schema file: opentrackio_schema.json
Reading OTIO sample file: opentrackio_complete_static_sample.json
Parsing JSON string from sample buffer...
Parsed the sample JSON successfully.
Parsed the schema JSON successfully.

Detected protocol: OpenTrackIO
Protocol version: 1.0.0
On slate: A101_A_4
Current camera timecode: 01:02:03:04
At a camera frame rate of: 23.976

Sample time PTP time is: 1718806554.5 sec
Sample time PTP as a string: year:2024 day:183 hour:14 min:15 sec:54 nsec:500000000
Sample time PTP as timecode: 14:15:54:11
Sample time PTP elements: 2024 183 14 15 54 500000000

Tracking device serial number: 1234567890A
Camera position is: (100.0,200.0,300.0) cm
Camera rotation is: (180.0,90.0,45.0) deg
Camera rotation is: (3.1416,1.5708,0.7854) radians

Active camera sensor height: 2160, width: 3840 micron
Focal length is: 24.305 millimeter
Focus distance is: 100.0 cm
Focus distance is: 39.37 in
```

Note that JSON dictionary contents and other debug info can be examined with the verbose flag: -v
