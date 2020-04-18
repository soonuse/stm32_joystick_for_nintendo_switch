# stm32_joystick_for_nintendo_switch
STM32 Joystick for Nintendo Switch

I am also a Nintendo big fan outside of working hours. I tried to play switch games by my PC. There are many ways to do such things.  Using Arduino/Teensy is a good choice. But for me, porting the joystick USB driver to a STM32 development board is also a nice game, faster and more stable. With serial (UART) control function I can play my Switch using the PC.

This program allows you to control your Nintendo switch through the serial port using an STM32 development board, which means that you can control your switch just like using your PC.

This code was tested on Waveshare STM32F103C development board. Settings can be found in the STM32CubeMx project (.ioc file), this may help you to port them to another STM32 board with different chip.

![image](https://github.com/soonuse/stm32_joystick_for_nintendo_switch/blob/master/Examples/example_spin.gif)

## Main points of the code
1.  requires your board go with 8M oscillator (PD0 / PD1).
2.  PA9 / PA10 for TX / RX of UART.
3.  requires a USB port on the board.

## Getting Started
1.  A .hex file is compiled and released for STM32F103C. You can download it to your STM32F103C board directly for most cases. [STM32CubeProg](https://www.st.com/en/development-tools/stm32cubeprog.html) is a good choice for downloading the .hex to the chip (if you are using UART to download it, remember seting the boot0 jumper to HIGH to enable ISP mode). Or you can go with Keil V5 and ST-Link to flash the program (there is no need to set the boot0 to HIGH by this way).
2.  Connect a USB UART serial module between your PC and the PA9 / PA10 pins of your board. The Tx pin of the UART board should be connected to the PA10 (Rx pin of the STM32 chip) and UART's Rx pin to the board's Tx pin. There are many choices of UART module, FT232 / PL2303 / CP2102 and so on...
3.  UART settings: 115200 bauds / 1 stop bit / no parity / no flow control
4.  Just try it by sending serial command:
```
88  04 00 08 80  80 80 80 00
```
This command tells Switch the key "A" is pressed on the USB console. Then you send this command to release "A":
```
88  00 00 08 80  80 80 80 00
```
Actually they send a USB HID report to your Switch, just like a common USB Joystick.

## How to send other keys?
Just pressing the key "A" was not enough to control your game console and means nothing. But how to send other keys?

### What's the USB Report
The data sent by your board to Switch is called USB Report, e.g.
```
04 00 08 80  80 80 80 00
```
The only difference between USB report and the serial data is the leading byte 0x88.  For simplicity, we also called the data sent from your PC (to your board)  as report. Like:
```
88  04 00 08 80  80 80 80 00
```

The first byte 88 is the leading byte, of which binary bits are set as 10001000. The first bit tells the board this byte indicates the length of the HID report but not the data. Of this example, the length of report is 8.

In fact, all report sent to the switch is always 8 bytes. But for other game pad or other console, the lenth of report is not fixed. For example, if the leading byte is 0x89, the number of following bytes is 9 (binary 1001), and the board will send 9 bytes as a USB report. If the leading byte is 0xFF, the number of following bytes is 127 (binary 111 1111). For Nintendo Switch, you can just send 0x88 as the leading byte.

Then, how do the following bytes composed to a USB report? See the file `ns_joystick.h`:
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
uint16_t means the buttons use two bytes to be expressed.

If you want to press multiple buttons "A" "B" "MINUS" "PLUS", you can send:
-   1st byte: 88 --> leading byte, fixed to 0x88 for Nintendo Switch due to the size of report is always 8.
-   2nd, 3rd bytes: 06 03 --> SWITCH_A | SWITCH_B | SWITCH_MINUS | SWITCH_PLUS = 0x0306 with little endian --> 06 03
-   4th byte: 08 --> hat on center (byte reserved)
-   5th byte: 80 --> left stick on center (X axis, 0 to 255, 128 the center)
-   6th byte: 80 --> left stick on center (Y axis, 0 to 255, 128 the center)
-   7th byte: 80 --> right stick on center (X axis, 0 to 255, 128 the center)
-   8th byte: 80 --> right stick on center (Y axis, 0 to 255, 128 the center)
-   9th byte: 00 --> ignore
i.e.
```
88  06 03 08 80  80 80 80 00
```
