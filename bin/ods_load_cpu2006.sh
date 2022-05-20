#!bin/sh

curl -X POST http://127.0.0.1:8000/ods/load/ \
-d '{"bm_type": "cpu2006", "filename": "/home/scott/Documents/SPEC_Spider/clean/cpu/cpu2006.csv"}'

