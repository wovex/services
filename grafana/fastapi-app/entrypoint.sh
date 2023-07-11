#!/bin/bash

/opt/node_exporter-1.6.0.linux-amd64/node_exporter &

if [ "$DEBUG" == "true" ]
then
  uvicorn main:app --reload --port 5000 --host 0.0.0.0
else
  uvicorn main:app --port 5000 --host 0.0.0.0
fi
