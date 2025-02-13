

from fractions import Fraction

from camdkit.camera_types import PhysicalDimensions as ActiveSensorPhysicalDimensions
from camdkit.camera_types import SenselDimensions as Dimensions
from camdkit.lens_types import (FizEncoders, RawFizEncoders,
                                ExposureFalloff,
                                Distortion, DistortionOffset,
                                ProjectionOffset)
from camdkit.numeric_types import StrictlyPositiveRational
from camdkit.timing_types import SynchronizationSource as SynchronizationSourceEnum
from camdkit.timing_types import (PTPProfile, Timestamp,
                                  TimingMode, Timecode,
                                  SynchronizationOffsets, SynchronizationPTPPriorities, SynchronizationPTP,
                                  Synchronization)
from camdkit.tracker_types import GlobalPosition
from camdkit.transform_types import Vector3, Rotator3, Transform
from camdkit.versioning_types import (OPENTRACKIO_PROTOCOL_NAME,
                                      OPENTRACKIO_PROTOCOL_VERSION,
                                      VersionedProtocol)