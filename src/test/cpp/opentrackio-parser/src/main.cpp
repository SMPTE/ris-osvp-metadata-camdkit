// main.cpp
//
// Reference code for decoding opentrackIO messages
// Copyright Contributors to the SMTPE RIS OSVP Metadata Project
//
// License: this code is open-source under the FreeBSD License
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

#include "argparse/argparse.hpp"
#include "opentrackio-lib/OpenTrackIOParser.h"


int main(int argc, char* argv[])
{
    argparse::ArgumentParser parser("OpenTrackIOProtocol parser");

    parser.add_argument("-f", "--file")
            .help("OpenTrackIO JSON file to parse.")
            .default_value(std::string());

    parser.add_argument("-s", "--schema")
            .help("The OpenTrackIO schema JSON file.")
            .default_value(std::string());

    parser.add_argument("-v", "--verbose")
            .help("Verbose logging of the parsing process.")
            .default_value(false)
            .implicit_value(true);

    try
    {
        parser.parse_args(argc, argv);
    }
    catch (const std::runtime_error& err)
    {
        std::cerr << err.what() << std::endl;
        std::cerr << parser;
        return 1;
    }

    std::string sampleText;
    std::string schemaText;
    bool verbose = parser.get<bool>("--verbose");

    if (parser.is_used("--schema"))
    {
        if (const auto schemaPath = parser.get<std::string>("--schema");
            std::filesystem::exists(schemaPath))
        {
            if (std::ifstream file(schemaPath);
                file.is_open())
            {
                std::cout << "Reading OpenTrackIO schema file: " << schemaPath << std::endl;
                schemaText.assign(
                    (std::istreambuf_iterator<char>(file)),
                    std::istreambuf_iterator<char>());
                file.close();
            }

            if (!schemaText.empty())
            {
                std::cout << "Successfully read schema." << std::endl;
            }
        }
    }

    if (parser.is_used("--file"))
    {
        if (auto filepath = parser.get<std::string>("--file");
            std::filesystem::exists(filepath))
        {
            if (std::ifstream file(filepath);
                file.is_open())
            {
                std::cout << "Reading OpenTrackIO sample file: " << filepath << std::endl;
                sampleText.assign(
                    (std::istreambuf_iterator<char>(file)),
                    std::istreambuf_iterator<char>());

                file.close();
            }
        }
    }

    OpenTrackIOSampleParser sample(sampleText, schemaText, verbose);
    if (!sample.parse())
    {
        std::cerr << "Failed to parse OpenTrackIO sample." << std::endl;
        return 1;
    }

    sample.importSchema();

    sample.setTranslationUnits(opentrackio_parser::PositionUnits::Millimeters);
    sample.setSampleTimeFormat(opentrackio_parser::SampleTimeFormat::Seconds);
    sample.setFocusDistanceUnits(opentrackio_parser::PositionUnits::Centimeters);
    sample.setRotationUnits(opentrackio_parser::RotationUnits::Degrees);
    std::cout << std::endl;

    std::string protocol = sample.getProtocol();
    std::cout << "Detected protocol: " << protocol << std::endl;

    std::string slate = sample.getSlate();
    std::cout << "On slate: " << slate << std::endl;

    std::string timecode = sample.getTimecode();
    std::cout << "Current camera timecode: " << timecode << std::endl;

    double sampleRate = sample.getSampleRate();
    std::cout << "At a camera frame rate of: " << std::fixed << std::setprecision(5) << sampleRate << std::endl;
    std::cout << std::endl;

    std::cout << "Sample time PTP time is: " << sample.getSampleTime() << " sec" << std::endl;
    sample.setSampleTimeFormat(opentrackio_parser::SampleTimeFormat::Seconds);
    std::cout << "Sample time PTP as a string: " << sample.getSampleTime() << std::endl;
    sample.setSampleTimeFormat(opentrackio_parser::SampleTimeFormat::Timecode);
    std::cout << "Sample time PTP as timecode: " << sample.getSampleTime() << std::endl;
    std::cout << "Sample time PTP elements: " << sample.getSampleTime("yy") << " "
            << sample.getSampleTime("dd") << " "
            << sample.getSampleTime("hh") << " "
            << sample.getSampleTime("mm") << " "
            << sample.getSampleTime("ss") << " "
            << sample.getSampleTime("ns") << std::endl;

    std::cout << std::endl;

    if (std::string serialNumber = sample.getTrackingDeviceSerialNumber();
        !serialNumber.empty())
    {
        std::cout << "Tracking device serial number: " << serialNumber << std::endl;
    }
    else
    {
        std::cout << "Unknown tracking device, wait for static sample to come in..." << std::endl;
    }

    double posX = sample.getTransform("x");
    double posY = sample.getTransform("y");
    double posZ = sample.getTransform("z");
    std::cout << "Camera position is: (" << posX << "," << posY << "," << posZ << ") cm" << std::endl;

    double rotX = sample.getRotation("p");
    double rotY = sample.getRotation("t");
    double rotZ = sample.getRotation("r");
    std::cout << "Camera rotation is: (" << rotX << "," << rotY << "," << rotZ << ") deg" << std::endl;

    sample.setRotationUnits(opentrackio_parser::RotationUnits::Radians);
    rotX = sample.getRotation("p");
    rotY = sample.getRotation("t");
    rotZ = sample.getRotation("r");
    std::cout << "Camera rotation is: (" << std::fixed << std::setprecision(5)
            << rotX << "," << rotY << "," << rotZ << ") radians" << std::endl;
    std::cout << std::endl;

    double fl = sample.getFocalLength();
    if (double height = sample.getSensoryResolutionHeight();
        height != 0)
    {
        double width = sample.getSensorResolutionWidth();
        std::string units = sample.getSensorDimensionsUnits();
        std::cout << "Active camera sensor height: " << height << ", width: " << width << " " << units << std::endl;
    }
    else
    {
        std::cout << "Unknown camera sensor, wait for static sample to come in..." << std::endl;
    }

    std::cout << "Focal length is: " << fl << std::endl;

    double fd = sample.getFocusDistance();
    std::cout << "Focus distance is: " << fd << " cm" << std::endl;

    sample.setFocusDistanceUnits(opentrackio_parser::PositionUnits::Inches);
    fd = sample.getFocusDistance();
    std::cout << "Focus distance is: " << std::fixed << std::setprecision(4) << fd << " in" << std::endl;

    return 0;
}
