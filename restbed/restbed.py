#!/usr/bin/env python3
"""
restbed scanner API
"""

from flask import Flask, jsonify

import pyinsane2

pyinsane2.init()
API = Flask(__name__)

@API.route("/scanners")
def list_scanners():
    """
    list scanners available to SANE
    """
    devices = pyinsane2.get_devices()
    names = [device.name for device in devices]
    return jsonify(names)

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
    try:
        main()
    finally:
        pyinsane2.exit()
