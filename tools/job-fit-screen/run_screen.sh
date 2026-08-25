#!/bin/bash
# Thin launcher for job_fit_screen.py — mirrors run_converter.sh in docx-to-markdown.
python3 "$(dirname "$0")/job_fit_screen.py" "$@"
