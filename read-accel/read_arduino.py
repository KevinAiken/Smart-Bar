import ctypes
from time import sleep

import os
import serial
import sys


def _cast_int8(val):
    return ctypes.c_int8(val).value


def _raw_data_to_accl(x, y, z):
    return x / 21.0, y / 21.0, z / 21.0


class ArduinoAccelerometer:
    def __init__(self):
        self._serial = serial.Serial(
            '/dev/ttyACM1',
            baudrate=115200,
            timeout=0.2,
            exclusive=True)
        sleep(1)  # ugh. see stackoverflow.com/a/4242445/2299084

    def _get_response(self):
        self._serial.read_all()  # flush existing data
        bytes_written = self._serial.write(b"G")
        assert bytes_written == 1
        return self._serial.readline().decode('ascii')

    def get_acceleration(self):
        """returns a 3-tuple with the acceleration (x, y, z)"""
        response = self._get_response()
        return _raw_data_to_accl(
            _cast_int8(int(response[0:2], base=16)),
            _cast_int8(int(response[2:4], base=16)),
            _cast_int8(int(response[4:6], base=16)))


def main():
    v = ArduinoAccelerometer()
    while True:
        x, y, z = v.get_acceleration()
        sys.stdout.write("{:.02f}, {:.02f}, {:.02f}    \r".format(x, y, z))


if __name__ == '__main__':
    main()
