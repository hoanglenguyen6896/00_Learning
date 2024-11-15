#include "LED.h"

/*******************************************************************************
 * Function name: LED_vBlinkAlternate
 * Function: Blink 2 led Alternate
*******************************************************************************/
void LED_vBlinkAlternate( void * pvParameters )
{
    while(1)
    {
        RED_LED_ON;
        //GREEN_LED_OFF;
        vTaskDelay( pdMS_TO_TICKS( 250 ) );
        RED_LED_OFF;
        //GREEN_LED_ON;
        vTaskDelay( pdMS_TO_TICKS( 650 ) );
    }
}

/*******************************************************************************
 * Function name: LED_vDimLED
 * Function: Dim 2 led Alternate
*******************************************************************************/
void LED_vDimLED(uint8_t u8DutyCycle)
{
    int16_t i = 0;

    for(i = 0; i <= 100; i+=2)
    {
        RED_LED_ON;
        GREEN_LED_OFF;
        INIT_vDelay(i*(DELAY_1S/(DIM_FREQ*u8DutyCycle)));
        RED_LED_OFF;
        GREEN_LED_ON;
        INIT_vDelay((100-i)*(DELAY_1S/(DIM_FREQ*u8DutyCycle)));
    }
    for(i = 100; i >= 1; i-=2)
    {
        RED_LED_ON;
        GREEN_LED_OFF;
        INIT_vDelay(i*(DELAY_1S/(DIM_FREQ*u8DutyCycle)));
        RED_LED_OFF;
        GREEN_LED_ON;
        INIT_vDelay((100-i)*(DELAY_1S/(DIM_FREQ*u8DutyCycle)));
    }
}
