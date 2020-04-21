from math import sin, cos, pi
from time import sleep
import serial
from ns_joystick import action
import settings


if __name__ == '__main__':
    port = settings.PORT
    baud = settings.BAUD
    ser = serial.Serial(port, baud)
    r = 127
    phi = 0
    while True:
        action(ser, lx=int(127 + r * cos(phi)), ly=int(127 + r * sin(phi)))
        sleep(0.02)
        if phi > 2 * pi:
            phi = 0
        else:
            phi += 0.1
