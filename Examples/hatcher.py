from math import sin, cos, pi
from time import sleep, time
import serial
from ns_joystick import action, Button, Stick, Hat
import settings


if __name__ == '__main__':
    port = settings.PORT
    baud = settings.BAUD
    ser = serial.Serial(port, baud)
    while True:
        # Flying to front of daycare
        action(ser, buttons=Button.X, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(3)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(3)
        # Walking back to get egg and putting it in party 
        action(ser, ly=Stick.MAX, duration=1)
        action(ser, lx=Stick.MIN, duration=0.1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(2)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(2)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(2)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(2)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(3)
        action(ser, ly=Stick.MAX, duration=0.1)
        sleep(2)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        # Take the item off
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        action(ser, buttons=Button.A, duration=0.1)
        sleep(1)
        # Getting on bike, moving up and to the right, then start looping
        action(ser, buttons=Button.PLUS, duration=0.1)
        action(ser, lx=Stick.MAX, ly=Stick.MIN, duration=3)
        # rock and roll
        r = 127
        phi = 0
        start_hatch = time()
        while time() - start_hatch < 30:
            action(ser, lx=int(127 + r * cos(phi)), ly=int(127 + r * sin(phi)))
            sleep(0.02)
            if phi > 2 * pi:
                phi = 0
            else:
                phi += 0.1