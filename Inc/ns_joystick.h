/**
  ******************************************************************************
  * @file           : ns_joystick.h
  * @brief          : Header for ns_joystick.c file.
  *                   This file contains the key codes and report functions.
  ******************************************************************************
  */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __NS_JOYSTICK_H
#define __NS_JOYSTICK_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include "stm32f1xx_hal.h"
#include "usb_device.h"
#include "usbd_hid.h"

extern USBD_HandleTypeDef hUsbDeviceFS;
extern uint8_t USBD_HID_SendReport (
  USBD_HandleTypeDef *pdev, 
  uint8_t *report,
  uint16_t len);

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

#define HAT_TOP          0x00
#define HAT_TOP_RIGHT    0x01
#define HAT_RIGHT        0x02
#define HAT_BOTTOM_RIGHT 0x03
#define HAT_BOTTOM       0x04
#define HAT_BOTTOM_LEFT  0x05
#define HAT_LEFT         0x06
#define HAT_TOP_LEFT     0x07
#define HAT_CENTER       0x08

#define STICK_MIN      0
#define STICK_CENTER 128
#define STICK_MAX    255

typedef struct USB_JoystickReport_Input_t {
  uint16_t Button; // 16 buttons; see JoystickButtons for bit mapping
  uint8_t  HAT;    // HAT switch; one nibble w/ unused nibble
  uint8_t  LX;     // Left  Stick X
  uint8_t  LY;     // Left  Stick Y
  uint8_t  RX;     // Right Stick X
  uint8_t  RY;     // Right Stick Y
  uint8_t  VendorSpec;
} USB_JoystickReport_Input;

typedef struct USB_JoystickReport_Output_t {
  uint16_t Button; // 16 buttons; see JoystickButtons for bit mapping
  uint8_t  HAT;    // HAT switch; one nibble w/ unused nibble
  uint8_t  LX;     // Left  Stick X
  uint8_t  LY;     // Left  Stick Y
  uint8_t  RX;     // Right Stick X
  uint8_t  RY;     // Right Stick Y
} USB_JoystickReport_Output;

extern USB_JoystickReport_Input joystick_input_data;
extern USB_JoystickReport_Output joystick_output_data;

void ResetReport(USB_JoystickReport_Input* report);
uint8_t SendReport(USBD_HandleTypeDef* pdev, USB_JoystickReport_Input* const input_data);
void HoldReport(USBD_HandleTypeDef* pdev, USB_JoystickReport_Input* const input_data, uint32_t tick);


#ifdef __cplusplus
}
#endif

#endif /* __NS_JOYSTICK_H */

/****END OF FILE****/
