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

Height and width, in microns, of the active area of the camera sensor

#### Sampling

Static

#### Constraints

The height and width shall be each be an integer in the range [0..2,147,483,647].

### `active_sensor_pixel_dimensions`

#### Description

Height and width, in pixels, of the active area of the camera sensor

#### Sampling

Static

#### Constraints

The height and width shall be each be an integer in the range [0..2,147,483,647].

### `duration`

#### Description

Duration of the clip in seconds

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `entrance_pupil_position`

#### Description

Entrance pupil of the lens in millimeters

#### Sampling

Regular

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `focal_length`

#### Description

Focal length of the lens in millimeter

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `focal_position`

#### Description

Focus distance/position of the lens millimeters

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `fps`

#### Description

Capture frame frate of the camera in frames per second (fps)

#### Sampling

Static

#### Constraints

The parameter shall be a rational number whose numerator and denominator are in the range (0..2,147,483,647].

### `iso`

#### Description

Arithmetic ISO scale as defined in ISO 12232

#### Sampling

Static

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `lens_serial_number`

#### Description

Unique identifier of the lens

#### Sampling

Static

#### Constraints

The parameter shall be a Unicode string betwee 0 and 1023 codepoints.

### `t_number`

#### Description

Thousandths of the t-number of the lens

#### Sampling

Regular

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

### `white_balance`

#### Description

White balance of the camera expressed in degrees kelvin.

#### Sampling

Static

#### Constraints

The parameter shall be a integer in the range (0..2,147,483,647].

#### JSON Schema

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
  "active_sensor_pixel_dimensions": {
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
  "fps": {
    "type": "string",
    "regex": "[0-9]{1,10}/[0-9]{1,10}"
  },
  "iso": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2147483647
  },
  "lens_serial_number": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1023
  },
  "t_number": {
    "type": "array",
    "items": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    }
  },
  "white_balance": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2147483647
  }
}
```
