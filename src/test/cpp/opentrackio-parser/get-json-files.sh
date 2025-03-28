#!/bin/bash

echo "Downloading OpenTrackIO JSON files..."

# Create a directory for the json files if it doesn't exist.
if [ ! -d "opentrackio_json" ]; then
    mkdir opentrackio_json
fi

# Grab schema.
if command -v curl > /dev/null; then
    curl -L "https://www.opentrackio.org/schema.json" -o "opentrackio_json/schema.json"
elif command -v wget > /dev/null; then
    wget -O "opentrackio_json/schema.json" "https://www.opentrackio.org/schema.json"
else
    echo "Error: Neither curl nor wget is installed. Please install one of them and try again."
    exit 1
fi
echo "Downloaded schema.json"

# Grab example file.
if command -v curl > /dev/null; then
    curl -L "https://www.opentrackio.org/examples/complete_static_example.json" -o "opentrackio_json/complete_static_example.json"
elif command -v wget > /dev/null; then
    wget -O "opentrackio_json/complete_static_example.json" "https://www.opentrackio.org/examples/complete_static_example.json"
fi
echo "Downloaded complete_static_example.json"

echo "Download complete! Files saved to opentrackio_json folder."
echo "Press Enter to continue..."
read
