#include "INIT.h"

/*******************************************************************************
 * Function name: INIT_vInitLed
 * Function: Config pin
*******************************************************************************/
void INIT_vInitLed()
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

    /* Clear PTD5 and PTE29 */
    RED_LED_ON;
    GREEN_LED_ON;
}

/*******************************************************************************
 * Function name: INIT_vDelay
 * Function: Create delay
*******************************************************************************/
void INIT_vDelay(uint32_t u32DelayCount)
{
    unsigned long i;

    for (i = 0; i < u32DelayCount; i++)
    {
        __asm("nop");
    }
}
