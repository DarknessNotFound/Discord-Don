#!/bin/bash
clear
rm -rf testing_outputs

mkdir "./testing_outputs"
mkdir "./testing_outputs/data"
python3 -m unittest discover -t .
cd "testing_outputs"
python3 ../manual_tests.py