#include "HAL.h"

/*******************************************************************************
 * Function name: INIT_vInitLed
 * Function: Config pin
*******************************************************************************/
void HAL_vInit(void)
{
    /* Enable clock for PORTC, PORTD, PORTE */
    SIM->SCGC5 |= (CLOCKC_ENABLE);
    SIM->SCGC5 |= (CLOCKD_ENABLE);
    SIM->SCGC5 |= (CLOCKE_ENABLE);

    /* Configure multiplex of PTE29 as GPIO */
    PORTE->PCR[29] |= (1 << 8);
    /* Configure multiplex of PTC3 and PTC12 as GPIO */
    PORTC->PCR[3] |= (1 << 8);
    PORTC->PCR[12] |= (1 << 8);

    /* Configure PTE29 as output */
    GPIOE->PDDR |= (1 << 29);

    /* Configure PTC3 and PTC12 as input */
    GPIOC->PDDR &= (~(1 << 3));
    GPIOC->PDDR &= (~(1 << 12));

    /* Enable pull on PTC3 and PTC12 */
    PORTC->PCR[3] |= (1 << 1);
    PORTC->PCR[12] |= (1 << 1);

    /* Configure PTC3 and PTC12 as pull-up */
    PORTC->PCR[3] |= (1);
    PORTC->PCR[12] |= (1);
}

/*******************************************************************************
 * Function name: INIT_vDelay
 * Function: Create delay
*******************************************************************************/
void HAL_vDelay(uint32_t u32DelayCount)
{
    unsigned long i;

    for (i = 0; i < u32DelayCount; i++)
    {
        __asm("nop");
    }
}
