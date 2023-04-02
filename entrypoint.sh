#!/usr/bin/env bash

python3 get_raw_data.py
uvicorn financial.main:app --proxy-headers --host 0.0.0.0 --port 8000