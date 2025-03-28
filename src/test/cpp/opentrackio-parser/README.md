required software

python3

python -m venv vevn

Activate the virtual environment (Command Prompt)

`.\vevn\Scripts\activate.bat`

Activate the virtual environment (PowerShell)

`.\vevn\Scripts\Activate.ps1`

`pip install conan`

`conan install . --output-folder=build --build=missing -s compiler.cppstd=20`

`cmake.exe" -G "Visual Studio 17 2022" -S opentrackio-parser -B ./build`
