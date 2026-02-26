#!/bin/sh

# Loop over all tweet files from 2020
for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
    # Run the mapper in the background, ignoring hangups
    echo "Starting map job for $file"
    nohup python3 src/map.py --input_path "$file" > /dev/null 2>&1 &

done

echo "All 2020 map jobs have been submitted to the background!"
