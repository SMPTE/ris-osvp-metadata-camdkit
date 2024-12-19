# OpenTrackIO Parser Example

This C++ application mirrors the Python parser found in /src/test/python/parser

It uses the opentrackio-cpp Conan package to replicate the output of the Python
version.

## Configure Conan
```
conan profile detect --force
```
Then edit the profile to force C++ 20. THe profile path is found with:
```
conan profile path default
```
Update `compiler.cppstd=20`

## Build and run

In Windows:
```
conan install . --output-folder=build --build=missing
cd build
cmake .. -G "Visual Studio 17 2022" -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake"
cmake --build . --config Release
.\Release\opentrackIO_parser.exe --file=opentrackio_sample.json --schema=opentrackio_schema.json
```

See [this tutorial](https://docs.conan.io/2/tutorial/consuming_packages/build_simple_cmake_project.html) for other platforms.
