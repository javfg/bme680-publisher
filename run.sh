#!/bin/bash

screen -d -m -S bme680-reader ./bme680-reader.py -v
echo "Started bme-reader"
screen -d -m -S bme680-publisher ./bme680-publisher.py -v
echo "Started bme-publisher"
