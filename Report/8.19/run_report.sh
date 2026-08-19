#!/bin/bash

BASE_DIR=/opt/json-report

python3 "$BASE_DIR/report.py" \
    "$BASE_DIR/inference.json" \
    "$BASE_DIR/report.md"
