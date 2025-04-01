# OpenTrackIO Parser C++ Example

## Contents

- [Overview](#overview)
- [Required Software](#required-software)
- [Setup Instructions](#setup-instructions)
    - [Windows](#windows)
    - [Linux/MacOS](#linuxmacos)

## Overview

This C++ example implements a simple OpenTrackIO JSON sample parser. The parser includes methods for accessing values 
and scaling them to user-preferred units.

## Required Software
- C++20
- Python 3.8 or higher
- CMake

## Setup Instructions

### Windows

1. Download OpenTrackIO schema and a sample examples.
   ```
   get-opentrackio-json.bat
   ```

2. Set up Python virtual environment
   ```
   python -m venv venv
   ```

   - Command Prompt:
   ```
   .\venv\Scripts\activate.bat
   ```

   - PowerShell:
   ```
   .\venv\Scripts\Activate.ps1
   ```

3. Set up Conan
   ```
   pip install conan
   ```
   
   Set up Conan profile (first-time only)
   ```
   conan profile detect
   ```

   Install Conan dependencies
   ```
   conan install . --build=missing -s compiler.cppstd=20 -s build_type=Release
   conan install . --build=missing -s compiler.cppstd=20 -s build_type=Debug
   ```

4. Generate and build CMake
   ```
   cmake -S . -B ./build
   cmake --build ./build --target opentrackio-parser --config Release
   ```

5. Run OpenTrackIO parser
    - Command Prompt:
      ```
      .\build\Release\opentrackio-parser.exe -f %CD%\opentrackio-json\complete_static_example.json -s %CD%\opentrackio-json\schema.json
      ```

    - PowerShell:
      ```
      .\build\Release\opentrackio-parser.exe -f $PWD\opentrackio-json\complete_static_example.json -s $PWD\opentrackio-json\schema.json
      ```

### Linux/MacOS

1. Download JSON files
   ```
   sudo bash ./get-opentrackio-json.sh
   ```

2. Set up Python virtual environment
   ```
   python3 -m venv venv
   source ./venv/bin/activate
   ```

3. Install Conan
   ```
   pip install conan
   ```

   Set up Conan profile (first-time only)
   ```
   conan profile detect
   ```

   Install Conan dependencies
   ```
   conan install . --build=missing -s compiler.cppstd=20 -s build_type=Release
   conan install . --build=missing -s compiler.cppstd=20 -s build_type=Debug
   ```

4. Generate and build CMake
   Release
   ```
   cmake -S . -B ./build -DCMAKE_BUILD_TYPE=Release
   cmake --build ./build --target opentrackio-parser --config Release
   ```
   
    Debug
    ```
   cmake -S . -B ./build -DCMAKE_BUILD_TYPE=Debug
   cmake --build ./build --target opentrackio-parser --config Debug
    ```

5. Run OpenTrackIO parser
   ```
   ./build/opentrackio-parser -f $PWD/opentrackio-json/complete_static_example.json -s $PWD/opentrackio-json/schema.json
   ```
   