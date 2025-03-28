required software
python3
cmake

Linux/MacOS
`sudo bash ./get-json-files.sh`

`python -m venv vevn`

Activate the virtual environment (Command Prompt)

`.\vevn\Scripts\activate.bat`

Activate the virtual environment (PowerShell)

`.\vevn\Scripts\Activate.ps1`

Linux

MacOS
`source ./venv/bin/activate`



`pip install conan`

If it's your first time running conan you will need to create a profile with the following.
`conan profile detect`

`conan install . --build=missing -s compiler.cppstd=20`

Windows
`cmake -S . -B ./build`

Linux/MacOS
`cmake -S . -B ./build -DCMAKE_BUILD_TYPE=Release`

`cmake --build ./build --target opentrackio-parser --config Release`

## Windows

Run in command prompt
`.\build\Release\opentrackio-parser.exe -f %CD%\opentrackio-json\complete_static_example.json -s %CD%\opentrackio-json\schema.json`

PowerShell
`.\build\Release\opentrackio-parser.exe -f $PWD\opentrackio-json\complete_static_example.json -s $PWD\opentrackio-json\schema.json`

Linux/MacOS
`./build/opentrackio-parser -f $PWD/opentrackio_json/complete_static_example.json -s $PWD/opentrackio_json/schema.json`