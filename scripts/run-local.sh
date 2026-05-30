#!/usr/bin/env bash
set -e

docker build -t space-data-monitor:local .
docker run --rm -p 8080:8080 space-data-monitor:local
