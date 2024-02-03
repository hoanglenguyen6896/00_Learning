/*INCLUDE***********************************************************************
 *
*END***************************************************************************/
#include "FreeRTOS.h"
#include "task.h"

#include "LED.h"

void vTaskBlinGreenkLed( void * pvParameters )
{
  while (1)
  {
    GREEN_LED_ON;
    vTaskDelay( pdMS_TO_TICKS( 20 ) );
    GREEN_LED_OFF;
    vTaskDelay( pdMS_TO_TICKS( 80 ) );
  }
}

void vTaskBlinRedkLed( void * pvParameters )
{
  while (1)
  {
    RED_LED_ON;
    vTaskDelay( pdMS_TO_TICKS( 250 ) );
    RED_LED_OFF;
    vTaskDelay( pdMS_TO_TICKS( 650 ) );
  }
}


/*FUNCTION**********************************************************************
 *
 * -Name : Main
 * -Description : ham thuc thi cua chuong trinh
 *
*END***************************************************************************/
int main(void)
{
  TaskHandle_t xHandleBlinkTaks;
  
  LED_vInitLed();
  
  /* enable global interrupt */
  //asm("cpsie i");
  
  xTaskCreate( vTaskBlinGreenkLed,
               "Blink Led",
               configMINIMAL_STACK_SIZE,
               NULL,
               1,
               &xHandleBlinkTaks);
  xTaskCreate( vTaskBlinRedkLed,
               "Blink Led",
               configMINIMAL_STACK_SIZE,
               NULL,
               1,
               &xHandleBlinkTaks);
  /* Start the scheduler. */
  vTaskStartScheduler();
  
  while(1);
  return 0;
}


void vApplicationGetIdleTaskMemory( StaticTask_t ** ppxIdleTaskTCBBuffer,
                                               StackType_t ** ppxIdleTaskStackBuffer,
                                               uint32_t * pulIdleTaskStackSize )
{
}

void vApplicationGetTimerTaskMemory( StaticTask_t ** ppxTimerTaskTCBBuffer,
                                          StackType_t ** ppxTimerTaskStackBuffer,
                                              uint32_t * pulTimerTaskStackSize )
{
}


void vAssertCalled( const char *pcFile, uint32_t ulLine )
{
}
/* *****************************************************************************
 * EOF
 ******************************************************************************/