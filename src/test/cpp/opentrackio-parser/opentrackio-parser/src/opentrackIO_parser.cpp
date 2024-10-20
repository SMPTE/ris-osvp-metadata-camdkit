#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "argparse/argparse.hpp"
#include "opentrackIOlib.h"

int main(int argc, char* argv[]) {
    argparse::ArgumentParser parser("OpenTrackingProtocol parser");
    
    parser.add_argument("-f", "--file")
        .help("The JSON input file.")
        .default_value(std::string());
    
    parser.add_argument("-s", "--schema")
        .help("The schema (JSON) input file.")
        .default_value(std::string());
    
    parser.add_argument("-v", "--verbose")
        .help("Make script more verbose")
        .default_value(false)
        .implicit_value(true);

    try {
        parser.parse_args(argc, argv);
    }
    catch (const std::runtime_error& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << parser;
        return 1;
    }
    std::string sample_text;
    std::string schematext;
    bool verbose = parser.get<bool>("--verbose");
    
    if (parser.is_used("--schema")) {
        std::string schemapath = parser.get<std::string>("--schema");
        if (std::filesystem::exists(schemapath)) {
            std::ifstream file(schemapath);
            if (file.is_open()) {
                std::cout << "Reading OTIO schema file: " << schemapath << std::endl;
                schematext.assign((std::istreambuf_iterator<char>(file)),
                                   std::istreambuf_iterator<char>());
                file.close();
            }
        }
    }

    if (parser.is_used("--file")) {
        std::string filepath = parser.get<std::string>("--file");
        if (std::filesystem::exists(filepath)) {
            std::ifstream file(filepath);
            if (file.is_open()) {
                std::cout << "Reading OTIO sample file: " << filepath << std::endl;
                sample_text.assign((std::istreambuf_iterator<char>(file)),
                                    std::istreambuf_iterator<char>());
                file.close();
            }
        }
    }


    OTProtocol sample(sample_text, schematext, verbose);
    sample.Parse();
    sample.Import_schema();

    sample.Set_trans_units("cm");
    sample.Set_sample_time_format("sec");
    sample.Set_focus_distance_units("cm");
    sample.Set_rotation_units("deg");
    std::cout << std::endl;

    std::string protocol = sample.Get_protocol();
    std::string slate = sample.Get_slate();
    std::cout << "Detected protocol: " << protocol << std::endl;
    std::cout << "On slate: " << slate << std::endl;
    std::string timecode = sample.Get_timecode();
    std::cout << "Current camera timecode: " << timecode << std::endl;
    double framerate = sample.Get_timecode_framerate();
    std::cout << "At a camera frame rate of: " << std::fixed << std::setprecision(5) << framerate << std::endl;
    std::cout << std::endl;

    std::cout << "Sample time PTP time is: " << sample.Get_sample_time() << " sec" << std::endl;
    sample.Set_sample_time_format("string");
    std::cout << "Sample time PTP as a string: " << sample.Get_sample_time() << std::endl;
    sample.Set_sample_time_format("timecode");
    std::cout << "Sample time PTP as timecode: " << sample.Get_sample_time() << std::endl;
    std::cout << "Sample time PTP elements: " << sample.Get_sample_time("yy") << " "
              << sample.Get_sample_time("dd") << " "
              << sample.Get_sample_time("hh") << " "
              << sample.Get_sample_time("mm") << " "
              << sample.Get_sample_time("ss") << " "
              << sample.Get_sample_time("ns") << std::endl;
    std::cout << std::endl;

    std::string snum = sample.Get_tracking_device_serial_number();
    if (!snum.empty()) {
        std::cout << "Tracking device serial number: " << snum << std::endl;
    } else {
        std::cout << "Unknown tracking device, wait for static sample to come in..." << std::endl;
    }

    double posX = sample.Get_camera_trans("x");
    double posY = sample.Get_camera_trans("y");
    double posZ = sample.Get_camera_trans("z");
    std::cout << "Camera position is: (" << posX << "," << posY << "," << posZ << ") cm" << std::endl;

    double rotX = sample.Get_camera_rot("p");
    double rotY = sample.Get_camera_rot("t");
    double rotZ = sample.Get_camera_rot("r");
    std::cout << "Camera rotation is: (" << rotX << "," << rotY << "," << rotZ << ") deg" << std::endl;

    sample.Set_rotation_units("rad");
    rotX = sample.Get_camera_rot("p");
    rotY = sample.Get_camera_rot("t");
    rotZ = sample.Get_camera_rot("r");
    std::cout << "Camera rotation is: (" << std::fixed << std::setprecision(5) 
              << rotX << "," << rotY << "," << rotZ << ") radians" << std::endl;
    std::cout << std::endl;

    double fl = sample.Get_focal_length();
    double height = sample.Get_sensor_dim_height();
    if (height != 0) {
        double width = sample.Get_sensor_dim_width();
        std::string units = sample.Get_sensor_dim_units();
        std::cout << "Active camera sensor height: " << height << ", width: " << width << " " << units << std::endl;
    } else {
        std::cout << "Unknown camera sensor, wait for static sample to come in..." << std::endl;
    }

    std::cout << "Focal length is: " << fl << std::endl;

    double fd = sample.Get_focus_distance();
    std::cout << "Focus distance is: " << fd << " cm" << std::endl;

    sample.Set_focus_distance_units("in");
    fd = sample.Get_focus_distance();
    std::cout << "Focus distance is: " << std::fixed << std::setprecision(4) << fd << " in" << std::endl;

    return 0;
}

