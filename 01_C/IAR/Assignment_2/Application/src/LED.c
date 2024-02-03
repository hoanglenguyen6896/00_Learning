#include "LED.h"

/*******************************************************************************
 * Global variables
*******************************************************************************/
static uint8_t g_s_u8DimBrightness = BRIGHTNESS_0; /* Brightness from 0 - 100 */
static uint8_t g_s_u8DimUp = TRUE;  /* Increase or Decrease brightness */

/*******************************************************************************
 * Function name: LED_vStepLED
 * Function: Bright the LED in step 0 25 50 75 100% (MODE 2A and 2B)
*******************************************************************************/
void LED_vStepLED(uint8_t u8Brightness)
{
    /* Reset state of MODE 1 */
    g_s_u8DimBrightness = BRIGHTNESS_0;
    g_s_u8DimUp = TRUE;
    /* Brightness changes in each step */
    RED_LED_ON;
    HAL_vDelay((DELAY_100US)*(u8Brightness));
    RED_LED_OFF;
    HAL_vDelay((DELAY_100US)*(100 - u8Brightness));
}

/*******************************************************************************
 * Function name: LED_vDimLED
 * Function: Dim the LED from 0 - 100 and 100 - 0 in 2s, 100Hz
*******************************************************************************/
void LED_vDimLED(void)
{
    /* Increase the bightness of LED (DIM) from 0 - 100 */
    if(g_s_u8DimUp == TRUE)
    {
        /* Light the led with the brightness */
        RED_LED_ON;
        HAL_vDelay((DELAY_100US)*(g_s_u8DimBrightness));
        RED_LED_OFF;
        HAL_vDelay((DELAY_100US)*(100 - g_s_u8DimBrightness));

        if(g_s_u8DimBrightness == REVERSE_DIRECTION)
        {
            /* Change to Decrease brightness after reach max brightness */
            g_s_u8DimBrightness = BRIGHTNESS_0;
            g_s_u8DimUp = FALSE;
        }
        else
        {
            (g_s_u8DimBrightness)++;
        }
    }

    /* Decrease the bightness of LED (DIM) 100 - 0 */
    else
    {
        /* Light the led with the brightness */
        RED_LED_OFF;
        HAL_vDelay((DELAY_100US)*(g_s_u8DimBrightness));
        RED_LED_ON;
        HAL_vDelay((DELAY_100US)*(100 - g_s_u8DimBrightness));

        if(g_s_u8DimBrightness == REVERSE_DIRECTION)
        {
            /* Change to Increase brightness after reach min brightness */
            g_s_u8DimBrightness = BRIGHTNESS_0;
            g_s_u8DimUp = TRUE;
        }
        else
        {
            (g_s_u8DimBrightness)++;
        }
    }
}
