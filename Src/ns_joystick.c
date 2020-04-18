#include "ns_joystick.h"

USB_JoystickReport_Input joystick_input;
USB_JoystickReport_Output joystick_output;

void ResetReport(USB_JoystickReport_Input* report) {
  memset(report, 0, sizeof(USB_JoystickReport_Input));
  report->LX = STICK_CENTER;
  report->LY = STICK_CENTER;
  report->RX = STICK_CENTER;
  report->RY = STICK_CENTER;
  report->HAT = HAT_CENTER;
}

uint8_t SendReport(USBD_HandleTypeDef* pdev, USB_JoystickReport_Input* input_data)
{
  uint8_t result = USBD_FAIL;
  result = USBD_HID_SendReport(pdev, (uint8_t*)input_data, sizeof(USB_JoystickReport_Input));
  return result;
}

void HoldReport(USBD_HandleTypeDef* pdev, USB_JoystickReport_Input* const input_data, uint32_t delay_ms)
{
  uint32_t tickstart = HAL_GetTick();
  while ((HAL_GetTick() - tickstart) < delay_ms)
  {
    SendReport(pdev, input_data);
  }
}

/****END OF FILE****/
