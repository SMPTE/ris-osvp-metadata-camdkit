// opentrackIOlib.h
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

// Class to decode and interpret the OpenTrackIO protocol
// msg_text: string containing a single json "sample"
// schema_text: string containing a json schema for the protocol
// verbose: Whether to print extra status during processing
class OpenTrackIOSampleParser
{
public:
    // class constructor
    OpenTrackIOSampleParser(const std::string& msg_text, const std::string& schema_text, bool verbose);
    ~OpenTrackIOSampleParser() = default;

    int importSchema(); // Read the schema which governs the interpretation of the protocol

    bool parse(); // Ingest the text and store the JSON items in a dictionary

    // TODO: change the guts of these.
    double getTransform(const std::string& dimension) const;
    double getRotation(const std::string& dimension) const;

    std::tuple<double, double, double> getCameraTransform() const; // todo: bum tuples.

    std::string getTimecode() const; // Return house timecode
    std::string getSampleTime(const std::string& part = "") const; // Time at which this sample was captured
    double getTimecodeFormat() const; // Frame rate which this timecode represents

    int getSensoryResolutionHeight() const; // If present in this sample, the 'static' block has the active sensor dimensions
    int getSensorResolutionWidth() const; // If present in this sample, the 'static' block has the active sensor dimensions
    std::string getSensorDimensionsUnits();

    std::string getTrackingDeviceSerialNumber() const;

    double getFocalLength() const;

    double getFocusDistance() const;

    std::string getProtocol() const;

    void setTranslationUnits(const std::string& unit_str); // Set user-preferred units for translations.
    void setRotationUnits(const std::string& unit_str); // Set user-preferred units for rotations.
    void setSampleTimeFormat(const std::string& format_str); // User preference for time format
    void setFocusDistanceUnits(const std::string& unit_str);

    // Establish a user-preference for units of focus distance by storing a conversion factor.
    std::string setSlate() const;

private:
    opentrackio::OpenTrackIOSample _sample;
    std::string _sample_str;
    std::string _schema_str;

    nlohmann::json sd;

    bool _isVerbose;

    double _trans_mult = 1.0;
    double _rot_mult = 1.0;
    double _focus_dist_mult = 1.0;

    std::string _sample_time_format = "sec"; // TODO: Maybe make an enum.

    std::vector<std::string> _sample_time_formats = {"sec", "timecode", "string"}; // todo: check this out.
};
