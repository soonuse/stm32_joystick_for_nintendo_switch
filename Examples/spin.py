from math import sin, cos, pi
from time import sleep
import serial
from ns_joystick import send_report


if __name__ == '__main__':
    port = '/dev/ttyUSB0'
    baud = 115200
    ser = serial.Serial(port, baud)
    r = 127
    phi = 0
    while True:
        send_report(ser, lx=int(127 + r * cos(phi)), ly=int(127 + r * sin(phi)))
        sleep(0.02)
        if phi > 2 * pi:
            phi = 0
        else:
            phi += 0.1
