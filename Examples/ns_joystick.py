"""
@brief: Buttons / Joystick configurations for Nintendo Switch
        often used for serial control.
@author: Yehui
"""
import time

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
        buttons=0x0000, hat=Hat.CENTER,
        lx=Stick.CENTER, ly=Stick.CENTER,
        rx=Stick.CENTER, ry=Stick.CENTER,
    ):
        self.buttons = buttons
        self.hat = hat
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        assert Stick.MIN <= lx <= Stick.MAX
        assert Stick.MIN <= ly <= Stick.MAX
        assert Stick.MIN <= rx <= Stick.MAX
        assert Stick.MIN <= ry <= Stick.MAX

    def set_report(
        self,
        buttons=0x0000, hat=Hat.CENTER,
        lx=Stick.CENTER, ly=Stick.CENTER,
        rx=Stick.CENTER, ry=Stick.CENTER,
    ):
        self.buttons = buttons
        self.hat = hat
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        assert 0 <= lx <= 255, f'{lx}'
        assert 0 <= ly <= 255, f'{ly}'
        assert 0 <= rx <= 255, f'{rx}'
        assert 0 <= ry <= 255, f'{ry}'

    def get_bytes(self):
        buttons = self.buttons.to_bytes(length=2, byteorder='little', signed=False)
        hat = self.hat.to_bytes(length=1, byteorder='little', signed=False)
        lx = self.lx.to_bytes(length=1, byteorder='little', signed=False)
        ly = self.ly.to_bytes(length=1, byteorder='little', signed=False)
        rx = self.rx.to_bytes(length=1, byteorder='little', signed=False)
        ry = self.ry.to_bytes(length=1, byteorder='little', signed=False)
        b_arr = bytearray(buttons + hat + lx + ly + rx + ry)
        return b_arr

    def get_serial_bytes(self):
        """
        Expends the bytes of report. len(ret_arr) = len(b_arr) / 7 * 8
        The first bit indicates the beginning of sync.
        The first bits of the following bytes are fixed to 0.
        """
        b_arr = self.get_bytes()
        ret_arr = bytearray(8)
        ret_arr[0] = 0x80 | (b_arr[0] >> 1)
        for i in range(1, 7):
            temp = (b_arr[i - 1] << (7 - i)) & 0xFF
            ret_arr[i] = (temp | (b_arr[i] >> (i + 1))) & 0x7F
        ret_arr[-1] = b_arr[-1] & 0x7F
        return ret_arr

    def reset(self):
        self.buttons = 0x0000
        self.hat = Hat.CENTER
        self.lx = Stick.CENTER
        self.ly = Stick.CENTER
        self.rx = Stick.CENTER
        self.ry = Stick.CENTER
        
def action(
    ser,
    buttons=0x0000, hat=Hat.CENTER,
    lx=Stick.CENTER, ly=Stick.CENTER,
    rx=Stick.CENTER, ry=Stick.CENTER,
    duration=None,
):
    """
    If the duration is None, the action loops forever
    else the report will be reset after the duration.
    """
    report = UsbJoystickReport(buttons=buttons, hat=hat, lx=lx, ly=ly, rx=rx, ry=ry)
    ser.write(report.get_serial_bytes())
    if duration is not None:
        time.sleep(duration)
        report.reset()
        ser.write(report.get_serial_bytes())
