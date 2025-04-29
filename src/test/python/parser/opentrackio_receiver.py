#!/usr/bin/env python3
#
# opentrackio_receiver.py
#
# Reference code for receiving and decoding OpenTrackIO data
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import argparse
import os
import socket
import time
import urllib.error
import urllib.request
from typing import Any

import ntplib

from opentrackio_lib import *


class OpenTrackIOArgumentParser:
    """Handles parsing command line arguments for OpenTrackIO Receiver"""

    def __init__(self):
        self._parser = argparse.ArgumentParser(description=f'OpenTrackIO {OTRK_VERSION} protocol receiver.')
        self._setup_parser()

    def parse_args(self) -> dict[str, Any]:
        """
        Parse command line arguments and return a configuration dictionary.

        Returns:
            Dict[str, Any]: Configuration dictionary containing parsed arguments:
                - 'verbose': Boolean indicating verbose output.
                - 'schema_text': The schema JSON text content.
                - 'source_number': Source number to listen for.
                - 'port': Port number to listen on.
                - 'multicast_group': Formatted multicast address.
        """
        args = self._parser.parse_args()
        config: dict[str, Any] = dict()

        config['verbose'] = args.verbose

        schematext = ''
        if args.schema:
            if os.path.exists(args.schema):
                schemapath = args.schema
                try:
                    with open(schemapath, 'r') as file_io_handler:
                        print(f'Reading OpenTrackIO schema file: {schemapath}.')
                        schematext = file_io_handler.read()
                except Exception as e:
                    print(f'Error reading schema file: {e}.')
                    exit(-1)
            else:
                print(f'Schema file not found: {args.schema}. Attempting to download from opentrackio.org')
                try:
                    with urllib.request.urlopen('https://www.opentrackio.org/schema.json') as response:
                        schematext = response.read().decode('utf-8')
                        print(f'Successfully downloaded schema from opentrackio.org')

                        try:
                            with open(args.schema, 'w') as file_io_handler:
                                file_io_handler.write(schematext)
                                print(f'Saved downloaded schema to {args.schema}')
                        except Exception as e:
                            print(f'Note: Could not save downloaded schema to file: {e}')
                except urllib.error.HTTPError as e:
                    print(f'Error downloading schema: HTTP status {e.code}.')
                    print('No schema available, exiting.')
                    exit(1)
                except Exception as e:
                    print(f'Error downloading schema: {e}.')
                    print('No schema available, exiting.')
                    exit(1)
        else:
            print('No schema available, exiting.')
            exit(1)

        config['schema_text'] = schematext

        if args.source is not None:
            if not (1 <= args.source <= 200):
                print('Error: Source Number must be between 0 and 200.')
                exit(-1)
            else:
                config['source_number'] = args.source
        else:
            config['source_number'] = OTRK_SOURCE_NUMBER

        if args.port:
            if not (49152 <= args.port <= 65535):
                print('Error: port number must be between 49152 and 65535.')
                exit(-1)
            else:
                config['port'] = args.port
        else:
            config['port'] = OTRK_MULTICAST_PORT

        config['multicast_group'] = f'{OTRK_MULTICAST_PREFIX}{config["source_number"]}'

        return config

    def _setup_parser(self):
        """Configure argument parser with all required command line options."""
        self._parser.add_argument('-n', '--source', type=int,
                                  help='The Source Number (1-200) to listen for.',
                                  default=OTRK_SOURCE_NUMBER)

        self._parser.add_argument('-p', '--port', type=int,
                                  help=f'The port number (49152–65535) to listen on. Default: {OTRK_MULTICAST_PORT}',
                                  default=OTRK_MULTICAST_PORT)

        self._parser.add_argument('-s', '--schema',
                                  help='The schema (JSON) input file. Default: opentrackio_schema.json. '
                                       'If not found locally, will attempt to download from opentrackio.org/schema.json',
                                  default='opentrackio_schema.json')

        self._parser.add_argument('-v', '--verbose',
                                  help='Make script more verbose',
                                  action='store_true')


class OpenTrackIOPacketReceiver:
    """Class for receiving and processing OpenTrackIO packets"""

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the OpenTrackIO packet receiver.

        Args:
            config: Configuration dictionary containing:
                - 'verbose': Boolean for verbose output
                - 'multicast_group': Multicast group address
                - 'port': Port number to listen on
                - 'schema_text': Schema JSON text

        Raises:
            Exception: If OpenTrackIO protocol parser initialization fails
        """
        self._verbose: bool = config['verbose']
        self._multicast_group: str = config['multicast_group']
        self._multicast_port: int = config['port']

        # Initialize protocol parser
        try:
            self.protocol = OpenTrackIOProtocol(config['schema_text'])
        except Exception as e:
            print(f'Error initializing OpenTrackIO protocol parser: {e}.')
            raise

        self._sequence_number: int = 0
        self._prev_sequence_number: int = 0
        self._segment_buffer: bytearray = bytearray()
        self.encoding: Optional[PayloadFormat] = None
        self._timesource: Optional[TimeSource] = None
        self._ntpclient: ntplib.NTPClient = ntplib.NTPClient()
        self._ntpoffset: float = 0.0
        self._packets_received: int = 0
        self._last_receive_time: Optional[float] = None

    def start_receiving(self) -> None:
        """
        Start receiving packets from the multicast group.
        This method blocks indefinitely until interrupted (e.g., by keyboard interrupt).

        Raises:
            Exception: If socket setup fails
        """

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self._multicast_port))
            mreq = struct.pack('4sl', socket.inet_aton(self._multicast_group), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            print(f'Error setting up socket: {e}.')
            raise

        print(f'Listening for OpenTrackIO packets on {self._multicast_group}:{self._multicast_port}.')

        # Main receive loop
        try:
            while True:
                data, addr = sock.recvfrom(OTRK_MTU)
                self._packets_received += 1

                current_time = time.time()
                if self._last_receive_time is not None:
                    interval = current_time - self._last_receive_time
                    frequency = 1 / interval if interval > 0 else 0

                    if self._verbose:
                        print(f'\nReceive frequency: {frequency:.3f} Hz')
                        print(f'Received packets: {self._packets_received}')

                self._last_receive_time = current_time

                self._parse_packet(data)
        except KeyboardInterrupt:
            print('\nReceiver stopped by user.')
        finally:
            sock.close()

    def _init_time_source(self):
        """Initialize time synchronization based on time source."""

        if self._timesource == TimeSource.PTP:
            if self._verbose:
                print('Initializing PTP time source.')
            return
        elif self._timesource == TimeSource.NTP:
            if self._verbose:
                print(f'Initializing NTP time source using {NTPSERVER}.')
            try:
                ntpresponse = self._ntpclient.request(NTPSERVER)
                self._ntpoffset = ntpresponse.offset
                if self._verbose:
                    print(f'NTP offset: {self._ntpoffset} seconds.')
            except Exception as e:
                print(f'Warning: Failed to get NTP time from {NTPSERVER}: {e}.')
                print('Continuing with local system time.')
        elif self._timesource == TimeSource.GENLOCK:
            if self._verbose:
                print('Initializing genlock time source.')
            return
        elif self._timesource == TimeSource.VIDEO_IN:
            if self._verbose:
                print('Initializing videoIn time source.')
            return
        else:
            print('Unknown time source, using local system time.')
            return

    def _get_local_timestamp(self) -> float:
        """ Get local timestamp adjusted for time source offset.

        Returns:
            float: Current time in seconds (epoch time), adjusted for NTP offset if applicable.
        """
        if self._timesource == TimeSource.NTP:
            timestamp = time.time() + self._ntpoffset
            return timestamp
        else:

            return time.time()

    def _parse_packet(self, data: bytes) -> bool:
        """
        Parse an OpenTrackIO packet and validate its contents.

        Args:
            data: Raw packet data bytes.

        Returns:
            bool: True if packet was successfully parsed, False otherwise.
        """

        if len(data) < OTRK_HEADER_LENGTH:
            print('Invalid packet: Packet is too short.')
            return False

        identifier = data[:OTRK_IDENTIFIER_LENGTH]
        if identifier != OTRK_IDENTIFIER:
            print(f'Invalid packet: Identifier mismatch. Expected {OTRK_IDENTIFIER}, got {identifier}.')
            return False

        # reserved = data[4]  # Reserved for future use.
        self.encoding = PayloadFormat(data[5])
        self._sequence_number = struct.unpack('!H', data[6:8])[0]
        segment_offset = struct.unpack('!I', data[8:12])[0]
        l_and_payload_length = struct.unpack('!H', data[12:14])[0]

        last_segment = bool(l_and_payload_length >> 15)
        payload_length = l_and_payload_length & 0x7FFF

        if self._sequence_number == self._prev_sequence_number:
            if self._verbose:
                print(f'Duplicate packet: Sequence number {self._sequence_number} received again.')
            return False

        self._prev_sequence_number = self._sequence_number

        payload: bytes = data[16:16 + payload_length]
        if len(payload) != payload_length:
            print(f'Invalid packet: Expected payload length {payload_length}, but got {len(payload)}.')
            return False

        # Verify checksum
        received_checksum = data[14:16]
        header_without_checksum = data[:14]
        calculated_checksum = fletcher16(header_without_checksum + payload)
        if calculated_checksum != received_checksum:
            print(f'Invalid packet: Checksum mismatch.')
            return False

        if len(self._segment_buffer) != segment_offset:
            print(
                f'Invalid packet: Segment offset mismatch. Expected {len(self._segment_buffer)}, got {segment_offset}.')
            self._segment_buffer.clear()
            return False

        self._segment_buffer.extend(payload)

        if last_segment:
            self._process_payload()
            self._segment_buffer.clear()

        return True

    def _process_payload(self) -> bool:
        """ Process a complete reassembled payload.

        Decodes the payload according to its format (CBOR or JSON) and extracts
        OpenTrackIO protocol data.

        Returns:
            bool: True if payload was successfully processed, False otherwise.
        """

        try:
            if self.encoding == PayloadFormat.CBOR:
                self.protocol.parse_cbor(bytes(self._segment_buffer))
            elif self.encoding == PayloadFormat.JSON:
                self.protocol.parse_json(bytes(self._segment_buffer))
            else:
                print(f'Unsupported payload format: {self.encoding}.')
                self._segment_buffer = bytearray()
                return False

            if not self._timesource:
                try:
                    self._timesource = self.protocol.get_time_source()
                    self._init_time_source()
                except OpenTrackIOException as e:
                    print(f'Could not determine time source: {e}.')

            if self._verbose:
                self._display_packet_info()

            return True

        except Exception as e:
            print(f'Error processing payload: {e}.')
            return False

    def _display_packet_info(self):
        """Display packet information in verbose mode"""
        try:
            ref_timestamp = self._get_local_timestamp()
            sample_time = self.protocol.get_sample_time(TimeFormat.SECONDS)
            ref_delta = ref_timestamp - sample_time if sample_time else None

            print(f'\nPacket header:')
            print(f'  Sequence number: {self._sequence_number}')
            print(f'  Payload format: {self.encoding.name}')

            print(f'\nOpenTrackIO packet:')
            print(f'  Timecode: {self.protocol.get_timecode()}')
            print(f'  Time source: {self.protocol.get_time_source().value}')

            if ref_timestamp is not None:
                print(f'  Local time: {ref_timestamp:.6f}')

            print(f'  Sample time: {sample_time:.6f}')

            if ref_delta is not None:
                print(f'  Delta: {ref_delta:.6f} seconds')

            print(f'  Translation: {self.protocol.get_camera_translations()}')
            print(f'  Rotation: {self.protocol.get_camera_rotations()}')
            print(f'  Lens encoders: {self.protocol.get_lens_encoders()}')
        except Exception as e:
            print(f'Error displaying packet information: {e}.')


def main():
    parser = OpenTrackIOArgumentParser()
    config = parser.parse_args()

    try:
        receiver = OpenTrackIOPacketReceiver(config)
        receiver.start_receiving()  # Blocks until keyboard interrupt.
    except Exception as e:
        print(f'Error: {e}.')
        exit(1)


if __name__ == '__main__':
    main()
