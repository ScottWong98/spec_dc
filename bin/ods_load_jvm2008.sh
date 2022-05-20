#!bin/sh

curl -X POST http://127.0.0.1:8000/ods/load/ \
-d '{"bm_type": "jvm2008", "filename": "/home/scott/Documents/SPEC_Spider/clean/java/jvm2008.csv"}'

