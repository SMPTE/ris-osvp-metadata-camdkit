@echo off
echo Downloading OpenTrackIO JSON files...

REM Create a directory for the json files.
if not exist "opentrackio-json" mkdir opentrackio_json

REM Grab schema.
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.opentrackio.org/schema.json' -OutFile 'opentrackio_json\schema.json'}"
echo Downloaded schema.json

REM Grab example file.
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.opentrackio.org/examples/complete_static_example.json' -OutFile 'opentrackio_json\complete_static_example.json'}"
echo Downloaded complete_static_example.json

echo Download complete! Files saved to opentrackio_json folder.
pause
