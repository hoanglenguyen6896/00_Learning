#include "HAL.h"

/*******************************************************************************
 * Function name: INIT_vInitLed
 * Function: Config pin
*******************************************************************************/
void HAL_vInit(void)
{
    /* Enable clock for PORTC, PORTD, PORTE */
    SIM->SCGC5 |= (CLOCKD_ENABLE);
    SIM->SCGC5 |= (CLOCKE_ENABLE);

    /* Configure multiplex of PTD5, PTE29 as GPIO */
    PORTD->PCR[5] |= (1 << 8);
    PORTE->PCR[29] |= (1 << 8);

    /* Configure PTD5, PTE29 as output */
    GPIOD->PDDR |= (1 << 5);
    GPIOE->PDDR |= (1 << 29);

    GPIOD->PSOR |= (1 << 29);
    GPIOE->PSOR |= (1 << 5);
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
