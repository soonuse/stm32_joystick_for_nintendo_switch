# stm32_joystick_for_nintendo_switch
STM32 Joystick for Nintendo Switch

I am also a Nintendo big fan outside of working hours. I tried to play switch games by my PC. There are many ways to do such things.  Using Arduino/Teensy is a good choice. But for me, porting the joystick USB driver to a STM32 development board is also a nice game, faster and more stable. With serial (UART) control function I can play my Switch using the PC.

This program allows you to control your Nintendo switch through the serial port using an STM32 development board, which means that you can control your switch just like using your PC.

This code was tested on Waveshare STM32F103C development board. Settings can be found in the STM32CubeMx project (.ioc file), this may help you to port them to another STM32 board with different chip.

## Main points of the code
1.  requires your board go with 8M oscillator (PD0 / PD1).
2.  PA9 / PA10 for TX / RX of UART.
3.  requires a USB port on the board.

## Getting Started
1.  A .hex file is released for STM32F103C. You can download it to your STM32F103C board directly for most cases. [STM32CubeProg](https://www.st.com/en/development-tools/stm32cubeprog.html) is a good choice for downloading the .hex to the chip (if you are using UART to download it, remember seting the boot0 jumper to HIGH to enable ISP mode). Or you can go with Keil V5 and ST-Link to flash the program (there is no need to set the boot0 to HIGH by this way).
2.  Connect a USB UART serial module between your PC and the PA9 / PA10 pins of your board. The Tx pin of the UART board should be connected to the PA10 (Rx pin of the STM32 chip) and UART's Rx pin to the board's Tx pin. There are many choices of UART module, FT232 / PL2303 / CP2102 and so on...
3.  UART settings: 115200 bauds / 1 stop bit / no parity / no flow control
4.  Just try it by sending serial command:
```
88 04 00 08 80  80 80 80 00
```
This command tells Switch the key "A" is pressed on the USB console. Then you send this command to release "A":
```
88 00 00 08 80  80 80 80 00
```
