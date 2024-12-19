cmake_minimum_required(VERSION 3.20)
project(opentrackIO_parser)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)

find_package(nlohmann_json REQUIRED)
find_package(opentrackio-cpp REQUIRED)

add_executable(${PROJECT_NAME} src/opentrackIOlib.cpp)

target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_20)
target_sources(${PROJECT_NAME} PRIVATE src/opentrackIO_parser.cpp)

target_link_libraries(${PROJECT_NAME} 
	opentrackio-cpp::opentrackio-cpp
	nlohmann_json::nlohmann_json
)
