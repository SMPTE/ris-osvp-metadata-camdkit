cmake_minimum_required(VERSION 3.30)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(opentrackio-parser)

if(WIN32)
    set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_BINARY_DIR}/generators/" ${CMAKE_PREFIX_PATH})
else()
    set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_BUILD_TYPE}/generators/" ${CMAKE_PREFIX_PATH})
endif()

find_package(opentrackio-cpp CONFIG REQUIRED)
find_package(nlohmann_json REQUIRED)

add_executable(
        ${PROJECT_NAME}
        src/main.cpp
        src/opentrackio-lib/OpenTrackIOParser.cpp)

target_include_directories(
        ${PROJECT_NAME}
        PRIVATE
        src/opentrackio-lib
        src/argparse)

target_link_libraries(
        ${PROJECT_NAME}
        PRIVATE
        opentrackio-cpp::opentrackio-cpp
        nlohmann_json::nlohmann_json)
