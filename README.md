# stm32_joystick_for_nintendo_switch
STM32 Joystick for Nintendo Switch

I am also a Nintendo big fan outside of working hours. I tried to play switch games by my PC. There are many ways to do such things.  Using Arduino/Teensy is a good choice. But for me, porting the joystick USB driver to a STM32 development board is also a nice game, faster and more stable. With serial (UART) control function I can play my Switch using the PC.

This program allows you to control your Nintendo switch through the serial port using an STM32 development board, which means that you can control your switch just like using your PC.

This code was tested on Waveshare STM32F103C development board. Settings can be found in the STM32CubeMx project (.ioc file), this may help you to port them to another STM32 board with different chip.

Main points of the code:
1.  requires your board go with 8M oscillator (PD0 / PD1).
2.  PA9 / PA10 for TX / RX of UART.
3.  requires a USB port on the board.

## Getting Started
1.  A .hex file is released for STM32F103C. You can download it to your board directly for most cases. For Windows user, [Flash Loader Demonstrator](https://www.st.com/en/development-tools/flasher-stm32.html) is a good choice for downloading the .hex to the chip (remember set the boot0 jumper to HIGH to enable ISP mode). Or you can go with Keil V5 and ST-Link to flash the program (there is no need to set the boot0 to HIGH by this way).
