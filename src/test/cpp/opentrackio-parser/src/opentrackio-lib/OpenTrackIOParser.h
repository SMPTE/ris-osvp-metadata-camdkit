// OpenTrackIOParser.h
//
// Reference code for decoding opentrackIO messages
//
// SPDX-License-Identifier: BSD-3-Clause
// Copyright Contributors to the SMTPE RIS OSVP Metadata Project
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

#pragma once

#include <string>

#include <nlohmann/json.hpp>
#include <opentrackio-cpp/OpenTrackIOSample.h>

namespace opentrackio_parser
{
    enum class PositionUnits
    {
        Meters,
        Centimeters,
        Millimeters,
        Inches
    };

    inline std::string toString(const PositionUnits unit)
    {
        switch (unit)
        {
            case PositionUnits::Meters: return "m";
            case PositionUnits::Centimeters: return "cm";
            case PositionUnits::Millimeters: return "mm";
            case PositionUnits::Inches: return "in";
            default:
                assert(false && "Unsupported unit");
                return "Unsupported unit";
        }
    }

    enum class RotationUnits
    {
        Degrees,
        Radians
    };

    inline std::string toString(const RotationUnits unit)
    {
        switch (unit)
        {
            case RotationUnits::Degrees: return "deg";
            case RotationUnits::Radians: return "rad";
            default:
                assert(false && "Unsupported unit");
                return "Unsupported unit";
        }
    }

    enum class SampleTimeFormat
    {
        Seconds,
        Timecode,
        String
    };

    inline std::string toString(const SampleTimeFormat format)
    {
        switch (format)
        {
            case SampleTimeFormat::Seconds: return "sec";
            case SampleTimeFormat::Timecode: return "timecode";
            case SampleTimeFormat::String: return "string";
            default:
                assert(false && "Unsupported format");
                return "Unsupported format";
        }
    }

    struct Transform
    {
        double x = 0.0;
        double y = 0.0;
        double z = 0.0;
    };

    struct Rotation
    {
        double pan = 0.0;
        double tilt = 0.0;
        double roll = 0.0;
    };
}

/**
 * OpenTrackIOSampleParser provides functionality for parsing and extracting data from OpenTrackIO JSON samples.
 *
 * This class handles the parsing, validation and access to OpenTrackIO data, with features including:
 * Unit conversion for position, rotation, and focus distance values.
 * Access to camera transform and rotation data.
 * Access to lens information (focal length, focus distance).
 * Access to timing information (timecode, sample time).
 * Access to camera sensor information.
 *
 * The parser supports customization of output units through dedicated setter methods,
 * allowing consumers to work with their preferred measurement systems.
 */
class OpenTrackIOSampleParser
{
public:
    /** Constructor that initializes the parser with sample data and schema. */
    OpenTrackIOSampleParser(const std::string& sample, const std::string& schema, bool verbose);

    ~OpenTrackIOSampleParser() = default;

    /** Returns whether the sample and schema has successfully been parsed. */
    bool isValid() const { return _isValid; }

    /** Gets camera transform. */
    opentrackio_parser::Transform getCameraTransform() const;

    opentrackio_parser::Rotation getRotation() const;

    /** Gets the slate (shot identification) information. */
    std::string getSlate() const;

    /** Gets the camera timecode as a formatted string. */
    std::string getTimecode() const;

    /** Gets timestamp information, optionally filtered by part (yy, dd, hh, mm, ss, ns). */
    std::string getSampleTime(const std::string& part = "") const;

    /** Gets the camera's active sensor height in pixels. */
    int getSensoryResolutionHeight() const;

    /** Gets the camera's active sensor width in pixels. */
    int getSensorResolutionWidth() const;

    /** Gets the measurement units for sensor dimensions as stated in the schema. */
    std::string getSensorDimensionsUnits();

    /** Gets the tracking device's serial number. */
    std::string getTrackingDeviceSerialNumber() const;

    /** Gets the lens focal length in millimeters. */
    double getPineHoleFocalLength() const;

    /** Gets the lens focus distance in the configured units. */
    double getFocusDistance() const;

    /** Gets the sample frame rate. */
    double getSampleRate() const;

    /** Get the protocol name and version. */
    std::string getProtocol() const;

    /** Set measurement units format for transforms. */
    void setTranslationUnits(opentrackio_parser::PositionUnits unit);

    /** Set rotation units format. */
    void setRotationUnits(opentrackio_parser::RotationUnits unit);

    /** Set sample time format. */
    void setSampleTimeFormat(opentrackio_parser::SampleTimeFormat format);

    /** Set measurement units format for focus distance. */
    void setFocusDistanceUnits(opentrackio_parser::PositionUnits unit);

private:
    bool importSchema();
    bool parse();

    opentrackio::OpenTrackIOSample _sample;
    std::string _sampleStr;
    std::string _schemaStr;

    nlohmann::json _schemaJson;

    bool _isVerbose;
    bool _isValid = false;

    double _transformMultiplier = 1.0;
    double _rotationMultiplier = 1.0;
    double _focusDistanceMultiplier = 1.0;

    std::string _sampleTimeFormat = "sec";
};
