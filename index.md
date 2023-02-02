# OSVP Clip documentation

## Introduction

The OSVP Clip (clip) is a collection of metadata parameters sampled over a
specified duration. Each parameter is either:

* static: the parameter has at constant value over the duration of the clip
* dynamic: the parameter is sampled at regular intervals over the duration of the clip

Each parameter is identified by a unique name. It also has a general description
as well as a specific set of constraints.

## Parameters

### `active_sensor_physical_dimensions`

#### Description

Height and width of the active area of the camera sensor

#### Units

micron

#### Sampling

Static

#### Constraints

The height and width shall be each be an integer in the range [0..2,147,483,647].

### `anamorphic_squeeze`

#### Description

Nominal ratio of height to width of the image of an axis-aligned square
  captured by the camera sensor. It can be used to de-squeeze images but is not
  however an exact number over the entire captured area due to a lens' intrinsic
  analog nature.

#### Units

0.01 unit

#### Sampling

Static

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `camera_firmware`

#### Description

Version identifier for the firmware of the camera

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `camera_make`

#### Description

Make of the camera

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `camera_model`

#### Description

Model of the camera

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `camera_serial_number`

#### Description

Unique identifier of the camera

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `capture_fps`

#### Description

Capture frame frate of the camera

#### Units

hertz

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `duration`

#### Description

Duration of the clip

#### Units

second

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `entrance_pupil_position`

#### Description

Entrance pupil diameter of the lens

#### Units

millimeter

#### Sampling

Regular

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `f_number`

#### Description

The linear f-number of the lens, equal to the focal length divided by the
  diameter of the entrance pupil.

#### Units

0.001 unit

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `fdl_link`

#### Description

Unique identifier of the FDL used by the camera.

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a UUID URN as specified in IETF RFC 4122. Onlyu lowercase characters shall be used.
    Example: `urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6`

### `focal_length`

#### Description

Focal length of the lens

#### Units

millimeter

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `focal_position`

#### Description

Focus distance/position of the lens

#### Units

millimeter

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `iso`

#### Description

Arithmetic ISO scale as defined in ISO 12232

#### Units

unit

#### Sampling

Static

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `lens_firmware`

#### Description

Version identifier for the firmware of the lens

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `lens_make`

#### Description

Make of the lens

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `lens_model`

#### Description

Model of the lens

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `lens_serial_number`

#### Description

Unique identifier of the lens

#### Units

n/a

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `shutter_angle`

#### Description

Shutter speed as a fraction of the capture frame rate. The shutter speed
  (in units of 1/s) is equal to the value of the parameter divided by 360 times
  the capture frame rate.

#### Units

degrees (angular)

#### Sampling

Static

#### Constraints

The parameter shall be an integer in the range (0..360000].

### `t_number`

#### Description

The linear t-number of the lens, equal to the F-number of the lens divided
  by the square root of the transmittance of the lens.

#### Units

0.001 unit

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

## JSON Schema

```{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {},
  "active_sensor_physical_dimensions": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "height",
      "width"
    ],
    "properties": {
      "height": {
        "type": "integer",
        "minimum": 0,
        "maximum": 2147483647
      },
      "width": {
        "type": "integer",
        "minimum": 0,
        "maximum": 2147483647
      }
    }
  },
  "anamorphic_squeeze": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2147483647
  },
  "camera_firmware": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "camera_make": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "camera_model": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "camera_serial_number": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "capture_fps": {
    "type": "string",
    "regex": "[0-9]{1,10}/[0-9]{1,10}"
  },
  "duration": {
    "type": "string",
    "regex": "[0-9]{1,10}/[0-9]{1,10}"
  },
  "entrance_pupil_position": {
    "type": "array",
    "items": {
      "type": "string",
      "regex": "[0-9]{1,10}/[0-9]{1,10}"
    }
  },
  "f_number": {
    "type": "array",
    "items": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    }
  },
  "fdl_link": {
    "type": "string",
    "pattern": "^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
  },
  "focal_length": {
    "type": "array",
    "items": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    }
  },
  "focal_position": {
    "type": "array",
    "items": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    }
  },
  "iso": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2147483647
  },
  "lens_firmware": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "lens_make": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "lens_model": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "lens_serial_number": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "shutter_angle": {
    "type": "integer",
    "minimum": 1,
    "maximum": 360000
  },
  "t_number": {
    "type": "array",
    "items": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    }
  }
}
```
## Reader coverage

The following table indicates the camera parameters supported by each of the readers.

| Reader      | active_sensor_physical_dimensions | anamorphic_squeeze | camera_firmware | camera_make | camera_model | camera_serial_number | capture_fps | duration | entrance_pupil_position | f_number | fdl_link | focal_length | focal_position | iso | lens_firmware | lens_make | lens_model | lens_serial_number | shutter_angle | t_number |
| ----------- | ----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |----------- |
| RED | + | + | + | + | + | + | + | + | + | | | + | + | + | + | + | + | + | + | + |
| ARRI | + | + | | + | + | + | + | + | | | | + | + | + | | + | + | + | + | + |
| Venice | + | + | + | + | + | + | + | + | | | | + | + | + | | | + | + | + | + |
| Canon | | + | | + | | | | + | | | | + | + | + | | | | | + | + |
