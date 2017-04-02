import ctypes
from time import sleep
from os import path
import sys

import serial


def _cast_int8(val):
    return ctypes.c_int8(val).value


def _raw_data_to_accl(x, y, z):
    return x / 21.0, y / 21.0, z / 21.0



class ArduinoAccelerometer(object):
    def __init__(self, dev="ttyACM1"):
        self._serial = serial.Serial(
            path.join("/dev/", dev),
            baudrate=115200,
            timeout=0.2,
            exclusive=True)
        sleep(2)  # ugh. see stackoverflow.com/a/4242445/2299084

    def _get_response(self):
        self._serial.read_all()  # flush existing data
        bytes_written = self._serial.write(b"G")
        assert bytes_written == 1
        return self._serial.readline().decode('ascii')

    def get_acceleration(self):
        response = self._get_response()
        return _raw_data_to_accl(
            _cast_int8(int(response[0:2], base=16)),
            _cast_int8(int(response[2:4], base=16)),
            _cast_int8(int(response[4:6], base=16)))


def main():
    v = ArduinoAccelerometer("ttyACM1")
    v2 = ArduinoAccelerometer("ttyACM0")
    while True:
        x, y, z = v.get_acceleration()
        x2, y2, z2 = v2.get_acceleration()
        sys.stdout.write("\r{:+.02f}, {:+.02f}, {:+.02f}; {:+.02f}, {:+.02f}, {:+.02f}".format(x, y, z, x2, y2, z2))


if __name__ == '__main__':
    main()
