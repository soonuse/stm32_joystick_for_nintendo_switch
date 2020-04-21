from math import sin, cos, pi
from time import sleep
import serial
from ns_joystick import action, Button, Stick, Hat
import settings


if __name__ == '__main__':
    port = settings.PORT
    baud = settings.BAUD
    ser = serial.Serial(port, baud)
    action(ser)