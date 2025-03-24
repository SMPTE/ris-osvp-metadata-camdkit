#!/usr/bin/env python3
#
# opentrackio_sender.py
#
# Reference code for encoding and sending OpenTrackIO data
#
# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the SMTPE RIS OSVP Metadata Project

import argparse
import socket
import time
import uuid

import ntplib

from opentrackio_lib import *

UINT16_MAX = 65535  # 16-bit max value


class OpenTrackIOArgumentParser:
    """Handles parsing command line arguments for OpenTrackIO"""

    def __init__(self):
        self._parser = argparse.ArgumentParser(description=f'OpenTrackIO {OTRK_VERSION} protocol sender.')
        self._setup_parser()

    def parse_args(self):
        args = self._parser.parse_args()
        config = {}

        try:
            time_source_str = args.ref.lower()
            if time_source_str == "ntp":
                config['time_source'] = TimeSource.NTP
            elif time_source_str == "ptp":
                config['time_source'] = TimeSource.PTP
            elif time_source_str == "genlock":
                config['time_source'] = TimeSource.GENLOCK
            elif time_source_str == "videoin":
                config['time_source'] = TimeSource.VIDEO_IN
            else:
                raise ValueError("Invalid time source.")
        except ValueError:
            print("Error: Time source must be genlock, videoIn, ptp, or ntp.")
            exit(-1)

        config['source_number'] = args.source

        if not (49152 <= args.port <= 65535):
            print("Error: port number must be between 49152 and 65535.")
            exit(-1)
        config['port'] = args.port

        if args.format.upper() == 'CBOR':
            config['format'] = PayloadFormat.CBOR
        elif args.format.upper() == 'JSON':
            config['format'] = PayloadFormat.JSON
        else:
            print("Error: Format must be JSON or CBOR.")
            exit(-1)

        config['multicast_group'] = args.ip
        config['debug'] = args.verbose
        config['num-segments'] = args.num_segments

        return config

    def _setup_parser(self):
        self._parser.add_argument('-s', '--source', type=int,
                                  help='The Source Number to send to.',
                                  default=OTRK_SOURCE_NUMBER)

        self._parser.add_argument('-p', '--port', type=int,
                                  help=f'The port number (49152–65535) to send to. Default: {OTRK_MULTICAST_PORT}',
                                  default=OTRK_MULTICAST_PORT)

        self._parser.add_argument('-f', '--format',
                                  help='The format [JSON, CBOR] to use.',
                                  default='JSON')

        self._parser.add_argument('-r', '--ref',
                                  help='The time source [genlock, videoIn, ptp, ntp] to use.',
                                  default='NTP')

        self._parser.add_argument('-i', '--ip',
                                  help='The IP address to send to. Default: 235.135.1.1',
                                  default=f'{OTRK_MULTICAST_PREFIX}{OTRK_SOURCE_NUMBER}')

        self._parser.add_argument('-v', '--verbose',
                                  action='store_true',
                                  help='Enable packet information logging.')

        self._parser.add_argument('--num-segments', type=int,
                                  help='Fixed number of segments per packet (0 = auto based on payload size).',
                                  default=0)


class OpenTrackIOPacketTransmitter:
    """Handles creation and transmission of minimal OpenTrackIO packets with time source handling"""

    # Constants
    BASE_FREQUENCY = 24000
    FREQUENCY_DENOM = 1001
    FREQUENCY = BASE_FREQUENCY / FREQUENCY_DENOM
    INTERVAL = 1 / FREQUENCY

    def __init__(self, config):
        # Configuration
        self._source_number = config['source_number']
        self._multicast_port = config['port']
        self._multicast_group = config['multicast_group']
        self._payload_format = config['format']
        self._time_source = config['time_source']
        self._verbose = config['debug']
        self._fixed_num_segments = config['num-segments']

        # Sequence number for UDP packet headers (16-bit)
        self._sequence_number = 1

        # Frame counter for timecode
        self._frame_counter = 0

        # Time synchronization state
        self._ref_offset_s = 0.0
        self.ntpclient = ntplib.NTPClient() if self._time_source == TimeSource.NTP else None

        # Generate stable UUIDs for source and sample
        self._source_uuid = str(uuid.uuid4())
        self._sample_uuid = str(uuid.uuid4())

        # Animation parameters
        self._start_time = time.time()
        self._animation_duration_seconds = 10.0  # Animation cycle

        self._init_time_source()

    def start_transmission(self):
        """Start sending packets to the multicast group"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        print(f'Sending packets to {self._multicast_group}:{self._multicast_port} '
              f'at {self.FREQUENCY} packets per second')
        print(f'Using time source: {self._time_source.value}')

        try:
            while True:
                self._sample_uuid = str(uuid.uuid4())
                segments = self._create_opentrackio_packet()

                for segment in segments:

                    sock.sendto(segment, (self._multicast_group, self._multicast_port))

                time.sleep(self.INTERVAL)
        except KeyboardInterrupt:
            print("\nTransmission ended.")

    def _init_time_source(self):
        """Initialize time synchronization based on configured time source"""
        if self._time_source == TimeSource.PTP:
            # PTP initialization would go here in a real implementation
            print(f"Initializing PTP time source.")

        elif self._time_source == TimeSource.NTP:
            try:
                print(f"Initializing NTP time source using {NTPSERVER}.")
                ntp_response = self.ntpclient.request(NTPSERVER)
                self._ref_offset_s = ntp_response.offset
                print(f"NTP offset: {self._ref_offset_s} seconds.")
            except Exception as e:
                print(f"Warning: Failed to get NTP time from {NTPSERVER}: {e}.")
                print("Continuing with local system time.")

        elif self._time_source == TimeSource.GENLOCK:
            print(f"Initializing genlock time source.")

        elif self._time_source == TimeSource.VIDEO_IN:
            print(f"Initializing videoIn time source.")

    def _get_local_timestamp(self):
        """Get local timestamp adjusted for time source"""
        if self._time_source == TimeSource.NTP:
            timestamp = time.time() + self._ref_offset_s
            return timestamp
        else:
            return time.time()

    def _increment_sequence_number(self):
        """Update sequence number"""
        # Wrap around at 65535 (max 16-bit unsigned integer)
        if self._sequence_number >= UINT16_MAX:
            self._sequence_number = 1
        else:
            self._sequence_number += 1

    def _move_camera(self):
        """Update animation values based on time with more dramatic movement"""
        elapsed = (time.time() - self._start_time) % self._animation_duration_seconds
        progress = elapsed / self._animation_duration_seconds

        self._frame_counter = (self._frame_counter + 1) % 24

        sin_progress = math.sin(progress * 2 * math.pi)
        cos_progress = math.cos(progress * 2 * math.pi)

        x_pos = 1.0 + sin_progress * 3.0
        y_pos = 2.0 + cos_progress * 2.0
        z_pos = 3.0 + sin_progress * cos_progress * 4.0

        pan = 180.0 + sin_progress * 90.0
        tilt = 90.0 + cos_progress * 45.0
        roll = 45.0 + sin_progress * 30.0

        focus = 0.1 + abs(sin_progress) * 0.8
        iris = 0.2 + abs(cos_progress) * 0.6
        zoom = 0.3 + (0.5 + sin_progress / 2) * 0.7

        return {
            "x": x_pos, "y": y_pos, "z": z_pos,
            "pan": pan, "tilt": tilt, "roll": roll,
            "focus": focus, "iris": iris, "zoom": zoom
        }

    def _create_opentrackio_packet(self):
        """Create a minimal OpenTrackIO packet with time source information"""
        now = datetime.now()

        ref_timestamp = self._get_local_timestamp()
        seconds = int(ref_timestamp)
        fraction = ref_timestamp - seconds
        nanoseconds = int(fraction * 1_000_000_000)

        camera_anim = self._move_camera()

        payload_data = {
            "tracker": {
                "notes": "Example generated sample.",
                "recording": False,
                "slate": "A101_A_4",
                "status": "Optical Good"
            },
            "timing": {
                "mode": "internal" if self._time_source in [TimeSource.NTP, TimeSource.PTP] else "external",
                "sampleRate": {
                    "num": self.BASE_FREQUENCY,
                    "denom": self.FREQUENCY_DENOM
                },
                "sampleTimestamp": {
                    "seconds": seconds,
                    "nanoseconds": nanoseconds
                },
                "synchronization": {
                    "locked": True,
                    "source": self._time_source.value
                },
                "timecode": {
                    "hours": now.hour,
                    "minutes": now.minute,
                    "seconds": now.second,
                    "frames": self._frame_counter,
                    "frameRate": {
                        "num": self.BASE_FREQUENCY,
                        "denom": self.FREQUENCY_DENOM
                    }
                }
            },
            "lens": {
                "distortion": [
                    {
                        "radial": [1.0, 2.0, 3.0],
                        "tangential": [1.0, 2.0],
                        "overscan": 3.1
                    }
                ],
                "encoders": {
                    "focus": camera_anim["focus"],
                    "iris": camera_anim["iris"],
                    "zoom": camera_anim["zoom"]
                },
                "entrancePupilOffset": 0.123,
                "fStop": 4.0,
                "pinholeFocalLength": 24.305,
                "focusDistance": 10.0,
                "projectionOffset": {
                    "x": 0.1,
                    "y": 0.2
                }
            },
            "protocol": {
                "name": "OpenTrackIO",
                "version": [1, 0, 0]
            },
            "sampleId": f"urn:uuid:{self._sample_uuid}",
            "sourceId": f"urn:uuid:{self._source_uuid}",
            "sourceNumber": self._source_number,
            "transforms": [
                {
                    "translation": {
                        "x": camera_anim["x"],
                        "y": camera_anim["y"],
                        "z": camera_anim["z"]
                    },
                    "rotation": {
                        "pan": camera_anim["pan"],
                        "tilt": camera_anim["tilt"],
                        "roll": camera_anim["roll"]
                    },
                    "id": "Camera"
                }
            ]
        }

        if self._time_source in [TimeSource.GENLOCK, TimeSource.VIDEO_IN]:
            payload_data["timing"]["synchronization"]["frequency"] = {
                "num": self.BASE_FREQUENCY,
                "denom": self.FREQUENCY_DENOM
            }

        if self._time_source == TimeSource.PTP:
            payload_data["timing"]["synchronization"]["ptp"] = {
                "profile": "IEEE Std 1588-2019",
                "domain": 0,
                "leaderIdentity": "01:02:03:04:05:06",
                "leaderPriorities": {
                    "priority1": 128,
                    "priority2": 128
                },
                "leaderAccuracy": 0.000000050,
                "meanPathDelay": 0.000000100
            }

        if self._payload_format == PayloadFormat.CBOR:
            payload = dumps(payload_data)
        else:
            payload = json.dumps(payload_data).encode('utf-8')

        # Debug output for payload sizes
        if self._verbose and self._sequence_number == 1:  # First packet only
            print(f"Payload size: {len(payload)} bytes")
            if len(payload) > OTRK_MAX_PAYLOAD_SIZE:
                print(f"Payload exceeds {OTRK_MAX_PAYLOAD_SIZE} bytes, will be segmented")

        return self._construct_udp_segments(payload, self._payload_format.value)

    def _construct_udp_header(self, sequence_number, segment_offset, payload, encoding=0, last_segment=False):
        """Construct UDP packet header"""
        reserved = 0  # Reserved field (1 byte)
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

        checksum = self._fletcher16(header + payload)

        if self._verbose:
            print(f'''
            Header details:
              Header length: {OTRK_HEADER_LENGTH} bytes
              Encoding: {encoding}
              Sequence number: {sequence_number}
              Segment offset: {segment_offset}
              Last segment: {last_segment}
              Payload length: {payload_length} bytes
              Checksum: {int.from_bytes(checksum, byteorder='big')}
              Total packet size: {OTRK_HEADER_LENGTH + payload_length} bytes''')

        return header + checksum

    def _construct_udp_segments(self, payload, encoding=0):
        """Split payload into UDP segments with headers"""
        segments = []
        total_length = len(payload)

        # Determine max_payload_size and number of segments
        if self._fixed_num_segments > 0:
            # If user specified a fixed number of segments
            num_segments = self._fixed_num_segments
            max_payload_size = (total_length + num_segments - 1) // num_segments
        else:
            # Default behavior - auto segment based on max payload size
            max_payload_size = OTRK_MAX_PAYLOAD_SIZE

        for offset in range(0, total_length, max_payload_size):
            segment_payload = payload[offset: offset + max_payload_size]
            last_segment = (offset + max_payload_size >= total_length)

            header = self._construct_udp_header(
                sequence_number=self._sequence_number,
                segment_offset=offset,
                payload=segment_payload,
                encoding=encoding,
                last_segment=last_segment)

            self._increment_sequence_number()  # Every packet has a unique sequence number.

            segments.append(header + segment_payload)

        return segments

    @classmethod
    def _fletcher16(cls, data):
        """Calculate Fletcher-16 checksum."""
        sum1 = 0
        sum2 = 0
        for b in data:
            sum1 = (sum1 + b) % 255
            sum2 = (sum2 + sum1) % 255
        return bytes([sum1, sum2])


def main():
    parser = OpenTrackIOArgumentParser()
    config = parser.parse_args()

    transmitter = OpenTrackIOPacketTransmitter(config)
    transmitter.start_transmission()  # Blocks until keyboard interrupt.


if __name__ == "__main__":
    main()
