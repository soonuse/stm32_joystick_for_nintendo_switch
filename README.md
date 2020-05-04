# stm32_joystick_for_nintendo_switch
STM32 Joystick for Nintendo Switch

I am also a Nintendo big fan outside of working hours. I tried to play switch games by my PC and there are many ways to do such things.  Using Arduino/Teensy is a good choice, but for me porting the joystick USB driver to a STM32 development board is also a nice game, faster and more stable. With serial (UART) control function I can play my Switch using the PC.

This program allows you to control your Nintendo switch through the serial port using an STM32 development board, which means that you can control your switch using PC. Writing python scripts are also perfect choices for TAS.

This code was tested on Waveshare STM32F103C development board. Settings can be found in the STM32CubeMx project (.ioc file), this may help you to port them to another STM32 board with different chip.

## Main points of the code
1.  requires your board go with 8M oscillator (PD0 / PD1).
2.  PA9 / PA10 for TX / RX of UART.
3.  requires a USB port on the board.
-   Almost all of the STM32F103C development boards satisfy the condition.

## Getting Started
1.  Download the firmware to your board. A .hex file was compiled and released for STM32F103C, [click to download](https://github.com/soonuse/stm32_joystick_for_nintendo_switch/releases). You can download it to your STM32F103C board directly for most cases. [STM32CubeProg](https://www.st.com/en/development-tools/stm32cubeprog.html) is used for downloading the .hex to the chip. STM32CubeProg supports multiple OS (Windows, Linux, Mac...). If you are using UART to download it, remember seting the boot0 jumper to HIGH to enable ISP mode. Or you can go with Keil V5 and ST-Link to flash the program. There is no need to set the boot0 to HIGH in this method.
2.  Connect a USB UART serial module between your PC and the PA9 / PA10 pins of your board. The Tx pin of the UART board should be connected to the PA10 (Rx pin of the STM32 chip) and UART's Rx pin to the board's Tx pin. There are many kinds of UART module, FT232 / PL2303 / CP2102 and so on...  they are almost the same at this point.
3.  UART settings: 115200 bauds / 1 stop bit / no parity / no flow control
4.  Just try it by sending serial command:
```
82 00 01 08 04 02 01 00
```
This command tells Switch the key "A" is pressed on the USB console. Then you send this command to release "A":
```
80 00 01 08 04 02 01 00
```
Actually they send a USB HID report to your Switch, just like a common USB Joystick.

## How to send other keys?
Just pressing the key "A" was not enough to control your game console and means nothing. But how to send other keys?

### What's the USB Report
The data sent by your board to Switch is called USB Report, e.g.
```
04 00 08 80  80 80 80 00
```
This report tells Switch the user is press the button A. It's a bytes like object of the USB report struct:
```
typedef struct USB_JoystickReport_Input_t {
  uint16_t Button; // 16 buttons; see JoystickButtons for bit mapping
  uint8_t  HAT;    // HAT switch; one nibble w/ unused nibble
  uint8_t  LX;     // Left  Stick X
  uint8_t  LY;     // Left  Stick Y
  uint8_t  RX;     // Right Stick X
  uint8_t  RY;     // Right Stick Y
  uint8_t  VendorSpec;
} USB_JoystickReport_Input;
```
Meanwhile the buttons:
```
typedef enum {
    SWITCH_Y       = 0x01,
    SWITCH_B       = 0x02,
    SWITCH_A       = 0x04,
    SWITCH_X       = 0x08,
    SWITCH_L       = 0x10,
    SWITCH_R       = 0x20,
    SWITCH_ZL      = 0x40,
    SWITCH_ZR      = 0x80,
    SWITCH_MINUS   = 0x100,
    SWITCH_PLUS    = 0x200,
    SWITCH_LCLICK  = 0x400,
    SWITCH_RCLICK  = 0x800,
    SWITCH_HOME    = 0x1000,
    SWITCH_CAPTURE = 0x2000,
} JoystickButtons;
```
uint16_t means the buttons are expressed using two bytes.

The coresponding USB report is:
-   1nd, 2nd bytes: 04 00 --> SWITCH_A as uint16_t = 0x0004 with little endian --> 04 00
-   3rd byte: 08 --> hat on center
-   4th byte: 80 --> left stick on center (X axis, 0 to 255, 128 the center)
-   5th byte: 80 --> left stick on center (Y axis, 0 to 255, 128 the center)
-   6th byte: 80 --> right stick on center (X axis, 0 to 255, 128 the center)
-   7th byte: 80 --> right stick on center (Y axis, 0 to 255, 128 the center)
-   8th byte: 00 --> specified by the vendor, ignore

i.e.
```
04 00 08 80  80 80 80 00
```
-   To press multiple buttons, you can use the operator "|" to put them together, e.g. for the python examples:
```
report = UsbJoystickReport(buttons=Button.A | Button.B)
```
and for the C/C++:
```
USB_JoystickReport_Input joystick_input;
joystick_input.Button = SWITCH_A | SWITCH_B;
```

### How to convert USB report to the serial data
Then we should convert the USB report to the serial data to input.
It's not the same as the serial data but what's the relation ship of them?
1.  remove the last byte from the USB report
```
04 00 08 80  80 80 80
```
2.  in binary:
```
00000100 00000000 00001000 10000000  10000000 10000000 10000000
```
Split them for each 7 bits, we get:
```
0000010 0000000 0000001 0001000 0000100 0000010 0000001 0000000
```
3.  The first byte | 0x80 to indicate it is the start byte, and for the others add bit 0 as the highest bit.
```
10000010 00000000 00000001 00001000 00000100 00000010 00000001 00000000
```
in hex:
```
82 00 01 08 04 02 01 00
```
## Control with Python scripts
For ease of use, you can write Python Scripts for serial (UART) control.
```
pip3 install pyserial
```
For Example, run the script:
```
python3 Example/spin.py
```
This script rock the left stick forever. In games, your hero will rotate its body.

The line of `port` for serial should be changed according to your serial device name. For Windows user, it seems like COM1, COM2, COM3 ... on Device Manager. For Linux, you can find them by `ls -l /dev | grep ttyUSB`
