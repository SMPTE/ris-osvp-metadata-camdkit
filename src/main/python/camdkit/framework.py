

from fractions import Fraction

from camdkit.lens_types import (FizEncoders, RawFizEncoders, ExposureFalloff,
                                Distortion, DistortionOffset, ProjectionOffset)
from camdkit.timing_types import SynchronizationSource as SynchronizationSourceEnum
from camdkit.timing_types import (Timestamp, TimecodeFormat, TimingMode, Timecode,
                                  SynchronizationOffsets, SynchronizationPTP, Synchronization)
from camdkit.tracker_types import GlobalPosition
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.versioning_types import (OPENTRACKIO_PROTOCOL_NAME,
                                      OPENTRACKIO_PROTOCOL_VERSION,
                                      VersionedProtocol)