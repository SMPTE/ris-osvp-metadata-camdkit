cmake_minimum_required(VERSION 3.30)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(opentrackio-parser)

# todo: directory changes on linux, windows, and mac.
set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_BINARY_DIR}/generators/" ${CMAKE_PREFIX_PATH})

find_package(opentrackio-cpp CONFIG REQUIRED)
find_package(nlohmann_json REQUIRED)

add_executable(
        ${PROJECT_NAME}
        src/main.cpp
        src/helpers/opentrackIOlib.cpp)

target_include_directories(
        ${PROJECT_NAME}
        PRIVATE
        src/helpers
        src/argparse)

target_link_libraries(
        ${PROJECT_NAME}
        PRIVATE
        opentrackio-cpp::opentrackio-cpp
        nlohmann_json::nlohmann_json)
