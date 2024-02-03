#include "BUTTON.h"

/*******************************************************************************
 * Global variables
*******************************************************************************/
/* Variable check for SW1 */
static uint8_t g_s_u8ButOld1 = RELEASE;
static uint8_t g_s_u8But1 = RELEASE;

/* Variable check for SW2 */
static uint8_t g_s_u8ButOld2 = RELEASE;
static uint8_t g_s_u8But2 = RELEASE;

/* Get status of SW1 */
static uint8_t g_s_u8Status1 = MODE_1;

/*******************************************************************************
 * Function name: BUTTON_u8CheckButton2
 * Function: Light LED in step SW2 (PORTC_PIN12) status to change to mode 2A
*******************************************************************************/
void BUTTON_vCheckButtonMode1(uint8_t* u8Brightness, uint8_t *u8Status2)
{
    /* Dim LED */
    LED_vDimLED();

    /* Check if SW was pressed to change to mode 2A */
    g_s_u8But2 = BUTTON_2_STATUS; /* Get status of SW2 */

    /* If SW2 was pressed */
    if((g_s_u8But2 == PRESS) && (g_s_u8ButOld2 == RELEASE))
    {
        *u8Brightness = BRIGHTNESS_0;
        *u8Status2 = !*u8Status2;
        g_s_u8ButOld2 = PRESS;
    }
    /* If SW2 was released */
    else if ((g_s_u8But2 == RELEASE) && (g_s_u8ButOld2 == PRESS))
    {
        g_s_u8ButOld2 = RELEASE;
    }
}

/*******************************************************************************
 * Function name: BUTTON_u8CheckButton1Up
 * Function: Get button 1 (PORTC_PIN3) status to increased the brightness
*******************************************************************************/
void BUTTON_vCheckButtonMode2A(uint8_t* u8Brightness, uint8_t *u8Status2)
{
    /* Light the LED with brightness in step */
    LED_vStepLED(*u8Brightness);

    g_s_u8But1 = BUTTON_1_STATUS; /* Get status of SW1 */

    /* If SW1 was pressed */
    if((g_s_u8But1 == PRESS) && (g_s_u8ButOld1 == RELEASE))
    {
        g_s_u8Status1 = PERFORM_CHANGE_BRIGHTNESS;
        g_s_u8ButOld1 = PRESS;
    }
    /* If SW1 was released */
    else if ((g_s_u8But1 == RELEASE) && (g_s_u8ButOld1 == PRESS))
    {
        g_s_u8ButOld1 = RELEASE;
        g_s_u8Status1 = DONOT_CHANGE_BRIGHTNESS;
    }

    /* Increase brightness if SW1 was pressed */
    if(g_s_u8Status1 == PERFORM_CHANGE_BRIGHTNESS)
    {
        if(*u8Brightness < BRIGHTNESS_100)
        {
            *u8Brightness += STEP_BRIGHTNESS;
            g_s_u8Status1 = DONOT_CHANGE_BRIGHTNESS;
        }
        /* Change to mode 2B if SW1 was pressed and brightness is 100 */
        else
        {
            *u8Brightness = BRIGHTNESS_100;
            g_s_u8Status1 = PERFORM_CHANGE_BRIGHTNESS;
            *u8Status2 = MODE_2B;
        }
    }

    /* Check if SW was pressed to change to mode 1 */
    g_s_u8But2 = BUTTON_2_STATUS; /* Get status of SW2 */

    /* If SW2 was pressed return Mode 1*/
    if((g_s_u8But2 == PRESS) && (g_s_u8ButOld2 == RELEASE))
    {
        *u8Brightness = BRIGHTNESS_0;
        *u8Status2 = MODE_1;
        g_s_u8ButOld2 = PRESS;
    }
    /* If SW2 was released */
    else if ((g_s_u8But2 == RELEASE) && (g_s_u8ButOld2 == PRESS))
    {
        g_s_u8ButOld2 = RELEASE;
    }
}

/*******************************************************************************
 * Function name: BUTTON_u8CheckButton1Down
 * Function: Get button 1 (PORTC_PIN3) status to decreased the brightness
*******************************************************************************/
void BUTTON_vCheckButtonMode2B(uint8_t* u8Brightness, uint8_t *u8Status2)
{
    /* Light the LED with brightness in step */
    LED_vStepLED(*u8Brightness);

    g_s_u8But1 = BUTTON_1_STATUS; /* Get status of SW1 */

    /* If SW1 was pressed */
    if((g_s_u8But1 == PRESS) && (g_s_u8ButOld1 == RELEASE))
    {
        g_s_u8Status1 = PERFORM_CHANGE_BRIGHTNESS;
        g_s_u8ButOld1 = PRESS;
    }
    /* If SW1 was released */
    else if ((g_s_u8But1 == RELEASE) && (g_s_u8ButOld1 == PRESS))
    {
        g_s_u8ButOld1 = RELEASE;
        g_s_u8Status1 = DONOT_CHANGE_BRIGHTNESS;
    }

    if(g_s_u8Status1 == PERFORM_CHANGE_BRIGHTNESS)
    {
         /* Decrease brightness if SW1 was pressed */
        if(*u8Brightness > BRIGHTNESS_0)
        {
            *u8Brightness -= STEP_BRIGHTNESS;
            g_s_u8Status1 = DONOT_CHANGE_BRIGHTNESS;
        }
        /* Change to mode 2A if SW1 was pressed and brightness is 0 */
        else
        {
            *u8Brightness = BRIGHTNESS_0;
            g_s_u8Status1 = PERFORM_CHANGE_BRIGHTNESS;
            *u8Status2 = MODE_2A;
        }
    }

    /* Check if SW was pressed to change to mode 1 */
    g_s_u8But2 = BUTTON_2_STATUS; /* Get status of SW2 */

    /* If SW2 was pressed return Mode 1*/
    if((g_s_u8But2 == PRESS) && (g_s_u8ButOld2 == RELEASE))
    {
        *u8Brightness = BRIGHTNESS_0;
        *u8Status2 = MODE_1;
        g_s_u8ButOld2 = PRESS;
    }
    /* If SW2 was released */
    else if ((g_s_u8But2 == RELEASE) && (g_s_u8ButOld2 == PRESS))
    {
        g_s_u8ButOld2 = RELEASE;
    }
}
