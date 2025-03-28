// opentrackIOlib.cpp
//
// Library reference code for decoding opentrackIO messages
//
// SPDX-License-Identifier: BSD-3-Clause
// Copyright Contributors to the SMTPE RIS OSVP Metadata Project
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

#include "opentrackIOlib.h"

#include <iostream>
#include <numbers>

#include "opentrackio-cpp/OpenTrackIOProperties.h"

namespace opentrackio_sample_parser
{
    // Shorthand namespace alias.
    namespace otiop = opentrackio::opentrackioproperties;

    std::string protocolVersionToString(const otiop::Protocol& protocol)
    {
        std::string version;
        constexpr uint8_t versionStringCap = 10; // Arbitrary cap to avoid string resize.
        version.reserve(versionStringCap);

        for (size_t idx = 0; idx < protocol.version.size(); ++idx)
        {
            version.append(std::to_string(protocol.version[idx]));
            if (idx == protocol.version.size())
            {
                continue;
            }

            version.append(".");
        }

        return version;
    }
}

// constructor
OpenTrackIOSampleParser::OpenTrackIOSampleParser(const std::string& msg_text,
                                                 const std::string& schema_text,
                                                 const bool verbose) :
    _sample_str(msg_text),
    _schema_str(schema_text),
    _isVerbose(verbose)
{
}

int OpenTrackIOSampleParser::importSchema()
{
    if (!_schema_str.empty())
    {
        try
        {
            sd = nlohmann::json::parse(_schema_str);
        }
        catch (nlohmann::json::parse_error&)
        {
            std::cout << "Got JSONDecodeError while decoding the sample!" << std::endl;
            sd = nullptr;
        }

        if (sd.is_null())
        {
            std::cout << "Import_schema(): Failed to parse OpenTrackIO schema file." << std::endl;
        }
        else
        {
            std::cout << "Parsed the schema JSON successfully." << std::endl;
            if (_isVerbose)
            {
                std::cout << "Contents of the parsed JSON schema dict:\n" << sd.dump(4) << "\n" << std::endl;
            }
        }
    }
    else
    {
        std::cout << "ERROR: no schema provided!" << std::endl;
        return -1;
    }
    return 0;
}

bool OpenTrackIOSampleParser::parse()
{
    if (_sample_str.empty())
    {
        std::cout << "Parse(): Error. No json text provided!" << std::endl;
        return false;
    }

    std::cout << "Parsing JSON string from sample buffer..." << std::endl;
    if (!_sample.initialise(static_cast<std::string_view>(_sample_str)))
    {
        for (const auto& errors = _sample.getErrors();
             const auto& error : errors)
        {
            std::cout << "Error: " << error << std::endl;
        }

        return false;
    }

    if (_isVerbose)
    {
        for (const auto& warnings = _sample.getWarnings();
             const auto& warning : warnings)
        {
            std::cout << "Warning: " << warning << std::endl;
        }

        const auto json = _sample.getJson();
        std::cout << "Contents of the parsed JSON dict:\n" << json.dump(4) << "\n" << std::endl;
    }

    return true;
}

double Conversion_factor_from_meters(const std::string& unit_str)
{
    if (unit_str == "m")
    {
        return 1.0;
    }

    if (unit_str == "cm")
    {
        return 100.0;
    }

    if (unit_str == "mm")
    {
        return 1000.0;
    }

    if (unit_str == "in")
    {
        return (1000.0 / 25.4);
    }

    return 0.0;
}

double OpenTrackIOSampleParser::getTransform(const std::string& dimension) const
{
    for (const auto& transform : _sample.transforms->transforms)
    {
        if (transform.id == "Camera")
        {
            if (_isVerbose)
            {
                std::cout << "found camera, dim = " << dimension << ", mult factor: " << _trans_mult << std::endl;
            }

            if (dimension == "x")
            {
                return transform.translation.x * _trans_mult;
            }

            if (dimension == "y")
            {
                return transform.translation.y * _trans_mult;
            }

            if (dimension == "z")
            {
                return transform.translation.z * _trans_mult;
            }

            break; // todo: this isn't needed?
        }
    }
    return 0.0;
}

double OpenTrackIOSampleParser::getRotation(const std::string& dimension) const
{
    for (auto transform : _sample.transforms->transforms)
    {
        if (transform.id == "Camera")
        {
            if (dimension == "p")
            {
                return transform.rotation.pan * _rot_mult;
            }

            if (dimension == "t")
            {
                return transform.rotation.tilt * _rot_mult;
            }

            if (dimension == "r")
            {
                return transform.rotation.roll * _rot_mult;
            }

            break; // todo: this isn't needed.?
        }
    }

    return 0.0;
}

std::tuple<double, double, double> OpenTrackIOSampleParser::getCameraTransform() const
{
    return std::make_tuple(getTransform("x"), getTransform("y"), getTransform("z"));
}

std::string OpenTrackIOSampleParser::getTimecode() const
{
    if (!_sample.timing.has_value() || !_sample.timing->timecode.has_value())
    {
        return "";
    }

    return std::to_string(_sample.timing->timecode->hours) + ":" +
           std::to_string(_sample.timing->timecode->minutes) + ":" +
           std::to_string(_sample.timing->timecode->seconds) + ":" +
           std::to_string(_sample.timing->timecode->frames);
}

std::string OpenTrackIOSampleParser::getSampleTime(const std::string& part) const
{
    const int seconds = _sample.timing->sampleTimestamp->seconds;
    const int nano_seconds = _sample.timing->sampleTimestamp->nanoseconds;
    // Constants
    constexpr int epoch = 1970; // PTP is since this epoch
    constexpr int spm = 60; // seconds per minute. Common knowledge, but consistency is important
    constexpr int sph = 3600; // seconds per hour
    constexpr int spd = 86400; // sec per day
    constexpr int spy = 31536000; // sec per year

    // separate into years, days, hours, min, sec
    const int y_delta = seconds / spy; // years since epoch
    const int yr = epoch + y_delta; // current year
    const int sty = seconds - y_delta * spy; // seconds elapsed this year
    const int day = sty / spd; // current day of year
    const int std = sty - day * spd; // seconds elapsed today (since midnight)
    const int hr = std / sph; // hours elapsed today
    const int mn = (std - hr * sph) / spm; // remainder minutes
    const int st = std - hr * sph - mn * spm; // remainder seconds

    if (part.empty())
    {
        if (_sample_time_format == "sec")
        {
            return std::to_string(seconds + (nano_seconds * 0.000000001));
        }

        if (_sample_time_format == "timecode")
        {
            const int frm = static_cast<int>(nano_seconds * 0.000000001 * getTimecodeFormat());
            return std::to_string(hr) + ":" + std::to_string(mn) + ":" + std::to_string(st) + ":" + std::to_string(frm);
        }

        if (_sample_time_format == "string")
        {
            return "year:" + std::to_string(yr) + " day:" + std::to_string(day) + " hour:" + std::to_string(hr) +
                   " min:" + std::to_string(mn) + " sec:" + std::to_string(st) + " nsec:" +
                   std::to_string(nano_seconds);
        }
    }
    else
    {
        if (part == "yy")
            return std::to_string(yr);
        if (part == "dd")
            return std::to_string(day);
        if (part == "hh")
            return std::to_string(hr);
        if (part == "mm")
            return std::to_string(mn);
        if (part == "ss")
            return std::to_string(st);
        if (part == "ns")
            return std::to_string(nano_seconds);
    }
    return "";
}

double OpenTrackIOSampleParser::getTimecodeFormat() const
{
    if (!_sample.timing.has_value() || !_sample.timing->timecode.has_value())
    {
        return 0.0;
    }

    return 0.0;

    // todo - update this.
    // return _sample.timing->timecode->format.frameRate.numerator /
    // _sample.timing->timecode->format.frameRate.denominator;
}

// Set user-preferred units for translations.
// Valid args: "m", "cm", "mm", "in"
void OpenTrackIOSampleParser::setTranslationUnits(const std::string& unit_str)
{
    const std::string& schema_units = sd["properties"]["transforms"]["items"]["properties"]["translation"]["units"];
    if (_isVerbose)
    {
        std::cout << "Schema says camera translation units are: " << schema_units << std::endl;
        std::cout << "Setting preferred translation units to: " << unit_str << std::endl;
    }
    if (schema_units == "meter") // todo: this isn't supporting other units, make enum!
    {
        _trans_mult = Conversion_factor_from_meters(unit_str);
    }
}

// Set user-preferred units for rotations.
// Valid args: "deg", "rad"
void OpenTrackIOSampleParser::setRotationUnits(const std::string& unit_str)
{
    const std::string& schema_units = sd["properties"]["transforms"]["items"]["properties"]["rotation"]["units"];
    if (_isVerbose)
    {
        std::cout << "Schema says camera rotation units are: " << schema_units << std::endl;
        std::cout << "Setting preferred camera rotation units to: " << unit_str << std::endl;
    }

    if (schema_units == "degree")
    {
        if (unit_str == "deg")
        {
            _rot_mult = 1.0;
        }
        else if (unit_str == "rad")
        {
            _rot_mult = std::numbers::pi_v<float> / 180.f;
        }
    }
}

// User preference for time format
// Valid args: "sec", "timecode", "string"
void OpenTrackIOSampleParser::setSampleTimeFormat(const std::string& format_str)
{
    if (_isVerbose)
    {
        const std::string& schema_units = sd["properties"]["timing"]["properties"]["sampleTimestamp"]["units"];
        std::cout << "Schema says sample time units are: " << schema_units << std::endl;
        std::cout << "Setting preferred sample time format to: " << format_str << std::endl;
    }
    if (std::ranges::find(_sample_time_formats, format_str) != _sample_time_formats.end())
    {
        _sample_time_format = format_str;
    }
}

// Establish a user-preference for units of focus distance by storing a conversion factor.
// Valid: "m","cm","mm","in"
void OpenTrackIOSampleParser::setFocusDistanceUnits(const std::string& unit_str)
{
    const std::string& schema_units = sd["properties"]["lens"]["properties"]["focusDistance"]["units"];
    if (_isVerbose)
    {
        std::cout << "Schema says focus distance units are: " << schema_units << std::endl;
        std::cout << "Setting preferred focus distance units to: " << unit_str << std::endl;
    }

    if (schema_units == "millimeter")
    {
        if (unit_str == "m")
        {
            _focus_dist_mult = 0.001;
        }
        else if (unit_str == "cm")
        {
            _focus_dist_mult = 0.1;
        }
        else if (unit_str == "mm")
        {
            _focus_dist_mult = 1.0;
        }
        else if (unit_str == "in")
        {
            _focus_dist_mult = 1.0 / 25.4;
        }
    }
}

// The protocol to which this sample conforms
std::string OpenTrackIOSampleParser::getProtocol() const
{
    return _sample.protocol->name + " v" + opentrackio_sample_parser::protocolVersionToString(_sample.protocol.value());
}

std::string OpenTrackIOSampleParser::setSlate() const
{
    if (_sample.tracker->slate)
    {
        return *_sample.tracker->slate;
    }
    return "";
}

// If present in this sample, the 'static' block has the active sensor dimensions
int OpenTrackIOSampleParser::getSensoryResolutionHeight() const
{
    return _sample.camera->activeSensorResolution->height;
}

// If present in this sample, the 'static' block has the active sensor dimensions
int OpenTrackIOSampleParser::getSensorResolutionWidth() const
{
    return _sample.camera->activeSensorResolution->width;
}

std::string OpenTrackIOSampleParser::getSensorDimensionsUnits()
{
    if (sd["properties"]["camera"].contains("activeSensorPhysicalDimensions"))
    {
        return sd["properties"]["camera"]["activeSensorPhysicalDimensions"]["units"].get<std::string>();
    }

    return "";
}

std::string OpenTrackIOSampleParser::getTrackingDeviceSerialNumber() const
{
    if (!_sample.tracker->serialNumber.has_value())
    {
        return "";
    }

    return _sample.tracker->serialNumber.value();
}

double OpenTrackIOSampleParser::getFocalLength() const
{
    // todo - update this.
    // if (_sample.lens->focalLength)
    // {
    //     return *_sample.lens->focalLength;
    // }

    return 0.0;
}

double OpenTrackIOSampleParser::getFocusDistance() const
{
    if (_sample.lens->focusDistance)
    {
        return *_sample.lens->focusDistance * _focus_dist_mult;
    }

    return 0.0;
}
