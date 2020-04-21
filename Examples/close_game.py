from math import sin, cos, pi
from time import sleep
import serial
from ns_joystick import action, Button, Stick, Hat
import settings


if __name__ == '__main__':
    port = settings.PORT
    baud = settings.BAUD
    ser = serial.Serial(port, baud)
    action(ser, buttons=Button.HOME, duration=0.1)
    sleep(2)
    action(ser, buttons=Button.X, duration=0.1)
    sleep(1)
    action(ser, buttons=Button.A, duration=0.1)
    sleep(1)
    action(ser, buttons=Button.A, duration=0.1)