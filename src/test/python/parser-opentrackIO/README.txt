opentrackIO_parser.py

This is python reference code for parsing an OpentrackIO packet.
User API is in the methods of the class: OTProtocol
This code works with Python 3.11


Example output:

 python3 opentrackIO_parser.py --schema=example_json/dynamic_schema.pretty.json --file=example_json/open_tracking_example-1.json 
Reading OTP schema file: example_json/dynamic_schema.pretty.json
Parsed the schema JSON successfully.

Reading OTP protocol file: example_json/open_tracking_example-1.json
Parsed the sample JSON successfully.
Setting preferred translation units to: cm.
Setting preferred time format to: timecode.
Detected protocol: OpenTrackIO_0.1.0.
On slate A101_A_4
At 01:09:55:12 the camera position is (124.50000000000001,223.0,412.0)


JSON dictionary contents can be examined with the verbose flag:

 python3 opentrackIO_parser.py -v --file=example_json/open_tracking_example-1.json 
Reading OTP protocol file: example_json/open_tracking_example-1.json
Parsed the sample JSON successfully.
Contents of the parsed JSON dict:

{'packetId': 'urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a65', 'protocol': 'OpenTrackIO_0.1.0', 'sampleType': 'dynamic', 'metadata': {'status': 'tracking', 'recording': False, 'slate': 'A101_A_4', 'notes': 'Free string', 'relatedPackets': ['urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66', 'urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a67']}, 'timing': {'mode': 'internal', 'timestamp': 1203120982.1423, 'sequenceNumber': 12345, 'frameRate': 29.976, 'timecode': {'format': '23.98', 'hours': 1, 'minutes': 9, 'seconds': 55, 'frames': 12}, 'synchronization': {'enabled': True, 'frequency': 23.976, 'locked': True, 'source': 'genlock', 'ptpMaster': '00:12:23:34:45:56', 'ptpOffset': 0.0, 'ptpDomain': 0, 'offsets': {'translation': 0.0, 'rotation': 0.0, 'encoders': 0.0}}}, 'transforms': [{'name': 'Dolly', 'translation': {'x': 1.245}}, {'name': 'Crane Arm', 'parent': 'Dolly', 'translation': {'x': 1.245, 'y': 2.23, 'z': 4.12}, 'rotation': {'pan': 223.1, 'tilt': 124.3, 'roll': 0.0}}, {'name': 'Camera', 'parent': 'Crane Arm', 'translation': {'x': 1.245, 'y': 2.23, 'z': 4.12}, 'rotation': {'pan': 223.3, 'tilt': 124.2, 'roll': 0.0}, 'perspectiveShift': {'Cx': 0.1, 'Cy': 0.2}}], 'lens': {'focalLength': 24.003, 'fovScale': 1, 'sensorWidth': 23.76, 'aspectRatio': [4, 3], 'inverseFocalDistance': 0.1, 'aperture': 4.0, 'fStop': False, 'entrancePupilDistance': 0.123, 'exposureFalloff': {'a1': 10.012, 'a2': 1.012, 'a3': 2.012}, 'encoders': {'focus': 0.234, 'iris': 0.123, 'zoom': 0.456}, 'distortion': {'radial': [0.1, -0.05, 0.001, 0.0001], 'tangential': [0.01, -0.02]}, 'centerShift': {'cx': 0.1, 'cy': 0.2}, 'custom': [0.2, 0.3]}, 'virtualCamera': {'pot1': 2435, 'button1': False}}

Setting preferred translation units to: cm.
Setting preferred time format to: timecode.
Detected protocol: OpenTrackIO_0.1.0.
On slate A101_A_4
At 01:09:55:12 the camera position is (124.50000000000001,223.0,412.0)

