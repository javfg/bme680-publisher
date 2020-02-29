#!/usr/bin/env python3

import argparse
import calendar
import json
import time

import bme680


parser = argparse.ArgumentParser(description="Read measurements from BME680.")
parser.add_argument("-o", "--out", default="measurements", help="File to write to.")
parser.add_argument("-v", "--verbose", action="store_true", help="Print out additional info.")
args = parser.parse_args()


try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)


if (args.verbose):
    print("Calibration data:")
    for name in dir(sensor.calibration_data):
        if not name.startswith("_"):
            value = getattr(sensor.calibration_data, name)
            if isinstance(value, int):
                print(f"{name}: {value}")


# Default oversampling settings.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)


if (args.verbose):
    print("\n\nInitial reading:")
    for name in dir(sensor.data):
        value = getattr(sensor.data, name)

        if not name.startswith("_"):
            print(f"{name}: {value}")


# Default settings.
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


# Response template.
measurement = {'time': None, 'temp': None, 'humi': None, 'pres': None, 'airq': None}


# Reading.
try:
    while True:
        with open(args.out, "wt") as measurements_file:
            if sensor.get_sensor_data():
                measurement['time'] = calendar.timegm(time.gmtime())
                measurement['temp'] = sensor.data.temperature
                measurement['humi'] = sensor.data.humidity
                measurement['pres'] = sensor.data.pressure

                if sensor.data.heat_stable:
                    measurement['airq'] = sensor.data.gas_resistance

            if args.verbose:
                print(measurement)

            json.dump(measurement, measurements_file)
            measurements_file.flush()

            time.sleep(1)

except KeyboardInterrupt:
    pass
