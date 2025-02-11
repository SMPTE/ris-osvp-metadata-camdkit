# OSVP Clip Documentation

## Introduction

The OSVP Clip (clip) is a collection of metadata parameters sampled over a
specified duration. Each parameter is either:

* static: the parameter has at constant value over the duration of the clip
* dynamic: the parameter is sampled at regular intervals over the duration of the clip

Each parameter is identified by a unique name. It also has a general description
as well as a specific set of constraints.

The OSVP Frame (frame) is a collection of metadata parameters that is dynamic and has a
synchronous relationship with a video frame. In an OSVP environment this describes live
camera position ('tracking') and lens data.

## Clip Parameters

### `duration`

#### Description

Duration of the clip

#### Units

second

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator
is in the range [0..2,147,483,647] and denominator in the range
(0..4,294,967,295].


### `captureFrameRate`

#### Description

Capture frame rate of the camera

#### Units

hertz

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator
is in the range [0..2,147,483,647] and denominator in the range
(0..4,294,967,295].


### `activeSensorPhysicalDimensions`

#### Description

Height and width of the active area of the camera sensor in microns

#### Units

millimeter

#### Sampling

Static

#### Constraints

The height and width shall be each be real non-negative numbers.

### `activeSensorResolution`

#### Description

Photosite resolution of the active area of the camera sensor in pixels

#### Units

pixel

#### Sampling

Static

#### Constraints

The height and width shall be each be an integer in the range
[0..2,147,483,647].


### `make`

#### Description

Non-blank string naming camera manufacturer

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `model`

#### Description

Non-blank string identifying camera model

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `serialNumber`

#### Description

Non-blank string uniquely identifying the camera

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `firmwareVersion`

#### Description

Non-blank string identifying camera firmware version

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `label`

#### Description

Non-blank string containing user-determined camera identifier

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `anamorphicSqueeze`

#### Description

Nominal ratio of height to width of the image of an axis-aligned
square captured by the camera sensor. It can be used to de-squeeze
images but is not however an exact number over the entire captured
area due to a lens' intrinsic analog nature.


#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator
is in the range [0..2,147,483,647] and denominator in the range
(0..4,294,967,295].


### `isoSpeed`

#### Description

Arithmetic ISO scale as defined in ISO 12232

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a integer in the range (1..4,294,967,295].

### `fdlLink`

#### Description

URN identifying the ASC Framing Decision List used by the camera.

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a UUID URN as specified in IETF RFC 4122.
Only lowercase characters shall be used.
Example: `f81d4fae-7dec-11d0-a765-00a0c91e6bf6`


### `shutterAngle`

#### Description

Shutter speed as a fraction of the capture frame rate. The shutter
speed (in units of 1/s) is equal to the value of the parameter divided
by 360 times the capture frame rate.


#### Units

degree

#### Sampling

Static

#### Constraints

The parameter shall be a real number in the range (0..360].

### `distortionOverscanMax`

#### Description

Static maximum overscan factor on lens distortion. This is primarily
relevant when storing overscan values, not in transmission as the
overscan should be calculated by the consumer.


#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a real number >= 1.

### `undistortionOverscanMax`

#### Description

Static maximum overscan factor on lens undistortion. This is primarily
relevant when storing overscan values, not in transmission as the
overscan should be calculated by the consumer.


#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a real number >= 1.

### `distortionIsProjection`

#### Description

Indicator that the OpenLensIO distortion model is the Projection
Characterization, not the Field-Of-View Characterization. This is 
primarily relevant when storing overscan values, not in transmission
as the overscan should be calculated by the consumer.


#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a boolean.

### `make`

#### Description

Non-blank string naming lens manufacturer

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `model`

#### Description

Non-blank string identifying lens model

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `serialNumber`

#### Description

Non-blank string uniquely identifying the lens

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `firmwareVersion`

#### Description

Non-blank string identifying lens firmware version

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `nominalFocalLength`

#### Description

Nominal focal length of the lens. The number printed on the side
of a prime lens, e.g. 50 mm, and undefined in the case of a zoom lens.


#### Units

millimeter

#### Sampling

Static

#### Constraints

The parameter shall be a real number greater than 0.

### `make`

#### Description

Non-blank string naming tracking device manufacturer

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `model`

#### Description

Non-blank string identifying tracking device model

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `serialNumber`

#### Description

Non-blank string uniquely identifying the tracking device

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `firmwareVersion`

#### Description

Non-blank string identifying tracking device firmware version

#### Units

None

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `notes`

#### Description

Non-blank string containing notes about tracking system

#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `recording`

#### Description

Boolean indicating whether tracking system is recording data

#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a boolean.

### `slate`

#### Description

Non-blank string describing the recording slate

#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `status`

#### Description

Non-blank string describing status of tracking system

#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a Unicode string between 0 and 1023
codepoints.


### `mode`

#### Description

Enumerated value indicating whether the sample transport mechanism
provides inherent ('external') timing, or whether the transport
mechanism lacks inherent timing and so the sample must contain a PTP
timestamp itself ('internal') to carry timing information.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be one of the allowed values.

### `recordedTimestamp`

#### Description

PTP timestamp of the data recording instant, provided for convenience
during playback of e.g. pre-recorded tracking data. The timestamp
comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
integer (nanoseconds)


#### Units

second

#### Sampling

Regular

#### Constraints

The parameter shall contain valid number of seconds, nanoseconds
elapsed since the start of the epoch.


### `sampleRate`

#### Description

Sample frame rate as a rational number. Drop frame rates such as
29.97 should be represented as e.g. 30000/1001. In a variable rate
system this should is estimated from the last sample delta time.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a rational number whose numerator
is in the range [0..2,147,483,647] and denominator in the range
(0..4,294,967,295].


### `sampleTimestamp`

#### Description

PTP timestamp of the data capture instant. Note this may differ
from the packet's transmission PTP timestamp. The timestamp
comprises a 48-bit unsigned integer (seconds), a 32-bit unsigned
integer (nanoseconds)


#### Units

second

#### Sampling

Regular

#### Constraints

The parameter shall contain valid number of seconds, nanoseconds
elapsed since the start of the epoch.


### `sequenceNumber`

#### Description

Integer incrementing with each sample.

#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..4,294,967,295].

### `synchronization`

#### Description

Object describing how the tracking device is synchronized for this
sample.

frequency: The frequency of a synchronization signal.This may differ from
the sample frame rate for example in a genlocked tracking device. This is
not required if the synchronization source is PTP or NTP.
locked: Is the tracking device locked to the synchronization source
offsets: Offsets in seconds between sync and sample. Critical for e.g.
frame remapping, or when using different data sources for
position/rotation and lens encoding
present: Is the synchronization source present (a synchronization
source can be present but not locked if frame rates differ for
example)
ptp: If the synchronization source is a PTP leader, then this object
contains:
- "profile": Specifies the PTP profile in use. This defines the operational
rules and parameters for synchronization. For example "SMPTE ST2059-2:2021"
for SMPTE 2110 based systems, or "IEEE Std 1588-2019" or
"IEEE Std 802.1AS-2020" for industrial applications
- "domain": Identifies the PTP domain the device belongs to. Devices in the
same domain can synchronize with each other
- "leaderIdentity": The unique identifier (usually MAC address) of the
current PTP leader (grandmaster)
- "leaderPriorities": The priority values of the leader used in the Best
Master Clock Algorithm (BMCA). Lower values indicate higher priority
- "priority1": Static priority set by the administrator
- "priority2": Dynamic priority based on the leader's role or clock quality
- "leaderAccuracy": The timing offset in seconds from the sample timestamp
to the PTP timestamp
- "meanPathDelay": The average round-trip delay between the device and the
PTP leader, measured in seconds
source: The source of synchronization must be defined as one of the
following:
- "vlan": Integer representing the VLAN ID for PTP traffic (e.g., 100 for
VLAN 100)
- "timeSource": Indicates the leader's source of time, such as GNSS, atomic
clock, or NTP
- "genlock": The tracking device has an external black/burst or
tri-level analog sync signal that is triggering the capture of
tracking samples
- "videoIn": The tracking device has an external video signal that is
triggering the capture of tracking samples
- "ptp": The tracking device is locked to a PTP leader
- "ntp": The tracking device is locked to an NTP server


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall contain the required valid fields.

### `timecode`

#### Description

SMPTE timecode of the sample. Timecode is a standard for labeling
individual frames of data in media systems and is useful for
inter-frame synchronization.
- format.frameRate: The frame rate as a rational number. Drop frame
rates such as 29.97 should be represented as e.g. 30000/1001. The
timecode frame rate may differ from the sample frequency.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall contain a valid format and hours, minutes,
seconds and frames with appropriate min/max values.


### `custom`

#### Description

This list provides optional additional custom coefficients that can 
extend the existing lens model. The meaning of and how these characteristics
are to be applied to a virtual camera would require negotiation between a
particular producer and consumer.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a tuple of items of the class itemClass.
The tuple can be empty


### `distortion`

#### Description

A list of Distortion objects that each define the coefficients for
calculating the distortion characteristics of a lens comprising radial
distortion coefficients of the spherical distortion (k1-N) and the
tangential distortion (p1-N). An optional key 'model' can be used that
describes the distortion model. The default is Brown-Conrady D-U (that
maps Distorted to Undistorted coordinates).


#### Units

None

#### Sampling

Regular

#### Constraints

The list shall contain at least one Distortion object, and in each
object the radial and tangential coefficients shall each be real numbers.


### `distortionOverscan`

#### Description

Overscan factor on lens distortion. This is primarily relevant when
storing overscan values, not in transmission as the overscan should be
calculated by the consumer.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a real number >= 1.

### `undistortionOverscan`

#### Description

Overscan factor on lens undistortion. This is primarily relevant when
storing overscan values, not in transmission as the overscan should be
calculated by the consumer.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a real number >= 1.

### `distortionOffset`

#### Description

Offset in x and y of the centre of distortion of the virtual camera

#### Units

millimeter

#### Sampling

Regular

#### Constraints

X and Y centre shift shall each be real numbers.

### `encoders`

#### Description

Normalised real numbers (0-1) for focus, iris and zoom.
Encoders are represented in this way (as opposed to raw integer
values) to ensure values remain independent of encoder resolution,
minimum and maximum (at an acceptable loss of precision).
These values are only relevant in lenses with end-stops that
demarcate the 0 and 1 range.
Value should be provided in the following directions (if known):
Focus:   0=infinite     1=closest
Iris:    0=open         1=closed
Zoom:    0=wide angle   1=telephoto


#### Units

None

#### Sampling

Regular

#### Constraints


The parameter shall contain at least one normalised values (0..1) for the FIZ encoders.


### `entrancePupilOffset`

#### Description

Offset of the entrance pupil relative to the nominal imaging plane
(positive if the entrance pupil is located on the side of the nominal
imaging plane that is towards the object, and negative otherwise).
Measured in meters as in a render engine it is often applied in the
virtual camera's transform chain.


#### Units

meter

#### Sampling

Regular

#### Constraints

The parameter shall be a real number.

### `exposureFalloff`

#### Description

Coefficients for calculating the exposure fall-off (vignetting) of
a lens


#### Units

None

#### Sampling

Regular

#### Constraints

The coefficients shall each be real numbers.

### `fStop`

#### Description

The linear f-number of the lens, equal to the focal length divided
by the diameter of the entrance pupil.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a non-negative real number.

### `focalLength`

#### Description

Focal length of the lens.

#### Units

millimeter

#### Sampling

Regular

#### Constraints

The parameter shall be a non-negative real number.

### `focusDistance`

#### Description

Focus distance/position of the lens

#### Units

meter

#### Sampling

Regular

#### Constraints

The parameter shall be a real number greater than 0.

### `projectionOffset`

#### Description

Offset in x and y of the centre of perspective projection of the
virtual camera


#### Units

millimeter

#### Sampling

Regular

#### Constraints

X and Y projection offset shall each be real numbers.

### `rawEncoders`

#### Description

Raw encoder values for focus, iris and zoom.
These values are dependent on encoder resolution and before any
homing / ranging has taken place.


#### Units

None

#### Sampling

Regular

#### Constraints


The parameter shall contain at least one integer value for the FIZ encoders.


### `tStop`

#### Description

Linear t-number of the lens, equal to the F-number of the lens
divided by the square root of the transmittance of the lens.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a non-negative real number.

### `protocol`

#### Description

Name of the protocol in which the sample is being employed, and
version of that protocol


#### Units

None

#### Sampling

Regular

#### Constraints

Protocol name is nonblank string; protocol version is basic x.y.z
semantic versioning string


### `sampleId`

#### Description

URN serving as unique identifier of the sample in which data is
being transported.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a UUID URN as specified in IETF RFC 4122.
Only lowercase characters shall be used.
Example: `f81d4fae-7dec-11d0-a765-00a0c91e6bf6`


### `sourceId`

#### Description

URN serving as unique identifier of the source from which data is
being transported.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a UUID URN as specified in IETF RFC 4122.
Only lowercase characters shall be used.
Example: `f81d4fae-7dec-11d0-a765-00a0c91e6bf6`


### `sourceNumber`

#### Description

Number that identifies the index of the stream from a source from which
data is being transported. This is most important in the case where a source
is producing multiple streams of samples.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..4,294,967,295].

### `relatedSampleIds`

#### Description

List of sampleId properties of samples related to this sample. The
existence of a sample with a given sampleId is not guaranteed.


#### Units

None

#### Sampling

Regular

#### Constraints

The parameter shall be a tuple of items of the class itemClass.
The tuple can be empty


### `globalStage`

#### Description

Position of stage origin in global ENU and geodetic coordinates
(E, N, U, lat0, lon0, h0). Note this may be dynamic if the stage is
inside a moving vehicle.


#### Units

meter

#### Sampling

Regular

#### Constraints

Each field in the GlobalPosition shall be a real number

### `transforms`

#### Description

A list of transforms.
Transforms are composed in order with the last in the list representing
the X,Y,Z in meters of camera sensor relative to stage origin.
The Z axis points upwards and the coordinate system is right-handed.
Y points in the forward camera direction (when pan, tilt and roll are
zero).
For example in an LED volume Y would point towards the centre of the
LED wall and so X would point to camera-right.
Rotation expressed as euler angles in degrees of the camera sensor
relative to stage origin
Rotations are intrinsic and are measured around the axes ZXY, commonly
referred to as [pan, tilt, roll]
Notes on Euler angles:
Euler angles are human readable and unlike quarternions, provide the
ability for cycles (with angles >360 or <0 degrees).
Where a tracking system is providing the pose of a virtual camera,
gimbal lock does not present the physical challenges of a robotic
system.
Conversion to and from quarternions is trivial with an acceptable loss
of precision.


#### Units

meter / degree

#### Sampling

Regular

#### Constraints

Each component of each transform shall contain Real numbers.

## Reader coverage

The following table indicates the camera parameters supported by each of the readers.

| Reader      | duration | captureFrameRate | activeSensorPhysicalDimensions | activeSensorResolution | make | model | serialNumber | firmwareVersion | label | anamorphicSqueeze | isoSpeed | fdlLink | shutterAngle | distortionOverscanMax | undistortionOverscanMax | distortionIsProjection | make | model | serialNumber | firmwareVersion | nominalFocalLength | make | model | serialNumber | firmwareVersion | notes | recording | slate | status | mode | recordedTimestamp | sampleRate | sampleTimestamp | sequenceNumber | synchronization | timecode | custom | distortion | distortionOverscan | undistortionOverscan | distortionOffset | encoders | entrancePupilOffset | exposureFalloff | fStop | focalLength | focusDistance | projectionOffset | rawEncoders | tStop | protocol | sampleId | sourceId | sourceNumber | relatedSampleIds | globalStage | transforms |
| ----------- | ----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |
| RED | + | + | + | | + | + | + | + | | + | + | | + | | | | + | + | + | + | | | | | | | | | | | | | | | | | | | | | | | + | | | + | + | | | + | | | | | | | |
| ARRI | + | + | + | | + | + | + | | | + | + | | + | | | | + | + | + | | | | | | | | | | | | | | | | | | | | | | | | | | | + | + | | | + | | | | | | | |
| Venice | + | + | + | | + | + | + | + | | + | + | | + | | | | | + | + | | | | | | | | | | | | | | | | | | | | | | | | | | | + | + | | | + | | | | | | | |
| Canon | + | | | | + | | | | | + | + | | + | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | + | + | | | + | | | | | | | |
## Clip JSON Schema

```{
  "$id": "https://opentrackio.org/schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "static": {
      "type": "object",
      "properties": {
        "duration": {
          "type": "object",
          "properties": {
            "num": {
              "type": "integer",
              "maximum": 2147483647,
              "minimum": 1
            },
            "denom": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 1
            }
          },
          "required": [
            "num",
            "denom"
          ],
          "additionalProperties": false,
          "description": "Duration of the clip",
          "units": "second"
        },
        "camera": {
          "type": "object",
          "properties": {
            "captureFrameRate": {
              "type": "object",
              "properties": {
                "num": {
                  "type": "integer",
                  "maximum": 2147483647,
                  "minimum": 1
                },
                "denom": {
                  "type": "integer",
                  "maximum": 4294967295,
                  "minimum": 1
                }
              },
              "required": [
                "num",
                "denom"
              ],
              "additionalProperties": false,
              "description": "Capture frame rate of the camera",
              "units": "hertz"
            },
            "activeSensorPhysicalDimensions": {
              "type": "object",
              "properties": {
                "height": {
                  "type": "number",
                  "minimum": 0.0
                },
                "width": {
                  "type": "number",
                  "minimum": 0.0
                }
              },
              "required": [
                "height",
                "width"
              ],
              "description": "Height and width of the active area of the camera sensor in microns",
              "additionalProperties": false,
              "units": "millimeter"
            },
            "activeSensorResolution": {
              "type": "object",
              "properties": {
                "height": {
                  "type": "integer",
                  "maximum": 2147483647,
                  "minimum": 0
                },
                "width": {
                  "type": "integer",
                  "maximum": 2147483647,
                  "minimum": 0
                }
              },
              "required": [
                "height",
                "width"
              ],
              "description": "Photosite resolution of the active area of the camera sensor in pixels",
              "additionalProperties": false,
              "units": "pixel"
            },
            "make": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string naming camera manufacturer"
            },
            "model": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying camera model"
            },
            "serialNumber": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string uniquely identifying the camera"
            },
            "firmwareVersion": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying camera firmware version"
            },
            "label": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string containing user-determined camera identifier"
            },
            "anamorphicSqueeze": {
              "type": "object",
              "properties": {
                "num": {
                  "type": "integer",
                  "maximum": 2147483647,
                  "minimum": 1
                },
                "denom": {
                  "type": "integer",
                  "maximum": 4294967295,
                  "minimum": 1
                }
              },
              "required": [
                "num",
                "denom"
              ],
              "additionalProperties": false,
              "description": "Nominal ratio of height to width of the image of an axis-aligned\nsquare captured by the camera sensor. It can be used to de-squeeze\nimages but is not however an exact number over the entire captured\narea due to a lens' intrinsic analog nature.\n"
            },
            "isoSpeed": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 1,
              "description": "Arithmetic ISO scale as defined in ISO 12232"
            },
            "fdlLink": {
              "type": "string",
              "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
              "description": "URN identifying the ASC Framing Decision List used by the camera."
            },
            "shutterAngle": {
              "type": "number",
              "maximum": 360.0,
              "minimum": 0.0,
              "description": "Shutter speed as a fraction of the capture frame rate. The shutter\nspeed (in units of 1/s) is equal to the value of the parameter divided\nby 360 times the capture frame rate.\n",
              "units": "degree"
            }
          },
          "additionalProperties": false
        },
        "lens": {
          "type": "object",
          "properties": {
            "distortionOverscanMax": {
              "type": "number",
              "minimum": 1.0,
              "description": "Static maximum overscan factor on lens distortion. This is primarily\nrelevant when storing overscan values, not in transmission as the\noverscan should be calculated by the consumer.\n"
            },
            "undistortionOverscanMax": {
              "type": "number",
              "minimum": 1.0,
              "description": "Static maximum overscan factor on lens undistortion. This is primarily\nrelevant when storing overscan values, not in transmission as the\noverscan should be calculated by the consumer.\n"
            },
            "distortionIsProjection": {
              "type": "boolean",
              "description": "Indicator that the OpenLensIO distortion model is the Projection\nCharacterization, not the Field-Of-View Characterization. This is \nprimarily relevant when storing overscan values, not in transmission\nas the overscan should be calculated by the consumer.\n"
            },
            "make": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string naming lens manufacturer"
            },
            "model": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying lens model"
            },
            "serialNumber": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string uniquely identifying the lens"
            },
            "firmwareVersion": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying lens firmware version"
            },
            "nominalFocalLength": {
              "type": "number",
              "exclusiveMinimum": 0.0,
              "description": "Nominal focal length of the lens. The number printed on the side\nof a prime lens, e.g. 50 mm, and undefined in the case of a zoom lens.\n",
              "units": "millimeter"
            }
          },
          "additionalProperties": false
        },
        "tracker": {
          "type": "object",
          "properties": {
            "make": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string naming tracking device manufacturer"
            },
            "model": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying tracking device model"
            },
            "serialNumber": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string uniquely identifying the tracking device"
            },
            "firmwareVersion": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1023,
              "description": "Non-blank string identifying tracking device firmware version"
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "tracker": {
      "type": "object",
      "properties": {
        "notes": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1023,
          "description": "Non-blank string containing notes about tracking system"
        },
        "recording": {
          "type": "boolean",
          "description": "Boolean indicating whether tracking system is recording data"
        },
        "slate": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1023,
          "description": "Non-blank string describing the recording slate"
        },
        "status": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1023,
          "description": "Non-blank string describing status of tracking system"
        }
      },
      "additionalProperties": false
    },
    "timing": {
      "type": "object",
      "properties": {
        "mode": {
          "enum": [
            "internal",
            "external"
          ],
          "type": "string",
          "description": "Enumerated value indicating whether the sample transport mechanism\nprovides inherent ('external') timing, or whether the transport\nmechanism lacks inherent timing and so the sample must contain a PTP\ntimestamp itself ('internal') to carry timing information.\n"
        },
        "recordedTimestamp": {
          "type": "object",
          "properties": {
            "seconds": {
              "type": "integer",
              "maximum": 281474976710655,
              "minimum": 0
            },
            "nanoseconds": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 0
            }
          },
          "required": [
            "seconds",
            "nanoseconds"
          ],
          "additionalProperties": false,
          "units": "second",
          "description": "PTP timestamp of the data recording instant, provided for convenience\nduring playback of e.g. pre-recorded tracking data. The timestamp\ncomprises a 48-bit unsigned integer (seconds), a 32-bit unsigned\ninteger (nanoseconds)\n"
        },
        "sampleRate": {
          "type": "object",
          "properties": {
            "num": {
              "type": "integer",
              "maximum": 2147483647,
              "minimum": 1
            },
            "denom": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 1
            }
          },
          "required": [
            "num",
            "denom"
          ],
          "additionalProperties": false,
          "description": "Sample frame rate as a rational number. Drop frame rates such as\n29.97 should be represented as e.g. 30000/1001. In a variable rate\nsystem this should is estimated from the last sample delta time.\n"
        },
        "sampleTimestamp": {
          "type": "object",
          "properties": {
            "seconds": {
              "type": "integer",
              "maximum": 281474976710655,
              "minimum": 0
            },
            "nanoseconds": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 0
            }
          },
          "required": [
            "seconds",
            "nanoseconds"
          ],
          "additionalProperties": false,
          "units": "second",
          "description": "PTP timestamp of the data capture instant. Note this may differ\nfrom the packet's transmission PTP timestamp. The timestamp\ncomprises a 48-bit unsigned integer (seconds), a 32-bit unsigned\ninteger (nanoseconds)\n"
        },
        "sequenceNumber": {
          "type": "integer",
          "maximum": 4294967295,
          "minimum": 0,
          "description": "Integer incrementing with each sample."
        },
        "synchronization": {
          "type": "object",
          "properties": {
            "locked": {
              "type": "boolean"
            },
            "source": {
              "enum": [
                "genlock",
                "videoIn",
                "ptp",
                "ntp"
              ],
              "type": "string"
            },
            "frequency": {
              "type": "object",
              "properties": {
                "num": {
                  "type": "integer",
                  "maximum": 2147483647,
                  "minimum": 1
                },
                "denom": {
                  "type": "integer",
                  "maximum": 4294967295,
                  "minimum": 1
                }
              },
              "required": [
                "num",
                "denom"
              ],
              "additionalProperties": false
            },
            "offsets": {
              "type": "object",
              "properties": {
                "translation": {
                  "type": "number"
                },
                "rotation": {
                  "type": "number"
                },
                "lensEncoders": {
                  "type": "number"
                }
              },
              "additionalProperties": false
            },
            "present": {
              "type": "boolean"
            },
            "ptp": {
              "type": "object",
              "properties": {
                "profile": {
                  "enum": [
                    "IEEE Std 1588-2019",
                    "IEEE Std 802.1AS-2020",
                    "SMPTE ST2059-2:2021"
                  ],
                  "type": "string"
                },
                "domain": {
                  "type": "integer",
                  "maximum": 127,
                  "minimum": 0
                },
                "leaderIdentity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 1023,
                  "pattern": "(?:^[0-9a-f]{2}(?::[0-9a-f]{2}){5}$)|(?:^[0-9a-f]{2}(?:-[0-9a-f]{2}){5}$)"
                },
                "leaderPriorities": {
                  "type": "object",
                  "properties": {
                    "priority1": {
                      "type": "integer",
                      "maximum": 255,
                      "minimum": 0
                    },
                    "priority2": {
                      "type": "integer",
                      "maximum": 255,
                      "minimum": 0
                    }
                  },
                  "required": [
                    "priority1",
                    "priority2"
                  ],
                  "description": "Data structure for PTP synchronization priorities",
                  "additionalProperties": false
                },
                "leaderAccuracy": {
                  "type": "number",
                  "minimum": 0.0
                },
                "timeSource": {
                  "enum": [
                    "GNSS",
                    "Atomic clock",
                    "NTP"
                  ],
                  "type": "string"
                },
                "meanPathDelay": {
                  "type": "number",
                  "minimum": 0.0
                },
                "vlan": {
                  "type": "integer",
                  "maximum": 4294967295,
                  "minimum": 0
                }
              },
              "required": [
                "profile",
                "domain",
                "leaderIdentity",
                "leaderPriorities",
                "leaderAccuracy",
                "meanPathDelay"
              ],
              "additionalProperties": false
            }
          },
          "required": [
            "locked",
            "source"
          ],
          "additionalProperties": false,
          "description": "Object describing how the tracking device is synchronized for this\nsample.\n\nfrequency: The frequency of a synchronization signal.This may differ from\nthe sample frame rate for example in a genlocked tracking device. This is\nnot required if the synchronization source is PTP or NTP.\nlocked: Is the tracking device locked to the synchronization source\noffsets: Offsets in seconds between sync and sample. Critical for e.g.\nframe remapping, or when using different data sources for\nposition/rotation and lens encoding\npresent: Is the synchronization source present (a synchronization\nsource can be present but not locked if frame rates differ for\nexample)\nptp: If the synchronization source is a PTP leader, then this object\ncontains:\n- \"profile\": Specifies the PTP profile in use. This defines the operational\nrules and parameters for synchronization. For example \"SMPTE ST2059-2:2021\"\nfor SMPTE 2110 based systems, or \"IEEE Std 1588-2019\" or\n\"IEEE Std 802.1AS-2020\" for industrial applications\n- \"domain\": Identifies the PTP domain the device belongs to. Devices in the\nsame domain can synchronize with each other\n- \"leaderIdentity\": The unique identifier (usually MAC address) of the\ncurrent PTP leader (grandmaster)\n- \"leaderPriorities\": The priority values of the leader used in the Best\nMaster Clock Algorithm (BMCA). Lower values indicate higher priority\n- \"priority1\": Static priority set by the administrator\n- \"priority2\": Dynamic priority based on the leader's role or clock quality\n- \"leaderAccuracy\": The timing offset in seconds from the sample timestamp\nto the PTP timestamp\n- \"meanPathDelay\": The average round-trip delay between the device and the\nPTP leader, measured in seconds\nsource: The source of synchronization must be defined as one of the\nfollowing:\n- \"vlan\": Integer representing the VLAN ID for PTP traffic (e.g., 100 for\nVLAN 100)\n- \"timeSource\": Indicates the leader's source of time, such as GNSS, atomic\nclock, or NTP\n- \"genlock\": The tracking device has an external black/burst or\ntri-level analog sync signal that is triggering the capture of\ntracking samples\n- \"videoIn\": The tracking device has an external video signal that is\ntriggering the capture of tracking samples\n- \"ptp\": The tracking device is locked to a PTP leader\n- \"ntp\": The tracking device is locked to an NTP server\n"
        },
        "timecode": {
          "type": "object",
          "properties": {
            "hours": {
              "type": "integer",
              "maximum": 23,
              "minimum": 0
            },
            "minutes": {
              "type": "integer",
              "maximum": 59,
              "minimum": 0
            },
            "seconds": {
              "type": "integer",
              "maximum": 59,
              "minimum": 0
            },
            "frames": {
              "type": "integer",
              "maximum": 119,
              "minimum": 0
            },
            "format": {
              "type": "object",
              "properties": {
                "frameRate": {
                  "type": "object",
                  "properties": {
                    "num": {
                      "type": "integer",
                      "maximum": 2147483647,
                      "minimum": 1
                    },
                    "denom": {
                      "type": "integer",
                      "maximum": 4294967295,
                      "minimum": 1
                    }
                  },
                  "required": [
                    "num",
                    "denom"
                  ],
                  "additionalProperties": false
                },
                "subFrame": {
                  "type": "integer",
                  "maximum": 4294967295,
                  "minimum": 0
                }
              },
              "required": [
                "frameRate"
              ],
              "description": "The timecode format is defined as a rational frame rate and - where a\nsignal with sub-frames is described, such as an interlaced signal - an\nindex of which sub-frame is referred to by the timecode.\n",
              "additionalProperties": false
            }
          },
          "required": [
            "hours",
            "minutes",
            "seconds",
            "frames",
            "format"
          ],
          "description": "SMPTE timecode of the sample. Timecode is a standard for labeling\nindividual frames of data in media systems and is useful for\ninter-frame synchronization.\n- format.frameRate: The frame rate as a rational number. Drop frame\nrates such as 29.97 should be represented as e.g. 30000/1001. The\ntimecode frame rate may differ from the sample frequency.\n",
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "lens": {
      "type": "object",
      "properties": {
        "custom": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "description": "This list provides optional additional custom coefficients that can \nextend the existing lens model. The meaning of and how these characteristics\nare to be applied to a virtual camera would require negotiation between a\nparticular producer and consumer.\n"
        },
        "distortion": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "radial": {
                "type": "array",
                "items": {
                  "type": "number"
                },
                "minItems": 1
              },
              "tangential": {
                "type": "array",
                "items": {
                  "type": "number"
                },
                "minItems": 1
              },
              "model": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1023
              }
            },
            "required": [
              "radial"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "description": "A list of Distortion objects that each define the coefficients for\ncalculating the distortion characteristics of a lens comprising radial\ndistortion coefficients of the spherical distortion (k1-N) and the\ntangential distortion (p1-N). An optional key 'model' can be used that\ndescribes the distortion model. The default is Brown-Conrady D-U (that\nmaps Distorted to Undistorted coordinates).\n"
        },
        "distortionOverscan": {
          "type": "number",
          "minimum": 1.0,
          "description": "Overscan factor on lens distortion. This is primarily relevant when\nstoring overscan values, not in transmission as the overscan should be\ncalculated by the consumer.\n"
        },
        "undistortionOverscan": {
          "type": "number",
          "minimum": 1.0,
          "description": "Overscan factor on lens undistortion. This is primarily relevant when\nstoring overscan values, not in transmission as the overscan should be\ncalculated by the consumer.\n"
        },
        "distortionOffset": {
          "type": "object",
          "properties": {
            "x": {
              "type": "number"
            },
            "y": {
              "type": "number"
            }
          },
          "required": [
            "x",
            "y"
          ],
          "additionalProperties": false,
          "description": "Offset in x and y of the centre of distortion of the virtual camera",
          "units": "millimeter"
        },
        "encoders": {
          "type": "object",
          "properties": {
            "focus": {
              "type": "number",
              "maximum": 1.0,
              "minimum": 0.0
            },
            "iris": {
              "type": "number",
              "maximum": 1.0,
              "minimum": 0.0
            },
            "zoom": {
              "type": "number",
              "maximum": 1.0,
              "minimum": 0.0
            }
          },
          "additionalProperties": false,
          "description": "Normalised real numbers (0-1) for focus, iris and zoom.\nEncoders are represented in this way (as opposed to raw integer\nvalues) to ensure values remain independent of encoder resolution,\nminimum and maximum (at an acceptable loss of precision).\nThese values are only relevant in lenses with end-stops that\ndemarcate the 0 and 1 range.\nValue should be provided in the following directions (if known):\nFocus:   0=infinite     1=closest\nIris:    0=open         1=closed\nZoom:    0=wide angle   1=telephoto\n",
          "anyOf": [
            {
              "required": [
                "focus"
              ]
            },
            {
              "required": [
                "iris"
              ]
            },
            {
              "required": [
                "zoom"
              ]
            }
          ]
        },
        "entrancePupilOffset": {
          "type": "number",
          "description": "Offset of the entrance pupil relative to the nominal imaging plane\n(positive if the entrance pupil is located on the side of the nominal\nimaging plane that is towards the object, and negative otherwise).\nMeasured in meters as in a render engine it is often applied in the\nvirtual camera's transform chain.\n",
          "units": "meter"
        },
        "exposureFalloff": {
          "type": "object",
          "properties": {
            "a1": {
              "type": "number"
            },
            "a2": {
              "type": "number"
            },
            "a3": {
              "type": "number"
            }
          },
          "required": [
            "a1"
          ],
          "additionalProperties": false,
          "description": "Coefficients for calculating the exposure fall-off (vignetting) of\na lens\n"
        },
        "fStop": {
          "type": "number",
          "minimum": 0.0,
          "description": "The linear f-number of the lens, equal to the focal length divided\nby the diameter of the entrance pupil.\n"
        },
        "focalLength": {
          "type": "number",
          "minimum": 0.0,
          "description": "Focal length of the lens.",
          "units": "millimeter"
        },
        "focusDistance": {
          "type": "number",
          "exclusiveMinimum": 0.0,
          "description": "Focus distance/position of the lens",
          "units": "meter"
        },
        "projectionOffset": {
          "type": "object",
          "properties": {
            "x": {
              "type": "number"
            },
            "y": {
              "type": "number"
            }
          },
          "required": [
            "x",
            "y"
          ],
          "additionalProperties": false,
          "description": "Offset in x and y of the centre of perspective projection of the\nvirtual camera\n",
          "units": "millimeter"
        },
        "rawEncoders": {
          "type": "object",
          "properties": {
            "focus": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 0
            },
            "iris": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 0
            },
            "zoom": {
              "type": "integer",
              "maximum": 4294967295,
              "minimum": 0
            }
          },
          "additionalProperties": false,
          "description": "Raw encoder values for focus, iris and zoom.\nThese values are dependent on encoder resolution and before any\nhoming / ranging has taken place.\n",
          "anyOf": [
            {
              "required": [
                "focus"
              ]
            },
            {
              "required": [
                "iris"
              ]
            },
            {
              "required": [
                "zoom"
              ]
            }
          ]
        },
        "tStop": {
          "type": "number",
          "minimum": 0.0,
          "description": "Linear t-number of the lens, equal to the F-number of the lens\ndivided by the square root of the transmittance of the lens.\n"
        }
      },
      "additionalProperties": false
    },
    "protocol": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1023
        },
        "version": {
          "type": "array",
          "items": {
            "type": "integer",
            "maximum": 9,
            "minimum": 0
          },
          "minItems": 3,
          "maxItems": 3
        }
      },
      "required": [
        "name",
        "version"
      ],
      "additionalProperties": false,
      "description": "Name of the protocol in which the sample is being employed, and\nversion of that protocol\n"
    },
    "sampleId": {
      "type": "string",
      "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "URN serving as unique identifier of the sample in which data is\nbeing transported.\n"
    },
    "sourceId": {
      "type": "string",
      "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
      "description": "URN serving as unique identifier of the source from which data is\nbeing transported.\n"
    },
    "sourceNumber": {
      "type": "integer",
      "maximum": 4294967295,
      "minimum": 0,
      "description": "Number that identifies the index of the stream from a source from which\ndata is being transported. This is most important in the case where a source\nis producing multiple streams of samples.\n"
    },
    "relatedSampleIds": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
      },
      "description": "List of sampleId properties of samples related to this sample. The\nexistence of a sample with a given sampleId is not guaranteed.\n"
    },
    "globalStage": {
      "type": "object",
      "properties": {
        "E": {
          "type": "number"
        },
        "N": {
          "type": "number"
        },
        "U": {
          "type": "number"
        },
        "lat0": {
          "type": "number"
        },
        "lon0": {
          "type": "number"
        },
        "h0": {
          "type": "number"
        }
      },
      "required": [
        "E",
        "N",
        "U",
        "lat0",
        "lon0",
        "h0"
      ],
      "description": "Position of stage origin in global ENU and geodetic coordinates\n(E, N, U, lat0, lon0, h0). Note this may be dynamic if the stage is\ninside a moving vehicle.\n",
      "additionalProperties": false,
      "units": "meter"
    },
    "transforms": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "translation": {
            "type": "object",
            "properties": {
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "z": {
                "type": "number"
              }
            },
            "additionalProperties": false,
            "units": "meter"
          },
          "rotation": {
            "type": "object",
            "properties": {
              "pan": {
                "type": "number"
              },
              "tilt": {
                "type": "number"
              },
              "roll": {
                "type": "number"
              }
            },
            "additionalProperties": false,
            "units": "degree"
          },
          "scale": {
            "type": "object",
            "properties": {
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "z": {
                "type": "number"
              }
            },
            "additionalProperties": false
          },
          "id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1023
          }
        },
        "required": [
          "translation",
          "rotation"
        ],
        "additionalProperties": false
      },
      "minItems": 1,
      "description": "A list of transforms.\nTransforms are composed in order with the last in the list representing\nthe X,Y,Z in meters of camera sensor relative to stage origin.\nThe Z axis points upwards and the coordinate system is right-handed.\nY points in the forward camera direction (when pan, tilt and roll are\nzero).\nFor example in an LED volume Y would point towards the centre of the\nLED wall and so X would point to camera-right.\nRotation expressed as euler angles in degrees of the camera sensor\nrelative to stage origin\nRotations are intrinsic and are measured around the axes ZXY, commonly\nreferred to as [pan, tilt, roll]\nNotes on Euler angles:\nEuler angles are human readable and unlike quarternions, provide the\nability for cycles (with angles >360 or <0 degrees).\nWhere a tracking system is providing the pose of a virtual camera,\ngimbal lock does not present the physical challenges of a robotic\nsystem.\nConversion to and from quarternions is trivial with an acceptable loss\nof precision.\n",
      "units": "meter / degree",
      "uniqueItems": false
    }
  }
}
```
