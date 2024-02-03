/*INCLUDE***********************************************************************
 *
*END***************************************************************************/
#include "LED.h"
/*FUNCTION PROPOTYPE************************************************************
 *
*END***************************************************************************/
static void LED_s_vDimLedPwm(uint8_t DutyCycle);
static void LED_s_vDelay(uint32_t temp);
/*FUNCTION**********************************************************************
 *
 * -Name : initLed
 * -Description : ham config clock va GPIO
 *
*END***************************************************************************/
void LED_vInitLed()
{
    /* Enable clock for PORTD, PORTE */
    SIM->SCGC5 |= (1 << 12);    /* Set bit 12 */
    SIM->SCGC5 |= (1 << 13);    /* Set bit 13 */
    
    /* Configure multiplex of PTD5 and PTE29 as GPIO */
    PORTD->PCR[5] |= PORT_PCR_MUX(1);
    PORTE->PCR[29] |= PORT_PCR_MUX(1);
    
    /* Configure PTD5 and PTE29 as output */
    GPIOD->PDDR |= (1 << 5);
    GPIOE->PDDR |= (1 << 29);
}
/*FUNCTION**********************************************************************
 *
 * -Name : LED_s_vDimLedPwm
 * -Description : control led sang DutyCycle percent
 *
*END***************************************************************************/
static void LED_s_vDimLedPwm(uint8_t DutyCycle)
{
    RED_LED_ON;
    GREEN_LED_OFF;
    LED_s_vDelay(DutyCycle);/*  */
    RED_LED_OFF;
    GREEN_LED_ON;
    LED_s_vDelay(DUTY_CYCLE_MAX - DutyCycle);
}
/*FUNCTION**********************************************************************
 *
 * -Name : LED_s_vDelay
 * -Description : ham delay temp*100 microsecond
 *
*END***************************************************************************/
static void LED_s_vDelay(uint32_t temp)
{
    uint32_t count = temp * DELAY_COUNT;
    uint32_t i;
    
    for (i = 0; i < count; i++)
    {
        __asm("nop");
    }
}
/*FUNCTION**********************************************************************
 *
 * -Name : LED_mode1
 * -Description : ham thuc hien link led voi tan so 2hz
 *
*END***************************************************************************/
void LED_vMode1()
{
    RED_LED_ON;
    GREEN_LED_OFF;
    LED_s_vDelay(SECOND_MODE_1);/* 0.25s */
    GREEN_LED_ON;
    RED_LED_OFF;
    LED_s_vDelay(SECOND_MODE_1);/* 0.25 */
}
/*FUNCTION**********************************************************************
 *
 * -Name : LED_mode2
 * -Description : ham dim led voi tan so 1hz
 *
*END***************************************************************************/
void LED_vMode2()
{
    int8_t i;
    
    for(i = DUTY_CYCLE_MIN; i <= DUTY_CYCLE_MAX; i += 2)
    {
        LED_s_vDimLedPwm(i);
    }
    for(i = DUTY_CYCLE_MAX; i >= DUTY_CYCLE_MIN; i -= 2)
    {
        LED_s_vDimLedPwm(i);
    }
}
/* *****************************************************************************
 * EOF
 ******************************************************************************/