// opentrackIOlib.h
//
// Reference code for decoding opentrackIO messages
// Copyright (c) 2024 Steve Rosenbluth, RiS OSVP camera tracking committee
//
// License: this code is open-source under the FreeBSD License
//
// nlohmann JSON library licensed under the MIT License, Copyright (c) 2013-2022 Niels Lohmann

// PROBLEMS: 
// return tr["translation"]["z"].get<double>() * trans_mult; 
// std::string hh = std::to_string(pd["timing"]["timecode"]["hours"].get<int>());
// is template necessary? I think I should just cast
// std::tuple<double, double, double> Get_camera_translations() {
// omit tuple or the template?

#ifndef OPENTRACKIO_H
#define OPENTRACKIO_H

#include <string>
#include <vector>

#include <nlohmann/json.hpp>
#include <opentrackio-cpp/OpenTrackIOSample.h>

// Class to decode and interpret the OpenTrackIO protocol
// msg_text: string containing a single json "sample"
// schema_text: string containing a json schema for the protocol
// verbose: Whether to print extra status during processing
class OTProtocol {

public:
    // class constructor
    OTProtocol(std::string msg_text = "", std::string schema_text = "", bool verbose = false)
        { Init(msg_text,schema_text,verbose); }
 
    void Init(std::string msg_text, std::string schema_text, bool verbose); // Initailize objects
    int Import_schema(void);                                            // Read the schema which governs the interpretation of the protocol
    int Parse(void);                                                    // Ingest the text and store the JSON items in a dictionary
    double Get_camera_trans(const std::string& dimension);
    double Get_camera_rot(const std::string& dimension);
    std::tuple<double, double, double> Get_camera_translations(void);   // Return order: x,y,z
    std::string Get_timecode(void);                                     // Return house timecode
    std::string Get_sample_time(const std::string& part = "");          // Time at which this sample was captured
    double Get_timecode_framerate(void);                                // Frame rate which this timecode represents
    void Set_trans_units(const std::string& unit_str);                  // Set user-preferred units for translations. 
    void Set_rotation_units(const std::string& unit_str);               // Set user-preferred units for rotations. 
    void Set_sample_time_format(const std::string& format_str);         // User preference for time format
    void Set_focus_distance_units(const std::string& unit_str);         // Establish a user-preference for units of focus distance by storing a conversion factor.
    std::string Get_protocol(void);                                     // The protocol to which this sample conforms
    std::string Get_slate(void);
    int Get_sensor_dim_height(void);                                    // If present in this sample, the 'static' block has the active sensor dimensions
    int Get_sensor_dim_width(void);                                     // If present in this sample, the 'static' block has the active sensor dimensions
    std::string Get_sensor_dim_units(void);
    std::string Get_tracking_device_serial_number(void);
    double Get_focal_length(void);
    double Get_focus_distance(void);

private:
    opentrackio::OpenTrackIOSample sample;
    std::string sample_str;
    std::string schema_str;
    nlohmann::json sd;
    bool verbose;
    double trans_mult;
    double rot_mult;
    std::string sample_time_format;
    std::vector<std::string> sample_time_formats = {"sec", "timecode", "string"};
    double focus_dist_mult;
};    

#endif /* OPENTRACKIO_H */
