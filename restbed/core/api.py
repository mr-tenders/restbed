"""
restbed core api
"""
import pyinsane2

from typing import List

class CoreApi(object):
    scanner: pyinsane2.Scanner = None
    scan_session: pyinsane2.ScanSession = None

    @staticmethod
    def initialize():
        """
        initialize SANE, don't call if unit testing
        (well that's the hope...)
        """
        pyinsane2.init()

    def select_device(self):
        devs: List[pyinsane2.Scanner] = pyinsane2.get_devices()
        self.scanner = devs[0]
        return self.scanner

    def start_scanning(self):
        pyinsane2.maximize_scan_area(self.scanner)
        self.scan_session = self.scanner.scan()
