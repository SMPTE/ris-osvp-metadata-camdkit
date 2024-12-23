#!/usr/bin/env python3
#
# opentrackio_sender.py
#
# Reference code for encoding and sending OpenTrackIO data
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

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

opentrackiolib = None

ntpclient = ntplib.NTPClient()

# Static configuration
UINT32_MAX = 4294967295
BASE_FREQUENCY = 24000
FREQUENCY_DENOM = 1001
FREQUENCY = BASE_FREQUENCY / FREQUENCY_DENOM 
INTERVAL = 1 / FREQUENCY
MY_UUID = "" # UUID to be set in the main() function

payloadformat = None

timesource = ''

NTPSERVER = "pool.ntp.org"
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
	else:
		return time.time()

def create_opentrackio_packet(use_cbor=False, sequence_number=1, segment_index=0, total_segments=1, source_number=OTRK_SOURCE_NUMBER):
	current_time = datetime.now()
	increment_frame(current_time)
	ref_timestamp = get_local_timestamp()
	
	seconds = int(math.floor(ref_timestamp))
	fraction = ref_timestamp - seconds
	nanoseconds = int(fraction * 1_000_000_000)
	
	payload_data = {
		"protocol": {
			"name": "OpenTrackIO",
			"version": OTRK_VERSION
		},
		"sourceId": f"urn:uuid:{MY_UUID}",
		"sourceNumber": source_number,
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
		  "nanoseconds": nanoseconds
		}
	
	if payloadformat == PayloadFormat.CBOR:
		payload = dumps(payload_data)
	else:	
		payload = json.dumps(payload_data).encode('utf-8')
	
	udp_segments = construct_udp_segments(sequence_number, payload, payloadformat.value)
	
	return udp_segments

def construct_udp_header(sequence_number: int, segment_offset: int, payload: bytes, encoding: int = 0, last_segment: bool = False) -> bytes:
	"""
	Construct a UDP header with the new format.

	Args:
		sequence_number (int): Sequence number of the packet (0-65535).
		segment_offset (int): Offset of this segment in the full data stream (0-2^32-1).
		payload (bytes): The payload to be sent.
		encoding (int): Encoding type (0-255).
		last_segment (bool): Whether this is the last segment.

	Returns:
		bytes: The constructed UDP header and payload.
	"""
	reserved = 0          # Reserved field (1 byte)
	encoding_byte = struct.pack('!B', encoding)  # Encoding (1 byte)
	sequence_number_bytes = struct.pack('!H', sequence_number)  # Sequence number (2 bytes)
	segment_offset_bytes = struct.pack('!I', segment_offset)  # Segment offset (4 bytes)

	payload_length = len(payload)
	
	l_and_payload_length = (int(last_segment) << 15) | payload_length
	l_and_payload_length_bytes = struct.pack('!H', l_and_payload_length)
	
	header = (
		OTRK_IDENTIFIER +
		struct.pack('!B', reserved) +
		encoding_byte +
		sequence_number_bytes +
		segment_offset_bytes +
		l_and_payload_length_bytes
	)

	checksum = fletcher16(header + payload)
	
	return header + checksum
	
def construct_udp_segments(sequence_number: int, payload: bytes, encoding: int = 0) -> list:
		"""
		Construct UDP packets with segmentation if payload exceeds 1500 bytes.
	
		Args:
			sequence_number (int): Sequence number of the first packet.
			payload (bytes): The payload to be sent.
			encoding (int): Encoding type (0-255).
	
		Returns:
			list: A list of UDP packets (bytes), each with its own header and payload.
		"""
	
		segments = []  # List to store individual segments
		total_length = len(payload)
	
		for offset in range(0, total_length, OTRK_MAX_PAYLOAD_SIZE):
			segment_payload = payload[offset : offset + OTRK_MAX_PAYLOAD_SIZE]
			last_segment = (offset + OTRK_MAX_PAYLOAD_SIZE >= total_length)  # Is this the last segment?
			
			header = construct_udp_header(
				sequence_number=sequence_number,
				segment_offset=offset,
				payload=segment_payload,
				encoding=encoding,
				last_segment=last_segment
			)
	
			# Append the complete packet (header + payload)
			segments.append(header + segment_payload)
			
			# Increment sequence number for the next segment
			sequence_number += 1
	
		return segments
	
def send_multicast_packets(multicast_group, multicast_port, source_number):
	global sequence_number
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	
	sequence_number = 1  # Initial sequence number

	print(f"Sending packets to {multicast_group}:{multicast_port} at {FREQUENCY} packets per second")

	while True:
		segments = create_opentrackio_packet(use_cbor = (payloadformat == PayloadFormat.CBOR), sequence_number=sequence_number, source_number=source_number)
	
		for i, segment in enumerate(segments):
			sock.sendto(segment, (multicast_group, multicast_port))
		
		increment_sequence_number()
		move_camera()
		time.sleep(INTERVAL)

def main():
	
	global timesource, payloadformat
	
	source_number = OTRK_SOURCE_NUMBER
	multicast_port = OTRK_MULTICAST_PORT
	multicast_group = f"{OTRK_MULTICAST_PREFIX}{OTRK_SOURCE_NUMBER}"
	
	parser = argparse.ArgumentParser(description=f'OpenTrackIO {OTRK_VERSION} protocol sender')
	parser.add_argument('-s', '--source', type=int, help='The Source Number (1-200) to send to.', default=1)
	parser.add_argument('-p', '--port', type=int, help=f'The port number (49152–65535) to send to. Default: {OTRK_MULTICAST_PORT}', default=OTRK_MULTICAST_PORT)
	parser.add_argument('-f', '--format', help='The format [JSON, CBOR] to use.', default='CBOR')
	parser.add_argument('-r', '--ref', help='The time source [genlock, PTP, NTP] to use.', default='NTP')
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
			source_number = args.source
			multicast_group = f"{OTRK_MULTICAST_PREFIX}{source_number}"
	else:
		print("Error: Source Number must be between 1 and 200.")
		exit(-1)
	
	if (args.port):
		if not (49152 <= args.port <= 65535):
			print("Error: port number must be between 49152 and 65535.")
			exit(-1)
		else:
			multicast_port = args.port	
	
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
	send_multicast_packets(multicast_group, multicast_port, source_number)
	

if __name__ == "__main__":
	main()
	
