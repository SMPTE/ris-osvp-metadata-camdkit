// OpenTrackIOParser.h
//
// Reference code for decoding opentrackIO messages
//
// SPDX-License-Identifier: BSD-3-Clause
// Copyright Contributors to the SMTPE RIS OSVP Metadata Project
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

// PROBLEMS: 
// return tr["translation"]["z"].get<double>() * trans_mult; 
// std::string hh = std::to_string(pd["timing"]["timecode"]["hours"].get<int>());
// is template necessary? I think I should just cast
// std::tuple<double, double, double> Get_camera_translations() {
// omit tuple or the template?

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
}

// Class to decode and interpret the OpenTrackIO protocol
// msg_text: string containing a single json "sample"
// schema_text: string containing a json schema for the protocol
// verbose: Whether to print extra status during processing
class OpenTrackIOSampleParser
{
public:
    // class constructor
    OpenTrackIOSampleParser(const std::string& sample, const std::string& schema, bool verbose);

    ~OpenTrackIOSampleParser() = default;

    int importSchema(); // Read the schema which governs the interpretation of the protocol

    bool parse(); // Ingest the text and store the JSON items in a dictionary

    double getTransform(const std::string& dimension) const;

    double getRotation(const std::string& dimension) const;

    std::tuple<double, double, double> getCameraTransform() const;

    std::string getTimecode() const; // Return house timecode
    std::string getSampleTime(const std::string& part = "") const; // Time at which this sample was captured

    int getSensoryResolutionHeight() const;

    // If present in this sample, the 'static' block has the active sensor dimensions
    int getSensorResolutionWidth() const;

    // If present in this sample, the 'static' block has the active sensor dimensions
    std::string getSensorDimensionsUnits();

    std::string getTrackingDeviceSerialNumber() const;

    double getFocalLength() const;

    double getFocusDistance() const;

    double getSampleRate() const;

    std::string getProtocol() const;

    void setTranslationUnits(opentrackio_parser::PositionUnits unit); // Set user-preferred units for translations.
    void setRotationUnits(opentrackio_parser::RotationUnits unit); // Set user-preferred units for rotations.
    void setSampleTimeFormat(opentrackio_parser::SampleTimeFormat format); // User preference for time format
    void setFocusDistanceUnits(opentrackio_parser::PositionUnits unit);

    // Establish a user-preference for units of focus distance by storing a conversion factor.
    std::string getSlate() const;

private:
    opentrackio::OpenTrackIOSample _sample;
    std::string _sampleStr;
    std::string _schemaStr;

    nlohmann::json _schemaJson;

    bool _isVerbose;

    double _transformMultiplier = 1.0;
    double _rotationMultiplier = 1.0;
    double _focusDistanceMultiplier = 1.0;

    std::string _sampleTimeFormat = "sec";
};
