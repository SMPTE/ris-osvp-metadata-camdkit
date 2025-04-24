#!/bin/bash

echo "Downloading OpenTrackIO JSON files..."

# Create a directory for the json files if it doesn't exist.
if [ ! -d "opentrackio-json" ]; then
    mkdir opentrackio-json
fi

# Grab schema.
if command -v curl > /dev/null; then
    curl -L "https://www.opentrackio.org/schema.json" -o "opentrackio-json/schema.json"
elif command -v wget > /dev/null; then
    wget -O "opentrackio-json/schema.json" "https://www.opentrackio.org/schema.json"
else
    echo "Error: Neither curl nor wget is installed. Please install one of them and try again."
    exit 1
fi
echo "Downloaded schema.json"

# Grab example file.
if command -v curl > /dev/null; then
    curl -L "https://www.opentrackio.org/examples/complete_static_example.json" -o "opentrackio-json/complete_static_example.json"
elif command -v wget > /dev/null; then
    wget -O "opentrackio-json/complete_static_example.json" "https://www.opentrackio.org/examples/complete_static_example.json"
fi
echo "Downloaded complete_static_example.json"

echo "Download complete! Files saved to opentrackio_json folder."
