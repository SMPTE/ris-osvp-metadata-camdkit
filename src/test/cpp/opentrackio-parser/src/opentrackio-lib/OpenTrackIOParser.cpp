// OpenTrackIOParser.cpp
//
// Library reference code for decoding opentrackIO messages
//
// SPDX-License-Identifier: BSD-3-Clause
// Copyright Contributors to the SMTPE RIS OSVP Metadata Project
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

#include "OpenTrackIOParser.h"

#include <iostream>
#include <numbers>

#include "opentrackio-cpp/OpenTrackIOProperties.h"

namespace opentrackio_parser
{
    // Shorthand namespace alias.
    namespace otiop = opentrackio::opentrackioproperties;

    std::string toString(const otiop::Protocol& protocol)
    {
        std::string version;
        for (size_t idx = 0; idx < protocol.version.size(); ++idx)
        {
            version.append(std::to_string(protocol.version[idx]));
            if (idx == protocol.version.size() - 1)
            {
                break;
            }

            version.append(".");
        }

        return version;
    }

    double ConvertFactorFromMeters(const PositionUnits unit)
    {
        switch (unit)
        {
            case PositionUnits::Meters: return 1.0;
            case PositionUnits::Centimeters: return 100.0;
            case PositionUnits::Millimeters: return 1000.0;
            case PositionUnits::Inches: return (1000.0 / 25.4);
            default: return 0.0;
        }
    }
}

OpenTrackIOSampleParser::OpenTrackIOSampleParser(const std::string& sample,
                                                 const std::string& schema,
                                                 const bool verbose) : _sampleStr(sample),
                                                                       _schemaStr(schema),
                                                                       _isVerbose(verbose)
{
    _isValid = parse();
    _isValid &= importSchema();
}

bool OpenTrackIOSampleParser::importSchema()
{
    if (_schemaStr.empty())
    {
        std::cout << "ERROR: no schema provided!" << std::endl;
        return false;
    }

    try
    {
        _schemaJson = nlohmann::json::parse(_schemaStr);
    }
    catch (nlohmann::json::parse_error&)
    {
        std::cerr << "Got JSONDecodeError while decoding the sample!" << std::endl;
        _schemaJson = nullptr;
    }

    if (_schemaJson.is_null())
    {
        std::cerr << "Import_schema(): Failed to parse OpenTrackIO schema file." << std::endl;
        return false;
    }

    std::cout << "Parsed the schema JSON successfully." << std::endl;
    if (_isVerbose)
    {
        std::cout << "Contents of the parsed JSON schema dict:\n" << _schemaJson.dump(4) << "\n" << std::endl;
    }

    return true;
}

bool OpenTrackIOSampleParser::parse()
{
    if (_sampleStr.empty())
    {
        std::cout << "Parse(): Error. No json text provided!" << std::endl;
        return false;
    }

    std::cout << "Parsing JSON string from sample buffer..." << std::endl;
    if (!_sample.initialise(static_cast<std::string_view>(_sampleStr)))
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

opentrackio_parser::Transform OpenTrackIOSampleParser::getCameraTransform() const
{
    if (!_sample.transforms.has_value())
    {
        return {};
    }

    for (const auto& transform : _sample.transforms->transforms)
    {
        if (transform.id == "Camera")
        {
            return {
                transform.translation.x * _transformMultiplier,
                transform.translation.y * _transformMultiplier,
                transform.translation.z * _transformMultiplier
            };
        }
    }

    return {};
}

opentrackio_parser::Rotation OpenTrackIOSampleParser::getRotation() const
{
    if (!_sample.transforms.has_value())
    {
        return {};
    }

    for (const auto& transform : _sample.transforms->transforms)
    {
        if (transform.id == "Camera")
        {
            return {
                transform.rotation.pan * _rotationMultiplier,
                transform.rotation.tilt * _rotationMultiplier,
                transform.rotation.roll * _rotationMultiplier
            };
        }
    }

    return {};
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
    if (!_sample.timing.has_value() || !_sample.timing->sampleTimestamp.has_value())
    {
        return "";
    }

    const uint64_t seconds = _sample.timing->sampleTimestamp->seconds;
    const uint32_t nano_seconds = _sample.timing->sampleTimestamp->nanoseconds;

    constexpr int epoch = 1'970; // PTP is since this epoch
    constexpr int secondsPerMinute = 60;
    constexpr int secondsPerHour = 3'600; // seconds per hour
    constexpr int secondsPerDay = 86'400; // sec per day
    constexpr uint64_t secondsPerYear = 31'536'000; // sec per year

    // separate into years, days, hours, min, sec
    const double y_delta = static_cast<double>(seconds) / secondsPerYear; // years since epoch
    const uint32_t yr = std::floor(epoch + y_delta); // current year
    const uint32_t sty = seconds - std::floor(y_delta) * secondsPerYear; // seconds elapsed this year
    const uint32_t day = std::floor(sty / secondsPerDay); // current day of year
    const uint32_t std = sty - day * secondsPerDay; // seconds elapsed today (since midnight)
    const uint32_t hr = std::floor(std / secondsPerHour); // hours elapsed today
    const uint32_t mn = std::floor((std - hr * secondsPerHour) / secondsPerMinute); // remainder minutes
    const uint32_t st = std - hr * secondsPerHour - mn * secondsPerMinute; // remainder seconds

    if (part.empty())
    {
        constexpr double formattingCoefficient = 0.000000001;
        if (_sampleTimeFormat == "sec")
        {
            return std::to_string(seconds + nano_seconds * formattingCoefficient);
        }

        if (_sampleTimeFormat == "timecode")
        {
            const int frm = static_cast<int>(nano_seconds * formattingCoefficient * getSampleRate());
            return std::to_string(hr) + ":" + std::to_string(mn) + ":" + std::to_string(st) + ":" + std::to_string(frm);
        }

        if (_sampleTimeFormat == "string")
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

double OpenTrackIOSampleParser::getSampleRate() const
{
    return _sample.timing->sampleRate->numerator /
           _sample.timing->sampleRate->denominator;
}

void OpenTrackIOSampleParser::setTranslationUnits(const opentrackio_parser::PositionUnits unit)
{
    const std::string& schema_units = _schemaJson["properties"]["transforms"]["items"]["properties"]["translation"]
            ["units"];

    if (_isVerbose)
    {
        std::cout << "Schema says camera translation units are: " << schema_units << std::endl;
        std::cout << "Setting preferred translation units to: " << toString(unit) << std::endl;
    }

    if (schema_units == "meter")
    {
        _transformMultiplier = ConvertFactorFromMeters(unit);
    }
}

void OpenTrackIOSampleParser::setRotationUnits(const opentrackio_parser::RotationUnits unit)
{
    const std::string& schemaUnit = _schemaJson["properties"]["transforms"]["items"]["properties"]["rotation"]
            ["units"];

    if (_isVerbose)
    {
        std::cout << "Schema says camera rotation units are: " << schemaUnit << std::endl;
        std::cout << "Setting preferred camera rotation units to: " << toString(unit) << std::endl;
    }

    if (constexpr auto expectedSchemaUnit = "degree";
        schemaUnit == expectedSchemaUnit)
    {
        switch (unit)
        {
            case opentrackio_parser::RotationUnits::Degrees: _rotationMultiplier = 1.0;
                break;
            case opentrackio_parser::RotationUnits::Radians: _rotationMultiplier = std::numbers::pi_v<float> / 180.f;
                break;
            default:
                assert(false && "Invalid unit for rotation");
                break;
        }

        return;
    }

    assert(false && "Invalid schema unit, expectedSchemaUnit may need updating.");
}

void OpenTrackIOSampleParser::setSampleTimeFormat(const opentrackio_parser::SampleTimeFormat format)
{
    if (_isVerbose)
    {
        const std::string& schema_units = _schemaJson["properties"]["timing"]["properties"]["sampleTimestamp"]
                ["units"];

        std::cout << "Schema says sample time units are: " << schema_units << std::endl;
        std::cout << "Setting preferred sample time format to: " << toString(format) << std::endl;
    }

    _sampleTimeFormat = toString(format);
}

void OpenTrackIOSampleParser::setFocusDistanceUnits(const opentrackio_parser::PositionUnits unit)
{
    const std::string& schemaUnit = _schemaJson["properties"]["lens"]["properties"]["focusDistance"]["units"];

    if (_isVerbose)
    {
        std::cout << "Schema says focus distance units are: " << schemaUnit << std::endl;
        std::cout << "Setting preferred focus distance units to: " << toString(unit) << std::endl;
    }

    if (constexpr auto expectedSchemaUnit = "meter";
        schemaUnit == expectedSchemaUnit)
    {
        switch (unit)
        {
            case opentrackio_parser::PositionUnits::Meters: _focusDistanceMultiplier = 0.001;
                break;
            case opentrackio_parser::PositionUnits::Centimeters: _focusDistanceMultiplier = 0.1;
                break;
            case opentrackio_parser::PositionUnits::Millimeters: _focusDistanceMultiplier = 1.0;
                break;
            case opentrackio_parser::PositionUnits::Inches: _focusDistanceMultiplier = 1.0 / 25.4;
                break;
            default:
                assert(false && "Invalid unit for focus distance");
                break;
        }

        return; // Successfully set the focus distance unit
    }

    assert(false && "Invalid schema unit, expectedSchemaUnit may need updating.");
}

std::string OpenTrackIOSampleParser::getProtocol() const
{
    if (_sample.protocol.has_value())
    {
        return _sample.protocol->name + " v" + opentrackio_parser::toString(_sample.protocol.value());
    }

    return "";
}

std::string OpenTrackIOSampleParser::getSlate() const
{
    if (_sample.tracker.has_value() && _sample.tracker->slate.has_value())
    {
        return _sample.tracker->slate.value();
    }

    return "";
}

int OpenTrackIOSampleParser::getSensoryResolutionHeight() const
{
    if (_sample.camera.has_value() && _sample.camera->activeSensorResolution.has_value())
    {
        return _sample.camera->activeSensorResolution->height;
    }

    return 0;
}

int OpenTrackIOSampleParser::getSensorResolutionWidth() const
{
    if (_sample.camera.has_value() && _sample.camera->activeSensorResolution.has_value())
    {
        return _sample.camera->activeSensorResolution->width;
    }

    return 0.0;
}

std::string OpenTrackIOSampleParser::getSensorDimensionsUnits()
{
    if (_schemaJson["properties"]["camera"].contains("activeSensorPhysicalDimensions"))
    {
        return _schemaJson["properties"]["camera"]["activeSensorPhysicalDimensions"]["units"].get<std::string>();
    }

    return "";
}

std::string OpenTrackIOSampleParser::getTrackingDeviceSerialNumber() const
{
    if (_sample.tracker.has_value() && _sample.tracker->serialNumber.has_value())
    {
        return _sample.tracker->serialNumber.value();
    }

    return "";
}

double OpenTrackIOSampleParser::getPineHoleFocalLength() const
{
    if (_sample.lens.has_value() &&
        _sample.lens->pinholeFocalLength.has_value() &&
        _sample.lens->pinholeFocalLength.has_value())
    {
        return _sample.lens->pinholeFocalLength.value();
    }

    return 0.0;
}

double OpenTrackIOSampleParser::getFocusDistance() const
{
    if (_sample.lens.has_value() && _sample.lens->focusDistance.has_value())
    {
        return *_sample.lens->focusDistance * _focusDistanceMultiplier;
    }

    return 0.0;
}
