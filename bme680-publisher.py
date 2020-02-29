#!/usr/bin/env python3

import argparse
import flask
import json
import logging


parser = argparse.ArgumentParser(description="Publish measurements from BME680.")
parser.add_argument("-i", "--in", dest="_in", default="measurements", help="File to read from.")
parser.add_argument("-p", "--port", type=int, default=8008, help="Port to publish data on.")
parser.add_argument("-v", "--verbose", action="store_true", help="Print out additional info.")
args = parser.parse_args()


# Flask config.
app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')

if not args.verbose:
    log.disabled = True


# Flask endpoint.
@app.route('/')
def publish():
    with open(args._in, "r") as measurements_file:
        return flask.jsonify(json.load(measurements_file))


# Run flask app.
app.run(debug=False, host="0.0.0.0", port=args.port)
