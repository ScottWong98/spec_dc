#!bin/sh

curl -X POST http://127.0.0.1:8000/ods/load/ \
-d '{"bm_type": "jbb2015", "filename": "/home/scott/Documents/SPEC_Spider/clean/java/jbb2015.csv"}'

