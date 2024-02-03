#include "HAL.h"

/*******************************************************************************
 * Global Variables
*******************************************************************************/
volatile static uint16_t s_u16RedToggleCount = 0u;   /* Counter for red LED */
volatile static uint16_t s_u16GreenToggleCount = 0u; /* Counter for green LED */

/*******************************************************************************
 * Main Function
*******************************************************************************/
int main(void)
{
    uint8_t u8SystickError; /* Check error Systick parameter variable */
    HAL_vPinInit(); /* Init GPIO */
    u8SystickError = HAL_vSysConfig(SYSTICK_COUNT_1MS); /* HAL_vSysConfig */
    /* Checking error parameter */
    if(u8SystickError == 1)
    {
        while(1); /* Hang program here */
    }

    while(1)
    {
        /* Toggle red LED each 1s */
        if(s_u16RedToggleCount == RED_TOGGLE_CYCLE)
        {
            RED_LED_TOGGLE;
            s_u16RedToggleCount = 0;
        }
        /* Toggle green LED each 1/6s */
        if(s_u16GreenToggleCount == GREEN_TOGGLE_CYCLE)
        {
            GREEN_LED_TOGGLE;
            s_u16GreenToggleCount = 0;
        }
    }
}

/*******************************************************************************
 * Exception Handler
*******************************************************************************/

/*******************************************************************************
 * Function name: SysTick_Handler
 * Funtion: Handle Systick Exception
*******************************************************************************/
void SysTick_Handler()
{
    /* Increase counter of LEDs when exception occurs */
    s_u16RedToggleCount++;
    s_u16GreenToggleCount++;
}
