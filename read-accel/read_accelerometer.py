import abc
import ctypes
from time import sleep
import sys

import serial
import smbus


def _cast_int8(val):
    return ctypes.c_int8(val).value


def _raw_data_to_accl(x, y, z):
    return x / 21.0, y / 21.0, z / 21.0


class AccelerometerReader(abc.ABC):
    @abc.abstractmethod
    def get_acceleration(self):
        """returns a 3-tuple with the acceleration (x, y, z)"""
        pass


class ArduinoAccelerometer(AccelerometerReader):
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
        response = self._get_response()
        return _raw_data_to_accl(
            _cast_int8(int(response[0:2], base=16)),
            _cast_int8(int(response[2:4], base=16)),
            _cast_int8(int(response[4:6], base=16)))


class _RegisterReadFailed(RuntimeError):
    pass


class RpiAccelerometer(AccelerometerReader):
    # this class is based upon MMA7660.cpp

    # spec sheet: http://www.nxp.com/assets/documents/data/en/data-sheets/MMA7660FC.pdf
    # register definitions are on page 14
    MMA7660_ADDR = 0x4c
    REG_XOUT = 0x00
    REG_YOUT = 0x01
    REG_ZOUT = 0x02
    REG_TILT = 0x03  # tilt status
    REG_SRST = 0x04  # sampling rate status
    REG_SPCNT = 0x05  # sleep count
    REG_INTSU = 0x06  # interrupt setup
    REG_MODE = 0x07
    REG_SR = 0x08  # Auto-Wake/Sleep and Portrait/Landscape samples per seconds
    # and Debounce Filter
    REG_PDET = 0x09  # tap detection
    REG_PD = 0x0A  # tap debounce count
    INTSU_X = 0x80
    INTSU_Y = 0x40
    INTSU_Z = 0x20
    INTSU_G = 0x10
    INTSU_AS = 0x08
    INTSU_PD = 0x04
    INTSU_PL = 0x02
    INTSU_FB = 0x01
    MODE_STAND_BY = 0x00
    MODE_ACTIVE = 0x01
    AUTO_SLEEP_120 = 0X00  # 120 sample per second
    AUTO_SLEEP_64 = 0X01
    AUTO_SLEEP_32 = 0X02
    AUTO_SLEEP_16 = 0X03
    AUTO_SLEEP_8 = 0X04
    AUTO_SLEEP_4 = 0X05
    AUTO_SLEEP_2 = 0X06
    AUTO_SLEEP_1 = 0X07

    def __init__(self):
        self._bus = smbus.SMBus(0)
        self._set_mode(self.MODE_STAND_BY)
        self._set_sample_rate(self.AUTO_SLEEP_32)
        self._set_mode(self.MODE_ACTIVE)

    def _read(self, reg):
        return self._bus.read_byte_data(reg)

    def _write(self, reg, data):
        self._bus.write_byte_data(self.MMA7660_ADDR, reg, data)

    def _set_mode(self, mode):
        self._write(self.REG_MODE, mode)

    def _set_sample_rate(self, rate):
        self._write(self.REG_SR, rate)

    def _read_xyz_reg(self, reg):
        """for certain regs, bit 7 is an alert bit the alerts the programmer
        that the read might be torn. In the case that it is, all regs must be
        re-read"""
        v = self._read(reg)
        if v & 0x40 > 0:  # alert set, raise so we can retry
            raise _RegisterReadFailed()

    def _get_xyz(self):
        try:
            return self._read(self.REG_XOUT), \
                   self._read(self.REG_YOUT), \
                   self._read(self.REG_ZOUT)
        except _RegisterReadFailed:
            return self._get_xyz()

    def get_acceleration(self):
        return _raw_data_to_accl(*self._get_xyz())


def main():
    v = RpiAccelerometer()
    while True:
        x, y, z = v.get_acceleration()
        sys.stdout.write("{:.02f}, {:.02f}, {:.02f}    \r".format(x, y, z))


if __name__ == '__main__':
    main()
