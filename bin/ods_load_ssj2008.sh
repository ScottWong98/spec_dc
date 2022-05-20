#!bin/sh

curl -X POST http://127.0.0.1:8000/ods/load/ \
-d '{"bm_type": "ssj2008", "filename": "/home/scott/Documents/SPEC_Spider/clean/power/ssj2008.csv"}'

