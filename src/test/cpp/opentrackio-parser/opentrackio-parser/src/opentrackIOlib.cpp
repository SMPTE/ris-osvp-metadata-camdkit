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
#include <unordered_map>
#include <cmath>

#include <opentrackio-cpp/OpenTrackIOSample.h>
#include <nlohmann/json.hpp>

// constructor
void OTProtocol::Init(std::string msg_text, std::string schema_text, bool verbose){
    sample_str = msg_text; 
    schema_str = schema_text; 
    this->verbose = verbose; 
    trans_mult = 1.0; 
    rot_mult = 1.0; 
    sample_time_format = "sec"; 
    focus_dist_mult = 1.0;
 }
      
// Read the schema which governs the interpretation of the protocol
int OTProtocol::Import_schema(void) {
    if (!schema_str.empty()) {
        try {
            sd = nlohmann::json::parse(schema_str);
        } catch (nlohmann::json::parse_error&) {
            std::cout << "Got JSONDecodeError while decoding the sample!" << std::endl;
            sd = nullptr;
        }
        if (sd.is_null()) {
            std::cout << "Import_schema(): Failed to parse OpenTrackIO schema file." << std::endl;
        } else {
            std::cout << "Parsed the schema JSON successfully." << std::endl;
            if (verbose) {
                std::cout << "Contents of the parsed JSON schema dict:\n" << sd.dump(4) << "\n" << std::endl;
            }
        }
    } else {
        std::cout << "ERROR: no schema provided!" << std::endl;
        return -1;
    }
    return 0;
}

// Ingest the text and store the JSON items in a dictionary
int OTProtocol::Parse(void) {
    if (!sample_str.empty()) {
        std::cout << "Parsing JSON string from sample buffer..." << std::endl;
        if (!sample.initialise((std::string_view)sample_str)) {
            auto errors = sample.getErrors();
            for (auto error : errors) {
                std::cout << "Error: " << error << std::endl;
            }
            exit(-1);
        }
        if (verbose) {
            auto warnings = sample.getWarnings();
            for (auto warning : warnings) {
                std::cout << "Warning: " << warning << std::endl;
            }
            auto json = sample.getJson();
            std::cout << "Contents of the parsed JSON dict:\n" << json.dump(4) << "\n" << std::endl;
        }
    } else {
        std::cout << "Parse(): Error. No json text provided!" << std::endl;
        return -1;
    }
    return 0;
}

double Conversion_factor_from_meters(const std::string& unit_str) {
    if (unit_str == "m") {
        return 1.0;
    } else if (unit_str == "cm") {
        return 100.0;
    } else if (unit_str == "mm") {
        return 1000.0;
    } else if (unit_str == "in") {
        return (1000.0 / 25.4);
    }
    return 0.0;
}

double OTProtocol::Get_camera_trans(const std::string& dimension) {
    for (auto transform : sample.transforms->transforms) {
        if (transform.id == "Camera") {
            if (verbose) {
                std::cout << "found camera, dim = " << dimension << ", mult factor: " << trans_mult << std::endl;
            }
            if (dimension == "x") {
                return transform.translation.x * trans_mult;
            } else if (dimension == "y") {
                return transform.translation.y * trans_mult;
            } else if (dimension == "z") {
                return transform.translation.z * trans_mult;
            }
            break;
        }
    }
    return 0.0;
}

double OTProtocol::Get_camera_rot(const std::string& dimension) {
    for (auto transform : sample.transforms->transforms) {
        if (transform.id == "Camera") {
            if (dimension == "p") {
                return transform.rotation.pan * rot_mult;
            } else if (dimension == "t") {
                return transform.rotation.tilt * rot_mult;
            } else if (dimension == "r") {
                return transform.rotation.roll * rot_mult;
            }
            break;
        }
    }
    return 0.0;
}

// Return order: x,y,z
std::tuple<double, double, double> OTProtocol::Get_camera_translations(void) {
    return std::make_tuple(Get_camera_trans("x"), Get_camera_trans("y"), Get_camera_trans("z"));
}

// Return house timecode
std::string OTProtocol::Get_timecode(void) {
    std::string hh = std::to_string(sample.timing->timecode->hours);
    std::string mm = std::to_string(sample.timing->timecode->minutes);
    std::string ss = std::to_string(sample.timing->timecode->seconds);
    std::string ff = std::to_string(sample.timing->timecode->frames);
    return hh + ":" + mm + ":" + ss + ":" + ff;
}

// Get the PTP sample time
std::string OTProtocol::Get_sample_time(const std::string& part) {
    int ssec = sample.timing->sampleTimestamp->seconds;
    int nsec = sample.timing->sampleTimestamp->nanoseconds;
    // Constants
    const int epoch = 1970; // PTP is since this epoch
    const int spm = 60;     // seconds per minute. Common knowledge, but consistency is important
    const int sph = 3600;   // seconds per hour
    const int spd = 86400;  // sec per day
    const int spy = 31536000;   // sec per year
    // separate into years, days, hours, min, sec
    int ydelta = ssec / spy;            // years since epoch
    int yr = epoch + ydelta;            // current year
    int sty = ssec - (ydelta * spy);    // seconds elapsed this year
    int day = sty / spd;                // current day of year
    int std = sty - (day * spd);        // seconds elapsed today (since midnight)
    int hr = std / sph;                 // hours elapsed today
    int mn = (std - (hr * sph)) / spm;  // remainder minutes
    int st = std - (hr * sph) - (mn * spm); // remainder seconds

    if (part.empty()) {
        if (sample_time_format == "sec") {
            return std::to_string(ssec + (nsec * 0.000000001));
        } else if (sample_time_format == "timecode") {
            int frm = static_cast<int>((nsec * 0.000000001) * Get_timecode_framerate());
            return std::to_string(hr) + ":" + std::to_string(mn) + ":" + std::to_string(st) + ":" + std::to_string(frm);
        } else if (sample_time_format == "string") {
            return "year:" + std::to_string(yr) + " day:" + std::to_string(day) + " hour:" + std::to_string(hr) + 
                   " min:" + std::to_string(mn) + " sec:" + std::to_string(st) + " nsec:" + std::to_string(nsec);
        }
    } else {
        if (part == "yy") 
            return std::to_string(yr);
        else if (part == "dd") 
            return std::to_string(day);
        else if (part == "hh") 
            return std::to_string(hr);
        else if (part == "mm") 
            return std::to_string(mn);
        else if (part == "ss") 
            return std::to_string(st);
        else if (part == "ns") 
            return std::to_string(nsec);
    }
    return "";
}

// Frame rate which this timecode represents
double OTProtocol::Get_timecode_framerate(void) {
    double numerator = sample.timing->timecode->format.frameRate.numerator;
    double denominator = sample.timing->timecode->format.frameRate.denominator;
    return numerator / denominator;
}

// Set user-preferred units for translations. 
// Valid args: "m", "cm", "mm", "in"
void OTProtocol::Set_trans_units(const std::string& unit_str) {
    std::string schema_units = sd["properties"]["transforms"]["items"]["properties"]["translation"]["units"];
    if (verbose) {
        std::cout << "Schema says camera translation units are: " << schema_units << std::endl;
        std::cout << "Setting preferred translation units to: " << unit_str << std::endl;
    }
    if (schema_units == "meter") {
        trans_mult = Conversion_factor_from_meters(unit_str);
    }
}

// Set user-preferred units for rotations. 
// Valid args: "deg", "rad"
void OTProtocol::Set_rotation_units(const std::string& unit_str) {
    std::string schema_units = sd["properties"]["transforms"]["items"]["properties"]["rotation"]["units"];
    if (verbose) {
        std::cout << "Schema says camera rotation units are: " << schema_units << std::endl;
        std::cout << "Setting preferred camera rotation units to: " << unit_str << std::endl;
    }
    if (schema_units == "degree") {
        if (unit_str == "deg") {
            rot_mult = 1.0;
        } else if (unit_str == "rad") {
            rot_mult = M_PI / 180;
        }
    }
}

// User preference for time format
// Valid args: "sec", "timecode", "string"
void OTProtocol::Set_sample_time_format(const std::string& format_str) {
    if (verbose) {
        std::string schema_units = sd["properties"]["timing"]["properties"]["sampleTimestamp"]["units"];
        std::cout << "Schema says sample time units are: " << schema_units << std::endl;
        std::cout << "Setting preferred sample time format to: " << format_str << std::endl;
    }
    if (std::find(sample_time_formats.begin(), sample_time_formats.end(), format_str) != sample_time_formats.end()) {
        sample_time_format = format_str;
    }
}

// Establish a user-preference for units of focus distance by storing a conversion factor.
// Valid: "m","cm","mm","in"
void OTProtocol::Set_focus_distance_units(const std::string& unit_str) {
    std::string schema_units = sd["properties"]["lens"]["properties"]["focusDistance"]["units"];
    if (verbose) {
        std::cout << "Schema says focus distance units are: " << schema_units << std::endl;
        std::cout << "Setting preferred focus distance units to: " << unit_str << std::endl;
    }
    if (schema_units == "millimeter") {
        if (unit_str == "m") {
            focus_dist_mult = 0.001;
        } else if (unit_str == "cm") {
            focus_dist_mult = 0.1;
        } else if (unit_str == "mm") {
            focus_dist_mult = 1.0;
        } else if (unit_str == "in") {
            focus_dist_mult = 1.0 / 25.4;
        }
    }
}

// The protocol to which this sample conforms
std::string OTProtocol::Get_protocol() {
    return sample.protocol->name + " v" + sample.protocol->version;
}

std::string OTProtocol::Get_slate(void) {
    if (sample.tracker->slate) {
        return *sample.tracker->slate;
    }
    return "";
}

// If present in this sample, the 'static' block has the active sensor dimensions
int OTProtocol::Get_sensor_dim_height(void) {
    if (sample.camera->activeSensorResolution->height) {
        return sample.camera->activeSensorResolution->height;
    }
    return 0;
}

// If present in this sample, the 'static' block has the active sensor dimensions
int OTProtocol::Get_sensor_dim_width(void) {
    if (sample.camera->activeSensorResolution->width) {
        return sample.camera->activeSensorResolution->width;
    }
    return 0;
}

std::string OTProtocol::Get_sensor_dim_units(void) {
    if (sd["properties"]["camera"].contains("activeSensorPhysicalDimensions")) {
        return sd["properties"]["camera"]["activeSensorPhysicalDimensions"]["units"].get<std::string>();
    }
    return "";
}

std::string OTProtocol::Get_tracking_device_serial_number(void) {
    if (sample.tracker->serialNumber) {
        return *sample.tracker->serialNumber;
    }
    return "";
}

double OTProtocol::Get_focal_length(void) {
    if (sample.lens->focalLength) {
        return *sample.lens->focalLength;
    }
    return 0.0;
}

double OTProtocol::Get_focus_distance(void) {
    if (sample.lens->focusDistance) {
        return *sample.lens->focusDistance * focus_dist_mult;
    }
    return 0.0;
}
