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

The height and width shall be each be an integer in the range (0..2,147,483,647].

### `active_sensor_pixel_dimensions`

#### Description

Height and width, in pixels, of the active area of the camera sensor

#### Sampling

Static

#### Constraints

The height and width shall be each be an integer in the range (0..2,147,483,647].

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

