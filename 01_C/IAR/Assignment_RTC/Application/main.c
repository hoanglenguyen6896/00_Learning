#include "HAL.h"

/*******************************************************************************
 * Global Variables
*******************************************************************************/
unsigned char led1_on = 3u;     /* Led red on duration */
unsigned char led1_off = 6u;    /* Led red off duration */
unsigned char led2_on = 2u;     /* Led green on duration */
unsigned char led2_off = 1u;    /* Led green off duration */

/*******************************************************************************
 * Main Function
*******************************************************************************/
int main(void)
{
    /* Local Variable defititions*/
    float dPrevTime1 = DEFAULT_TSR;
    float dPrevTime2 = DEFAULT_TSR;
    float dCurrTime;
    uint8_t u8LedRedStatus = LED_IS_ON;
    uint8_t u8LedGreenStatus = LED_IS_ON;
    uint32_t u32TSRValue;
    uint32_t u32TPRValue;

    /* Initialize */
    HAL_vPinInit();
    HAL_vRTCInit();
    RED_LED_ON;
    GREEN_LED_ON;

    while(1)
    {
        u32TSRValue = RTC->TSR;
        u32TPRValue = RTC->TPR & TPR_MASK;
        dCurrTime = (u32TSRValue*DEFAULT_TSR) + (u32TPRValue/LPO_CLK_SOURCE);
        if(((dCurrTime - dPrevTime1) >= (float) led1_on)\
                        && (u8LedRedStatus == LED_IS_ON))
        {
            dPrevTime1 = dCurrTime;
            u8LedRedStatus = LED_IS_OFF;
            RED_LED_OFF;
        }
        else if(((dCurrTime - dPrevTime1) >= (float) led1_off)\
                        && (u8LedRedStatus == LED_IS_OFF))
        {
            dPrevTime1 = dCurrTime;
            u8LedRedStatus = LED_IS_ON;
            RED_LED_ON;
        }
        if(((dCurrTime - dPrevTime2) >= (float) led2_on)\
                        && (u8LedGreenStatus == LED_IS_ON))
        {
            dPrevTime2 = dCurrTime;
            u8LedGreenStatus = LED_IS_OFF;
            GREEN_LED_OFF;
        }
        else if(((dCurrTime - dPrevTime2) >= (float) led2_off)\
                        && (u8LedGreenStatus == LED_IS_OFF))
        {
            dPrevTime2 = dCurrTime;
            u8LedGreenStatus = LED_IS_ON;
            GREEN_LED_ON;
        }
    }
}
