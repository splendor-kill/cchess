#!/bin/bash

PYTHONUNBUFFERED=1 python src/main.py --cmd $1 src/config.yaml > ${1}.log 2>&1
