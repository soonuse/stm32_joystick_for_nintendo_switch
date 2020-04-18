"""
@brief: Buttons / Joystick configurations for Nintendo Switch
        often used for serial control.
@author: Yehui
"""


class Hat:
    TOP = 0x00
    TOP_RIGHT = 0x01
    RIGHT = 0x02
    BOTTOM_RIGHT = 0x03
    BOTTOM = 0x04
    BOTTOM_LEFT = 0x05
    LEFT = 0x06
    TOP_LEFT = 0x07
    CENTER = 0x08


class Button:
    Y = 0x01
    B = 0x02
    A = 0x04
    X = 0x08
    L = 0x10
    R = 0x20
    ZL = 0x40
    ZR = 0x80
    MINUS = 0x100
    PLUS = 0x200
    LCLICK = 0x400
    RCLICK = 0x800
    HOME = 0x1000
    CAPTURE = 0x2000


class Stick:
    MIN = 0
    CENTER = 128
    MAX = 255


class UsbJoystickReport:

    def __init__(
        self,
        buttons=0x0000,
        hat=Hat.CENTER,
        lx=Stick.CENTER,
        ly=Stick.CENTER,
        rx=Stick.CENTER,
        ry=Stick.CENTER,
        vendor=0x00
    ):
        self.buttons = buttons
        self.hat = hat
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.vendor = vendor
        assert Stick.MIN <= lx <= Stick.MAX
        assert Stick.MIN <= ly <= Stick.MAX
        assert Stick.MIN <= rx <= Stick.MAX
        assert Stick.MIN <= ry <= Stick.MAX

    def set_report(
        self,
        buttons=0x0000,
        hat=Hat.CENTER,
        lx=Stick.CENTER,
        ly=Stick.CENTER,
        rx=Stick.CENTER,
        ry=Stick.CENTER,
        vendor=0x00
    ):
        self.buttons = buttons
        self.hat = hat
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.vendor = vendor
        assert 0 <= lx <= 255, f'{lx}'
        assert 0 <= ly <= 255, f'{ly}'
        assert 0 <= rx <= 255, f'{rx}'
        assert 0 <= ry <= 255, f'{ry}'

    def get_bytes(self):
        leading = b'\x88'
        buttons = self.buttons.to_bytes(length=2, byteorder='little', signed=False)
        hat = self.hat.to_bytes(length=1, byteorder='little', signed=False)
        lx = self.lx.to_bytes(length=1, byteorder='little', signed=False)
        ly = self.ly.to_bytes(length=1, byteorder='little', signed=False)
        rx = self.rx.to_bytes(length=1, byteorder='little', signed=False)
        ry = self.ry.to_bytes(length=1, byteorder='little', signed=False)
        vendor = self.vendor.to_bytes(length=1, byteorder='little', signed=False)
        b_arr = bytearray(leading + buttons + hat + lx + ly + rx + ry + vendor)
        return b_arr

    def reset(self):
        self.buttons = 0x0000
        self.hat = Hat.CENTER
        self.lx = Stick.CENTER
        self.ly = Stick.CENTER
        self.rx = Stick.CENTER
        self.ry = Stick.CENTER
        self.vendor = 0x00
