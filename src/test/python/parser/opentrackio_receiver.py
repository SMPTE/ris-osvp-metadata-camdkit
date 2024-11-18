#!/usr/bin/env python3
#
# opentrackio_receiver.py
#
# Reference code for receiving and decoding OpenTrackIO data
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import socket
import struct
import argparse
import zlib
import sys
import time
import ntplib
from cbor2 import loads
from opentrackio_lib import *

MULTICAST_PORT = 55555
IDENTIFIER = b'OTrIO'  # ASCII "OTrIO"
IDENTIFIER_LENGTH = len(IDENTIFIER) 
HEADER_LENGTH = 19
VERBOSE = False
#CBOR_FORMAT = 0x02
#JSON_FORMAT = 0x01

sequence_number = 0
prev_sequence_number = 0

opentrackiolib = None

timesource = ''

NTPSERVER = "time.originalsyndicate.com"
ntpclient = ntplib.NTPClient()
ntpresponse = None 
ntpoffset = 0.0

def init_time_source():
	if timesource == TimeSource.PTP:
		return
	elif timesource == TimeSource.NTP:
		global ntpresponse, ntpoffset
		ntpresponse = ntpclient.request(NTPSERVER)
		ntpoffset = ntpresponse.offset
	elif timesource == TimeSource.GENLOCK:
		return
	else:
		return


def parse_opentrackio_packet(data):
	global sequence_number, prev_sequence_number, opentrackiolib, timesource
	
	if len(data) < HEADER_LENGTH:
		print("Invalid packet: Packet is too short.")
		return False

	identifier = data[:IDENTIFIER_LENGTH]
	if identifier != IDENTIFIER:
		print("Invalid packet: Identifier mismatch.")
		return False

	sequence_number = struct.unpack('!I', data[5:9])[0]
	total_segments = struct.unpack('!B', data[9:10])[0]
	segment_index = struct.unpack('!B', data[10:11])[0]
	format_type = struct.unpack('!B', data[11:12])[0]
	payload_length = struct.unpack('!H', data[12:14])[0]
	crc_value = struct.unpack('!I', data[14:18])[0]
	payload = data[18:]
	
	if sequence_number == prev_sequence_number:
		print(f"Invalid packet: Same sequence number received twice.")
		return False
	
	prev_sequence_number = sequence_number

	if len(payload) != payload_length:
		print(f"Invalid packet: Expected payload length {payload_length}, but got {len(payload)}.")
		return False

	header_without_crc = data[:14]
	calculated_crc = zlib.crc32(header_without_crc + payload) & 0xFFFFFFFF
	if calculated_crc != crc_value:
		print("Invalid packet: CRC checksum mismatch.")
		return False
		
	try:
		payloadformat = PayloadFormat(format_type)
	except:
		print("Invalid payload format.")
		return False
	
	if payloadformat == PayloadFormat.CBOR:
		try:
			opentrackiolib.parse_cbor(payload)
		except OpenTrackIOException as e:
			print(e)
			return False
	elif payloadformat == PayloadFormat.JSON:
		try:
			opentrackiolib.parse_json(payload)
		except OpenTrackIOException as e:
			print(e)
			return False				
	
	if not timesource:
		timesource = opentrackiolib.get_time_source()
		init_time_source()
	
	ref_timestamp = get_local_timestamp()
	ref_delta = ref_timestamp - opentrackiolib.get_sample_time(TimeFormat.SECONDS)
	
	if VERBOSE:
		print(f"OpenTrackIO header:\n")
		print(f"  Sequence Number: {sequence_number}")
		print(f"  Total Segments: {total_segments}")
		print(f"  Segment Index: {segment_index}")
		print(f"  Format Type: {payloadformat.name}")
		print(f"  Checksum: {crc_value}")
		print(f"  Payload Length: {payload_length}\n")
		
		#if format_type == CBOR_FORMAT:	
		#	print(f"    OpenTrackIO Payload: {json.dumps(payload, indent=4)}")
		#else:
		#	print(f"    OpenTrackIO Payload: {json.dumps(json.loads(payload), indent=4)}")
			
	try:
		if VERBOSE:
			print(f"OpenTrackIO packet:\n")
			print(f"  Timecode: {opentrackiolib.get_timecode()}")
			print(f"  Time source: {opentrackiolib.get_time_source().name}")
			print(f"  Local time: {ref_timestamp}")
			print(f"  Sample time: {opentrackiolib.get_sample_time(TimeFormat.SECONDS)}")
			print(f"  Delta: {ref_delta}")
			print(f"  Translation: {opentrackiolib.get_camera_translations()}")
			print(f"  Rotation: {opentrackiolib.get_camera_rotations()}")
	except OpenTrackIOException as e:
		print(e)

def get_local_timestamp():
	if timesource == TimeSource.NTP:
		timestamp = time.time() + ntpoffset
		#print(f"Local time: {timestamp}")
		return timestamp

def main():
	global VERBOSE, opentrackiolib
	
	parser = argparse.ArgumentParser(description='OpenTrackIO protocol receiver')
	parser.add_argument('-n', '--source', type=int, help='The Source Number (1-200) to listen for.', default=None)
	parser.add_argument('-p', '--port', type=int, help='The port number to listen on. Default: 55555.', default=None)
	parser.add_argument('-s', '--schema', help='The schema (JSON) input file. Default: opentrackio_schema.json', default='opentrackio_schema.json')
	parser.add_argument('-v', '--verbose', help='Make script more verbose', action='store_true')
	args = parser.parse_args()
	
	schematext = ''
	schemapath = None
	source_number = None
	multicast_port = MULTICAST_PORT

	if (args.schema):
		if os.path.exists(args.schema):
			schemapath = args.schema
			if (schemapath != None):        
				with open(schemapath, 'r') as fd:
					if VERBOSE:
						print("Reading OpenTrackIO schema file: {0}".format(schemapath))
					lines = fd.readlines()
					for line in lines:
						schematext = schematext + line		
	
	if (args.source):
		if not (1 <= args.source <= 200):
			print("Error: Source Number must be between 1 and 200.")
			exit(-1)
		else:
			source_number = args.source	
	
	if (args.port):
		if not (49152 <= args.port <= 65535):
			print("Error: port number must be between 49153 and 65535.")
			exit(-1)
		else:
			multicast_port = args.port	
			
	if (args.verbose):
		VERBOSE = True
	
	if not source_number or not schematext:
		print("Usage: python3 opentrackio_receiver.py --source=[1-200] --schema=opentrackio_schema.json --verbose")
		exit(-1)		
	
	opentrackiolib = OpenTrackIOProtocol(schematext, False)	

	multicast_group = f"235.135.1.{source_number}"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", MULTICAST_PORT))
	mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	
	print(f"Listening for OpenTrackIO packets on {multicast_group}:{MULTICAST_PORT}")

	last_time = None
	packets = 0
	
	while True:
		data, addr = sock.recvfrom(1024)
		packets = packets + 1
		
		current_time = time.time()
		if last_time is not None:
			interval = current_time - last_time
			frequency = 1 / interval if interval > 0 else 0
			if VERBOSE:
				print(f"\n")
				print(f"Receive frequency: {frequency:.3f} Hz")
				print(f"Received packets: {packets}")
			
		last_time = current_time
	
		parse_opentrackio_packet(data)

if __name__ == "__main__":
	main()

