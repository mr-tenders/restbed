#!/usr/bin/env python3
"""
restbed scanner API
"""

from flask import Flask, jsonify, request, send_file
from PIL import Image
# from core import CoreApi

import pyinsane2

import tempfile
import os
import sys

API = Flask(__name__)

@API.route("/scanners")
def list_scanners():
    """
    list scanners available to SANE
    """
    devices = pyinsane2.get_devices()
    names = [device.name for device in devices]
    return jsonify(names)

@API.route("/scanner/<int:scanner_pos>/scan")
def scan(scanner_pos: int):
    devices = pyinsane2.get_devices()
    print(f"Number of scanners found: {len(devices)}")
    dev: pyinsane2.Scanner = devices[scanner_pos]
    query = request.args.get("filename")
    filename = "out.tiff"
    if query is not None:
        filename = query
    filename = os.path.join(tempfile.gettempdir(), filename)
    print(f"Scanning from device: {str(dev)}")
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
    image = session.images[0]
    image.save(filename)
    return send_file(filename, as_attachment=True)

@API.route("/")
def home():
    """
    Home route/index page
    """
    return "Hola, Lola!"

def main():
    """
    API entrypoint
    """
    API.run(port=8080)


if __name__ == '__main__':
    pyinsane2.init()
    try:
        main()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        pyinsane2.exit()
