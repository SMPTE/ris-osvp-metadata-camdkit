import socket
import struct
import time
import zlib
import json
import uuid
import math
import ntplib
import argparse
from datetime import datetime
from cbor2 import dumps
from opentrackio_lib import *

ntpclient = ntplib.NTPClient()

# Static configuration
UINT32_MAX = 4294967295
SOURCE_NUMBER = 150
MULTICAST_GROUP =  f"235.135.1.{SOURCE_NUMBER}"
MULTICAST_PORT = 55555
MULTICAST_TTL = 2 
BASE_FREQUENCY = 24000
FREQUENCY_DENOM = 1001
FREQUENCY = BASE_FREQUENCY / FREQUENCY_DENOM 
INTERVAL = 1 / FREQUENCY
MY_UUID = "" # UUID to be set in the main() function

payloadformat = None

timesource = ''

NTPSERVER = "time.originalsyndicate.com"
ntpclient = ntplib.NTPClient()

ref_offset_s = 0.0

camera_z_start = 1.0
camera_z_current = camera_z_start
camera_z_max = 4
camera_tilt_start = 0.0
camera_tilt_current = camera_tilt_start
camera_tilt_max = -10

duration = 5.0
half_duration = duration / 2
start_time = time.time()

last_second = None
current_frame = 0

sequence_number = 1  # Initial sequence number

def init_time_source():
	if timesource == TimeSource.PTP:
		return
	elif timesource == TimeSource.NTP:
		global ref_offset_s
		ntpresponse = ntpclient.request(NTPSERVER)
		ref_offset_s = ntpresponse.offset
	elif timesource == TimeSource.GENLOCK:
		return
	else:
		return


def increment_frame(current_time):
	global last_second, current_frame

	millis = current_time.microsecond / 1000
	seconds = current_time.second
	minutes = current_time.minute

	if last_second != seconds:
		if last_second == None:
			current_frame = math.ceil(millis/(1/FREQUENCY*1000))
		else:
			current_frame = 0
		
		last_second = seconds

		# Drop frames at the start of each minute, except every tenth minute
		drop_frame = not FREQUENCY.is_integer()
		if drop_frame and seconds == 0 and minutes % 10 != 0:
			# Skip frames 00 and 01 in the new second
			current_frame = 2

	else:
		current_frame += 1

	return current_frame

def increment_sequence_number():
	global sequence_number
	
	if sequence_number + 1 == UINT32_MAX:
		sequence_number = 1
	else:
		sequence_number += 1

def move_camera():
	global camera_tilt_current, camera_z_current, start_time
	elapsed_time = (time.time() - start_time) % duration
	progress = (elapsed_time / half_duration) if elapsed_time <= half_duration else (1 - ((elapsed_time - half_duration) / half_duration))
	camera_z_current = camera_z_start + (camera_z_max - camera_z_start) * progress
	camera_tilt_current = camera_tilt_start + (camera_tilt_max - camera_tilt_start) * progress	

def generate_stable_uuid():
	mac_address = uuid.getnode()
	stable_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(mac_address))
	return stable_uuid
	
def get_local_timestamp():
	if timesource == TimeSource.NTP:
		timestamp = time.time() + ref_offset_s
		#print(f"Local time: {timestamp}")
		return timestamp

def create_opentrackio_packet(use_cbor=False, sequence_number=1, segment_index=0, total_segments=1):
	current_time = datetime.now()
	increment_frame(current_time)
	ref_timestamp = get_local_timestamp()
	
	seconds = int(math.floor(ref_timestamp))
	fraction = ref_timestamp - seconds
	nanoseconds = int(fraction * 1_000_000_000)
	
	payload_data = {
		"protocol": {
			"name": "OpenTrackIO",
			"version": "0.9.0"
		},
		"sourceId": f"urn:uuid:{MY_UUID}",
		"sourceNumber": SOURCE_NUMBER,
		"timing": {
			"frameRate": {
			  "num": BASE_FREQUENCY,
			  "denom": FREQUENCY_DENOM
			},
			"mode": "internal",
			"sequenceNumber": sequence_number,
			"synchronization": {
		  		"frequency": {
					"num": BASE_FREQUENCY,
					"denom": FREQUENCY_DENOM
		  		},
		  		"locked": True,
		  		"source": timesource.value
			},
			"sampleTimestamp": {
			  "seconds": seconds,
			  "nanoseconds": nanoseconds
			},
	  		"timecode": {
				"hours": current_time.hour,
				"minutes": current_time.minute,
				"seconds": current_time.second,
				"frames": current_frame,
				"format": {
		  			"frameRate": {
						"num": BASE_FREQUENCY,
						"denom": FREQUENCY_DENOM
					},
						"dropFrame": True
				}
			}
		},
		"transforms": [
			{
				"translation": {"x": 0.0, "y": 0.0, "z": camera_z_current},
				"rotation": {"pan": 0.0, "tilt": camera_tilt_current, "roll": 0.0},
				"transformId": "Camera"
			}
		],
		"lens": {
			"rawEncoders": {
			  "focus": 0,
			  "iris": 0,
			  "zoom": 0
			}
		} 
	}
	
	if timesource == TimeSource.NTP:
		payload_data["timing"]["synchronization"]["ntp"] = {
			"server": NTPSERVER,
			"offset": ref_offset_s
		}
		
		payload_data["timing"]["sampleTimestamp"] = {
		  "seconds": seconds,
		  "nanoseconds": nanoseconds,
		  "attoseconds" : 0
		}
	
	if payloadformat == PayloadFormat.CBOR:
		payload = dumps(payload_data)
	else:	
		payload = json.dumps(payload_data).encode('utf-8')
	
	identifier = b'OTrIO'
	sequence_number_bytes = struct.pack('!I', sequence_number)
	total_segments_byte = struct.pack('!B', total_segments)
	segment_index_byte = struct.pack('!B', segment_index)
	#format_type = CBOR_FORMAT if use_cbor else JSON_FORMAT
	#format_type = struct.pack('!B', PayloadFormat.CBOR.value) if use_cbor else struct.pack('!B', PayloadFormat.JSON.value)
	format_type = struct.pack('!B', payloadformat.value)
	payload_length = struct.pack('!H', len(payload))

	header = (
		identifier +
		sequence_number_bytes +
		total_segments_byte +
		segment_index_byte +
		format_type +
		payload_length
	)

	crc_value = zlib.crc32(header + payload) & 0xFFFFFFFF
	crc_bytes = struct.pack('!I', crc_value)

	return header + crc_bytes + payload

def send_multicast_packets():
	global sequence_number
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
	
	sequence_number = 1  # Initial sequence number

	print(f"Sending packets to {MULTICAST_GROUP}:{MULTICAST_PORT} at {FREQUENCY} packets per second")

	while True:
		packet = create_opentrackio_packet(use_cbor = (payloadformat == PayloadFormat.CBOR), sequence_number=sequence_number)
		sock.sendto(packet, (MULTICAST_GROUP, MULTICAST_PORT))
		increment_sequence_number()
		move_camera()
		time.sleep(INTERVAL)

def main():
	
	global SOURCE_NUMBER, MULTICAST_GROUP, timesource, payloadformat
	
	parser = argparse.ArgumentParser(description='OpenTrackIO protocol sender')
	parser.add_argument('-n', '--source', type=int, help='The Source Number (1-200) to send to.', default=None)
	parser.add_argument('-f', '--format', help='The format [JSON, CBOR] to use.', default=None)
	parser.add_argument('-r', '--ref', help='The time source [genlock, PTP, NTP] to use.', default=None)
	args = parser.parse_args()
	
	if (args.ref):
		try:
			timesource = TimeSource(args.ref.lower())
			init_time_source()
		except:
			print("Error: Time source must be genlock, PTP, or NTP.")
			exit(-1)
	else:
		timesource = TimeSource.NONE
	
	if (args.source):
		if not (1 <= args.source <= 200):
			print("Error: Source Number must be between 1 and 200.")
			exit(-1)
		else:
			SOURCE_NUMBER = args.source
			MULTICAST_GROUP =  f"235.135.1.{SOURCE_NUMBER}"
	else:
		print("Error: Source Number must be between 1 and 200.")
		exit(-1)
	
	if (args.format):
		if args.format.upper() == 'CBOR':
			payloadformat = PayloadFormat.CBOR
		elif args.format.upper() == 'JSON':
			payloadformat = PayloadFormat.JSON
		else:
			print("Error: Format must be JSON or CBOR.")
			exit(-1)
	else:
		print("Error: Format must be JSON or CBOR.")
		exit(-1)
	
	MY_UUID = generate_stable_uuid()
	send_multicast_packets()
	

if __name__ == "__main__":
	main()
	
