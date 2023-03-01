#!/bin/sh
set -e

echo "Garabge Collector DockerImage"


exec python3 webscraper.py &
exec python3 -m flask run --host 0.0.0.0 --port 8080 
