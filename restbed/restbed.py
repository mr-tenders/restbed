#!/usr/bin/env python3
"""
restbed scanner API
"""

import pyinsane2

from flask import Flask, jsonify, request, send_file
from PIL import Image

from .core import context

import logging
import tempfile
import os
import sys

if sys.version_info.major != 3:
    raise SystemError("Python 3 required")

API = Flask(__name__)
LOGGER = logging.getLogger(__name__)

@API.route("/scanners")
def list_scanners():
    """
    list scanners available to SANE
    """
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    names = [device.name for device in devices]
    pyinsane2.exit()
    return jsonify(names)

@API.route("/scanner/<int:scanner_pos>/scan")
def scan(scanner_pos: int):
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    print(f"Number of scanners found: {len(devices)}")
    dev: pyinsane2.Scanner = devices[scanner_pos]
    query = request.args.get("filename")
    temp_handle, filename = tempfile.mkstemp(".tif", dir=tempfile.gettempdir())
    os.close(temp_handle) # closing so PILLOW can handle the file save
    if query is not None:
        filename = os.path.join(tempfile.gettempdir(), query)
    LOGGER.info(f"Scanning from device: {str(dev)}")
    LOGGER.info(f"Temp file: {filename}")
    session: pyinsane2.ScanSession = dev.scan()
    try:
        PROGRESSION_INDICATOR = ['|', '/', '-', '\\']
        i = -1
        while True:
            i += 1
            i %= len(PROGRESSION_INDICATOR)
            sys.stdout.write("\b%s" % PROGRESSION_INDICATOR[i])
            sys.stdout.flush()

            session.scan.read()
    except EOFError:
        pass
    image: Image.Image = session.images[0]
    image.save(filename)

    pyinsane2.exit()
    return send_file(filename, as_attachment=True)

@API.route("/")
def home():
    """
    Home route/index page
    """
    return "Hola, Lola!"


def main(port=9090):
    """
    API entrypoint
    """
    API.run(port=port)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9090, help="HTTP port to use")
    args = parser.parse_args()
    try:
        main(args.port)
    except Exception as ex:
        LOGGER.error(f"Unknown error occurred. Message: {str(ex)}")
